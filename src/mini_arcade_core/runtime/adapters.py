"""
Module providing runtime adapters for window and scene management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional
from venv import logger

from PIL import Image

from mini_arcade_core.backend import Backend, Event, EventType
from mini_arcade_core.keymaps import Key
from mini_arcade_core.runtime.input_frame import InputFrame
from mini_arcade_core.runtime.services import (
    AudioPort,
    CapturePort,
    FilePort,
    InputPort,
    SceneEntry,
    ScenePolicy,
    ScenePort,
    WindowPort,
)
from mini_arcade_core.scenes.registry import SceneRegistry

if TYPE_CHECKING:  # avoid runtime circular import
    from mini_arcade_core.game import Game
    from mini_arcade_core.scenes import Scene


@dataclass
class _StackItem:
    entry: SceneEntry


class WindowAdapter(WindowPort):
    """
    Manages multiple game windows (not implemented).
    """

    def __init__(self, backend):
        self.backend = backend

    def set_window_size(self, width, height):
        self.backend.init(width, height)

    def set_title(self, title: str):
        self.backend.set_window_title(title)

    def set_clear_color(self, r: int, g: int, b: int):
        self.backend.set_clear_color(r, g, b)


class SceneAdapter(ScenePort):
    """
    Manages multiple scenes (not implemented).
    """

    def __init__(self, registry: SceneRegistry, game: Game):
        self._registry = registry
        self._stack: List[_StackItem] = []
        self._game = game

    @property
    def current_scene(self) -> "Scene | None":
        return self._stack[-1].entry.scene if self._stack else None

    @property
    def visible_stack(self) -> list["Scene"]:
        return [e.scene for e in self.visible_entries()]

    def change(self, scene_id: str):
        self.clean()
        self.push(scene_id, as_overlay=False)

    def push(
        self,
        scene_id: str,
        *,
        as_overlay: bool = False,
        policy: ScenePolicy | None = None,
    ):
        # default policy based on overlay vs base
        if policy is None:
            # base scenes: do not block anything by default
            policy = ScenePolicy()
        scene = self._registry.create(
            scene_id, self._game
        )  # or whatever your factory call is
        scene.on_enter()

        entry = SceneEntry(
            scene_id=scene_id,
            scene=scene,
            is_overlay=as_overlay,
            policy=policy,
        )
        self._stack.append(_StackItem(entry=entry))

    def pop(self):
        if not self._stack:
            return
        item = self._stack.pop()
        item.entry.scene.on_exit()

    def clean(self):
        while self._stack:
            self.pop()

    def quit(self):
        self._game.quit()

    def visible_entries(self) -> list[SceneEntry]:
        entries = [i.entry for i in self._stack]
        # find highest opaque from top down; render starting there
        for idx in range(len(entries) - 1, -1, -1):
            if entries[idx].policy.is_opaque:
                return entries[idx:]
        return entries

    def update_entries(self) -> list[SceneEntry]:
        vis = self.visible_entries()
        if not vis:
            return []
        out: list[SceneEntry] = []
        for entry in reversed(vis):  # top->down
            out.append(entry)
            if entry.policy.blocks_update:
                break
        return list(reversed(out))  # bottom->top order

    def input_entry(self) -> SceneEntry | None:
        vis = self.visible_entries()
        return vis[-1] if vis else None


class NullAudioAdapter(AudioPort):
    """A no-op audio adapter."""

    def play(self, sound_id: str): ...


class LocalFilesAdapter(FilePort):
    """Adapter for local file operations."""

    def write_text(self, path: str, text: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def write_bytes(self, path: str, data: bytes):
        with open(path, "wb") as f:
            f.write(data)


@dataclass
class CapturePathBuilder:
    """
    Helper to build file paths for captured screenshots.

    :ivar directory (str): Directory to save screenshots in.
    :ivar prefix (str): Prefix for screenshot filenames.
    :ivar ext (str): File extension/format for screenshots.
    """

    directory: str = "screenshots"
    prefix: str = ""
    ext: str = "png"  # final output format

    def build(self, label: str) -> Path:
        """
        Build a file path for a screenshot with the given label.

        :param label: Label to include in the filename.
        :type label: str

        :return: Full path for the screenshot file.
        :rtype: Path
        """
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_label = "".join(
            c if c.isalnum() or c in ("-", "_") else "_" for c in label
        )
        name = f"{self.prefix}{stamp}_{safe_label}.{self.ext}"
        return Path(self.directory) / name


class CaptureAdapter(CapturePort):
    """Adapter for capturing frames."""

    def __init__(
        self,
        backend: Backend,
        path_builder: Optional[CapturePathBuilder] = None,
    ):
        self.backend = backend
        self.path_builder = path_builder or CapturePathBuilder()

    def _bmp_to_image(self, bmp_path: str, out_path: str):
        img = Image.open(bmp_path)
        img.save(out_path)

    def screenshot(self, label: str | None = None) -> str:
        label = label or "shot"
        out_path = self.path_builder.build(label)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # If backend only saves BMP, capture to a temp bmp next to output
        bmp_path = out_path.with_suffix(".bmp")

        self.backend.capture_frame(str(bmp_path))
        if not bmp_path.exists():
            raise RuntimeError("Backend capture_frame did not create BMP file")

        self._bmp_to_image(str(bmp_path), str(out_path))
        try:
            bmp_path.unlink(missing_ok=True)
        # Justification: Various exceptions can occur on file deletion
        # pylint: disable=broad-exception-caught
        except Exception:
            logger.warning(f"Failed to delete temporary BMP file: {bmp_path}")
        # pylint: enable=broad-exception-caught

        return str(out_path)

    def screenshot_bytes(self) -> bytes:
        data = self.backend.capture_frame(path=None)
        if data is None:
            raise RuntimeError("Backend returned None for screenshot_bytes()")
        return data


@dataclass
class InputAdapter(InputPort):
    """Adapter for processing input events."""

    _down: set[Key] = field(default_factory=set)

    def build(
        self, events: list[Event], frame_index: int, dt: float
    ) -> InputFrame:
        pressed: set[Key] = set()
        released: set[Key] = set()
        quit_req = False

        for ev in events:
            if ev.type == EventType.QUIT:
                quit_req = True

            elif ev.type == EventType.KEYDOWN and ev.key is not None:
                if ev.key not in self._down:
                    pressed.add(ev.key)
                self._down.add(ev.key)

            elif ev.type == EventType.KEYUP and ev.key is not None:
                if ev.key in self._down:
                    self._down.remove(ev.key)
                released.add(ev.key)

        return InputFrame(
            frame_index=frame_index,
            dt=dt,
            keys_down=frozenset(self._down),
            keys_pressed=frozenset(pressed),
            keys_released=frozenset(released),
            quit=quit_req,
        )

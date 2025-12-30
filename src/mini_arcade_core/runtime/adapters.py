"""
Module providing runtime adapters for window and scene management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional
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
    ScenePort,
    WindowPort,
)
from mini_arcade_core.scenes.registry import SceneRegistry

if TYPE_CHECKING:  # avoid runtime circular import
    from mini_arcade_core.game import Game
    from mini_arcade_core.scenes import Scene


@dataclass
class _StackEntry:
    scene: "Scene"
    as_overlay: bool = False


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
        self.registry = registry
        self._scene_stack: list[_StackEntry] = []
        self.game = game

    @property
    def current_scene(self) -> "Scene | None":
        return self._scene_stack[-1].scene if self._scene_stack else None

    @property
    def visible_stack(self) -> list["Scene"]:
        if not self._scene_stack:
            return []

        # find top-most base scene (as_overlay=False)
        base_idx = 0
        for i in range(len(self._scene_stack) - 1, -1, -1):
            if not self._scene_stack[i].as_overlay:
                base_idx = i
                break

        return [e.scene for e in self._scene_stack[base_idx:]]

    def change(self, scene_id: str):
        scene = self._resolve_scene(scene_id)

        while self._scene_stack:
            entry = self._scene_stack.pop()
            entry.scene.on_exit()

        self._scene_stack.append(_StackEntry(scene=scene, as_overlay=False))
        scene.on_enter()

    def push(self, scene_id: str, *, as_overlay: bool = False):
        scene = self._resolve_scene(scene_id)

        top = self.current_scene
        if top is not None:
            top.on_pause()

        self._scene_stack.append(
            _StackEntry(scene=scene, as_overlay=as_overlay)
        )
        scene.on_enter()

    def pop(self) -> "Scene | None":
        if not self._scene_stack:
            return None

        popped = self._scene_stack.pop()
        popped.scene.on_exit()

        top = self.current_scene
        if top is None:
            self.game.quit()
            return popped.scene

        top.on_resume()
        return popped.scene

    def clean(self):
        while self._scene_stack:
            entry = self._scene_stack.pop()
            entry.scene.on_exit()

    def quit(self):
        self.game.quit()

    def _resolve_scene(self, scene_id: str) -> "Scene":
        return self.registry.create(scene_id, self.game)


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

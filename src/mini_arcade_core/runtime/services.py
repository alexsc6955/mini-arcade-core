from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


class WindowPort(Protocol):
    def set_window_size(self, width: int, height: int) -> None: ...
    def set_title(self, title: str) -> None: ...
    def set_clear_color(self, r: int, g: int, b: int) -> None: ...


class ScenePort(Protocol):
    def change(self, scene_id: str) -> None: ...
    def push(self, scene_id: str, *, as_overlay: bool = False) -> None: ...
    def pop(self) -> None: ...


class AudioPort(Protocol):
    def play(self, sound_id: str) -> None: ...


class FilePort(Protocol):
    def write_bytes(self, path: str, data: bytes) -> None: ...
    def write_text(self, path: str, text: str) -> None: ...


@dataclass
class RuntimeServices:
    window: Optional[WindowPort] = None
    scenes: Optional[ScenePort] = None
    audio: Optional[AudioPort] = None
    files: Optional[FilePort] = None

"""
Service interfaces for runtime components.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


class WindowPort(Protocol):
    """Interface for window-related operations."""

    def set_window_size(self, width: int, height: int):
        """
        Set the size of the window.

        :param width: Width in pixels.
        :type width: int

        :param height: Height in pixels.
        :type height: int
        """

    def set_title(self, title: str):
        """
        Set the window title.

        :param title: The new title for the window.
        :type title: str
        """

    def set_clear_color(self, r: int, g: int, b: int):
        """
        Set the clear color for the window.

        :param r: Red component (0-255).
        :type r: int

        :param g: Green component (0-255).
        :type g: int

        :param b: Blue component (0-255).
        :type b: int
        """


class ScenePort(Protocol):
    """Interface for scene management operations."""

    def change(self, scene_id: str):
        """
        Change the current scene to the specified scene.

        :param scene_id: Identifier of the scene to switch to.
        :type scene_id: str
        """

    def push(self, scene_id: str, *, as_overlay: bool = False):
        """
        Push a new scene onto the scene stack.

        :param scene_id: Identifier of the scene to push.
        :type scene_id: str

        :param as_overlay: Whether to push the scene as an overlay.
        :type as_overlay: bool
        """

    def pop(self):
        """
        Pop the current scene from the scene stack.
        """


class AudioPort(Protocol):
    """Interface for audio playback operations."""

    def play(self, sound_id: str):
        """
        Play the specified sound.

        :param sound_id: Identifier of the sound to play.
        :type sound_id: str
        """


class FilePort(Protocol):
    """Interface for file operations."""

    def write_bytes(self, path: str, data: bytes):
        """
        Write bytes to a file.

        :param path: Path to the file.
        :type path: str

        :param data: Data to write.
        :type data: bytes
        """

    def write_text(self, path: str, text: str):
        """
        Write text to a file.

        :param path: Path to the file.
        :type path: str

        :param text: Text to write.
        :type text: str
        """


@dataclass
class RuntimeServices:
    """
    Container for runtime service ports.

    :ivar window (Optional[WindowPort]): Window service port.
    :ivar scenes (Optional[ScenePort]): Scene management service port.
    :ivar audio (Optional[AudioPort]): Audio service port.
    :ivar files (Optional[FilePort]): File service port.
    """

    window: Optional[WindowPort] = None
    scenes: Optional[ScenePort] = None
    audio: Optional[AudioPort] = None
    files: Optional[FilePort] = None

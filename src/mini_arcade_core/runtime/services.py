"""
Service interfaces for runtime components.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Protocol

from mini_arcade_core.backend import Backend, Event
from mini_arcade_core.runtime.input_frame import InputFrame

if TYPE_CHECKING:
    from mini_arcade_core.scenes.scene import Scene


class WindowPort(Protocol):
    """Interface for window-related operations."""

    backend: Backend

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

    @property
    def current_scene(self) -> "Scene | None":
        """
        Get the currently active scene.

        :return: The active Scene instance, or None if no scene is active.
        :rtype: Scene | None
        """

    @property
    def visible_stack(self) -> List["Scene"]:
        """
        Return the list of scenes that should be drawn (base + overlays).
        We draw from the top-most non-overlay scene upward.

        :return: List of visible Scene instances.
        :rtype: list[Scene]
        """

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

    def pop(self) -> "Scene | None":
        """
        Pop the current scene from the scene stack.

        :return: The popped Scene instance, or None if the stack was empty.
        :rtype: Scene | None
        """

    def clean(self):
        """
        Clean up all scenes from the scene stack.
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


class CapturePort(Protocol):
    """Interface for frame capture operations."""

    backend: Backend

    def screenshot(self, label: str | None = None) -> str:
        """
        Capture the current frame.

        :param label: Optional label for the screenshot file.
        :type label: str | None

        :return: Screenshot file path.
        :rtype: str
        """

    def screenshot_bytes(self) -> bytes | None:
        """
        Capture the current frame and return it as bytes.

        :return: Screenshot data as bytes.
        :rtype: bytes | None
        """


class InputPort(Protocol):
    """Interface for input handling operations."""

    def build(
        self, events: list[Event], frame_index: int, dt: float
    ) -> InputFrame:
        """
        Build an InputFrame from the given events.

        :param events: List of input events.
        :type events: list[Event]

        :param frame_index: Current frame index.
        :type frame_index: int

        :param dt: Delta time since last frame.
        :type dt: float

        :return: Constructed InputFrame.
        :rtype: InputFrame
        """


@dataclass
class RuntimeServices:
    """
    Container for runtime service ports.

    :ivar window (WindowPort): Window service port.
    :ivar scenes (ScenePort): Scene management service port.
    :ivar audio (AudioPort): Audio service port.
    :ivar files (FilePort): File service port.
    :ivar capture (CapturePort): Capture service port.
    :ivar input (InputPort): Input handling service port.
    """

    window: WindowPort
    scenes: ScenePort
    audio: AudioPort
    files: FilePort
    capture: CapturePort
    input: InputPort

"""
Backend interface for rendering and input.
This is the only part of the code that talks to SDL/pygame directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Optional, Protocol, Tuple, Union

Color = Union[Tuple[int, int, int], Tuple[int, int, int, int]]


class EventType(Enum):
    """
    High-level event types understood by the core.

    :cvar UNKNOWN: Unknown/unhandled event.
    :cvar QUIT: User requested to quit the game.
    :cvar KEYDOWN: A key was pressed.
    :cvar KEYUP: A key was released.
    :cvar MOUSEMOTION: The mouse was moved.
    :cvar MOUSEBUTTONDOWN: A mouse button was pressed.
    :cvar MOUSEBUTTONUP: A mouse button was released.
    :cvar MOUSEWHEEL: The mouse wheel was scrolled.
    :cvar WINDOWRESIZED: The window was resized.
    :cvar TEXTINPUT: Text input event (for IME support).
    """

    UNKNOWN = auto()
    QUIT = auto()

    KEYDOWN = auto()
    KEYUP = auto()

    # Mouse
    MOUSEMOTION = auto()
    MOUSEBUTTONDOWN = auto()
    MOUSEBUTTONUP = auto()
    MOUSEWHEEL = auto()

    # Window / text
    WINDOWRESIZED = auto()
    TEXTINPUT = auto()


# Justification: Simple data container for now
# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class Event:
    """
    Core event type.

    For now we only care about:
    - type: what happened
    - key: integer key code (e.g. ESC = 27), or None if not applicable

    :ivar type (EventType): The type of event.
    :ivar key (int | None): The key code associated with the event, if any.
    :ivar scancode (int | None): The hardware scancode of the key, if any.
    :ivar mod (int | None): Modifier keys bitmask, if any.
    :ivar repeat (bool | None): Whether this key event is a repeat, if any.
    :ivar x (int | None): Mouse X position, if any.
    :ivar y (int | None): Mouse Y position, if any.
    :ivar dx (int | None): Mouse delta X, if any.
    :ivar dy (int | None): Mouse delta Y, if any.
    :ivar button (int | None): Mouse button number, if any.
    :ivar wheel (Tuple[int, int] | None): Mouse wheel scroll (x, y), if any.
    :ivar size (Tuple[int, int] | None): New window size (width, height), if any.
    :ivar text (str | None): Text input, if any.
    """

    type: EventType
    key: Optional[int] = None

    # Keyboard extras (optional)
    scancode: Optional[int] = None
    mod: Optional[int] = None
    repeat: Optional[bool] = None

    # Mouse (optional)
    x: Optional[int] = None
    y: Optional[int] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    button: Optional[int] = None
    wheel: Optional[Tuple[int, int]] = None  # (wheel_x, wheel_y)

    # Window (optional)
    size: Optional[Tuple[int, int]] = None  # (width, height)

    # Text input (optional)
    text: Optional[str] = None


# pylint: enable=too-many-instance-attributes


class Backend(Protocol):
    """
    Interface that any rendering/input backend must implement.

    mini-arcade-core only talks to this protocol, never to SDL/pygame directly.
    """

    def init(self, width: int, height: int, title: str):
        """
        Initialize the backend and open a window.
        Should be called once before the main loop.

        :param width: Width of the window in pixels.
        :type width: int

        :param height: Height of the window in pixels.
        :type height: int

        :param title: Title of the window.
        :type title: str
        """

    def poll_events(self) -> Iterable[Event]:
        """
        Return all pending events since last call.
        Concrete backends will translate their native events into core Event objects.

        :return: An iterable of Event objects.
        :rtype: Iterable[Event]
        """

    def set_clear_color(self, r: int, g: int, b: int):
        """
        Set the background/clear color used by begin_frame.

        :param r: Red component (0-255).
        :type r: int

        :param g: Green component (0-255).
        :type g: int

        :param b: Blue component (0-255).
        :type b: int
        """

    def begin_frame(self):
        """
        Prepare for drawing a new frame (e.g. clear screen).
        """

    def end_frame(self):
        """
        Present the frame to the user (swap buffers).
        """

    # Justification: Simple drawing API for now
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: Color = (255, 255, 255),
    ):
        """
        Draw a filled rectangle in some default color.
        We'll keep this minimal for now; later we can extend with colors/sprites.

        :param x: X position of the rectangle's top-left corner.
        :type x: int

        :param y: Y position of the rectangle's top-left corner.
        :type y: int

        :param w: Width of the rectangle.
        :type w: int

        :param h: Height of the rectangle.
        :type h: int

        :param color: RGB color tuple.
        :type color: Color
        """

    # pylint: enable=too-many-arguments,too-many-positional-arguments

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: Color = (255, 255, 255),
    ):
        """
        Draw text at the given position in a default font and color.

        Backends may ignore advanced styling for now; this is just to render
        simple labels like menu items, scores, etc.

        :param x: X position of the text's top-left corner.
        :type x: int

        :param y: Y position of the text's top-left corner.
        :type y: int

        :param text: The text string to draw.
        :type text: str

        :param color: RGB color tuple.
        :type color: Color
        """

    def capture_frame(self, path: str | None = None) -> bytes | None:
        """
        Capture the current frame.
        If `path` is provided, save to that file (e.g. PNG).
        Returns raw bytes (PNG) or None if unsupported.

        :param path: Optional file path to save the screenshot.
        :type path: str | None

        :return: Raw image bytes if no path given, else None.
        :rtype: bytes | None
        """
        raise NotImplementedError

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Iterable

import pytest

from mini_arcade_core.backend import Backend, Color, Event, EventType

# -------------------------------------------------------------------
# Helper: a concrete backend implementation to exercise the Protocol
# -------------------------------------------------------------------


class DummyBackend:
    """
    Minimal concrete backend to validate the Backend Protocol contract.

    It records calls so we can assert on side effects.
    """

    def __init__(self):
        self.inited = False
        self.init_args: tuple[int, int, str] | None = None

        self.clear_color: tuple[int, int, int] | None = None

        self.begin_called = 0
        self.end_called = 0

        self.rect_calls: list[tuple[int, int, int, int, Color]] = []
        self.text_calls: list[tuple[int, int, str, Color]] = []

        self._events: list[Event] = []
        self.capture_paths: list[str | None] = []

    # --- Backend API ---

    def init(self, width: int, height: int, title: str):
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self) -> Iterable[Event]:
        # Just return whatever has been queued
        return list(self._events)

    def set_clear_color(self, r: int, g: int, b: int):
        self.clear_color = (r, g, b)

    def begin_frame(self):
        self.begin_called += 1

    def end_frame(self):
        self.end_called += 1

    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: Color = (255, 255, 255),
    ):
        self.rect_calls.append((x, y, w, h, color))

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: Color = (255, 255, 255),
    ):
        self.text_calls.append((x, y, text, color))

    def capture_frame(self, path: str | None = None) -> bytes | None:
        # For this test backend, we don't actually capture anything;
        # we only record the requested path.
        self.capture_paths.append(path)
        return None

    # --- Test-only helpers ---

    def queue_event(self, event: Event):
        """Utility to queue an event that poll_events will return."""
        self._events.append(event)


# -------------------------
# I/O tests
# -------------------------


def test_event_type_members_exist():
    """I/O: EventType should expose the expected basic members."""
    assert EventType.UNKNOWN in EventType
    assert EventType.QUIT in EventType
    assert EventType.KEYDOWN in EventType
    assert EventType.KEYUP in EventType


def test_event_default_key_is_none():
    """I/O: Event.key should default to None when not provided."""
    ev = Event(type=EventType.KEYDOWN)
    assert ev.type is EventType.KEYDOWN
    assert ev.key is None


def test_event_stores_type_and_key():
    """I/O: Event should store the provided key code."""
    ev = Event(type=EventType.KEYDOWN, key=27)
    assert ev.type is EventType.KEYDOWN
    assert ev.key == 27


def test_dummy_backend_behaves_like_backend_protocol():
    """
    I/O + side effects: DummyBackend should be usable wherever a Backend
    is expected and record calls appropriately.
    """

    def use_backend(backend: Backend):
        backend.init(800, 600, "Test")
        list(backend.poll_events())  # just to exercise the method
        backend.set_clear_color(10, 20, 30)
        backend.begin_frame()
        backend.draw_rect(0, 0, 10, 10)
        backend.draw_text(5, 5, "hello")
        backend.end_frame()
        result = backend.capture_frame()
        assert result is None  # our dummy backend never returns bytes

    backend = DummyBackend()
    backend.queue_event(Event(EventType.QUIT))

    use_backend(backend)

    # Verify side effects
    assert backend.inited is True
    assert backend.init_args == (800, 600, "Test")
    assert backend.clear_color == (10, 20, 30)
    assert backend.begin_called == 1
    assert backend.end_called == 1
    assert len(backend.rect_calls) == 1
    assert len(backend.text_calls) == 1
    assert backend.capture_paths == [None]


def test_dummy_backend_accepts_rgba_color():
    """I/O: Backend.draw_rect should accept both RGB and RGBA Colors."""
    backend = DummyBackend()
    backend.draw_rect(0, 0, 10, 10, color=(255, 0, 0))  # RGB
    backend.draw_rect(0, 0, 10, 10, color=(255, 0, 0, 128))  # RGBA

    assert len(backend.rect_calls) == 2
    _, _, _, _, color_rgb = backend.rect_calls[0]
    _, _, _, _, color_rgba = backend.rect_calls[1]

    assert color_rgb == (255, 0, 0)
    assert color_rgba == (255, 0, 0, 128)


# -------------------------
# Edge cases
# -------------------------


def test_event_is_immutable():
    """
    Edge case: Event is a frozen dataclass; attempting to modify it
    should raise FrozenInstanceError.
    """
    ev = Event(type=EventType.KEYDOWN, key=13)

    with pytest.raises(FrozenInstanceError):  # type: ignore[name-defined]
        # mypy/linters may complain about attribute assignment, but we
        # want to assert it fails at runtime.
        ev.key = 42  # type: ignore[misc]

# tests/test_scene.py
from __future__ import annotations

from typing import Any, List

from mini_arcade_core import Entity, Game, GameConfig, Scene


class _DummyBackend:
    """Minimal backend for Scene/Game tests."""

    def __init__(self):
        self.inited = False
        self.init_args = None

    def init(self, width: int, height: int, title: str):
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self):
        return []

    def set_clear_color(self, r: int, g: int, b: int):
        pass

    def begin_frame(self):
        pass

    def end_frame(self):
        pass

    def draw_rect(self, x: int, y: int, w: int, h: int, color=(255, 255, 255)):
        pass

    def draw_text(self, x: int, y: int, text: str, color=(255, 255, 255)):
        pass

    def capture_frame(self, path: str | None = None) -> bytes | None:
        return None


class _DummyEntity(Entity):
    """Test double that records update/draw calls."""

    def __init__(self):
        self.updated_with: List[float] = []
        self.drawn_on: List[Any] = []

    def update(self, dt: float):  # type: ignore[override]
        self.updated_with.append(dt)

    def draw(self, surface: Any):  # type: ignore[override]
        self.drawn_on.append(surface)


class _DummyScene(Scene):
    """Concrete Scene implementation for testing helpers."""

    def __init__(self, game: Game):
        super().__init__(game)
        self.entered = False
        self.exited = False
        self.handled_events: list[Any] = []
        self.updated_with: list[float] = []
        self.drawn_on: list[Any] = []

    def on_enter(self):  # type: ignore[override]
        self.entered = True

    def on_exit(self):  # type: ignore[override]
        self.exited = True

    def handle_event(self, event: object):  # type: ignore[override]
        self.handled_events.append(event)

    def update(self, dt: float):  # type: ignore[override]
        self.updated_with.append(dt)
        # Typically you’d call self.update_entities(dt) here in a real scene

    def draw(self, surface: Any):  # type: ignore[override]
        self.drawn_on.append(surface)
        # Typically you’d call self.draw_entities(surface) and self.draw_overlays(surface)


# -------------------------
# I/O tests
# -------------------------


def test_scene_initializes_size_and_empty_entity_list():
    """I/O: Scene should derive size from GameConfig and start with no entities."""
    backend = _DummyBackend()
    cfg = GameConfig(width=640, height=480, backend=backend)
    game = Game(cfg)

    scene = _DummyScene(game)

    assert scene.size.width == 640
    assert scene.size.height == 480
    assert scene.entities == []


def test_add_remove_and_clear_entities():
    """I/O: add_entity/remove_entity/clear_entities should manage the entity list."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))
    scene = _DummyScene(game)

    e1 = _DummyEntity()
    e2 = _DummyEntity()

    # add multiple in one call
    scene.add_entity(e1, e2)
    assert e1 in scene.entities
    assert e2 in scene.entities

    # remove single entity
    scene.remove_entity(e1)
    assert e1 not in scene.entities
    assert e2 in scene.entities

    # clear all
    scene.clear_entities()
    assert scene.entities == []


def test_update_entities_calls_update_on_all():
    """Side effect: update_entities should call update(dt) on each entity."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))
    scene = _DummyScene(game)

    e1 = _DummyEntity()
    e2 = _DummyEntity()
    scene.add_entity(e1, e2)

    scene.update_entities(0.5)

    assert e1.updated_with == [0.5]
    assert e2.updated_with == [0.5]


def test_draw_entities_calls_draw_on_all():
    """Side effect: draw_entities should call draw(surface) on each entity."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))
    scene = _DummyScene(game)

    e1 = _DummyEntity()
    e2 = _DummyEntity()
    scene.add_entity(e1, e2)

    surface = object()
    scene.draw_entities(surface)  # type: ignore[arg-type]

    assert e1.drawn_on == [surface]
    assert e2.drawn_on == [surface]


# -------------------------
# Overlays
# -------------------------


def test_add_remove_and_clear_overlays():
    """I/O: add_overlay/remove_overlay/clear_overlays should manage overlay list."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))
    scene = _DummyScene(game)

    calls = []

    def ov1(surface):
        calls.append(("ov1", surface))

    def ov2(surface):
        calls.append(("ov2", surface))

    # add overlays
    scene.add_overlay(ov1)
    scene.add_overlay(ov2)
    assert len(scene._overlays) == 2  # type: ignore[attr-defined]

    # remove one
    scene.remove_overlay(ov1)
    assert ov1 not in scene._overlays  # type: ignore[attr-defined]
    assert ov2 in scene._overlays  # type: ignore[attr-defined]

    # clear them all
    scene.clear_overlays()
    assert scene._overlays == []  # type: ignore[attr-defined]


def test_draw_overlays_calls_all_registered_overlays():
    """Side effect: draw_overlays should invoke each overlay with the surface."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))
    scene = _DummyScene(game)

    calls = []

    def ov1(surface):
        calls.append(("ov1", surface))

    def ov2(surface):
        calls.append(("ov2", surface))

    scene.add_overlay(ov1)
    scene.add_overlay(ov2)

    surface = object()
    scene.draw_overlays(surface)  # type: ignore[arg-type]

    assert calls == [("ov1", surface), ("ov2", surface)]

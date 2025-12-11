from __future__ import annotations

import pytest

from mini_arcade_core import (
    Backend,
    Bounds2D,
    Entity,
    Event,
    EventType,
    Game,
    GameConfig,
    KinematicData,
    KinematicEntity,
    Position2D,
    RectCollider,
    RectKinematic,
    RectSprite,
    Scene,
    Size2D,
    SpriteEntity,
    Velocity2D,
    VerticalBounce,
    VerticalWrap,
    __version__,
    get_version,
    run_game,
)


class _DummyBackend:
    """Minimal backend for run_game tests."""

    def __init__(self):
        self.inited = False
        self.init_args = None
        self.begin_called = 0
        self.end_called = 0
        self.clear_color = None

    # --- Backend API ---

    def init(self, width: int, height: int, title: str):
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self):
        # No events by default
        return []

    def begin_frame(self):
        self.begin_called += 1

    def end_frame(self):
        self.end_called += 1

    def set_clear_color(self, r: int, g: int, b: int):
        self.clear_color = (r, g, b)

    # Kept minimal on purpose – core doesn't use these in the tests
    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        pass

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        pass

    def capture_frame(self, path: str | None = None):
        return None


# -------------------------
# I/O / public API tests
# -------------------------


def test_public_api_exports():
    """I/O: top-level package should expose the main types."""

    # Simple existence checks – import above would already fail if symbols
    # were not exported correctly, but we assert explicitly for clarity.
    assert Game is not None
    assert GameConfig is not None
    assert Scene is not None
    assert Entity is not None
    assert SpriteEntity is not None
    assert KinematicEntity is not None

    # Geometry / physics / collisions
    assert Position2D is not None
    assert Size2D is not None
    assert Bounds2D is not None
    assert Velocity2D is not None
    assert KinematicData is not None
    assert RectCollider is not None

    # Boundaries helpers and protocols
    assert VerticalBounce is not None
    assert VerticalWrap is not None
    assert RectSprite is not None
    assert RectKinematic is not None

    # Backend and events
    assert Backend is not None
    assert Event is not None
    assert EventType is not None

    # Helper
    assert callable(run_game)


def test_get_version_and_dunder_version_are_strings():
    """I/O: get_version and __version__ should both return strings."""
    v = get_version()
    assert isinstance(v, str)
    assert isinstance(__version__, str)


# -------------------------
# Test Scene for run_game
# -------------------------


class _DummyScene(Scene):
    constructed = False

    def __init__(self, game: Game):
        super().__init__(game)
        _DummyScene.constructed = True
        self.entered = False
        self.exited = False
        self.updated = 0

    def on_enter(self):
        self.entered = True

    def on_exit(self):
        self.exited = True

    def handle_event(self, event: object):
        # No-op for this test
        pass

    def update(self, dt: float):
        self.updated += 1
        # Quit immediately so run_game() returns quickly.
        self.game.quit()

    def draw(self, surface: object):
        # No-op for this test
        pass


# -------------------------
# I/O: run_game behaviour
# -------------------------


def test_run_game_instantiates_scene_and_runs_with_backend():
    """
    I/O: run_game should construct the scene class with a Game instance and
    execute at least one frame using the provided backend.
    """
    backend = _DummyBackend()
    cfg = GameConfig(
        width=400,
        height=300,
        title="RunGameTest",
        backend=backend,
    )
    _DummyScene.constructed = False

    run_game(_DummyScene, cfg)

    assert _DummyScene.constructed is True
    assert backend.inited is True
    assert backend.init_args == (400, 300, "RunGameTest")
    assert backend.begin_called >= 1
    assert backend.end_called >= 1


def test_run_game_accepts_custom_config_and_propagates_size_title():
    """
    I/O: run_game should accept a custom GameConfig object and propagate it
    to the backend via Game.
    """
    backend = _DummyBackend()
    cfg = GameConfig(width=1024, height=768, title="Custom", backend=backend)

    run_game(_DummyScene, cfg)

    assert backend.inited is True
    assert backend.init_args == (1024, 768, "Custom")


# -------------------------
# Edge cases
# -------------------------


def test_run_game_without_backend_raises_value_error():
    """
    Edge case: run_game with a config that has no backend should fail fast.
    """
    cfg = GameConfig()  # backend is None by default
    with pytest.raises(ValueError):
        run_game(_DummyScene, cfg)


# -------------------------
# Side effects
# -------------------------


def test_run_game_calls_game_run(monkeypatch):
    """
    Side effect: ensure that Game.run is actually called by run_game.
    We monkeypatch Game to a test double that records the call.
    """
    called = {"run": False}

    class TestGame(Game):
        def run(self, initial_scene: Scene):  # type: ignore[override]
            called["run"] = True

        def change_scene(self, scene: Scene):  # type: ignore[override]
            # For this test we don't care about scene lifecycle.
            self._current_scene = scene  # type: ignore[attr-defined]

    # Patch the Game symbol inside the mini_arcade_core package
    import mini_arcade_core

    original_game_cls = mini_arcade_core.Game
    mini_arcade_core.Game = TestGame  # type: ignore[assignment]

    try:
        backend = _DummyBackend()
        cfg = GameConfig(backend=backend)
        run_game(_DummyScene, cfg)
    finally:
        mini_arcade_core.Game = original_game_cls  # restore

    assert called["run"] is True

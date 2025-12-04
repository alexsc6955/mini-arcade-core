from __future__ import annotations

import pytest

from mini_arcade_core import (
    Entity,
    Game,
    GameConfig,
    Scene,
    SpriteEntity,
    run_game,
)


class _DummyBackend:
    """Minimal backend for run_game tests."""

    def __init__(self) -> None:
        self.inited = False
        self.init_args = None
        self.begin_called = 0
        self.end_called = 0

    def init(self, width: int, height: int, title: str) -> None:
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self):
        return []

    def begin_frame(self) -> None:
        self.begin_called += 1

    def end_frame(self) -> None:
        self.end_called += 1

    def draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        pass


# -------------------------
# I/O tests
# -------------------------


def test_public_api_exports():
    """I/O: __all__ should expose the main types."""
    # Just importing above will fail if __all__ or exports are wrong.
    assert Game is not None
    assert GameConfig is not None
    assert Scene is not None
    assert Entity is not None
    assert SpriteEntity is not None
    assert callable(run_game)


class _DummyScene(Scene):
    constructed = False

    def __init__(self, game: Game):
        super().__init__(game)
        _DummyScene.constructed = True
        self.entered = False
        self.exited = False
        self.updated = 0

    def on_enter(self) -> None:
        self.entered = True

    def on_exit(self) -> None:
        self.exited = True

    def handle_event(self, event: object) -> None:
        pass

    def update(self, dt: float) -> None:
        self.updated += 1
        # Quit immediately so run_game() returns quickly.
        self.game.quit()

    def draw(self, surface: object) -> None:
        pass


def test_run_game_instantiates_scene_and_runs_with_backend():
    """
    I/O: run_game should construct the scene class with a Game instance and
    execute at least one frame using the provided backend.
    """
    backend = _DummyBackend()
    cfg = GameConfig(
        width=400, height=300, title="RunGameTest", backend=backend
    )
    _DummyScene.constructed = False

    run_game(_DummyScene, cfg)

    assert _DummyScene.constructed is True
    assert backend.inited is True
    assert backend.begin_called >= 1
    assert backend.end_called >= 1


def test_run_game_accepts_custom_config():
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
    cfg = GameConfig()
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
        def run(self, initial_scene: Scene) -> None:  # type: ignore[override]
            called["run"] = True

        def change_scene(self, scene: Scene) -> None:  # type: ignore[override]
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

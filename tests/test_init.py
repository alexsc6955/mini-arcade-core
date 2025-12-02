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

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: object) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: object) -> None:
        pass


def test_run_game_instantiates_scene_before_running():
    """
    I/O: run_game should construct the scene class with a Game instance.
    We expect NotImplementedError from Game.run, but the scene must be created.
    """
    _DummyScene.constructed = False

    with pytest.raises(NotImplementedError):
        run_game(_DummyScene)

    assert _DummyScene.constructed is True


def test_run_game_accepts_custom_config():
    """
    I/O: run_game should accept a custom GameConfig object.
    We assert it propagates to Game via NotImplementedError message/behavior.
    """

    class _ConfigAwareGame(Game):
        # Just a helper in this test to check config; we won't patch core Game here.
        pass

    cfg = GameConfig(width=1024, height=768, title="Custom")

    # We can't easily inspect the Game created inside run_game without monkeypatch,
    # so this test mostly exists as a "smoke" check that custom config doesn't crash.
    with pytest.raises(NotImplementedError):
        run_game(_DummyScene, cfg)


# -------------------------
# Edge cases
# -------------------------


def test_run_game_raises_not_implemented_from_default_game():
    """
    Edge case: Game.run is abstract via NotImplementedError.
    run_game should propagate that error.
    """
    with pytest.raises(NotImplementedError):
        run_game(_DummyScene)


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
            pass

    # Patch the Game symbol inside the mini_arcade_core package
    import mini_arcade_core

    original_game_cls = mini_arcade_core.Game
    mini_arcade_core.Game = TestGame  # type: ignore[assignment]

    try:
        run_game(_DummyScene)
    finally:
        mini_arcade_core.Game = original_game_cls  # restore

    assert called["run"] is True

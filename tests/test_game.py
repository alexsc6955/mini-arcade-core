from __future__ import annotations

import pytest

from mini_arcade_core import Game, GameConfig, Scene


# -------------------------
# I/O tests
# -------------------------


def test_game_config_defaults():
    """I/O: GameConfig should provide sensible defaults."""
    cfg = GameConfig()
    assert cfg.width == 800
    assert cfg.height == 600
    assert cfg.title == "Mini Arcade Game"
    assert cfg.fps == 60
    assert cfg.background_color == (0, 0, 0)


def test_game_config_custom_values():
    """I/O: GameConfig should accept custom initialization values."""
    cfg = GameConfig(
        width=1024,
        height=576,
        title="Test Game",
        fps=120,
        background_color=(10, 20, 30),
    )
    assert cfg.width == 1024
    assert cfg.height == 576
    assert cfg.title == "Test Game"
    assert cfg.fps == 120
    assert cfg.background_color == (10, 20, 30)


def test_game_initial_state():
    """I/O: Game should store config and initialize internal state."""
    cfg = GameConfig(width=640, height=480, title="InitTest")
    game = Game(cfg)
    assert game.config is cfg
    assert game._current_scene is None  # type: ignore[attr-defined]
    assert game._running is False  # type: ignore[attr-defined]


# -------------------------
# Edge cases
# -------------------------


class _DummyScene(Scene):
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


def test_game_change_scene_not_implemented():
    """Edge case: default Game.change_scene must raise NotImplementedError."""
    game = Game(GameConfig())
    scene = _DummyScene(game)

    with pytest.raises(NotImplementedError) as excinfo:
        game.change_scene(scene)

    assert "Game.change_scene must be implemented" in str(excinfo.value)


def test_game_run_not_implemented():
    """Edge case: default Game.run must raise NotImplementedError."""
    game = Game(GameConfig())
    scene = _DummyScene(game)

    with pytest.raises(NotImplementedError) as excinfo:
        game.run(scene)

    assert "Game.run must be implemented" in str(excinfo.value)


# -------------------------
# Side effects
# -------------------------


def test_custom_game_change_scene_updates_state():
    """
    Side effect: a concrete Game implementation can manage _current_scene.
    This verifies that the base class attributes are usable.
    """

    class ConcreteGame(Game):
        def change_scene(self, scene: Scene) -> None:  # type: ignore[override]
            if self._current_scene is not None:
                self._current_scene.on_exit()
            self._current_scene = scene
            self._current_scene.on_enter()

        def run(self, initial_scene: Scene) -> None:  # type: ignore[override]
            # minimal fake loop: just set current scene
            self.change_scene(initial_scene)
            self._running = False

    game = ConcreteGame(GameConfig())
    scene = _DummyScene(game)

    assert game._current_scene is None  # type: ignore[attr-defined]
    game.change_scene(scene)
    assert game._current_scene is scene  # type: ignore[attr-defined]

from __future__ import annotations

import pytest

from mini_arcade_core import Game, GameConfig, Scene

# -------------------------
# I/O tests
# -------------------------


def test_scene_stores_game_reference():
    """I/O: Concrete Scene implementations should receive and store Game."""

    class ConcreteScene(Scene):
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

    game = Game(GameConfig())
    scene = ConcreteScene(game)

    assert scene.game is game


# -------------------------
# Edge cases
# -------------------------


def test_scene_cannot_be_instantiated_directly():
    """Edge case: Scene is abstract and cannot be instantiated."""
    game = Game(GameConfig())
    with pytest.raises(TypeError):
        Scene(game)  # type: ignore[abstract]


# -------------------------
# Side effects
# -------------------------


def test_scene_methods_can_mutate_internal_state():
    """
    Side effect: verify that a Scene subclass can track state across
    on_enter/update/on_exit.
    """

    class StatefulScene(Scene):
        def __init__(self, game: Game) -> None:
            super().__init__(game)
            self.entered = False
            self.updated_frames = 0
            self.exited = False

        def on_enter(self) -> None:
            self.entered = True

        def on_exit(self) -> None:
            self.exited = True

        def handle_event(self, event: object) -> None:
            # no-op for now
            pass

        def update(self, dt: float) -> None:
            self.updated_frames += 1

        def draw(self, surface: object) -> None:
            # no-op for now
            pass

    scene = StatefulScene(Game(GameConfig()))
    assert scene.entered is False
    assert scene.exited is False
    assert scene.updated_frames == 0

    scene.on_enter()
    scene.update(0.016)
    scene.update(0.016)
    scene.on_exit()

    assert scene.entered is True
    assert scene.updated_frames == 2
    assert scene.exited is True

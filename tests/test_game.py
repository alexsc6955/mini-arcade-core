from __future__ import annotations

import pytest

from mini_arcade_core import Game, GameConfig, Scene


class _DummyBackend:
    """Minimal backend implementation for tests."""

    def __init__(self) -> None:
        self.inited = False
        self.init_args = None
        self.begin_called = 0
        self.end_called = 0
        self.rects = []

    def init(self, width: int, height: int, title: str) -> None:
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self):
        return []  # no events by default

    def begin_frame(self) -> None:
        self.begin_called += 1

    def end_frame(self) -> None:
        self.end_called += 1

    def draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        self.rects.append((x, y, w, h))


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
    backend = _DummyBackend()
    cfg = GameConfig(width=640, height=480, title="InitTest", backend=backend)
    game = Game(cfg)
    assert game.config is cfg
    assert game._current_scene is None  # type: ignore[attr-defined]
    assert game._running is False  # type: ignore[attr-defined]
    assert game.backend is backend  # type: ignore[attr-defined]


# -------------------------
# Edge cases
# -------------------------


def test_game_requires_backend_instance():
    """Edge case: Game must be constructed with a backend instance."""
    cfg = GameConfig()
    with pytest.raises(ValueError) as excinfo:
        Game(cfg)

    assert "backend" in str(excinfo.value)


class _DummyScene(Scene):
    def on_enter(self) -> None:
        self.entered = True  # type: ignore[attr-defined]

    def on_exit(self) -> None:
        self.exited = True  # type: ignore[attr-defined]

    def handle_event(self, event: object) -> None:
        pass

    def update(self, dt: float) -> None:
        # For tests that call Game.run, we quit on first update to avoid an infinite loop.
        self.updated_frames = getattr(self, "updated_frames", 0) + 1  # type: ignore[attr-defined]
        self.game.quit()

    def draw(self, surface: object) -> None:
        pass


def test_game_change_scene_switches_current_scene_and_calls_hooks():
    """I/O: Game.change_scene should swap _current_scene and call on_exit/on_enter."""
    backend = _DummyBackend()
    game = Game(GameConfig(backend=backend))

    scene1 = _DummyScene(game)
    scene2 = _DummyScene(game)

    # first scene
    game.change_scene(scene1)
    assert game._current_scene is scene1  # type: ignore[attr-defined]
    assert getattr(scene1, "entered", False) is True
    assert getattr(scene1, "exited", False) is False

    # switch to second scene
    game.change_scene(scene2)
    assert game._current_scene is scene2  # type: ignore[attr-defined]
    assert getattr(scene1, "exited", False) is True
    assert getattr(scene2, "entered", False) is True


def test_game_run_executes_basic_loop_and_uses_backend():
    """
    Side effect: Game.run should call backend.init, poll_events, and scene hooks
    at least once. We use _DummyScene.update to call game.quit() to exit quickly.
    """
    backend = _DummyBackend()
    cfg = GameConfig(
        width=320, height=240, title="LoopTest", fps=60, backend=backend
    )
    game = Game(cfg)
    scene = _DummyScene(game)

    game.run(scene)

    # backend was inited with config
    assert backend.inited is True
    assert backend.init_args == (320, 240, "LoopTest")

    # at least one frame was rendered
    assert backend.begin_called >= 1
    assert backend.end_called >= 1

    # scene lifecycle happened
    assert getattr(scene, "entered", False) is True
    assert getattr(scene, "updated_frames", 0) >= 1
    assert getattr(scene, "exited", False) is True


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

        # We still can provide our own run implementation if we want for tests
        def run(self, initial_scene: Scene) -> None:  # type: ignore[override]
            self.change_scene(initial_scene)
            self._running = False

    backend = _DummyBackend()
    game = ConcreteGame(GameConfig(backend=backend))
    scene = _DummyScene(game)

    assert game._current_scene is None  # type: ignore[attr-defined]
    game.change_scene(scene)
    assert game._current_scene is scene  # type: ignore[attr-defined]

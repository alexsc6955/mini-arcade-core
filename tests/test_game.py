from __future__ import annotations

import os
from pathlib import Path

import pytest

from mini_arcade_core import Game, GameConfig, Scene


class _DummyBackend:
    """Minimal backend implementation for Game tests."""

    def __init__(self):
        self.inited = False
        self.init_args = None
        self.begin_called = 0
        self.end_called = 0
        self.rects = []
        self.clear_color = None
        self.captured_paths: list[str] = []

    def init(self, width: int, height: int, title: str) -> None:
        self.inited = True
        self.init_args = (width, height, title)

    def poll_events(self):
        return []  # no events by default

    def begin_frame(self) -> None:
        self.begin_called += 1

    def end_frame(self) -> None:
        self.end_called += 1

    def draw_rect(self, x: int, y: int, w: int, h: int, color=(255, 255, 255)):
        self.rects.append((x, y, w, h, color))

    def draw_text(self, x: int, y: int, text: str, color=(255, 255, 255)):
        # Not needed for these tests, but present to match Backend protocol
        pass

    def set_clear_color(self, r: int, g: int, b: int) -> None:
        self.clear_color = (r, g, b)

    def capture_frame(self, path: str | None = None) -> bytes | None:
        """
        For screenshot tests we just record the path and pretend capture succeeded
        (or not), controlled externally by setting a flag.
        """
        if path is not None:
            self.captured_paths.append(path)
        # Default behavior: pretend success; tests can override by monkeypatching
        return b"fake-bmp-bytes"


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
    assert cfg.backend is None


def test_game_config_custom_values():
    """I/O: GameConfig should accept custom initialization values."""
    backend = _DummyBackend()
    cfg = GameConfig(
        width=1024,
        height=576,
        title="Test Game",
        fps=120,
        background_color=(10, 20, 30),
        backend=backend,
    )
    assert cfg.width == 1024
    assert cfg.height == 576
    assert cfg.title == "Test Game"
    assert cfg.fps == 120
    assert cfg.background_color == (10, 20, 30)
    assert cfg.backend is backend


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
    """Concrete Scene implementation for exercising Game behavior."""

    def on_enter(self) -> None:  # type: ignore[override]
        self.entered = True  # type: ignore[attr-defined]

    def on_exit(self) -> None:  # type: ignore[override]
        self.exited = True  # type: ignore[attr-defined]

    def handle_event(self, event: object) -> None:  # type: ignore[override]
        # For these tests we don't care about events.
        pass

    def update(self, dt: float) -> None:  # type: ignore[override]
        # For tests that call Game.run, we quit on first update
        # to avoid an infinite loop.
        self.updated_frames = getattr(self, "updated_frames", 0) + 1  # type: ignore[attr-defined]
        self.game.quit()

    def draw(self, surface) -> None:  # type: ignore[override]
        # No-op for these tests.
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
    Side effect: Game.run should call backend.init, set_clear_color,
    poll_events, and scene hooks at least once.
    _DummyScene.update calls game.quit() to exit quickly.
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

    # background color was applied
    assert backend.clear_color == cfg.background_color

    # at least one frame was rendered
    assert backend.begin_called >= 1
    assert backend.end_called >= 1

    # scene lifecycle happened
    assert getattr(scene, "entered", False) is True
    assert getattr(scene, "updated_frames", 0) >= 1
    assert getattr(scene, "exited", False) is True


# -------------------------
# Side effects: subclassing & screenshot
# -------------------------


def test_custom_game_change_scene_updates_state():
    """
    Side effect: a concrete Game implementation can manage _current_scene.
    This verifies that the base class attributes are usable.
    """

    class ConcreteGame(Game):
        def change_scene(self, scene: Scene):  # type: ignore[override]
            if self._current_scene is not None:
                self._current_scene.on_exit()
            self._current_scene = scene
            self._current_scene.on_enter()

        # Minimal custom run for this test
        def run(self, initial_scene: Scene):  # type: ignore[override]
            self.change_scene(initial_scene)
            self._running = False

    backend = _DummyBackend()
    game = ConcreteGame(GameConfig(backend=backend))
    scene = _DummyScene(game)

    assert game._current_scene is None  # type: ignore[attr-defined]
    game.change_scene(scene)
    assert game._current_scene is scene  # type: ignore[attr-defined]


def test_screenshot_returns_path_and_calls_capture_and_convert(
    tmp_path, monkeypatch
):
    """
    Side effect: screenshot() should:
    - create the directory if needed
    - call backend.capture_frame with a .bmp path
    - call _convert_bmp_to_image
    - return the resulting .png path
    """
    backend = _DummyBackend()
    cfg = GameConfig(backend=backend)
    game = Game(cfg)

    # Track calls to _convert_bmp_to_image
    called = {"args": None}

    def fake_convert(bmp_path: str, out_path: str) -> bool:
        called["args"] = (bmp_path, out_path)
        # Pretend conversion succeeded
        # Also create a dummy file so that if someone inspects it later it exists.
        Path(out_path).write_bytes(b"png")
        return True

    monkeypatch.setattr(
        Game, "_convert_bmp_to_image", staticmethod(fake_convert)
    )

    out_dir = tmp_path / "shots"
    label = "testlabel"

    result = game.screenshot(label=label, directory=str(out_dir))

    # Directory should exist
    assert out_dir.exists()

    # backend.capture_frame was called with a .bmp path inside directory
    assert len(backend.captured_paths) == 1
    bmp_path = backend.captured_paths[0]
    assert bmp_path.endswith(".bmp")
    assert str(out_dir) in bmp_path

    # _convert_bmp_to_image should have been called with bmp + png paths
    assert called["args"] is not None
    conv_bmp_path, conv_png_path = called["args"]
    assert conv_bmp_path == bmp_path
    assert conv_png_path.endswith(".png")

    # screenshot() should return the PNG path
    assert result is not None
    assert result.endswith(".png")
    # And the returned file should exist
    assert os.path.exists(result)


def test_screenshot_returns_none_if_capture_fails(tmp_path, monkeypatch):
    """
    Edge case: if backend.capture_frame returns falsy value,
    screenshot() should return None and not call _convert_bmp_to_image.
    """
    backend = _DummyBackend()

    # Override capture_frame to simulate failure
    def failing_capture(path: str | None = None) -> bytes | None:
        if path is not None:
            backend.captured_paths.append(path)
        return None

    backend.capture_frame = failing_capture  # type: ignore[assignment]

    cfg = GameConfig(backend=backend)
    game = Game(cfg)

    called = {"convert": False}

    def fake_convert(bmp_path: str, out_path: str) -> bool:
        called["convert"] = True
        return False

    monkeypatch.setattr(
        Game, "_convert_bmp_to_image", staticmethod(fake_convert)
    )

    out_dir = tmp_path / "shots_fail"
    result = game.screenshot(label="fail", directory=str(out_dir))

    # capture_frame was still called (with a bmp path)
    assert len(backend.captured_paths) == 1
    assert backend.captured_paths[0].endswith(".bmp")

    # No conversion attempted
    assert called["convert"] is False

    # screenshot should return None
    assert result is None

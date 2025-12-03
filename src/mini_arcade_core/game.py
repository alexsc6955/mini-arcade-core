"""
Game core module defining the Game class and configuration.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .backend import Backend

if TYPE_CHECKING:  # avoid runtime circular import
    from .scene import Scene


@dataclass
class GameConfig:
    """
    Configuration options for the Game.

    :ivar width: Width of the game window in pixels.
    :ivar height: Height of the game window in pixels.
    :ivar title: Title of the game window.
    :ivar fps: Target frames per second.
    :ivar background_color: RGB background color.
    :ivar backend: Optional backend class to use for rendering and input.
    """

    width: int = 800
    height: int = 600
    title: str = "Mini Arcade Game"
    fps: int = 60
    background_color: tuple[int, int, int] = (0, 0, 0)
    backend: type[Backend] | None = None


class Game:
    """Core game object responsible for managing the main loop and active scene."""

    def __init__(self, config: GameConfig):
        """
        :param config: Game configuration options.
        :type config: GameConfig
        """
        self.config = config
        self._current_scene: Scene | None = None
        self._running: bool = False
        self.backend: Backend | None = config.backend

    def change_scene(self, scene: Scene):
        """
        Swap the active scene. Concrete implementations should call
        ``on_exit``/``on_enter`` appropriately.

        :param scene: The new scene to activate.
        :type scene: Scene
        """
        if self._current_scene is not None:
            self._current_scene.on_exit()

        self._current_scene = scene
        self._current_scene.on_enter()

    def quit(self):
        """Request that the main loop stops."""
        self._running = False

    def run(self, initial_scene: Scene):
        """
        Run the main loop starting with the given scene.

        This is intentionally left abstract so you can plug pygame, pyglet,
        or another backend.

        :param initial_scene: The scene to start the game with.
        :type initial_scene: Scene
        """
        if self.backend is None:
            raise RuntimeError(
                "GameConfig.backend must be set before running the game."
            )

        backend = self.backend

        # Init backend window
        backend.init(self.config.width, self.config.height, self.config.title)

        # Set the initial scene
        self.change_scene(initial_scene)

        self._running = True

        target_dt = (
            1.0 / float(self.config.fps) if self.config.fps > 0 else 0.0
        )
        last_time = time.perf_counter()

        while self._running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            # 1) Poll events and pass to scene
            events = list(backend.poll_events())
            if self._current_scene is not None:
                for ev in events:
                    self._current_scene.handle_event(ev)  # type: ignore[arg-type]

                # 2) Update scene
                self._current_scene.update(dt)

                # 3) Draw
                backend.begin_frame()
                self._current_scene.draw(backend)
                backend.end_frame()

            # Simple FPS cap
            if target_dt > 0 and dt < target_dt:
                time.sleep(target_dt - dt)

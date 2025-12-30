"""
Game core module defining the Game class and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter, sleep
from typing import Literal

from mini_arcade_core.backend import Backend
from mini_arcade_core.commands import CommandQueue, QuitCommand
from mini_arcade_core.managers.cheats import CheatManager
from mini_arcade_core.render.pipeline import RenderPipeline
from mini_arcade_core.runtime.adapters import (
    CaptureAdapter,
    InputAdapter,
    LocalFilesAdapter,
    NullAudioAdapter,
    SceneAdapter,
    WindowAdapter,
)
from mini_arcade_core.runtime.input_frame import InputFrame
from mini_arcade_core.runtime.services import RuntimeServices
from mini_arcade_core.scenes.registry import SceneRegistry
from mini_arcade_core.sim.runner import SimRunner, SimRunnerConfig
from mini_arcade_core.view.render_packet import RenderPacket


@dataclass
class WindowConfig:
    """
    Configuration for a game window (not implemented).
    """

    width: int
    height: int
    background_color: tuple[int, int, int]
    title: str


@dataclass
class GameConfig:
    """
    Configuration options for the Game.

    :ivar width: Width of the game window in pixels.
    :ivar height: Height of the game window in pixels.
    :ivar title: Title of the game window.
    :ivar fps: Target frames per second.
    :ivar background_color: RGB background color.
    :ivar backend: Optional Backend instance to use for rendering and input.
    """

    window: WindowConfig | None = None
    fps: int = 60
    backend: Backend | None = None


Difficulty = Literal["easy", "normal", "hard", "insane"]


@dataclass
class GameSettings:
    """
    Game settings that can be modified during gameplay.

    :ivar difficulty: Current game difficulty level.
    """

    difficulty: Difficulty = "normal"


def _neutral_input(frame_index: int, dt: float) -> InputFrame:
    return InputFrame(frame_index=frame_index, dt=dt)


class Game:
    """Core game object responsible for managing the main loop and active scene."""

    def __init__(
        self, config: GameConfig, registry: SceneRegistry | None = None
    ):
        """
        :param config: Game configuration options.
        :type config: GameConfig

        :param registry: Optional SceneRegistry for scene management.
        :type registry: SceneRegistry | None

        :raises ValueError: If the provided config does not have a valid Backend.
        """
        self.config = config
        self._running: bool = False

        if config.backend is None:
            raise ValueError(
                "GameConfig.backend must be set to a Backend instance"
            )
        self.backend: Backend = config.backend
        self.registry = registry or SceneRegistry(_factories={})
        self.settings = GameSettings()
        self.services = RuntimeServices(
            window=WindowAdapter(
                self.backend,
            ),
            scenes=SceneAdapter(self.registry, self),
            audio=NullAudioAdapter(),
            files=LocalFilesAdapter(),
            capture=CaptureAdapter(self.backend),
            input=InputAdapter(),
        )

        self._commands = CommandQueue()
        self.cheats = CheatManager()

    def quit(self):
        """Request that the main loop stops."""
        self._running = False

    def run(self, initial_scene_id: str):
        """
        Run the main loop starting with the given scene.

        This is intentionally left abstract so you can plug pygame, pyglet,
        or another backend.

        :param initial_scene_id: The scene id to start the game with (must be registered).
        :type initial_scene_id: str
        """
        backend = self.backend

        if self.config.window is None:
            raise ValueError("GameConfig.window must be set")

        self.services.window.set_window_size(
            self.config.window.width, self.config.window.height
        )
        self.services.window.set_title(self.config.window.title)

        br, bg, bb = self.config.window.background_color
        self.services.window.set_clear_color(br, bg, bb)

        self.services.scenes.change(initial_scene_id)

        pipeline = RenderPipeline()

        self._running = True
        target_dt = 1.0 / self.config.fps if self.config.fps > 0 else 0.0
        last_time = perf_counter()
        frame_index = 0

        # cache packets so blocked-update scenes still render their last frame
        packet_cache: dict[int, RenderPacket] = {}

        while self._running:
            now = perf_counter()
            dt = now - last_time
            last_time = now

            events = list(backend.poll_events())
            input_frame = self.services.input.build(events, frame_index, dt)

            # Window/OS quit (close button)
            if input_frame.quit:
                self._commands.push(QuitCommand())
                break

            # who gets input?
            input_entry = self.services.scenes.input_entry()
            if input_entry is None:
                break

            # tick policy-aware scenes
            for entry in self.services.scenes.update_entries():
                scene = entry.scene
                effective_input = (
                    input_frame
                    if entry is input_entry
                    else _neutral_input(frame_index, dt)
                )

                packet = scene.tick(effective_input, dt)
                packet_cache[id(scene)] = packet

            backend.begin_frame()
            for entry in self.services.scenes.visible_entries():
                scene = entry.scene
                packet = packet_cache.get(id(scene))
                if packet is None:
                    # bootstrap (first frame visible but not updated)
                    packet = scene.tick(_neutral_input(frame_index, 0.0), 0.0)
                    packet_cache[id(scene)] = packet

                pipeline.draw_packet(backend, packet)
            backend.end_frame()

            # Execute commands at the end of the frame (consistent write path)
            for cmd in self._commands.drain():
                cmd.execute(self.services)

            if target_dt > 0 and dt < target_dt:
                sleep(target_dt - dt)

            frame_index += 1

        # exit remaining scenes
        self.services.scenes.clean()

    def run_sim(
        self,
        initial_scene_id: str,
        *,
        cfg: SimRunnerConfig | None = None,
    ) -> None:
        """
        Run the simulation-first loop using the already configured backend + services.

        This keeps Game as the composition root. No duplicate setup elsewhere.
        """
        backend = self.backend

        # reuse window setup from classic run (same behavior)
        if self.config.window is None:
            raise ValueError("GameConfig.window must be set")

        self.services.window.set_window_size(
            self.config.window.width, self.config.window.height
        )
        self.services.window.set_title(self.config.window.title)

        br, bg, bb = self.config.window.background_color
        self.services.window.set_clear_color(br, bg, bb)

        # run the sim loop
        runner = SimRunner(
            backend=backend,
            services=self.services,
            render_pipeline=RenderPipeline(),
        )
        runner.run(initial_scene_id, cfg=cfg)

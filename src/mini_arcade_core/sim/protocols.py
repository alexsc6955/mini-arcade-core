from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core.render import RenderPacket
from mini_arcade_core.runtime.context import RuntimeContext
from mini_arcade_core.runtime.input_frame import InputFrame


@dataclass
class SimScene:
    """
    Simulation-first scene protocol.

    tick() advances the simulation and returns a RenderPacket for this scene.
    """

    context: RuntimeContext

    def on_enter(self) -> None: ...
    def on_exit(self) -> None: ...

    def tick(self, input_frame: InputFrame, dt: float) -> RenderPacket: ...

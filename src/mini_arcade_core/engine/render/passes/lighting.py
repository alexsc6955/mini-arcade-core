# mini_arcade_core/engine/render/passes/lighting.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class LightingPass:
    name: str = "LightingPass"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        # hook/no-op for now
        return
        return

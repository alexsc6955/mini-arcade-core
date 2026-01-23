# mini_arcade_core/engine/render/passes/end_frame.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class EndFramePass:
    name: str = "EndFrame"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        backend.end_frame()
        backend.end_frame()

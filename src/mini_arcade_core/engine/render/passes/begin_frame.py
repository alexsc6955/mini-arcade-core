# mini_arcade_core/engine/render/passes/begin_frame.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class BeginFramePass:
    name: str = "BeginFrame"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        backend.begin_frame()
        backend.begin_frame()

# mini_arcade_core/engine/render/passes/postfx.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class PostFXPass:
    name: str = "PostFXPass"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        # hook/no-op for now (CRT later)
        return
        return

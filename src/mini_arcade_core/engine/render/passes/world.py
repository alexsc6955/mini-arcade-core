# mini_arcade_core/engine/render/passes/world.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class WorldPass:
    name: str = "WorldPass"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        # world packets default path
        for packet in packets:
            if not packet or not packet.ops:
                continue

            # stats (approx ok)
            ctx.stats.packets += 1
            ctx.stats.ops += len(packet.ops)
            ctx.stats.draw_groups += 1  # approx: 1 group per packet

            backend.set_viewport_transform(
                ctx.viewport.offset_x,
                ctx.viewport.offset_y,
                ctx.viewport.scale,
            )
            backend.set_clip_rect(
                ctx.viewport.offset_x,
                ctx.viewport.offset_y,
                ctx.viewport.viewport_w,
                ctx.viewport.viewport_h,
            )
            try:
                for op in packet.ops:
                    op(backend)
            finally:
                backend.clear_clip_rect()
                backend.clear_viewport_transform()
                backend.clear_viewport_transform()

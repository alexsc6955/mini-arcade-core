# mini_arcade_core/engine/render/passes/ui.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.frame_packet import FramePacket


@dataclass
class UIPass:
    name: str = "UIPass"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[FramePacket]
    ) -> None:
        # UI overlays should be screen-space (no world transform / no clip unless you want it)
        backend.clear_viewport_transform()
        backend.clear_clip_rect()

        for fp in packets:
            if not fp.is_overlay:
                continue
            if not fp.packet or not fp.packet.ops:
                continue

            # count overlays too (optional; I’d count them)
            ctx.stats.packets += 1
            ctx.stats.renderables += len(fp.packet.ops)
            ctx.stats.draw_groups += 1

            for op in fp.packet.ops:
                op(backend)

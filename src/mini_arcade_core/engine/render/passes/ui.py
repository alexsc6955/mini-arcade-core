# mini_arcade_core/engine/render/passes/ui.py
from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass
class UIPass:
    name: str = "UIPass"

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None:
        if not ctx.debug_overlay:
            return

        # ensure screen-space
        backend.clear_clip_rect()
        backend.clear_viewport_transform()

        y = 8
        backend.draw_text(8, y, f"{ctx.frame_ms:.2f}ms", color=(200, 200, 200))
        y += 18
        backend.draw_text(
            8, y, f"packets: {ctx.stats.packets}", color=(200, 200, 200)
        )
        y += 18
        backend.draw_text(
            8, y, f"renderables: {ctx.stats.ops}", color=(200, 200, 200)
        )
        y += 18
        backend.draw_text(
            8,
            y,
            f"draw_groups~: {ctx.stats.draw_groups}",
            color=(200, 200, 200),
        )

# mini_arcade_core/engine/render/passes/base.py
from __future__ import annotations

from typing import Protocol

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.context import RenderContext
from mini_arcade_core.engine.render.packet import RenderPacket


class RenderPass(Protocol):
    name: str

    def run(
        self, backend: Backend, ctx: RenderContext, packets: list[RenderPacket]
    ) -> None: ...

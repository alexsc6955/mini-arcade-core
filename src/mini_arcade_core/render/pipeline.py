from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.render.packet import RenderPacket


@dataclass
class RenderPipeline:
    """
    Minimal pipeline for v1.

    Later you can expand this into passes:
      - build draw list
      - cull
      - sort
      - backend draw pass
    """

    def draw_packet(self, backend: Backend, packet: RenderPacket) -> None:
        if not packet:
            return
        for op in packet.ops:
            op(backend)

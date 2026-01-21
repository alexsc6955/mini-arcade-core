"""
Render pipeline module.
Defines the RenderPipeline class for rendering RenderPackets.
"""

from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core.backend import Backend
from mini_arcade_core.engine.render.packet import RenderPacket


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

    def draw_packet(self, backend: Backend, packet: RenderPacket):
        """
        Draw the given RenderPacket using the provided Backend.

        :param backend: Backend to use for drawing.
        :type backend: Backend

        :param packet: RenderPacket to draw.
        :type packet: RenderPacket
        """
        if not packet:
            return
        for op in packet.ops:
            op(backend)

# mini_arcade_core/engine/render/frame_packet.py
from __future__ import annotations
from dataclasses import dataclass

from mini_arcade_core.engine.render.packet import RenderPacket


@dataclass(frozen=True)
class FramePacket:
    scene_id: str
    is_overlay: bool
    packet: RenderPacket

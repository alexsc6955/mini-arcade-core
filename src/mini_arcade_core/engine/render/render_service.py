# mini_arcade_core/runtime/render/render_service.py
from __future__ import annotations
from dataclasses import dataclass
from mini_arcade_core.engine.render.context import RenderStats


@dataclass
class RenderService:
    last_frame_ms: float = 0.0
    last_stats: RenderStats = RenderStats()

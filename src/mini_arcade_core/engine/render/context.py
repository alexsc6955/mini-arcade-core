# mini_arcade_core/engine/render/context.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from mini_arcade_core.engine.render.viewport import ViewportState


@dataclass
class RenderStats:
    packets: int = 0
    ops: int = 0
    draw_groups: int = 0  # approx ok


@dataclass
class RenderContext:
    viewport: ViewportState
    debug_overlay: bool = False
    frame_ms: float = 0.0
    stats: RenderStats = field(default_factory=RenderStats)
    meta: dict[str, Any] = field(default_factory=dict)

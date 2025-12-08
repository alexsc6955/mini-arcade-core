from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Velocity2D:
    vx: Optional[float] = 0.0
    vy: Optional[float] = 0.0

    def advance(self, x: float, y: float, dt: float) -> tuple[float, float]:
        """Return new (x, y) after dt seconds."""
        return x + self.vx * dt, y + self.vy * dt

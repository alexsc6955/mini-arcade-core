from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position2D:
    x: float
    y: float


@dataclass
class Size2D:
    width: int
    height: int

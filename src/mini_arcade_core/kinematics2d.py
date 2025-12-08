"""
Entity base classes for mini_arcade_core.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from mini_arcade_core.geometry2d import Position2D, Size2D
from mini_arcade_core.physics2d import Velocity2D

Color = Union[tuple[int, int, int], tuple[int, int, int, int]]


@dataclass
class KinematicData:
    position: Position2D
    size: Size2D
    velocity: Velocity2D
    color: Optional[Color] = None  # future use

    @classmethod
    def rect(
        cls,
        x: float,
        y: float,
        width: int,
        height: int,
        vx: float = 0.0,
        vy: float = 0.0,
        color: Optional[Color] = None,
    ) -> "KinematicData":
        return cls(
            position=Position2D(float(x), float(y)),
            size=Size2D(int(width), int(height)),
            velocity=Velocity2D(float(vx), float(vy)),
            color=color,
        )

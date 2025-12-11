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


@dataclass
class Bounds2D:
    """
    Axis-aligned rectangular bounds in world space.
    (left, top) .. (right, bottom)
    """

    left: float
    top: float
    right: float
    bottom: float

    @classmethod
    def from_size(cls, size: "Size2D") -> "Bounds2D":
        """
        Convenience factory for screen/world bounds starting at (0, 0).
        """
        return cls(
            left=0.0,
            top=0.0,
            right=float(size.width),
            bottom=float(size.height),
        )

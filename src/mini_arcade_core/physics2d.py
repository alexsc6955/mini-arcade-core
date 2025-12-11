from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Velocity2D:
    vx: float = 0.0
    vy: float = 0.0

    def advance(self, x: float, y: float, dt: float) -> tuple[float, float]:
        """Return new (x, y) after dt seconds."""
        return x + self.vx * dt, y + self.vy * dt

    def stop(self) -> None:
        """Stop movement in both axes."""
        self.vx = 0.0
        self.vy = 0.0

    def stop_x(self) -> None:
        """Stop horizontal movement."""
        self.vx = 0.0

    def stop_y(self) -> None:
        """Stop vertical movement."""
        self.vy = 0.0

    def move_up(self, speed: float) -> None:
        """Set vertical velocity upwards (negative Y)."""
        self.vy = -abs(speed)

    def move_down(self, speed: float) -> None:
        """Set vertical velocity downwards (positive Y)."""
        self.vy = abs(speed)

    def move_left(self, speed: float) -> None:
        """Set horizontal velocity to the left (negative X)."""
        self.vx = -abs(speed)

    def move_right(self, speed: float) -> None:
        """Set horizontal velocity to the right (positive X)."""
        self.vx = abs(speed)

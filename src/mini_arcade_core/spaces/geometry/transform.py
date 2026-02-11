from __future__ import annotations

from dataclasses import dataclass, field

from mini_arcade_core.spaces.geometry.rect import Rect
from mini_arcade_core.spaces.geometry.size import Size2D
from mini_arcade_core.spaces.math.vec2 import Vec2


@dataclass
class Transform2D:
    center: Vec2
    size: Size2D
    _pos: Vec2 = field(init=False)

    def __post_init__(self):
        self._pos = Vec2(0.0, 0.0)
        self._recalc_pos()

    @property
    def position(self) -> Vec2:
        return self._pos

    @position.setter
    def position(self, pos: Vec2) -> None:
        self._pos.x = pos.x
        self._pos.y = pos.y
        self.center.x = self._pos.x + self.size.width * 0.5
        self.center.y = self._pos.y + self.size.height * 0.5

    @property
    def rect(self) -> Rect:
        return Rect(self._pos, self.size)

    def _recalc_pos(self) -> None:
        self._pos.x = self.center.x - self.size.width * 0.5
        self._pos.y = self.center.y - self.size.height * 0.5

    def move_center_scaled(self, velocity: Vec2, dt: float) -> None:
        self.center.x += velocity.x * dt
        self.center.y += velocity.y * dt
        self._recalc_pos()

    def move_center(self, delta: Vec2) -> None:
        self.center += delta
        self._recalc_pos()

    def set_center(self, center: Vec2) -> None:
        self.center.x = center.x
        self.center.y = center.y
        self._recalc_pos()

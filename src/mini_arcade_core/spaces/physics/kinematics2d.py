from __future__ import annotations

from dataclasses import dataclass, field

from mini_arcade_core.spaces.collision.rect_collider import RectCollider
from mini_arcade_core.spaces.geometry.rect import Rect
from mini_arcade_core.spaces.geometry.size import Size2D
from mini_arcade_core.spaces.geometry.transform import Transform2D
from mini_arcade_core.spaces.math.vec2 import Vec2


@dataclass
class Kinematic2D:
    transform: Transform2D
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    collider: RectCollider = field(init=False)
    speed: float = 0.0

    def __post_init__(self):
        self.collider = RectCollider(
            self.transform.position, self.transform.size
        )

    def step(self, dt: float) -> None:
        self.transform.move_center_scaled(self.velocity, dt)

    @property
    def rect(self) -> Rect:
        return self.transform.rect

    @property
    def center(self) -> Vec2:
        return self.transform.center

    @property
    def size(self) -> Size2D:
        return self.transform.size

    @property
    def position(self) -> Vec2:
        return self.transform.position

    @position.setter
    def position(self, pos: Vec2) -> None:
        self.transform.position = pos

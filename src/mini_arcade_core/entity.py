"""
Entity base classes for mini_arcade_core.
"""

from __future__ import annotations

from typing import Any

from mini_arcade_core.collision2d import RectCollider
from mini_arcade_core.geometry2d import Position2D, Size2D
from mini_arcade_core.kinematics2d import KinematicData
from mini_arcade_core.physics2d import Velocity2D


class Entity:
    """Entity base class for game objects."""

    def update(self, dt: float):
        """
        Advance the entity state by ``dt`` seconds.

        :param dt: Time delta in seconds.
        :type dt: float
        """

    def draw(self, surface: Any):
        """
        Render the entity to the given surface.

        :param surface: The surface to draw on.
        :type surface: Any
        """


class SpriteEntity(Entity):
    """Entity with position and size."""

    def __init__(self, position: Position2D, size: Size2D):
        """
        :param x: X position.
        :type x: float

        :param y: Y position.
        :type y: float

        :param width: Width of the entity.
        :type width: int

        :param height: Height of the entity.
        :type height: int
        """
        self.position = Position2D(float(position.x), float(position.y))
        self.size = Size2D(int(size.width), int(size.height))
        self.collider = RectCollider(self.position, self.size)


class KinematicEntity(SpriteEntity):
    """SpriteEntity with velocity-based movement."""

    def __init__(self, kinematic_data: KinematicData):
        super().__init__(
            position=kinematic_data.position,
            size=kinematic_data.size,
        )

        self.velocity = Velocity2D(
            vx=kinematic_data.velocity.vx,
            vy=kinematic_data.velocity.vy,
        )

    def update(self, dt: float) -> None:
        self.position.x, self.position.y = self.velocity.advance(
            self.position.x, self.position.y, dt
        )

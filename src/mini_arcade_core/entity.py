"""
Entity base classes for mini_arcade_core.
"""

from __future__ import annotations

from typing import Any

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

    # TODO: Remove compatibility layer in future versions
    @property
    def x(self) -> float:
        return self.position.x

    @x.setter
    def x(self, value: float) -> None:
        self.position.x = float(value)

    @property
    def y(self) -> float:
        return self.position.y

    @y.setter
    def y(self, value: float) -> None:
        self.position.y = float(value)

    @property
    def width(self) -> int:
        return self.size.width

    @width.setter
    def width(self, value: int) -> None:
        self.size.width = int(value)

    @property
    def height(self) -> int:
        return self.size.height

    @height.setter
    def height(self, value: int) -> None:
        self.size.height = int(value)


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

    # optional compatibility layer: vx / vy properties
    @property
    def vx(self) -> float:
        return self.velocity.vx

    @vx.setter
    def vx(self, value: float) -> None:
        self.velocity.vx = value

    @property
    def vy(self) -> float:
        return self.velocity.vy

    @vy.setter
    def vy(self, value: float) -> None:
        self.velocity.vy = value

    def update(self, dt: float) -> None:
        self.x, self.y = self.velocity.advance(self.x, self.y, dt)

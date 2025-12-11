from __future__ import annotations

from typing import Any

import pytest

from mini_arcade_core import (
    Entity,
    SpriteEntity,
    KinematicEntity,
    Position2D,
    Size2D,
    KinematicData,
    Velocity2D,
)


# -------------------------
# I/O tests
# -------------------------


def test_sprite_entity_initialization():
    """I/O: SpriteEntity should correctly store position and size."""
    pos = Position2D(10.5, 20.25)
    size = Size2D(32, 16)

    sprite = SpriteEntity(position=pos, size=size)

    assert sprite.position.x == 10.5
    assert sprite.position.y == 20.25
    assert sprite.size.width == 32
    assert sprite.size.height == 16


def test_entity_has_update_and_draw():
    """I/O: Entity base class exposes update/draw methods without error."""
    ent = Entity()

    class DummySurface:
        def __init__(self):
            self.draw_calls: list[Any] = []

    surface = DummySurface()

    # Methods are no-ops by default but must exist.
    ent.update(0.016)
    ent.draw(surface)


# -------------------------
# Edge cases
# -------------------------


def test_sprite_entity_accepts_negative_or_zero_values():
    """
    Edge case: SpriteEntity currently does not validate width/height/position.
    Construction with unusual values should still succeed.
    """
    pos = Position2D(-5.0, 0.0)
    size = Size2D(0, -10)

    sprite = SpriteEntity(position=pos, size=size)

    assert sprite.position.x == -5.0
    assert sprite.position.y == 0.0
    assert sprite.size.width == 0
    assert sprite.size.height == -10


# -------------------------
# Side effects for generic Entity
# -------------------------


def test_custom_entity_can_apply_side_effects_on_update_and_draw():
    """
    Side effect: verify that a custom Entity can modify state and
    interact with a drawing surface.
    """

    class DummySurface:
        def __init__(self):
            self.draw_calls: list[tuple[float, float]] = []

    class MovingEntity(Entity):
        def __init__(self):
            self.x = 0.0
            self.y = 0.0
            self.speed = 10.0

        def update(self, dt: float):
            self.x += self.speed * dt
            self.y += self.speed * dt

        def draw(self, surface: DummySurface):  # type: ignore[override]
            surface.draw_calls.append((self.x, self.y))

    surface = DummySurface()
    ent = MovingEntity()

    ent.update(0.5)  # move by 5 units on both axes
    ent.draw(surface)

    assert ent.x == 5.0
    assert ent.y == 5.0
    assert surface.draw_calls == [(5.0, 5.0)]


# -------------------------
# KinematicEntity tests
# -------------------------


def test_kinematic_entity_uses_velocity_to_advance_position():
    """
    I/O: KinematicEntity.update should move according to its velocity.
    """
    data = KinematicData.rect(
        x=0.0,
        y=0.0,
        width=10,
        height=10,
        vx=10.0,
        vy=5.0,
    )
    ent = KinematicEntity(data)

    ent.update(0.5)  # half a second

    assert ent.position.x == pytest.approx(5.0)
    assert ent.position.y == pytest.approx(2.5)


def test_kinematic_entity_shares_velocity_object_from_kinematic_data():
    """
    Side effect: KinematicEntity should reference the same Velocity2D
    object held in KinematicData, so external changes are reflected.
    """
    vel = Velocity2D(vx=0.0, vy=0.0)
    data = KinematicData(
        position=Position2D(0.0, 0.0),
        size=Size2D(10, 10),
        velocity=vel,
    )

    ent = KinematicEntity(data)

    # Same object
    assert ent.velocity is vel

    # Change velocity after construction and update
    vel.vx = 20.0
    vel.vy = 0.0

    ent.update(0.5)
    assert ent.position.x == pytest.approx(10.0)
    assert ent.position.y == pytest.approx(0.0)

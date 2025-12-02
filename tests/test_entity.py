from __future__ import annotations

from typing import Any

from mini_arcade_core import Entity, SpriteEntity

# -------------------------
# I/O tests
# -------------------------


def test_sprite_entity_initialization():
    """I/O: SpriteEntity should correctly store position and size."""
    sprite = SpriteEntity(x=10.5, y=20.25, width=32, height=16)
    assert sprite.x == 10.5
    assert sprite.y == 20.25
    assert sprite.width == 32
    assert sprite.height == 16


def test_entity_has_update_and_draw():
    """I/O: Entity base class exposes update/draw methods without error."""
    ent = Entity()

    class DummySurface:
        def __init__(self) -> None:
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
    sprite = SpriteEntity(x=-5.0, y=0.0, width=0, height=-10)
    assert sprite.x == -5.0
    assert sprite.y == 0.0
    assert sprite.width == 0
    assert sprite.height == -10


# -------------------------
# Side effects
# -------------------------


def test_custom_entity_can_apply_side_effects_on_update_and_draw():
    """
    Side effect: verify that a custom Entity can modify state and
    interact with a drawing surface.
    """

    class DummySurface:
        def __init__(self) -> None:
            self.draw_calls: list[tuple[float, float]] = []

    class MovingEntity(Entity):
        def __init__(self) -> None:
            self.x = 0.0
            self.y = 0.0
            self.speed = 10.0

        def update(self, dt: float) -> None:
            self.x += self.speed * dt
            self.y += self.speed * dt

        def draw(self, surface: DummySurface) -> None:  # type: ignore[override]
            surface.draw_calls.append((self.x, self.y))

    surface = DummySurface()
    ent = MovingEntity()

    ent.update(0.5)  # move by 5 units on both axes
    ent.draw(surface)

    assert ent.x == 5.0
    assert ent.y == 5.0
    assert surface.draw_calls == [(5.0, 5.0)]

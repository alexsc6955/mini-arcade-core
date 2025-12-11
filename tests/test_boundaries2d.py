from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core import (
    Bounds2D,
    Position2D,
    Size2D,
    VerticalBounce,
    VerticalWrap,
)

# -------------------------------------------------------------------
# Test doubles for the Protocols
# -------------------------------------------------------------------


@dataclass
class DummyKinematic:
    """Simple RectKinematic-compatible object."""

    position: Position2D
    size: Size2D
    velocity: "Velocity2D"


@dataclass
class Velocity2D:
    vx: float = 0.0
    vy: float = 0.0


@dataclass
class DummySprite:
    """Simple RectSprite-compatible object."""

    position: Position2D
    size: Size2D


# -------------------------
# I/O: VerticalBounce
# -------------------------


def test_vertical_bounce_bounces_at_top():
    """
    I/O + side effect: when an object goes above the top bound,
    it should be snapped to top and its vy inverted.
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    obj = DummyKinematic(
        position=Position2D(x=10.0, y=-5.0),
        size=Size2D(width=10, height=10),
        velocity=Velocity2D(vx=0.0, vy=50.0),
    )

    VerticalBounce(bounds).apply(obj)

    assert obj.position.y == bounds.top
    assert obj.velocity.vy == -50.0


def test_vertical_bounce_bounces_at_bottom():
    """
    I/O + side effect: when an object goes below the bottom bound,
    it should be snapped to bottom - height and its vy inverted.
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    obj = DummyKinematic(
        position=Position2D(x=10.0, y=95.0),  # 95 + 10 = 105 > bottom
        size=Size2D(width=10, height=10),
        velocity=Velocity2D(vx=0.0, vy=-30.0),
    )

    VerticalBounce(bounds).apply(obj)

    assert obj.position.y == bounds.bottom - obj.size.height  # 90
    assert obj.velocity.vy == 30.0


def test_vertical_bounce_no_change_inside_bounds():
    """Edge case: object fully inside vertical bounds should remain unchanged."""
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    obj = DummyKinematic(
        position=Position2D(x=10.0, y=20.0),
        size=Size2D(width=10, height=10),
        velocity=Velocity2D(vx=0.0, vy=5.0),
    )

    VerticalBounce(bounds).apply(obj)

    assert obj.position.y == 20.0
    assert obj.velocity.vy == 5.0


def test_vertical_bounce_triggers_on_exact_edges():
    """
    Edge case: y == top or y + height == bottom should also trigger
    bounce logic (because of <= and >= checks).
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)

    # Exact top
    obj_top = DummyKinematic(
        position=Position2D(x=10.0, y=0.0),
        size=Size2D(width=10, height=10),
        velocity=Velocity2D(vx=0.0, vy=-10.0),
    )
    VerticalBounce(bounds).apply(obj_top)
    assert obj_top.position.y == 0.0
    assert obj_top.velocity.vy == 10.0

    # Exact bottom
    obj_bottom = DummyKinematic(
        position=Position2D(x=10.0, y=90.0),  # 90 + 10 == bottom
        size=Size2D(width=10, height=10),
        velocity=Velocity2D(vx=0.0, vy=10.0),
    )
    VerticalBounce(bounds).apply(obj_bottom)
    assert obj_bottom.position.y == 90.0
    assert obj_bottom.velocity.vy == -10.0


# -------------------------
# I/O: VerticalWrap
# -------------------------


def test_vertical_wrap_from_above_appears_at_bottom():
    """
    I/O + side effect: if object is completely above top (bottom < top),
    it should reappear at bottom.
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    sprite = DummySprite(
        position=Position2D(x=10.0, y=-15.0),  # -15 + 10 = -5 < top
        size=Size2D(width=10, height=10),
    )

    VerticalWrap(bounds).apply(sprite)

    assert sprite.position.y == bounds.bottom  # 100


def test_vertical_wrap_from_below_appears_at_top_minus_height():
    """
    I/O + side effect: if object is completely below bottom (y > bottom),
    it should reappear at top - height.
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    sprite = DummySprite(
        position=Position2D(x=10.0, y=110.0),
        size=Size2D(width=10, height=10),
    )

    VerticalWrap(bounds).apply(sprite)

    assert sprite.position.y == bounds.top - sprite.size.height  # -10


def test_vertical_wrap_does_not_trigger_when_partially_outside():
    """
    Edge case: objects that are only partially outside (not fully above or
    below) should NOT wrap.
    """
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)

    # Partially above: bottom >= top
    sprite_above = DummySprite(
        position=Position2D(x=10.0, y=-5.0),  # -5 + 10 = 5 >= 0
        size=Size2D(width=10, height=10),
    )

    # Partially below: y <= bottom
    sprite_below = DummySprite(
        position=Position2D(x=10.0, y=95.0),  # 95 <= 100
        size=Size2D(width=10, height=10),
    )

    VerticalWrap(bounds).apply(sprite_above)
    VerticalWrap(bounds).apply(sprite_below)

    assert sprite_above.position.y == -5.0
    assert sprite_below.position.y == 95.0


def test_vertical_wrap_no_change_inside_bounds():
    """Edge case: object fully inside bounds should not move."""
    bounds = Bounds2D(left=0.0, top=0.0, right=100.0, bottom=100.0)
    sprite = DummySprite(
        position=Position2D(x=10.0, y=20.0),
        size=Size2D(width=10, height=10),
    )

    VerticalWrap(bounds).apply(sprite)

    assert sprite.position.y == 20.0


# -------------------------
# Bounds2D convenience
# -------------------------


def test_bounds2d_from_size_helper():
    """I/O: Bounds2D.from_size should build bounds starting at (0, 0)."""
    size = Size2D(width=800, height=600)
    bounds = Bounds2D.from_size(size)

    assert bounds.left == 0.0
    assert bounds.top == 0.0
    assert bounds.right == 800.0
    assert bounds.bottom == 600.0

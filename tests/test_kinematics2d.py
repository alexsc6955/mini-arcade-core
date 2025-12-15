from __future__ import annotations

from mini_arcade_core import KinematicData, Position2D, Size2D, Velocity2D

# -------------------------
# I/O tests
# -------------------------


def test_kinematicdata_direct_construction():
    """I/O: KinematicData should store position, size, velocity, and color."""
    pos = Position2D(10.5, 20.25)
    size = Size2D(32, 16)
    vel = Velocity2D(1.0, -2.0)
    color = (255, 0, 0)

    kd = KinematicData(position=pos, size=size, velocity=vel, color=color)

    assert kd.position is pos
    assert kd.size is size
    assert kd.velocity is vel
    assert kd.color == color


def test_kinematicdata_rect_factory_basic():
    """I/O: KinematicData.rect should build a valid structure with correct types."""
    kd = KinematicData.rect(
        x=5.0,
        y=7.5,
        width=64,
        height=48,
        vx=100.0,
        vy=-50.0,
    )

    # Position/size are converted to the expected types
    assert isinstance(kd.position, Position2D)
    assert isinstance(kd.size, Size2D)
    assert isinstance(kd.velocity, Velocity2D)

    assert kd.position.x == 5.0
    assert kd.position.y == 7.5
    assert kd.size.width == 64
    assert kd.size.height == 48
    assert kd.velocity.vx == 100.0
    assert kd.velocity.vy == -50.0
    assert kd.color is None  # default


def test_kinematicdata_rect_with_color():
    """I/O: KinematicData.rect should accept an optional color argument."""
    color = (255, 255, 0, 128)  # RGBA
    kd = KinematicData.rect(
        x=0.0,
        y=0.0,
        width=10,
        height=10,
        vx=0.0,
        vy=0.0,
        color=color,
    )

    assert kd.color == color


# -------------------------
# Edge cases
# -------------------------


def test_kinematicdata_rect_accepts_negative_and_zero_values():
    """
    Edge case: KinematicData.rect does not validate dimensions or velocity.
    It should still construct successfully with unusual values.
    """
    kd = KinematicData.rect(
        x=-5.5,
        y=0.0,
        width=0,
        height=-10,
        vx=-1.0,
        vy=0.0,
    )

    assert kd.position.x == -5.5
    assert kd.position.y == 0.0
    assert kd.size.width == 0
    assert kd.size.height == -10
    assert kd.velocity.vx == -1.0
    assert kd.velocity.vy == 0.0


# -------------------------
# Side effects / behavior
# -------------------------


def test_kinematicdata_velocity_can_advance_position():
    """
    Side effect: Using Velocity2D.advance with KinematicData values
    should move the position as expected.
    """
    kd = KinematicData.rect(
        x=10.0,
        y=20.0,
        width=16,
        height=16,
        vx=50.0,
        vy=-25.0,
    )

    x2, y2 = kd.velocity.advance(kd.position.x, kd.position.y, dt=0.5)

    # x = 10 + 50 * 0.5 = 35
    # y = 20 + (-25) * 0.5 = 7.5
    assert x2 == 35.0
    assert y2 == 7.5

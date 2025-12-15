from __future__ import annotations

from mini_arcade_core import Velocity2D

# -------------------------
# I/O tests
# -------------------------


def test_velocity2d_defaults():
    """I/O: Velocity2D should default to zero velocity on both axes."""
    v = Velocity2D()
    assert v.vx == 0.0
    assert v.vy == 0.0


def test_velocity2d_custom_initialization():
    """I/O: Velocity2D should accept custom vx/vy values."""
    v = Velocity2D(vx=10.5, vy=-3.25)
    assert v.vx == 10.5
    assert v.vy == -3.25


def test_velocity2d_advance_basic():
    """I/O: advance should move a point according to vx, vy and dt."""
    v = Velocity2D(vx=2.0, vy=-4.0)
    x2, y2 = v.advance(x=1.0, y=10.0, dt=0.5)
    # x = 1 + 2 * 0.5 = 2.0
    # y = 10 + (-4) * 0.5 = 8.0
    assert x2 == 2.0
    assert y2 == 8.0


# -------------------------
# Edge cases
# -------------------------


def test_velocity2d_advance_zero_dt():
    """Edge case: advance with dt=0 should not change position."""
    v = Velocity2D(vx=100.0, vy=-50.0)
    x2, y2 = v.advance(x=5.0, y=7.0, dt=0.0)
    assert x2 == 5.0
    assert y2 == 7.0


def test_velocity2d_advance_zero_velocity():
    """Edge case: advance with zero velocity should not move the point."""
    v = Velocity2D(vx=0.0, vy=0.0)
    x2, y2 = v.advance(x=-3.0, y=4.0, dt=1.0)
    assert x2 == -3.0
    assert y2 == 4.0


# -------------------------
# Side effects / behavior
# -------------------------


def test_velocity2d_stop_resets_both_axes():
    """Side effect: stop() should zero out vx and vy."""
    v = Velocity2D(vx=5.0, vy=-7.0)
    v.stop()
    assert v.vx == 0.0
    assert v.vy == 0.0


def test_velocity2d_stop_x_and_stop_y():
    """Side effect: stop_x/stop_y should only affect their respective axes."""
    v = Velocity2D(vx=3.0, vy=-4.0)

    v.stop_x()
    assert v.vx == 0.0
    assert v.vy == -4.0

    v.stop_y()
    assert v.vx == 0.0
    assert v.vy == 0.0


def test_velocity2d_move_direction_helpers_set_correct_signs():
    """
    Side effect: move_up/down/left/right should set signs correctly and
    use the absolute value of speed.
    """
    v = Velocity2D()

    v.move_up(10.0)
    assert v.vy == -10.0

    v.move_down(10.0)
    assert v.vy == 10.0

    v.move_left(5.0)
    assert v.vx == -5.0

    v.move_right(5.0)
    assert v.vx == 5.0


def test_velocity2d_move_direction_helpers_normalize_speed_sign():
    """
    Side effect: passing a negative speed to direction helpers should still
    result in the correct sign.
    """
    v = Velocity2D()

    v.move_up(-8.0)
    assert v.vy == -8.0  # still upwards (negative)

    v.move_down(-8.0)
    assert v.vy == 8.0  # downwards (positive)

    v.move_left(-2.5)
    assert v.vx == -2.5  # left (negative)

    v.move_right(-2.5)
    assert v.vx == 2.5  # right (positive)

from __future__ import annotations

from mini_arcade_core.two_d.geometry2d import Bounds2D, Position2D, Size2D

# -------------------------
# I/O tests
# -------------------------


def test_position2d_initialization():
    """I/O: Position2D should store x and y as given."""
    pos = Position2D(x=10.5, y=-3.25)
    assert pos.x == 10.5
    assert pos.y == -3.25


def test_size2d_initialization():
    """I/O: Size2D should store width and height as given."""
    size = Size2D(width=320, height=240)
    assert size.width == 320
    assert size.height == 240


def test_bounds2d_initialization():
    """I/O: Bounds2D should store left, top, right, bottom as given."""
    bounds = Bounds2D(left=1.0, top=2.0, right=3.0, bottom=4.0)
    assert bounds.left == 1.0
    assert bounds.top == 2.0
    assert bounds.right == 3.0
    assert bounds.bottom == 4.0


def test_bounds2d_from_size_creates_zero_based_bounds():
    """
    I/O: Bounds2D.from_size should create bounds starting at (0, 0)
    and ending at (width, height) as floats.
    """
    size = Size2D(width=800, height=600)
    bounds = Bounds2D.from_size(size)

    assert bounds.left == 0.0
    assert bounds.top == 0.0
    assert bounds.right == 800.0
    assert bounds.bottom == 600.0
    assert isinstance(bounds.right, float)
    assert isinstance(bounds.bottom, float)


# -------------------------
# Edge cases
# -------------------------


def test_bounds2d_from_size_accepts_zero_or_negative_values():
    """
    Edge case: Bounds2D.from_size does not validate width/height.
    It should still construct even for unusual values.
    """
    size = Size2D(width=-10, height=0)
    bounds = Bounds2D.from_size(size)

    # Right/bottom are still derived directly as floats from size
    assert bounds.left == 0.0
    assert bounds.top == 0.0
    assert bounds.right == -10.0
    assert bounds.bottom == 0.0

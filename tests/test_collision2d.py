from __future__ import annotations

from mini_arcade_core.geometry2d import Position2D, Size2D
from mini_arcade_core.collision2d import _rects_intersect, RectCollider


# -------------------------
# I/O tests for _rects_intersect
# -------------------------


def test_rects_intersect_overlapping_rectangles():
    """
    I/O: two clearly overlapping rectangles should report intersection.
    """
    pos_a = Position2D(10.0, 10.0)
    size_a = Size2D(20, 20)

    pos_b = Position2D(15.0, 15.0)
    size_b = Size2D(20, 20)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is True


def test_rects_do_not_intersect_when_separated_horizontally():
    """
    I/O: rectangles separated on the X axis should not intersect.
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(10, 10)

    pos_b = Position2D(20.0, 0.0)  # to the right of A, with a gap
    size_b = Size2D(10, 10)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is False


def test_rects_do_not_intersect_when_separated_vertically():
    """
    I/O: rectangles separated on the Y axis should not intersect.
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(10, 10)

    pos_b = Position2D(0.0, 20.0)  # below A, with a gap
    size_b = Size2D(10, 10)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is False


# -------------------------
# Edge cases for _rects_intersect
# -------------------------


def test_rects_intersect_when_touching_edges_horizontally():
    """
    Edge case: when A's right edge == B's left edge, they should
    still count as intersecting (no gap).
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(10, 10)

    # A: [0, 10], B: [10, 20] -> right of A == left of B
    pos_b = Position2D(10.0, 0.0)
    size_b = Size2D(10, 10)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is True


def test_rects_intersect_when_touching_edges_vertically():
    """
    Edge case: when A's bottom edge == B's top edge, they should
    still count as intersecting (no gap).
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(10, 10)

    # A: [0,10] vertically, B: [10,20]
    pos_b = Position2D(0.0, 10.0)
    size_b = Size2D(10, 10)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is True


def test_rects_with_zero_size_still_intersect_when_overlapping_point():
    """
    Edge case: a zero-size rectangle located inside another rect
    should be treated as intersecting (no separating axis).
    """
    pos_a = Position2D(5.0, 5.0)
    size_a = Size2D(0, 0)  # degenerate rect

    pos_b = Position2D(0.0, 0.0)
    size_b = Size2D(10, 10)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is True


def test_rects_with_zero_size_far_apart_do_not_intersect():
    """
    Edge case: zero-size rectangles far apart should not intersect.
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(0, 0)

    pos_b = Position2D(100.0, 100.0)
    size_b = Size2D(0, 0)

    assert _rects_intersect(pos_a, size_a, pos_b, size_b) is False


# -------------------------
# I/O + side effects for RectCollider
# -------------------------


def test_rect_collider_intersects_delegates_to_rects_intersect():
    """
    I/O: RectCollider.intersects should reflect the same logic as _rects_intersect.
    """
    collider_a = RectCollider(
        position=Position2D(0.0, 0.0),
        size=Size2D(10, 10),
    )
    collider_b = RectCollider(
        position=Position2D(5.0, 5.0),
        size=Size2D(10, 10),
    )

    assert collider_a.intersects(collider_b) is True
    assert collider_b.intersects(collider_a) is True


def test_rect_collider_tracks_position_changes():
    """
    Side effect: RectCollider does not own the Position2D, it references it.
    If the position changes, collision results should change accordingly.
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(10, 10)
    collider_a = RectCollider(position=pos_a, size=size_a)

    pos_b = Position2D(30.0, 0.0)
    size_b = Size2D(10, 10)
    collider_b = RectCollider(position=pos_b, size=size_b)

    # Initially separated
    assert collider_a.intersects(collider_b) is False

    # Move A so that it overlaps B
    pos_a.x = 25.0  # 25..35 overlaps 30..40
    assert collider_a.intersects(collider_b) is True


def test_rect_collider_tracks_size_changes():
    """
    Side effect: changing Size2D referenced by RectCollider should also affect
    intersection results.
    """
    pos_a = Position2D(0.0, 0.0)
    size_a = Size2D(5, 5)
    collider_a = RectCollider(position=pos_a, size=size_a)

    pos_b = Position2D(10.0, 0.0)
    size_b = Size2D(10, 10)
    collider_b = RectCollider(position=pos_b, size=size_b)

    # A: [0,5], B: [10,20] → no overlap
    assert collider_a.intersects(collider_b) is False

    # Grow A so its right edge reaches 10 → edge-touching = intersect
    size_a.width = 10
    assert collider_a.intersects(collider_b) is True

"""Tests for pygame_tile_kit.enums."""

import pytest

from pygame_tile_kit.enums import EdgeType, TileCategory, TileSize, are_edges_compatible


@pytest.mark.parametrize(
    "edge1, edge2, expected",
    [
        (EdgeType.OPEN, EdgeType.OPEN, True),
        (EdgeType.OPEN, EdgeType.SOLID, True),
        (EdgeType.OPEN, EdgeType.PLATFORM, True),
        (EdgeType.OPEN, EdgeType.CLIMBABLE, True),
        (EdgeType.SOLID, EdgeType.OPEN, True),
        (EdgeType.SOLID, EdgeType.SOLID, True),
        (EdgeType.SOLID, EdgeType.PLATFORM, False),
        (EdgeType.SOLID, EdgeType.CLIMBABLE, False),
        (EdgeType.PLATFORM, EdgeType.OPEN, True),
        (EdgeType.PLATFORM, EdgeType.SOLID, False),
        (EdgeType.PLATFORM, EdgeType.PLATFORM, True),
        (EdgeType.PLATFORM, EdgeType.CLIMBABLE, False),
        (EdgeType.CLIMBABLE, EdgeType.OPEN, True),
        (EdgeType.CLIMBABLE, EdgeType.SOLID, False),
        (EdgeType.CLIMBABLE, EdgeType.PLATFORM, False),
        (EdgeType.CLIMBABLE, EdgeType.CLIMBABLE, True),
    ],
)
def test_are_edges_compatible_covers_every_ordered_pair(edge1, edge2, expected):
    assert are_edges_compatible(edge1, edge2) is expected


def test_tile_size_has_exactly_three_members():
    assert len(TileSize) == 3


def test_tile_category_has_exactly_six_members():
    assert len(TileCategory) == 6

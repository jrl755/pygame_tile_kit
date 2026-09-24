"""Tests for pygame_tile_kit.registry.

Every test uses a plain `str` (or a small unrelated dataclass) as the
payload type T, deliberately - this package must not depend on any
particular consumer's tile-content shape, and using a trivial payload
throughout proves the registry is genuinely generic.
"""

from dataclasses import dataclass

from pygame_tile_kit.enums import EdgeType, TileCategory, TileSize
from pygame_tile_kit.registry import TileEdges, TileMetadata, TileRegistry


@dataclass
class _Payload:
    note: str


def test_register_and_get_round_trips_a_tile():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(TileMetadata(tile_id="a", payload="payload-a"))

    result = registry.get("a")

    assert result is not None
    assert result.payload == "payload-a"


def test_all_returns_every_registered_tile():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(TileMetadata(tile_id="a", payload="a"))
    registry.register(TileMetadata(tile_id="b", payload="b"))

    assert {m.tile_id for m in registry.all()} == {"a", "b"}


def test_by_category_and_by_size_and_by_tag_filter_correctly():
    registry: TileRegistry[_Payload] = TileRegistry()
    registry.register(
        TileMetadata(
            tile_id="ground_small",
            payload=_Payload("g"),
            category=TileCategory.GROUND,
            size=TileSize.SMALL,
            tags=("flat",),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="hazard_medium",
            payload=_Payload("h"),
            category=TileCategory.HAZARD,
            size=TileSize.MEDIUM,
            tags=("spikes",),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="ground_large",
            payload=_Payload("g2"),
            category=TileCategory.GROUND,
            size=TileSize.LARGE,
            tags=("flat", "boss"),
        )
    )

    assert {m.tile_id for m in registry.by_category(TileCategory.GROUND)} == {
        "ground_small",
        "ground_large",
    }
    assert {m.tile_id for m in registry.by_size(TileSize.MEDIUM)} == {"hazard_medium"}
    assert {m.tile_id for m in registry.by_tag("flat")} == {
        "ground_small",
        "ground_large",
    }


def test_compatible_filters_by_left_and_right_edge_independently():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(
        TileMetadata(
            tile_id="solid_both",
            payload="s",
            edges=TileEdges(left=EdgeType.SOLID, right=EdgeType.SOLID),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="climbable_both",
            payload="c",
            edges=TileEdges(left=EdgeType.CLIMBABLE, right=EdgeType.CLIMBABLE),
        )
    )

    assert {m.tile_id for m in registry.compatible(left=EdgeType.SOLID)} == {
        "solid_both"
    }
    assert {m.tile_id for m in registry.compatible(right=EdgeType.CLIMBABLE)} == {
        "climbable_both"
    }


def test_compatible_filters_by_top_and_bottom_edge_independently():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(
        TileMetadata(
            tile_id="solid_both",
            payload="s",
            edges=TileEdges(top=EdgeType.SOLID, bottom=EdgeType.SOLID),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="climbable_both",
            payload="c",
            edges=TileEdges(top=EdgeType.CLIMBABLE, bottom=EdgeType.CLIMBABLE),
        )
    )

    assert {m.tile_id for m in registry.compatible(top=EdgeType.SOLID)} == {
        "solid_both"
    }
    assert {m.tile_id for m in registry.compatible(bottom=EdgeType.CLIMBABLE)} == {
        "climbable_both"
    }


def test_compatible_combines_edge_and_category_and_tag_constraints():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(
        TileMetadata(
            tile_id="match",
            payload="m",
            category=TileCategory.GROUND,
            tags=("flat",),
            edges=TileEdges(left=EdgeType.SOLID),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="wrong_category",
            payload="w",
            category=TileCategory.HAZARD,
            tags=("flat",),
            edges=TileEdges(left=EdgeType.SOLID),
        )
    )
    registry.register(
        TileMetadata(
            tile_id="wrong_tag",
            payload="w2",
            category=TileCategory.GROUND,
            tags=("spikes",),
            edges=TileEdges(left=EdgeType.SOLID),
        )
    )

    result = registry.compatible(
        left=EdgeType.SOLID, category=TileCategory.GROUND, tags=("flat",)
    )

    assert {m.tile_id for m in result} == {"match"}


def test_exclude_tags_removes_matches():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(TileMetadata(tile_id="a", payload="a", tags=("flat",)))
    registry.register(TileMetadata(tile_id="b", payload="b", tags=("flat", "risky")))

    result = registry.compatible(exclude_tags=("risky",))

    assert {m.tile_id for m in result} == {"a"}


def test_stats_counts_total_and_per_category():
    registry: TileRegistry[str] = TileRegistry()
    registry.register(
        TileMetadata(tile_id="a", payload="a", category=TileCategory.GROUND)
    )
    registry.register(
        TileMetadata(tile_id="b", payload="b", category=TileCategory.GROUND)
    )
    registry.register(TileMetadata(tile_id="c", payload="c"))

    assert registry.stats() == {"total": 3, "ground": 2}


def test_get_returns_none_for_an_unregistered_id():
    registry: TileRegistry[str] = TileRegistry()

    assert registry.get("missing") is None

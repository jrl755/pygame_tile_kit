"""Generic per-tile metadata record + query engine.

Generalizes Skodrak's TileRegistry (skodrak/levels/tiles/tile_registry.py)
to work over any opaque payload type T - the registry knows nothing
about what a tile *contains* (platforms, ladders, ceiling polylines,
whatever a project's own tile-content type looks like); it only knows a
tile's id, size/category/tags/edges, and how to filter by them.
"""

from dataclasses import dataclass, field

from pygame_tile_kit.enums import EdgeType, TileCategory, TileSize, are_edges_compatible


@dataclass(frozen=True)
class TileEdges:
    """A tile's four edge types, for edge-compatibility queries.

    top/bottom were added for grid-based, multi-cell-span consumers,
    where vertical adjacency (what can stack above/below a tile) is as
    meaningful as horizontal adjacency. Left/right-only consumers are
    unaffected - both fields default to OPEN, which is compatible with
    everything (see are_edges_compatible).
    """

    left: EdgeType = EdgeType.OPEN
    right: EdgeType = EdgeType.OPEN
    top: EdgeType = EdgeType.OPEN
    bottom: EdgeType = EdgeType.OPEN


@dataclass
class TileMetadata[T]:
    """One registered tile: its id, optional catalog metadata, and its
    project-defined payload (opaque to this package).
    """

    tile_id: str
    payload: T
    size: TileSize | None = None
    category: TileCategory | None = None
    tags: tuple[str, ...] = ()
    edges: TileEdges = field(default_factory=TileEdges)


class TileRegistry[T]:
    """In-memory catalog of TileMetadata[T], queryable by category,
    size, tag, and edge compatibility.
    """

    def __init__(self) -> None:
        self._tiles: dict[str, TileMetadata[T]] = {}

    def register(self, metadata: TileMetadata[T]) -> None:
        """Add or replace a tile's metadata record, keyed by its tile_id."""
        self._tiles[metadata.tile_id] = metadata

    def get(self, tile_id: str) -> TileMetadata[T] | None:
        """Look up a single tile's metadata by id."""
        return self._tiles.get(tile_id)

    def all(self) -> list[TileMetadata[T]]:
        """All registered tiles, in registration order."""
        return list(self._tiles.values())

    def by_category(self, category: TileCategory) -> list[TileMetadata[T]]:
        return [t for t in self._tiles.values() if t.category == category]

    def by_size(self, size: TileSize) -> list[TileMetadata[T]]:
        return [t for t in self._tiles.values() if t.size == size]

    def by_tag(self, tag: str) -> list[TileMetadata[T]]:
        return [t for t in self._tiles.values() if tag in t.tags]

    def compatible(
        self,
        *,
        left: EdgeType | None = None,
        right: EdgeType | None = None,
        top: EdgeType | None = None,
        bottom: EdgeType | None = None,
        category: TileCategory | None = None,
        size: TileSize | None = None,
        tags: tuple[str, ...] = (),
        exclude_tags: tuple[str, ...] = (),
    ) -> list[TileMetadata[T]]:
        """Find tiles matching all given constraints."""
        result = []
        for t in self._tiles.values():
            if not self._edges_match(t.edges, left, right, top, bottom):
                continue
            if category is not None and t.category != category:
                continue
            if size is not None and t.size != size:
                continue
            if tags and not all(tag in t.tags for tag in tags):
                continue
            if exclude_tags and any(tag in t.tags for tag in exclude_tags):
                continue
            result.append(t)
        return result

    @staticmethod
    def _edges_match(
        edges: TileEdges,
        left: EdgeType | None,
        right: EdgeType | None,
        top: EdgeType | None,
        bottom: EdgeType | None,
    ) -> bool:
        """Whether a tile's edges satisfy every given side constraint -
        extracted from compatible() so adding top/bottom didn't just
        duplicate the left/right branch shape twice over.
        """
        if left is not None and not are_edges_compatible(left, edges.left):
            return False
        if right is not None and not are_edges_compatible(edges.right, right):
            return False
        if top is not None and not are_edges_compatible(top, edges.top):
            return False
        if bottom is not None and not are_edges_compatible(edges.bottom, bottom):
            return False
        return True

    def stats(self) -> dict[str, int]:
        """Summary counts: total tiles + counts per category present."""
        counts: dict[str, int] = {"total": len(self._tiles)}
        for t in self._tiles.values():
            if t.category is not None:
                counts[t.category.value] = counts.get(t.category.value, 0) + 1
        return counts

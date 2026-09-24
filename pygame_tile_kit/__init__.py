"""pygame_tile_kit - generic tile metadata + registry/query engine for
tile-based 2D games.
"""

from .enums import EdgeType, TileCategory, TileSize, are_edges_compatible
from .registry import TileEdges, TileMetadata, TileRegistry

__version__ = "0.2.0"

__all__ = [
    "TileSize",
    "TileCategory",
    "EdgeType",
    "are_edges_compatible",
    "TileEdges",
    "TileMetadata",
    "TileRegistry",
]

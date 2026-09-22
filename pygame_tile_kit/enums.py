"""Generic tile-metadata vocabulary: size/category labels and an
edge-compatibility system for describing how tiles may be authored to
connect, independent of what a tile's own payload contains.
"""

from enum import Enum


class TileSize(Enum):
    """Coarse, dimension-free size label for browsing/filtering a tile
    catalog. Deliberately carries no fixed pixel mapping - unlike
    Skodrak's TileSize (skodrak/levels/tiles/tile_data.py:24), whose
    enum members ARE literal (width, height) pixel pairs tied to
    Skodrak's own fixed 1920x1080, 3-row screen-locked layout. That
    shape doesn't generalize: a project with free-scrolling, arbitrary-
    width tiles (e.g. SP_Adventure's 1000/2000/900/260/800/500px tile
    widths) has no natural (width, height) pair to put in a shared
    enum. Each consuming project maps SMALL/MEDIUM/LARGE to whatever
    its own tiles' typical dimensions are, purely as an authoring/
    curation label.
    """

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class TileCategory(Enum):
    """Coarse content category for filtering a tile catalog.

    Trimmed from Skodrak's TileCategory (tile_data.py:220): drops
    CEILING (Skodrak-specific ceiling-overlay concept) and folds
    TRANSITION into SPECIAL (no second consumer needs the distinction
    yet); renames VINE -> CLIMBABLE (SP_Adventure's climbable concept
    is "ladder", not "vine" - the enum name stays payload-agnostic).
    Adds ENEMY: SP_Adventure has tiles (enemy_aquatic.json,
    enemy_ground_melee.json, enemy_heavy_melee.json) whose entire
    content is enemy spawns; Skodrak has no equivalent since it places
    entities via a separate spawn-zone mechanism, not enemy-only tiles.
    """

    GROUND = "ground"
    FLOATING = "floating"
    HAZARD = "hazard"
    CLIMBABLE = "climbable"
    ENEMY = "enemy"
    SPECIAL = "special"


class EdgeType(Enum):
    """Edge types for describing whether two tiles may be authored to
    sit side by side.

    Trimmed from Skodrak's EdgeType (tile_data.py:168): collapses
    PLATFORM_GROUND/PLATFORM_MID/PLATFORM_HIGH's 3-way height-tier
    split (tied to Skodrak's HeightLevel: fixed world-Y platform
    heights of 900/720/540) down to a single PLATFORM value. A project
    wanting a finer-grained distinction expresses it via `tags` instead
    (e.g. tag a tile "edge_height_a") rather than needing it baked into
    this shared enum.
    """

    OPEN = "open"
    SOLID = "solid"
    PLATFORM = "platform"
    CLIMBABLE = "climbable"


def are_edges_compatible(edge1: EdgeType, edge2: EdgeType) -> bool:
    """Whether two tile edges may be authored to sit side by side.

    Ported from Skodrak's are_edges_compatible (tile_data.py:182),
    minus its water_height_1/water_height_2 parameters - those encode
    Skodrak's own water-pool-edge concept, tied to its own payload
    shape. Per this package's design (metadata operates purely on
    EdgeType, independent of payload shape), a consuming project that
    needs a water-height-style compatibility axis composes it on top of
    this predicate itself, rather than this package special-casing one
    payload's concept.

    Rules (unchanged from Skodrak): OPEN is compatible with anything;
    otherwise two edges are compatible only if they're the same type.
    """
    if edge1 == EdgeType.OPEN or edge2 == EdgeType.OPEN:
        return True
    return edge1 == edge2

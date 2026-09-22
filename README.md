# pygame_tile_kit

Generic tile metadata + registry/query engine for tile-based 2D games.
Extracted from [SP_Adventure](https://github.com/jrl755/SP_Adventure),
generalizing the tile-catalog vocabulary
[Skodrak](https://github.com/jrl755/Skodrak) built for its own
endless-mode segment generator into a shape any project can reuse for
authoring hand-placed tile catalogs.

This package owns only the *metadata* layer: a small labeled vocabulary
(`TileSize`, `TileCategory`, `EdgeType`), an edge-compatibility
predicate, and a generic `TileRegistry[T]` that indexes tiles by
category/size/tag/edge — independent of what a tile actually *contains*.
Each consuming project supplies its own payload type `T` (its own
geometry, sprite data, or whatever a "tile" means in that game) and its
own JSON schema/loading code; this package never touches either.

## Status

**v0.1.0** — initial extraction: `TileSize`/`TileCategory`/`EdgeType`
enums, `are_edges_compatible`, and `TileRegistry[T]` with
`register`/`get`/`all`/`by_category`/`by_size`/`by_tag`/`compatible`/`stats`.

## Install

```bash
pip install git+https://github.com/jrl755/pygame_tile_kit.git@v0.1.0
```

## Quick start

```python
from pygame_tile_kit import EdgeType, TileCategory, TileEdges, TileMetadata, TileRegistry

registry: TileRegistry[str] = TileRegistry()
registry.register(
    TileMetadata(
        tile_id="flat_ground_1000",
        payload="whatever your game's tile content is",
        category=TileCategory.GROUND,
        tags=("starter",),
        edges=TileEdges(left=EdgeType.SOLID, right=EdgeType.SOLID),
    )
)

ground_tiles = registry.by_category(TileCategory.GROUND)
```

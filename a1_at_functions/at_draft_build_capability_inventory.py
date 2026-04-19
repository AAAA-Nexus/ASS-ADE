# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:301
# Component id: at.source.ass_ade.build_capability_inventory
from __future__ import annotations

__version__ = "0.1.0"

def build_capability_inventory(
    *,
    working_dir: str | Path = ".",
    hosted_tools: list[str] | None = None,
) -> dict[CapabilityType, set[str]]:
    """Build the current capability inventory from local tools, assets, and hosted MCP."""
    root = Path(working_dir).resolve()
    inventory = {key: set(value) for key, value in _BASE_INVENTORY.items()}
    inventory["tools"].update(default_registry(str(root)).list_tools())
    inventory["tools"].update(_slug(tool) for tool in (hosted_tools or []) if tool)

    for cap_type, names in _load_repo_inventory(root).items():
        inventory[cap_type].update(names)

    for cap_type, names in _load_asset_memory(root).items():
        inventory[cap_type].update(names)

    return inventory

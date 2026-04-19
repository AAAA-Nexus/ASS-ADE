# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_capability_inventory.py:7
# Component id: at.source.a1_at_functions.build_capability_inventory
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

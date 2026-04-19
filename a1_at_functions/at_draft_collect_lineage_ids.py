# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_lineage_ids.py:7
# Component id: at.source.a1_at_functions.collect_lineage_ids
from __future__ import annotations

__version__ = "0.1.0"

def collect_lineage_ids(root: Path) -> list[str]:
    birth_dir = root.resolve() / ".ass-ade" / "birth"
    if not birth_dir.exists():
        return []
    lineage_ids: list[str] = []
    for path in sorted(birth_dir.glob("*.response.json")):
        data = _read_json(path)
        for key in ("lineage_id", "lineageId", "id"):
            value = data.get(key)
            if isinstance(value, str) and value.startswith("dlv-"):
                lineage_ids.append(value)
        nested = data.get("lineage")
        if isinstance(nested, dict):
            value = nested.get("id")
            if isinstance(value, str) and value.startswith("dlv-"):
                lineage_ids.append(value)
    return sorted(set(lineage_ids))

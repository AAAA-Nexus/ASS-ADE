# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_collect_hooks.py:7
# Component id: mo.source.a2_mo_composites.collect_hooks
from __future__ import annotations

__version__ = "0.1.0"

def collect_hooks(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    root = _repo_root_from_working_dir(working_dir)
    hooks_dir = root / "hooks"
    if not hooks_dir.is_dir():
        return []
    return [
        CapabilityEntry(kind="hook", name=path.name, description="")
        for path in sorted(hooks_dir.glob("*.py"))
        if not path.name.startswith("_")
    ]

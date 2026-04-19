# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:171
# Component id: mo.source.ass_ade.collect_hooks
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

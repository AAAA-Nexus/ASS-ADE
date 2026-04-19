# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_local_tools.py:7
# Component id: at.source.a1_at_functions.collect_local_tools
from __future__ import annotations

__version__ = "0.1.0"

def collect_local_tools(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    """Return local agent tool schemas from the registered tool system."""
    try:
        from ass_ade.tools.registry import default_registry

        registry = default_registry(str(working_dir))
        return [
            CapabilityEntry(kind="tool", name=schema.name, description=_first_sentence(schema.description))
            for schema in registry.schemas()
        ]
    except Exception:
        return []

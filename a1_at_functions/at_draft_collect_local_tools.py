# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:97
# Component id: at.source.ass_ade.collect_local_tools
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

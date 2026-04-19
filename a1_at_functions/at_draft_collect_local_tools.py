# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_collect_local_tools.py:5
# Component id: at.source.ass_ade.collect_local_tools
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

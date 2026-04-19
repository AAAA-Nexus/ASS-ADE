# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tier_prefix_from_id.py:5
# Component id: at.source.ass_ade.tier_prefix_from_id
__version__ = "0.1.0"

def tier_prefix_from_id(dep_id: str) -> str | None:
    """Return the two-letter tier prefix from a component id like ``at.parse.foo``."""
    if "." not in dep_id:
        return None
    prefix = dep_id.split(".", 1)[0]
    return prefix if prefix in _PREFIX_TO_TIER else None

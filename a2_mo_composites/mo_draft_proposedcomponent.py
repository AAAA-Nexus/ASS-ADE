# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/rebuild/gap_filler.py:37
# Component id: mo.source.ass_ade.proposedcomponent
__version__ = "0.1.0"

class ProposedComponent:
    id: str
    tier: str
    kind: str
    name: str
    source_symbol: dict[str, Any]
    product_categories: list[str]
    fulfills_blueprints: list[str] = field(default_factory=list)
    made_of: list[str] = field(default_factory=list)
    description: str = ""
    dedup_key: str = ""

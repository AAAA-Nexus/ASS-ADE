# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/rebuild/body_extractor.py:163
# Component id: mo.source.ass_ade.derive_made_of_graph
__version__ = "0.1.0"

def derive_made_of_graph(plan: dict[str, Any]) -> dict[str, Any]:
    """Populate each component's ``made_of`` from call-graph analysis. Mutates ``plan``."""
    by_name: dict[str, str] = {}
    for prop in plan.get("proposed_components") or []:
        name = (prop.get("name") or "").lower()
        if name:
            by_name[name] = prop["id"]

    for prop in plan.get("proposed_components") or []:
        made_of: list[str] = list(prop.get("made_of") or [])
        for callee in prop.get("callers_of") or []:
            target_id = by_name.get((callee or "").lower())
            if target_id and target_id != prop["id"] and target_id not in made_of:
                made_of.append(target_id)
        prop["made_of"] = made_of
    return plan

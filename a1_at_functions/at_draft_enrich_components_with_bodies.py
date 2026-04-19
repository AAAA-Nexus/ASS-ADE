# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_enrich_components_with_bodies.py:5
# Component id: at.source.ass_ade.enrich_components_with_bodies
__version__ = "0.1.0"

def enrich_components_with_bodies(
    plan: dict[str, Any],
    *,
    max_body_chars: int = 40_000,
) -> dict[str, Any]:
    """Attach extracted source bodies to every proposed component. Mutates ``plan``."""
    for prop in plan.get("proposed_components") or []:
        sym = prop.get("source_symbol") or {}
        src_path = sym.get("path") or ""
        name = sym.get("name") or prop.get("name")
        lang = sym.get("language") or "python"
        if not src_path or not name:
            continue
        extracted = extract_body(src_path, name, lang)
        if extracted is None:
            continue
        prop["body"] = extracted.body[:max_body_chars]
        prop["imports"] = extracted.imports
        prop["callers_of"] = extracted.callers_of
        prop["exceptions_raised"] = extracted.exceptions_raised
        prop["body_truncated"] = len(extracted.body) > max_body_chars
    return plan

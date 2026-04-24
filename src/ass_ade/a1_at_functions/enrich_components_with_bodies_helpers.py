"""Tier a1 — assimilated function 'enrich_components_with_bodies'

Assimilated from: rebuild/body_extractor.py:147-172
"""

from __future__ import annotations


# --- assimilated symbol ---
def enrich_components_with_bodies(
    plan: dict[str, Any],
    *,
    max_body_chars: int | None = None,
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
        if max_body_chars is None:
            prop["body"] = extracted.body
            prop["body_truncated"] = False
        else:
            prop["body"] = extracted.body[:max_body_chars]
            prop["body_truncated"] = len(extracted.body) > max_body_chars
        prop["imports"] = extracted.imports
        prop["callers_of"] = extracted.callers_of
        prop["exceptions_raised"] = extracted.exceptions_raised
    return plan


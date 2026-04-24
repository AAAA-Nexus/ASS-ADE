"""Tier a1 — assimilated function 'assert_proposals_under_source_root'

Assimilated from: rebuild/schema_materializer.py:555-577
"""

from __future__ import annotations


# --- assimilated symbol ---
def assert_proposals_under_source_root(
    plan: dict[str, Any],
    allowed_root: Path,
) -> None:
    """Fail closed if any proposal's ``source_symbol.path`` escapes ``allowed_root``."""
    root = allowed_root.resolve()
    bad: list[str] = []
    for proposal in plan.get("proposed_components") or []:
        src_sym = proposal.get("source_symbol") or {}
        raw = (src_sym.get("path") or "").strip()
        if not raw:
            continue
        p = _resolve_source_symbol_path(raw, root)
        if not _is_under_source_root(p, root):
            bad.append(str(p))
    if bad:
        sample = bad[:20]
        more = f" (+{len(bad) - 20} more)" if len(bad) > 20 else ""
        raise RebuildProvenanceError(
            f"{len(bad)} source_symbol.path value(s) are outside the allowed root "
            f"{root} — mixed-tree proposals must not be materialized when a single "
            f"source root is enforced. First paths: {sample!r}{more}"
        )


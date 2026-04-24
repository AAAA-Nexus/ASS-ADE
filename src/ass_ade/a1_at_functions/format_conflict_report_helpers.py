"""Tier a1 — assimilated function 'format_conflict_report'

Assimilated from: rebuild/conflict_detector.py:107-121
"""

from __future__ import annotations


# --- assimilated symbol ---
def format_conflict_report(result: dict[str, Any]) -> str:
    """Return a human-readable conflict summary for CLI display."""
    conflicts = result.get("conflicts", [])
    if not conflicts:
        return "[ok] No module name conflicts detected."

    lines = [f"[warn] {len(conflicts)} namespace conflict(s) detected — rebuild used last_wins:"]
    for c in conflicts:
        lines.append(f"  • {c['stem']}.py  ({len(c['sources'])} versions, hashes: {', '.join(c['hashes'])})")
        for src in c["sources"]:
            lines.append(f"      {src}")
        lines.append(f"    -> Resolution: {c['resolution']}  (last source path wins at materialize)")
    lines.append("")
    lines.append("  Tip: add a REBUILD_MANIFEST.json to promote shared utilities to tools/.")
    return "\n".join(lines)


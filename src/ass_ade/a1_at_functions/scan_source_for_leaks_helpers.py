"""Tier a1 — assimilated function 'scan_source_for_leaks'

Assimilated from: registry.py:184-200
"""

from __future__ import annotations


# --- assimilated symbol ---
def scan_source_for_leaks(
    source: str, *, pattern_dir: Path | None = None
) -> list[LeakHit]:
    """Scan ``source`` for sovereign-leak patterns. Pure function.

    Returns an empty list when clean. Each hit's raw matched substring
    is redacted (first two chars + block glyphs) so the hit itself
    cannot re-leak — same discipline as the genesis-log escalation.
    """
    regex = _compile_leak_regex(pattern_dir or _leak_pattern_dir())
    if regex is None:
        return []
    hits: list[LeakHit] = []
    for m in regex.finditer(source):
        matched = m.group(0)
        hits.append(LeakHit(category="leak", redacted=_redact(matched)))
    return hits


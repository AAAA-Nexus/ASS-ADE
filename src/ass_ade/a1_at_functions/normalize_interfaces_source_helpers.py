"""Tier a1 — assimilated function 'normalize_interfaces_source'

Assimilated from: rebuild/schema_materializer.py:400-414
"""

from __future__ import annotations


# --- assimilated symbol ---
def normalize_interfaces_source(src: str | None) -> str | None:
    """Strip a trailing ``:line`` suffix so paths compare to filesystem paths.

    Component JSON stores ``interfaces.source`` as ``path:line``; diff tools
    must normalize before comparing to ``.py`` paths or disk roots.
    """
    if not src or not isinstance(src, str):
        return None
    raw = src.strip()
    if not raw:
        return None
    parts = raw.rsplit(":", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return raw


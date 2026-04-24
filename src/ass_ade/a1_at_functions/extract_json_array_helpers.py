"""Tier a1 — assimilated function 'extract_json_array'

Assimilated from: rebuild/nexus_parse.py:57-92
"""

from __future__ import annotations


# --- assimilated symbol ---
def extract_json_array(text: str) -> str:
    """Extract the first top-level JSON array from arbitrary model output.

    Handles fenced ```json blocks, leading prose/headings, and trailing
    commentary. Deterministic: scans for the first ``[`` and tracks
    bracket depth with string-literal awareness.
    """
    s = text.strip()
    fence = re.search(r"```(?:json)?\s*\n(.*?)```", s, re.DOTALL)
    if fence:
        s = fence.group(1).strip()
    start = s.find("[")
    if start == -1:
        return s
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return s[start : i + 1]
    return s[start:]


"""Tier a1 — assimilated function 'classify_change'

Assimilated from: rebuild/version_tracker.py:102-124
"""

from __future__ import annotations


# --- assimilated symbol ---
def classify_change(old_body: str, new_body: str, language: str = "python") -> str:
    """Classify the nature of change between two body texts.

    Returns: 'none' | 'patch' | 'minor' | 'major'
    """
    if old_body == new_body:
        return "none"
    if language == "python":
        old_api = _public_python_api(old_body)
        new_api = _public_python_api(new_body)
    elif language in {"typescript", "javascript"}:
        old_api = _public_ts_api(old_body)
        new_api = _public_ts_api(new_body)
    else:
        return "patch"

    removed = old_api - new_api
    added = new_api - old_api
    if removed:
        return "major"
    if added:
        return "minor"
    return "patch"


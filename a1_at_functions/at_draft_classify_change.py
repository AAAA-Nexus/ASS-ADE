# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_classify_change.py:7
# Component id: at.source.a1_at_functions.classify_change
from __future__ import annotations

__version__ = "0.1.0"

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

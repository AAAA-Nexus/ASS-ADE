# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_classify_change.py:5
# Component id: at.source.ass_ade.classify_change
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

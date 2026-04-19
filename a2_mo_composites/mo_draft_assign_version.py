# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/version_tracker.py:129
# Component id: mo.source.ass_ade.assign_version
from __future__ import annotations

__version__ = "0.1.0"

def assign_version(
    artifact_id: str,
    new_body: str,
    language: str,
    prev_versions: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    """Return (version_string, change_type) for a component artifact.

    Args:
        artifact_id:   Component id (e.g. ``at.source.myapp.parse_token``).
        new_body:      Source body of the new/updated component (may be empty).
        language:      'python', 'typescript', 'rust', etc.
        prev_versions: Previous build's version map (from ``load_prev_versions``).

    Returns:
        (version, change_type) where change_type is one of:
        'new', 'none', 'patch', 'minor', 'major'.
    """
    prev = prev_versions.get(artifact_id)
    if prev is None:
        return INITIAL_VERSION, "new"

    new_hash = content_hash(new_body)
    if prev.get("body_hash") == new_hash:
        return prev.get("version", INITIAL_VERSION), "none"

    old_body = prev.get("body", "")
    change_type = classify_change(old_body, new_body, language)
    if change_type == "none":
        return prev.get("version", INITIAL_VERSION), "none"

    return bump_version(prev.get("version", INITIAL_VERSION), change_type), change_type

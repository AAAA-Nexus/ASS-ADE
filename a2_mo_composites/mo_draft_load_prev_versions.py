# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/rebuild/version_tracker.py:222
# Component id: mo.source.ass_ade.load_prev_versions
__version__ = "0.1.0"

def load_prev_versions(prev_manifest_path: Path | None) -> dict[str, dict[str, Any]]:
    """Load version data from a previous build's MANIFEST.json.

    Returns a dict keyed by component id with keys:
    ``version``, ``body_hash``, ``body``.
    """
    if prev_manifest_path is None or not prev_manifest_path.exists():
        return {}
    try:
        manifest = json.loads(prev_manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for comp in manifest.get("components") or []:
        cid = comp.get("id")
        if cid:
            result[cid] = {
                "version": comp.get("version", INITIAL_VERSION),
                "body_hash": comp.get("body_hash", ""),
                "body": comp.get("body", ""),
            }
    return result

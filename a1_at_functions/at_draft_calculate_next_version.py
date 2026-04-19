# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_calculate_next_version.py:5
# Component id: at.source.ass_ade.calculate_next_version
__version__ = "0.1.0"

def calculate_next_version(root: Path, bump: str, new_version: str = "") -> tuple[str, str]:
    old_version = read_project_version(root)
    requested = new_version.strip()
    if requested:
        if not _SEMVER_RE.match(requested):
            raise ValueError(f"Version must be semantic version-like: {requested}")
        return old_version, requested
    if bump not in {"patch", "minor", "major"}:
        raise ValueError("Bump must be one of: patch, minor, major")
    return old_version, bump_version(old_version, bump)

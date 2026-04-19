# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_detect_languages.py:5
# Component id: at.source.ass_ade.detect_languages
__version__ = "0.1.0"

def detect_languages(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORED_DIRS]
        for filename in files:
            suffix = Path(filename).suffix.lstrip(".").lower()
            if suffix:
                counts[suffix] = counts.get(suffix, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))

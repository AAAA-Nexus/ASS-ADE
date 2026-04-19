# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_detect_languages.py:7
# Component id: at.source.a1_at_functions.detect_languages
from __future__ import annotations

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

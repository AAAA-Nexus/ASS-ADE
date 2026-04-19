# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_iter_source_files.py:7
# Component id: at.source.a1_at_functions.iter_source_files
from __future__ import annotations

__version__ = "0.1.0"

def iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in SOURCE_SUFFIXES:
                yield path

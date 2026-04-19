# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/project_parser.py:66
# Component id: at.source.ass_ade.iter_source_files
from __future__ import annotations

__version__ = "0.1.0"

def iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in SOURCE_SUFFIXES:
                yield path

"""Tier a1 — assimilated function 'iter_source_files'

Assimilated from: rebuild/project_parser.py:103-109
"""

from __future__ import annotations


# --- assimilated symbol ---
def iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in SOURCE_SUFFIXES:
                yield path


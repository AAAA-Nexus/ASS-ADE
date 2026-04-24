"""Ensure local engine paths are importable without an editable install."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
for _path in (_ROOT, _SRC):
    if _path.is_dir() and str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

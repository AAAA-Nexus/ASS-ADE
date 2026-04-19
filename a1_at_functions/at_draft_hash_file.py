# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_hash_file.py:7
# Component id: at.source.a1_at_functions.hash_file
from __future__ import annotations

__version__ = "0.1.0"

def hash_file(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()

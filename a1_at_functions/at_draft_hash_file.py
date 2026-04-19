# Extracted from C:/!ass-ade/src/ass_ade/local/certifier.py:40
# Component id: at.source.ass_ade.hash_file
from __future__ import annotations

__version__ = "0.1.0"

def hash_file(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()

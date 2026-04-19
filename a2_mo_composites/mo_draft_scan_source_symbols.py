# Extracted from C:/!ass-ade/src/ass_ade/local/docs_engine.py:143
# Component id: mo.source.ass_ade.scan_source_symbols
from __future__ import annotations

__version__ = "0.1.0"

def scan_source_symbols(root: Path, max_files: int = 200) -> list[dict[str, Any]]:
    _def_re = re.compile(r"^(?:async\s+)?def\s+([A-Za-z_]\w*)")
    _class_re = re.compile(r"^class\s+([A-Za-z_]\w*)")
    symbols: list[dict[str, Any]] = []
    files_seen = 0

    _ignored = DEFAULT_IGNORED_DIRS | {".venv"}

    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _ignored]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            if files_seen >= max_files:
                break
            files_seen += 1
            full_path = Path(dirpath) / filename
            try:
                rel = str(full_path.relative_to(root))
                for line in full_path.read_text(encoding="utf-8", errors="replace").splitlines():
                    stripped = line.lstrip()
                    m = _class_re.match(stripped)
                    if m:
                        symbols.append({"file": rel, "kind": "class", "name": m.group(1)})
                        continue
                    m = _def_re.match(stripped)
                    if m:
                        symbols.append({"file": rel, "kind": "function", "name": m.group(1)})
            except Exception:
                pass

    return symbols

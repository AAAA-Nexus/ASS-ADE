# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:1470
# Component id: at.source.ass_ade.quick_project_scan
from __future__ import annotations

__version__ = "0.1.0"

def quick_project_scan(path: Path) -> dict:
    """Scan ``path`` and return a summary dict in under 2 seconds.

    Covers: file count, language, tier structure, security findings (eval/exec/shell=True),
    untested modules, docstring coverage, and CERTIFICATE.json metadata.
    Results are cached on the Atomadic instance as ``_startup_scan``.
    """
    _ignore = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
               "dist", "build", "target", ".ass-ade"}
    tier_names = {"a0_qk_constants", "a1_at_functions", "a2_mo_composites",
                  "a3_og_features", "a4_sy_orchestration"}
    lang_map = {
        ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript/React",
        ".js": "JavaScript", ".jsx": "JavaScript/React", ".rs": "Rust",
        ".go": "Go", ".java": "Java", ".cs": "C#", ".cpp": "C++",
        ".rb": "Ruby", ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    }

    ext_counts: dict[str, int] = {}
    total_files = 0
    tier_dirs_found: set[str] = set()
    py_source_files: list[Path] = []
    test_stems: set[str] = set()

    try:
        for entry in path.rglob("*"):
            if any(part in _ignore for part in entry.parts):
                continue
            if entry.is_dir():
                if entry.name in tier_names:
                    tier_dirs_found.add(entry.name)
                continue
            total_files += 1
            ext = entry.suffix.lower()
            if ext:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            if ext == ".py":
                stem = entry.stem
                if stem.startswith("test_") or stem.endswith("_test"):
                    test_stems.add(stem[5:] if stem.startswith("test_") else stem[:-5])
                else:
                    py_source_files.append(entry)
    except (PermissionError, OSError):
        pass

    # Security scan — cap at 200 files to stay fast
    security_findings = 0
    _sec_patterns = (b"eval(", b"exec(", b"shell=True")
    for pyf in py_source_files[:200]:
        try:
            raw = pyf.read_bytes()
            if any(p in raw for p in _sec_patterns):
                security_findings += 1
        except OSError:
            pass

    # Docstring coverage — check first 512 bytes for triple-quote
    files_with_docstrings = 0
    sample = py_source_files[:200]
    for pyf in sample:
        try:
            head = pyf.read_bytes()[:512]
            if b'"""' in head or b"'''" in head:
                files_with_docstrings += 1
        except OSError:
            pass
    docstring_pct = int(files_with_docstrings / len(sample) * 100) if sample else 0

    # Untested modules
    source_stems = {f.stem for f in py_source_files}
    untested = len(source_stems - test_stems)

    # Top language
    top_ext = max(ext_counts, key=lambda k: ext_counts[k]) if ext_counts else ""
    lang = lang_map.get(top_ext, top_ext.lstrip(".").upper() if top_ext else "mixed")

    has_tier_structure = len(tier_dirs_found) == 5

    # Component count for tier builds = all py files under tier dirs
    component_count = 0
    if has_tier_structure:
        for pyf in py_source_files:
            if any(t in pyf.parts for t in tier_dirs_found):
                component_count += 1

    # Certificate metadata
    cert_info: dict[str, str] = {}
    cert_path = path / "CERTIFICATE.json"
    if cert_path.exists():
        try:
            cert_data = json.loads(cert_path.read_text(encoding="utf-8"))
            raw_date = cert_data.get("date", cert_data.get("timestamp", ""))
            cert_info["date"] = str(raw_date)[:10]
            raw_conf = cert_data.get("conformance", cert_data.get("score", ""))
            if raw_conf:
                cert_info["conformance"] = str(raw_conf)
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "project_name": path.name,
        "total_files": total_files,
        "language": lang,
        "has_tier_structure": has_tier_structure,
        "tier_dirs_found": sorted(tier_dirs_found),
        "component_count": component_count,
        "security_findings": security_findings,
        "untested_modules": untested,
        "docstring_pct": docstring_pct,
        "cert_info": cert_info,
    }

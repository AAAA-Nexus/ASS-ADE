# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compute_codebase_digest.py:7
# Component id: at.source.a1_at_functions.compute_codebase_digest
from __future__ import annotations

__version__ = "0.1.0"

def compute_codebase_digest(root: Path) -> dict[str, Any]:
    root = root.resolve()
    file_hashes: dict[str, str] = {}

    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _IGNORE_DIRS]
        for filename in files:
            if any(filename.endswith(sfx) for sfx in _IGNORE_SUFFIXES):
                continue
            abs_path = Path(dirpath) / filename
            rel_path = abs_path.relative_to(root).as_posix()
            file_hashes[rel_path] = hash_file(abs_path)

    sorted_pairs = sorted(file_hashes.items())

    combined = "".join(f"{rel}{digest}" for rel, digest in sorted_pairs)
    root_digest = hashlib.sha256(combined.encode()).hexdigest()

    truncated = dict(sorted_pairs[:500])

    return {
        "root": str(root),
        "file_count": len(file_hashes),
        "root_digest": root_digest,
        "files": truncated,
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "sha256",
    }

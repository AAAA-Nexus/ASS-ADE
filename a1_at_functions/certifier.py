"""Local codebase certifier for the ass-ade certify command.

Computes a tamper-evident digest of a codebase. The local digest
is forwarded to the Nexus API for signing; a signed certificate
is only valid when countersigned by atomadic.tech.
"""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_CERTIFY_IGNORE: set[str] = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "target",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
}

_IGNORE_DIRS: set[str] = {
    s for s in DEFAULT_CERTIFY_IGNORE if not s.startswith("*")
}
_IGNORE_SUFFIXES: set[str] = {
    s.lstrip("*") for s in DEFAULT_CERTIFY_IGNORE if s.startswith("*")
}


def hash_file(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()


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


def build_local_certificate(root: Path, version: str | None = None) -> dict[str, Any]:
    return {
        "schema": "ASS-ADE-CERT-001",
        "version": version or "unknown",
        "digest": compute_codebase_digest(root),
        "signed_by": None,
        "signature": None,
        "valid": False,
        "issuer": "atomadic.tech",
    }


def render_certificate_text(cert: dict[str, Any]) -> str:
    digest = cert.get("digest", {})
    root_digest = digest.get("root_digest", "")
    sig = cert.get("signature")
    valid = cert.get("valid", False)

    lines = [
        "ASS-ADE Codebase Certificate",
        "=" * 40,
        f"Schema:      {cert.get('schema', '')}",
        f"Version:     {cert.get('version', '')}",
        f"Root:        {digest.get('root', '')}",
        f"File count:  {digest.get('file_count', 0)}",
        f"Root digest: {root_digest[:32]}",
        f"Computed at: {digest.get('computed_at', '')}",
        f"Valid:       {valid}",
        f"Signature:   {'present' if sig else 'none'}",
    ]
    return "\n".join(lines)

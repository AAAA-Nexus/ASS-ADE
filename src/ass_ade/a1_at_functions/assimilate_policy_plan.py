"""Tier a1 — pure helper that resolves a validated policy doc into per-root rules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.policy_types import RootPolicy

_DEFAULT_FORBID_GLOBS: tuple[str, ...] = (
    ".git/**",
    "**/pytest_tmp/**",
    "**/node_modules/**",
)
_DEFAULT_MAX_FILE_BYTES: int = 2_000_000
_DEFAULT_BINARY_HANDLING: str = "forbid"


def _row_to_policy(row: dict[str, Any], doc: dict[str, Any]) -> RootPolicy:
    """Apply schema-aligned defaults to a single roots[] row."""
    doc_forbid = doc.get("forbid_globs")
    row_forbid = row.get("forbid_globs")
    if isinstance(row_forbid, list):
        forbid_list = row_forbid
    elif isinstance(doc_forbid, list):
        forbid_list = doc_forbid
    else:
        forbid_list = list(_DEFAULT_FORBID_GLOBS)

    doc_allow = doc.get("allow_globs")
    row_allow = row.get("allow_globs")
    if isinstance(row_allow, list):
        allow_val: tuple[str, ...] | None = tuple(str(x) for x in row_allow)
    elif isinstance(doc_allow, list):
        allow_val = tuple(str(x) for x in doc_allow)
    else:
        allow_val = None

    max_bytes_val = row.get("max_file_bytes")
    if not isinstance(max_bytes_val, int):
        max_bytes_val = doc.get("max_file_bytes")
    if not isinstance(max_bytes_val, int) or max_bytes_val <= 0:
        max_bytes_val = _DEFAULT_MAX_FILE_BYTES

    binary = row.get("binary_handling") or doc.get("binary_handling") or _DEFAULT_BINARY_HANDLING

    policy: RootPolicy = {
        "role": str(row.get("role", "input")),
        "license_class": str(row.get("license_class", "unknown")),
        "forbid_globs": tuple(str(x) for x in forbid_list),
        "allow_globs": allow_val,
        "max_file_bytes": int(max_bytes_val),
        "binary_handling": str(binary),
    }
    return policy


def build_policy_plan(
    policy_doc: dict[str, Any] | None,
    roots: list[Path],
) -> dict[Path, RootPolicy]:
    """Map resolved root paths → per-root RootPolicy.

    Returns an empty dict when ``policy_doc`` is falsy. Unlisted roots are absent
    from the map so callers can keep legacy behavior for them.
    """
    if not policy_doc:
        return {}

    resolved_roots = {Path(r).resolve() for r in roots}
    doc_rows = policy_doc.get("roots")
    if not isinstance(doc_rows, list):
        return {}

    plan: dict[Path, RootPolicy] = {}
    for row in doc_rows:
        if not isinstance(row, dict):
            continue
        raw_path = row.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            continue
        p = Path(raw_path)
        candidate = p if p.is_absolute() else Path.cwd() / p
        resolved = candidate.resolve()
        if resolved not in resolved_roots:
            # Only plan for roots actually being processed; ignore stray policy entries.
            continue
        plan[resolved] = _row_to_policy(row, policy_doc)
    return plan

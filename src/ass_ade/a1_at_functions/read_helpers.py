"""Tier a1 — assimilated function 'read'

Assimilated from: bindings_lock.py:137-174
"""

from __future__ import annotations


# --- assimilated symbol ---
def read(path: Path) -> LockFile:
    """Load a ``bindings.lock`` and validate its integrity hash."""
    raw = Path(path).read_bytes()
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise BindingsLockVerifyError(f"lock at {path} is not a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise BindingsLockVerifyError(
            f"lock at {path}: unsupported schema_version={data.get('schema_version')!r}; "
            f"expected {SCHEMA_VERSION}"
        )
    integrity = data.get("integrity") or {}
    claimed = integrity.get("content_sha256")
    if not isinstance(claimed, str) or len(claimed) != 64:
        raise BindingsLockVerifyError(
            f"lock at {path}: integrity.content_sha256 missing or malformed"
        )
    recomputed = _content_hash(data)
    if recomputed != claimed:
        raise BindingsLockVerifyError(
            f"lock at {path}: integrity hash mismatch; expected {claimed[:8]}… "
            f"but recomputed {recomputed[:8]}…"
        )
    manifest_fp = data.get("manifest_fingerprint")
    if not isinstance(manifest_fp, str) or len(manifest_fp) != 64:
        raise BindingsLockVerifyError(
            f"lock at {path}: manifest_fingerprint missing or malformed"
        )
    entries_raw = data.get("entries", [])
    if not isinstance(entries_raw, list):
        raise BindingsLockVerifyError(f"lock at {path}: entries must be a list")
    entries = [_lock_entry_from_dict(e) for e in entries_raw]
    return LockFile(
        manifest_fingerprint=manifest_fp,
        entries=entries,
        tool_version=str(data.get("tool_version", "")),
        generated_at_iso=str(data.get("generated_at_iso", "")),
    )


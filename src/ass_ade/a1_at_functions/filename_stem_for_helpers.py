"""Tier a1 — assimilated function 'filename_stem_for'

Assimilated from: rebuild/schema_materializer.py:371-382
"""

from __future__ import annotations


# --- assimilated symbol ---
def filename_stem_for(canonical_name: str) -> str:
    """Filename stem for a canonical name: dots → underscores.

    `a1.crypto.hash.sha256_hex` → `a1_crypto_hash_sha256_hex`.
    The tier head stays in the stem so the file is self-describing
    regardless of where it lives.
    """
    stem = canonical_name.replace(".", "_")
    stem = re.sub(r"_+", "_", stem).strip("_") or "atom"
    if stem[:1].isdigit():
        stem = f"a_{stem}"
    return stem


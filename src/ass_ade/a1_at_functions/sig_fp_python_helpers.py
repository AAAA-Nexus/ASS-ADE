"""Tier a1 — assimilated function 'sig_fp_python'

Assimilated from: fingerprint.py:307-326
"""

from __future__ import annotations


# --- assimilated symbol ---
def sig_fp_python(source: str) -> str:
    """Signature fingerprint for a Python source string.

    Stable under:
      - whitespace / blank lines
      - comment additions / edits / deletions
      - docstring additions / edits / deletions
      - function-body edits that preserve the signature
      - reordering of top-level def/class definitions

    Changes when any of these change:
      - function or class name
      - decorator identity (adding ``@staticmethod`` on a method, etc.)
      - argument name, presence of default, annotation, return type
      - class base list or keyword args (metaclass, protocols)
    """

    module = _parse_python(source)
    payload = "\n".join(_signature_lines(module))
    return _sha256("py-sig:v1\n" + payload)


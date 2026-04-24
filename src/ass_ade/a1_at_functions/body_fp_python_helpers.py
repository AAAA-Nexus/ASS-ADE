"""Tier a1 — assimilated function 'body_fp_python'

Assimilated from: fingerprint.py:329-353
"""

from __future__ import annotations


# --- assimilated symbol ---
def body_fp_python(source: str) -> str:
    """Body fingerprint for a Python source string.

    Stable under:
      - whitespace / blank lines
      - comments (``ast`` drops them during parse)

    Changes when any of these change:
      - any AST-visible statement
      - any identifier rename (variable, function, class)
      - any literal value used in code
      - **any docstring edit** — per agent-10 Fingerprinter, docstrings
        are semantic for the engine and changing one is a changed body.

    Implementation: ``ast.dump`` with ``annotate_fields=False`` and
    ``include_attributes=False`` so source line numbers and column
    offsets (which move on every whitespace edit) are excluded from
    the hash input.
    """

    module = _parse_python(source)
    dumped = ast.dump(
        module, annotate_fields=False, include_attributes=False
    )
    return _sha256("py-body:v1\n" + dumped)


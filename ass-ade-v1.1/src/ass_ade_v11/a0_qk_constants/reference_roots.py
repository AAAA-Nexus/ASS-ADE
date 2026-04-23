"""MAP=TERRAIN: documented paths and basenames for ass-ade-v1* reference artifacts.

Operators compare v1.1 rebuild output against the self-rebuilt **ass-ade-v1** tree
(see ``C:\\!atomadic\\ass-ade-v1`` and lineage label ``ass-ade-v1*``). Runtime code
must not assume these paths exist; use ``a1_at_functions.v1_reference_index`` to probe.
"""

from __future__ import annotations

# Environment override for non-default layouts (CI, Linux, etc.).
ASS_ADE_V1_REFERENCE_ROOT_ENV = "ASS_ADE_V1_REFERENCE_ROOT"

# Documented Windows developer layout (Atomadic umbrella). Overridden by env above.
DOCUMENTED_ASS_ADE_V1_REFERENCE_ROOT = r"C:\!atomadic\ass-ade-v1"

# Lineage glob label for docs / receipts (not expanded by the filesystem layer).
ASS_ADE_V1_LINEAGE_GLOB = "ass-ade-v1*"

# Canonical filenames at the reference root (aligned with ass-ade-v1 README / MANIFEST).
REFERENCE_MANIFEST_BASENAME = "MANIFEST.json"
REFERENCE_CERTIFICATE_BASENAME = "CERTIFICATE.json"
REFERENCE_BLUEPRINT_BASENAME = "BLUEPRINT.json"
REFERENCE_PROVENANCE_BASENAME = "PROVENANCE.json"

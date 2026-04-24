"""Tier a1 — assimilated function 'run_phase6_audit'

Assimilated from: phase6_audit.py:11-13
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.audit_rebuild import validate_rebuild_v11


# --- assimilated symbol ---
def run_phase6_audit(target_root: Path) -> dict[str, Any]:
    audit = validate_rebuild_v11(Path(target_root))
    return {"phase": 6, "audit": audit}


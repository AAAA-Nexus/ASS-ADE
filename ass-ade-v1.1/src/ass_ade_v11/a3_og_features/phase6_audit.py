"""Phase 6 — validate materialized tree."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade_v11.a1_at_functions.audit_rebuild import validate_rebuild_v11


def run_phase6_audit(target_root: Path) -> dict[str, Any]:
    audit = validate_rebuild_v11(Path(target_root))
    return {"phase": 6, "audit": audit}

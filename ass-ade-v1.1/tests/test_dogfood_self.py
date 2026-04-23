"""T10 — self-dogfood: v1.1 repo rebuilds through phase 7 (scratch output)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade_v11.a4_sy_orchestration import rebuild_project_v11

_REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.dogfood
def test_self_repo_full_rebuild_conformant_audit(tmp_path: Path) -> None:
    book = rebuild_project_v11(_REPO_ROOT, tmp_path, rebuild_tag="pytest-dogfood")
    assert book["stopped_after"] == 7
    audit = book["phase6"]["audit"]
    assert audit["validated"] is True
    assert audit["summary"]["structure_conformant"] is True
    assert book["phase5"]["materialize"]["written_count"] >= 1

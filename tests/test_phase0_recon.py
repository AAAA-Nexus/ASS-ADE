from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.a3_og_features.phase0_recon import run_phase0_recon


@pytest.mark.phase0_recon
def test_phase0_ready_on_fixture(minimal_pkg_root: Path) -> None:
    r = run_phase0_recon(minimal_pkg_root)
    assert r["verdict"] == "READY_FOR_PHASE_1"
    assert r["codebase"]["python_files"] >= 1


@pytest.mark.phase0_recon
def test_phase0_required_on_empty_tmp(tmp_path: Path) -> None:
    r = run_phase0_recon(tmp_path)
    assert r["verdict"] == "RECON_REQUIRED"
    assert r["required_actions"]

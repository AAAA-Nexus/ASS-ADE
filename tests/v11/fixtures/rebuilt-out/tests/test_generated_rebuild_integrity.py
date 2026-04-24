"""Auto-emitted rebuild integrity tests.

This suite gives rebuilt outputs a baseline verification harness even when the
source repository had no original test suite to carry forward.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PYTHON_TARGETS = [
  "__init__.py",
  "a1_at_functions/__init__.py",
  "a1_at_functions/a1_compile_python_compile.py",
  "a1_at_functions/a1_minimal_pkg_invariant_metadata.py",
  "a1_at_functions/a1_minimal_pkg_pure_helper.py",
  "a1_at_functions/a1_minimal_pkg_run.py",
  "a2_mo_composites/__init__.py",
  "a2_mo_composites/a2_compile_python_compile.py"
]
COMPONENT_TARGETS = [
  "a1_at_functions/a1_compile_python_compile.json",
  "a1_at_functions/a1_minimal_pkg_invariant_metadata.json",
  "a1_at_functions/a1_minimal_pkg_pure_helper.json",
  "a1_at_functions/a1_minimal_pkg_run.json",
  "a2_mo_composites/a2_compile_python_compile.json"
]
TIER_PACKAGES = [
  "a1_at_functions",
  "a2_mo_composites"
]
DOC_ARTIFACTS = [
  "API_INVENTORY.md",
  "DOC_COVERAGE.md",
  "TEST_COVERAGE.md"
]


@pytest.mark.parametrize("relpath", PYTHON_TARGETS, ids=PYTHON_TARGETS)
def test_emitted_python_files_compile(relpath: str) -> None:
    path = ROOT / relpath
    source = path.read_text(encoding="utf-8", errors="replace")
    compile(source, str(path), "exec")


@pytest.mark.parametrize("relpath", COMPONENT_TARGETS, ids=COMPONENT_TARGETS)
def test_emitted_component_json_has_body_hash_and_interfaces_source(relpath: str) -> None:
    path = ROOT / relpath
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert str(payload.get("body_hash", "")).strip()
    interfaces = payload.get("interfaces") or {}
    assert str(interfaces.get("source", "")).strip()


@pytest.mark.parametrize("relpath", DOC_ARTIFACTS, ids=DOC_ARTIFACTS)
def test_documentation_artifacts_exist(relpath: str) -> None:
    assert (ROOT / relpath).exists()


@pytest.mark.parametrize("package_name", TIER_PACKAGES, ids=TIER_PACKAGES)
def test_tier_packages_expose_available_modules(package_name: str) -> None:
    module = __import__(package_name, fromlist=["available_modules"])
    assert hasattr(module, "available_modules")
    available = module.available_modules()
    assert isinstance(available, list)
    assert available


def test_vendored_ass_ade_cli_help_runs_when_present() -> None:
    if not (ROOT / "ass_ade" / "__main__.py").is_file():
        pytest.skip("vendored ass_ade package not present")
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONPATH"] = (
        f"{ROOT}{os.pathsep}{env['PYTHONPATH']}"
        if env.get("PYTHONPATH")
        else str(ROOT)
    )
    result = subprocess.run(
        [sys.executable, "-m", "ass_ade", "--help"],
        capture_output=True,
        check=False,
        cwd=ROOT,
        env=env,
    )
    assert result.returncode == 0
    stdout = result.stdout.decode("utf-8", errors="replace")
    assert "Usage:" in stdout

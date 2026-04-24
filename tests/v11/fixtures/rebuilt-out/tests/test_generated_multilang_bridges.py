"""Auto-emitted smoke tests for multi-language rebuild bridge scaffolding."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = ".ass-ade/bridges/bridge_manifest.json"
REPORT_REL = "MULTILANG_BRIDGES.md"
BRIDGE_FILES = [
  "bridges/README.md",
  "bridges/kotlin/build.gradle.kts",
  "bridges/kotlin/settings.gradle.kts",
  "bridges/kotlin/src/main/kotlin/AssAdeBridge.kt",
  "bridges/kotlin/src/main/kotlin/a0_qk_constants/BridgeContract.kt",
  "bridges/kotlin/src/main/kotlin/a1_at_functions/ManifestLoader.kt",
  "bridges/kotlin/src/main/kotlin/a2_mo_composites/PythonBridgeClient.kt",
  "bridges/kotlin/src/main/kotlin/a3_og_features/BridgeFeature.kt",
  "bridges/kotlin/src/main/kotlin/a4_sy_orchestration/BridgeMain.kt",
  "bridges/rust/Cargo.toml",
  "bridges/rust/src/a0_qk_constants/bridge_contract.rs",
  "bridges/rust/src/a0_qk_constants/mod.rs",
  "bridges/rust/src/a1_at_functions/manifest_loader.rs",
  "bridges/rust/src/a1_at_functions/mod.rs",
  "bridges/rust/src/a2_mo_composites/mod.rs",
  "bridges/rust/src/a2_mo_composites/python_bridge_client.rs",
  "bridges/rust/src/a3_og_features/bridge_feature.rs",
  "bridges/rust/src/a3_og_features/mod.rs",
  "bridges/rust/src/a4_sy_orchestration/bridge_main.rs",
  "bridges/rust/src/a4_sy_orchestration/mod.rs",
  "bridges/rust/src/main.rs",
  "bridges/samples/bridge_request.sample.json",
  "bridges/samples/bridge_response.sample.json",
  "bridges/swift/Package.swift",
  "bridges/swift/Sources/AssAdeBridge/a0_qk_constants/BridgeContract.swift",
  "bridges/swift/Sources/AssAdeBridge/a1_at_functions/ManifestLoader.swift",
  "bridges/swift/Sources/AssAdeBridge/a2_mo_composites/PythonBridgeClient.swift",
  "bridges/swift/Sources/AssAdeBridge/a3_og_features/BridgeFeature.swift",
  "bridges/swift/Sources/AssAdeBridge/a4_sy_orchestration/BridgeMain.swift",
  "bridges/swift/Sources/AssAdeBridge/main.swift",
  "bridges/typescript/package.json",
  "bridges/typescript/smoke.mjs",
  "bridges/typescript/src/a0_qk_constants/bridge_contract.ts",
  "bridges/typescript/src/a1_at_functions/manifest_loader.ts",
  "bridges/typescript/src/a2_mo_composites/python_bridge_client.ts",
  "bridges/typescript/src/a3_og_features/bridge_feature.ts",
  "bridges/typescript/src/a4_sy_orchestration/bridge_main.ts",
  "bridges/typescript/src/index.ts",
  "bridges/typescript/src/node-shims.d.ts",
  "bridges/typescript/tsconfig.json"
]


@pytest.mark.parametrize("relpath", BRIDGE_FILES, ids=BRIDGE_FILES)
def test_multilang_bridge_artifacts_exist(relpath: str) -> None:
    assert (ROOT / relpath).is_file()


def test_multilang_bridge_manifest_is_consistent() -> None:
    payload = json.loads((ROOT / MANIFEST_REL).read_text(encoding="utf-8"))
    assert payload["schema"] == "ASSADE-MULTILANG-BRIDGE-1"
    assert payload["bridge_languages"] == ["typescript", "rust", "kotlin", "swift"]
    assert payload["generated_tests"] == ["tests/test_generated_multilang_bridges.py"]
    assert payload["generated_report"] == REPORT_REL
    if payload.get("vendored_ass_ade"):
        assert payload["python_bridge_command"] == ["python", "-m", "ass_ade"]


def test_multilang_bridge_report_exists() -> None:
    assert (ROOT / REPORT_REL).is_file()


def test_typescript_bridge_compiles_when_tsc_present() -> None:
    tsc = shutil.which("tsc")
    if not tsc:
        pytest.skip("tsc not installed")
    result = subprocess.run(
        [tsc, "--noEmit", "-p", str(ROOT / "bridges/typescript/tsconfig.json")],
        capture_output=True,
        check=False,
        cwd=ROOT,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_typescript_bridge_smoke_when_node_present() -> None:
    node = shutil.which("node")
    if not node:
        pytest.skip("node not installed")
    result = subprocess.run(
        [node, str(ROOT / "bridges/typescript/smoke.mjs")],
        capture_output=True,
        check=False,
        cwd=ROOT,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["schema"] == "ASSADE-MULTILANG-BRIDGE-1"


def test_rust_bridge_compiles_when_cargo_present() -> None:
    cargo = shutil.which("cargo")
    if not cargo:
        pytest.skip("cargo not installed")
    result = subprocess.run(
        [
            cargo,
            "check",
            "--quiet",
            "--manifest-path",
            str(ROOT / "bridges/rust/Cargo.toml"),
        ],
        capture_output=True,
        check=False,
        cwd=ROOT,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_kotlin_bridge_runs_when_gradle_present() -> None:
    gradle = shutil.which("gradle")
    if not gradle:
        pytest.skip("gradle not installed")
    result = subprocess.run(
        [gradle, "--quiet", "run"],
        capture_output=True,
        check=False,
        cwd=ROOT / "bridges/kotlin",
        text=True,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema"] == "ASSADE-MULTILANG-BRIDGE-1"


def test_swift_bridge_builds_when_swift_present() -> None:
    swift = shutil.which("swift")
    if not swift:
        pytest.skip("swift not installed")
    result = subprocess.run(
        [
            swift,
            "build",
            "--package-path",
            str(ROOT / "bridges/swift"),
        ],
        capture_output=True,
        check=False,
        cwd=ROOT,
        text=True,
    )
    assert result.returncode == 0, result.stderr

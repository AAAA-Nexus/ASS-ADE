"""Tier a3 — multi-language bridge emitter: generates TypeScript/Rust/Kotlin/Swift scaffolding."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ass_ade.local.bridge_templates import (
    BRIDGES_README,
    BRIDGE_REQUEST_SAMPLE,
    BRIDGE_RESPONSE_SAMPLE,
    SCHEMA_VERSION,
    TS_BRIDGE_CONTRACT,
    TS_BRIDGE_FEATURE,
    TS_BRIDGE_MAIN,
    TS_INDEX,
    TS_MANIFEST_LOADER,
    TS_NODE_SHIMS,
    TS_PYTHON_BRIDGE_CLIENT,
    TS_SMOKE_MJS,
    TS_TSCONFIG,
    bridge_report_md,
    ts_package_json,
)

_SUPPORTED = ["python", "rust", "typescript", "kotlin", "swift", "atomadic"]
_DEFAULT_BRIDGE_LANGS = ["typescript"]


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def emit_typescript_bridge(target_root: Path, project_name: str) -> list[str]:
    """Write TypeScript bridge files into ``target_root/bridges/typescript/``.

    Returns the list of relative paths written.
    """
    base = target_root / "bridges" / "typescript"
    written: list[str] = []

    files: dict[str, str] = {
        "package.json": ts_package_json(project_name),
        "tsconfig.json": TS_TSCONFIG,
        "smoke.mjs": TS_SMOKE_MJS,
        "src/node-shims.d.ts": TS_NODE_SHIMS,
        "src/a0_qk_constants/bridge_contract.ts": TS_BRIDGE_CONTRACT,
        "src/a1_at_functions/manifest_loader.ts": TS_MANIFEST_LOADER,
        "src/a2_mo_composites/python_bridge_client.ts": TS_PYTHON_BRIDGE_CLIENT,
        "src/a3_og_features/bridge_feature.ts": TS_BRIDGE_FEATURE,
        "src/a4_sy_orchestration/bridge_main.ts": TS_BRIDGE_MAIN,
        "src/index.ts": TS_INDEX,
    }
    for rel, content in files.items():
        _write(base / rel, content)
        written.append(f"bridges/typescript/{rel}")

    return written


def emit_bridge_samples(target_root: Path) -> list[str]:
    _write(target_root / "bridges" / "samples" / "bridge_request.sample.json", BRIDGE_REQUEST_SAMPLE)
    _write(target_root / "bridges" / "samples" / "bridge_response.sample.json", BRIDGE_RESPONSE_SAMPLE)
    return [
        "bridges/samples/bridge_request.sample.json",
        "bridges/samples/bridge_response.sample.json",
    ]


def emit_bridge_readme(target_root: Path) -> str:
    _write(target_root / "bridges" / "README.md", BRIDGES_README)
    return "bridges/README.md"


def emit_bridge_manifest(
    target_root: Path,
    *,
    project_name: str = "",
    python_bridge_command: list[str] | None = None,
    bridge_languages: list[str] | None = None,
    generated_files: list[str] | None = None,
    bridge_ready: bool = False,
) -> Path:
    """Write ``.ass-ade/bridges/bridge_manifest.json`` and return its path."""
    cmd = python_bridge_command or []
    langs = bridge_languages or _DEFAULT_BRIDGE_LANGS
    slug = project_name.lower().replace(" ", "_").replace("-", "_") if project_name else "project"

    manifest = {
        "schema": SCHEMA_VERSION,
        "bridge_mode": "spawn-cli",
        "bridge_ready": bridge_ready,
        "vendored_ass_ade": False,
        "package_name": slug,
        "python_bridge_command": cmd,
        "supported_languages": _SUPPORTED,
        "bridge_languages": langs,
        "generated_report": "MULTILANG_BRIDGES.md",
        "generated_tests": ["tests/test_generated_multilang_bridges.py"],
        "request_sample": "bridges/samples/bridge_request.sample.json",
        "response_sample": "bridges/samples/bridge_response.sample.json",
        "bridge_roots": {lang: f"bridges/{lang}" for lang in langs},
        "generated_files": sorted(generated_files or []),
    }
    out = target_root / ".ass-ade" / "bridges" / "bridge_manifest.json"
    _write(out, json.dumps(manifest, indent=2) + "\n")
    return out


def emit_bridge_report(
    target_root: Path,
    project_name: str,
    python_bridge_command: list[str],
    bridge_ready: bool,
    languages: list[str],
) -> str:
    content = bridge_report_md(project_name, python_bridge_command, bridge_ready, languages)
    _write(target_root / "MULTILANG_BRIDGES.md", content)
    return "MULTILANG_BRIDGES.md"


def emit_smoke_test(target_root: Path) -> str:
    """Generate a smoke test that validates the bridge manifest and TypeScript assets."""
    content = _build_smoke_test()
    _write(target_root / "tests" / "test_generated_multilang_bridges.py", content)
    return "tests/test_generated_multilang_bridges.py"


def _build_smoke_test() -> str:
    return '''\
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
  "bridges/samples/bridge_request.sample.json",
  "bridges/samples/bridge_response.sample.json",
  "bridges/typescript/package.json",
  "bridges/typescript/smoke.mjs",
  "bridges/typescript/src/a0_qk_constants/bridge_contract.ts",
  "bridges/typescript/src/a1_at_functions/manifest_loader.ts",
  "bridges/typescript/src/a2_mo_composites/python_bridge_client.ts",
  "bridges/typescript/src/a3_og_features/bridge_feature.ts",
  "bridges/typescript/src/a4_sy_orchestration/bridge_main.ts",
  "bridges/typescript/src/index.ts",
  "bridges/typescript/src/node-shims.d.ts",
  "bridges/typescript/tsconfig.json",
]


@pytest.mark.parametrize("relpath", BRIDGE_FILES, ids=BRIDGE_FILES)
def test_multilang_bridge_artifacts_exist(relpath: str) -> None:
    assert (ROOT / relpath).is_file()


def test_multilang_bridge_manifest_is_consistent() -> None:
    payload = json.loads((ROOT / MANIFEST_REL).read_text(encoding="utf-8"))
    assert payload["schema"] == "ASSADE-MULTILANG-BRIDGE-1"
    assert "typescript" in payload["bridge_languages"]
    assert payload["generated_tests"] == ["tests/test_generated_multilang_bridges.py"]
    assert payload["generated_report"] == REPORT_REL
    if payload.get("vendored_ass_ade"):
        assert payload["python_bridge_command"] == ["python", "-m", "ass_ade"]


def test_multilang_bridge_report_exists() -> None:
    assert (ROOT / REPORT_REL).is_file()


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
'''


def generate_typescript_bridge(
    target_dir: str | Path,
    *,
    python_bridge_command: list[str] | None = None,
    project_name: str = "",
    bridge_ready: bool | None = None,
) -> dict[str, object]:
    """Top-level entry point: generate the full TypeScript bridge in *target_dir*.

    Args:
        target_dir: Root of the target repo (where ``.ass-ade/`` will be written).
        python_bridge_command: Command to invoke ass-ade, e.g. ``["python", "-m", "ass_ade"]``.
            Defaults to auto-detection via ``sys.executable``.
        project_name: Human-readable project name for generated files.
        bridge_ready: Whether to mark the bridge as ready in the manifest.
            Defaults to True if ``python_bridge_command`` is provided and non-empty.

    Returns a summary dict with ``manifest_path``, ``files_written``, ``bridge_ready``.
    """
    root = Path(target_dir).resolve()
    if not project_name:
        project_name = root.name

    if python_bridge_command is None:
        python_bridge_command = [sys.executable, "-m", "ass_ade"]

    if bridge_ready is None:
        bridge_ready = bool(python_bridge_command)

    ts_files = emit_typescript_bridge(root, project_name)
    sample_files = emit_bridge_samples(root)
    readme = emit_bridge_readme(root)
    all_files = sorted([readme] + ts_files + sample_files)

    manifest_path = emit_bridge_manifest(
        root,
        project_name=project_name,
        python_bridge_command=python_bridge_command,
        bridge_languages=["typescript"],
        generated_files=all_files + ["tests/test_generated_multilang_bridges.py"],
        bridge_ready=bridge_ready,
    )
    emit_bridge_report(root, project_name, python_bridge_command, bridge_ready, ["typescript"])
    emit_smoke_test(root)

    return {
        "target_dir": str(root),
        "project_name": project_name,
        "manifest_path": str(manifest_path),
        "files_written": len(all_files) + 2,  # +manifest, +smoke test
        "bridge_ready": bridge_ready,
        "python_bridge_command": python_bridge_command,
    }

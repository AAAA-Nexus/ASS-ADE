"""Tier a1 — assimilated function 'emit_multilang_bridge_suite'

Assimilated from: rebuild/bridge_emitter.py:862-1035
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ass_ade.capability.types import SUPPORTED_LANGUAGES
from ass_ade.engine.rebuild.bridge_manifest import (


# --- assimilated symbol ---
def emit_multilang_bridge_suite(
    target_root: Path,
    *,
    control_root: Path,
    package_name: str,
    tier_names_present: list[str],
    vendored_ass_ade: bool,
) -> dict[str, Any]:
    """Write bridge-ready scaffolding for TypeScript, Rust, Kotlin, and Swift."""
    target_root = target_root.resolve()
    control_root = control_root.resolve()

    bridge_control_root = bridge_dir(target_root)
    _enforce_boundary(bridge_control_root, control_root)
    bridge_control_root.mkdir(parents=True, exist_ok=True)

    bridges_root = target_root / "bridges"
    _enforce_boundary(bridges_root, control_root)
    bridges_root.mkdir(parents=True, exist_ok=True)

    tests_dir = target_root / "tests"
    _enforce_boundary(tests_dir, control_root)
    tests_dir.mkdir(parents=True, exist_ok=True)

    component_count, by_tier = _load_component_counts(target_root)
    package_slug = _package_slug(package_name)
    manifest_rel = ".ass-ade/bridges/bridge_manifest.json"
    report_rel = MULTILANG_BRIDGE_REPORT_NAME
    bridge_ready = (target_root / "ass_ade" / "__main__.py").is_file()

    bridge_files: list[str] = []

    def _write_text(relpath: str, content: str) -> None:
        path = target_root / relpath
        _enforce_boundary(path, control_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        bridge_files.append(relpath)

    def _write_json(relpath: str, payload: dict[str, Any]) -> None:
        _write_text(relpath, json.dumps(payload, indent=2) + "\n")

    _write_text(
        "bridges/README.md",
        (
            "# Rebuild Bridges\n\n"
            "This folder contains generated cross-language bridge scaffolding.\n"
            "Each language-specific adapter reads the rebuild bridge manifest\n"
            "from `.ass-ade/bridges/bridge_manifest.json` and exposes a stable\n"
            "process-spawn integration point around the shipped Python surface.\n"
        ),
    )
    _write_json(
        _REQUEST_SAMPLE_NAME,
        {
            "command": "recon",
            "args": ["."],
            "cwd": ".",
            "expect_json": False,
        },
    )
    _write_json(
        _RESPONSE_SAMPLE_NAME,
        {
            "ok": True,
            "transport": "spawn-cli",
            "bridge_ready": vendored_ass_ade,
            "notes": "Example envelope returned by an adapter around the rebuilt Python CLI.",
        },
    )
    _write_text("bridges/typescript/package.json", _build_typescript_package_json(package_slug))
    _write_text(
        "bridges/typescript/tsconfig.json",
        (
            "{\n"
            '  "compilerOptions": {\n'
            '    "target": "ES2022",\n'
            '    "module": "NodeNext",\n'
            '    "moduleResolution": "NodeNext",\n'
            '    "strict": true,\n'
            '    "outDir": "dist"\n'
            "  },\n"
            '  "include": ["src/**/*"]\n'
            "}\n"
        ),
    )
    _write_text(
        "bridges/typescript/src/index.ts",
        _build_typescript_index(manifest_rel),
    )
    _write_text(
        "bridges/typescript/src/node-shims.d.ts",
        _build_typescript_node_shims(),
    )
    for relpath, content in _build_typescript_monadic_files(manifest_rel).items():
        _write_text(relpath, content)
    _write_text("bridges/typescript/smoke.mjs", _build_typescript_smoke(manifest_rel))
    _write_text("bridges/rust/Cargo.toml", _build_rust_cargo_toml(package_slug))
    _write_text("bridges/rust/src/main.rs", _build_rust_main(manifest_rel))
    for relpath, content in _build_rust_monadic_files(manifest_rel).items():
        _write_text(relpath, content)
    _write_text("bridges/kotlin/settings.gradle.kts", _build_kotlin_settings())
    _write_text("bridges/kotlin/build.gradle.kts", _build_kotlin_gradle())
    _write_text(
        "bridges/kotlin/src/main/kotlin/AssAdeBridge.kt",
        _build_kotlin_main(manifest_rel),
    )
    for relpath, content in _build_kotlin_monadic_files(manifest_rel).items():
        _write_text(relpath, content)
    _write_text("bridges/swift/Package.swift", _build_swift_package())
    _write_text(
        "bridges/swift/Sources/AssAdeBridge/main.swift",
        _build_swift_main(manifest_rel),
    )
    for relpath, content in _build_swift_monadic_files(manifest_rel).items():
        _write_text(relpath, content)
    _write_text(
        _BRIDGE_TEST_NAME,
        _build_bridge_test(
            manifest_rel=manifest_rel,
            report_rel=report_rel,
            bridge_files=bridge_files,
        ),
    )

    bridge_roots = {
        "typescript": "bridges/typescript",
        "rust": "bridges/rust",
        "kotlin": "bridges/kotlin",
        "swift": "bridges/swift",
    }
    manifest = {
        "schema": MULTILANG_BRIDGE_SCHEMA,
        "bridge_mode": "spawn-cli",
        "bridge_ready": bridge_ready,
        "vendored_ass_ade": vendored_ass_ade,
        "package_name": package_name,
        "python_bridge_command": _bridge_command(bridge_ready),
        "supported_languages": list(SUPPORTED_LANGUAGES),
        "bridge_languages": list(_BRIDGE_LANGUAGES),
        "generated_report": MULTILANG_BRIDGE_REPORT_NAME,
        "generated_tests": [_BRIDGE_TEST_NAME],
        "request_sample": _REQUEST_SAMPLE_NAME,
        "response_sample": _RESPONSE_SAMPLE_NAME,
        "component_count": component_count,
        "by_tier": by_tier,
        "tier_packages": list(tier_names_present),
        "bridge_monadic_layout": [
            "a0_qk_constants",
            "a1_at_functions",
            "a2_mo_composites",
            "a3_og_features",
            "a4_sy_orchestration",
        ],
        "bridge_roots": bridge_roots,
        "generated_files": sorted(bridge_files),
    }

    manifest_path = bridge_manifest_path(target_root)
    _enforce_boundary(manifest_path, control_root)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    report_path = target_root / MULTILANG_BRIDGE_REPORT_NAME
    _enforce_boundary(report_path, control_root)
    report_path.write_text(_build_multilang_bridge_report(manifest), encoding="utf-8")

    return {
        "generated_tests": list(manifest["generated_tests"]),
        "bridge_reports": [MULTILANG_BRIDGE_REPORT_NAME, "bridges/README.md"],
        "bridge_manifests": [_relative(target_root, manifest_path)],
        "bridge_files": sorted(bridge_files),
        "bridge_languages": list(_BRIDGE_LANGUAGES),
        "bridge_ready": bridge_ready,
    }


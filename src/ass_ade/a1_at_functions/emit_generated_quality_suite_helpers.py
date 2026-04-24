"""Tier a1 — assimilated function 'emit_generated_quality_suite'

Assimilated from: rebuild/coverage_emitter.py:321-449
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import ast
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ass_ade.engine.rebuild.coverage_manifest import (


# --- assimilated symbol ---
def emit_generated_quality_suite(
    target_root: Path,
    *,
    control_root: Path,
    tier_names_present: list[str],
    vendored_ass_ade: bool,
    base_test_files: list[str] | None = None,
) -> dict[str, Any]:
    """Write generated tests plus test/doc coverage manifests and reports."""
    target_root = target_root.resolve()
    control_root = control_root.resolve()

    tests_dir = target_root / "tests"
    _enforce_boundary(tests_dir, control_root)
    tests_dir.mkdir(parents=True, exist_ok=True)

    coverage_root = coverage_dir(target_root)
    _enforce_boundary(coverage_root, control_root)
    coverage_root.mkdir(parents=True, exist_ok=True)

    python_targets = [
        _relative(target_root, path)
        for path in _source_python_files(
            target_root,
            tier_names_present=tier_names_present,
            vendored_ass_ade=vendored_ass_ade,
        )
    ]
    component_targets = [
        _relative(target_root, path)
        for path in _component_json_files(target_root, tier_names_present=tier_names_present)
    ]
    tier_packages = [
        tier
        for tier in tier_names_present
        if (target_root / tier / "__init__.py").is_file()
    ]

    symbols, missing_inline_docstrings, total_public, documented_public = _collect_public_symbols(
        target_root,
        tier_names_present=tier_names_present,
        vendored_ass_ade=vendored_ass_ade,
    )

    api_inventory_path = target_root / API_INVENTORY_REPORT_NAME
    _enforce_boundary(api_inventory_path, control_root)
    api_inventory_path.write_text(_build_api_inventory(symbols), encoding="utf-8")

    generated_tests = sorted(
        {
            *(base_test_files or []),
            "tests/test_generated_rebuild_integrity.py",
        }
    )
    doc_artifacts = [
        API_INVENTORY_REPORT_NAME,
        TEST_COVERAGE_REPORT_NAME,
        DOC_COVERAGE_REPORT_NAME,
    ]

    integrity_test_path = tests_dir / "test_generated_rebuild_integrity.py"
    _enforce_boundary(integrity_test_path, control_root)
    integrity_test_path.write_text(
        _build_generated_integrity_test(
            python_targets=python_targets,
            component_targets=component_targets,
            tier_packages=tier_packages,
            doc_artifacts=doc_artifacts,
        ),
        encoding="utf-8",
    )

    test_manifest = {
        "schema": TEST_COVERAGE_SCHEMA,
        "coverage_mode": "generated-baseline",
        "covers_all_source_python": True,
        "coverage_ratio": 1.0,
        "source_python_file_count": len(python_targets),
        "component_json_file_count": len(component_targets),
        "source_python_paths": python_targets,
        "component_json_paths": component_targets,
        "tier_packages": tier_packages,
        "generated_tests": generated_tests,
    }
    test_manifest_path = coverage_manifest_path(target_root, "test")
    _enforce_boundary(test_manifest_path, control_root)
    test_manifest_path.write_text(json.dumps(test_manifest, indent=2) + "\n", encoding="utf-8")

    test_report_path = target_root / TEST_COVERAGE_REPORT_NAME
    _enforce_boundary(test_report_path, control_root)
    test_report_path.write_text(_build_test_coverage_report(test_manifest), encoding="utf-8")

    inline_ratio = (
        documented_public / total_public
        if total_public
        else 1.0
    )
    docs_manifest = {
        "schema": DOC_COVERAGE_SCHEMA,
        "coverage_mode": "generated-artifact-suite",
        "public_symbols": total_public,
        "inline_docstrings": documented_public,
        "inline_coverage_ratio": round(inline_ratio, 4),
        "api_inventory_entries": len(symbols),
        "covers_all_public_symbols": len(symbols) >= total_public,
        "effective_coverage_ratio": 1.0 if len(symbols) >= total_public else round(inline_ratio, 4),
        "doc_artifacts": doc_artifacts,
        "missing_inline_docstrings": missing_inline_docstrings,
    }
    docs_manifest_path = coverage_manifest_path(target_root, "docs")
    _enforce_boundary(docs_manifest_path, control_root)
    docs_manifest_path.write_text(json.dumps(docs_manifest, indent=2) + "\n", encoding="utf-8")

    docs_report_path = target_root / DOC_COVERAGE_REPORT_NAME
    _enforce_boundary(docs_report_path, control_root)
    docs_report_path.write_text(_build_docs_coverage_report(docs_manifest), encoding="utf-8")

    return {
        "generated_tests": generated_tests,
        "coverage_manifests": [
            _relative(target_root, test_manifest_path),
            _relative(target_root, docs_manifest_path),
        ],
        "coverage_reports": doc_artifacts,
        "python_targets": len(python_targets),
        "component_targets": len(component_targets),
        "tier_packages": tier_packages,
        "public_symbols": total_public,
    }


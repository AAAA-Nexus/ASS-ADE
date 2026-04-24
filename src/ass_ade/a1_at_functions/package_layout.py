"""Installable layout derived from the materialized tree (MAP = TERRAIN).

Phase 7 writes **final-intent** artifacts: ``pyproject.toml`` and per-tier ``__init__.py``
surfaces grounded in ``BLUEPRINT.json`` / JSON sidecars, not generic placeholders.
"""

from __future__ import annotations

import json
import keyword
import re
import tomllib
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.tier_names import VALID_TIER_DIRS
from ass_ade.a1_at_functions.test_synth_plan import (
    generated_smoke_test_source,
    plan_manifest_payload_for_package,
)


def _stem_from_id(cid: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._]+", "_", cid.strip())
    return s.replace(".", "_") or "component"


def _load_intended_components(
    project_root: Path,
    package_root: Path,
) -> tuple[list[dict[str, Any]], str | None, str | None]:
    """Return ``(components, rebuild_tag, content_digest)`` from BLUEPRINT or sidecars."""
    bp_path = project_root / "BLUEPRINT.json"
    if bp_path.is_file():
        try:
            doc = json.loads(bp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            doc = {}
        else:
            comps = list(doc.get("components") or [])
            if comps:
                return (
                    comps,
                    str(doc.get("rebuild_tag")) if doc.get("rebuild_tag") else None,
                    str(doc.get("content_digest")) if doc.get("content_digest") else None,
                )
    out: list[dict[str, Any]] = []
    for tier_dir in sorted(package_root.iterdir()):
        if not tier_dir.is_dir() or tier_dir.name not in VALID_TIER_DIRS:
            continue
        for jf in sorted(tier_dir.glob("*.json")):
            try:
                d = json.loads(jf.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            cid, tier, name = d.get("id"), d.get("tier"), d.get("name")
            if cid and tier and name:
                out.append({"id": cid, "tier": tier, "name": name})
    return out, None, None


def _assimilation_source_roots(project_root: Path) -> list[str]:
    p = project_root / "ASSIMILATION.json"
    if not p.is_file():
        return []
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return [str(x) for x in (doc.get("source_roots") or []) if x]


def _write_tier_init(tier_dir: Path, tier: str, rows: list[dict[str, Any]]) -> None:
    lines = [
        f'"""Tier ``{tier}`` — public surface re-exported from materialized modules (MAP = TERRAIN)."""',
        "",
    ]
    exported: list[str] = []
    seen: set[str] = set()
    for row in sorted(rows, key=lambda r: str(r.get("id") or "")):
        cid = str(row.get("id") or "")
        nm = str(row.get("name") or "")
        if not cid or not nm or not nm.isidentifier() or keyword.iskeyword(nm):
            continue
        stem = _stem_from_id(cid)
        mod_py = tier_dir / f"{stem}.py"
        if not mod_py.is_file():
            continue
        if nm in seen:
            continue
        seen.add(nm)
        lines.append(f"from .{stem} import {nm}")
        exported.append(nm)
    lines.append("")
    lines.append(f"__all__ = {exported!r}")
    lines.append("")
    (tier_dir / "__init__.py").write_text("\n".join(lines), encoding="utf-8")


def _write_root_package_init(package_root: Path, tiers: list[str]) -> None:
    lines = [
        '"""Materialized ASS-ADE root package (MAP = TERRAIN)."""',
        "",
    ]
    exported: list[str] = []
    for tier in tiers:
        if not (package_root / tier / "__init__.py").is_file():
            continue
        lines.append(f"from . import {tier}")
        exported.append(tier)
    lines.append("")
    lines.append(f"__all__ = {exported!r}")
    lines.append("")
    (package_root / "__init__.py").write_text("\n".join(lines), encoding="utf-8")


def _write_generated_smoke_tests(
    project_root: Path,
    package_root: Path,
    package_name: str,
) -> dict[str, str]:
    tests_dir = project_root / "tests" / "generated_smoke"
    tests_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = tests_dir / "_qualnames.json"
    manifest_path.write_text(
        plan_manifest_payload_for_package(package_root, package_name),
        encoding="utf-8",
    )
    test_path = tests_dir / "test_import_all_smoke.py"
    test_path.write_text(generated_smoke_test_source(), encoding="utf-8")
    return {
        "manifest": manifest_path.as_posix(),
        "smoke_test": test_path.as_posix(),
    }


def _find_nearest_pyproject(start: Path | None) -> Path | None:
    if start is None:
        return None
    current = start.resolve()
    for candidate in (current, *current.parents):
        pyproject = candidate / "pyproject.toml"
        if pyproject.is_file():
            return pyproject
    return None


def _read_source_dependencies(source_project_root: Path | None) -> list[str]:
    pyproject = _find_nearest_pyproject(source_project_root)
    if pyproject is None:
        return []
    try:
        doc = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return []
    project = doc.get("project") or {}
    deps = [str(dep) for dep in (project.get("dependencies") or []) if str(dep).strip()]
    dev_deps = [
        str(dep)
        for dep in ((project.get("optional-dependencies") or {}).get("dev") or [])
        if str(dep).strip()
    ]
    out: list[str] = []
    seen: set[str] = set()
    for dep in [*deps, *dev_deps]:
        if dep in seen:
            continue
        seen.add(dep)
        out.append(dep)
    return out


def emit_robust_package(
    target_root: Path,
    *,
    distribution_name: str,
    version: str = "0.0.0",
    gap_plan: dict[str, Any] | None = None,
    output_package_name: str | None = None,
    package_root: Path | None = None,
    source_project_root: Path | None = None,
) -> dict[str, Any]:
    """Write ``pyproject.toml``, ``README.md``, and tier ``__init__.py`` from terrain + MAP."""
    target_root = target_root.resolve()
    resolved_package_root = Path(package_root).resolve() if package_root is not None else target_root
    components, bp_tag, bp_digest = _load_intended_components(target_root, resolved_package_root)
    digest = str((gap_plan or {}).get("content_digest") or bp_digest or "")
    tag = bp_tag or target_root.name
    dependencies = _read_source_dependencies(source_project_root)

    by_tier: dict[str, list[dict[str, Any]]] = {}
    for row in components:
        t = str(row.get("tier") or "")
        if t in VALID_TIER_DIRS:
            by_tier.setdefault(t, []).append(row)

    pkg_dirs = sorted(
        p
        for p in resolved_package_root.iterdir()
        if p.is_dir() and p.name in VALID_TIER_DIRS and any(p.glob("*.py"))
    )
    tiers = [p.name for p in pkg_dirs]
    packages = (
        [output_package_name] + [f"{output_package_name}.{tier}" for tier in tiers]
        if output_package_name
        else tiers
    )
    init_count = 0
    for p in pkg_dirs:
        _write_tier_init(p, p.name, by_tier.get(p.name, []))
        init_count += 1
    if output_package_name:
        _write_root_package_init(resolved_package_root, tiers)
        init_count += 1
        smoke = _write_generated_smoke_tests(
            target_root,
            resolved_package_root,
            output_package_name,
        )
    else:
        smoke = None

    title = distribution_name.replace("-", " ").strip() or "Materialized product"
    readme_lines = [
        f"# {title}",
        "",
        "Materialized **ASS-ADE v11** product — packaging and exports follow the materialized tree (**MAP = TERRAIN**).",
        "",
        f"- **Rebuild tag:** `{tag}`",
    ]
    if digest:
        readme_lines.append(f"- **Content digest:** `{digest}`")
    if output_package_name:
        readme_lines.append(f"- **Python package root:** `src/{output_package_name}`")
    readme_lines.extend(
        [
            f"- **Declared components:** {len(components)}",
            "",
            "Authoritative intent snapshot: `BLUEPRINT.json`.",
            "",
        ]
    )
    roots = _assimilation_source_roots(target_root)
    if roots:
        readme_lines.extend(["## Assimilated source roots", ""] + [f"- `{r}`" for r in roots] + [""])
    readme_path = target_root / "README.md"
    readme_path.write_text("\n".join(readme_lines), encoding="utf-8")

    desc = (
        f"ASS-ADE v11 materialized monadic product (tag {tag}"
        + (f", digest {digest}" if digest else "")
        + ")."
    )
    dep_block = ""
    if dependencies:
        dep_lines = "\n".join(
            f"    {json.dumps(dep, ensure_ascii=True)},"
            for dep in dependencies
        )
        dep_block = f"dependencies = [\n{dep_lines}\n]\n"
    if output_package_name:
        include_line = json.dumps(f"{output_package_name}*", ensure_ascii=True)
        pyproject = f"""[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = {json.dumps(distribution_name, ensure_ascii=True)}
version = {json.dumps(version, ensure_ascii=True)}
description = {json.dumps(desc, ensure_ascii=True)}
readme = "README.md"
requires-python = ">=3.11"
{dep_block}

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[tool.setuptools]
package-dir = {{"" = "src"}}

[tool.setuptools.packages.find]
where = ["src"]
include = [{include_line}]

[tool.importlinter]
root_package = {json.dumps(output_package_name, ensure_ascii=True)}

[[tool.importlinter.contracts]]
name = "Materialized monadic tiers"
type = "layers"
layers = [
    "{output_package_name}.a4_sy_orchestration",
    "{output_package_name}.a3_og_features",
    "{output_package_name}.a2_mo_composites",
    "{output_package_name}.a1_at_functions",
    "{output_package_name}.a0_qk_constants",
]
"""
    else:
        pkg_list = ", ".join(f'"{n}"' for n in packages)
        pyproject = f"""[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = {json.dumps(distribution_name, ensure_ascii=True)}
version = {json.dumps(version, ensure_ascii=True)}
description = {json.dumps(desc, ensure_ascii=True)}
readme = "README.md"
requires-python = ">=3.11"
{dep_block}

[tool.setuptools]
packages = [{pkg_list}]
"""
    path = target_root / "pyproject.toml"
    path.write_text(pyproject, encoding="utf-8")
    return {
        "pyproject": path.as_posix(),
        "readme": readme_path.as_posix(),
        "package_root": resolved_package_root.as_posix(),
        "importable": len(packages) > 0,
        "packages": packages,
        "generated_smoke": smoke,
        "tier_packages_initialized": init_count,
        "components_declared": len(components),
        "emit": "robust_map_terrain",
    }

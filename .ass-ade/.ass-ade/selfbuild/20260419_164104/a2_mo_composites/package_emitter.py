"""Package Emitter — turn a rebuild folder into a pip-installable Python package.

Writes ``__init__.py`` per tier (with real imports, not just ``__all__`` lists)
and a root ``pyproject.toml`` that includes the source project's dependencies
and CLI entry points.
"""

from __future__ import annotations

import ast
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

TIER_NAMES: tuple[str, ...] = (
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
)


def _enforce_boundary(path: Path, control_root: Path) -> None:
    try:
        path.resolve().relative_to(control_root.resolve())
    except ValueError:
        raise RuntimeError(
            f"Security boundary: attempted write to {path!r} "
            f"outside rebuild root {control_root!r}."
        )


def _extract_public_names(py_path: Path) -> list[str]:
    """Return top-level public names (functions, classes, assignments) from a .py file."""
    try:
        source = py_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(py_path))
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.append(target.id)
    return names


def _build_tier_init(py_files: list[Path]) -> str:
    """Generate a tier __init__.py that actually imports public symbols."""
    lines: list[str] = ['"""Auto-generated tier package."""', ""]
    all_exported: list[str] = []

    for py_file in sorted(py_files):
        stem = py_file.stem
        names = _extract_public_names(py_file)
        if names:
            lines.append(f"from .{stem} import {', '.join(sorted(names))}")
            all_exported.extend(names)
        else:
            lines.append(f"from . import {stem}")

    if all_exported:
        lines.append("")
        lines.append("__all__ = [")
        for name in sorted(set(all_exported)):
            lines.append(f'    "{name}",')
        lines.append("]")

    lines.append("")
    return "\n".join(lines)


def _build_top_init(tier_names: list[str]) -> str:
    """Generate root __init__.py that imports each tier subpackage."""
    lines: list[str] = ['"""Auto-generated rebuild package."""', ""]
    for tier in sorted(tier_names):
        lines.append(f"from . import {tier}")
    if tier_names:
        lines.append("")
        lines.append("__all__ = [")
        for tier in sorted(tier_names):
            lines.append(f'    "{tier}",')
        lines.append("]")
    lines.append("")
    return "\n".join(lines)


def _read_source_pyproject(source_root: Path) -> tuple[list[str], dict[str, str]]:
    """Read dependencies and scripts from the source project's pyproject.toml.

    Walks up the directory tree from ``source_root`` to find the nearest
    ``pyproject.toml`` (handles ``src/`` layout projects).

    Returns (deps_list, scripts_dict).
    """
    # Walk up the directory tree to find pyproject.toml
    candidate = source_root
    pyproject = None
    for _ in range(5):  # limit search depth
        if (candidate / "pyproject.toml").exists():
            pyproject = candidate / "pyproject.toml"
            break
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    if pyproject is None:
        return [], {}
    text = pyproject.read_text(encoding="utf-8")
    data: dict[str, Any] = {}
    # Use tomllib (stdlib ≥3.11) with fallback to tomli
    try:
        if sys.version_info >= (3, 11):
            import tomllib
            data = tomllib.loads(text)
        else:
            import tomli  # type: ignore[import-untyped]
            data = tomli.loads(text)
    except Exception:  # noqa: BLE001
        return [], {}
    proj = data.get("project", {})
    deps: list[str] = proj.get("dependencies", [])
    scripts: dict[str, str] = proj.get("scripts", {})
    return deps, scripts


def _find_cli_entry_point(tier_names: list[str], target_root: Path) -> dict[str, str]:
    """Detect a Typer ``app`` or ``def main(`` in a4_sy_orchestration and return scripts."""
    sy_dir = target_root / "a4_sy_orchestration"
    if not sy_dir.exists():
        return {}
    for py_file in sorted(sy_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Typer app pattern
        if re.search(r"^app\s*=\s*typer\.Typer", source, re.MULTILINE):
            cmd = py_file.stem.replace("_", "-")
            return {cmd: f"a4_sy_orchestration.{py_file.stem}:app"}
        # Plain main() pattern
        if re.search(r"^def main\(", source, re.MULTILINE):
            cmd = py_file.stem.replace("_", "-")
            return {cmd: f"a4_sy_orchestration.{py_file.stem}:main"}
    return {}


def _build_pyproject(
    package_name: str,
    deps: list[str] | None = None,
    entry_points: dict[str, str] | None = None,
    src_layout: bool = True,
) -> str:
    dep_block = ""
    if deps:
        dep_lines = "".join(f'    "{d}",\n' for d in deps)
        dep_block = f"dependencies = [\n{dep_lines}]\n"

    script_block = ""
    if entry_points:
        script_lines = "".join(f'{k} = "{v}"\n' for k, v in entry_points.items())
        script_block = f"\n[project.scripts]\n{script_lines}"

    wheel_packages = (
        f'packages = ["src/{package_name}"]' if src_layout else 'packages = ["."]'
    )

    return (
        "[build-system]\n"
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n'
        "\n"
        "[project]\n"
        f'name = "{package_name}"\n'
        'version = "0.1.0.dev0"\n'
        'description = "Auto-emitted rebuild package"\n'
        'requires-python = ">=3.11"\n'
        f"{dep_block}"
        f"{script_block}"
        "\n"
        "[tool.hatch.build.targets.wheel]\n"
        f"{wheel_packages}\n"
    )


def _compile_check(text: str, path: str) -> bool:
    try:
        compile(text, path, "exec")
        return True
    except SyntaxError:
        return False


def emit_runnable_package(
    target_root: Path,
    *,
    package_name: str = "ass_ade_rebuild",
    control_root: Path | None = None,
    source_root: Path | None = None,
) -> dict[str, Any]:
    """Turn a rebuild folder into a pip-installable Python package.

    Args:
        target_root:   The rebuild output folder (e.g. ``output/20260418_153000``).
        package_name:  Name for the generated package.
        control_root:  Safety boundary — writes must stay inside this directory.
        source_root:   Original source directory; used to read dependencies and
                       CLI entry points from its ``pyproject.toml``.

    Returns:
        Dict with ``package_root``, ``init_files``, ``pyproject``, ``importable``.
    """
    target_root = Path(target_root).resolve()
    if control_root is None:
        control_root = target_root

    _enforce_boundary(target_root, control_root)

    # Read source project metadata (deps + scripts)
    source_deps: list[str] = []
    source_scripts: dict[str, str] = {}
    if source_root is not None:
        source_deps, source_scripts = _read_source_pyproject(Path(source_root))

    init_files: list[str] = []
    importable: bool = True
    tier_names_present: list[str] = []

    for tier in TIER_NAMES:
        tier_dir = target_root / tier
        if not tier_dir.is_dir():
            continue
        # Include ALL .py files in the tier directory (not just draft-prefixed ones)
        py_files = [
            f
            for f in sorted(tier_dir.iterdir())
            if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
        ]
        if not py_files:
            continue

        tier_names_present.append(tier)
        tier_init_path = tier_dir / "__init__.py"
        _enforce_boundary(tier_init_path, control_root)
        tier_init_text = _build_tier_init(py_files)
        tier_init_path.write_text(tier_init_text, encoding="utf-8")
        init_files.append(str(tier_init_path))
        if not _compile_check(tier_init_text, str(tier_init_path)):
            importable = False

    top_init_path = target_root / "__init__.py"
    _enforce_boundary(top_init_path, control_root)
    top_init_text = _build_top_init(tier_names_present)
    top_init_path.write_text(top_init_text, encoding="utf-8")
    init_files.append(str(top_init_path))
    if not _compile_check(top_init_text, str(top_init_path)):
        importable = False

    # ── Also generate __init__.py files for src/ layout ──────────────────────
    src_pkg_root = target_root / "src" / package_name
    if src_pkg_root.exists():
        src_tier_names: list[str] = []
        for tier in TIER_NAMES:
            tier_src_dir = src_pkg_root / tier
            if not tier_src_dir.is_dir():
                continue
            py_files_src = [
                f for f in sorted(tier_src_dir.iterdir())
                if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
            ]
            if not py_files_src:
                continue
            src_tier_names.append(tier)
            tier_src_init = tier_src_dir / "__init__.py"
            _enforce_boundary(tier_src_init, control_root)
            tier_src_init_text = _build_tier_init(py_files_src)
            tier_src_init.write_text(tier_src_init_text, encoding="utf-8")
            init_files.append(str(tier_src_init))
            if not _compile_check(tier_src_init_text, str(tier_src_init)):
                importable = False

        src_top_init = src_pkg_root / "__init__.py"
        _enforce_boundary(src_top_init, control_root)
        src_top_init_text = _build_top_init(src_tier_names)
        src_top_init.write_text(src_top_init_text, encoding="utf-8")
        init_files.append(str(src_top_init))
        if not _compile_check(src_top_init_text, str(src_top_init)):
            importable = False

    # Determine CLI entry points: prefer source scripts, fall back to detection
    entry_points = source_scripts or _find_cli_entry_point(tier_names_present, target_root)

    pyproject_path = target_root / "pyproject.toml"
    _enforce_boundary(pyproject_path, control_root)
    pyproject_path.write_text(
        _build_pyproject(
            package_name,
            deps=source_deps or None,
            entry_points=entry_points or None,
            src_layout=src_pkg_root.exists(),
        ),
        encoding="utf-8",
    )

    return {
        "package_root": str(target_root),
        "init_files": init_files,
        "pyproject": str(pyproject_path),
        "importable": importable,
    }


def emit_tier_map(
    target_root: Path,
    tier_map: dict[str, dict[str, str]],
    *,
    package_name: str = "ass_ade_rebuild",
    control_root: Path | None = None,
) -> str:
    """Write .ass-ade/tier-map.json — master file → tier assignment map."""
    control_root = control_root or target_root
    ass_ade_dir = target_root / ".ass-ade"
    ass_ade_dir.mkdir(parents=True, exist_ok=True)
    tier_map_path = ass_ade_dir / "tier-map.json"
    _enforce_boundary(tier_map_path, control_root)
    payload = {
        "files": tier_map,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "package": package_name,
        "version": "0.2.0",
    }
    tier_map_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return tier_map_path.as_posix()


def emit_agent_configs(
    target_root: Path,
    *,
    package_name: str = "ass_ade_rebuild",
    control_root: Path | None = None,
) -> dict[str, str]:
    """Write .claude/CLAUDE.md, .vscode/tasks.json, .ass-ade/config.json."""
    control_root = control_root or target_root
    written: dict[str, str] = {}

    claude_dir = target_root / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_md = claude_dir / "CLAUDE.md"
    _enforce_boundary(claude_md, control_root)
    claude_md.write_text(
        f"# {package_name} — Tier-Aware Rebuild\n\n"
        "## Layout\n"
        f"- `src/{package_name}/` — installable Python package (src layout)\n"
        "- `a0_qk_constants/` through `a4_sy_orchestration/` — tier overlays with TIER_OVERLAY.json\n"
        "- `.ass-ade/tier-map.json` — master file → tier assignment map\n\n"
        "## Tiers\n"
        "| Tier | Classification |\n"
        "|------|----------------|\n"
        "| a0_qk_constants | constant |\n"
        "| a1_at_functions | pure_function |\n"
        "| a2_mo_composites | composite |\n"
        "| a3_og_features | feature |\n"
        "| a4_sy_orchestration | orchestrator |\n\n"
        "## Install\n"
        "```\npip install -e .\n```\n",
        encoding="utf-8",
    )
    written["claude_md"] = claude_md.as_posix()

    vscode_dir = target_root / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    tasks_path = vscode_dir / "tasks.json"
    _enforce_boundary(tasks_path, control_root)
    tasks_payload = {
        "version": "2.0.0",
        "tasks": [
            {
                "group": "build",
                "label": "ass-ade: install package",
                "options": {"cwd": "${workspaceFolder}"},
                "type": "shell",
                "command": "pip install -e .",
            },
            {
                "label": "ass-ade: validate rebuild",
                "options": {"cwd": "${workspaceFolder}"},
                "type": "shell",
                "command": (
                    "python -c \""
                    "from ass_ade.engine.rebuild.schema_materializer import validate_rebuild; "
                    "from pathlib import Path; import json; "
                    "print(json.dumps(validate_rebuild(Path('.')), indent=2))\""
                ),
            },
        ],
    }
    tasks_path.write_text(json.dumps(tasks_payload, indent=2) + "\n", encoding="utf-8")
    written["vscode_tasks"] = tasks_path.as_posix()

    ass_ade_dir = target_root / ".ass-ade"
    ass_ade_dir.mkdir(parents=True, exist_ok=True)
    config_path = ass_ade_dir / "config.json"
    _enforce_boundary(config_path, control_root)
    config_payload = {
        "package_name": package_name,
        "schema": "ASSADE-LAYOUT-1",
        "src_layout": f"src/{package_name}",
        "tier_map": ".ass-ade/tier-map.json",
        "tiers": list(TIER_NAMES),
    }
    config_path.write_text(
        json.dumps(config_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    written["ass_ade_config"] = config_path.as_posix()

    return written

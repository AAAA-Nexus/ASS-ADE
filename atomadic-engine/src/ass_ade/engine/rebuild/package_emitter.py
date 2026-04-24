"""Package Emitter — turn a rebuild folder into a pip-installable Python package.

Writes ``__init__.py`` per tier (with real imports, not just ``__all__`` lists)
and a root ``pyproject.toml`` that includes the source project's dependencies
and CLI entry points.
"""

from __future__ import annotations

import ast
import datetime as _dt
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from ass_ade.engine.rebuild.autopoiesis_layout import (
    episodes_jsonl_path,
    format_package_emit_episode_line,
    iter_autopoiesis_topic_paths,
)

# Minimal deps so ``pip install -e .`` on a rebuild folder runs ``ass-ade`` without
# hand-editing pyproject (source tree may have no pyproject.toml at repo root).
_DEFAULT_PYPROJECT_DEPS: tuple[str, ...] = (
    "httpx>=0.28,<0.29",
    "pydantic>=2.11,<3",
    "rich>=14,<15",
    "typer>=0.15,<1",
    "python-dotenv>=1.0,<2",
    # ass_ade.mcp.utils (imported by ass_ade.cli) validates MCP payloads
    "jsonschema>=4.23,<5",
)

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
    """Generate root ``__init__.py`` (shim only).

    Tier directories are separate top-level packages (see Hatch ``packages``).
    Avoid eager ``import a*`` here so pytest and other tools can load this file
    without pulling the full tier graph during collection.
    """
    _ = tier_names  # emitted for symmetry with tier dir layout; no eager imports
    return (
        '"""Auto-generated rebuild package (tier dirs are top-level Hatch packages)."""\n'
        "\n"
    )


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


def _vendor_ignore(_src: str, names: list[str]) -> list[str]:
    skip = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return [n for n in names if n in skip or n.endswith(".pyc")]


def _copy_ass_ade_vendor(vendor_repo_root: Path, target_root: Path, control_root: Path) -> bool:
    """Copy ``src/ass_ade`` from a canonical ASS-ADE repo into ``target_root/ass_ade``."""
    src_pkg = (vendor_repo_root / "src" / "ass_ade").resolve()
    if not (src_pkg.is_dir() and (src_pkg / "__init__.py").is_file()):
        return False
    dest = (target_root / "ass_ade").resolve()
    _enforce_boundary(dest, control_root)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src_pkg, dest, ignore=_vendor_ignore)
    return True


def _copy_support_artifacts_from_repo(
    vendor_repo_root: Path,
    target_root: Path,
    control_root: Path,
    *,
    copy_dotenv: bool,
) -> dict[str, bool]:
    """Copy monadic config, tier map, and optionally ``.env`` for out-of-the-box dev."""
    done = {"config_json": False, "tier_map": False, "dotenv": False}
    ass_ade_meta = vendor_repo_root / ".ass-ade"
    if not ass_ade_meta.is_dir():
        return done
    dest_meta = target_root / ".ass-ade"
    _enforce_boundary(dest_meta, control_root)
    dest_meta.mkdir(parents=True, exist_ok=True)
    cfg_src = ass_ade_meta / "config.json"
    if cfg_src.is_file():
        shutil.copy2(cfg_src, dest_meta / "config.json")
        done["config_json"] = True
    tier_src = ass_ade_meta / "tier-map.json"
    if tier_src.is_file():
        shutil.copy2(tier_src, dest_meta / "tier-map.json")
        done["tier_map"] = True
    env_src = vendor_repo_root / ".env"
    if copy_dotenv and env_src.is_file():
        dest_env = target_root / ".env"
        _enforce_boundary(dest_env, control_root)
        shutil.copy2(env_src, dest_env)
        done["dotenv"] = True
    return done


def _write_rebuild_gitignore(target_root: Path, control_root: Path) -> None:
    """Avoid accidental commit of copied local secrets."""
    path = target_root / ".gitignore"
    _enforce_boundary(path, control_root)
    if not path.exists():
        path.write_text(
            "# Generated by ASS-ADE rebuild — local-only secrets\n"
            ".env\n"
            ".venv/\n"
            ".pytest_cache/\n",
            encoding="utf-8",
        )


def _find_cli_entry_point(tier_names: list[str], target_root: Path) -> dict[str, str]:
    """Detect a Typer ``app`` or ``def main`` in tier packages (a1 CLI, then a4)."""
    for subpkg, prefix in (
        ("a1_at_functions", "a1_at_functions"),
        ("a4_sy_orchestration", "a4_sy_orchestration"),
    ):
        tier_dir = target_root / subpkg
        if not tier_dir.is_dir():
            continue
        for py_file in sorted(tier_dir.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            try:
                source = py_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if re.search(r"^app\s*=\s*typer\.Typer", source, re.MULTILINE):
                cmd = "ass-ade" if py_file.stem == "cli" else py_file.stem.replace("_", "-")
                return {cmd: f"{prefix}.{py_file.stem}:app"}
            if re.search(r"^def main\(", source, re.MULTILINE):
                cmd = py_file.stem.replace("_", "-")
                return {cmd: f"{prefix}.{py_file.stem}:main"}
    return {}


def _hatch_wheel_package_dirs(
    target_root: Path,
    tier_names_present: list[str],
    *,
    vendored_ass_ade: bool,
) -> list[str]:
    """Top-level importable directories to list for Hatch (explicit > implicit ``'.'``)."""
    names: list[str] = []
    if vendored_ass_ade and (target_root / "ass_ade" / "__init__.py").is_file():
        names.append("ass_ade")
    for tier in tier_names_present:
        if (target_root / tier / "__init__.py").is_file():
            names.append(tier)
    return names


def _dependency_distribution_name(spec: str) -> str:
    """Normalize a PEP 508 dependency line to a comparable distribution name."""
    s = spec.strip()
    if not s:
        return ""
    bracket = s.find("[")
    if bracket != -1:
        s = s[:bracket].strip()
    for sep in (">=", "==", "~=", "!=", "<=", "<", ">", " @", ";"):
        idx = s.find(sep)
        if idx != -1:
            s = s[:idx].strip()
            break
    return s.strip().lower().replace("_", "-")


def _merge_emit_dependencies(source_deps: list[str]) -> list[str]:
    """Merge canonical ``[project.dependencies]`` with emitter defaults.

    Defaults supply any distribution missing from the source list; the source
    wins on version pins when it declares the same distribution (so emitted
    wheels stay aligned with canonical pins while still including e.g.
    ``jsonschema`` required by ``ass_ade.mcp.utils``).
    """
    if not source_deps:
        return list(_DEFAULT_PYPROJECT_DEPS)
    merged: dict[str, str] = {}
    for d in _DEFAULT_PYPROJECT_DEPS:
        merged[_dependency_distribution_name(d)] = d
    for s in source_deps:
        merged[_dependency_distribution_name(s)] = s
    out: list[str] = []
    for d in _DEFAULT_PYPROJECT_DEPS:
        out.append(merged[_dependency_distribution_name(d)])
    default_names = {_dependency_distribution_name(d) for d in _DEFAULT_PYPROJECT_DEPS}
    for s in source_deps:
        name = _dependency_distribution_name(s)
        if name not in default_names:
            out.append(merged[name])
    return out


_EMIT_SMOKE_TEST_PY = '''"""Auto-emitted import smoke tests (fail fast on missing runtime deps)."""


def test_jsonschema_importable() -> None:
    import jsonschema  # noqa: F401


def test_mcp_utils_importable() -> None:
    import ass_ade.mcp.utils  # noqa: F401


def test_cli_module_importable() -> None:
    import ass_ade.cli  # noqa: F401
'''


def _write_emit_smoke_tests(target_root: Path, control_root: Path) -> str | None:
    """Write ``tests/test_emit_smoke_imports.py`` when vendoring ``ass_ade``."""
    tests_dir = target_root / "tests"
    _enforce_boundary(tests_dir, control_root)
    tests_dir.mkdir(parents=True, exist_ok=True)
    path = tests_dir / "test_emit_smoke_imports.py"
    _enforce_boundary(path, control_root)
    path.write_text(_EMIT_SMOKE_TEST_PY, encoding="utf-8")
    return str(path)


def _build_pyproject(
    package_name: str,
    deps: list[str] | None = None,
    entry_points: dict[str, str] | None = None,
    *,
    wheel_package_dirs: list[str] | None = None,
    include_dev_optional: bool = False,
    include_pytest_ini: bool = False,
) -> str:
    resolved_deps = list(deps) if deps else []
    if not resolved_deps:
        resolved_deps = list(_DEFAULT_PYPROJECT_DEPS)
    dep_lines = "".join(f'    "{d}",\n' for d in resolved_deps)
    dep_block = f"dependencies = [\n{dep_lines}]\n"

    script_block = ""
    if entry_points:
        script_lines = "".join(f'{k} = "{v}"\n' for k, v in entry_points.items())
        script_block = f"\n[project.scripts]\n{script_lines}"

    if wheel_package_dirs:
        pkg_lines = "".join(f'    "{name}",\n' for name in wheel_package_dirs)
        hatch_wheel = f'[tool.hatch.build.targets.wheel]\npackages = [\n{pkg_lines}]\n'
    else:
        hatch_wheel = '[tool.hatch.build.targets.wheel]\npackages = ["."]\n'

    extra_toml = ""
    if include_dev_optional:
        extra_toml += (
            "\n[project.optional-dependencies]\n"
            "dev = [\n"
            '    "pytest>=8.0,<9",\n'
            "]\n"
        )
    if include_pytest_ini:
        extra_toml += '\n[tool.pytest.ini_options]\ntestpaths = ["tests"]\n'

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
        f"{hatch_wheel}"
        f"{extra_toml}"
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
    vendor_repo_root: Path | None = None,
    copy_dotenv: bool = True,
) -> dict[str, Any]:
    """Turn a rebuild folder into a pip-installable Python package.

    Args:
        target_root:   The rebuild output folder (e.g. ``output/20260418_153000``).
        package_name:  Name for the generated package.
        control_root:  Safety boundary — writes must stay inside this directory.
        source_root:   Original source directory; used to read dependencies and
                       CLI entry points from its ``pyproject.toml``.
        vendor_repo_root:  Root of a canonical ASS-ADE repo (contains ``src/ass_ade``).
                           When set, copies the full ``ass_ade`` package plus
                           ``.ass-ade/config.json``, ``tier-map.json``, and optionally ``.env``
                           so ``ass-ade`` works without ``PYTHONPATH`` hacks.
        copy_dotenv:   When ``vendor_repo_root`` is set, copy ``.env`` if present.

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

    vendored = False
    support_copies: dict[str, bool] = {}
    if vendor_repo_root is not None:
        vendored = _copy_ass_ade_vendor(vendor_repo_root, target_root, control_root)
        support_copies = _copy_support_artifacts_from_repo(
            vendor_repo_root,
            target_root,
            control_root,
            copy_dotenv=copy_dotenv,
        )
        _write_rebuild_gitignore(target_root, control_root)

    wheel_dirs = _hatch_wheel_package_dirs(target_root, tier_names_present, vendored_ass_ade=vendored)

    # Autopoiesis MVA: topic shards under .ass-ade/memory (dirs only; no secrets).
    for topic_path in iter_autopoiesis_topic_paths(target_root):
        _enforce_boundary(topic_path, control_root)
        topic_path.mkdir(parents=True, exist_ok=True)

    episode_appended = False
    try:
        log_path = episodes_jsonl_path(target_root)
        _enforce_boundary(log_path, control_root)
        line = format_package_emit_episode_line(
            utc_iso=_dt.datetime.now(_dt.timezone.utc).isoformat(),
            vendored_ass_ade=vendored,
            hatch_wheel_packages=list(wheel_dirs),
        )
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        episode_appended = True
    except OSError:
        episode_appended = False

    entry_points: dict[str, str] = {}
    if source_scripts:
        entry_points.update(source_scripts)
    if vendored and (target_root / "ass_ade" / "cli.py").is_file():
        entry_points["ass-ade"] = "ass_ade.cli:app"
    elif not entry_points:
        entry_points.update(_find_cli_entry_point(tier_names_present, target_root))

    deps_for_emit = _merge_emit_dependencies(source_deps)
    smoke_test_file: str | None = None
    if vendored:
        smoke_test_file = _write_emit_smoke_tests(target_root, control_root)

    pyproject_path = target_root / "pyproject.toml"
    _enforce_boundary(pyproject_path, control_root)
    pyproject_path.write_text(
        _build_pyproject(
            package_name,
            deps=deps_for_emit,
            entry_points=entry_points or None,
            wheel_package_dirs=wheel_dirs or None,
            include_dev_optional=bool(vendored),
            include_pytest_ini=bool(vendored),
        ),
        encoding="utf-8",
    )

    return {
        "package_root": str(target_root),
        "init_files": init_files,
        "pyproject": str(pyproject_path),
        "importable": importable,
        "vendored_ass_ade": vendored,
        "support_copies": support_copies,
        "hatch_wheel_packages": wheel_dirs,
        "autopoiesis_episode_appended": episode_appended,
        "emit_smoke_tests": smoke_test_file,
    }

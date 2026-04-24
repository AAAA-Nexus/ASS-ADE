"""Tier a1 — assimilated function 'emit_runnable_package'

Assimilated from: rebuild/package_emitter.py:501-688
"""

from __future__ import annotations


# --- assimilated symbol ---
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
        tier_init_text = _build_tier_init()
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

    source_package_dirs: list[str] = []
    if source_root is not None:
        source_package_dirs = _copy_source_package_surface(
            Path(source_root),
            target_root,
            control_root,
        )

    wheel_dirs = _hatch_wheel_package_dirs(
        target_root,
        tier_names_present,
        vendored_ass_ade=vendored,
        source_package_dirs=source_package_dirs,
    )

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
    generated_bridge: dict[str, Any] | None = None
    generated_quality: dict[str, Any] | None = None
    if vendored:
        smoke_test_file = _write_emit_smoke_tests(target_root, control_root)
    generated_bridge = emit_multilang_bridge_suite(
        target_root,
        control_root=control_root,
        package_name=package_name,
        tier_names_present=tier_names_present,
        vendored_ass_ade=vendored,
    )
    generated_quality = emit_generated_quality_suite(
        target_root,
        control_root=control_root,
        tier_names_present=tier_names_present,
        vendored_ass_ade=vendored,
        base_test_files=[
            *( [smoke_test_file] if smoke_test_file else [] ),
            *((generated_bridge or {}).get("generated_tests") or []),
        ],
    )

    pyproject_path = target_root / "pyproject.toml"
    _enforce_boundary(pyproject_path, control_root)
    pyproject_path.write_text(
        _build_pyproject(
            package_name,
            deps=deps_for_emit,
            entry_points=entry_points or None,
            wheel_package_dirs=wheel_dirs or None,
            include_dev_optional=True,
            include_pytest_ini=True,
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
        "source_package_dirs": source_package_dirs,
        "autopoiesis_episode_appended": episode_appended,
        "emit_smoke_tests": smoke_test_file,
        "generated_tests": (generated_quality or {}).get("generated_tests", []),
        "coverage_manifests": (generated_quality or {}).get("coverage_manifests", []),
        "coverage_reports": (generated_quality or {}).get("coverage_reports", []),
        "coverage_python_targets": (generated_quality or {}).get("python_targets", 0),
        "coverage_component_targets": (generated_quality or {}).get("component_targets", 0),
        "coverage_public_symbols": (generated_quality or {}).get("public_symbols", 0),
        "bridge_reports": (generated_bridge or {}).get("bridge_reports", []),
        "bridge_manifests": (generated_bridge or {}).get("bridge_manifests", []),
        "bridge_files": (generated_bridge or {}).get("bridge_files", []),
        "bridge_languages": (generated_bridge or {}).get("bridge_languages", []),
        "bridge_ready": (generated_bridge or {}).get("bridge_ready", False),
    }


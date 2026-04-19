# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_emit_runnable_package.py:5
# Component id: at.source.ass_ade.emit_runnable_package
__version__ = "0.1.0"

def emit_runnable_package(
    target_root: Path,
    *,
    package_name: str = "ass_ade_rebuild",
    control_root: Path | None = None,
) -> dict[str, Any]:
    """Turn a rebuild folder into a pip-installable Python package.

    Returns a dict with ``package_root``, ``init_files``, ``pyproject``, ``importable``.
    """
    target_root = Path(target_root).resolve()
    if control_root is None:
        control_root = target_root

    _enforce_boundary(target_root, control_root)

    init_files: list[str] = []
    importable: bool = True
    tier_names_present: list[str] = []

    for tier in TIER_NAMES:
        tier_dir = target_root / tier
        if not tier_dir.is_dir():
            continue
        py_files = [
            f
            for f in tier_dir.iterdir()
            if f.is_file() and f.suffix == ".py" and _DRAFT_PY_RE.match(f.name)
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

    pyproject_path = target_root / "pyproject.toml"
    _enforce_boundary(pyproject_path, control_root)
    pyproject_path.write_text(_build_pyproject(package_name), encoding="utf-8")

    return {
        "package_root": str(target_root),
        "init_files": init_files,
        "pyproject": str(pyproject_path),
        "importable": importable,
    }

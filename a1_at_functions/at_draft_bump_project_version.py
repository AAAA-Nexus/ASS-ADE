# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_bump_project_version.py:5
# Component id: at.source.ass_ade.bump_project_version
__version__ = "0.1.0"

def bump_project_version(
    *,
    root: Path,
    bump: str,
    new_version: str = "",
    summary: str = "Version update",
    dry_run: bool = False,
) -> VersionBumpResult:
    root = root.resolve()
    old_version, target_version = calculate_next_version(root, bump, new_version)
    files_updated: list[str] = []
    files_backed_up: list[str] = []
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = root / DEFAULT_EVOLUTION_DIR / "version-backups" / f"{old_version}-to-{target_version}-{timestamp}"

    def backup_file(path: Path) -> None:
        if dry_run or not path.exists():
            return
        rel = path.relative_to(root)
        target = backup_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        files_backed_up.append(str(target))

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        backup_file(pyproject)
        updated = _replace_project_version(pyproject.read_text(encoding="utf-8"), target_version)
        if not dry_run:
            pyproject.write_text(updated, encoding="utf-8")
        files_updated.append(str(pyproject))

    init_file = root / "src" / "ass_ade" / "__init__.py"
    if init_file.exists():
        backup_file(init_file)
        updated = _replace_init_version(init_file.read_text(encoding="utf-8"), target_version)
        if not dry_run:
            init_file.write_text(updated, encoding="utf-8")
        files_updated.append(str(init_file))

    readme = root / "README.md"
    if readme.exists():
        backup_file(readme)
        updated = _replace_readme_version(readme.read_text(encoding="utf-8"), target_version)
        if not dry_run:
            readme.write_text(updated, encoding="utf-8")
        files_updated.append(str(readme))

    changelog = root / "CHANGELOG.md"
    if changelog.exists():
        backup_file(changelog)
        release_timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        updated = _insert_changelog_entry(
            changelog.read_text(encoding="utf-8"),
            target_version,
            summary,
            release_timestamp,
        )
        if not dry_run:
            changelog.write_text(updated, encoding="utf-8")
        files_updated.append(str(changelog))

    return VersionBumpResult(
        old_version=old_version,
        new_version=target_version,
        bump=bump,
        dry_run=dry_run,
        files_updated=files_updated,
        backup_dir=str(backup_dir) if files_backed_up else "",
        files_backed_up=files_backed_up,
    )

# Extracted from C:/!ass-ade/tests/test_protocol.py:95
# Component id: at.source.ass_ade.test_bump_project_version_updates_public_surfaces
from __future__ import annotations

__version__ = "0.1.0"

def test_bump_project_version_updates_public_surfaces(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    package_dir = tmp_path / "src" / "ass_ade"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text('__version__ = "0.0.1"\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n\n**Version:** 0.0.1\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n", encoding="utf-8")

    result = bump_project_version(
        root=tmp_path,
        bump="minor",
        summary="Prepare next evolution branch",
    )

    assert result.old_version == "0.0.1"
    assert result.new_version == "0.1.0"
    assert 'version = "0.1.0"' in (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert '__version__ = "0.1.0"' in (package_dir / "__init__.py").read_text(encoding="utf-8")
    assert "**Version:** 0.1.0" in (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "## [0.1.0]" in (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8")
    assert result.backup_dir
    assert len(result.files_backed_up) == 4
    assert (Path(result.backup_dir) / "pyproject.toml").exists()

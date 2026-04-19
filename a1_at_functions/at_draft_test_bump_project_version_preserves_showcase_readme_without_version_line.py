# Extracted from C:/!ass-ade/tests/test_protocol.py:123
# Component id: at.source.ass_ade.test_bump_project_version_preserves_showcase_readme_without_version_line
from __future__ import annotations

__version__ = "0.1.0"

def test_bump_project_version_preserves_showcase_readme_without_version_line(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    package_dir = tmp_path / "src" / "ass_ade"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text('__version__ = "0.0.1"\n', encoding="utf-8")
    readme = tmp_path / "README.md"
    showcase = b"# Showcase README\r\n\r\nNo version marker here.\r\n"
    readme.write_bytes(showcase)

    result = bump_project_version(root=tmp_path, bump="patch")

    assert readme.read_bytes() == showcase
    assert str(readme) not in result.files_updated

# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:145
# Component id: at.source.ass_ade.test_iter_files_skips_ignored_dirs
from __future__ import annotations

__version__ = "0.1.0"

def test_iter_files_skips_ignored_dirs(tmp_path: Path) -> None:
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "pkg.py").write_text("x=1", encoding="utf-8")
    (tmp_path / "main.py").write_text("x=1", encoding="utf-8")
    files = _iter_files(tmp_path)
    names = [f.name for f in files]
    assert "main.py" in names
    assert "pkg.py" not in names

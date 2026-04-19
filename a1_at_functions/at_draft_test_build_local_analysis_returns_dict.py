# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_build_local_analysis_returns_dict.py:7
# Component id: at.source.a1_at_functions.test_build_local_analysis_returns_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_build_local_analysis_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )

    analysis = build_local_analysis(tmp_path)

    assert isinstance(analysis, dict)
    for key in ("root", "languages", "metadata", "symbols", "test_framework", "ci", "summary"):
        assert key in analysis, f"missing key: {key}"

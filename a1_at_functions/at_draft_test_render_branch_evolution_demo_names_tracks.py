# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_render_branch_evolution_demo_names_tracks.py:7
# Component id: at.source.a1_at_functions.test_render_branch_evolution_demo_names_tracks
from __future__ import annotations

__version__ = "0.1.0"

def test_render_branch_evolution_demo_names_tracks(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    markdown = render_branch_evolution_demo(
        root=tmp_path,
        branches=["tests-first", "docs-first"],
        iterations=2,
    )

    assert "git switch -c evolve/tests-first" in markdown
    assert "docs-first iteration 2" in markdown
    assert "ass-ade protocol evolution-record" in markdown

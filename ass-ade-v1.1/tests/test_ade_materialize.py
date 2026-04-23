"""ASS-ADE ``.ade`` materialize — smoke: discover monorepo, write ``.ade`` in temp."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from ass_ade_v11.ade import ADE_LAYOUT_VERSION, materialize_dotted_ade
from ass_ade_v11.ade.discover import find_monorepo_root


def test_ade_layout_version() -> None:
    assert ADE_LAYOUT_VERSION >= 1


def test_find_monorepo_uses_cwd() -> None:
    root = find_monorepo_root(None)
    assert root is not None
    assert (Path(root) / "agents" / "INDEX.md").is_file()


def test_materialize_creates_ade_with_layout(tmp_path: Path) -> None:
    monorepo = find_monorepo_root(None)
    if monorepo is None:  # pragma: no cover
        raise RuntimeError("need agents/INDEX.md in walkable tree")
    out = tmp_path / "app"
    out.mkdir()
    r = materialize_dotted_ade(
        out,
        source=monorepo,
        with_agents=False,
        install_cursor=False,
    )
    assert (r.ade_dir / "LAYOUT.json").is_file()
    layout = json.loads((r.ade_dir / "LAYOUT.json").read_text(encoding="utf-8"))
    assert layout.get("ade_layout_version") == ADE_LAYOUT_VERSION
    assert (r.ade_dir / "cursor-hooks" / "swarm_signal.py").is_file()
    assert (r.ade_dir / "persistent" / "run_swarm_services.py").is_file()
    assert (r.ade_dir / "cross-ide" / "CODEX-BUILD-CYCLE.md").is_file()
    assert (r.ade_dir / "cross-ide" / "vscode-mcp.example.json").is_file()
    assert (r.ade_dir / "SWARM-ONE-PROMPT.md").is_file()

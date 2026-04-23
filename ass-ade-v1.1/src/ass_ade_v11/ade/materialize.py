from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ass_ade_v11.ade.discover import find_monorepo_root
from ass_ade_v11.ade.versions import ADE_LAYOUT_VERSION

ISO = "%Y-%m-%dT%H:%M:%SZ"


@dataclass(frozen=True)
class MaterializeResult:
    """Paths written under ``workspace / ".ade"`` and optional ``.cursor``."""

    ade_dir: Path
    cursor_installed: bool
    source_root: Path
    files_written: int


def _now() -> str:
    return datetime.now(timezone.utc).strftime(ISO)


def _copy_file(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def _copy_tree_selective(
    src_dir: Path, dst_dir: Path, globs: tuple[str, ...], *, max_files: int = 5000
) -> int:
    if not src_dir.is_dir():
        return 0
    n = 0
    for pat in globs:
        for p in sorted(src_dir.glob(pat)):
            if p.is_file() and n < max_files:
                rel = p.relative_to(src_dir)
                if _copy_file(p, dst_dir / rel):
                    n += 1
    return n


def _ade_package_dir() -> Path:
    return Path(__file__).resolve().parent


def _fill_cursor_hooks_from_bundled(ade_hooks: Path) -> int:
    """When the monorepo has no ``.cursor/hooks`` (public ASS-ADE), copy defaults from the wheel."""
    bundled = _ade_package_dir() / "cursor_hooks_bundled"
    if not bundled.is_dir():
        return 0
    n = 0
    for p in sorted(bundled.rglob("*"), key=lambda x: str(x)):
        if p.is_file():
            rel = p.relative_to(bundled)
            dst = ade_hooks / rel
            if not dst.is_file():
                if _copy_file(p, dst):
                    n += 1
    return n


def _copy_cross_ide_bundle(ade: Path) -> int:
    """Copy shipped ``cross-ide_bundled/`` (VS Code / Copilot / Codex) into ``.ade/cross-ide/``."""
    src = _ade_package_dir() / "cross_ide_bundled"
    if not src.is_dir():
        return 0
    dst = ade / "cross-ide"
    n = 0
    for f in sorted(src.rglob("*"), key=lambda p: str(p)):
        if f.is_file():
            rel = f.relative_to(src)
            if _copy_file(f, dst / rel):
                n += 1
    return n


def _merge_vscode_extension_recommendations(ws: Path) -> int:
    """Union Copilot + Python extension IDs into ``.vscode/extensions.json``."""
    ex = _ade_package_dir() / "cross_ide_bundled" / "extensions-recommendations.json"
    if not ex.is_file():
        return 0
    try:
        rec_data = json.loads(ex.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    recs = rec_data.get("recommendations")
    if not isinstance(recs, list) or not recs:
        return 0
    dst = ws / ".vscode" / "extensions.json"
    if dst.is_file():
        try:
            data = json.loads(dst.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
    else:
        data = {}
    have = {str(x) for x in (data.get("recommendations") or []) if str(x).strip()}
    for r in recs:
        if isinstance(r, str) and r.strip():
            have.add(r.strip())
    data["recommendations"] = sorted(have)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 1


def _write_ade_readme(ade: Path, source: Path, cursor_installed: bool) -> None:
    ch = f"`{ade / 'cursor-hooks'}`" + (
        f" and copied into `.cursor/hooks/`"
        if cursor_installed
        else f" (run `ass-ade-unified ade install-cursor` to push into `.cursor/hooks`)"
    )
    body = f"""# ADE / Atomadic operator stack (shipped with ASS-ADE)

**Materialized at:** `{_now()}` (UTC)  
**Source monorepo:** `{source.as_posix()}`  
**Layout version:** {ADE_LAYOUT_VERSION}

This tree mirrors the **Atomadic development** layout so you get the same
*prompt → product* workflow: swarm signal bus, scribe, persistent services,
and (optional) the strict ADE harness.

## What is here

| Subfolder | Role |
|----------|------|
| `cursor-hooks/` | Templates from monorepo `.cursor/hooks` — {ch} |
| `persistent/` | `run_swarm_services.py` + `swarm_services` (long-running automation) |
| `scripts/` | `regenerate_ass_ade_docs.py` and related terrain refresh |
| `ade-harness/` | `ade_hook_gate.py` for Cursor hook `additional_context` (optional) |
| `agents-core/` | Small agent docs slice (`INDEX`, protocol, ATO) — not the full 25-prompt set unless `--with-agents` was used at materialize time |
| `cross-ide/` | **Cursor vs VS Code (Copilot, Codex, MCP)** playbooks, MCP sample, optional Copilot instructions, VS Code **tasks** sample |

`swarm_signal.py` expects to live at **`<repo>/.cursor/hooks/swarm_signal.py`**
so `_REPO_ROOT` resolves to your workspace. Do **not** run hooks from inside
`./.ade/cursor-hooks` for daily work; install to `.cursor/hooks` or use
`ass-ade-unified ade install-cursor`.

## Cross-IDE (Cursor + VS Code)

See **`cross-ide/CURSOR-VS-CODE.md`** and **`cross-ide/CODEX-BUILD-CYCLE.md`**.  
VS Code does not run Cursor `hooks.json`; it uses **Copilot Agent mode**, **MCP** (see `vscode-mcp.example.json` → your `.vscode/mcp.json`), and the **OpenAI Codex** extension in the model/agent picker. Materialize may **merge** extension recommendations into `.vscode/extensions.json`.

## Commands

- Persistent services: `python .ade/persistent/run_swarm_services.py status` (from repo root)
- Terrain: `python .ade/scripts/regenerate_ass_ade_docs.py`
- Cursor bridges (dev): `python agents/sync_build_swarm_to_cursor.py` (run from this monorepo; ships in `scripts/` in `.ade/`)
- VS Code: **Run Task** → use `cross-ide/vscode-tasks.example.json` (merge into `.vscode/tasks.json`) for doctor / swarm / ade doctor
- **One-paste dev:** `SWARM-ONE-PROMPT.md` in this folder (if present in source) — same prompt for Cursor, Copilot, Codex; see **Host prep** inside that file

## ASS-ADE / CI

In CI, point `ATOMADIC_WORKSPACE` at the checkout. Hooks are optional; the
**golden assimilate** and import law remain the release gates
(`ASS_ADE_SHIP_PLAN` / `ass-ade-ship` workflow).
"""
    (ade / "README.md").write_text(body, encoding="utf-8", newline="\n")


def materialize_dotted_ade(
    workspace: Path,
    source: Path | None = None,
    *,
    with_agents: bool = False,
    install_cursor: bool = True,
    merge_vscode_recommendations: bool = True,
) -> MaterializeResult:
    """Copy the ADE operator slice into ``workspace / ".ade"`` and optionally ``.cursor/hooks``."""
    root = find_monorepo_root(source)
    if root is None:
        raise FileNotFoundError(
            "Could not find monorepo root (need agents/INDEX.md). Set ATOMADIC_WORKSPACE, "
            "ASS_ADE_MONOREPO, or run `ass-ade-unified ade materialize --source PATH` from "
            "a checkout of the ass-ade / Atomadic tree; PyPI sdist-only trees need that path."
        )

    ws = workspace.resolve()
    ade = ws / ".ade"
    ade.mkdir(parents=True, exist_ok=True)
    n = 0
    n += _copy_tree_selective(
        root / ".cursor" / "hooks",
        ade / "cursor-hooks",
        ("*.py", "*.md", "*.json", "*.ps1", "*.throttle.json"),
    )
    n += _fill_cursor_hooks_from_bundled(ade / "cursor-hooks")
    p_run = root / "scripts" / "run_swarm_services.py"
    p_pkg = root / "scripts" / "swarm_services"
    p_regen = root / "scripts" / "regenerate_ass_ade_docs.py"
    p_win = root / "scripts" / "windows" / "run_swarm_services_loop.ps1"
    for src, sub in (
        (p_run, "persistent"),
        (p_regen, "scripts"),
    ):
        if _copy_file(src, ade / sub / src.name):
            n += 1
    p_sync = root / "agents" / "sync_build_swarm_to_cursor.py"
    if p_sync.is_file() and _copy_file(p_sync, ade / "scripts" / p_sync.name):
        n += 1
    if p_pkg.is_dir():
        dst = ade / "persistent" / "swarm_services"
        for py in p_pkg.rglob("*.py"):
            rel = py.relative_to(p_pkg)
            if _copy_file(py, dst / rel):
                n += 1
    if p_win.is_file() and _copy_file(p_win, ade / "persistent" / p_win.name):
        n += 1
    h = root / "ADE" / "harness" / "ade_hook_gate.py"
    v = root / "ADE" / "harness" / "verify_ade_harness.py"
    for src in (h, v):
        if src.is_file() and _copy_file(src, ade / "ade-harness" / src.name):
            n += 1

    agent_dst = ade / "agents-core"
    for name in (
        "INDEX.md",
        "_PROTOCOL.md",
        "ASS_ADE_MONADIC_CODING.md",
        "NEXUS_SWARM_MCP.md",
        "ATO_DEV_ENVIRONMENT.md",
    ):
        p = root / "agents" / name
        if p.is_file() and _copy_file(p, agent_dst / name):
            n += 1
    if with_agents:
        n += _copy_tree_selective(root / "agents", agent_dst, ("*.md",), max_files=4000)

    n += _copy_cross_ide_bundle(ade)
    p_one = root / "SWARM-ONE-PROMPT.md"
    if p_one.is_file() and _copy_file(p_one, ade / "SWARM-ONE-PROMPT.md"):
        n += 1
    else:
        fb = _ade_package_dir() / "cross_ide_bundled" / "SWARM-ONE-PROMPT.md"
        if fb.is_file() and _copy_file(fb, ade / "SWARM-ONE-PROMPT.md"):
            n += 1
    if merge_vscode_recommendations:
        n += _merge_vscode_extension_recommendations(ws)

    layout: dict[str, Any] = {
        "ade_layout_version": ADE_LAYOUT_VERSION,
        "source_root": str(root),
        "workspace": str(ws),
        "created_utc": _now(),
        "with_agents": with_agents,
        "install_cursor": install_cursor,
    }
    (ade / "LAYOUT.json").write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8", newline="\n")
    _write_ade_readme(ade, root, install_cursor)  # after all .ade/ payloads (incl. cross-ide) exist

    cursor_ok = False
    if install_cursor:
        ch_src = ade / "cursor-hooks"
        ch_dst = ws / ".cursor" / "hooks"
        if ch_src.is_dir():
            ch_dst.mkdir(parents=True, exist_ok=True)
            for f in ch_src.iterdir():
                if f.is_file():
                    if _copy_file(f, ch_dst / f.name):
                        n += 1
            cursor_ok = (ch_dst / "swarm_signal.py").is_file()
        h_root = root / ".cursor" / "hooks.json"
        if h_root.is_file() and _copy_file(h_root, ws / ".cursor" / "hooks.json"):
            n += 1

    return MaterializeResult(
        ade_dir=ade,
        cursor_installed=cursor_ok,
        source_root=root,
        files_written=n,
    )

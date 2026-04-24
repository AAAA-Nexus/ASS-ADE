#!/usr/bin/env python3
"""
Path-agnostic regeneration of ASS-ADE terrain documents (repo-root suite).

Writes / updates:
  - ASS_ADE_INVENTORY.md + ASS_ADE_INVENTORY.paths.json  (full regen)
  - ASS_ADE_SUITE_SNAPSHOT.md                            (full regen, machine truth)
  - Bounded <!-- ASS_ADE_AUTOGEN:BEGIN --> ... END --> blocks in:
      ASS_ADE_MATRIX.md, ASS_ADE_SHIP_PLAN.md, ASS_ADE_GOAL_PIPELINE.md

Repo root is discovered by walking parents from --root, $PWD, and this script's
directory until `agents/INDEX.md` exists (Atomadic / ASS-ADE swarm layout).

Usage:
  python scripts/regenerate_ass_ade_docs.py
  python scripts/regenerate_ass_ade_docs.py --root /path/to/atomadic
  python scripts/regenerate_ass_ade_docs.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib  # py3.11+
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

AUTOGEN_BEGIN = "<!-- ASS_ADE_AUTOGEN:BEGIN -->"
AUTOGEN_END = "<!-- ASS_ADE_AUTOGEN:END -->"

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".venv",
        "venv",
        ".tox",
        "dist",
        "build",
        ".mypy_cache",
        ".ruff_cache",
        ".eggs",
        "eggs",
        ".cursor",
    }
)


def _is_skipped_dir(name: str) -> bool:
    if name in SKIP_DIR_NAMES:
        return True
    if name.endswith(".egg-info"):
        return True
    return False


def discover_repo_root(explicit: Path | None, start_paths: Iterable[Path]) -> Path:
    markers = ("agents" / Path("INDEX.md"),)
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit.resolve())
    candidates.extend(p.resolve() for p in start_paths)

    for start in candidates:
        cur = start if start.is_dir() else start.parent
        for _ in range(40):
            if all((cur / m).is_file() for m in markers):
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent

    raise SystemExit(
        "Could not find repo root (missing agents/INDEX.md). "
        "Run from the Atomadic repo or pass --root <path>."
    )


def git_short_head(repo: Path) -> str:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


def read_pyproject_project(path: Path) -> dict[str, Any] | None:
    if tomllib is None:
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    proj = data.get("project")
    if not isinstance(proj, dict):
        return None
    return {
        "name": proj.get("name"),
        "version": proj.get("version"),
        "readme": proj.get("readme"),
    }


def path_is_ephemeral(p: Path) -> bool:
    s = p.as_posix().lower()
    if ".pytest_tmp" in s:
        return True
    if "rebuild-outputs" in s:
        return True
    if "-backup-" in p.name.lower():
        return True
    return False


@dataclass
class ScanResult:
    ass_ade_dirs: list[Path] = field(default_factory=list)
    tier_maps: list[Path] = field(default_factory=list)
    pyprojects_ass_roots: list[Path] = field(default_factory=list)
    tier_map_roots_extra: list[Path] = field(default_factory=list)

    def all_hits_json(self, repo_root: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for d in self.ass_ade_dirs:
            rows.append({"path": str(d.resolve()), "kind": "dir_ass_ade_star"})
        for t in self.tier_maps:
            rel = "tier_map_ephemeral" if path_is_ephemeral(t) else "tier_map_workspace"
            rows.append({"path": str(t.resolve()), "kind": rel})
        for py in self.pyprojects_ass_roots:
            kind = "pyproject"
            if py.resolve() == (repo_root / "pyproject.toml").resolve():
                kind = "pyproject_root_spine"
            rows.append({"path": str(py.resolve()), "kind": kind})
        v11 = repo_root / "ass-ade-v1.1" / "pyproject.toml"
        if v11.is_file():
            rows.append({"path": str(v11.resolve()), "kind": "pyproject_v11_pointer"})
        return rows


def scan_repo(repo_root: Path) -> ScanResult:
    out = ScanResult()
    for child in sorted(repo_root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        if child.name.startswith("ass-ade"):
            out.ass_ade_dirs.append(child)
            pp = child / "pyproject.toml"
            if pp.is_file():
                out.pyprojects_ass_roots.append(pp)
        tm = child / ".ass-ade" / "tier-map.json"
        if tm.is_file() and not child.name.startswith("ass-ade"):
            out.tier_map_roots_extra.append(child)

    tier_maps: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(repo_root, topdown=True):
        dp = Path(dirpath)
        # prune
        dirnames[:] = [d for d in dirnames if not _is_skipped_dir(d)]
        if "tier-map.json" in filenames:
            tier_maps.append(dp / "tier-map.json")
    out.tier_maps = sorted(set(tier_maps), key=lambda p: str(p).lower())

    root_py = repo_root / "pyproject.toml"
    if root_py.is_file() and root_py not in out.pyprojects_ass_roots:
        out.pyprojects_ass_roots.append(root_py)

    return out


def spine_assessment(repo_root: Path, scan: ScanResult) -> dict[str, Any]:
    root_py = repo_root / "pyproject.toml"
    v11_src = repo_root / "ass-ade-v1.1" / "src" / "ass_ade_v11"
    v11_ptr = repo_root / "ass-ade-v1.1" / "pyproject.toml"
    info = read_pyproject_project(root_py) if root_py.is_file() else None
    name = (info or {}).get("name")
    return {
        "root_pyproject_exists": root_py.is_file(),
        "root_project_name": name,
        "ass_ade_v11_package_dir_exists": v11_src.is_dir(),
        "v11_pointer_pyproject_exists": v11_ptr.is_file(),
        "ass_ade_sibling_trees": [p.name for p in scan.ass_ade_dirs],
        "default_spine_for_new_work": (
            "ass_ade_v11 under ass-ade-v1.1/src/ (T12 root pyproject)"
            if v11_src.is_dir() and name == "ass-ade-v1-1"
            else "Resolve manually — T12 spine markers incomplete for this checkout."
        ),
    }


def render_inventory_md(repo_root: Path, scan: ScanResult) -> str:
    lines: list[str] = []
    lines.append("# ASS-ADE inventory (auto-generated)")
    lines.append("")
    lines.append(
        "Fingerprint scan: immediate `ass-ade*` children of repo root, "
        "all `tier-map.json` under the repo (skipping common cache dirs), "
        "and `pyproject.toml` next to those trees + repo root."
    )
    lines.append("")
    lines.append("**Regenerate:** `python scripts/regenerate_ass_ade_docs.py` (path-agnostic) or `scripts/inventory_ass_ade.ps1` (Windows-wide scan).")
    lines.append("")
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")
    lines.append("## Directory roots (`ass-ade*`)")
    lines.append("")
    for d in sorted(scan.ass_ade_dirs, key=lambda p: p.name.lower()):
        lines.append(f"- `{d.resolve().as_posix()}`")
    if not scan.ass_ade_dirs:
        lines.append("- _(none — check repo root)_")
    lines.append("")
    lines.append("## Other repo roots with `.ass-ade/tier-map.json`")
    lines.append("")
    for d in sorted(scan.tier_map_roots_extra, key=lambda p: p.name.lower()):
        lines.append(f"- `{d.resolve().as_posix()}`")
    if not scan.tier_map_roots_extra:
        lines.append("- _(none)_")
    lines.append("")
    lines.append("## tier-map.json hits")
    lines.append("")
    ephemeral = [p for p in scan.tier_maps if path_is_ephemeral(p)]
    stable = [p for p in scan.tier_maps if not path_is_ephemeral(p)]
    for label, bucket in (
        ("Stable / product", stable),
        ("Ephemeral / tmp (do not treat as product truth)", ephemeral),
    ):
        lines.append(f"### {label}")
        lines.append("")
        if not bucket:
            lines.append("- _(none)_")
        else:
            for t in sorted(bucket, key=lambda p: str(p).lower()):
                lines.append(f"- `{t.resolve().as_posix()}`")
        lines.append("")
    lines.append("## pyproject.toml (spine + ass-ade roots)")
    lines.append("")
    for p in sorted(set(scan.pyprojects_ass_roots), key=lambda p: str(p).lower()):
        try:
            rel = p.relative_to(repo_root).as_posix()
        except ValueError:
            rel = p.as_posix()
        note = ""
        if p.name == "pyproject.toml" and p.parent == repo_root:
            note = " — canonical `pip install -e .` / `ass-ade-unified` when T12"
        lines.append(f"- `{p.resolve().as_posix()}` (`{rel}`){note}")
    lines.append("")
    lines.append("## v1.1 pointer stub (no `[project]` in-tree)")
    lines.append("")
    lines.append(
        "- `ass-ade-v1.1/pyproject.toml` (relative to repo root) — T12 pointer only when root `[project]` is canonical."
    )
    v11 = repo_root / "ass-ade-v1.1" / "pyproject.toml"
    if v11.is_file():
        lines.append(f"- Resolved: `{v11.resolve().as_posix()}`")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_suite_snapshot(
    repo_root: Path, scan: ScanResult, spine: dict[str, Any]
) -> str:
    iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    root_git = git_short_head(repo_root)
    lines: list[str] = []
    lines.append("# ASS-ADE suite snapshot (auto-generated)")
    lines.append("")
    lines.append("**Do not hand-edit.** Regenerate with `python scripts/regenerate_ass_ade_docs.py`.")
    lines.append("")
    lines.append(f"- **UTC time:** {iso}")
    lines.append(f"- **Repo root:** `{repo_root.resolve().as_posix()}`")
    lines.append(f"- **Host:** `{os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME', '')}`")
    lines.append(f"- **Python:** `{sys.version.split()[0]}`")
    lines.append(f"- **Git (repo root):** `{root_git or '—'}`")
    lines.append("")
    lines.append("## Spine signals (T12)")
    lines.append("")
    for k, v in spine.items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    lines.append("## `ass-ade*` directories (repo root children)")
    lines.append("")
    for d in sorted(scan.ass_ade_dirs, key=lambda p: p.name.lower()):
        g = git_short_head(d)
        tm = (d / ".ass-ade" / "tier-map.json").is_file()
        pp = d / "pyproject.toml"
        pinfo = read_pyproject_project(pp) if pp.is_file() else None
        ver = pinfo.get("version") if pinfo else "—"
        name = pinfo.get("name") if pinfo else "—"
        lines.append(f"### `{d.name}`")
        lines.append("")
        lines.append(f"- Path: `{d.resolve().as_posix()}`")
        lines.append(f"- `tier-map.json`: {'yes' if tm else 'no'}")
        lines.append(f"- `[project]` name/version: `{name}` / `{ver}`")
        lines.append(f"- Git short: `{g or '—'}`")
        lines.append("")
    lines.append("## Hygiene hints (for cleanup passes)")
    lines.append("")
    lines.append(
        "- Prefer **one** editable install story from root `pyproject.toml` (see `agents/ATO_DEV_ENVIRONMENT.md`)."
    )
    lines.append(
        "- Tier-maps under `.pytest_tmp`, dated `*-backup-*`, or `rebuild-outputs` are **ephemeral** — archive or delete per `ASS_ADE_SHIP_PLAN.md` Phase 0."
    )
    lines.append(
        "- After moving trees, re-run this script and commit `ASS_ADE_INVENTORY.md`, `ASS_ADE_INVENTORY.paths.json`, and `ASS_ADE_SUITE_SNAPSHOT.md` together."
    )
    lines.append("")
    lines.append("## Related operator docs")
    lines.append("")
    lines.append("- [`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md)")
    lines.append("- [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md)")
    lines.append("- [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md)")
    lines.append("- [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md)")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_autogen_inner(repo_root: Path, scan: ScanResult, spine: dict[str, Any]) -> str:
    iso = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    root_git = git_short_head(repo_root)
    n_ass = len(scan.ass_ade_dirs)
    n_tm = len(scan.tier_maps)
    n_e = sum(1 for p in scan.tier_maps if path_is_ephemeral(p))
    lines = [
        f"_Terrain refresh: **{iso}** — [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md) has the full machine snapshot._",
        "",
        f"- **Repo root:** `{repo_root.resolve().as_posix()}`",
        f"- **Umbrella git (short):** `{root_git or '—'}`",
        f"- **`ass-ade*` dirs at root:** {n_ass}",
        f"- **`tier-map.json` files:** {n_tm} ({n_e} ephemeral / under tmp or backup paths)",
        f"- **Spine hint:** {spine.get('default_spine_for_new_work', '')}",
        "",
        "**Subtrees (name → git short):**",
        "",
    ]
    for d in sorted(scan.ass_ade_dirs, key=lambda p: p.name.lower()):
        g = git_short_head(d)
        lines.append(f"- `{d.name}` → `{g or '—'}`")
    if scan.tier_map_roots_extra:
        lines.append("")
        lines.append("**Other tier-mapped repo-root siblings:**")
        for d in sorted(scan.tier_map_roots_extra, key=lambda p: p.name.lower()):
            g = git_short_head(d)
            lines.append(f"- `{d.name}` → `{g or '—'}`")
    lines.append("")
    return "\n".join(lines)


def splice_autogen_block(content: str, inner_md: str, *, insert_before: str) -> str:
    """Replace existing autogen block, or insert a new block before `insert_before` heading."""
    block = (
        f"\n## Live terrain (auto-generated)\n\n{AUTOGEN_BEGIN}\n{inner_md}\n{AUTOGEN_END}\n\n"
    )
    if AUTOGEN_BEGIN in content and AUTOGEN_END in content:
        pattern = re.compile(
            re.escape(AUTOGEN_BEGIN) + r"[\s\S]*?" + re.escape(AUTOGEN_END),
            re.MULTILINE,
        )
        new_content, n = pattern.subn(f"{AUTOGEN_BEGIN}\n{inner_md}\n{AUTOGEN_END}", content, count=1)
        if n:
            return new_content
    if insert_before in content:
        return content.replace(insert_before, block + insert_before, 1)
    return content + block


def write_if_changed(path: Path, text: str, dry_run: bool) -> bool:
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == text:
        print(f"  unchanged: {path.name}")
        return False
    print(f"  write: {path.name} ({len(text)} bytes)")
    if not dry_run:
        path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    if tomllib is None:
        print(
            "Warning: tomllib unavailable (need Python 3.11+); pyproject name/version "
            "will be omitted in snapshot tables.",
            file=sys.stderr,
        )

    ap = argparse.ArgumentParser(description="Regenerate ASS_ADE* terrain docs.")
    ap.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repo root (must contain agents/INDEX.md). Default: discover from cwd / script.",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print actions without writing files.")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    starts = [Path.cwd(), script_dir.parent, script_dir]
    try:
        repo = discover_repo_root(args.root, starts)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 1

    scan = scan_repo(repo)
    spine = spine_assessment(repo, scan)
    hits = scan.all_hits_json(repo)

    inner = render_autogen_inner(repo, scan, spine)
    inv_md = render_inventory_md(repo, scan)
    snap_md = render_suite_snapshot(repo, scan, spine)
    inv_json = json.dumps(hits, indent=2, sort_keys=True) + "\n"

    print(f"Repo root: {repo}")
    print(f"Hits: {len(hits)} (dirs ass-ade*: {len(scan.ass_ade_dirs)}, tier-maps: {len(scan.tier_maps)})")
    if args.dry_run:
        print("Dry run — no files written.")

    changed = 0
    changed += write_if_changed(repo / "ASS_ADE_INVENTORY.md", inv_md, args.dry_run)
    changed += write_if_changed(repo / "ASS_ADE_INVENTORY.paths.json", inv_json, args.dry_run)
    changed += write_if_changed(repo / "ASS_ADE_SUITE_SNAPSHOT.md", snap_md, args.dry_run)

    matrix_path = repo / "ASS_ADE_MATRIX.md"
    if matrix_path.is_file():
        m = matrix_path.read_text(encoding="utf-8")
        m2 = splice_autogen_block(m, inner, insert_before="## Interpretation")
        changed += write_if_changed(matrix_path, m2, args.dry_run)

    ship_path = repo / "ASS_ADE_SHIP_PLAN.md"
    if ship_path.is_file():
        s = ship_path.read_text(encoding="utf-8")
        s2 = splice_autogen_block(s, inner, insert_before="## Phase 0")
        changed += write_if_changed(ship_path, s2, args.dry_run)

    goal_path = repo / "ASS_ADE_GOAL_PIPELINE.md"
    if goal_path.is_file():
        g = goal_path.read_text(encoding="utf-8")
        g2 = splice_autogen_block(g, inner, insert_before="## Track P")
        changed += write_if_changed(goal_path, g2, args.dry_run)

    print(f"Done. Files touched or refreshed: {changed if not args.dry_run else '(dry-run)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

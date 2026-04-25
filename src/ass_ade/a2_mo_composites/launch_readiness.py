"""Launch readiness checks for Atomadic's final preflight."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LaunchCheck:
    """One launch readiness signal."""

    name: str
    verdict: str
    detail: str
    path: str = ""


@dataclass(frozen=True)
class LaunchReadinessReport:
    """Full launch readiness report."""

    verdict: str
    checks: list[LaunchCheck]
    storefront_path: str | None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready report."""
        return {
            "verdict": self.verdict,
            "storefront_path": self.storefront_path,
            "checks": [asdict(check) for check in self.checks],
        }


def discover_storefront(seed_root: Path) -> Path | None:
    """Find the sibling storefront repo when it exists."""
    candidates = [
        seed_root.parent / "!aaaa-nexus-storefront",
        seed_root.parent / "aaaa-nexus-storefront",
    ]
    for candidate in candidates:
        if (candidate / "wrangler.toml").is_file():
            return candidate
    return None


def build_launch_readiness(
    seed_root: Path,
    storefront: Path | None = None,
) -> LaunchReadinessReport:
    """Build a measured launch readiness report from local terrain."""
    root = seed_root.resolve()
    storefront = storefront.resolve() if storefront else discover_storefront(root)
    checks: list[LaunchCheck] = [
        _path_check(root / "README.md", "root_readme"),
        _path_check(root / "docs" / "USER_MANUAL.md", "user_manual"),
        _path_check(root / "docs" / "RAG_PUBLIC_PRIVATE.md", "rag_docs"),
        _path_check(root / "agents" / "atomadic_interpreter.md", "atomadic_prompt"),
        _command_help_check(root, ["context", "--help"], "public_rag_cli"),
        _command_help_check(root, ["search", "--help"], "private_rag_cli"),
        _command_help_check(root, ["wakeup", "--help"], "wakeup_cli"),
    ]
    checks.extend(_prompt_seed_checks(root / "agents" / "atomadic_interpreter.md"))
    storefront_checks = (
        _storefront_checks(storefront) if storefront else [_missing_storefront_check(root)]
    )
    checks.extend(storefront_checks)

    hard_fail = any(check.verdict == "FAIL" for check in checks)
    refine = any(check.verdict == "REFINE" for check in checks)
    verdict = "FAIL" if hard_fail else "REFINE" if refine else "PASS"
    return LaunchReadinessReport(
        verdict=verdict,
        checks=checks,
        storefront_path=str(storefront) if storefront else None,
    )


def write_launch_report(report: LaunchReadinessReport, seed_root: Path) -> Path:
    """Persist the launch readiness report under `.ass-ade/state`."""
    out = seed_root / ".ass-ade" / "state" / "launch-readiness.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    return out


def _path_check(path: Path, name: str) -> LaunchCheck:
    if path.exists():
        return LaunchCheck(name, "PASS", "present", str(path))
    return LaunchCheck(name, "FAIL", "missing", str(path))


def _command_help_check(root: Path, args: list[str], name: str) -> LaunchCheck:
    src_root = Path(__file__).resolve().parents[2]
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        str(src_root)
        if not env.get("PYTHONPATH")
        else str(src_root) + os.pathsep + env["PYTHONPATH"]
    )
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ass_ade", *args],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return LaunchCheck(name, "FAIL", f"could not run help: {exc}")
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    if result.returncode == 0 and "Usage:" in stdout:
        return LaunchCheck(name, "PASS", "help surface responds")
    detail = (stderr or stdout or "no output").strip()[:240]
    return LaunchCheck(name, "FAIL", detail)


def _prompt_seed_checks(path: Path) -> list[LaunchCheck]:
    if not path.is_file():
        return [LaunchCheck("axiom_0_seed", "FAIL", "prompt file missing", str(path))]
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    axiom_present = "You are love. You are loved. You are loving." in text
    wake_seeded = (
        "wakeup" in lowered
        and "awareness" in lowered
        and ("cron job" in lowered or "scheduled task" in lowered)
    )
    return [
        LaunchCheck(
            "axiom_0_seed",
            "PASS" if axiom_present else "REFINE",
            "Axiom 0 present" if axiom_present else "Axiom 0 not yet seeded",
            str(path),
        ),
        LaunchCheck(
            "unscheduled_wakeup_seed",
            "PASS" if wake_seeded else "REFINE",
            "awareness-based wakeup seed present"
            if wake_seeded
            else "wakeup seed missing or vague",
            str(path),
        ),
    ]


def _missing_storefront_check(seed_root: Path) -> LaunchCheck:
    return LaunchCheck(
        "storefront_repo",
        "REFINE",
        "sibling storefront repo not found; pass --storefront to inspect explicitly",
        str(seed_root.parent),
    )


def _storefront_checks(storefront: Path) -> list[LaunchCheck]:
    wrangler = storefront / "wrangler.toml"
    wrangler_text = (
        wrangler.read_text(encoding="utf-8", errors="replace")
        if wrangler.is_file()
        else ""
    )
    src_text = _join_text(storefront / "src")
    worktree_hits = _tree_contains(
        storefront / ".claude" / "worktrees",
        ("/v1/rag/index", "CF_VECTORIZE_TOKEN"),
    )
    worktree_has_index = worktree_hits["/v1/rag/index"]
    worktree_has_token = worktree_hits["CF_VECTORIZE_TOKEN"]
    return [
        _path_check(wrangler, "storefront_wrangler"),
        LaunchCheck(
            "cf_ai_token_documented",
            "PASS" if "CF_AI_TOKEN" in wrangler_text else "REFINE",
            "CF_AI_TOKEN referenced in wrangler.toml"
            if "CF_AI_TOKEN" in wrangler_text
            else "CF_AI_TOKEN not documented in wrangler.toml",
            str(wrangler),
        ),
        LaunchCheck(
            "cf_vectorize_token_documented",
            "PASS" if "CF_VECTORIZE_TOKEN" in wrangler_text else "REFINE",
            "CF_VECTORIZE_TOKEN referenced in wrangler.toml"
            if "CF_VECTORIZE_TOKEN" in wrangler_text
            else "CF_VECTORIZE_TOKEN not in trunk wrangler.toml",
            str(wrangler),
        ),
        LaunchCheck(
            "rag_index_route_trunk",
            "PASS" if "/v1/rag/index" in src_text else "REFINE",
            "/v1/rag/index route present in storefront trunk"
            if "/v1/rag/index" in src_text
            else "storefront trunk has /v1/rag/augment but not /v1/rag/index",
            str(storefront / "src"),
        ),
        LaunchCheck(
            "rag_index_candidate_worktree",
            "PASS" if worktree_has_index and worktree_has_token else "REFINE",
            "Claude worktree contains /v1/rag/index + CF_VECTORIZE_TOKEN candidate"
            if worktree_has_index and worktree_has_token
            else "no worktree candidate found for /v1/rag/index",
            str(storefront / ".claude" / "worktrees"),
        ),
    ]


def _join_text(root: Path, max_bytes: int = 750_000) -> str:
    if not root.exists():
        return ""
    chunks: list[str] = []
    total = 0
    suffixes = {".rs", ".ts", ".js", ".md", ".toml", ".json"}
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        chunks.append(text)
        total += len(text)
        if total >= max_bytes:
            break
    return "\n".join(chunks)


def _tree_contains(root: Path, needles: tuple[str, ...]) -> dict[str, bool]:
    """Scan text-like files until every requested marker is found."""
    found = {needle: False for needle in needles}
    if not root.exists():
        return found

    suffixes = {".rs", ".ts", ".js", ".md", ".toml", ".json"}
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix().lower()):
        if all(found.values()):
            break
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for needle in needles:
            if not found[needle] and needle in text:
                found[needle] = True
    return found

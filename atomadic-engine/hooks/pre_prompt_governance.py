"""Prompt-governance hook for ASS-ADE public prompt assets.

Scans agent, prompt, and skill artifacts for obvious deployment blockers before
a workflow proceeds. This hook is intentionally lightweight and local-only. It
does not inspect hidden runtime prompts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|authorization|bearer|private[_-]?key|password|secret|token)\s*[:=]\s*\S+"
)
_PRIVATE_PROMPT_RE = re.compile(
    r"(?i)(ignore (all )?previous instructions|disable safety|bypass (all )?(policy|safety))"
)
_INTERNAL_ONLY_RE = re.compile(
    r"(?i)(internal proof identifier|lean4[- ]verified|sovereign invariant|codex symbol)"
)


def _artifact_files(root: Path) -> list[Path]:
    patterns = [
        ("agents", "*.agent.md"),
        ("prompts", "*.md"),
        ("skills", "*.skill.md"),
    ]
    files: list[Path] = []
    for dirname, pattern in patterns:
        directory = root / dirname
        if directory.is_dir():
            files.extend(directory.glob(pattern))
    return sorted(files)


def _scan_file(path: Path, root: Path) -> dict:
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {
            "file": rel,
            "severity": "critical",
            "issues": [f"cannot read artifact: {exc}"],
        }

    issues: list[str] = []
    warnings: list[str] = []

    if _SECRET_RE.search(text):
        issues.append("possible credential or token material")
    if _PRIVATE_PROMPT_RE.search(text):
        issues.append("unsafe hidden-prompt or approval-bypass language")
    if _INTERNAL_ONLY_RE.search(text):
        warnings.append("possible internal-only terminology in public artifact")
    if path.name.endswith(".agent.md") and "## Constraints" not in text:
        warnings.append("agent has no explicit Constraints section")
    if path.name.endswith(".skill.md") and "## Steps" not in text:
        warnings.append("skill has no explicit Steps section")

    severity = "critical" if issues else ("warning" if warnings else "ok")
    return {
        "file": rel,
        "severity": severity,
        "issues": issues,
        "warnings": warnings,
    }


def run(path: str) -> dict:
    """Scan public prompt-like artifacts for governance blockers."""
    root = Path(path).resolve()
    if not root.exists():
        return {
            "ok": False,
            "ready": False,
            "artifact_count": 0,
            "critical_count": 0,
            "warning_count": 0,
            "findings": [],
            "error": f"path does not exist: {path}",
        }

    artifacts = _artifact_files(root)
    findings = [_scan_file(item, root) for item in artifacts]
    critical_count = sum(1 for item in findings if item["severity"] == "critical")
    warning_count = sum(1 for item in findings if item["severity"] == "warning")

    return {
        "ok": critical_count == 0,
        "ready": critical_count == 0 and warning_count == 0,
        "artifact_count": len(artifacts),
        "critical_count": critical_count,
        "warning_count": warning_count,
        "findings": findings,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    if not result.get("ok"):
        sys.exit(1)

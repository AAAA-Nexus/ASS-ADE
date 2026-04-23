#!/usr/bin/env python3
"""Ship readiness audit — CI-equivalent gates + CLI smoke (no secrets on stdout).

Run from repository root:
  python scripts/ship_readiness_audit.py

Optional:
  SHIP_AUDIT_JSON=path   write machine-readable summary JSON
  SHIP_SKIP_CHAT=1       skip studio chat REPL smoke (first line ``exit``)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from shutil import which


def _run(
    label: str,
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int = 600,
    stdin: str | None = None,
) -> dict[str, object]:
    t0 = time.perf_counter()
    r = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        input=stdin,
    )
    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    return {
        "step": label,
        "argv": argv,
        "returncode": r.returncode,
        "elapsed_ms": elapsed_ms,
        "stdout_tail": (r.stdout or "")[-4000:],
        "stderr_tail": (r.stderr or "")[-4000:],
    }


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    return here.parents[1]


def main() -> int:
    root = _repo_root()
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONPATH", "")
    audit_tmp = Path(tempfile.mkdtemp(prefix="ass-ade-audit-"))
    steps: list[dict[str, object]] = []
    warnings: list[str] = []

    git_dir = root / ".git"
    steps.append(
        {
            "step": "git_root",
            "ok": git_dir.is_dir(),
            "blocking": False,
            "detail": "present" if git_dir.is_dir() else "missing — git push/PR flow needs a repo root",
        }
    )
    if not git_dir.is_dir():
        warnings.append("git_root_missing")

    gh = which("gh")
    if gh:
        r = _run("gh_auth_status", [gh, "auth", "status"], cwd=root, env=env, timeout=30)
        steps.append(r)
        if r["returncode"] != 0:  # type: ignore[comparison-overlap]
            warnings.append("gh_not_authenticated")
    else:
        steps.append({"step": "gh_auth_status", "skipped": True, "reason": "gh CLI not on PATH"})

    py = sys.executable
    uni = which("ass-ade-unified")
    v11 = which("ass-ade-v11")

    if uni:
        steps.append(_run("doctor", [uni, "doctor"], cwd=root, env=env, timeout=60))
    else:
        steps.append(
            _run(
                "doctor",
                [py, "-m", "ass_ade_v11.a4_sy_orchestration.unified_cli", "doctor"],
                cwd=root,
                env=env,
                timeout=60,
            )
        )

    li = which("lint-imports")
    if li:
        steps.append(_run("lint_imports", [li], cwd=root, env=env, timeout=120))
    else:
        steps.append({"step": "lint_imports", "skipped": True, "reason": "lint-imports not on PATH"})
        warnings.append("lint_imports_cli_missing")

    steps.append(
        _run(
            "pytest_not_dogfood",
            [
                py,
                "-m",
                "pytest",
                "ass-ade-v1.1/tests",
                "-m",
                "not dogfood",
                "-q",
                "--tb=no",
                "--basetemp",
                str(audit_tmp / "pytest-temp"),
            ],
            cwd=root,
            env=env,
            timeout=900,
        )
    )

    if v11:
        steps.append(
            _run(
                "synth_tests_check",
                [v11, "synth-tests", "--check", "--repo", "ass-ade-v1.1"],
                cwd=root,
                env=env,
                timeout=300,
            )
        )
    else:
        steps.append(
            _run(
                "synth_tests_check",
                [py, "-m", "ass_ade_v11.a4_sy_orchestration.cli", "synth-tests", "--check", "--repo", "ass-ade-v1.1"],
                cwd=root,
                env=env,
                timeout=300,
            )
        )

    out = audit_tmp / "golden"
    out.mkdir(parents=True, exist_ok=True)
    book = out / "book.json"
    plan = out / "ASSIMILATE_PLAN.json"
    uni_cmd = uni or which("ass-ade-unified")
    if uni_cmd:
        steps.append(
            _run(
                "golden_assimilate_gapfill",
                [
                    str(uni_cmd),
                    "assimilate",
                    str(root / "ass-ade-v1.1" / "tests" / "fixtures" / "minimal_pkg"),
                    str(out),
                    "--stop-after",
                    "gapfill",
                    "--json-out",
                    str(book),
                    "--plan-out",
                    str(plan),
                ],
                cwd=root,
                env=env,
                timeout=600,
            )
        )
    else:
        steps.append({"step": "golden_assimilate_gapfill", "skipped": True, "reason": "ass-ade-unified not on PATH"})
        warnings.append("golden_assimilate_skipped")

    if os.environ.get("SHIP_SKIP_CHAT") == "1":
        steps.append({"step": "studio_chat_smoke", "skipped": True, "reason": "SHIP_SKIP_CHAT=1"})
    elif not uni_cmd:
        steps.append({"step": "studio_chat_smoke", "skipped": True, "reason": "ass-ade-unified not on PATH"})
    else:
        try:
            import ass_ade  # noqa: F401
        except ImportError:
            steps.append({"step": "studio_chat_smoke", "skipped": True, "reason": "ass_ade (v1) not importable"})
        else:
            with tempfile.TemporaryDirectory() as tdh:
                fake_home = Path(tdh)
                mem = fake_home / ".ass-ade" / "memory"
                mem.mkdir(parents=True)
                (mem / "user_profile.json").write_text(
                    json.dumps({"name": "readiness-audit", "dominant_tone": "technical"}),
                    encoding="utf-8",
                )
                cenv = env.copy()
                cenv["USERPROFILE"] = str(fake_home)
                cenv["HOME"] = str(fake_home)
                steps.append(
                    _run(
                        "studio_chat_smoke",
                        [str(uni_cmd), "studio", "chat", "--dir", str(root)],
                        cwd=root,
                        env=cenv,
                        timeout=90,
                        stdin="exit\n",
                    )
                )

    ok = True
    for s in steps:
        if not isinstance(s, dict):
            continue
        if s.get("skipped"):
            continue
        if s.get("returncode") is not None and s["returncode"] != 0:
            ok = False
        if s.get("blocking") is True and s.get("ok") is False:
            ok = False

    summary = {
        "ok": ok,
        "warnings": warnings,
        "repo_root": str(root),
        "steps": steps,
    }
    out_path = os.environ.get("SHIP_AUDIT_JSON")
    if out_path:
        Path(out_path).write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"ok": ok, "warnings": warnings, "step_names": [s.get("step", "?") for s in steps]}, indent=2))
    if not ok:
        print("--- failing step tails (stderr) ---", file=sys.stderr)
        for s in steps:
            if isinstance(s, dict) and s.get("returncode") not in (None, 0) and not s.get("skipped"):
                print(s.get("step"), file=sys.stderr)
                print(s.get("stderr_tail", ""), file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

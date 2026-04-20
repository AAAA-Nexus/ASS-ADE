"""Tool wrapper: find and apply enhancements via ass-ade enhance."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def scan(
    path: str,
    local_only: bool = False,
    min_severity: str = "info",
    timeout: int = 120,
) -> dict:
    """Scan a codebase for enhancement opportunities.

    Args:
        path: Absolute or relative path to the codebase.
        local_only: Skip AAAA-Nexus enrichment; use local analysis only.
        min_severity: Minimum severity level to report (info/low/medium/high/critical).
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
            findings (list[dict] | None): Parsed findings list when ok=True.
    """
    cmd = [
        sys.executable, "-m", "ass_ade", "enhance", "scan", path,
        "--json",
        "--min-severity", min_severity,
    ]
    if local_only:
        cmd.append("--local-only")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "exit_code": 124,
            "stdout": "",
            "stderr": f"enhance scan timed out after {timeout}s",
            "findings": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "findings": None,
        }

    findings = None
    if result.returncode == 0 and result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
            findings = parsed if isinstance(parsed, list) else parsed.get("findings")
        except json.JSONDecodeError:
            pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "findings": findings,
    }


def apply(
    path: str,
    finding_id: str,
    dry_run: bool = False,
    timeout: int = 120,
) -> dict:
    """Apply a specific enhancement finding to a codebase.

    Args:
        path: Absolute or relative path to the codebase.
        finding_id: The finding ID from a prior scan (e.g. "enh-0042").
        dry_run: Show what would change without writing any files.
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
    """
    cmd = [
        sys.executable, "-m", "ass_ade", "enhance", "apply", path,
        "--finding", finding_id,
    ]
    if dry_run:
        cmd.append("--dry-run")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "exit_code": 124,
            "stdout": "",
            "stderr": f"enhance apply timed out after {timeout}s",
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
        }

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":
    # Usage: enhance_tool.py scan <path>
    #        enhance_tool.py apply <path> <finding-id>
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {
                    "ok": False,
                    "exit_code": 1,
                    "stderr": "Usage: enhance_tool.py <scan|apply> <path> [finding-id]",
                },
                indent=2,
            )
        )
        sys.exit(1)

    action = sys.argv[1]
    target = sys.argv[2]

    if action == "scan":
        print(json.dumps(scan(target), indent=2))
    elif action == "apply":
        if len(sys.argv) < 4:
            print(json.dumps({"ok": False, "exit_code": 1, "stderr": "finding-id required"}, indent=2))
            sys.exit(1)
        fid = sys.argv[3]
        print(json.dumps(apply(target, fid), indent=2))
    else:
        print(json.dumps({"ok": False, "exit_code": 1, "stderr": f"unknown action: {action}"}, indent=2))
        sys.exit(1)

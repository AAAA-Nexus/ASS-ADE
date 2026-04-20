"""Tool wrapper: prompt artifact governance via ass-ade prompt commands."""
from __future__ import annotations

import json
import subprocess
import sys
from typing import Any


def _run(cmd: list[str], timeout: int) -> dict[str, Any]:
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
            "stderr": f"prompt command timed out after {timeout}s",
            "data": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "data": None,
        }

    data: Any = None
    if result.stdout.strip():
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            data = None

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "data": data,
    }


def hash_prompt(path: str, repo_path: str = ".", timeout: int = 60) -> dict[str, Any]:
    """Return SHA-256 metadata for a prompt artifact."""
    return _run(
        [sys.executable, "-m", "ass_ade", "prompt", "hash", path, "--path", repo_path, "--json"],
        timeout,
    )


def validate(
    manifest_path: str,
    prompt_path: str,
    repo_path: str = ".",
    prompt_name: str | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Validate a prompt artifact against a JSON manifest."""
    cmd = [
        sys.executable,
        "-m",
        "ass_ade",
        "prompt",
        "validate",
        manifest_path,
        "--prompt-path",
        prompt_path,
        "--path",
        repo_path,
        "--json",
    ]
    if prompt_name:
        cmd.extend(["--prompt-name", prompt_name])
    return _run(cmd, timeout)


def section(
    section_name: str,
    prompt_path: str,
    repo_path: str = ".",
    timeout: int = 60,
) -> dict[str, Any]:
    """Extract a Markdown heading or XML tag section from a prompt artifact."""
    return _run(
        [
            sys.executable,
            "-m",
            "ass_ade",
            "prompt",
            "section",
            section_name,
            "--prompt-path",
            prompt_path,
            "--path",
            repo_path,
            "--json",
        ],
        timeout,
    )


def diff(
    baseline_path: str,
    prompt_path: str,
    repo_path: str = ".",
    max_lines: int = 200,
    timeout: int = 60,
) -> dict[str, Any]:
    """Return a redacted diff between a baseline and a prompt artifact."""
    return _run(
        [
            sys.executable,
            "-m",
            "ass_ade",
            "prompt",
            "diff",
            baseline_path,
            "--prompt-path",
            prompt_path,
            "--path",
            repo_path,
            "--max-lines",
            str(max_lines),
            "--json",
        ],
        timeout,
    )


def propose(
    objective: str,
    prompt_path: str,
    repo_path: str = ".",
    timeout: int = 60,
) -> dict[str, Any]:
    """Create a prompt improvement proposal for an artifact."""
    return _run(
        [
            sys.executable,
            "-m",
            "ass_ade",
            "prompt",
            "propose",
            objective,
            "--prompt-path",
            prompt_path,
            "--path",
            repo_path,
            "--json",
        ],
        timeout,
    )


def sync_agent(repo_path: str = ".", timeout: int = 60) -> dict[str, Any]:
    """Refresh Atomadic's generated capability block from live inventory."""
    return _run(
        [sys.executable, "-m", "ass_ade", "prompt", "sync-agent", "--path", repo_path, "--json"],
        timeout,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "ok": False,
                    "exit_code": 1,
                    "stderr": "Usage: prompt_tool.py <hash|validate|section|diff|propose|sync-agent> ...",
                },
                indent=2,
            )
        )
        sys.exit(1)

    action = sys.argv[1]
    if action == "hash" and len(sys.argv) >= 3:
        result = hash_prompt(sys.argv[2])
    elif action == "validate" and len(sys.argv) >= 4:
        result = validate(sys.argv[2], sys.argv[3])
    elif action == "section" and len(sys.argv) >= 4:
        result = section(sys.argv[2], sys.argv[3])
    elif action == "diff" and len(sys.argv) >= 4:
        result = diff(sys.argv[2], sys.argv[3])
    elif action == "propose" and len(sys.argv) >= 4:
        result = propose(sys.argv[2], sys.argv[3])
    elif action == "sync-agent":
        result = sync_agent(sys.argv[2] if len(sys.argv) >= 3 else ".")
    else:
        result = {"ok": False, "exit_code": 1, "stderr": f"invalid arguments for {action}"}

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else int(result.get("exit_code", 1) or 1))

"""Pre-rebuild hook: lint check before rebuild.

Runs ass-ade lint on the target path before allowing rebuild to proceed.
Lint failures are reported as warnings but do not block the rebuild.
The hook always returns ok=True so that rebuild can proceed even when
lint finds issues. Use the lint_clean field to decide whether to proceed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(path: str) -> dict:
    """Run a lint check before rebuild.

    Args:
        path: The codebase path that is about to be rebuilt.

    Returns:
        dict with keys:
            ok (bool): Always True; lint warnings do not block rebuild.
            lint_clean (bool): True when lint exits 0 (no errors found).
            lint_output (str): First 500 chars of lint stdout for logging.
            path_exists (bool): Whether the target path exists.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": False,
            "lint_clean": False,
            "lint_output": "",
            "path_exists": False,
            "error": f"path does not exist: {path}",
        }

    lint_result = subprocess.run(
        [
            sys.executable, "-m", "ass_ade", "lint", path,
            "--json", "--local-only",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    lint_output = lint_result.stdout[:500] if lint_result.stdout else lint_result.stderr[:500]
    lint_clean = lint_result.returncode == 0

    return {
        "ok": True,
        "lint_clean": lint_clean,
        "lint_output": lint_output,
        "path_exists": True,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    # Non-zero exit only when the path does not exist.
    if not result.get("ok"):
        sys.exit(1)

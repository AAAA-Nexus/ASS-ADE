"""Post-rebuild hook: run eco-scan on the rebuilt output folder.

Produces an onboarding pack (architecture snapshot, gap report, next moves)
after rebuild completes. Eco-scan failures are warnings only — they do not
block the pipeline.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(path: str) -> dict:
    """Run eco-scan on the rebuilt codebase.

    Args:
        path: The output folder produced by ass-ade rebuild.

    Returns:
        dict with keys:
            ok (bool): Always True; eco-scan failure is a warning.
            scan_completed (bool): True when eco-scan exits 0.
            exit_code (int): Raw process exit code.
            onboarding_pack (str | None): Path to the generated pack when ok.
            gap_count (int | None): Number of gaps found, if parseable.
            warnings (list[str]): Any issues encountered.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": True,
            "scan_completed": False,
            "exit_code": 3,
            "onboarding_pack": None,
            "gap_count": None,
            "warnings": [f"rebuilt output path does not exist: {path}"],
        }

    scan_result = subprocess.run(
        [sys.executable, "-m", "ass_ade", "eco-scan", path],
        capture_output=True,
        text=True,
        timeout=180,
    )

    scan_completed = scan_result.returncode == 0
    onboarding_pack: str | None = None
    gap_count: int | None = None
    warnings: list[str] = []

    # Parse stdout for the output path and gap count.
    for line in scan_result.stdout.splitlines():
        lower = line.lower()
        if "onboarding" in lower or "pack:" in lower or "written to" in lower:
            parts = line.split()
            if parts:
                onboarding_pack = parts[-1]
        if "gap" in lower:
            import re
            m = re.search(r"(\d+)\s+gap", lower)
            if m:
                gap_count = int(m.group(1))

    if not scan_completed:
        err = (scan_result.stderr.strip()[:300] or "no error output")
        warnings.append(f"eco-scan exited {scan_result.returncode}: {err}")

    return {
        "ok": True,
        "scan_completed": scan_completed,
        "exit_code": scan_result.returncode,
        "onboarding_pack": onboarding_pack,
        "gap_count": gap_count,
        "warnings": warnings,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    # Always exit 0; eco-scan failure is a warning.

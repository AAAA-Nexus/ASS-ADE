"""Post-rebuild hook: auto-generate documentation for the rebuilt output folder.

Runs ass-ade docs on the folder produced by ass-ade rebuild.
Reports the generated file count on success. Docs failures are
treated as warnings (ok=True) so the pipeline continues.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(path: str) -> dict:
    """Generate documentation for the rebuilt codebase.

    Args:
        path: The output folder produced by ass-ade rebuild.

    Returns:
        dict with keys:
            ok (bool): Always True; docs failure is a warning, not a blocker.
            docs_generated (bool): True when docs exits 0.
            exit_code (int): Raw process exit code from docs.
            output_dir (str | None): Directory where docs were written.
            file_count (int | None): Number of Markdown files generated.
            warnings (list[str]): Modules with missing docstrings, if any.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": True,
            "docs_generated": False,
            "exit_code": 3,
            "output_dir": None,
            "file_count": None,
            "warnings": [f"rebuilt output path does not exist: {path}"],
        }

    docs_result = subprocess.run(
        [sys.executable, "-m", "ass_ade", "docs", path],
        capture_output=True,
        text=True,
        timeout=120,
    )

    docs_generated = docs_result.returncode == 0
    output_dir = None
    file_count = None
    warnings: list[str] = []

    # Attempt to locate the output directory from stdout.
    for line in docs_result.stdout.splitlines():
        lower = line.lower()
        if "output:" in lower or "written to" in lower:
            parts = line.split()
            if parts:
                output_dir = parts[-1]
            break

    # Read DOCS_REPORT.json if we found the output directory.
    if output_dir:
        report_path = Path(output_dir) / "DOCS_REPORT.json"
        if report_path.exists():
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
                file_count = report.get("file_count")
                warnings = report.get("warnings", [])
            except (json.JSONDecodeError, OSError):
                pass

    if not docs_generated:
        warnings.append(
            f"docs command exited {docs_result.returncode}: "
            + (docs_result.stderr.strip()[:200] or "no error output")
        )

    return {
        "ok": True,
        "docs_generated": docs_generated,
        "exit_code": docs_result.returncode,
        "output_dir": output_dir,
        "file_count": file_count,
        "warnings": warnings,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    # Always exit 0; docs failure is a warning.

# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tools/docs_tool.py:10
# Component id: at.source.ass_ade.generate_docs
__version__ = "0.1.0"

def generate_docs(
    path: str,
    output: str | None = None,
    local_only: bool = False,
    fmt: str = "markdown",
    timeout: int = 120,
) -> dict:
    """Generate documentation for a codebase.

    Args:
        path: Absolute or relative path to the codebase.
        output: Write generated docs to this directory (default: auto-named).
        local_only: Skip AAAA-Nexus enrichment.
        fmt: Output format - "markdown" (default) or "html".
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
            report (dict | None): Parsed DOCS_REPORT.json when available.
    """
    cmd = [sys.executable, "-m", "ass_ade", "docs", path]
    if output:
        cmd.extend(["--output", output])
    if local_only:
        cmd.append("--local-only")
    if fmt != "markdown":
        cmd.extend(["--format", fmt])

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
            "stderr": f"docs timed out after {timeout}s",
            "report": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "report": None,
        }

    # Attempt to read DOCS_REPORT.json from the output directory.
    report = None
    if result.returncode == 0:
        # Output dir is either the user-supplied value or parsed from stdout.
        out_dir = output
        if not out_dir:
            for line in result.stdout.splitlines():
                if "output:" in line.lower() or "written to" in line.lower():
                    parts = line.split()
                    if parts:
                        out_dir = parts[-1]
                    break
        if out_dir:
            report_path = Path(out_dir) / "DOCS_REPORT.json"
            if report_path.exists():
                try:
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "report": report,
    }

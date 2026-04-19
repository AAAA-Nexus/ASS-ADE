# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_certify.py:7
# Component id: at.source.a1_at_functions.certify
from __future__ import annotations

__version__ = "0.1.0"

def certify(
    path: str,
    local_only: bool = False,
    output: str | None = None,
    timeout: int = 60,
) -> dict:
    """Compute a tamper-evident digest and request a Nexus-signed certificate.

    Args:
        path: Absolute or relative path to the codebase to certify.
        local_only: Skip Nexus signing; produce a local-only digest.
        output: Write the certificate to this file path (default: <path>/CERTIFICATE.json).
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
            certificate (dict | None): Parsed CERTIFICATE.json when available.
    """
    cmd = [sys.executable, "-m", "ass_ade", "certify", path]
    if local_only:
        cmd.append("--local-only")
    if output:
        cmd.extend(["--output", output])

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
            "stderr": f"certify timed out after {timeout}s",
            "certificate": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "certificate": None,
        }

    certificate = None
    if result.returncode == 0:
        cert_path = Path(output) if output else Path(path) / "CERTIFICATE.json"
        if cert_path.exists():
            try:
                certificate = json.loads(cert_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "certificate": certificate,
    }

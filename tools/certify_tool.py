"""Tool wrapper: certify and verify codebases via ass-ade certify."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


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


def verify(
    path: str,
    strict: bool = False,
    timeout: int = 60,
) -> dict:
    """Verify an existing certificate against the current state of a codebase.

    Args:
        path: Absolute or relative path to the codebase.
        strict: Exit non-zero if the certificate is local-only (unsigned).
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0 (digest matches + signature valid).
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
            valid (bool | None): Certificate validity from the stored JSON when readable.
    """
    cmd = [sys.executable, "-m", "ass_ade", "certify", "verify", path]
    if strict:
        cmd.append("--strict")

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
            "stderr": f"certify verify timed out after {timeout}s",
            "valid": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "valid": None,
        }

    valid = None
    cert_path = Path(path) / "CERTIFICATE.json"
    if cert_path.exists():
        try:
            cert = json.loads(cert_path.read_text(encoding="utf-8"))
            valid = cert.get("valid")
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "valid": valid,
    }


if __name__ == "__main__":
    # Usage: certify_tool.py <path>
    #        certify_tool.py verify <path>
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {
                    "ok": False,
                    "exit_code": 1,
                    "stderr": "Usage: certify_tool.py [verify] <path>",
                },
                indent=2,
            )
        )
        sys.exit(1)

    if sys.argv[1] == "verify":
        target = sys.argv[2] if len(sys.argv) > 2 else "."
        print(json.dumps(verify(target), indent=2))
    else:
        target = sys.argv[1]
        print(json.dumps(certify(target), indent=2))

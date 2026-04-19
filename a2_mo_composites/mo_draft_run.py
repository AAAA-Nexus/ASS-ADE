# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/hooks/post_rebuild.py:15
# Component id: mo.source.ass_ade.run
__version__ = "0.1.0"

def run(path: str) -> dict:
    """Certify the rebuilt codebase folder.

    Args:
        path: The output folder produced by ass-ade rebuild.

    Returns:
        dict with keys:
            ok (bool): True when certify exits 0.
            exit_code (int): Raw process exit code from certify.
            certificate_path (str | None): Path to CERTIFICATE.json when ok=True.
            digest_preview (str | None): First 16 chars of root_digest when ok=True.
            signed (bool): True when Nexus signature is present.
            error (str | None): Error message when ok=False.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": False,
            "exit_code": 3,
            "certificate_path": None,
            "digest_preview": None,
            "signed": False,
            "error": f"rebuilt output path does not exist: {path}",
        }

    certify_result = subprocess.run(
        [sys.executable, "-m", "ass_ade", "certify", path],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if certify_result.returncode != 0:
        return {
            "ok": False,
            "exit_code": certify_result.returncode,
            "certificate_path": None,
            "digest_preview": None,
            "signed": False,
            "error": certify_result.stderr.strip()[:300] or "certify returned non-zero",
        }

    cert_path = target / "CERTIFICATE.json"
    digest_preview = None
    signed = False

    if cert_path.exists():
        try:
            cert = json.loads(cert_path.read_text(encoding="utf-8"))
            root_digest = cert.get("digest", {}).get("root_digest", "")
            digest_preview = root_digest[:16] if root_digest else None
            signed = cert.get("signed_by") is not None
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "ok": True,
        "exit_code": certify_result.returncode,
        "certificate_path": str(cert_path) if cert_path.exists() else None,
        "digest_preview": digest_preview,
        "signed": signed,
        "error": None,
    }

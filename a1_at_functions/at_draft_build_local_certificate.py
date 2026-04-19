# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_build_local_certificate.py:5
# Component id: at.source.ass_ade.build_local_certificate
__version__ = "0.1.0"

def build_local_certificate(root: Path, version: str | None = None) -> dict[str, Any]:
    return {
        "schema": "ASS-ADE-CERT-001",
        "version": version or "unknown",
        "digest": compute_codebase_digest(root),
        "signed_by": None,
        "signature": None,
        "valid": False,
        "issuer": "atomadic.tech",
    }

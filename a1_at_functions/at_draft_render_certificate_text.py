# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_render_certificate_text.py:5
# Component id: at.source.ass_ade.render_certificate_text
__version__ = "0.1.0"

def render_certificate_text(cert: dict[str, Any]) -> str:
    digest = cert.get("digest", {})
    root_digest = digest.get("root_digest", "")
    sig = cert.get("signature")
    valid = cert.get("valid", False)

    lines = [
        "ASS-ADE Codebase Certificate",
        "=" * 40,
        f"Schema:      {cert.get('schema', '')}",
        f"Version:     {cert.get('version', '')}",
        f"Root:        {digest.get('root', '')}",
        f"File count:  {digest.get('file_count', 0)}",
        f"Root digest: {root_digest[:32]}",
        f"Computed at: {digest.get('computed_at', '')}",
        f"Valid:       {valid}",
        f"Signature:   {'present' if sig else 'none'}",
    ]
    return "\n".join(lines)

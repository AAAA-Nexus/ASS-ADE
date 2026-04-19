# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_content_hash.py:5
# Component id: at.source.ass_ade.content_hash
__version__ = "0.1.0"

def content_hash(text: str) -> str:
    """SHA-256 (first 16 hex chars) of whitespace-normalised content."""
    normalised = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]

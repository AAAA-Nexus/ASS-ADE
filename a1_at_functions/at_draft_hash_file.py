# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/certifier.py:40
# Component id: at.source.ass_ade.hash_file
__version__ = "0.1.0"

def hash_file(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_default_config_path.py:5
# Component id: at.source.ass_ade.default_config_path
__version__ = "0.1.0"

def default_config_path(base_dir: Path | None = None) -> Path:
    root = base_dir or Path.cwd()
    return root / ".ass-ade" / "config.json"

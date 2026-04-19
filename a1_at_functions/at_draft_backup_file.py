# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_bump_project_version.py:22
# Component id: at.source.a1_at_functions.backup_file
from __future__ import annotations

__version__ = "0.1.0"

def backup_file(path: Path) -> None:
    if dry_run or not path.exists():
        return
    rel = path.relative_to(root)
    target = backup_dir / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    files_backed_up.append(str(target))

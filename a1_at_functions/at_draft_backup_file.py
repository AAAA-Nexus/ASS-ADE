# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:577
# Component id: at.source.ass_ade.backup_file
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

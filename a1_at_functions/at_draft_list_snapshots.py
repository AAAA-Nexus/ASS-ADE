# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_filehistory.py:111
# Component id: at.source.ass_ade.list_snapshots
__version__ = "0.1.0"

    def list_snapshots(self, rel_path: str) -> list[Snapshot]:
        """List all snapshots for a file, oldest first."""
        snap_dir = self._snapshot_dir(rel_path)
        if not snap_dir.exists():
            return []

        result: list[Snapshot] = []
        for f in sorted(snap_dir.glob("*.snapshot")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                result.append(Snapshot(
                    path=data["path"],
                    sequence=data["sequence"],
                    timestamp=data["timestamp"],
                    content=data["content"],
                ))
            except (json.JSONDecodeError, KeyError):
                continue
        return result

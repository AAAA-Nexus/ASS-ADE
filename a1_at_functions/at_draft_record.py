# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_filehistory.py:42
# Component id: at.source.ass_ade.record
__version__ = "0.1.0"

    def record(self, rel_path: str, content: str) -> Snapshot:
        """Record current file content before a mutation."""
        seq = self._next_seq(rel_path)
        snap = Snapshot(
            path=rel_path,
            sequence=seq,
            timestamp=time.time(),
            content=content,
        )

        snap_dir = self._snapshot_dir(rel_path)
        snap_dir.mkdir(parents=True, exist_ok=True)

        snap_file = snap_dir / f"{seq:06d}.snapshot"
        snap_file.write_text(
            json.dumps({
                "path": snap.path,
                "sequence": snap.sequence,
                "timestamp": snap.timestamp,
                "content": snap.content,
            }),
            encoding="utf-8",
        )

        # Prune old snapshots
        self._prune(rel_path)

        return snap

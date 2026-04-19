# Extracted from C:/!ass-ade/src/ass_ade/tools/history.py:36
# Component id: mo.source.ass_ade.filehistory
from __future__ import annotations

__version__ = "0.1.0"

class FileHistory:
    """Manages undo history for file mutations.

    Stores snapshots in .ass-ade/history/ under the working directory.
    """

    def __init__(self, working_dir: str = ".", max_depth: int = 20) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history_dir = self._cwd / ".ass-ade" / "history"
        self._max_depth = max_depth
        self._counters: dict[str, int] = {}

    def _file_hash(self, rel_path: str) -> str:
        return hashlib.sha256(rel_path.encode()).hexdigest()[:16]

    def _snapshot_dir(self, rel_path: str) -> Path:
        return self._history_dir / self._file_hash(rel_path)

    def _next_seq(self, rel_path: str) -> int:
        if rel_path not in self._counters:
            snap_dir = self._snapshot_dir(rel_path)
            if snap_dir.exists():
                existing = sorted(snap_dir.glob("*.snapshot"))
                if existing:
                    try:
                        last = json.loads(existing[-1].read_text(encoding="utf-8"))
                        self._counters[rel_path] = last["sequence"] + 1
                    except (json.JSONDecodeError, KeyError):
                        self._counters[rel_path] = len(existing)
                else:
                    self._counters[rel_path] = 0
            else:
                self._counters[rel_path] = 0
        seq = self._counters[rel_path]
        self._counters[rel_path] = seq + 1
        return seq

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

    def undo(self, rel_path: str) -> Snapshot | None:
        """Pop the most recent snapshot and restore the file.

        Returns the snapshot that was restored, or None if no history.
        """
        snap_dir = self._snapshot_dir(rel_path)
        if not snap_dir.exists():
            return None

        snapshots = sorted(snap_dir.glob("*.snapshot"))
        if not snapshots:
            return None

        latest = snapshots[-1]
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            return None

        snap = Snapshot(
            path=data["path"],
            sequence=data["sequence"],
            timestamp=data["timestamp"],
            content=data["content"],
        )

        # Restore the file
        target = self._cwd / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(snap.content, encoding="utf-8")

        # Remove the snapshot (consumed)
        latest.unlink()

        # Reset counter
        if rel_path in self._counters:
            self._counters[rel_path] = max(0, self._counters[rel_path] - 1)

        return snap

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

    def depth(self, rel_path: str) -> int:
        """Number of undo steps available for a file."""
        snap_dir = self._snapshot_dir(rel_path)
        if not snap_dir.exists():
            return 0
        return len(list(snap_dir.glob("*.snapshot")))

    def _prune(self, rel_path: str) -> None:
        """Remove oldest snapshots beyond max_depth."""
        snap_dir = self._snapshot_dir(rel_path)
        if not snap_dir.exists():
            return

        snapshots = sorted(snap_dir.glob("*.snapshot"))
        while len(snapshots) > self._max_depth:
            snapshots[0].unlink()
            snapshots.pop(0)

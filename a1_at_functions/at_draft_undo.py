# Extracted from C:/!ass-ade/src/ass_ade/tools/history.py:102
# Component id: at.source.ass_ade.undo
from __future__ import annotations

__version__ = "0.1.0"

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

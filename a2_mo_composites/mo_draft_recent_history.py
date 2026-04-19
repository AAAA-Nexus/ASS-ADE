# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memorystore.py:98
# Component id: mo.source.ass_ade.recent_history
__version__ = "0.1.0"

    def recent_history(self, n: int = 5) -> list[dict]:
        if not self._history_path.exists():
            return []
        lines = self._history_path.read_text(encoding="utf-8").splitlines()
        results = []
        for line in reversed(lines[-n * 2:]):
            try:
                results.append(json.loads(line))
                if len(results) >= n:
                    break
            except json.JSONDecodeError:
                continue
        return list(reversed(results))

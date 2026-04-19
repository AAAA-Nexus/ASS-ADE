# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:111
# Component id: at.source.ass_ade.get_stale_files
__version__ = "0.1.0"

    def get_stale_files(self, paths: list[str | Path] | None = None) -> list[FreshnessReport]:
        """Return stale freshness reports for all tracked paths (or given subset)."""
        if paths is not None:
            targets = [str(Path(p).resolve()) for p in paths]
        else:
            targets = list(self._reads.keys())
        stale = []
        for p in targets:
            report = self.check_freshness(p)
            if not report.fresh:
                stale.append(report)
        self._stale_count = len(stale)
        return stale

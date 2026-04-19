# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:51
# Component id: mo.source.ass_ade.check_freshness
__version__ = "0.1.0"

    def check_freshness(self, path: str | Path) -> FreshnessReport:
        """Check whether a file is fresh (read within threshold)."""
        key = str(Path(path).resolve())
        ts = self._reads.get(key)
        now = time.time()
        if ts is None:
            return FreshnessReport(
                path=key, fresh=False, last_read_ts=None,
                age_hours=None, threshold_hours=self._threshold_hours,
            )
        age_hours = (now - ts) / 3600.0
        return FreshnessReport(
            path=key,
            fresh=age_hours <= self._threshold_hours,
            last_read_ts=ts,
            age_hours=round(age_hours, 2),
            threshold_hours=self._threshold_hours,
        )

# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:42
# Component id: mo.source.ass_ade.tcaengine
__version__ = "0.1.0"

class TCAEngine:
    """Technical Context Acquisition — NCB freshness enforcement."""

    def __init__(self, config: dict[str, Any] | None = None, nexus: Any = None) -> None:
        self._config = config or {}
        self._nexus = nexus
        cfg = self._config.get("tca") or {}
        self._threshold_hours = float(cfg.get("freshness_hours", _DEFAULT_FRESHNESS_HOURS))
        # Root the state file under working_dir if provided; else default to CWD.
        # This makes the freshness map survive MCP server restarts and lets
        # multiple projects each have their own TCA state.
        working_dir = self._config.get("working_dir") or cfg.get("working_dir") or "."
        default_state = Path(working_dir) / ".ass-ade" / "state" / "tca_reads.json"
        self._state_file = Path(cfg.get("state_file", str(default_state)))
        self._reads: dict[str, float] = {}  # path → timestamp
        self._gaps: list[GAPEntry] = []
        self._stale_count = 0
        self._load_state()

    # ── Persistence ───────────────────────────────────────────────────────

    def _load_state(self) -> None:
        try:
            if self._state_file.exists():
                data = json.loads(self._state_file.read_text(encoding="utf-8"))
                self._reads = {k: float(v) for k, v in data.get("reads", {}).items()}
        except Exception as exc:
            _log.debug("TCA state load failed: %s", exc)

    def _save_state(self) -> None:
        try:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            self._state_file.write_text(
                json.dumps({"reads": self._reads}, indent=2), encoding="utf-8"
            )
        except Exception as exc:
            _log.debug("TCA state save failed: %s", exc)

    # ── Public API ────────────────────────────────────────────────────────

    def record_read(self, path: str | Path) -> None:
        """Mark a file as freshly read. Call this from MCP read_file handler."""
        key = str(Path(path).resolve())
        self._reads[key] = time.time()
        self._save_state()

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

    def ncb_contract(self, target_path: str | Path) -> bool:
        """Return True if NCB contract is satisfied (file was read before writing)."""
        return self.check_freshness(target_path).fresh

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

    def record_gap(self, description: str, source: str = "") -> None:
        """Record a documentation gap discovered during synthesis."""
        self._gaps.append(GAPEntry(description=description, source=source))

    def get_gaps(self) -> list[dict[str, Any]]:
        return [
            {"description": g.description, "source": g.source, "ts": g.ts}
            for g in self._gaps
        ]

    def pre_synthesis_check(self, candidate_paths: list[str]) -> dict[str, Any]:
        """Run freshness check for a list of candidate write targets.

        Returns dict with: fresh_count, stale_paths, ncb_violated, gaps
        """
        stale = self.get_stale_files([p for p in candidate_paths if p])
        stale_paths = [r.path for r in stale]
        return {
            "fresh_count": len(candidate_paths) - len(stale_paths),
            "stale_paths": stale_paths,
            "ncb_violated": len(stale_paths) > 0,
            "gaps": self.get_gaps(),
        }

    def report(self) -> dict[str, Any]:
        return {
            "engine": "tca",
            "tracked_files": len(self._reads),
            "stale_count": self._stale_count,
            "gap_count": len(self._gaps),
            "threshold_hours": self._threshold_hours,
        }

# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1347
# Component id: mo.source.ass_ade.forge_leaderboard
__version__ = "0.1.0"

    def forge_leaderboard(self, **kwargs: Any) -> ForgeLeaderboardResponse:
        """GET /v1/forge/leaderboard — Forge agent leaderboard. Free."""
        return self._get_model("/v1/forge/leaderboard", ForgeLeaderboardResponse, **kwargs)

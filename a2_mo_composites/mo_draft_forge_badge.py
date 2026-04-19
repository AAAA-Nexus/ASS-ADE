# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1363
# Component id: mo.source.ass_ade.forge_badge
__version__ = "0.1.0"

    def forge_badge(self, badge_id: str, **kwargs: Any) -> ForgeBadgeResult:
        """GET /v1/forge/badge/{id} — retrieve Forge badge metadata. Free."""
        return self._get_model(f"/v1/forge/badge/{_pseg(badge_id, 'badge_id')}", ForgeBadgeResult, **kwargs)

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_providerprofile.py:41
# Component id: at.source.ass_ade.is_available
__version__ = "0.1.0"

    def is_available(self, config_key: str | None = None) -> bool:
        """True if this provider has auth (or is local + reachable)."""
        if self.local:
            return True
        return self.resolve_api_key(config_key) is not None

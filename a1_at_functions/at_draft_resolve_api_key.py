# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_providerprofile.py:24
# Component id: at.source.ass_ade.resolve_api_key
__version__ = "0.1.0"

    def resolve_api_key(self, config_key: str | None = None) -> str | None:
        """Resolve the API key: config override → env var → default."""
        if config_key:
            return config_key
        if self.api_key_env:
            env_val = os.getenv(self.api_key_env)
            if env_val:
                return env_val
        return self.api_key_default

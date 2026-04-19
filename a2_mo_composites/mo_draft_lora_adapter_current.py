# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1394
# Component id: mo.source.ass_ade.lora_adapter_current
__version__ = "0.1.0"

    def lora_adapter_current(self, language: str = "python", **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/adapter/{language} — latest adapter id for a language."""
        return self._get_raw(f"/v1/lora/adapter/{_pseg(language, 'language')}", **kwargs)

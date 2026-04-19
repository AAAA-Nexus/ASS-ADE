# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:65
# Component id: at.source.ass_ade.test_fallback_chain_contains_only_known_providers
__version__ = "0.1.0"

    def test_fallback_chain_contains_only_known_providers(self):
        known = set(FREE_PROVIDERS.keys())
        for name in DEFAULT_FALLBACK_CHAIN:
            assert name in known, f"fallback chain references unknown provider {name}"

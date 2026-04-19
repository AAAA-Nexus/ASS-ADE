# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexusasprovider.py:19
# Component id: at.source.ass_ade.test_nexus_selectable_via_tier_policy
__version__ = "0.1.0"

    def test_nexus_selectable_via_tier_policy(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        from ass_ade.agent.lse import LSEEngine

        lse = LSEEngine({"tier_policy": {"deep": "nexus"}})
        decision = lse.select(trs_score=0.3, complexity="critical")
        assert decision.provider == "nexus"

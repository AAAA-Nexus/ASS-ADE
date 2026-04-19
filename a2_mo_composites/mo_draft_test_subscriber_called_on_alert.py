# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:217
# Component id: mo.source.ass_ade.test_subscriber_called_on_alert
__version__ = "0.1.0"

    def test_subscriber_called_on_alert(self) -> None:
        b = BAS({})
        received: list[Alert] = []
        b.subscribe(lambda a: received.append(a))
        b.monitor_all({"synergy": 0.9})
        assert len(received) >= 1
        assert received[0].kind == "emergent_synergy"

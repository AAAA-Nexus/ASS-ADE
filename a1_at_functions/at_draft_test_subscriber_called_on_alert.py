# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:50
# Component id: at.source.ass_ade.test_subscriber_called_on_alert
__version__ = "0.1.0"

    def test_subscriber_called_on_alert(self) -> None:
        b = BAS({})
        received: list[Alert] = []
        b.subscribe(lambda a: received.append(a))
        b.monitor_all({"synergy": 0.9})
        assert len(received) >= 1
        assert received[0].kind == "emergent_synergy"

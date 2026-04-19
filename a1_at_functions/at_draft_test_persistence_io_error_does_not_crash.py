# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:87
# Component id: at.source.ass_ade.test_persistence_io_error_does_not_crash
__version__ = "0.1.0"

    def test_persistence_io_error_does_not_crash(self, tmp_path: Path) -> None:
        # Point to a directory path (not writable as file)
        b = BAS({"bas_state_path": str(tmp_path)})
        b.alert("novelty_spike", {"novelty": 0.8})  # should not raise

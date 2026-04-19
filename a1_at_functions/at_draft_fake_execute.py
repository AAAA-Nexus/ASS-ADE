# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_atomadic_dispatches_dynamic_cli_args.py:18
# Component id: at.source.ass_ade.fake_execute
__version__ = "0.1.0"

    def fake_execute(self: Atomadic, cmd: list[str]) -> str:
        captured["cmd"] = cmd
        return '{"profile":"local"}'

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_compliance_oversight_history_happy_path.py:7
# Component id: at.source.ass_ade.handler
__version__ = "0.1.0"

    def handler(request):
        return httpx.Response(200, json={"history": [{"reviewer": "rev1", "decision": "approved"}]})

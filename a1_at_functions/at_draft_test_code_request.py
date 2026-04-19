# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testclassifycomplexity.py:10
# Component id: at.source.ass_ade.test_code_request
__version__ = "0.1.0"

    def test_code_request(self):
        c = classify_complexity("Write a Python function to sort a list")
        assert c >= 0.3  # code keywords

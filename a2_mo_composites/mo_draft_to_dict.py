# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memorystore.py:70
# Component id: mo.source.ass_ade.to_dict
__version__ = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_profile": self.user_profile,
            "project_contexts": self.project_contexts,
            "preferences": self.preferences,
        }

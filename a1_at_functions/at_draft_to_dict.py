# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_reconreport.py:131
# Component id: at.source.ass_ade.to_dict
__version__ = "0.1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "duration_ms": self.duration_ms,
            "summary": self.summary,
            "scout": self.scout,
            "dependency": self.dependency,
            "tier": self.tier,
            "test": self.test,
            "doc": self.doc,
            "recommendations": self.recommendations,
            "next_action": self.next_action,
        }

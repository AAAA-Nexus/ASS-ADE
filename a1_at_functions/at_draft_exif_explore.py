# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_edee.py:66
# Component id: at.source.ass_ade.exif_explore
__version__ = "0.1.0"

    def exif_explore(self, missing_skill: str, env: dict | None = None):
        return self._get_exif().explore(missing_skill, env or {"name": "default"})

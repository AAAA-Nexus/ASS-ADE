# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_ide.py:25
# Component id: at.source.ass_ade.evaluate_fitness
__version__ = "0.1.0"

    def evaluate_fitness(self, cand: Candidate) -> float:
        novelty = 0.1 * (cand.features[0] + cand.features[1])
        return min(1.0, cand.fitness + novelty)

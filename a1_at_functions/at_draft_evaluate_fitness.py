# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_evaluate_fitness.py:7
# Component id: at.source.a1_at_functions.evaluate_fitness
from __future__ import annotations

__version__ = "0.1.0"

def evaluate_fitness(self, cand: Candidate) -> float:
    novelty = 0.1 * (cand.features[0] + cand.features[1])
    return min(1.0, cand.fitness + novelty)

# Extracted from C:/!ass-ade/src/ass_ade/agent/ide.py:42
# Component id: at.source.ass_ade.evaluate_fitness
from __future__ import annotations

__version__ = "0.1.0"

def evaluate_fitness(self, cand: Candidate) -> float:
    novelty = 0.1 * (cand.features[0] + cand.features[1])
    return min(1.0, cand.fitness + novelty)

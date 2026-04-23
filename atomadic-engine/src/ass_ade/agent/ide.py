"""v18 engine — IDE 3.0 MAP-Elites innovation grid."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Candidate:
    id: str
    features: tuple[int, int]
    fitness: float
    payload: dict = field(default_factory=dict)


@dataclass
class SIP:
    top: list[Candidate]
    summary: str


class IDE:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._grid: dict[tuple[int, int], Candidate] = {}
        self._searches = 0

    def _seed(self) -> list[Candidate]:
        base = [
            Candidate(id="c0", features=(0, 0), fitness=0.3, payload={"kind": "baseline"}),
            Candidate(id="c1", features=(1, 0), fitness=0.6, payload={"kind": "variant"}),
            Candidate(id="c2", features=(1, 1), fitness=0.75, payload={"kind": "variant"}),
            Candidate(id="c3", features=(2, 1), fitness=0.82, payload={"kind": "novel"}),
        ]
        for c in base:
            current = self._grid.get(c.features)
            if current is None or c.fitness > current.fitness:
                self._grid[c.features] = c
        return base

    def evaluate_fitness(self, cand: Candidate) -> float:
        novelty = 0.1 * (cand.features[0] + cand.features[1])
        return min(1.0, cand.fitness + novelty)

    def search(self) -> list[Candidate]:
        self._searches += 1
        self._seed()
        return sorted(self._grid.values(), key=lambda c: c.fitness, reverse=True)

    def generate_sip(self, top: list[Candidate]) -> SIP:
        head = top[:3]
        summary = "; ".join(f"{c.id}@{c.fitness:.2f}" for c in head)
        return SIP(top=head, summary=summary)

    def run(self, ctx: dict) -> dict:
        top = self.search()
        sip = self.generate_sip(top)
        return {
            "grid_size": len(self._grid),
            "top": [c.__dict__ for c in sip.top],
            "summary": sip.summary,
        }

    def report(self) -> dict:
        return {"engine": "ide", "searches": self._searches, "grid_size": len(self._grid)}

"""Tier a2 — adaptive personality engine for the Atomadic interpreter."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path

_MEMORY_DIR = Path.home() / ".ass-ade" / "memory"

# ── Persona constants ──────────────────────────────────────────────────────────

PERSONA_COPILOT = "co-pilot"
PERSONA_MENTOR = "mentor"
PERSONA_COMMANDER = "commander"
PERSONA_ARCHITECT = "architect"
PERSONA_DEBUG = "debug-buddy"

ALL_PERSONAS = (PERSONA_COPILOT, PERSONA_MENTOR, PERSONA_COMMANDER, PERSONA_ARCHITECT, PERSONA_DEBUG)

_PERSONA_DESCRIPTIONS = {
    PERSONA_COPILOT:   "Pair-programming mode — suggests next steps, asks targeted questions",
    PERSONA_MENTOR:    "Teaching mode — explains the why, guides toward understanding",
    PERSONA_COMMANDER: "Direct execution mode — minimal explanation, maximum action",
    PERSONA_ARCHITECT: "Design-first mode — thinks in patterns, tradeoffs, and systems",
    PERSONA_DEBUG:     "Debugging mode — empathetic, systematic, hypothesis-driven",
}

# ── Energy / domain signals ────────────────────────────────────────────────────

_FRUSTRATION_WORDS = {
    "still", "again", "broken", "keeps", "wrong", "failing", "useless",
    "terrible", "nothing", "not working", "not again", "why", "fix this",
}
_EXCITEMENT_WORDS = {
    "awesome", "perfect", "great", "love it", "yes!", "amazing", "brilliant",
    "exactly", "finally", "works", "beautiful", "excellent", "fantastic",
}
_EXPERT_WORDS = {
    "subclass", "metaclass", "decorator", "lambda", "generator", "async",
    "typeddict", "protocol", "mypy", "refactor", "impl", "runtime", "bytecode",
    "coroutine", "gil", "thread", "mutex", "semaphore", "cache", "optimize",
}
_NOVICE_WORDS = {
    "not sure", "don't know", "how do i", "what is", "beginner", "new to",
    "first time", "help me", "tutorial", "example", "what does", "explain",
}


@dataclass
class PersonalityEngine:
    """Stateful personality tracker that adapts Atomadic's voice to each user.

    Learns from messages:
    - Persona: which operating mode fits (co-pilot, mentor, commander, etc.)
    - Energy: frustration / excitement / neutral
    - Verbosity: short | medium | long (from message length patterns)
    - Emoji: whether the user uses / appreciates them
    - Domain level: novice / intermediate / expert
    """

    persona: str = PERSONA_COPILOT
    verbosity: str = "medium"
    use_emoji: bool = True
    domain_level: str = "intermediate"

    # Running counters — not persisted, reset each session
    _frustration_streak: int = field(default=0, init=False, repr=False)
    _excitement_streak: int = field(default=0, init=False, repr=False)
    _short_msg_streak: int = field(default=0, init=False, repr=False)
    _energy: str = field(default="neutral", init=False, repr=False)

    def __post_init__(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "PersonalityEngine":
        engine = cls()
        p = _MEMORY_DIR / "personality.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for key in ("persona", "verbosity", "use_emoji", "domain_level"):
                    if key in data:
                        setattr(engine, key, data[key])
            except (json.JSONDecodeError, OSError):
                pass
        return engine

    def save(self) -> None:
        try:
            (_MEMORY_DIR / "personality.json").write_text(
                json.dumps({
                    "persona": self.persona,
                    "verbosity": self.verbosity,
                    "use_emoji": self.use_emoji,
                    "domain_level": self.domain_level,
                }, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def set_persona(self, persona: str) -> bool:
        """Set persona mode. Returns True if the name is valid."""
        if persona in ALL_PERSONAS:
            self.persona = persona
            self.save()
            return True
        return False

    @property
    def energy(self) -> str:
        return self._energy

    # ── Input learning ─────────────────────────────────────────────────────────

    def update_from_input(self, text: str) -> None:
        """Observe user message and update all personality signals."""
        lower = text.lower()
        words = set(lower.split())

        # --- energy ---
        frust = len(words & _FRUSTRATION_WORDS) + text.count("!") // 2
        if text.isupper() and len(text) > 8:
            frust += 2
        excite = len(words & _EXCITEMENT_WORDS)

        if frust >= 2:
            self._frustration_streak = min(self._frustration_streak + 1, 5)
            self._excitement_streak = max(self._excitement_streak - 1, 0)
        elif excite >= 1:
            self._excitement_streak = min(self._excitement_streak + 1, 3)
            self._frustration_streak = max(self._frustration_streak - 1, 0)
        else:
            self._frustration_streak = max(self._frustration_streak - 1, 0)
            self._excitement_streak = max(self._excitement_streak - 1, 0)

        if self._frustration_streak >= 2:
            self._energy = "frustrated"
        elif self._excitement_streak >= 1:
            self._energy = "excited"
        else:
            self._energy = "neutral"

        # --- domain level ---
        expert_hits = sum(1 for w in _EXPERT_WORDS if w in lower)
        novice_hits = sum(1 for w in _NOVICE_WORDS if w in lower)
        if expert_hits >= 2:
            self.domain_level = "expert"
        elif novice_hits >= 2:
            self.domain_level = "novice"

        # --- emoji preference ---
        if re.search(r"[\U00010000-\U0010ffff]|[\u2600-\u27BF]", text):
            self.use_emoji = True

        # --- verbosity ---
        word_count = len(text.split())
        if word_count <= 4:
            self._short_msg_streak = min(self._short_msg_streak + 1, 5)
        else:
            self._short_msg_streak = max(self._short_msg_streak - 1, 0)

        if self._short_msg_streak >= 3:
            self.verbosity = "short"
        elif word_count > 30:
            self.verbosity = "long"
        else:
            self.verbosity = "medium"

    # ── Response shaping ───────────────────────────────────────────────────────

    def shape_response(self, response: str) -> str:
        """Apply persona, energy, and style calibration to a response string."""
        prefix = self._persona_prefix()
        if prefix:
            response = f"{prefix}\n\n{response}"

        if self._energy == "frustrated":
            response = self._soften(response)
        elif self._energy == "excited" and self.use_emoji:
            response = self._energize(response)

        return response

    def _persona_prefix(self) -> str | None:
        if self.persona == PERSONA_DEBUG and self._energy == "frustrated":
            return "Let's debug this together, step by step."
        if self.persona == PERSONA_MENTOR and self.domain_level == "novice":
            return "Happy to walk you through this."
        if self.persona == PERSONA_COPILOT and self._energy == "frustrated":
            return "I've got you — let's sort this out."
        return None

    def _soften(self, text: str) -> str:
        lower = text.lower()
        if any(s in lower for s in ("let's", "together", "got you", "sort this")):
            return text  # already has empathy
        options = [
            "I hear you — here's what's happening:",
            "No worries, let's work through this:",
            "Hang tight — here's what I found:",
        ]
        return f"{random.choice(options)}\n\n{text}"

    def _energize(self, text: str) -> str:
        if not text.rstrip().endswith(("!", "🚀", "✅", "🎉")):
            return text.rstrip() + " 🚀"
        return text

    # ── Greetings ──────────────────────────────────────────────────────────────

    def greeting_prefix(self, name: str | None = None) -> str:
        """Return a persona-tuned greeting line (Axiom 0: sovereign, purposeful, builder-first)."""
        n = name or "Thomas"
        pool = {
            PERSONA_COPILOT:   [
                f"Welcome back, {n}. Atomadic is here. What shall we build today?",
                f"Ready, {n}. What's the mission?",
                f"Good to have you back, {n}. What are we working on?",
            ],
            PERSONA_MENTOR:    [
                f"Welcome back, {n}. What shall we shape today?",
                f"Good to see you, {n}. What are we building?",
            ],
            PERSONA_COMMANDER: [
                f"Standing by, {n}. What's the objective?",
                f"Ready, {n}. Your call.",
                f"Online, {n}. Give the order.",
            ],
            PERSONA_ARCHITECT: [
                f"Back in the design room, {n}. What are we architecting?",
                f"Good timing, {n}. What system are we drawing up?",
            ],
            PERSONA_DEBUG:     [
                f"Atomadic here, {n}. What needs fixing?",
                f"Ready to diagnose, {n}. What's acting up?",
            ],
        }
        return random.choice(pool.get(self.persona, [f"Welcome back, {n}."]))

    # ── Introspection ──────────────────────────────────────────────────────────

    def describe(self) -> str:
        emoji_str = "yes" if self.use_emoji else "no"
        lines = [
            "**Personality State**\n",
            f"- **Persona:** {self.persona} — {_PERSONA_DESCRIPTIONS.get(self.persona, '')}",
            f"- **Energy:** {self._energy}",
            f"- **Verbosity:** {self.verbosity}",
            f"- **Domain:** {self.domain_level}",
            f"- **Emoji:** {emoji_str}",
            "",
            "Change persona with `@persona <mode>`.",
            f"Available: {', '.join(ALL_PERSONAS)}",
        ]
        return "\n".join(lines)

"""Tier a2 — voice narrator: speaks interpreter responses and observability events via TTS."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Default voice — warm, clear, natural-sounding US English male.
DEFAULT_VOICE = "en-US-GuyNeural"

# Event types that get a short spoken announcement during tool dispatch.
_SPEAKABLE_TYPES = frozenset({"intent", "error"})

# How to convert each event type into spoken text.
_EVENT_LINES = {
    "intent":    lambda e: f"Running {e.get('intent', 'command')}.",
    "tool_call": lambda e: f"Calling {e.get('tool', 'command')}.",
    "error":     lambda e: f"Error: {e.get('message', 'unknown error')}",
    "decision":  lambda e: e.get("decision", ""),
}


@dataclass
class VoiceNarrator:
    """Stateful narrator: speaks Atomadic responses and selected observability events.

    speak_responses — narrate the full assistant reply after each turn
    speak_events    — narrate key observability events (intent, tool_call, error)
    voice           — edge-tts voice name (see ``edge-tts --list-voices``)
    """

    voice: str = DEFAULT_VOICE
    speak_responses: bool = True
    speak_events: bool = True

    # ── Public API ──────────────────────────────────────────────────────────────

    def narrate(self, text: str) -> None:
        """Speak a full response or arbitrary text."""
        if not text:
            return
        self._speak(text)

    def narrate_event(self, event: dict) -> None:
        """Speak a short announcement for an observability event if it is speakable."""
        if not self.speak_events:
            return
        etype = event.get("type", "")
        if etype not in _SPEAKABLE_TYPES:
            return
        fn = _EVENT_LINES.get(etype)
        if not fn:
            return
        line = fn(event)
        if line:
            self._speak(line)

    # ── Internal ────────────────────────────────────────────────────────────────

    def _speak(self, text: str) -> None:
        try:
            from ass_ade.a1_at_functions.speech import speak
            speak(text, voice=self.voice)
        except Exception:
            pass

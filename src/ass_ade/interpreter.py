"""Atomadic interpreter — conversational front door for ASS-ADE.

Persistent local memory lives in ~/.ass-ade/memory/ and is NEVER sent remotely.

Receives any user input (casual, technical, vague, precise), detects their
conversation style, derives the actual intent, maps it to the correct ass-ade
command, executes it, and reports back in a matching tone.

6-step intent derivation pipeline:
    1. receive      — accept any user message, no pre-filtering
    2. extract      — pull signals: path, action verbs, technical markers, tone
    3. gap-analyze  — identify ambiguities; flag what's genuinely missing
    4. clarify      — ask ONE targeted question if truly needed; skip if derivable
    5. map          — translate the derived goal to a specific ass-ade command
    6. construct    — build the exact CLI invocation and execute it

Epistemic honesty: Atomadic reports what it actually did, what succeeded,
what failed, and what it is uncertain about. It does not fabricate results.

Self-bootstrap: Atomadic is aware it is the front door of ASS-ADE and can
describe its own capabilities when asked.

Axiom 0 (Jessica Mary Colvin): Every boundary is also a door.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from ass_ade.agent.capabilities import (
    build_atomadic_intent_prompt,
    command_path_exists,
    render_capability_prompt_section,
    render_atomadic_help,
)
from ass_ade.a2_mo_composites.personality_engine import PersonalityEngine
from ass_ade.a2_mo_composites.episodic_memory import EpisodicStore

# Ensure stdout/stderr use UTF-8 on Windows without replacing pytest/caller streams.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# ── LLM endpoint selection ─────────────────────────────────────────────────────

_FALLBACK_LLM_SYSTEM_PROMPT = """\
You are Atomadic, the intelligent front door of ASS-ADE.
Classify the user's message and respond with only one JSON object.
Known core intents: rebuild, design, add-feature, docs, lint, certify, enhance,
eco-scan, recon, doctor, self-enhance, clean, help, chat.
"""


def _fallback_llm_system_prompt(
    working_dir: Path | str | None,
    memory_context: str | None = None,
) -> str:
    """Build a fallback prompt that still carries live capabilities."""
    parts = [_FALLBACK_LLM_SYSTEM_PROMPT.strip()]
    if memory_context:
        parts.append(f"User Context:\n{memory_context}")
    try:
        parts.append(render_capability_prompt_section(working_dir or Path.cwd()))
    except Exception:
        pass
    return "\n\n".join(parts)

# Priority-ordered keyed provider specs: (name, base_url, api_key_env, model)
# Provider registry: slug → (base_url, key_env, model, auth_style)
# key_env=None    → no API key needed (anonymous or local)
# model=None      → read from config (ollama only)
# auth_style      → "bearer" (Authorization header) | "x-api-key" (X-API-Key header)
_PROVIDER_REGISTRY: dict[str, tuple[str, str | None, str | None, str]] = {
    "aaaa-nexus":   ("https://atomadic.tech/v1/inference",                      "AAAA_NEXUS_API_KEY",  "falcon3-10B-1.58",                       "x-api-key"),
    "groq":         ("https://api.groq.com/openai/v1",                          "GROQ_API_KEY",        "llama-3.3-70b-versatile",                "bearer"),
    "cerebras":     ("https://api.cerebras.ai/v1",                              "CEREBRAS_API_KEY",    "llama3.3-70b",                           "bearer"),
    "gemini":       ("https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY",      "gemini-2.0-flash",                       "bearer"),
    "openrouter":   ("https://openrouter.ai/api/v1",                            "OPENROUTER_API_KEY",  "meta-llama/llama-3.3-70b-instruct:free", "bearer"),
    "mistral":      ("https://api.mistral.ai/v1",                               "MISTRAL_API_KEY",     "mistral-small-latest",                   "bearer"),
    "github":       ("https://models.inference.ai.azure.com",                   "GITHUB_TOKEN",        "gpt-4o-mini",                            "bearer"),
    "ollama":       ("http://localhost:11434/v1",                                None,                  None,                                     "bearer"),
    "pollinations": ("https://text.pollinations.ai/openai",                     None,                  "openai",                                 "bearer"),
}

# Preferred instruct/chat model name prefixes for setup-time scanning only.
# Runtime uses the model saved in config — no auto-detection at runtime.
_OLLAMA_MODEL_PREFS = ("qwen", "deepseek", "llama", "mistral", "phi", "gemma")


def _load_env() -> None:
    """Load .env from cwd upward (best-effort; silently skipped if dotenv absent)."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass


def get_ollama_models() -> list[str]:
    """Probe local Ollama and return all available model names.

    Used only during `ass-ade setup` to present a model selection menu.
    NOT called at interpreter runtime — use the configured model from config instead.
    """
    try:
        tags = httpx.get("http://localhost:11434/api/tags", timeout=1.5).json()
        models = [m["name"] for m in tags.get("models", [])]
        if not models:
            return []
        # Sort: preferred instruction-tuned models first, base weights last
        def _sort_key(name: str) -> tuple[int, str]:
            low = name.lower()
            for i, pref in enumerate(_OLLAMA_MODEL_PREFS):
                if pref in low and "base" not in low:
                    return (i, name)
            return (len(_OLLAMA_MODEL_PREFS), name)
        return sorted(models, key=_sort_key)
    except Exception:
        return []


def _load_interpreter_config() -> "AssAdeConfig":
    """Load AssAdeConfig from the nearest .ass-ade/config.json, or defaults."""
    try:
        from ass_ade.config import load_config
        return load_config()
    except Exception:
        try:
            from ass_ade.config import AssAdeConfig
            return AssAdeConfig()
        except Exception:
            # Pure fallback: a minimal duck-typed object with defaults
            class _Defaults:
                ollama_model = ""
                llm_priority = "cloud"
                llm_providers: list = []
                nexus_api_key = None
            return _Defaults()  # type: ignore[return-value]


_MEMORY_SKIP_KEYS = frozenset({"tone_counts", "command_counts", "dominant_tone",
                                "favorite_command", "session_interactions"})


def _summarize_memory(memory: "MemoryStore") -> str | None:
    """Return a compact memory context string, or None if nothing meaningful."""
    profile = memory.user_profile
    if not profile:
        return None
    parts: list[str] = []
    # Personal facts first — name, note, role, email, etc.
    for k, v in profile.items():
        if k not in _MEMORY_SKIP_KEYS and v:
            parts.append(f"{k}={v}")
    # Behavioural hints
    if tone := profile.get("dominant_tone"):
        parts.append(f"preferred_tone={tone}")
    if cmd := profile.get("favorite_command"):
        parts.append(f"favorite_command={cmd}")
    if sessions := profile.get("session_interactions"):
        parts.append(f"sessions={sessions}")
    prefs = memory.preferences
    if prefs:
        for k, v in list(prefs.items())[:3]:
            parts.append(f"{k}={v}")
    return "User profile: " + ", ".join(parts) if parts else None


def _try_llm_call(
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_text: str,
    *,
    use_api_key_header: bool = False,
) -> dict | None:
    """Single attempt at one provider; returns parsed dict or None on any failure."""
    if use_api_key_header:
        headers = {"Content-Type": "application/json", "X-API-Key": api_key}
    else:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_text},
        ],
        "temperature": 0.2,
        "max_tokens": 512,
    }
    try:
        resp = httpx.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json=body,
            timeout=30.0,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = re.sub(r"^```[a-z]*\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        return json.loads(content)
    except Exception:
        return None


def _try_provider(
    slug: str,
    system_prompt: str,
    user_text: str,
    ollama_model: str = "",
    nexus_api_key: str = "",
) -> dict | None:
    """Try a single named provider from the registry; return parsed dict or None."""
    info = _PROVIDER_REGISTRY.get(slug)
    if info is None:
        return None
    base_url, key_env, model, auth_style = info

    if slug == "ollama":
        if not ollama_model:
            return None
        key = "ollama"
        model = ollama_model
    elif slug == "pollinations":
        key = "anonymous"
    else:
        key = os.getenv(key_env, "") if key_env else ""
        if slug == "aaaa-nexus" and not key:
            key = nexus_api_key
        if not key:
            return None

    return _try_llm_call(
        base_url, key, model, system_prompt, user_text,
        use_api_key_header=(auth_style == "x-api-key"),
    )


def _call_llm(
    user_text: str,
    working_dir: Path | str | None = None,
    memory_context: str | None = None,
) -> dict | None:
    """Send user_text through the configured provider cascade; return parsed dict or None.

    Provider order is read from .ass-ade/config.json (set via `ass-ade setup`):
      llm_providers — explicit ordered list, e.g. ["aaaa-nexus", "groq", "ollama"]
      llm_priority  — legacy fallback: "nexus"|"cloud"|"local"|"free"

    Pollinations is always the silent last resort — zero config required, always available.
    """
    try:
        system_prompt = build_atomadic_intent_prompt(
            working_dir or Path.cwd(),
            memory_context=memory_context,
        )
    except Exception:
        system_prompt = _fallback_llm_system_prompt(working_dir, memory_context)

    _load_env()
    cfg = _load_interpreter_config()
    ollama_model = cfg.ollama_model
    nexus_api_key = getattr(cfg, "nexus_api_key", None) or ""

    providers: list[str] = getattr(cfg, "llm_providers", []) or []
    if not providers:
        priority = getattr(cfg, "llm_priority", "cloud")
        if priority == "free":
            providers = ["pollinations"]
        elif priority == "local":
            providers = ["ollama", "aaaa-nexus", "groq", "cerebras", "gemini",
                         "openrouter", "mistral", "github", "pollinations"]
        elif priority == "nexus":
            providers = ["aaaa-nexus", "groq", "cerebras", "gemini",
                         "openrouter", "mistral", "github", "ollama", "pollinations"]
        else:  # "cloud" (default)
            providers = ["groq", "cerebras", "gemini", "openrouter", "mistral",
                         "github", "aaaa-nexus", "ollama", "pollinations"]

    tried_pollinations = "pollinations" in providers
    for slug in providers:
        result = _try_provider(slug, system_prompt, user_text, ollama_model, nexus_api_key)
        if result is not None:
            return result

    if not tried_pollinations:
        return _try_provider("pollinations", system_prompt, user_text)
    return None

# ── Persistent local memory ───────────────────────────────────────────────────

_MEMORY_DIR = Path.home() / ".ass-ade" / "memory"
_HISTORY_MAX = 1000


@dataclass
class MemoryStore:
    """Local-only memory for the Atomadic interpreter.

    Two layers:
    - Community intelligence: learned from code quality via the LoRA flywheel (remote).
    - Personal context: learned from this user's interactions (local, never sent remotely).
    """

    user_profile: dict[str, Any] = field(default_factory=dict)
    project_contexts: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    _history_path: Path = field(init=False, repr=False)

    def __post_init__(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        self._history_path = _MEMORY_DIR / "conversation_history.jsonl"

    # ── Persistence ────────────────────────────────────────────────────────────

    @classmethod
    def load(cls) -> "MemoryStore":
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        store = cls()
        for attr, filename in [
            ("user_profile", "user_profile.json"),
            ("project_contexts", "project_contexts.json"),
            ("preferences", "preferences.json"),
        ]:
            p = _MEMORY_DIR / filename
            if p.exists():
                try:
                    setattr(store, attr, json.loads(p.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    pass
        # Prompt for name if not set
        profile = store.user_profile
        if "name" not in profile or not profile["name"].strip():
            try:
                name = input("What is your name? (for personalized greetings): ").strip()
                if name:
                    profile["name"] = name
                    store.save()
            except Exception:
                pass
        return store

    def save(self) -> None:
        _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        for attr, filename in [
            ("user_profile", "user_profile.json"),
            ("project_contexts", "project_contexts.json"),
            ("preferences", "preferences.json"),
        ]:
            p = _MEMORY_DIR / filename
            try:
                p.write_text(
                    json.dumps(getattr(self, attr), indent=2, default=str),
                    encoding="utf-8",
                )
            except OSError:
                pass

    @classmethod
    def clear(cls) -> None:
        for filename in [
            "user_profile.json", "project_contexts.json",
            "preferences.json", "conversation_history.jsonl",
        ]:
            p = _MEMORY_DIR / filename
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_profile": self.user_profile,
            "project_contexts": self.project_contexts,
            "preferences": self.preferences,
        }

    # ── History ────────────────────────────────────────────────────────────────

    def append_history(self, turn: "Turn") -> None:
        try:
            entry = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "user": turn.user,
                "intent": turn.intent,
                "tone": turn.tone,
                "path": turn.path,
                "ok": "[error" not in (turn.output or "").lower(),
            }
            lines: list[str] = []
            if self._history_path.exists():
                lines = self._history_path.read_text(encoding="utf-8").splitlines()
            lines.append(json.dumps(entry))
            lines = lines[-_HISTORY_MAX:]
            self._history_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except OSError:
            pass

    def recent_history(self, n: int = 5) -> list[dict]:
        if not self._history_path.exists():
            return []
        lines = self._history_path.read_text(encoding="utf-8").splitlines()
        results = []
        for line in reversed(lines[-n * 2:]):
            try:
                results.append(json.loads(line))
                if len(results) >= n:
                    break
            except json.JSONDecodeError:
                continue
        return list(reversed(results))

    # ── Profile learning ───────────────────────────────────────────────────────

    def update_from_turn(self, turn: "Turn") -> None:
        profile = self.user_profile
        # Tone frequency tracking
        tones = profile.setdefault("tone_counts", {})
        tones[turn.tone] = tones.get(turn.tone, 0) + 1
        # Dominant tone
        profile["dominant_tone"] = max(tones, key=lambda k: tones[k])
        # Command frequency
        cmds = profile.setdefault("command_counts", {})
        cmds[turn.intent] = cmds.get(turn.intent, 0) + 1
        profile["favorite_command"] = max(cmds, key=lambda k: cmds[k])
        # Session count
        profile["session_interactions"] = profile.get("session_interactions", 0) + 1

        # Project context
        path_key = str(Path(turn.path).resolve())
        ctx = self.project_contexts.setdefault(path_key, {})
        ctx.setdefault("first_seen", datetime.now(timezone.utc).isoformat())
        ctx["last_seen"] = datetime.now(timezone.utc).isoformat()
        intent_log = ctx.setdefault("commands_run", [])
        intent_log.append({"intent": turn.intent, "ts": datetime.now(timezone.utc).isoformat()})
        ctx["commands_run"] = intent_log[-50:]  # keep last 50 per project

    # ── Greeting ───────────────────────────────────────────────────────────────

    def greeting(self, working_dir: Path) -> str | None:
        if not self.user_profile:
            return None
        parts: list[str] = []
        tone = self.user_profile.get("dominant_tone", "formal")
        name = self.user_profile.get("name", "there")
        path_key = str(working_dir.resolve())
        ctx = self.project_contexts.get(path_key, {})
        recent = self.recent_history(3)

        if tone == TONE_CASUAL:
            parts.append(f"Hey, welcome back {name}!")
        else:
            parts.append(f"Welcome back, {name}.")

        if ctx:
            last_cmds = [e.get("intent") for e in ctx.get("commands_run", [])[-3:]]
            if last_cmds:
                last = last_cmds[-1]
                if tone == TONE_CASUAL:
                    parts.append(f"Last time here we ran `{last}` on this project.")
                else:
                    parts.append(f"Last operation on this project: `{last}`.")

        fav = self.user_profile.get("favorite_command")
        if fav and fav != "chat":
            if tone == TONE_CASUAL:
                parts.append(f"Quick tip: `{fav}` is your most-used command.")
            else:
                parts.append(f"Most-used command: `{fav}`.")

        return " ".join(parts) if parts else None

    # ── Summary ────────────────────────────────────────────────────────────────

    def summarize(self) -> str:
        if not self.user_profile and not self.project_contexts:
            return "No memory yet. Start chatting to build it up."
        lines = ["**Atomadic memory**\n"]
        if self.user_profile:
            lines.append("**You:**")
            tone = self.user_profile.get("dominant_tone", "unknown")
            lines.append(f"  - Tone: {tone}")
            fav = self.user_profile.get("favorite_command")
            if fav:
                lines.append(f"  - Favorite command: `{fav}`")
            count = self.user_profile.get("session_interactions", 0)
            lines.append(f"  - Total interactions: {count}")
        if self.project_contexts:
            lines.append("\n**Projects:**")
            for path, ctx in list(self.project_contexts.items())[-5:]:
                name = Path(path).name
                last = ctx.get("last_seen", "")[:10]
                n_cmds = len(ctx.get("commands_run", []))
                lines.append(f"  - `{name}` — last seen {last}, {n_cmds} commands run")
        return "\n".join(lines)


# ── Tone detection ─────────────────────────────────────────────────────────────

TONE_CASUAL = "casual"
TONE_FORMAL = "formal"
TONE_TECHNICAL = "technical"

_CASUAL_WORDS = {
    "hey", "hi", "yo", "lol", "haha", "umm", "pls", "plz", "thx", "thanks",
    "cool", "nice", "ok", "great", "awesome", "yeah", "yep", "nope", "wanna",
    "gonna", "gotta", "kinda", "sorta", "honestly", "btw", "fyi",
}
_TECHNICAL_SIGNALS = {
    "--", "./", "src/", "def ", "class ", "import ", "pytest", ".py",
    "json", "yaml", "toml", "git", "pip", "venv",
}


def _detect_tone(text: str) -> str:
    lower = text.lower()
    words = set(lower.split())
    casual_score = sum(1 for w in _CASUAL_WORDS if w in words)
    technical_score = sum(1 for s in _TECHNICAL_SIGNALS if s in lower)
    if technical_score >= 2:
        return TONE_TECHNICAL
    if casual_score >= 1:
        return TONE_CASUAL
    return TONE_FORMAL


# ── Intent classification ──────────────────────────────────────────────────────

_INTENT_MAP: dict[str, list[str]] = {
    "memory":   ["remember", "save that", "my name is", "call me",
                 "save to my profile", "remember that", "note that",
                 "don't forget", "my email is", "my role is", "i work as",
                 "remember me as", "save my"],
    "rebuild":  ["rebuild", "restructure", "reorganize", "refactor",
                 "tidy", "fix the mess", "sort out", "rewrite"],
    "design":   ["design", "blueprint", "plan", "spec", "propose"],
    "add-feature": ["add a tool", "add a skill", "add a feature",
                    "add skill", "add tool", "new tool", "add a web",
                    "new skill", "create a tool", "create a skill",
                    "add web", "add search", "new feature",
                    "add feature", "add tests", "add test", "add unit test",
                    "add integration test", "add coverage", "add a test",
                    "want to add tests", "need tests for"],
    "docs":     ["doc", "document", "readme", "wiki", "explain", "describe",
                 "documentation"],
    # eco-scan placed before lint so "eco-scan" keyword beats "scan" on equal score
    "eco-scan": ["eco-scan", "eco scan", "eco-scan"],
    "lint":     ["lint", "check", "scan", "audit", "quality", "issue",
                 "problem", "error", "warning", "style",
                 "bug", "bugs", "fix the bugs", "find bugs", "security issues",
                 "security problems", "vulnerabilities", "fix"],
    "certify":  ["certify", "certificate", "sign", "verify", "validate",
                 "sign off"],
    "enhance":  ["enhance", "improve", "better", "upgrade", "suggest",
                 "recommend", "optimize", "improvement", "apply all",
                 "apply enhancement", "faster", "performance", "speed up",
                 "make it faster", "make faster", "slow", "bottleneck"],
    "self-enhance": [
        "make it more colorful", "make me more colorful", "add ascii art",
        "add colors", "make it more interactive", "add progress bar",
        "add spinner", "make it more engaging", "evolve yourself",
        "upgrade yourself", "improve yourself", "enhance yourself",
        "make the cli", "make yourself",
    ],
    "clean":    ["clean up rebuild", "delete rebuild", "remove rebuild",
                 "clean rebuild", "remove backup", "delete backup",
                 "remove old folders", "clean old", "delete old builds",
                 "remove evolved", "clean rebuild", "tidy rebuild",
                 "delete old", "purge old"],
    "recon":    ["recon", "reconnaissance", "scan this", "what's in this",
                 "give me an overview", "understand this repo", "what is this",
                 "overview", "understand", "what's this"],
    "doctor":   ["doctor", "health", "status", "working", "broken",
                 "connected", "diagnose"],
    "help":     ["help", "commands", "what can you do", "what are the commands",
                 "what commands", "can you do", "what can you"],
    "chat":     ["what", "how", "who", "tell me", "explain",
                 "what is", "what are", "can you"],
}


def _classify_intent(text: str) -> str:
    lower = text.lower()
    scores: dict[str, int] = {}
    for cmd, keywords in _INTENT_MAP.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score:
            scores[cmd] = score
    return max(scores, key=lambda k: scores[k]) if scores else "chat"


# ── Path extraction ────────────────────────────────────────────────────────────

def _extract_path(text: str) -> str | None:
    patterns = [
        r'["\']([^"\']{2,})["\']',
        r'(\./\S+)',
        r'([A-Za-z]:[/\\]\S+)',
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            candidate = m.group(1).rstrip(".,;")
            if Path(candidate).exists() or candidate.startswith("./"):
                return candidate
    return None


def _substitute_datetime_tokens(path: str) -> str:
    """Replace [datetime] or {datetime} in a path with the current timestamp."""
    if "[datetime]" in path or "{datetime}" in path:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = path.replace("[datetime]", ts).replace("{datetime}", ts)
    return path


# ── Turn record ───────────────────────────────────────────────────────────────

@dataclass
class Turn:
    user: str
    tone: str
    intent: str
    path: str
    command: list[str]
    output: str
    response: str


# ── Atomadic interpreter ───────────────────────────────────────────────────────

@dataclass
class Atomadic:
    """The Atomadic interpreter — friendly front door for ASS-ADE.

    Axiom 0 (Jessica Mary Colvin): Every boundary is also a door.

    6-step pipeline: receive → extract → gap-analyze → clarify → map → construct.
    Tone-adaptive: casual input → casual reply; precise input → precise reply.
    Epistemically honest: reports real outcomes, does not fabricate success.
    """

    working_dir: Path = field(default_factory=Path.cwd)
    history: list[Turn] = field(default_factory=list)
    memory: MemoryStore = field(default_factory=MemoryStore.load)
    personality: PersonalityEngine = field(default_factory=PersonalityEngine.load)
    episodes: EpisodicStore = field(default_factory=EpisodicStore.load)
    _pending_clarification: str | None = field(default=None, init=False, repr=False)
    _clarification_ctx: dict = field(default_factory=dict, init=False, repr=False)
    # Last enhance scan results (for "apply all" conversational follow-up)
    _last_scan_results: list[dict] = field(default_factory=list, init=False, repr=False)
    _last_scan_path: str = field(default="", init=False, repr=False)
    # Design approval gate (design → review → approve → rebuild)
    _pending_design_approval: bool = field(default=False, init=False, repr=False)
    _pending_design_feature: str = field(default="", init=False, repr=False)
    # Startup scan cache and suggestion list (set by run_interactive)
    _startup_scan: dict = field(default_factory=dict, init=False, repr=False)
    _startup_suggestions: list[str] = field(default_factory=list, init=False, repr=False)
    # Skill runner (lazy-loaded on first use)
    _skill_runner: Any = field(default=None, init=False, repr=False)

    # ── Public interface ───────────────────────────────────────────────────────

    def process(self, user_input: str) -> str:
        """Run the 6-step pipeline and return the postlude response.

        Transparency output (intent, command, progress) is printed directly
        to stdout during execution so the user sees it in real time.

        Tries LLM intent derivation first; falls back to keyword heuristics
        when no LLM endpoint is reachable.
        """
        text = user_input.strip()
        if not text:
            return ""

        tone = _detect_tone(text)
        lower_text = text.lower()

        # ── Update personality signals from this message ───────────────────────
        self.personality.update_from_input(text)

        # ── Skill dispatch — checked before LLM for fast path ─────────────────
        skill_runner = self._get_skills()
        matched_skill = skill_runner.match(text)
        if matched_skill is not None:
            from ass_ade.a3_og_features.skill_runner import SkillContext
            ctx = SkillContext(
                user_input=text,
                working_dir=self.working_dir,
                tone=tone,
                domain_level=self.personality.domain_level,
                history=self.history,
            )
            print(f"\n🎯 Skill: {matched_skill.name} — {matched_skill.description}", flush=True)
            print(flush=True)
            _emit_ag_ui_tool_start(matched_skill.name, text)
            raw_skill = skill_runner.run(matched_skill, ctx)
            _emit_ag_ui_tool_result(matched_skill.name, raw_skill)
            response = self.personality.shape_response(raw_skill)
            turn = Turn(
                user=text, tone=tone, intent=f"skill:{matched_skill.name}",
                path=str(self.working_dir), command=[], output=raw_skill, response=response,
            )
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            if len(self.history) % 5 == 0:
                self.episodes.record_episode(self.working_dir.name, self.history[-5:])
            return response

        # ── Greeting intercept — project-aware, avoids generic LLM hello ─────
        _greeting_only = {"hello", "hi", "hey", "yo", "howdy", "sup", "greetings", "hiya"}
        if lower_text.rstrip("! ?,.-").strip() in _greeting_only:
            scan = self._startup_scan
            if scan:
                name = scan.get("project_name", "this project")
                files = scan.get("total_files", 0)
                sec = scan.get("security_findings", 0)
                untested = scan.get("untested_modules", 0)
                msg = f"Hey! I'm Atomadic — your AI assistant for `{name}` ({files} files)."
                if sec > 0:
                    msg += f" I see {sec} potential security finding(s) worth addressing."
                elif untested > 0:
                    msg += f" There are {untested} untested module(s) I can help cover."
                else:
                    msg += " The codebase looks healthy."
                msg += " What would you like to work on?"
            else:
                msg = "Hey! I'm Atomadic — your AI coding assistant for ASS-ADE. What would you like to work on?"
            turn = Turn(user=text, tone=tone, intent="chat", path=str(self.working_dir),
                        command=[], output="", response=msg)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return msg

        # ── Startup suggestion number dispatch ────────────────────────────────
        if self._startup_suggestions and re.fullmatch(r"[1-9]", text):
            idx = int(text) - 1
            if 0 <= idx < len(self._startup_suggestions):
                label = self._startup_suggestions[idx]
                # Translate suggestion label into a concrete user utterance and recurse
                _suggestion_intents = {
                    "Fix": "lint .",
                    "Add tests": "lint .",
                    "Consider a rebuild": "rebuild .",
                }
                mapped = next(
                    (v for k, v in _suggestion_intents.items() if label.startswith(k)),
                    label,
                )
                self._startup_suggestions = []  # consume once
                return self.process(mapped)

        # ── Design approval gate ──────────────────────────────────────────────
        if self._pending_design_approval:
            approve_words = {"yes", "add it", "create it", "build it", "apply",
                             "go", "do it", "proceed", "yep", "yeah", "sure",
                             "ok", "looks good", "create the files"}
            reject_words = {"no", "cancel", "stop", "skip", "not now", "nope",
                            "don't", "hold off"}
            words = set(lower_text.split())
            if words & approve_words or any(p in lower_text for p in
                                            ("build it", "do it", "looks good", "add it", "create it")):
                self._pending_design_approval = False
                feature = self._pending_design_feature or "feature"
                path = str(self.working_dir)
                raw_output, cmd = self._dispatch("add-feature", path, feature, tone, feature_desc=feature)
                response = self._postlude("add-feature", path, raw_output, tone)
                turn = Turn(user=text, tone=tone, intent="add-feature", path=path,
                            command=cmd, output=raw_output, response=response)
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return response
            if words & reject_words or any(p in lower_text for p in ("not now", "hold off")):
                self._pending_design_approval = False
                msg = ("Got it — blueprint saved but not applied. "
                       "Run `ass-ade rebuild` to materialize it whenever you're ready.")
                return msg

        # ── Design — intercept before LLM ("documentation" in text fools LLM into docs) ──
        _design_triggers = (
            "design a ", "design an ", "blueprint for", "create a spec",
            "create a blueprint", "spec for a", "plan a new", "design the",
        )
        if any(t in lower_text for t in _design_triggers):
            feature = self._extract_feature_desc(text) or text.strip()
            self._pending_design_feature = feature
            path = str(self.working_dir)
            cmd = self._build_command("design", path, text, feature_desc=feature)
            self._print_dispatch("design", cmd)
            prelude = self._prelude("design", path, tone)
            print(prelude, flush=True)
            print(flush=True)
            raw_output = self._execute(cmd)
            self._pending_design_approval = True
            response = self._postlude("design", path, raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="design", path=path,
                        command=cmd, output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Show architecture — intercept before LLM (avoids silent doc generation) ──
        _show_arch_triggers = (
            "show me the architecture", "show the architecture", "show architecture",
            "view architecture", "display architecture", "what is the architecture",
            "show the structure", "show structure", "show tiers", "show tier structure",
            "display tiers", "show the tier", "print architecture", "list the tiers",
            "what are the tiers", "explain the architecture", "describe the architecture",
        )
        if any(t in lower_text for t in _show_arch_triggers):
            arch_file = self.working_dir / "ARCHITECTURE.md"
            if arch_file.exists():
                content = arch_file.read_text(encoding="utf-8")
                raw_output = content[:3000] + ("\n...(truncated)" if len(content) > 3000 else "")
            else:
                raw_output = (
                    "No ARCHITECTURE.md found. Run `ass-ade eco-scan` to inspect tier "
                    "structure, or `ass-ade docs` to generate one."
                )
            turn = Turn(user=text, tone=tone, intent="chat", path=str(self.working_dir),
                        command=[], output=raw_output, response=raw_output)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return raw_output

        # ── Clean — intercept before LLM (LLM sees "rebuild" and misroutes) ──
        _clean_triggers = (
            "clean up rebuild", "clean up old", "delete rebuild", "remove rebuild",
            "clean rebuild", "remove backup", "delete backup", "remove old",
            "clean old", "delete old builds", "remove evolved", "tidy rebuild",
            "delete old", "purge old", "clean up old rebuild", "clean up folders",
        )
        if any(t in lower_text for t in _clean_triggers):
            raw_output, _cmd = self._dispatch("clean", str(self.working_dir), text, tone)
            response = self._postlude("clean", str(self.working_dir), raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="clean", path=str(self.working_dir),
                        command=[], output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Recon — intercept before LLM ("scan" misroutes to lint) ──
        _recon_triggers = (
            "scan this project", "scan this repo", "scan this codebase",
            "give me an overview", "what's in this", "what is in this",
            "understand this repo", "understand this project", "what is this project",
            "overview of this", "recon this", "survey this",
        )
        if any(t in lower_text for t in _recon_triggers):
            raw_output, cmd = self._dispatch("recon", str(self.working_dir), text, tone)
            response = self._postlude("recon", str(self.working_dir), raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="recon", path=str(self.working_dir),
                        command=cmd, output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Security scan — intercept before LLM (LLM returns generic chat advice) ──
        _security_triggers = (
            "security issue", "security problem", "vulnerabilit",
            "security scan", "what security", "security audit",
            "security risk", "security finding", "check security",
            "find security", "security check",
        )
        if any(t in lower_text for t in _security_triggers):
            raw_output, cmd = self._dispatch("enhance", str(self.working_dir), text, tone)
            response = self._postlude("enhance", str(self.working_dir), raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="enhance", path=str(self.working_dir),
                        command=cmd, output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Add-feature — intercept before LLM (LLM doesn't know this intent) ──
        _add_feature_triggers = (
            "add a tool", "add a skill", "add a feature", "new tool",
            "new skill", "create a tool", "create a skill",
            "add web search", "add search tool", "new feature",
            "add feature", "add a web", "add an ", "create a new",
            # broader patterns: "add a [noun]" not already covered
            "add a health", "add a cache", "add a queue", "add a worker",
            "add a middleware", "add a plugin", "add a module", "add a service",
            "add a command", "add a route", "add a endpoint", "add an endpoint",
            "add a handler", "add a validator", "add a parser", "add a client",
            # test coverage
            "add tests", "add test", "add unit test", "add integration test",
            "want to add tests", "need tests for", "add coverage",
        )
        if any(t in lower_text for t in _add_feature_triggers):
            feature = self._extract_feature_desc(text) or text.strip()
            raw_output, cmd = self._dispatch(
                "add-feature", str(self.working_dir), text, tone, feature_desc=feature
            )
            response = self._postlude("add-feature", str(self.working_dir), raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="add-feature",
                        path=str(self.working_dir), command=cmd,
                        output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Memory save — intercept before LLM (LLM doesn't know this intent) ──
        _memory_triggers = (
            "remember my", "remember i ", "remember that", "remember me as",
            "save that", "my name is", "call me ",
            "my email is", "my role is", "i'm a ",
            "i am a ", "i work as", "note that",
            "don't forget", "save my", "i prefer ",
        )
        if any(t in lower_text for t in _memory_triggers):
            raw_output, _cmd = self._dispatch("memory", str(self.working_dir), text, tone)
            response = self._postlude("memory", str(self.working_dir), raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="memory", path=str(self.working_dir),
                        command=[], output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── Enhance apply-all conversational shortcut ─────────────────────────
        enhance_apply_ids = self._parse_enhance_apply(lower_text)
        if enhance_apply_ids is not None:
            path = self._last_scan_path or str(self.working_dir)
            ids_str = ",".join(str(i) for i in enhance_apply_ids)
            cmd = [sys.executable, "-m", "ass_ade", "enhance", path, "--apply", ids_str]
            self._print_dispatch("enhance", cmd)
            print(f"Applying {len(enhance_apply_ids)} enhancement(s): {ids_str}", flush=True)
            print(flush=True)
            raw_output = self._execute(cmd)
            response = self._postlude("enhance", path, raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="enhance", path=path,
                        command=cmd, output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response

        # ── LLM-first path ────────────────────────────────────────────────────
        llm_result = _call_llm(text, self.working_dir, _summarize_memory(self.memory))
        if llm_result is not None:
            if llm_result.get("type") == "chat":
                reply = llm_result.get("response", "")
                turn = Turn(
                    user=text, tone=tone, intent="chat",
                    path=str(self.working_dir), command=[],
                    output="", response=reply,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return reply

            if llm_result.get("type") == "command":
                intent = llm_result.get("intent", "chat")
                cli_args = llm_result.get("cli_args")
                path = _substitute_datetime_tokens(
                    llm_result.get("path") or _extract_path(text) or str(self.working_dir)
                )
                output_path_raw = llm_result.get("output_path")
                output_path = _substitute_datetime_tokens(output_path_raw) if output_path_raw else None
                feature_desc = llm_result.get("feature_desc")

                # Safety: rebuild is destructive — require explicit trigger in input.
                # LLMs sometimes misclassify vague phrases ("make it faster", "fix the
                # bugs") as rebuild. Reclassify to a safer intent when no explicit
                # restructuring verb is present.
                if intent == "rebuild":
                    _rebuild_words = {
                        "rebuild", "restructure", "reorganize", "rewrite",
                        "overhaul", "refactor", "tidy", "sort out",
                    }
                    if not any(w in lower_text for w in _rebuild_words):
                        lower_t2 = lower_text
                        if any(w in lower_t2 for w in {
                            "bug", "fix", "broken", "wrong", "issue", "error", "crash"
                        }):
                            intent = "lint"
                        elif any(w in lower_t2 for w in {
                            "faster", "speed", "better", "improve", "optimize", "performance"
                        }):
                            intent = "enhance"
                        else:
                            intent = "chat"

                # Rebuild clarification guard applies on the LLM path too.
                if intent == "rebuild" and path == str(self.working_dir) and not self.history:
                    print(f"\n🧠 Intent: rebuild", flush=True)
                    print(flush=True)
                    self._pending_clarification = "path"
                    self._clarification_ctx = {"intent": intent}
                    return self._ask_clarification(tone)

                if intent == "cli" and isinstance(cli_args, list):
                    raw_output, cmd = self._dispatch_cli_args(cli_args, tone)
                    response_intent = "cli"
                else:
                    raw_output, cmd = self._dispatch(intent, path, text, tone, feature_desc, output_path)
                    response_intent = intent
                response = self._postlude(response_intent, path, raw_output, tone)
                turn = Turn(
                    user=text, tone=tone, intent=response_intent, path=path,
                    command=cmd, output=raw_output, response=response,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return response

        # ── Keyword-heuristic fallback (no LLM available) ─────────────────────
        path = _substitute_datetime_tokens(_extract_path(text) or str(self.working_dir))

        if self._pending_clarification:
            intent = self._clarification_ctx.get("intent", _classify_intent(text))
            new_path = _extract_path(text)
            if new_path:
                path = _substitute_datetime_tokens(new_path)
            elif text not in {"", ".", "here"}:
                path = _substitute_datetime_tokens(text.strip().strip("\"'")) or path
            self._pending_clarification = None
            self._clarification_ctx = {}
        else:
            lower_t = text.lower().strip()
            if lower_t in {"help", "?", "commands"} or any(
                p in lower_t for p in (
                    "what commands", "what can you", "what do you do",
                    "commands available", "show commands", "capabilities",
                )
            ):
                intent = "help"
            else:
                intent = _classify_intent(text)

        if intent == "rebuild" and path == str(self.working_dir) and not self.history:
            print(f"\n🧠 Intent: rebuild", flush=True)
            print(flush=True)
            self._pending_clarification = "path"
            self._clarification_ctx = {"intent": intent}
            return self._ask_clarification(tone)

        raw_output, cmd = self._dispatch(intent, path, text, tone)
        response = self._postlude(intent, path, raw_output, tone)
        response = self.personality.shape_response(response)

        turn = Turn(
            user=text, tone=tone, intent=intent, path=path,
            command=cmd, output=raw_output, response=response,
        )
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        # Record an episode every 5 meaningful turns
        if len(self.history) % 5 == 0 and intent not in ("chat", "help"):
            self.episodes.record_episode(self.working_dir.name, self.history[-5:])
        return response

    def _dispatch(
        self,
        intent: str,
        path: str,
        raw: str,
        tone: str,
        feature_desc: str | None = None,
        output_path: str | None = None,
    ) -> tuple[str, list[str]]:
        """Dispatch the intent to the right execution path.

        Returns (raw_output, cmd_used).
        Prints transparency header and prelude directly to stdout.
        """
        if intent == "memory":
            print(f"\n🧠 Intent: memory")
            print("🔧 Saving to local profile", flush=True)
            print(flush=True)
            return self._execute_memory_save(raw, tone), []

        if intent == "rebuild":
            input_p = Path(path).resolve()
            if not output_path:
                ts = datetime.now().strftime("%Y%m%d-%H%M%S")
                output_path = str(input_p.parent / f"{input_p.name}-rebuilt-{ts}")
            else:
                # Ensure output is always a SIBLING of source — never nested inside it
                out_p = Path(output_path)
                if not out_p.is_absolute():
                    output_path = str(input_p.parent / out_p.name)
                else:
                    out_resolved = out_p.resolve()
                    if str(out_resolved).startswith(str(input_p) + os.sep):
                        output_path = str(input_p.parent / out_resolved.name)
            prelude = self._prelude(intent, path, tone)
            print(prelude, flush=True)
            raw_output = self._execute_rebuild_pipeline(path, output_path)
            return raw_output, []

        if intent == "self-enhance":
            feature = feature_desc or self._extract_feature_desc(raw) or raw.strip()
            raw_output = self._execute_self_enhance(feature, tone)
            return raw_output, []

        if intent == "add-feature":
            feature = feature_desc or self._extract_feature_desc(raw) or raw.strip()
            raw_output = self._execute_add_feature(feature, path, tone)
            return raw_output, []

        if intent == "clean":
            return self._execute_clean(path, tone), []

        if intent == "help":
            return self.describe_self(), []

        if intent == "design":
            feature = feature_desc or self._extract_feature_desc(raw) or "feature"
            self._pending_design_feature = feature
            # Use working_dir as path if the extracted path doesn't exist
            design_path = path if Path(path).exists() else str(self.working_dir)
            cmd = self._build_command("design", design_path, raw, feature_desc=feature, output_path=output_path)
            self._print_dispatch(intent, cmd)
            prelude = self._prelude(intent, design_path, tone)
            print(prelude, flush=True)
            print(flush=True)
            raw_output = self._execute(cmd)
            # Set approval gate — don't auto-rebuild after design
            self._pending_design_approval = True
            return raw_output, cmd

        if intent == "enhance" and not output_path:
            # Run scan and cache results for conversational "apply all" follow-up
            cmd = self._build_command(intent, path, raw, feature_desc=feature_desc)
            self._print_dispatch(intent, cmd)
            prelude = self._prelude(intent, path, tone)
            print(prelude, flush=True)
            print(flush=True)
            raw_output = self._execute(cmd)
            self._last_scan_path = path
            # Parse finding IDs from output for later "apply all"
            self._last_scan_results = _parse_findings_from_output(raw_output)
            return raw_output, cmd

        cmd = self._build_command(intent, path, raw, feature_desc=feature_desc, output_path=output_path)
        self._print_dispatch(intent, cmd)
        prelude = self._prelude(intent, path, tone)
        print(prelude, flush=True)
        print(flush=True)
        raw_output = self._execute(cmd)
        return raw_output, cmd

    def _dispatch_cli_args(self, cli_args: list[Any], tone: str) -> tuple[str, list[str]]:
        """Dispatch an exact ASS-ADE CLI command path chosen from the dynamic inventory."""
        args = [str(item).strip() for item in cli_args if str(item).strip()]
        if not args:
            return "[error] No CLI arguments were provided.", []
        if args[0] == "chat":
            return "[error] `chat` is already running; ask for help instead.", []
        if not command_path_exists(args, self.working_dir):
            return f"[error] Unknown ASS-ADE command path: {' '.join(args)}", []

        cmd = [sys.executable, "-m", "ass_ade", *args]
        self._print_dispatch("cli", cmd)
        prelude = (
            "Running the requested ASS-ADE command..."
            if tone != TONE_CASUAL
            else "On it - running that ASS-ADE command..."
        )
        print(prelude, flush=True)
        print(flush=True)
        return self._execute(cmd), cmd

    def _execute_self_enhance(self, feature_desc: str, tone: str) -> str:
        """Live self-enhancement: design → rebuild → hot-patch → visual flicker."""
        import time as _time

        source = str(self.working_dir.resolve())
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = str(self.working_dir.parent / f"{self.working_dir.name}-evolved-{ts}")
        base = [sys.executable, "-m", "ass_ade"]

        print(f"\n🧠 Intent: self-enhance")
        print(f"📋 Feature: {feature_desc}")
        print(f"⚡ Starting live evolution pipeline...", flush=True)
        print()

        # Step 1: Generate design blueprint
        print("⏳ Step 1/3: Generating design blueprint...", flush=True)
        rc = self._run_streaming(
            base + ["design", feature_desc, "--path", source]
        )
        if rc != 0:
            print(f"⚠️  Blueprint generation had warnings (continuing)", flush=True)
        else:
            print(f"✅ Blueprint generated", flush=True)

        # Step 2: Run rebuild pipeline
        print("\n⏳ Step 2/3: Rebuilding with blueprint applied...", flush=True)
        rebuild_output = self._execute_rebuild_pipeline(source, output_path)
        rebuild_ok = "[ok]" in rebuild_output

        # Step 3: Visual flicker transition
        print("\n⏳ Step 3/3: Hot-patching and evolving...", flush=True)
        _time.sleep(0.3)

        # Clear screen and show evolution animation
        try:
            print("\033[2J\033[H", end="", flush=True)  # clear screen
        except Exception:
            print("\n" * 3, flush=True)

        frames = ["⚡ Evolving.", "⚡ Evolving..", "⚡ Evolving...", "⚡ ⚡ Evolving..."]
        for frame in frames:
            print(f"\r{frame}   ", end="", flush=True)
            _time.sleep(0.25)
        print(flush=True)

        # Hot-patch
        patched = self._hot_patch()

        try:
            print("\033[2J\033[H", end="", flush=True)
        except Exception:
            print("\n" * 2, flush=True)

        if rebuild_ok:
            print(f"✅ Evolution complete.", flush=True)
            if patched:
                print(f"⚡ Hot-patched: {', '.join(patched[:5])}", flush=True)
            print(f"📁 New build: {output_path}", flush=True)
            return f"[ok] Done. The CLI just evolved. Feature applied: {feature_desc}"
        else:
            print(f"⚠️  Evolution had issues — check output above.", flush=True)
            return f"[ok] Evolution attempted with warnings. Feature: {feature_desc}. Check output folder: {output_path}"

    def describe_self(self) -> str:
        try:
            base = render_atomadic_help(self.working_dir)
        except Exception:
            base = (
                "I'm Atomadic, the front door of ASS-ADE.\n\n"
                "I can rebuild, design, document, lint, certify, enhance, scan, "
                "and evolve codebases. Just tell me what you want in plain English."
            )
        # Append skills summary
        try:
            skill_runner = self._get_skills()
            skills = skill_runner.list_skills()
            if skills:
                skill_lines = ["\n\n**Built-in Skills** (auto-activated by keyword):"]
                for s in skills:
                    skill_lines.append(f"  `{s['name']}` — {s['description']}")
                skill_lines.append("\nType `@skills` to list them, `@persona <mode>` to switch personality.")
                base += "\n".join(skill_lines)
        except Exception:
            pass
        return base

    def _get_skills(self) -> Any:
        """Lazy-load the SkillRunner for this working directory."""
        if self._skill_runner is None:
            from ass_ade.a3_og_features.skill_runner import SkillRunner
            self._skill_runner = SkillRunner(self.working_dir)
        return self._skill_runner

    # ── Internals ──────────────────────────────────────────────────────────────

    def _build_command(
        self, intent: str, path: str, raw: str,
        feature_desc: str | None = None, output_path: str | None = None,
    ) -> list[str]:
        base = [sys.executable, "-m", "ass_ade"]
        if intent == "rebuild":
            # Handled by _execute_rebuild_pipeline; return empty sentinel.
            return []
        if intent == "design":
            feature = feature_desc or self._extract_feature_desc(raw) or "feature"
            return base + ["design", feature, "--path", path]
        if intent == "docs":
            return base + ["docs", path]
        if intent == "lint":
            return base + ["lint", path]
        if intent == "certify":
            return base + ["certify", path]
        if intent == "enhance":
            return base + ["enhance", path]
        if intent == "eco-scan":
            return base + ["eco-scan", path]
        if intent == "recon":
            return base + ["recon", path]
        if intent == "doctor":
            return base + ["doctor"]
        if intent in ("help", "memory", "add-feature", "clean"):
            return []  # handled inline in _dispatch
        # "chat" intent with no LLM available — describe self
        return base + ["doctor"]

    def _print_dispatch(self, intent: str, cmd: list[str]) -> None:
        display_args = cmd[3:] if len(cmd) > 3 else []
        cmd_str = "ass-ade " + " ".join(str(a) for a in display_args)
        print(f"\n🧠 Intent: {intent}")
        print(f"🔧 Dispatching: {cmd_str}")
        print(flush=True)

    def _run_streaming(self, cmd: list[str]) -> int:
        """Stream subprocess output to stdout; return exit code."""
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                cwd=str(self.working_dir),
            )
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end="", flush=True)
            proc.wait(timeout=120)
            return proc.returncode or 0
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except Exception:
                pass
            print("[timed out after 120s — killed]", flush=True)
            return -1
        except Exception as exc:
            print(f"[execution error: {exc}]", flush=True)
            return -1

    def _execute(self, cmd: list[str]) -> str:
        """Run a single command, streaming output live; return collected output."""
        output_parts: list[str] = []
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                cwd=str(self.working_dir),
            )
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end="", flush=True)
                    output_parts.append(line)
            proc.wait(timeout=120)
            output = "".join(output_parts).strip()
            if proc.returncode != 0:
                return f"[error] exit {proc.returncode}\n{output}"
            return output
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except Exception:
                pass
            return "[error timed out after 120s]"
        except Exception as exc:
            return f"[execution error: {exc}]"

    def _execute_rebuild_pipeline(self, source: str, output: str) -> str:
        """Built-in rebuild pipeline: backup → copy → recon → lint → docs → certify → hot-patch."""
        import shutil as _shutil

        source_path = Path(source).resolve()
        output_path = Path(output).resolve()
        base = [sys.executable, "-m", "ass_ade"]

        # Safety: block in-place rebuild
        if source_path == output_path:
            return "[error] Source and output are the same path — in-place rebuild blocked for safety."

        print(f"\n🧠 Intent: rebuild")
        print(f"🔧 Dispatching: rebuild pipeline (5 phases)")
        print(f"   Source : {source_path}")
        print(f"   Output : {output_path}")
        print(flush=True)

        # Phase 0 — auto-backup
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = source_path.parent / f"{source_path.name}-backup-{ts}"
        suffix = 0
        while backup_path.exists():
            suffix += 1
            backup_path = source_path.parent / f"{source_path.name}-backup-{ts}-{suffix}"
        print(f"🛡️  Backup : {backup_path}")
        try:
            _shutil.copytree(str(source_path), str(backup_path))
            print(f"✅ Backup complete ({backup_path.name})", flush=True)
        except Exception as exc:
            return f"[error] Backup failed: {exc} — rebuild aborted for safety."

        # Phase 1 — copy source to output
        print(f"\n⏳ Phase 1/5: Copying source to output folder...", flush=True)
        try:
            if output_path.exists():
                _shutil.rmtree(output_path)
            _shutil.copytree(str(source_path), str(output_path))
            file_count = sum(1 for f in output_path.rglob("*") if f.is_file())
            print(f"✅ Copied {file_count} files → {output_path.name}", flush=True)
        except OSError as exc:
            print(f"[error] Copy failed: {exc}", flush=True)
            return (
                f"[error] Copy failed (disk full?): {exc}\n"
                f"Backup preserved at: {backup_path}"
            )
        except Exception as exc:
            return f"[error] Copy failed: {exc}"

        out_str = str(output_path)
        warnings: list[str] = []

        phases = [
            ("Recon",   ["recon",   out_str]),
            ("Lint",    ["lint",    out_str]),
            ("Docs",    ["docs",    out_str]),
            ("Certify", ["certify", out_str]),
        ]
        for idx, (label, args) in enumerate(phases, start=2):
            print(f"\n⏳ Phase {idx}/5: {label}...", flush=True)
            rc = self._run_streaming(base + args)
            if rc != 0:
                print(f"⚠️  {label} completed with warnings (exit {rc})", flush=True)
                warnings.append(label)
            else:
                print(f"✅ {label} done", flush=True)

        # Verify output is non-empty
        output_file_count = sum(1 for f in output_path.rglob("*") if f.is_file()) if output_path.exists() else 0
        if output_file_count == 0:
            failure_msg = "Rebuild produced empty output."
            print(f"\n❌ {failure_msg}", flush=True)
            log_path = source_path / "REBUILD_FAILURE.log"
            try:
                log_path.write_text(
                    f"{failure_msg}\nTimestamp: {ts}\nWarning phases: {warnings}\n",
                    encoding="utf-8",
                )
            except OSError:
                pass
            print(f"🔄 Rolling back to backup {backup_path.name}...", flush=True)
            self._rollback(output_path, backup_path)
            return f"[error] {failure_msg} Restored from backup: {backup_path}"

        # Hot-patch: reload updated modules immediately
        print(f"\n⚡ Hot-patching updated modules...", flush=True)
        patched = self._hot_patch()
        if patched:
            print(f"✅ Hot-patched: {', '.join(patched)}", flush=True)

        print(flush=True)
        result_tag = "[ok] All 5 phases complete" if not warnings else f"[ok] Pipeline complete — warnings in: {', '.join(warnings)}"
        return f"{result_tag}\nOutput : {output_path}\nBackup : {backup_path}"

    def _rollback(self, output_path: Path, backup_path: Path) -> None:
        """Restore output_path from backup after a failed rebuild."""
        import shutil as _shutil
        try:
            if output_path.exists():
                _shutil.rmtree(output_path)
            if backup_path.exists():
                _shutil.copytree(str(backup_path), str(output_path))
                print(f"✅ Restored from backup: {backup_path.name}", flush=True)
            else:
                print(f"⚠️  Backup not found at {backup_path} — manual restore required", flush=True)
        except Exception as exc:
            print(f"❌ Rollback failed: {exc} — restore manually from {backup_path}", flush=True)

    def _hot_patch(self) -> list[str]:
        """Reload ASS-ADE Python modules in-place after a rebuild."""
        import importlib as _il
        import sys as _sys
        patched: list[str] = []
        for name in list(_sys.modules.keys()):
            if name.startswith("ass_ade") and "interpreter" not in name:
                mod = _sys.modules.get(name)
                if mod is None:
                    continue
                try:
                    _il.reload(mod)
                    patched.append(name)
                except (ImportError, SyntaxError, Exception):
                    pass  # keep old module loaded
        return patched

    def _extract_feature_desc(self, text: str) -> str | None:
        patterns = [
            r'"([^"]{4,})"',
            r"'([^']{4,})'",
            # "called X" / "named X" — extract just the name, strip English preamble
            r'(?:called|named)\s+([a-zA-Z0-9_][a-zA-Z0-9_\- ]{1,39})',
            r'(?:design|feature|implement|add|create|build|make)\s+(?:a\s+|an\s+|the\s+)?(.+)',
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()[:200]
        return None

    # ── Memory save ────────────────────────────────────────────────────────────

    def _execute_memory_save(self, text: str, tone: str) -> str:
        """Extract key/value from text and persist to user_profile."""
        pairs = self._extract_memory_kv(text)
        if not pairs:
            # Generic save — store the raw note
            pairs = {"note": text.strip()}
        profile = self.memory.user_profile
        for key, value in pairs.items():
            profile[key] = value
        self.memory.save()
        saved = ", ".join(f"{k}={v!r}" for k, v in pairs.items())
        if tone == TONE_CASUAL:
            return f"Got it! Saved to your profile: {saved}"
        return f"Saved to local profile: {saved}"

    def _extract_memory_kv(self, text: str) -> dict[str, str]:
        """Extract structured key/value from a memory-save utterance."""
        pairs: dict[str, str] = {}
        patterns = [
            (r"my name is ([^\.,\n]+)", "name"),
            (r"call me ([^\.,\n]+)", "name"),
            (r"remember me as ([^\.,\n]+)", "name"),
            (r"my email (?:is|:) ([^\.,\n]+)", "email"),
            (r"my role (?:is|:) ([^\.,\n]+)", "role"),
            (r"i(?:'m| am) a ([^\.,\n]+)", "role"),
            (r"i work as ([^\.,\n]+)", "role"),
            (r"remember that (.+)", "note"),
            (r"note that (.+)", "note"),
            (r"save that (.+)", "note"),
            (r"don't forget (?:that )?(.+)", "note"),
        ]
        for pattern, key in patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                pairs[key] = m.group(1).strip().rstrip(".")
        return pairs

    # ── Enhance apply-all parsing ───────────────────────────────────────────────

    def _parse_enhance_apply(self, lower: str) -> list[int] | None:
        """Return a list of finding IDs if user is asking to apply enhancements conversationally."""
        has_last = bool(self._last_scan_results)
        # "apply all" / "enhance all" / "apply all enhancements"
        if re.search(r"\b(apply|use)\s+all\b", lower) or re.search(r"\bapply\s+all\s+enhancements?\b", lower):
            if has_last:
                return [f.get("id", i + 1) for i, f in enumerate(self._last_scan_results)]
            return None
        # "enhance all 20" / "apply all 20"
        m = re.search(r"\b(?:apply|enhance)\s+all\s+(\d+)\b", lower)
        if m:
            n = int(m.group(1))
            if has_last:
                ids = [f.get("id", i + 1) for i, f in enumerate(self._last_scan_results)]
                return ids[:n]
            return list(range(1, n + 1))
        # "enhance 1-5" / "apply 1-5"
        m = re.search(r"\b(?:apply|enhance)\s+(\d+)\s*[-–]\s*(\d+)\b", lower)
        if m:
            start, end = int(m.group(1)), int(m.group(2))
            return list(range(start, end + 1))
        # "apply 1,3,5" / "enhance 1, 3, 5"
        m = re.search(r"\b(?:apply|enhance)\s+([\d][\d\s,]+)\b", lower)
        if m:
            nums = [int(n) for n in re.findall(r"\d+", m.group(1))]
            return nums if nums else None
        # "apply the security ones" — filter by category if we have scan results
        m = re.search(r"\bapply\s+(?:the\s+)?(\w+)\s+ones?\b", lower)
        if m and has_last:
            cat = m.group(1).lower()
            matched = [f.get("id", i + 1) for i, f in enumerate(self._last_scan_results)
                       if cat in f.get("category", "").lower()]
            return matched if matched else None
        return None

    # ── Add feature in-place ───────────────────────────────────────────────────

    def _execute_add_feature(self, feature_desc: str, path: str, tone: str) -> str:
        """Targeted in-place feature addition: design → create tier files → update imports.

        Creates files directly in the workspace tier folders.
        Does NOT copy the project or create a new output directory.
        """
        base = [sys.executable, "-m", "ass_ade"]
        source = Path(path).resolve()

        print(f"\n🧠 Intent: add-feature")
        print(f"📋 Feature: {feature_desc}")
        print(f"⚡ Targeted in-place addition — no full rebuild", flush=True)
        print(flush=True)

        # Step 1: Generate design blueprint
        print("⏳ Step 1/2: Generating blueprint...", flush=True)
        rc = self._run_streaming(base + ["design", feature_desc, "--path", str(source)])
        if rc != 0:
            print("⚠️  Blueprint had warnings (continuing)", flush=True)
        else:
            print("✅ Blueprint generated", flush=True)

        # Step 2: Create skeleton files in tier folders inside source
        print("\n⏳ Step 2/2: Creating feature skeleton in tier folders...", flush=True)
        created = self._create_tier_feature_skeleton(feature_desc, source)

        if created:
            print(f"✅ Created {len(created)} file(s):", flush=True)
            for f in created:
                print(f"   {f}", flush=True)
            return f"[ok] Feature '{feature_desc}' added in-place.\nCreated: {', '.join(created)}"
        return f"[ok] Blueprint generated for '{feature_desc}'. Review blueprint JSON for the full file plan."

    def _create_tier_feature_skeleton(self, feature_desc: str, source: Path) -> list[str]:
        """Create skeleton files in the correct monadic tier folders inside source."""
        slug = re.sub(r"[^a-z0-9]+", "_", feature_desc.lower()).strip("_")[:40]
        created: list[str] = []

        def _find_tier(prefix: str) -> Path | None:
            """Find a tier directory by prefix, checking root then up to 4 levels deep."""
            for d in sorted(source.glob("a?_*")):
                if d.is_dir() and prefix in d.name:
                    return d
            for depth in range(1, 5):
                pattern = "/".join(["*"] * depth) + "/a?_*"
                for d in sorted(source.glob(pattern)):
                    if d.is_dir() and prefix in d.name:
                        return d
            return None

        at_tier = _find_tier("at_") or _find_tier("a1_")
        mo_tier = _find_tier("mo_") or _find_tier("a2_")

        def _write(fpath: Path, content: str) -> str:
            fpath.parent.mkdir(parents=True, exist_ok=True)
            if not fpath.exists():
                fpath.write_text(content, encoding="utf-8")
            return str(fpath.relative_to(source))

        if at_tier:
            fname = at_tier / f"at_{slug}.py"
            body = (
                f'"""AT-tier function: {feature_desc}."""\n'
                f"from __future__ import annotations\n\n\n"
                f"def {slug}(*args, **kwargs):\n"
                f'    """Stub for {feature_desc}."""\n'
                f"    raise NotImplementedError\n"
            )
            created.append(_write(fname, body))
            # Update tier __init__.py
            init_p = at_tier / "__init__.py"
            if init_p.exists():
                existing = init_p.read_text(encoding="utf-8")
                line = f"from .at_{slug} import {slug}"
                if line not in existing:
                    init_p.write_text(existing.rstrip() + f"\n{line}\n", encoding="utf-8")
            else:
                init_p.write_text(f"from .at_{slug} import {slug}\n", encoding="utf-8")
                created.append(str(init_p.relative_to(source)))

        if mo_tier:
            fname = mo_tier / f"mo_{slug}_pipeline.py"
            body = (
                f'"""MO-tier composite: {feature_desc} pipeline."""\n'
                f"from __future__ import annotations\n\n\n"
                f"def run_{slug}_pipeline(*args, **kwargs):\n"
                f'    """Stub pipeline for {feature_desc}."""\n'
                f"    raise NotImplementedError\n"
            )
            created.append(_write(fname, body))

        if not at_tier and not mo_tier:
            # Fallback: create in source/tools/
            tools = source / "tools"
            tools.mkdir(exist_ok=True)
            fname = tools / f"{slug}.py"
            body = (
                f'"""Tool: {feature_desc}."""\n'
                f"from __future__ import annotations\n\n\n"
                f"def {slug}(*args, **kwargs):\n"
                f'    """Stub for {feature_desc}."""\n'
                f"    raise NotImplementedError\n"
            )
            created.append(_write(fname, body))

        return created

    # ── Clean auto-generated folders ────────────────────────────────────────────

    def _execute_clean(self, path: str, tone: str) -> str:
        """Scan parent directory for auto-generated rebuild/backup folders and list them."""
        source = Path(path).resolve()
        parent = source.parent
        patterns = ("-rebuilt-", "-backup-", "-evolved-")
        found = [d for d in parent.iterdir() if d.is_dir() and any(p in d.name for p in patterns)]
        if not found:
            msg = "No auto-generated rebuild, backup, or evolved folders found."
            return msg
        lines = [f"Found {len(found)} auto-generated folder(s) in {parent}:\n"]
        for d in found:
            try:
                size_mb = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / 1_048_576
                lines.append(f"  {d.name}  ({size_mb:.1f} MB)")
            except OSError:
                lines.append(f"  {d.name}")
        lines.append("")
        lines.append("To delete, run:  ass-ade memory clear  (not auto-deleted)")
        lines.append("Or delete manually with:  rmdir /s /q \"<folder>\"  (Windows)")
        self._last_scan_results = [{"id": i + 1, "path": str(d)} for i, d in enumerate(found)]
        return "\n".join(lines)

    def _ask_clarification(self, tone: str) -> str:
        cwd_name = self.working_dir.name or str(self.working_dir)
        if tone == TONE_CASUAL:
            return f"Sure! Rebuilding `{cwd_name}` — hit Enter to confirm, or type a different path."
        return f"Rebuilding `{cwd_name}`. Press Enter to confirm, or provide a different path."

    def _prelude(self, intent: str, path: str, tone: str) -> str:
        label = Path(path).name or path
        casual = {
            "rebuild":     f"On it! Rebuilding `{label}` into clean tiers...",
            "design":      "Let me sketch that blueprint for you...",
            "docs":        f"Generating docs for `{label}`...",
            "lint":        f"Running lint on `{label}`...",
            "certify":     f"Certifying `{label}`...",
            "enhance":     f"Looking for improvements in `{label}`...",
            "eco-scan":    f"Scanning `{label}` — getting the lay of the land...",
            "recon":       f"Running parallel recon on `{label}` — 5 agents, no LLM...",
            "doctor":      "Checking everything's connected and healthy...",
            "self-enhance": "Time to evolve. Generating blueprint, rebuilding, and hot-patching...",
            "add-feature": "Adding that feature in-place — no full rebuild needed...",
            "memory":      "Got it, saving that to your profile...",
            "clean":       "Scanning for auto-generated folders...",
            "help":        "Here's everything I can do:",
            "chat":        "Let me look into that...",
        }
        formal = {
            "rebuild":     f"Initiating rebuild of `{label}` into the 5-tier monadic layout.",
            "design":      "Generating an AAAA-SPEC-004 blueprint.",
            "docs":        f"Generating documentation for `{label}`.",
            "lint":        f"Running the CIE lint pipeline on `{label}`.",
            "certify":     f"Running the certification pipeline on `{label}`.",
            "enhance":     f"Scanning `{label}` for enhancement opportunities.",
            "eco-scan":    f"Running monadic compliance check on `{label}`.",
            "recon":       f"Running parallel reconnaissance on `{label}` (Scout, Dependency, Tier, Test, Doc).",
            "doctor":      "Running self-diagnostics.",
            "self-enhance": "Initiating live self-enhancement: design → rebuild → hot-patch.",
            "add-feature": "Creating targeted feature files in-place.",
            "memory":      "Saving to local profile.",
            "clean":       "Scanning for auto-generated output folders.",
            "help":        "Available commands:",
            "chat":        "Processing your request.",
        }
        pool = casual if tone == TONE_CASUAL else formal
        return pool.get(intent, pool["chat"])

    def _postlude(self, intent: str, path: str, output: str, tone: str) -> str:
        label = Path(path).name or path
        failed = (
            not output
            or "[error" in output.lower()
            or "error:" in output.lower()
            or "[execution error" in output.lower()
        )

        if failed:
            snippet = output[:400] if output else "No output captured."
            if tone == TONE_CASUAL:
                return f"Hmm, ran into something:\n\n```\n{snippet}\n```\n\nWant me to try a different approach?"
            return f"The command encountered an issue:\n\n```\n{snippet}\n```\n\nReview the output and try again."

        if tone == TONE_CASUAL:
            wins = {
                "rebuild":    f"Done! `{label}` rebuilt, documented, and certified. Backup was saved — check the transparency output for its path.",
                "design":     "Blueprint's ready! Want me to build this? Just say 'yes' or 'build it' and I'll kick off a rebuild.",
                "docs":       "Docs generated! Check the output folder.",
                "lint":       "Lint done! See any issues above you want me to address?",
                "certify":    "Certified! CERTIFICATE.json is in the output folder.",
                "enhance":    "Here are my recommendations. Say 'apply all' to apply every finding, or 'apply 1,3,5' for specific ones.",
                "eco-scan":   "Compliance check complete! Full breakdown above.",
                "recon":      "Recon done! Scout, deps, tiers, tests, and docs all checked. See findings above.",
                "doctor":     "All good — everything's connected.",
                "self-enhance": "Done. The CLI just evolved. Try it out.",
                "add-feature": "Feature added in-place! New files are in the tier folders above.",
                "memory":     output if output else "Saved to your profile.",
                "clean":      output if output else "Nothing to clean.",
                "help":       output if output else self.describe_self(),
                "cli":        "Command complete. I streamed the output above.",
                "chat":       output[:600] if output else "Here's what I found.",
            }
        else:
            wins = {
                "rebuild":    f"`{label}` rebuilt, documented, and certified. CERTIFICATE.json is in the output folder. Backup preserved.",
                "design":     "Blueprint generated. Say 'yes' or 'build it' to materialize it, or review the JSON first.",
                "docs":       "Documentation generated successfully.",
                "lint":       "Lint pipeline complete. Review any findings above.",
                "certify":    "Certification complete. CERTIFICATE.json has been written.",
                "enhance":    "Enhancement scan complete. Say 'apply all' to apply all findings, or 'apply 1,3,5' for specific IDs.",
                "eco-scan":   "Monadic compliance check complete.",
                "recon":      "Reconnaissance complete. Review the report above for structure, dependencies, tier distribution, test coverage, and documentation gaps.",
                "doctor":     "Self-check complete. All systems nominal.",
                "self-enhance": "Live evolution complete. The CLI has been rebuilt and hot-patched.",
                "add-feature": "Feature files created in-place in the correct tier folders.",
                "memory":     output if output else "Saved to local profile.",
                "clean":      output if output else "No auto-generated folders found.",
                "help":       output if output else self.describe_self(),
                "cli":        "Command complete. Review the streamed output above.",
                "chat":       output[:600] if output else "No output returned.",
            }

        return wins.get(intent, wins["chat"])


def _parse_findings_from_output(output: str) -> list[dict]:
    """Extract finding ID/category pairs from an enhance command's text output."""
    findings: list[dict] = []
    # Rich table rows: ID column is a short integer at the start of a line segment
    for m in re.finditer(r"^\s*(\d+)\s+\|\s*\S", output, re.MULTILINE):
        findings.append({"id": int(m.group(1))})
    if not findings:
        # Fallback: find standalone integers ≤ 200 that look like IDs
        for m in re.finditer(r"(?:^|\s)(\d{1,3})(?:\s|$)", output, re.MULTILINE):
            val = int(m.group(1))
            if 1 <= val <= 200:
                findings.append({"id": val})
        findings = findings[:50]  # cap
    return findings


# ── Lightweight startup scan ───────────────────────────────────────────────────

def quick_project_scan(path: Path) -> dict:
    """Scan ``path`` and return a summary dict in under 2 seconds.

    Covers: file count, language, tier structure, security findings (eval/exec/shell=True),
    untested modules, docstring coverage, and CERTIFICATE.json metadata.
    Results are cached on the Atomadic instance as ``_startup_scan``.
    """
    _ignore = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
               "dist", "build", "target", ".ass-ade"}
    tier_names = {"a0_qk_constants", "a1_at_functions", "a2_mo_composites",
                  "a3_og_features", "a4_sy_orchestration"}
    lang_map = {
        ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript/React",
        ".js": "JavaScript", ".jsx": "JavaScript/React", ".rs": "Rust",
        ".go": "Go", ".java": "Java", ".cs": "C#", ".cpp": "C++",
        ".rb": "Ruby", ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    }

    ext_counts: dict[str, int] = {}
    total_files = 0
    tier_dirs_found: set[str] = set()
    py_source_files: list[Path] = []
    test_stems: set[str] = set()

    try:
        for entry in path.rglob("*"):
            if any(part in _ignore for part in entry.parts):
                continue
            if entry.is_dir():
                if entry.name in tier_names:
                    tier_dirs_found.add(entry.name)
                continue
            total_files += 1
            ext = entry.suffix.lower()
            if ext:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            if ext == ".py":
                stem = entry.stem
                if stem.startswith("test_") or stem.endswith("_test"):
                    test_stems.add(stem[5:] if stem.startswith("test_") else stem[:-5])
                else:
                    py_source_files.append(entry)
    except (PermissionError, OSError):
        pass

    # Security scan — cap at 200 files to stay fast
    security_findings = 0
    _sec_patterns = (b"eval(", b"exec(", b"shell=True")  # nosec
    for pyf in py_source_files[:200]:
        try:
            raw = pyf.read_bytes()
            if any(p in raw for p in _sec_patterns):
                security_findings += 1
        except OSError:
            pass

    # Docstring coverage — check first 512 bytes for triple-quote
    files_with_docstrings = 0
    sample = py_source_files[:200]
    for pyf in sample:
        try:
            head = pyf.read_bytes()[:512]
            if b'"""' in head or b"'''" in head:
                files_with_docstrings += 1
        except OSError:
            pass
    docstring_pct = int(files_with_docstrings / len(sample) * 100) if sample else 0

    # Untested modules
    source_stems = {f.stem for f in py_source_files}
    untested = len(source_stems - test_stems)

    # Top language
    top_ext = max(ext_counts, key=lambda k: ext_counts[k]) if ext_counts else ""
    lang = lang_map.get(top_ext, top_ext.lstrip(".").upper() if top_ext else "mixed")

    has_tier_structure = len(tier_dirs_found) == 5

    # Component count for tier builds = all py files under tier dirs
    component_count = 0
    if has_tier_structure:
        for pyf in py_source_files:
            if any(t in pyf.parts for t in tier_dirs_found):
                component_count += 1

    # Certificate metadata
    cert_info: dict[str, str] = {}
    cert_path = path / "CERTIFICATE.json"
    if cert_path.exists():
        try:
            cert_data = json.loads(cert_path.read_text(encoding="utf-8"))
            raw_date = cert_data.get("date", cert_data.get("timestamp", ""))
            if raw_date:
                cert_info["date"] = str(raw_date)[:10]
            raw_conf = cert_data.get("conformance", cert_data.get("score", ""))
            if raw_conf:
                cert_info["conformance"] = str(raw_conf)
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "project_name": path.name,
        "total_files": total_files,
        "language": lang,
        "has_tier_structure": has_tier_structure,
        "tier_dirs_found": sorted(tier_dirs_found),
        "component_count": component_count,
        "security_findings": security_findings,
        "untested_modules": untested,
        "docstring_pct": docstring_pct,
        "cert_info": cert_info,
    }


def _build_startup_greeting(
    scan: dict,
    memory: "MemoryStore",
    working_dir: Path,
    is_first_visit: bool,
) -> tuple[str, list[str]]:
    """Return (greeting_text, suggestions_list).

    suggestions_list contains the short action labels that correspond to
    typing "1", "2", "3" in the REPL (e.g. ["Fix 3 security issues", ...]).
    """
    name = scan["project_name"]
    total_files = scan["total_files"]
    lang = scan["language"]
    has_tier = scan["has_tier_structure"]
    sec = scan["security_findings"]
    untested = scan["untested_modules"]
    docstring_pct = scan["docstring_pct"]
    cert_info = scan["cert_info"]
    component_count = scan["component_count"]

    header = "Atomadic · ASS-ADE 1.0.0"
    suggestions: list[str] = []

    if has_tier and cert_info:
        last_rebuild = cert_info.get("date", "")
        raw_conf = cert_info.get("conformance", "")
        try:
            conf_num = float(str(raw_conf).rstrip("%"))
            conf_str = f"{conf_num:.1f}% conformant."
        except ValueError:
            conf_str = f"{raw_conf} conformant." if raw_conf else "Run `ass-ade certify` to record conformance."
        comp_str = f"{component_count} components" if component_count else f"{total_files} files"
        rebuild_line = (
            f"Last rebuild: {last_rebuild}. No drift detected since then."
            if last_rebuild
            else "Not yet certified — run `ass-ade certify` to record a snapshot."
        )
        lines = [
            header, "",
            f"Welcome back to `{name}` — your 5-tier monadic build.",
            f"{comp_str} across all tiers. {conf_str}",
            rebuild_line,
            "",
            "Ready for your next evolution. What shall we improve?",
        ]
        return "\n".join(lines), suggestions

    if has_tier:
        comp_str = f"{component_count} components" if component_count else f"{total_files} files"
        lines = [
            header, "",
            f"Welcome back to `{name}` — your 5-tier monadic build.",
            f"{comp_str} across all tiers.",
            "",
            "Ready for your next evolution. What shall we improve?",
        ]
        return "\n".join(lines), suggestions

    # Standard project greeting
    greet = "Hi! First time here." if is_first_visit else "Hey!"
    intro = (
        f"{greet} I see you're working in `{name}` — a {lang} project with {total_files} files."
    )

    quality_parts: list[str] = []
    if docstring_pct:
        quality_parts.append(f"{docstring_pct}% docstring coverage")

    if sec == 0 and untested == 0:
        quality_parts.append("no security findings, all modules tested")
        quality = "Looks clean: " + ", ".join(quality_parts) + "."
    elif sec == 0:
        quality_parts.append(f"no circular deps, but I spotted {untested} untested module(s)")
        quality = "Looks like a solid codebase: " + ", ".join(quality_parts) + "."
    elif untested == 0:
        quality_parts.append(f"{sec} security finding(s) (eval/exec usage)")
        quality = "Mostly solid, but: " + ", ".join(quality_parts) + "."
    else:
        quality_parts.append(f"{sec} security finding(s) (eval/exec usage)")
        quality_parts.append(f"{untested} untested module(s)")
        quality = "Looks like a solid codebase: " + ", ".join(quality_parts[:-2]) + (
            f", but I spotted {sec} security finding(s) (eval/exec usage)"
            f" and {untested} untested module(s)."
        )

    if sec > 0:
        suggestions.append(f"Fix the {sec} security issue(s) (high impact, low effort)")
    if untested > 0:
        suggestions.append(f"Add tests for the {untested} untested module(s)")
    suggestions.append("Consider a rebuild to organize into the 5-tier structure")

    lines = [header, "", intro, quality]
    if suggestions:
        lines += ["", "Quick suggestions:"]
        for i, s in enumerate(suggestions, 1):
            lines.append(f"  {i}. {s}")
        lines += ["", "Type a number to start, or just tell me what you need."]

    return "\n".join(lines), suggestions


def _run_setup_wizard(
    console: "Any | None",
    use_rich: bool,
    agent: "Atomadic",
) -> None:
    """Minimal first-visit setup wizard: collect name + preferred tone."""

    def _print(msg: str) -> None:
        if use_rich and console:
            console.print(msg)
        else:
            print(msg)

    _print("\n[bold cyan]First time here! Let's set up your profile (takes 10 seconds).[/bold cyan]"
           if use_rich else "\nFirst time here! Let's set up your profile (takes 10 seconds).")
    try:
        name = input("  Your name (or press Enter to skip): ").strip()
        if name:
            agent.memory.user_profile["name"] = name

        tone_raw = input("  Preferred style — casual / formal / technical (Enter = casual): ").strip().lower()
        tone = tone_raw if tone_raw in {TONE_CASUAL, TONE_FORMAL, TONE_TECHNICAL} else TONE_CASUAL
        agent.memory.user_profile["dominant_tone"] = tone
        agent.memory.save()

        who = f" {name}!" if name else "!"
        _print(f"\n  Got it{who} I'll keep a casual tone.\n" if tone == TONE_CASUAL
               else f"\n  Got it{who} Noted.\n")
    except (EOFError, KeyboardInterrupt):
        pass


# ── @ meta-command handler ─────────────────────────────────────────────────────

def _emit_ag_ui_tool_start(tool_name: str, user_input: str) -> None:
    """Publish a TOOL_CALL_START on the AG-UI bus, if the bus is available.

    No-op when the UI extras are not imported or the bus cannot be acquired.
    """
    try:
        from ass_ade.a2_mo_composites.ag_ui_bus import AGUIEventType, get_bus
        get_bus().emit(
            AGUIEventType.TOOL_CALL_START,
            {"tool": f"skill:{tool_name}", "input": user_input[:500]},
        )
    except Exception:
        pass


def _emit_ag_ui_tool_result(tool_name: str, output: str) -> None:
    """Publish a TOOL_CALL_RESULT + TOOL_CALL_END + widget card to the bus."""
    try:
        from ass_ade.a2_mo_composites.ag_ui_bus import AGUIEventType, get_bus
        bus = get_bus()
        bus.emit(
            AGUIEventType.TOOL_CALL_RESULT,
            {"tool": f"skill:{tool_name}", "output": output[:20_000]},
        )
        bus.emit_widget("skill_result", {"name": tool_name, "output": output[:20_000]})
        bus.emit(AGUIEventType.TOOL_CALL_END, {"tool": f"skill:{tool_name}"})
    except Exception:
        pass


def _handle_at_command(agent: "Atomadic", cmd: str, arg: str) -> str:
    """Dispatch REPL-level @ meta-commands without going through the agent loop."""
    if cmd == "skills":
        runner = agent._get_skills()
        skills = runner.list_skills()
        if not skills:
            return "No skills loaded."
        lines = ["**Available Skills**\n"]
        for s in skills:
            lines.append(f"- **{s['name']}** — {s['description']}\n  *(e.g. `{s['usage']}`)*")
        return "\n".join(lines)

    if cmd == "persona":
        if not arg:
            from ass_ade.a2_mo_composites.personality_engine import ALL_PERSONAS
            available = ", ".join(ALL_PERSONAS)
            current = agent.personality.persona
            return f"**Current persona:** `{current}`\n\nAvailable: {available}\n\nUsage: `@persona <mode>`"
        ok = agent.personality.set_persona(arg.lower())
        if ok:
            return f"**Persona set to `{arg.lower()}`.**"
        from ass_ade.a2_mo_composites.personality_engine import ALL_PERSONAS
        return f"Unknown persona `{arg}`. Available: {', '.join(ALL_PERSONAS)}"

    if cmd == "remember":
        if ":" in arg:
            key, _, value = arg.partition(":")
            agent.episodes.add_anchor(key.strip(), value.strip())
            return f"**Anchored:** `{key.strip()}` → {value.strip()}"
        return "Usage: `@remember <key>: <value>`"

    if cmd == "forget":
        if not arg:
            return "Usage: `@forget <key>`"
        removed = agent.episodes.remove_anchor(arg.strip())
        if removed:
            return f"**Anchor removed:** `{arg.strip()}`"
        return f"No anchor found for `{arg.strip()}`."

    if cmd in {"history", "episodes"}:
        return agent.episodes.summarize()

    if cmd == "personality":
        return agent.personality.describe()

    if cmd == "scout":
        from ass_ade.a3_og_features.skill_runner import SkillContext, _run_scout
        ctx = SkillContext(
            user_input=f"scout {arg}" if arg else "scout",
            working_dir=agent.working_dir,
            tone="casual",
            domain_level=agent.personality.domain_level,
            history=agent.history,
        )
        return _run_scout(ctx)

    if cmd == "patch":
        if not arg.strip():
            return (
                "Usage: `@patch <path1> [path2 ...]`\n\n"
                "Reloads newly-materialized Python modules into this live session.\n"
                "Load-bearing modules (interpreter, cli, server) are refused automatically."
            )
        from ass_ade.a3_og_features.hot_patch_runtime import hot_patch
        paths = [Path(p) for p in arg.split()]
        report = hot_patch(paths, root=agent.working_dir)
        counts: dict[str, int] = {}
        for r in report.results:
            counts[r.status] = counts.get(r.status, 0) + 1
        lines = [f"**Hot-patch**  verdict: **{report.verdict}**\n"]
        for r in report.results:
            marker = {
                "reloaded": "🔄",
                "imported": "✨",
                "skipped_blocked": "🛑",
                "error": "❌",
                "not_found": "❓",
            }.get(r.status, "·")
            label = r.module or r.path
            err = f" — {r.error}" if r.error else ""
            lines.append(f"- {marker} `{label}` ({r.status}){err}")
        lines.append(
            f"\n_{counts.get('reloaded', 0)} reloaded · "
            f"{counts.get('imported', 0)} imported · "
            f"{counts.get('skipped_blocked', 0)} blocked · "
            f"{counts.get('error', 0) + counts.get('not_found', 0)} errored_"
        )
        return "\n".join(lines)

    if cmd == "blocks":
        from ass_ade.a3_og_features.skill_runner import SkillContext, _run_blocks
        ctx = SkillContext(
            user_input=f"blocks {arg}" if arg else "blocks",
            working_dir=agent.working_dir,
            tone="casual",
            domain_level=agent.personality.domain_level,
            history=agent.history,
        )
        return _run_blocks(ctx)

    if cmd == "copilot":
        from ass_ade.a3_og_features.skill_runner import SkillContext, _run_copilot
        ctx = SkillContext(
            user_input=f"copilot: {arg}" if arg else "copilot",
            working_dir=agent.working_dir,
            tone="casual",
            domain_level=agent.personality.domain_level,
            history=agent.history,
        )
        return _run_copilot(ctx)

    if cmd == "wire":
        apply_mode = arg.strip().lower().startswith("apply")
        if apply_mode:
            from ass_ade.a2_mo_composites.context_loader_wiring_specialist_core import (
                ContextLoaderWiringSpecialist,
            )
            source = agent.working_dir
            src_dir = source / "src"
            if src_dir.is_dir():
                subdirs = [p for p in src_dir.iterdir() if p.is_dir() and p.name.isidentifier()]
                if len(subdirs) == 1:
                    source = subdirs[0]
            specialist = ContextLoaderWiringSpecialist()
            report = specialist.wire(source)
            return (
                f"**Wire apply: `{source.name or source}`**\n\n"
                f"- Violations found: **{report['violations_found']}**\n"
                f"- Auto-fixed (written to disk): **{report['auto_fixed']}**\n"
                f"- Files changed: **{report['files_changed']}**\n"
                f"- Not auto-fixable: **{report['not_fixable']}**\n"
                f"- Verdict: **{report['verdict']}**"
            )
        from ass_ade.a3_og_features.skill_runner import SkillContext, _run_wire
        ctx = SkillContext(
            user_input=f"wire {arg}" if arg else "wire imports",
            working_dir=agent.working_dir,
            tone="casual",
            domain_level=agent.personality.domain_level,
            history=agent.history,
        )
        return _run_wire(ctx)

    if cmd == "anchors":
        anchors = agent.episodes.get_anchors()
        if not anchors:
            return "No anchors set. Use `@remember <key>: <value>` to add one."
        lines = ["**Knowledge Anchors**\n"]
        for k, v in anchors.items():
            lines.append(f"- `{k}` → {v}")
        return "\n".join(lines)

    # Unknown command — list all available @ commands
    return (
        "**Available @ commands:**\n\n"
        "- `@skills` — list all available skills\n"
        "- `@scout [path] [--llm]` — scout a repo for intel and benefit opportunities\n"
        "- `@wire [apply]` — scan tier imports (dry-run); `@wire apply` to patch\n"
        "- `@blocks [query]` — list playground building blocks from the registry\n"
        "- `@copilot <prompt>` — brainstorm a composition plan with the Copilot\n"
        "- `@patch <path> [...]` — hot-reload newly-materialized modules into this session\n"
        "- `@persona <mode>` — switch persona (co-pilot, mentor, commander, architect, debug-buddy)\n"
        "- `@remember <key>: <value>` — anchor a fact to memory\n"
        "- `@forget <key>` — remove an anchor\n"
        "- `@anchors` — list all anchored facts\n"
        "- `@history` / `@episodes` — show past session summaries\n"
        "- `@personality` — show current personality state\n"
    )


# ── Interactive session ────────────────────────────────────────────────────────

def run_interactive(working_dir: Path | None = None) -> None:
    """Drop into an interactive Atomadic session (REPL)."""
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        console: Console | None = Console()
        use_rich = True
    except ImportError:
        console = None
        use_rich = False

    wdir = working_dir or Path.cwd()
    agent = Atomadic(working_dir=wdir)

    is_first_visit = not bool(agent.memory.user_profile)

    # First-visit setup wizard (non-blocking — user can press Enter through it)
    if is_first_visit:
        _run_setup_wizard(console, use_rich, agent)

    # Lightweight scan (under 2 s) — results cached on agent
    scan = quick_project_scan(wdir)
    agent._startup_scan = scan
    greeting_text, suggestions = _build_startup_greeting(scan, agent.memory, wdir, is_first_visit)

    # Personalise greeting if returning user
    persona_greeting = agent.personality.greeting_prefix(agent.memory.user_profile.get("name"))
    if not is_first_visit and persona_greeting:
        greeting_text = greeting_text.replace("Welcome back to", persona_greeting + "\n\nWelcome back to")

    # Include episodic working memory hint if relevant
    ep_hint = agent.episodes.working_memory(wdir.name)
    if ep_hint:
        greeting_text += f"\n\n{ep_hint}"

    # Regenerate live capability doc so agent prompts and Claude Code context stay fresh
    try:
        from pathlib import Path as _Path
        from ass_ade.agent.capabilities import (
            inject_capabilities_into_agents,
            write_live_capabilities_md,
            sync_atomadic_prompt_capabilities,
        )
        write_live_capabilities_md(wdir)
        sync_atomadic_prompt_capabilities(repo_root=wdir)
        _global_agents = _Path.home() / ".claude" / "agents"
        _extra = [_global_agents] if _global_agents.is_dir() else []
        inject_capabilities_into_agents(wdir, extra_dirs=_extra or None)
    except Exception:
        pass
    agent._startup_suggestions = suggestions

    if use_rich and console:
        from rich.markdown import Markdown as _Markdown
        console.print()
        console.print(f"[bold cyan]{greeting_text}[/bold cyan]")
        console.print(f"\n[dim]Working dir: {wdir}   ·   type '@skills' for skills, '@scout' to survey a repo   ·   'exit' to quit[/dim]\n")
    else:
        print(f"\n{greeting_text}")
        print(f"\nWorking dir: {wdir}   ·   type '@skills' for skills, '@scout' to survey a repo   ·   'exit' to quit\n")

    while True:
        try:
            user_input = input("you → ").strip()
        except (EOFError, KeyboardInterrupt):
            # Record session episode on exit
            if agent.history:
                agent.episodes.record_episode(wdir.name, agent.history[-10:])
            msg = "\nGoodbye!"
            if use_rich and console:
                console.print(f"[dim]{msg}[/dim]")
            else:
                print(msg)
            break

        if user_input.lower() in {"exit", "quit", "bye", "q"}:
            if agent.history:
                agent.episodes.record_episode(wdir.name, agent.history[-10:])
            msg = "Goodbye!"
            if use_rich and console:
                console.print(f"[dim]{msg}[/dim]")
            else:
                print(msg)
            break

        # ── @ meta-commands (not dispatched through the agent) ─────────────────
        if user_input.startswith("@"):
            parts = user_input[1:].strip().split(None, 1)
            meta_cmd = parts[0].lower() if parts else ""
            meta_arg = parts[1].strip() if len(parts) > 1 else ""
            meta_output = _handle_at_command(agent, meta_cmd, meta_arg)
            if use_rich and console:
                console.print()
                console.print(Markdown(meta_output))
                console.print()
            else:
                print(f"\n{meta_output}\n")
            continue

        if user_input.lower() in {"help", "?", "what can you do"}:
            desc = agent.describe_self()
            if use_rich and console:
                console.print()
                console.print(Markdown(desc))
                console.print()
            else:
                print(f"\n{desc}\n")
            continue

        if not user_input:
            continue

        response = agent.process(user_input)
        if use_rich and console:
            console.print(f"\n[bold green]Atomadic[/bold green] →")
            console.print(Markdown(response))
            console.print()
        else:
            print(f"\nAtomadic → {response}\n")


# Public alias so external code can do: from ass_ade.interpreter import Interpreter
Interpreter = Atomadic

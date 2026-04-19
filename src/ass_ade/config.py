from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from ass_ade.nexus.validation import sanitize_header_value, validate_api_key, validate_url

ProfileName = Literal["local", "hybrid", "premium"]
LlmPriority = Literal["nexus", "cloud", "local", "free"]


class ProviderOverride(BaseModel):
    """User override for a single provider.

    All fields optional — only populate what you want to override from the
    built-in catalog. `api_key` is never written to disk from defaults.
    """
    enabled: bool = True
    api_key: str | None = Field(default=None, repr=False)
    base_url: str | None = None  # override the catalog default (e.g., private endpoint)
    models_by_tier: dict[str, str] | None = None  # override tier → model id mapping


class AssAdeConfig(BaseModel):
    profile: ProfileName = Field(default="local")
    nexus_base_url: str = Field(default="https://atomadic.tech")
    request_timeout_s: float = Field(default=20.0, ge=1.0, le=120.0)
    agent_id: str = Field(default="ass-ade-local")
    agent_model: str = Field(default="")  # empty = let LSE + catalog decide
    nexus_api_key: str | None = Field(default=None, repr=False)

    # ── LSE + Provider configuration (Phase 1 free-tier support) ─────────
    lse_enabled: bool = Field(default=True)
    """Enable LSE tier-based model routing. If False, agent_model is used directly."""

    tier_policy: dict[str, str] = Field(default_factory=dict)
    """Explicit tier → provider preference, e.g. {"balanced": "groq", "deep": "openrouter"}.
    Keys: fast / balanced / deep. Values: provider names from the catalog."""

    provider_fallback_chain: list[str] = Field(default_factory=list)
    """Ordered list of provider names to try. Empty = use catalog default."""

    providers: dict[str, ProviderOverride] = Field(default_factory=dict)
    """Per-provider overrides. Key = provider name (groq, gemini, ollama, ...)."""

    # ── Interpreter LLM settings ──────────────────────────────────────────────
    ollama_model: str = Field(default="")
    """Ollama model name for the interpreter (e.g. 'qwen3:8b-fp16').
    Empty = skip Ollama at runtime. Set during `ass-ade setup`."""

    llm_priority: LlmPriority = Field(default="cloud")
    """Provider priority order for the interpreter cascade (legacy — prefer llm_providers).
    nexus  — AAAA-Nexus first, then cloud, then Ollama, then Pollinations.
    cloud  — keyed cloud providers first, then Ollama, then Pollinations.
    local  — Ollama first (privacy), then cloud, then Pollinations.
    free   — Pollinations only, no keys or local models needed."""

    llm_providers: list[str] = Field(default_factory=list)
    """Ordered list of provider slugs for the interpreter cascade.
    Slugs: aaaa-nexus, groq, cerebras, gemini, openrouter, mistral, github, ollama, pollinations.
    Empty = derive from llm_priority for backwards compatibility.
    Pollinations is always the silent last resort even if omitted."""


def default_config_path(base_dir: Path | None = None) -> Path:
    root = base_dir or Path.cwd()
    return root / ".ass-ade" / "config.json"


def load_config(path: Path | None = None) -> AssAdeConfig:
    if path is None:
        env_config = os.getenv("ASS_ADE_CONFIG")
        target = Path(env_config) if env_config else default_config_path()
    else:
        target = path
    if not target.exists():
        cfg = AssAdeConfig()
    else:
        cfg = AssAdeConfig.model_validate_json(target.read_text(encoding="utf-8"))

    # Allow API key override via environment variable or .env file.
    # Environment wins over .env file.
    api_key = os.getenv("AAAA_NEXUS_API_KEY")
    if not api_key:
        # Prefer a .env located at the project root near the config file.
        # If the config lives at <root>/.ass-ade/config.json, look in <root>/.env.
        search_root = target.parent.parent if target.parent.name == ".ass-ade" else target.parent
        env_path = search_root / ".env"
        if env_path.exists():
            try:
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() == "AAAA_NEXUS_API_KEY":
                        api_key = v.strip()
                        break
            except OSError:
                api_key = None

    if api_key:
        try:
            cfg.nexus_api_key = validate_api_key(api_key)
        except ValueError:
            # Malformed key (control chars / too long) — ignore and fall through
            # without logging the raw value to avoid leaking credentials.
            cfg.nexus_api_key = None

    # Optional base URL override via env — must be a valid http/https URL.
    base_url = os.getenv("AAAA_NEXUS_BASE_URL")
    if base_url:
        try:
            cfg.nexus_base_url = validate_url(base_url)
        except ValueError:
            pass  # Keep the config-file default; ignore the invalid env value.

    # Load .env values into os.environ so provider env vars (GROQ_API_KEY etc.)
    # are discoverable by the provider catalog. File-based vars never override
    # explicit process env.
    _hydrate_env_file(target)

    return cfg


def _hydrate_env_file(config_path: Path) -> None:
    """Merge .env KEY=VALUE pairs into os.environ (process env wins)."""
    search_root = config_path.parent.parent if config_path.parent.name == ".ass-ade" else config_path.parent
    env_path = search_root / ".env"
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError:
        pass


def write_default_config(
    path: Path | None = None,
    config: AssAdeConfig | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    target = path or default_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return target

    # Do not write sensitive API keys into the default config file.
    # This includes nexus_api_key AND every provider override's api_key.
    cfg = config or AssAdeConfig()
    payload_dict = cfg.model_dump(exclude={"nexus_api_key"})
    # Strip api_key from each provider override (secrets never go to disk)
    providers = payload_dict.get("providers") or {}
    for override in providers.values():
        if isinstance(override, dict):
            override.pop("api_key", None)
    import json as _json
    payload = _json.dumps(payload_dict, indent=2)
    target.write_text(f"{payload}\n", encoding="utf-8")
    # Restrict permissions to owner read/write only (0o600) so the config
    # directory is not world-readable on shared systems (OWASP A05).
    try:
        target.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, NotImplementedError):
        pass  # Best-effort; Windows does not support POSIX permission bits.
    return target

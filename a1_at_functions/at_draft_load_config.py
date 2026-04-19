# Extracted from C:/!ass-ade/src/ass_ade/config.py:55
# Component id: at.source.ass_ade.load_config
from __future__ import annotations

__version__ = "0.1.0"

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

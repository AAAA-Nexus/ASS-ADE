# Extracted from C:/!ass-ade/src/ass_ade/config.py:15
# Component id: mo.source.ass_ade.provideroverride
from __future__ import annotations

__version__ = "0.1.0"

class ProviderOverride(BaseModel):
    """User override for a single provider.

    All fields optional — only populate what you want to override from the
    built-in catalog. `api_key` is never written to disk from defaults.
    """
    enabled: bool = True
    api_key: str | None = Field(default=None, repr=False)
    base_url: str | None = None  # override the catalog default (e.g., private endpoint)
    models_by_tier: dict[str, str] | None = None  # override tier → model id mapping

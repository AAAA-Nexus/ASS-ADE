"""Tier a3 — premium feature gate: API key validation, authorization, and usage logging."""
from __future__ import annotations

import os
import sys

from ass_ade.a0_qk_constants.auth_gate_types import (
    TIER_MESSAGE,
    UPGRADE_URL,
    PremiumFeature,
)
from ass_ade.nexus.client import NexusClient
from ass_ade.nexus.errors import NexusAuthError, NexusConnectionError, NexusError, NexusTimeoutError
from ass_ade.nexus.validation import validate_api_key


class PremiumGateError(RuntimeError):
    """Raised when a premium CLI command is invoked without a valid Atomadic API key."""

    def __init__(self, detail: str = "", *, feature: PremiumFeature | None = None) -> None:
        self.feature = feature
        super().__init__(detail or TIER_MESSAGE)


def _resolve_key(api_key: str | None) -> str | None:
    """Return api_key if provided, otherwise read AAAA_NEXUS_API_KEY from the environment."""
    return api_key or os.getenv("AAAA_NEXUS_API_KEY")


def require_premium(
    feature: PremiumFeature,
    *,
    base_url: str = "https://atomadic.tech",
    api_key: str | None = None,
    agent_id: str | None = None,
) -> str:
    """Gate a premium CLI feature behind API key validation.

    Flow:
    1. Read AAAA_NEXUS_API_KEY from env (or use the supplied api_key argument).
    2. Validate key format locally — reject control characters, empty strings, over-long values.
    3. Call /v1/authorize/action on AAAA-Nexus with the key in Bearer headers.
       - 401/403 → key is revoked or invalid → raise PremiumGateError.
       - Network error / timeout → fail open (warn to stderr, allow the call).
       - Any other server error → fail open.

    Returns the validated, clean API key string on success.
    Raises PremiumGateError when key is absent, malformed, or explicitly rejected.
    """
    raw_key = _resolve_key(api_key)
    if not raw_key:
        raise PremiumGateError(feature=feature)

    try:
        clean_key = validate_api_key(raw_key)
    except ValueError as exc:
        raise PremiumGateError(
            f"Malformed AAAA_NEXUS_API_KEY: {exc}",
            feature=feature,
        ) from exc

    resolved_agent_id = agent_id or "ass-ade"

    try:
        with NexusClient(
            base_url=base_url,
            api_key=clean_key,
            agent_id=resolved_agent_id,
            timeout=10.0,
        ) as nx:
            nx.authorize_action(
                agent_id=resolved_agent_id,
                action=feature.value,
            )
    except NexusAuthError as exc:
        raise PremiumGateError(
            f"API key rejected by Atomadic (HTTP {exc.status_code}).\n"
            f"Check or renew your key at {UPGRADE_URL}",
            feature=feature,
        ) from exc
    except (NexusConnectionError, NexusTimeoutError):
        # Network unavailable — fail open so offline/air-gapped users aren't blocked.
        print(
            f"[ass-ade] warn: could not reach {base_url} to validate key — proceeding offline.",
            file=sys.stderr,
        )
    except NexusError:
        # Unexpected server error — fail open.
        pass

    return clean_key


def log_usage(
    feature: PremiumFeature,
    *,
    base_url: str = "https://atomadic.tech",
    api_key: str,
    agent_id: str | None = None,
    metric_value: float = 1.0,
    success: bool = True,
) -> None:
    """Record a per-call usage event to AAAA-Nexus billing_outcome.

    Best-effort: never raises. A failure to log does not block the caller.
    metric_value semantics per feature:
      rebuild.forge      — number of files processed
      rebuild.multi-repo — 1.0 (per run)
      enhance            — 1.0 (per analysis)
      certify            — 1.0 (per certificate)
      blueprint.*        — 1.0 (per build/design run)
      protocol.evolve    — 1.0 (per evolution event)
    """
    try:
        with NexusClient(
            base_url=base_url,
            api_key=api_key,
            agent_id=agent_id or "ass-ade",
            timeout=10.0,
        ) as nx:
            nx.billing_outcome(
                task_id=feature.value,
                success=success,
                metric_value=metric_value,
            )
    except Exception:
        pass

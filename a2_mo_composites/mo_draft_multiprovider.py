# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:281
# Component id: mo.source.ass_ade.multiprovider
from __future__ import annotations

__version__ = "0.1.0"

class MultiProvider:
    """Routes each CompletionRequest to the right underlying provider by model.

    Holds a dict of {provider_name: ModelProvider} and a reverse map from
    model id → provider_name. If the requested model is unknown, falls back
    to the first provider in fallback order. On HTTP/network errors, tries
    the next provider in the fallback chain.

    Used by the LSE-enabled AgentLoop: when LSE picks model X for step N,
    MultiProvider finds which underlying provider serves X and routes the call
    there. The next step can route to a completely different provider.
    """

    def __init__(
        self,
        providers: dict[str, "ModelProvider"],
        model_to_provider: dict[str, str] | None = None,
        fallback_order: list[str] | None = None,
    ) -> None:
        self._providers = dict(providers)
        self._model_to_provider = dict(model_to_provider or {})
        self._fallback_order = list(fallback_order or providers.keys())
        self._last_provider_name: str | None = None

    @property
    def providers(self) -> dict[str, "ModelProvider"]:
        return dict(self._providers)

    @property
    def last_provider_name(self) -> str | None:
        return self._last_provider_name

    @property
    def model_name(self) -> str:
        # For compatibility with the OpenAICompatibleProvider property
        if self._providers and self._fallback_order:
            first = self._providers.get(self._fallback_order[0])
            if first is not None and hasattr(first, "model_name"):
                return first.model_name  # type: ignore[no-any-return]
        return "multi-provider"

    def register(self, name: str, provider: "ModelProvider", models: list[str] | None = None) -> None:
        """Add a provider to the router at runtime."""
        self._providers[name] = provider
        if name not in self._fallback_order:
            self._fallback_order.append(name)
        for m in models or []:
            self._model_to_provider[m] = name

    def close(self) -> None:
        for p in self._providers.values():
            close = getattr(p, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Route a request to the right provider, with automatic fallback."""
        order = self._select_order(request.model)
        last_error: Exception | None = None
        for name in order:
            provider = self._providers.get(name)
            if provider is None:
                continue
            try:
                response = provider.complete(request)
                self._last_provider_name = name
                return response
            except httpx.HTTPError as exc:
                last_error = exc
                continue
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue
        # All providers failed — re-raise the last error so the caller sees it.
        if last_error is not None:
            raise last_error
        raise RuntimeError("MultiProvider: no providers configured")

    def _select_order(self, model: str | None) -> list[str]:
        """Compute provider-try order for a given model."""
        if not model:
            return list(self._fallback_order)
        primary = self._model_to_provider.get(model)
        if primary is None:
            return list(self._fallback_order)
        order = [primary]
        order.extend(n for n in self._fallback_order if n != primary)
        return order

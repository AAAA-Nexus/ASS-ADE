# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1274
# Component id: mo.source.ass_ade.bitnet_stream
__version__ = "0.1.0"

    def bitnet_stream(self, prompt: str, model: str = "bitnet-b1.58-2B-4T", **kwargs: Any) -> Iterator[str]:
        """POST /v1/bitnet/inference/stream — streaming 1-bit CoT (BIT-101). $0.040/call"""
        with self._client.stream("POST", "/v1/bitnet/inference/stream", json={"prompt": prompt, "model": model, **kwargs}) as r:
            r.raise_for_status()
            for chunk in r.iter_text():
                if chunk:
                    yield chunk

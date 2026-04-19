# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:417
# Component id: mo.source.ass_ade.inference
__version__ = "0.1.0"

    def inference(self, prompt: str, **kwargs: Any) -> InferenceResponse:
        """/v1/inference — Llama 3.1 8B via Cloudflare Workers AI. $0.060/call"""
        return self._post_model("/v1/inference", InferenceResponse, {"prompt": prompt, **kwargs})

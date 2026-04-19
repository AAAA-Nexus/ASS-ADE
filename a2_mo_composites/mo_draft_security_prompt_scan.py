# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:684
# Component id: mo.source.ass_ade.security_prompt_scan
__version__ = "0.1.0"

    def security_prompt_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
        """/v1/security/prompt-scan — detect + block adversarial inputs. $0.040/request"""
        return self._post_model("/v1/security/prompt-scan", PromptScanResult, {"prompt": prompt, **kwargs})

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_qualitygates.py:129
# Component id: at.source.ass_ade.trim_context
__version__ = "0.1.0"

    def trim_context(self, context: str, target_tokens: int) -> str | None:
        """Trim context using Nexus memory_trim for optimal token usage.

        Falls back to None if Nexus is unavailable (caller uses local trim).
        """
        try:
            result = self._client.memory_trim(context=context, target_tokens=target_tokens)
            gate = GateResult(
                gate="memory_trim",
                passed=True,
                confidence=1.0,
                details={"target_tokens": target_tokens},
            )
            self._gate_log.append(gate)
            return result.trimmed_context
        except Exception as _exc:  # noqa: BLE001
            logging.getLogger(__name__).warning(
                "Gate %s failed (fail-open): %s: %s",
                "trim_context",
                type(_exc).__name__,
                _exc,
            )
            return None

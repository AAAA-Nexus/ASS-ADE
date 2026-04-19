# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:512
# Component id: at.source.ass_ade.delegation_validate
__version__ = "0.1.0"

    def delegation_validate(self, chain: list[dict], **kwargs: Any) -> DelegationValidation:
        """/v1/identity/delegation/validate — IDT-201 chain depth validator. $0.080/call"""
        return self._post_model("/v1/identity/delegation/validate", DelegationValidation, {"chain": chain, **kwargs})

# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_x402clientflow.py:27
# Component id: at.source.ass_ade.parse_challenge
__version__ = "0.1.0"

    def parse_challenge(self, response_dict: dict) -> PaymentChallenge | None:
        """Parse a 402 response dict into a PaymentChallenge.

        Returns None if parsing fails; check last_error for details.
        """
        try:
            return PaymentChallenge.from_response(response_dict)
        except ValueError as e:
            self.last_error = str(e)
            return None

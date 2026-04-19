# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_nexussession.py:18
# Component id: at.source.ass_ade.start
__version__ = "0.1.0"

    def start(self, agent_id: str) -> RatchetSession:
        """Register a new RatchetGate session."""
        validate_agent_id(agent_id)
        # RatchetGate expects agent_id as an int multiple of G_18 (324)
        # The server handles the constraint; we send the raw value
        result = self._client.ratchet_register(
            int(agent_id) if agent_id.isdigit() else (
                int.from_bytes(hashlib.sha256(agent_id.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF
            )
        )
        self.session_id = result.session_id
        self.epoch = result.epoch or 0
        self._started = True
        return result

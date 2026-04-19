# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:208
# Component id: qk.source.ass_ade.messages_to_evict
__version__ = "0.1.0"

    def messages_to_evict(
        self,
        messages: list[Message],
        tools: list[ToolSchema] | None = None,
    ) -> int:
        """Compute how many oldest non-system messages to evict.

        Returns 0 if the conversation fits within the budget.
        The eviction count is the *minimum* needed to restore the invariant.
        """
        tool_overhead = estimate_tools_tokens(tools or [])

        # Calculate cumulative tokens for each message
        msg_tokens = [estimate_message_tokens(m) for m in messages]
        total = sum(msg_tokens) + tool_overhead

        if total <= self.available:
            return 0

        # Identify non-system messages eligible for eviction
        excess = total - self.available
        evicted = 0
        freed = 0
        for i, msg in enumerate(messages):
            if msg.role == "system":
                continue
            freed += msg_tokens[i]
            evicted += 1
            if freed >= excess:
                break

        return evicted

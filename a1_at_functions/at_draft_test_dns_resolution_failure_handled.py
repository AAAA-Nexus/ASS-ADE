# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateabsoluteendpoint.py:60
# Component id: at.source.ass_ade.test_dns_resolution_failure_handled
__version__ = "0.1.0"

    def test_dns_resolution_failure_handled(self) -> None:
        """DNS resolution failures should be caught and reported."""
        with pytest.raises(ValueError, match="private/loopback address"):
            # Invalid hostname that won't resolve
            _validate_absolute_endpoint("https://this-domain-does-not-exist-12345-test.invalid/api")

def caller_uses_helper() -> int:
    """Calls pure_helper so Phase 3 can derive a made_of edge."""
    return pure_helper(0)

## Summary

What changed and why (one short paragraph).

## Checklist

- [ ] Tests: `python -m pytest` (or scoped markers you touched).
- [ ] Import law: `lint-imports` (monadic tiers).
- [ ] No secrets, tokens, or private URLs in commits or PR description.
- [ ] If the change touches swarm/Nexus handoffs: preflight/postflight and trust receipts per workspace `agents/_PROTOCOL.md` (when that tree is available in the checkout).
- [ ] Context pack or plan link (if this PR implements a tracked plan node).

## CLI smoke (optional)

```bash
ass-ade-v11 rebuild tests/fixtures/minimal_pkg --stop-after gapfill
```

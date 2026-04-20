# Skill: ass-ade certify

## When to use this skill

Use `ass-ade certify` after any operation that produces or modifies a codebase that
needs a tamper-evident record. Common triggers:

- After `ass-ade rebuild` completes
- Before archiving or publishing a codebase
- When an auditor requests proof of codebase integrity
- When verifying that a received codebase has not been modified in transit

## Step-by-step

### Certifying a new codebase

1. Ensure the source path exists and is complete:
   ```
   ass-ade certify <path>
   ```
2. The command computes a local SHA-256 digest and submits it to AAAA-Nexus for
   countersigning. This requires `AAAA_NEXUS_API_KEY` to be set.
3. After completion, `CERTIFICATE.json` is written to `<path>/CERTIFICATE.json`.
4. Read the certificate:
   ```
   ass-ade certify show <path> --json
   ```
5. Confirm `valid: true` and that `signed_by` is `atomadic.tech`.

### Verifying an existing certificate

1. Run verify:
   ```
   ass-ade certify verify <path>
   ```
2. The command re-computes the local digest and checks it against the stored
   `root_digest`. It also verifies the Nexus signature.
3. A clean verification prints `[OK] certificate valid` and exits 0.
4. A drift detection prints the list of changed files and exits 1.

### Local-only certification (no API key)

If no API key is available, certify still produces a local-only certificate:
```
ass-ade certify <path> --local-only
```
The resulting certificate has `valid: false` and `signed_by: null`. It can be used
for local integrity tracking but is not recognized as a valid certificate by
external consumers.

## Flags and options

| Flag | Effect |
|------|--------|
| `--local-only` | Skip Nexus signing; produce a local digest only |
| `--json` | Print the certificate JSON to stdout after certifying |
| `--output <file>` | Write the certificate to a specific file path |

### certify verify flags
| Flag | Effect |
|------|--------|
| `--strict` | Exit 1 if the certificate is local-only (no Nexus signature) |

### certify show flags
| Flag | Effect |
|------|--------|
| `--json` | Emit the certificate as JSON |

## Output interpretation

`CERTIFICATE.json` key fields:

| Field | Meaning |
|-------|---------|
| `valid` | `true` only when digest matches AND Nexus signature is valid |
| `digest.root_digest` | Fingerprint of the codebase at certification time |
| `digest.file_count` | Number of files included in the digest |
| `digest.computed_at` | When the digest was computed |
| `signed_by` | `"atomadic.tech"` for a fully signed certificate |
| `signature` | Hex-encoded cryptographic signature; `null` if unsigned |

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Certificate issued or verified | Proceed |
| 1 | Drift detected (verify) or signing failed (certify) | Check stderr |
| 2 | Auth error | Set `AAAA_NEXUS_API_KEY` or use `--local-only` |
| 3 | Path not found | Verify the path exists |

If `certify` fails with exit code 1, do not treat the existing certificate as valid.
The certificate on disk may be from a previous run and no longer reflects current state.
Always re-certify after any file changes.

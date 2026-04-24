# Multi-language Bridges

Generated bridge scaffolding for the rebuilt artifact.

- Bridge mode: `spawn-cli`
- Bridge ready: NO
- Vendored ASS-ADE: NO
- Python bridge command: `not configured`
- Supported languages: `python`, `rust`, `typescript`, `kotlin`, `swift`, `atomadic`
- Prepared bridge targets: `typescript`, `rust`, `kotlin`, `swift`

## Wiring contract

- Manifest: `.ass-ade/bridges/bridge_manifest.json`
- Samples: `bridges/samples/bridge_request.sample.json`, `bridges/samples/bridge_response.sample.json`
- Generated tests: `tests/test_generated_multilang_bridges.py`

## Prepared bridge roots

| Language | Root |
|----------|------|
| `typescript` | `bridges/typescript` |
| `rust` | `bridges/rust` |
| `kotlin` | `bridges/kotlin` |
| `swift` | `bridges/swift` |

## Notes

- These files are bridge-ready wiring artifacts with a minimal a0-a4 monadic scaffold for each emitted bridge language.
- They read the rebuild bridge manifest and expose a stable process-spawn contract around the shipped Python surface.
- They do not synthesize domain-specific non-Python atom bodies yet.
- Use them as starting points for real TypeScript, Rust, Kotlin, and Swift adapters in downstream repos.

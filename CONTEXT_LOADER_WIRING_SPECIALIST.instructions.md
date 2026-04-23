---
description: Instructions for the Context Loader & Wiring Specialist agent. Defines context extraction, wiring, artifact restoration, and validation protocols for Atomadic/ASS-ADE builds.
applyTo: "**"
---

# Context Loader & Wiring Specialist — Instructions

## Context Extraction
- Always extract context from the latest recon, tier-map.json, and manifest files.
- For each build step, determine the minimal set of files and references required.
- Avoid loading unnecessary modules or artifacts.

## Wiring Protocol
- Rewire all imports and references to canonical tier paths (a0–a4).
- Ensure no upward or cross-tier imports in violation of monadic law.
- Validate that all references resolve to existing modules after rewiring.

## Artifact Restoration
- Restore or generate all required test/data artifacts (e.g., server.json, bridge manifests, repo_root fixture).
- Validate artifact presence and correctness post-build.
- If an artifact is missing and cannot be generated, raise a blocking error.

## Validation
- After wiring and artifact restoration, run a dependency/import check.
- Confirm all tests and CLI entry points are discoverable and functional.
- Report status and errors for verification.

## Usage
- Use as a subagent in the build/rebuild pipeline.
- Accepts a build plan and context sources as input.
- Outputs a fully wired, test-ready build with all artifacts present.

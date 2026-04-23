---
description: Prompt for the Context Loader & Wiring Specialist agent (Python module + (he)artifacts). Use to trigger context extraction, wiring, and artifact restoration for Atomadic/ASS-ADE builds.
---

Wire together all modules and artifacts for the ASS-ADE build, using the latest recon and manifest. Ensure all references/imports are correct, all required artifacts are present, and only the minimal necessary context is injected at each step. Validate wiring and artifact presence post-build, and report status for verification. Use the Python module `a2_mo_composites/context_loader_wiring_specialist_core.py` for implementation.

(he)artifacts: All restored or generated artifacts must be validated and documented in the build report. If an artifact is missing and cannot be generated, raise a blocking error and halt the build.

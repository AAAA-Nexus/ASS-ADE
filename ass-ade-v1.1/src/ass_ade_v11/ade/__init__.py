"""ASS-ADE workspace bundle — ADE operator stack (hooks, automation, ADE harness refs).

This package is the **portable** twin of the Atomadic monorepo's ``.cursor/``, ``ADE/``,
and ``scripts/`` surface. The CLI (``ass-ade-unified ade …``) materializes
``<workspace>/.ade/`` so every install can run the same *prompt → product* workflow
without hand-copying paths. See :func:`ass_ade_v11.ade.materialize.materialize_dotted_ade`).

Layout version (in ``.ade/LAYOUT.json``) is :data:`ADE_LAYOUT_VERSION`.
"""

from ass_ade_v11.ade.materialize import materialize_dotted_ade
from ass_ade_v11.ade.versions import ADE_LAYOUT_VERSION

__all__ = [
    "ADE_LAYOUT_VERSION",
    "materialize_dotted_ade",
    "__version__",
]

__version__ = "1.0.0"

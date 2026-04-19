# Extracted from C:/!ass-ade/tests/test_recon_context.py:89
# Component id: mo.source.ass_ade.test_vector_memory_store_and_query
from __future__ import annotations

__version__ = "0.1.0"

def test_vector_memory_store_and_query(tmp_path: Path) -> None:
    vector = vector_embed("trusted rag context")
    assert len(vector) == VECTOR_DIMENSIONS

    stored = store_vector_memory(
        text="trusted rag context for mcp tools",
        namespace="demo",
        metadata={"source": "unit"},
        working_dir=tmp_path,
    )
    result = query_vector_memory(
        query="mcp trusted context",
        namespace="demo",
        working_dir=tmp_path,
    )

    assert stored.id == result.matches[0].id
    assert result.matches[0].metadata["source"] == "unit"

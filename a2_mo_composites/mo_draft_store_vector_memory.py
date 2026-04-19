# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/context_memory.py:171
# Component id: mo.source.ass_ade.store_vector_memory
__version__ = "0.1.0"

def store_vector_memory(
    *,
    text: str,
    namespace: str = "default",
    metadata: dict[str, Any] | None = None,
    working_dir: str | Path = ".",
) -> VectorMemoryStoreResult:
    """Store a text memory as a local vector record."""
    if not text.strip():
        raise ValueError("text must not be empty")
    namespace = namespace.strip() or "default"
    path = _memory_path(working_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(UTC).isoformat()
    digest = hashlib.sha256(f"{namespace}\0{text}\0{created_at}".encode()).hexdigest()
    record = VectorMemoryRecord(
        id=digest[:24],
        namespace=namespace,
        text=text,
        vector=vector_embed(text),
        metadata=metadata or {},
        created_at=created_at,
    )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record.model_dump(), separators=(",", ":")) + "\n")

    return VectorMemoryStoreResult(
        id=record.id,
        namespace=namespace,
        path=str(path),
    )

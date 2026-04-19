# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_emit_certificate.py:7
# Component id: qk.source.a0_qk_constants.emit_certificate
from __future__ import annotations

__version__ = "0.1.0"

def emit_certificate(
    rebuild_receipt: dict[str, Any],
    audit: dict[str, Any],
    *,
    out_dir: Path | None = None,
) -> dict[str, Any]:
    """Write a SHA-256-bound rebuild certificate next to the rebuild folder.

    The certificate binds the rebuild tag, plan digest, and audit summary.
    A caller can verify the folder by re-running ``validate_rebuild`` and
    checking the certificate hash.
    """
    target_root = Path(rebuild_receipt.get("target_root", "") or (out_dir or Path(".")))
    cert_path = target_root / "CERTIFICATE.json"

    body = {
        "certificate_version": "ASSADE-SPEC-CERT-1",
        "issued_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "rebuild_tag": rebuild_receipt.get("rebuild_tag"),
        "source_plan_digest": rebuild_receipt.get("source_plan_digest"),
        "target_root": rebuild_receipt.get("target_root"),
        "written_count": rebuild_receipt.get("written_count"),
        "audit": {
            "total": audit.get("total"),
            "valid": audit.get("valid"),
            "summary": audit.get("summary"),
            "structure": audit.get("structure"),
        },
        "issuer": "ass_ade.engine.schema_rebuilder",
        "schema_covered": COMPONENT_SCHEMA,
    }
    blob = json.dumps(body, sort_keys=True).encode("utf-8")
    body["certificate_sha256"] = hashlib.sha256(blob).hexdigest()
    cert_path.write_text(
        json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "certificate_path": cert_path.as_posix(),
        "certificate_sha256": body["certificate_sha256"],
        "structure_conformant": audit.get("summary", {}).get("structure_conformant", False),
    }

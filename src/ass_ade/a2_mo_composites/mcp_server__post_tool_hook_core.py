"""Tier a2 — assimilated method 'MCPServer._post_tool_hook'

Assimilated from: server.py:611-700
"""

from __future__ import annotations


# --- assimilated symbol ---
def _post_tool_hook(
    self,
    name: str,
    arguments: dict[str, Any],
    result: Any,
    *,
    pre_write_content: str = "",
) -> Any:
    """Run post-execution gates.

    - read_file  → TCA.record_read
    - write_file / edit_file → CIE pipeline gate + LoRA fix capture

    Returns the (possibly modified) result. If CIE rejects the code, the
    file on disk is rolled back via undo_edit and the result is replaced
    with a structured error.
    """
    if not result or not getattr(result, "success", False):
        return result

    if name == "read_file":
        path = arguments.get("path") or arguments.get("file_path") or ""
        if path:
            try:
                self.tca.record_read(path)
            except (OSError, RuntimeError, TypeError, ValueError) as exc:
                _LOG.debug("TCA record_read failed: %s", exc)
        return result

    if name in ("write_file", "edit_file"):
        path = arguments.get("path") or arguments.get("file_path") or ""
        code = arguments.get("content") or arguments.get("new_content") or ""
        language = (
            "python"
            if path.endswith(".py")
            else "typescript"
            if path.endswith((".ts", ".tsx"))
            else "text"
        )
        if code and language != "text":
            try:
                cie_result = self.cie.run(code, language=language)
                if not cie_result.passed:
                    # Roll back the write by invoking undo_edit
                    try:
                        self._registry.execute("undo_edit", path=path)
                    except (AttributeError, LookupError, OSError, RuntimeError, TypeError, ValueError):
                        pass
                    # Capture rejection as negative training signal
                    if self.lora_flywheel is not None:
                        try:
                            self.lora_flywheel.capture_rejection(
                                candidate=code[:2000],
                                reason="; ".join(
                                    cie_result.errors + cie_result.owasp_findings
                                )[:200],
                            )
                        except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
                            pass
                    err_msg = (
                        f"[CIE REJECTED] {path}: "
                        f"ast_valid={cie_result.ast_valid}, "
                        f"owasp_clean={cie_result.owasp_clean}, "
                        f"errors={cie_result.errors[:3]}, "
                        f"owasp={cie_result.owasp_findings[:3]}"
                    )
                    from ass_ade.tools.base import ToolResult

                    return ToolResult(error=err_msg, success=False)
                # Passed: capture as accepted fix for LoRA training.
                # Only capture if the content actually changed — trivial
                # edits (e.g., formatting-only) are not training signal.
                if self.lora_flywheel is not None and code != pre_write_content:
                    try:
                        self.lora_flywheel.capture_fix(
                            original=pre_write_content,
                            fixed=code,
                            context={
                                "path": path,
                                "language": language,
                                "tool": name,
                            },
                        )
                    except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
                        pass
            except (AttributeError, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
                _LOG.debug("CIE gate skipped: %s", exc)
        return result

    return result


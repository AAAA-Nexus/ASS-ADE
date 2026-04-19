# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_qualitygates.py:229
# Component id: mo.source.ass_ade.hook_pci_verify
__version__ = "0.1.0"

    def hook_pci_verify(self, code: str, lang: str = "python", spec: str | None = None) -> dict[str, Any] | None:
        import ast
        import re
        try:
            findings: list[str] = []
            cc = 1
            if lang == "python":
                try:
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                            cc += 1
                except SyntaxError as exc:
                    findings.append(f"syntax:{exc.msg}")
                    cc = 999
            owasp_patterns = [
                (r"eval\s*\(", "a03_injection_eval"),
                (r"exec\s*\(", "a03_injection_exec"),
                (r"subprocess\.[a-z_]+\([^)]*shell\s*=\s*True", "a03_shell_injection"),
                (r"pickle\.loads?\s*\(", "a08_deserialization"),
                (r"md5\s*\(|sha1\s*\(", "a02_weak_hash"),
            ]
            for pat, code_id in owasp_patterns:
                if re.search(pat, code):
                    findings.append(code_id)
            cc_ok = cc <= 7
            lean4_ok = True
            if spec and "sorry" in spec:
                lean4_ok = False
            passed = cc_ok and not findings and lean4_ok
            self._gate_log.append(GateResult(
                gate="pci_verify",
                passed=passed,
                confidence=1.0 if passed else 0.3,
                details={"cc": cc, "findings": findings, "lean4_ok": lean4_ok},
            ))
            return {"cc": cc, "findings": findings, "passed": passed, "lean4_ok": lean4_ok}
        except Exception as exc:
            logging.getLogger(__name__).warning("hook_pci_verify failed: %s", exc)
            return None

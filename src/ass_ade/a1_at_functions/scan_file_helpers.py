"""Tier a1 — assimilated function 'scan_file'

Assimilated from: rebuild/finish.py:94-131
"""

from __future__ import annotations


# --- assimilated symbol ---
def scan_file(path: Path) -> list[IncompleteFunction]:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results: list[IncompleteFunction] = []

    def visit(node: ast.AST, stack: list[str]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fqn = stack + [child.name]
                reason = _body_is_stub(child)
                if reason is not None:
                    results.append(
                        IncompleteFunction(
                            path=path,
                            qualname=".".join(fqn),
                            lineno=child.lineno,
                            end_lineno=child.end_lineno or child.lineno,
                            col_offset=child.col_offset,
                            signature=_signature(source, child),
                            docstring=_docstring(child),
                            reason=reason,
                        )
                    )
                visit(child, fqn)
            elif isinstance(child, ast.ClassDef):
                visit(child, stack + [child.name])
            else:
                visit(child, stack)

    visit(tree, [])
    return results


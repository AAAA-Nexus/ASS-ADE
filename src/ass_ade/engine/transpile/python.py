"""Python->Python 'identity' transpiler.

Uses the standard-library :mod:`ast` module to extract real structure so
Python sources go through the same pipeline as foreign languages without
losing fidelity. The emitted code is the original source (normalized to
LF line endings).
"""

from __future__ import annotations

import ast
from pathlib import Path

from ass_ade.engine.transpile.base import (
    TranspileClass,
    TranspileError,
    TranspileFunction,
    TranspileResult,
    Transpiler,
)


class PythonTranspiler(Transpiler):
    """Identity transpiler for Python sources (used for AST introspection)."""

    language = "python"
    file_extensions = (".py",)

    def transpile_source(
        self,
        source: str,
        *,
        source_path: str | Path | None = None,
    ) -> TranspileResult:
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            raise TranspileError(f"python syntax error: {exc}") from exc

        functions: list[TranspileFunction] = []
        classes: list[TranspileClass] = []
        imports: list[str] = []

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(_extract_function(node))
            elif isinstance(node, ast.ClassDef):
                classes.append(_extract_class(node))
            elif isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for n in node.names:
                    imports.append(f"{mod}.{n.name}" if mod else n.name)

        return TranspileResult(
            source_language="python",
            source_path=str(source_path) if source_path else None,
            python_code=source.replace("\r\n", "\n"),
            functions=tuple(functions),
            classes=tuple(classes),
            imports=tuple(imports),
            backend="ast",
        )


def _extract_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> TranspileFunction:
    params = [a.arg for a in node.args.args]
    if node.args.vararg:
        params.append(f"*{node.args.vararg.arg}")
    if node.args.kwarg:
        params.append(f"**{node.args.kwarg.arg}")
    return TranspileFunction(
        name=node.name,
        params=params,
        return_type=ast.unparse(node.returns) if node.returns else None,
        docstring=ast.get_docstring(node),
        body=ast.unparse(node),
        is_async=isinstance(node, ast.AsyncFunctionDef),
        decorators=tuple(ast.unparse(d) for d in node.decorator_list),
    )


def _extract_class(node: ast.ClassDef) -> TranspileClass:
    bases = tuple(ast.unparse(b) for b in node.bases)
    methods: list[TranspileFunction] = []
    fields: list[str] = []
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            m = _extract_function(item)
            methods.append(
                TranspileFunction(
                    name=m.name,
                    params=m.params,
                    return_type=m.return_type,
                    docstring=m.docstring,
                    body=m.body,
                    is_async=m.is_async,
                    is_method=True,
                    decorators=m.decorators,
                )
            )
        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            fields.append(item.target.id)
        elif isinstance(item, ast.Assign):
            for t in item.targets:
                if isinstance(t, ast.Name):
                    fields.append(t.id)
    return TranspileClass(
        name=node.name,
        bases=bases,
        fields=tuple(fields),
        methods=tuple(methods),
        docstring=ast.get_docstring(node),
    )

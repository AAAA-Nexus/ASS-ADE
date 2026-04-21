"""Tests for the multi-language transpile engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.engine.transpile import (
    SUPPORTED_LANGUAGES,
    TranspileError,
    detect_language,
    get_transpiler,
    transpile_file,
    transpile_source,
    transpile_tree,
)


class TestDetect:
    def test_python(self):
        assert detect_language("mod.py") == "python"

    def test_swift(self):
        assert detect_language("View.swift") == "swift"

    def test_typescript(self):
        assert detect_language("Component.tsx") == "typescript"
        assert detect_language("index.ts") == "typescript"

    def test_javascript(self):
        assert detect_language("bundle.mjs") == "javascript"
        assert detect_language("app.js") == "javascript"

    def test_kotlin(self):
        assert detect_language("Main.kt") == "kotlin"

    def test_rust(self):
        assert detect_language("lib.rs") == "rust"

    def test_unknown(self):
        assert detect_language("README.md") is None

    def test_case_insensitive_extension(self):
        assert detect_language("Foo.PY") == "python"

    def test_supported_covers_registry(self):
        for lang in SUPPORTED_LANGUAGES:
            get_transpiler(lang)


class TestSwift:
    SOURCE = '''\
import Foundation
public struct Point {
    let x: Int
    let y: Int
    func distance(to other: Point) -> Double {
        return 0.0
    }
}
public func greet(name: String) -> String {
    return "Hello, " + name
}
'''

    def test_imports(self):
        r = transpile_source(self.SOURCE, language="swift")
        assert "Foundation" in r.imports

    def test_struct_fields(self):
        r = transpile_source(self.SOURCE, language="swift")
        names = [c.name for c in r.classes]
        assert "Point" in names

    def test_top_level_function_not_duplicated_as_method(self):
        r = transpile_source(self.SOURCE, language="swift")
        fn_names = [f.name for f in r.functions]
        assert fn_names == ["greet"]

    def test_class_method_present(self):
        r = transpile_source(self.SOURCE, language="swift")
        point = next(c for c in r.classes if c.name == "Point")
        assert any(m.name == "distance" for m in point.methods)

    def test_python_output_is_valid_python(self):
        import ast

        r = transpile_source(self.SOURCE, language="swift")
        ast.parse(r.python_code)

    def test_type_mapping(self):
        r = transpile_source(self.SOURCE, language="swift")
        greet = next(f for f in r.functions if f.name == "greet")
        assert greet.return_type == "String"


class TestTypeScript:
    SOURCE = '''\
import { readFile } from "fs/promises";
export class Widget extends Base implements Drawable {
    readonly id: string;
    label: string = "";
    constructor(id: string) { this.id = id; }
    async render(ctx: Ctx): Promise<string> { return ""; }
}
export function add(a: number, b: number): number { return a + b; }
const mul = async (a: number, b: number): Promise<number> => { return a * b; };
'''

    def test_class_extraction(self):
        r = transpile_source(self.SOURCE, language="typescript")
        names = [c.name for c in r.classes]
        assert "Widget" in names

    def test_class_inheritance(self):
        r = transpile_source(self.SOURCE, language="typescript")
        w = next(c for c in r.classes if c.name == "Widget")
        assert "Base" in w.bases
        assert "Drawable" in w.bases

    def test_top_level_functions_not_duplicated(self):
        r = transpile_source(self.SOURCE, language="typescript")
        fn_names = sorted(f.name for f in r.functions)
        assert fn_names == ["add", "mul"]

    def test_arrow_function_detected_as_async(self):
        r = transpile_source(self.SOURCE, language="typescript")
        mul = next(f for f in r.functions if f.name == "mul")
        assert mul.is_async is True

    def test_python_output_valid(self):
        import ast

        r = transpile_source(self.SOURCE, language="typescript")
        ast.parse(r.python_code)


class TestKotlin:
    SOURCE = '''\
package com.example
import kotlinx.coroutines.Deferred
class Service(private val repo: Repo) : BaseService() {
    suspend fun fetch(id: Int): User {
        return repo.get(id)
    }
    fun total(): Int {
        return 42
    }
}
'''

    def test_class_and_methods(self):
        r = transpile_source(self.SOURCE, language="kotlin")
        svc = next(c for c in r.classes if c.name == "Service")
        names = [m.name for m in svc.methods]
        assert "fetch" in names
        assert "total" in names

    def test_suspend_detected_as_async(self):
        r = transpile_source(self.SOURCE, language="kotlin")
        svc = next(c for c in r.classes if c.name == "Service")
        fetch = next(m for m in svc.methods if m.name == "fetch")
        assert fetch.is_async is True

    def test_top_level_functions_empty(self):
        r = transpile_source(self.SOURCE, language="kotlin")
        assert [f.name for f in r.functions] == []

    def test_python_output_valid(self):
        import ast

        r = transpile_source(self.SOURCE, language="kotlin")
        ast.parse(r.python_code)


class TestRust:
    SOURCE = '''\
use std::collections::HashMap;
pub struct Counter { pub value: i64, step: i32, }
pub fn inc(c: &mut Counter, n: i32) -> i64 {
    c.value + n as i64
}
pub async fn fetch(url: String) -> String { url }
'''

    def test_struct_fields(self):
        r = transpile_source(self.SOURCE, language="rust")
        counter = next(c for c in r.classes if c.name == "Counter")
        assert "value" in counter.fields
        assert "step" in counter.fields

    def test_top_level_functions(self):
        r = transpile_source(self.SOURCE, language="rust")
        names = sorted(f.name for f in r.functions)
        assert names == ["fetch", "inc"]

    def test_async_detected(self):
        r = transpile_source(self.SOURCE, language="rust")
        fetch = next(f for f in r.functions if f.name == "fetch")
        assert fetch.is_async is True

    def test_import_use_statements(self):
        r = transpile_source(self.SOURCE, language="rust")
        assert any("std" in imp for imp in r.imports)

    def test_python_output_valid(self):
        import ast

        r = transpile_source(self.SOURCE, language="rust")
        ast.parse(r.python_code)


class TestPythonIdentity:
    SOURCE = '''\
from __future__ import annotations
import json

def foo(x: int) -> int:
    """Double x."""
    return x * 2

class Bar:
    """A bar."""
    name: str = ""
    def greet(self, who: str) -> str:
        return f"hi {who}"
'''

    def test_uses_ast_backend(self):
        r = transpile_source(self.SOURCE, language="python")
        assert r.backend == "ast"

    def test_function_extracted(self):
        r = transpile_source(self.SOURCE, language="python")
        foo = next(f for f in r.functions if f.name == "foo")
        assert foo.docstring == "Double x."
        assert foo.return_type == "int"

    def test_class_extracted(self):
        r = transpile_source(self.SOURCE, language="python")
        bar = next(c for c in r.classes if c.name == "Bar")
        assert bar.docstring == "A bar."
        assert any(m.name == "greet" for m in bar.methods)


class TestDispatch:
    def test_unknown_language(self):
        with pytest.raises(TranspileError):
            get_transpiler("cobol")

    def test_transpile_file_missing(self, tmp_path):
        with pytest.raises(TranspileError):
            transpile_file(tmp_path / "nope.swift")

    def test_transpile_file_writes_output(self, tmp_path):
        src = tmp_path / "hello.swift"
        src.write_text("public func hi() -> String { return \"hi\" }\n", encoding="utf-8")
        out = tmp_path / "out" / "hello.py"
        result = transpile_file(src, output_path=out)
        assert out.exists()
        assert "from __future__ import annotations" in out.read_text(encoding="utf-8")
        assert result.source_language == "swift"

    def test_transpile_file_language_override(self, tmp_path):
        src = tmp_path / "weird.txt"
        src.write_text("fun go(): Int { return 0 }\n", encoding="utf-8")
        result = transpile_file(src, language="kotlin")
        assert result.source_language == "kotlin"

    def test_transpile_tree_mirrors_structure(self, tmp_path):
        (tmp_path / "a").mkdir()
        (tmp_path / "a" / "one.swift").write_text(
            "public func f() -> Int { return 1 }\n", encoding="utf-8"
        )
        (tmp_path / "a" / "two.ts").write_text(
            "export function g(): number { return 2; }\n", encoding="utf-8"
        )
        (tmp_path / "README.md").write_text("# readme\n", encoding="utf-8")
        out = tmp_path / "out"
        results = transpile_tree(tmp_path, output_root=out, exclude=(".git", "out"))
        assert (out / "a" / "one.py").exists()
        assert (out / "a" / "two.py").exists()
        assert not (out / "README.md").exists()
        assert len(results) == 2

    def test_transpile_tree_language_filter(self, tmp_path):
        (tmp_path / "x.swift").write_text(
            "public func f() -> Int { return 1 }\n", encoding="utf-8"
        )
        (tmp_path / "x.rs").write_text(
            "pub fn g() -> i32 { 2 }\n", encoding="utf-8"
        )
        out = tmp_path / "out"
        results = transpile_tree(
            tmp_path, output_root=out, languages=("swift",), exclude=("out",)
        )
        assert len(results) == 1
        assert next(iter(results)).endswith(".swift")


class TestEmissionShape:
    """Lock in the shape of the generated Python so downstream tooling stays stable."""

    def test_header_mentions_source_language(self):
        r = transpile_source("public func f() {}", language="swift")
        assert "Auto-transpiled from swift" in r.python_code

    def test_empty_source_yields_hint(self):
        r = transpile_source("", language="rust")
        assert "No top-level declarations extracted" in r.python_code

    def test_python_output_always_imports_annotations(self):
        for lang, sample in [
            ("swift", "public func f() -> Int { return 0 }"),
            ("typescript", "export function f(): number { return 0; }"),
            ("kotlin", "fun f(): Int { return 0 }"),
            ("rust", "pub fn f() -> i32 { 0 }"),
        ]:
            r = transpile_source(sample, language=lang)
            assert "from __future__ import annotations" in r.python_code

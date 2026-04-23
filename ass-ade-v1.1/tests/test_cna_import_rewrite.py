"""CNA import index and cross-root ``from … import …`` rewrite."""

from __future__ import annotations

import ast
import unittest.mock
from pathlib import Path

import pytest

import ass_ade_v11.a1_at_functions.cna_import_rewrite as cna
from ass_ade_v11.a1_at_functions.cna_import_rewrite import (
    CNAImportTarget,
    assimilate_component_body,
    build_cna_import_index,
    resolve_import_from_module,
    resolve_import_from_module_any,
    rewrite_python_imports_in_body,
)
from ass_ade_v11.a3_og_features.pipeline_book import run_book_until


def test_partial_import_from_keeps_unmapped_names_on_original_module(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def foo() -> None: ...\ndef bar() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "c1",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    body = "from pkg.util import foo, bar\n\nx = foo()\n"
    out, stats = rewrite_python_imports_in_body(
        body, source_roots=[tmp_path], index=index
    )
    assert stats.get("imports_rewritten") == 1
    assert "from a1_at_functions.c1 import foo" in out
    assert "from pkg.util import bar" in out


def test_assimilate_dedupes_prepend_and_inline_same_import(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def foo() -> int:\n    return 1\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "entry",
                "tier": "a1_at_functions",
                "name": "main",
                "source_symbol": {"path": str(tmp_path / "app" / "main.py"), "name": "main"},
                "imports": ["pkg.util.foo"],
                "body": "from pkg.util import foo\n\ndef main() -> int:\n    return foo()\n",
            },
            {
                "id": "util_comp",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            },
        ]
    }
    main = tmp_path / "app" / "main.py"
    main.parent.mkdir(parents=True)
    main.write_text("def main(): pass\n", encoding="utf-8")
    entry_prop = next(p for p in plan["proposed_components"] if p["id"] == "entry")
    body = str(entry_prop["body"])
    final, _ = assimilate_component_body(
        body, entry_prop, gap_plan=plan, source_roots=[tmp_path]
    )
    assert final.count("from a1_at_functions.util_comp import foo") == 1
    assert "from pkg.util import foo" not in final


def test_plain_import_rewrites_when_single_cna_target_per_file(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def add_one(x: int) -> int:\n    return x + 1\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "util_c",
                "tier": "a1_at_functions",
                "name": "add_one",
                "source_symbol": {"path": str(util.resolve()), "name": "add_one"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    body = "import pkg.util\n\n\ndef f() -> int:\n    return util.add_one(1)\n"
    out, stats = rewrite_python_imports_in_body(
        body, source_roots=[tmp_path], index=index
    )
    assert stats.get("import_stmt_rewritten") == 1
    assert "import a1_at_functions.util_c as util" in out
    assert "pkg.util" not in out


def test_relative_import_from_rewrites_with_owning_path(tmp_path: Path) -> None:
    app = tmp_path / "app_pkg"
    app.mkdir(parents=True)
    entry = app / "entry.py"
    util = app / "util.py"
    util.write_text(
        "def add_one(value: int) -> int:\n    return value + 1\n", encoding="utf-8"
    )
    entry.write_text("def run() -> int: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "entry_c",
                "tier": "a1_at_functions",
                "name": "run",
                "source_symbol": {"path": str(entry.resolve()), "name": "run"},
            },
            {
                "id": "util_c",
                "tier": "a1_at_functions",
                "name": "add_one",
                "source_symbol": {"path": str(util.resolve()), "name": "add_one"},
            },
        ]
    }
    index = build_cna_import_index(plan)
    body = "from .util import add_one\n\ndef run() -> int:\n    return add_one(2)\n"
    out, stats = rewrite_python_imports_in_body(
        body,
        source_roots=[tmp_path],
        index=index,
        owning_source_file=str(entry.resolve()),
    )
    assert stats.get("imports_rewritten") == 1
    assert "from a1_at_functions.util_c import add_one" in out
    assert ".util import" not in out


def test_star_import_expands_to_indexed_symbols(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text(
        "def foo() -> int:\n    return 1\n\ndef bar() -> int:\n    return 2\n",
        encoding="utf-8",
    )
    plan = {
        "proposed_components": [
            {
                "id": "c_foo",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            },
            {
                "id": "c_bar",
                "tier": "a1_at_functions",
                "name": "bar",
                "source_symbol": {"path": str(util.resolve()), "name": "bar"},
            },
        ]
    }
    index = build_cna_import_index(plan)
    body = "from pkg.util import *\n\nx = foo() + bar()\n"
    out, stats = rewrite_python_imports_in_body(
        body, source_roots=[tmp_path], index=index
    )
    assert stats.get("star_expanded") == 1
    assert "from a1_at_functions.c_foo import foo" in out
    assert "from a1_at_functions.c_bar import bar" in out
    assert "import *" not in out


def test_plain_import_unchanged_when_multiple_components_share_file(
    tmp_path: Path,
) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def foo() -> None: ...\ndef bar() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "c1",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            },
            {
                "id": "c2",
                "tier": "a1_at_functions",
                "name": "bar",
                "source_symbol": {"path": str(util.resolve()), "name": "bar"},
            },
        ]
    }
    index = build_cna_import_index(plan)
    body = "import pkg.util\n"
    out, stats = rewrite_python_imports_in_body(
        body, source_roots=[tmp_path], index=index
    )
    assert stats.get("import_stmt_rewritten", 0) == 0
    assert out.strip() == body.strip()


def test_build_cna_import_index_skips_incomplete_rows() -> None:
    plan = {
        "proposed_components": [
            {"id": "x", "tier": "a1_at_functions", "name": "n", "source_symbol": {"path": "", "name": "n"}},
            {"id": "y", "name": "only", "source_symbol": {"path": "/a.py", "name": "only"}},
        ]
    }
    assert build_cna_import_index(plan) == {}


def test_norm_path_oserror_falls_back_to_str() -> None:
    with unittest.mock.patch("pathlib.Path.resolve", side_effect=OSError("boom")):
        assert cna._norm_path("anything") == "anything"


def test_candidate_module_files_finds_init_without_stub_py(tmp_path: Path) -> None:
    pkg = tmp_path / "nest" / "pkg"
    pkg.mkdir(parents=True)
    init_f = pkg / "__init__.py"
    init_f.write_text('"""pkg"""\n', encoding="utf-8")
    found = cna._candidate_module_files("nest.pkg", tmp_path)
    assert init_f.resolve() in [p.resolve() for p in found]


def test_resolve_import_from_module_stdlib_and_miss(tmp_path: Path) -> None:
    assert resolve_import_from_module("json", "loads", index={}, source_roots=[tmp_path]) is None
    util = tmp_path / "u.py"
    util.write_text("x=1\n", encoding="utf-8")
    index = {("no_match", "x"): CNAImportTarget("a1", "s", "c", "x")}
    assert (
        resolve_import_from_module("u", "nope", index=index, source_roots=[tmp_path]) is None
    )


def test_relative_base_dir_level_gt_one(tmp_path: Path) -> None:
    deep = tmp_path / "a" / "b" / "c" / "here.py"
    deep.parent.mkdir(parents=True)
    deep.write_text("pass\n", encoding="utf-8")
    base = cna._relative_base_dir(deep, 3)
    assert base.resolve() == (tmp_path / "a").resolve()


def test_paths_for_relative_module_package_init(tmp_path: Path) -> None:
    app = tmp_path / "app"
    sub = app / "subpkg"
    sub.mkdir(parents=True)
    (sub / "__init__.py").write_text("def f(): ...\n", encoding="utf-8")
    here = app / "here.py"
    here.write_text("pass\n", encoding="utf-8")
    paths = cna._paths_for_relative_module(here, 1, "subpkg")
    assert paths and paths[0].name == "__init__.py"


def test_paths_for_import_from_edges(tmp_path: Path) -> None:
    assert cna._paths_for_import_from("m", 1, owning_py=None, source_roots=[tmp_path]) == []
    assert cna._paths_for_import_from(None, 0, owning_py=None, source_roots=[tmp_path]) == []


def test_resolve_import_from_module_any_edges(tmp_path: Path) -> None:
    assert resolve_import_from_module_any(None, "x", 1, owning_source=None, index={}, source_roots=[]) is None
    util = tmp_path / "json.py"
    util.write_text("def x(): ...\n", encoding="utf-8")
    here = tmp_path / "here.py"
    here.write_text("pass\n", encoding="utf-8")
    assert (
        resolve_import_from_module_any(
            "json", "x", 1, owning_source=here, index={}, source_roots=[tmp_path]
        )
        is None
    )
    assert (
        resolve_import_from_module_any("json", "x", 0, owning_source=here, index={}, source_roots=[tmp_path])
        is None
    )


def test_parse_flat_import_ref_variants() -> None:
    assert cna._parse_flat_import_ref("") is None
    assert cna._parse_flat_import_ref("nope") is None
    assert cna._parse_flat_import_ref(".bad") is None
    assert cna._parse_flat_import_ref("mod.1bad") is None
    assert cna._parse_flat_import_ref("not.valid") is None  # keyword segment


def test_rewriter_owning_resolve_oserror(tmp_path: Path) -> None:
    with unittest.mock.patch("pathlib.Path.resolve", side_effect=OSError("nope")):
        rw = cna._AssimilateImportRewriter({}, [tmp_path], {"imports_rewritten": 0}, tmp_path / "x.py")
        assert rw._owning == tmp_path / "x.py"


def test_plain_import_alias_variants(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def f() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "u",
                "tier": "a1_at_functions",
                "name": "f",
                "source_symbol": {"path": str(util.resolve()), "name": "f"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    out_as, st_as = rewrite_python_imports_in_body(
        "import pkg.util as pu\n", source_roots=[tmp_path], index=index
    )
    assert st_as.get("import_stmt_rewritten") == 1
    assert "as pu" in out_as


def test_visit_import_mixed_stdlib_and_rewrite(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def g() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "uc",
                "tier": "a1_at_functions",
                "name": "g",
                "source_symbol": {"path": str(util.resolve()), "name": "g"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    body = "import os, pkg.util\n"
    out, stats = rewrite_python_imports_in_body(body, source_roots=[tmp_path], index=index)
    assert stats.get("import_stmt_rewritten") == 1
    assert "import os" in out
    assert "a1_at_functions.uc" in out


def test_visit_import_no_resolve_path_keeps_module(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def g() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "uc",
                "tier": "a1_at_functions",
                "name": "g",
                "source_symbol": {"path": str(util.resolve()), "name": "g"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    out, stats = rewrite_python_imports_in_body(
        "import missing.mod, pkg.util\n", source_roots=[tmp_path], index=index
    )
    assert stats.get("import_stmt_rewritten") == 1
    assert "missing.mod" in out


def test_relative_only_submodule_package_import(tmp_path: Path) -> None:
    app = tmp_path / "app"
    sub = app / "subpkg"
    sub.mkdir(parents=True)
    (sub / "__init__.py").write_text("def h() -> int: return 1\n", encoding="utf-8")
    entry = app / "entry.py"
    entry.write_text("def run() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "e",
                "tier": "a1_at_functions",
                "name": "run",
                "source_symbol": {"path": str(entry.resolve()), "name": "run"},
            },
            {
                "id": "sp",
                "tier": "a1_at_functions",
                "name": "h",
                "source_symbol": {"path": str((sub / "__init__.py").resolve()), "name": "h"},
            },
        ]
    }
    index = build_cna_import_index(plan)
    out, stats = rewrite_python_imports_in_body(
        "from . import subpkg\n",
        source_roots=[tmp_path],
        index=index,
        owning_source_file=str(entry.resolve()),
    )
    assert stats.get("import_stmt_rewritten") == 1
    assert "a1_at_functions.sp" in out


def test_expand_star_no_paths_and_star_relative_without_owning(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def a() -> int: return 1\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "ca",
                "tier": "a1_at_functions",
                "name": "a",
                "source_symbol": {"path": str(util.resolve()), "name": "a"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    out1, st1 = rewrite_python_imports_in_body(
        "from pkg.nope import *\n", source_roots=[tmp_path], index=index
    )
    assert st1.get("star_expanded", 0) == 0
    assert out1.strip() == "from pkg.nope import *"
    app = tmp_path / "app2"
    app.mkdir()
    (app / "x.py").write_text("pass\n", encoding="utf-8")
    out2, _ = rewrite_python_imports_in_body(
        "from .util import *\n",
        source_roots=[tmp_path],
        index=index,
        owning_source_file=None,
    )
    assert "import *" in out2


def test_from_import_all_unmapped_returns_node(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def foo() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "c1",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    body = "from pkg.util import not_in_index\n"
    out, stats = rewrite_python_imports_in_body(body, source_roots=[tmp_path], index=index)
    assert stats.get("imports_rewritten", 0) == 0
    assert out.strip() == body.strip()


def test_visit_import_from_manual_module_none_level_zero() -> None:
    rw = cna._AssimilateImportRewriter(
        {}, [Path(".")], {"imports_rewritten": 0}, None
    )
    node = ast.ImportFrom(module=None, names=[ast.alias(name="x")], level=0)
    ast.fix_missing_locations(node)
    assert rw.visit_ImportFrom(node) is node


def test_rewrite_python_imports_syntax_error_and_unparse_fallback(tmp_path: Path) -> None:
    out_err, st_err = rewrite_python_imports_in_body("def bad\n", source_roots=[tmp_path], index={})
    assert st_err.get("ast_error") == 1
    assert out_err == "def bad\n"
    with unittest.mock.patch.object(ast, "unparse", side_effect=AttributeError("old py")):
        out_u, st_u = rewrite_python_imports_in_body("x = 1\n", source_roots=[tmp_path], index={})
    assert st_u.get("no_unparse") == 1
    assert out_u == "x = 1\n"


def test_rewrite_owning_file_resolve_oserror(tmp_path: Path) -> None:
    ghost = tmp_path / "ghost.py"
    real_resolve = Path.resolve

    def _sel_resolve(self: Path, *args: object, **kwargs: object) -> Path:
        if self.name == "ghost.py":
            raise OSError("bad")
        return real_resolve(self, *args, **kwargs)

    with unittest.mock.patch.object(Path, "resolve", _sel_resolve):
        out, stats = rewrite_python_imports_in_body(
            "x = 1\n",
            source_roots=[tmp_path],
            index={},
            owning_source_file=str(ghost),
        )
    assert out.strip() == "x = 1"
    assert stats.get("body_changed", 0) in (0, 1)


def test_build_prepended_import_lines_branches(tmp_path: Path) -> None:
    util = tmp_path / "pkg" / "util.py"
    util.parent.mkdir(parents=True)
    util.write_text("def foo() -> None: ...\n", encoding="utf-8")
    plan = {
        "proposed_components": [
            {
                "id": "u",
                "tier": "a1_at_functions",
                "name": "foo",
                "source_symbol": {"path": str(util.resolve()), "name": "foo"},
            }
        ]
    }
    index = build_cna_import_index(plan)
    prop: dict = {
        "imports": [
            42,
            "not.valid",
            "json.loads",
            "pkg.util.foo",
            "pkg.util.foo",
            "pkg.util.nope",
        ]
    }
    lines, pst = cna.build_prepended_import_lines(
        prop, owning_source_file=str(util), index=index, source_roots=[tmp_path]
    )
    assert "from a1_at_functions.u import foo" in lines
    assert pst["prepended"] == 1
    assert pst["unresolved"] == 1


def test_dedupe_duplicate_import_lines() -> None:
    text = "from a.b import c\nfrom a.b import c\nimport d\nimport d\n"
    deduped = cna._dedupe_from_import_lines(text)
    assert deduped.count("from a.b import c") == 1
    assert deduped.count("import d") == 1


def test_assimilate_skips_without_roots_or_body(tmp_path: Path) -> None:
    prop = {"source_symbol": {"path": str(tmp_path / "a.py"), "name": "x"}}
    same, rec = assimilate_component_body("", prop, gap_plan={"proposed_components": []}, source_roots=[])
    assert rec.get("skipped") is True
    assert same == ""


def test_cross_fixture_materialize_rewrites_lib_pkg_import(tmp_path: Path) -> None:
    cross_app = Path(__file__).resolve().parent / "fixtures" / "cross_app"
    cross_lib = Path(__file__).resolve().parent / "fixtures" / "cross_lib"
    book = run_book_until(
        cross_app,
        tmp_path,
        extra_source_roots=[cross_lib],
        stop_after=5,
        rebuild_tag="cross-rewrite",
    )
    assert book["stopped_after"] == 5
    root = Path(book["phase5"]["target_root"])
    entry_files = list(root.glob("**/a1_source_cross_app_run_add.py"))
    assert len(entry_files) == 1
    text = entry_files[0].read_text(encoding="utf-8")
    assert "lib_pkg" not in text
    assert "from a1_at_functions.a1_source_cross_lib_add_one import add_one" in text

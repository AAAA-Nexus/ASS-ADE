"""Tier a2 — Typer CLI introspection.

Walks a Typer app's registered commands and returns a list of JSON-schema-ish
dicts describing each command's name, help text, and parameters. The dashboard
uses this to auto-generate forms for the ⌘K command palette, so new commands
added to the CLI appear in the UI with zero extra code.
"""

from __future__ import annotations

import inspect
import typing
from pathlib import Path
from typing import Any

import typer
from typer.models import ArgumentInfo, OptionInfo


def _unwrap_annotated(annotation: Any) -> tuple[Any, tuple[Any, ...]]:
    """Return (base_type, metadata_tuple) for an Annotated[T, *meta]; else (T, ())."""
    origin = typing.get_origin(annotation)
    if origin is typing.Annotated or (hasattr(typing, "_AnnotatedAlias") and type(annotation).__name__ == "_AnnotatedAlias"):
        args = typing.get_args(annotation)
        if args:
            return args[0], args[1:]
    return annotation, ()


def _type_to_schema(t: Any) -> dict:
    """Map a Python type annotation to a small JSON-schema-ish dict."""
    if t is inspect.Parameter.empty or t is None:
        return {"type": "string"}

    # Optional[X] / Union[X, None] / PEP 604: X | None
    import types as _types  # local to avoid polluting module namespace
    origin = typing.get_origin(t)
    if origin is typing.Union or origin is getattr(_types, "UnionType", None):
        args = [a for a in typing.get_args(t) if a is not type(None)]
        if args:
            schema = _type_to_schema(args[0])
            schema["nullable"] = True
            return schema

    if t is str:
        return {"type": "string"}
    if t is int:
        return {"type": "integer"}
    if t is float:
        return {"type": "number"}
    if t is bool:
        return {"type": "boolean"}
    if t is Path or (isinstance(t, type) and issubclass(t, Path)):
        return {"type": "string", "format": "path"}

    return {"type": "string"}


def _serialize_default(value: Any) -> Any:
    """Make a default value JSON-safe."""
    if value is inspect.Parameter.empty:
        return None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    try:
        import json
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return str(value)


def _option_flags(opt: OptionInfo) -> list[str]:
    """Extract all flag strings from an OptionInfo (both ``default`` and ``param_decls``)."""
    flags: list[str] = []
    # Typer stores the first positional arg in ``default`` when it's a flag string
    first = opt.default
    if isinstance(first, str) and first.startswith("-"):
        flags.append(first)
    for decl in opt.param_decls or ():
        if isinstance(decl, str) and decl.startswith("-") and decl not in flags:
            flags.append(decl)
    return flags


def _param_from_signature(pname: str, param: inspect.Parameter) -> dict:
    base_type, meta = _unwrap_annotated(param.annotation)
    schema = _type_to_schema(base_type)
    schema["name"] = pname

    default = param.default
    param_kind = "option"
    help_text = ""
    flag_names: list[str] = []

    # Typer metadata may live in Annotated[...] OR in the parameter default.
    typer_info: ArgumentInfo | OptionInfo | None = None
    for m in meta:
        if isinstance(m, (ArgumentInfo, OptionInfo)):
            typer_info = m
            break
    is_annotated_style = typer_info is not None
    if typer_info is None and isinstance(default, (ArgumentInfo, OptionInfo)):
        typer_info = default

    if isinstance(typer_info, ArgumentInfo):
        param_kind = "argument"
        help_text = typer_info.help or ""
    elif isinstance(typer_info, OptionInfo):
        param_kind = "option"
        help_text = typer_info.help or ""
        flag_names = _option_flags(typer_info)

    # Resolve the actual Python default:
    # - Annotated style: the real default is on inspect.Parameter.default
    # - Classic style:   the real default is typer_info.default (but only if it's
    #                    not a flag-string for OptionInfo)
    real_default: Any = inspect.Parameter.empty
    if is_annotated_style:
        if default is not inspect.Parameter.empty and not isinstance(default, (ArgumentInfo, OptionInfo)):
            real_default = default
    else:
        if isinstance(typer_info, ArgumentInfo):
            if typer_info.default is not ... and typer_info.default is not inspect.Parameter.empty:
                real_default = typer_info.default
        elif isinstance(typer_info, OptionInfo):
            candidate = typer_info.default
            if not (isinstance(candidate, str) and candidate.startswith("-")):
                if candidate is not ... and candidate is not inspect.Parameter.empty:
                    real_default = candidate

    if real_default is not inspect.Parameter.empty:
        schema["default"] = _serialize_default(real_default)

    schema["kind"] = param_kind
    schema["help"] = help_text
    if flag_names:
        schema["flags"] = flag_names
    schema["required"] = (
        "default" not in schema
        and not schema.get("nullable", False)
    )
    return schema


def _resolve_annotations(fn: Any) -> dict[str, Any]:
    """Best-effort type-hint resolution that respects ``from __future__ import annotations``.

    Falls back to raw annotations if the function's globals can't satisfy forward references.
    """
    try:
        return typing.get_type_hints(fn, include_extras=True)
    except Exception:
        try:
            return dict(getattr(fn, "__annotations__", {}))
        except Exception:
            return {}


def introspect_typer_app(app: typer.Typer) -> list[dict]:
    """Return one schema dict per registered command, sorted by name."""
    commands: list[dict] = []
    for cmd_info in app.registered_commands:
        fn = cmd_info.callback
        if fn is None:
            continue
        name = cmd_info.name or fn.__name__.replace("_", "-")
        if cmd_info.hidden:
            continue
        doc = inspect.getdoc(fn) or ""
        summary = cmd_info.help or (doc.splitlines()[0] if doc else "")
        params: list[dict] = []
        try:
            sig = inspect.signature(fn)
        except (TypeError, ValueError):
            sig = None
        resolved = _resolve_annotations(fn)
        if sig is not None:
            for pname, p in sig.parameters.items():
                if pname in ("self", "ctx"):
                    continue
                # Replace stringified annotation with the resolved type, if available
                effective = p
                if pname in resolved and resolved[pname] is not p.annotation:
                    effective = p.replace(annotation=resolved[pname])
                try:
                    params.append(_param_from_signature(pname, effective))
                except Exception:
                    params.append({"name": pname, "type": "string", "kind": "option", "help": ""})

        commands.append({
            "name": name,
            "summary": summary.strip(),
            "doc": doc,
            "params": params,
        })
    return sorted(commands, key=lambda c: c["name"])


def categorize_commands(commands: list[dict]) -> dict[str, list[dict]]:
    """Group commands into dashboard categories by naming convention."""
    groups: dict[str, list[dict]] = {
        "Core": [],
        "Scout & Assimilate": [],
        "Memory & Agent": [],
        "Nexus": [],
        "Ops": [],
        "Other": [],
    }
    for cmd in commands:
        name = cmd["name"].lower()
        if name in {"scout", "cherry-pick", "assimilate", "phase0-recon", "map-terrain"}:
            groups["Scout & Assimilate"].append(cmd)
        elif any(n in name for n in ("memory", "remember", "personality", "skill", "chat", "interpret")):
            groups["Memory & Agent"].append(cmd)
        elif "nexus" in name or name.startswith("trust"):
            groups["Nexus"].append(cmd)
        elif any(n in name for n in ("version", "doctor", "config", "status", "ui", "login")):
            groups["Core"].append(cmd)
        elif any(n in name for n in ("lora", "certify", "audit", "lineage")):
            groups["Ops"].append(cmd)
        else:
            groups["Other"].append(cmd)
    return {k: v for k, v in groups.items() if v}

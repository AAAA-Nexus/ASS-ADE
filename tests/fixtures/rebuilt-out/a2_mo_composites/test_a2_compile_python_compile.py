"""Pytest for a2_mo_composites ExampleService composite."""

import sys
import types
import importlib.util
import pytest

# Dynamically import the ExampleService from the rebuilt-out composite
spec = importlib.util.spec_from_file_location(
    "a2_compile_python_compile",
    "c:/!aaaa-nexus/!ass-ade/ass-ade-v1.1/tests/fixtures/rebuilt-out/a2_mo_composites/a2_compile_python_compile.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Patch: The class may not be properly indented in the rebuilt file, so we check for it
ExampleService = getattr(mod, "ExampleService", None)


def test_example_service_run():
    """Test ExampleService.run returns 'ok'."""
    assert ExampleService is not None, "ExampleService class missing in composite"
    inst = ExampleService()
    assert hasattr(inst, "run"), "run method missing in ExampleService"
    assert inst.run() == "ok"

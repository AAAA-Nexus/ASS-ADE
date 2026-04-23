from __future__ import annotations


def test_a4_main_module_importable() -> None:
    import ass_ade_v11.a4_sy_orchestration.__main__ as m

    assert hasattr(m, "main")

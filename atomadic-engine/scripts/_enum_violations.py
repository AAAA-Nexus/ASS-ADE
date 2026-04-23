import ast, sys
from pathlib import Path
sys.path.insert(0, 'tests')
from test_monadic_purity import (
    _load_tier_map, _classify_import, _iter_imports,
    _TIER_ORDER, _SRC, _IMPURE_MODULES,
)
tm = _load_tier_map()
ups, a1s = [], []
for rel, self_tier in tm.items():
    p = _SRC / rel
    if not p.exists():
        continue
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError:
        continue
    for imp in _iter_imports(tree):
        ot = _classify_import(imp)
        if ot and _TIER_ORDER[ot] > _TIER_ORDER[self_tier]:
            ups.append(f"{rel}->{imp}")
        root = imp.split(".")[0]
        if self_tier == "a1" and (root in _IMPURE_MODULES or imp in _IMPURE_MODULES):
            a1s.append(f"{rel}->{imp}")
print("UPWARD:", len(ups))
for v in sorted(set(ups)):
    print(" ", v)
print("A1_IMPURE:", len(a1s))
for v in sorted(set(a1s)):
    print(" ", v)

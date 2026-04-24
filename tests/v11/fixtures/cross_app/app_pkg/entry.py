"""Entry that imports from lib_pkg on a sibling source root."""

from lib_pkg.util import add_one


def run_add() -> int:
    return add_one(41)

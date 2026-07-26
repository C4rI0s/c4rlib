"""Import integrity — the failure mode that breaks every user at once.

A broken ``__init__`` or a name in ``__all__`` that no longer exists ships a
package that cannot even be imported. These tests are cheap and catch it.
"""
import importlib
import re
from pathlib import Path

import pytest

import c4rlib

MODULES = [
    "animations", "ascii", "audio", "banners", "colors", "console", "crypto",
    "discord", "files", "fx", "http", "interactive", "logger", "text", "utils",
]


@pytest.mark.parametrize("name", MODULES)
def test_submodule_imports(name):
    importlib.import_module(f"c4rlib.{name}")


def test_all_names_are_exported():
    missing = [n for n in c4rlib.__all__ if not hasattr(c4rlib, n)]
    assert not missing, f"__all__ lists names absent from the package: {missing}"


def test_all_has_no_duplicates():
    assert len(c4rlib.__all__) == len(set(c4rlib.__all__))


def test_version_matches_pyproject():
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    if not pyproject.exists():          # installed wheel, no source tree
        pytest.skip("pyproject.toml not present (running against installed dist)")
    text = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    assert match, "no version field found in pyproject.toml"
    assert c4rlib.__version__ == match.group(1), (
        f"__init__.py says {c4rlib.__version__}, pyproject.toml says {match.group(1)}"
    )


def test_metadata_present():
    assert c4rlib.__license__ == "MIT"
    assert c4rlib.__author__

"""Shared helpers for song-team unit tests."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def load_script(name: str):
    """Import ``song-team/scripts/<name>.py`` as a fresh module object."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def mixed_path(path: str) -> str:
    """On Windows return a genuinely mixed-separator path (first ``/`` -> ``\\``);
    on POSIX return the plain path."""
    if sys.platform.startswith("win"):
        return Path(path).as_posix().replace("/", "\\", 1)
    return path

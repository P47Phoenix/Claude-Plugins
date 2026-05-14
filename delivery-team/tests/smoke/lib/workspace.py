"""Isolated workspace: mktemp workdir + plugin install + scrub on exit.

Note (D-tk5-04 fix, BACKLOG-107): the subprocess env preserves the parent
process's HOME so Claude Code's credential lookup at ``~/.claude/.credentials.json``
(or system keychain) keeps working. Isolation is achieved via cwd + XDG_*
overrides + ``CLAUDE_PROJECT_DIR``, NOT via HOME override.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


PLUGIN_LOAD_PLUGIN_DIR = "plugin-dir"
PLUGIN_LOAD_COPY_INTO_HOME = "copy-into-home"


@dataclass
class Workspace:
    """One smoke-run sandbox: tmpdir HOME, plugin install, minimal config."""

    repo_root: Path
    plugin_path: Path
    config_fixture: Path
    home: Optional[Path] = None
    workdir: Optional[Path] = None
    plugin_load_strategy: Optional[str] = None
    _setup_done: bool = field(default=False, init=False)

    def setup(self) -> None:
        """Create isolated HOME, plant `.delivery/`, install plugin (probe + fallback)."""
        if self._setup_done:
            return

        tmp_root = Path(tempfile.mkdtemp(prefix="smoke-"))
        self.home = tmp_root
        self.workdir = tmp_root / "work"
        self.workdir.mkdir(parents=True, exist_ok=True)

        (tmp_root / ".claude").mkdir(parents=True, exist_ok=True)

        delivery_root = self.workdir / ".delivery"
        delivery_root.mkdir(parents=True, exist_ok=True)
        (delivery_root / "telemetry").mkdir(parents=True, exist_ok=True)
        (delivery_root / "artifacts").mkdir(parents=True, exist_ok=True)
        (delivery_root / "memory").mkdir(parents=True, exist_ok=True)

        if self.config_fixture.is_file():
            shutil.copy2(str(self.config_fixture), str(delivery_root / "config.yml"))

        self.plugin_load_strategy = self._probe_plugin_load_strategy()
        if self.plugin_load_strategy == PLUGIN_LOAD_COPY_INTO_HOME:
            self._install_plugin_into_home()

        self._setup_done = True

    @property
    def cwd_for_subprocess(self) -> Path:
        """Working directory the spawned `claude` subprocess should chdir to."""
        if self.workdir is None:
            raise RuntimeError("Workspace.setup() must run before cwd_for_subprocess access")
        return self.workdir

    def subprocess_env(self, base_env: Optional[dict] = None) -> dict:
        """Build env dict for subprocess.Popen.

        IMPORTANT (D-tk5-04 / BACKLOG-107): HOME is NOT overridden. Claude Code
        reads credentials from ``~/.claude/.credentials.json`` (or the system
        keychain via its libsecret/Keychain backend), so the spawned process
        must inherit the parent's HOME to authenticate. Isolation is achieved
        via:

        - ``cwd_for_subprocess`` (the spawned process is chdir'd into a tmp
          workdir; ``.delivery/`` inside that workdir is the pipeline scratch
          area).
        - ``XDG_CONFIG_HOME`` / ``XDG_DATA_HOME`` redirected into the tmp tree
          so any *non-credential* config or data the subprocess writes lands
          in the sandbox instead of the user's real XDG dirs.
        - ``CLAUDE_PROJECT_DIR`` set to the workdir so the spawned Claude Code
          instance (if it honors the env var) treats the sandbox workdir as
          its project root.
        """
        if self.home is None or self.workdir is None:
            raise RuntimeError("Workspace.setup() must run before subprocess_env()")
        env = dict(base_env or os.environ)
        # Deliberately DO NOT override HOME — preserves Claude auth path.
        env["XDG_CONFIG_HOME"] = str(self.home / ".config")
        env["XDG_DATA_HOME"] = str(self.home / ".local" / "share")
        env["CLAUDE_PROJECT_DIR"] = str(self.workdir)
        return env

    def cleanup(self) -> None:
        """Idempotent tmpdir scrub."""
        if self.home is None:
            return
        shutil.rmtree(str(self.home), ignore_errors=True)
        self.home = None
        self.workdir = None
        self._setup_done = False

    def __enter__(self) -> "Workspace":
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cleanup()

    def _probe_plugin_load_strategy(self) -> str:
        """Run `claude --help`; pick plugin-dir if flag is present, else fallback."""
        try:
            result = subprocess.run(
                ["claude", "--help"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return PLUGIN_LOAD_COPY_INTO_HOME

        haystack = (result.stdout or "") + (result.stderr or "")
        if "--plugin-dir" in haystack:
            return PLUGIN_LOAD_PLUGIN_DIR
        return PLUGIN_LOAD_COPY_INTO_HOME

    def _install_plugin_into_home(self) -> None:
        """Recursively copy plugin into <home>/.claude/plugins/<name>/ (skip tests/smoke)."""
        if self.home is None:
            return
        if not self.plugin_path.is_dir():
            return

        dest = self.home / ".claude" / "plugins" / self.plugin_path.name
        dest.parent.mkdir(parents=True, exist_ok=True)

        # tests/smoke/ is excluded to prevent the runner copying itself recursively.
        def _ignore(directory: str, names: list) -> list:
            rel = Path(directory).resolve()
            ignored: list[str] = []
            try:
                rel_to_plugin = rel.relative_to(self.plugin_path.resolve())
            except ValueError:
                return ignored
            if str(rel_to_plugin) == "tests":
                ignored.append("smoke")
            return ignored

        shutil.copytree(str(self.plugin_path), str(dest), ignore=_ignore, dirs_exist_ok=True)

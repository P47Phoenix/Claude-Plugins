"""Subprocess runner: spawn `claude`, tee stream-json, enforce caps.

Note (D-tk5-05 fix, BACKLOG-107 iter2): the live-spawn path additionally
tees the spawned subprocess's stderr to ``<run-dir>/stderr.log`` so that
exit-1 / startup-failure diagnostics are recoverable post-mortem. The
file's first line is the ``argv`` of the spawned process so future
debugging knows exactly what was invoked.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import threading
import time
import warnings
from pathlib import Path
from typing import Optional

from .workspace import (
    PLUGIN_LOAD_COPY_INTO_HOME,
    PLUGIN_LOAD_PLUGIN_DIR,
    Workspace,
)


COST_CAP_EXCEEDED_REASON = "cost-cap-exceeded"
TIMEOUT_REASON = "timeout"
SUCCESS_REASON = None


class PipelineTimeout(Exception):
    """Raised when subprocess wall-clock exceeds the configured timeout."""


def _running_cost(events: list[dict]) -> float:
    total = 0.0
    for evt in events:
        usage = evt.get("usage") if isinstance(evt, dict) else None
        if isinstance(usage, dict):
            cost = usage.get("cost_usd")
            try:
                total += float(cost) if cost is not None else 0.0
            except (TypeError, ValueError):
                continue
    return total


def _tee_event(event: dict, stream_path: Path) -> None:
    with stream_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
        fh.flush()


def _parse_line(line: str) -> Optional[dict]:
    text = line.strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        warnings.warn(f"runner: malformed stream line dropped ({exc})", stacklevel=2)
        return None
    if not isinstance(obj, dict):
        warnings.warn("runner: stream line not a JSON object; dropped", stacklevel=2)
        return None
    return obj


def _read_fixture_events(fixture_path: Path) -> list[dict]:
    events: list[dict] = []
    with fixture_path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            parsed = _parse_line(raw)
            if parsed is not None:
                events.append(parsed)
    return events


def _run_from_fixture(
    fixture_path: Path,
    stream_path: Path,
    cost_cap: float,
) -> dict:
    events: list[dict] = []
    outcome_reason = SUCCESS_REASON
    outcome_success = True
    exit_code = 0

    for evt in _read_fixture_events(fixture_path):
        events.append(evt)
        _tee_event(evt, stream_path)
        if _running_cost(events) > cost_cap:
            outcome_success = False
            outcome_reason = COST_CAP_EXCEEDED_REASON
            exit_code = 2
            break

    return {
        "events": events,
        "outcome": {
            "success": outcome_success,
            "exit_code": exit_code,
            "reason": outcome_reason,
        },
        "elapsed_seconds": 0.0,
    }


def _build_claude_command(
    workspace: Workspace,
    prompt_path: Path,
) -> list[str]:
    # D-tk5-05 fix (BACKLOG-107 iter2): `--print --output-format=stream-json`
    # requires `--verbose` per Claude Code CLI contract; absence caused the
    # subprocess to exit 1 with "When using --print, --output-format=stream-json
    # requires --verbose" before emitting any stream events.
    cmd = ["claude", "--print", "--output-format", "stream-json", "--verbose"]
    if workspace.plugin_load_strategy == PLUGIN_LOAD_PLUGIN_DIR:
        cmd.extend(["--plugin-dir", str(workspace.plugin_path)])
    return cmd


def _stderr_log_path(stream_path: Path) -> Path:
    """Stderr log lives next to stream.jsonl inside the run dir."""
    return stream_path.parent / "stderr.log"


def _drain_stderr_to_file(stderr_stream, stderr_path: Path) -> None:
    """Append spawned subprocess's stderr to ``stderr_path`` line-by-line.

    Runs in a background daemon thread so the main loop can still drive
    stdout without deadlocking on a full stderr pipe buffer. The header
    (argv) is written by the caller BEFORE the thread starts so the
    invocation context is present even if the subprocess emits nothing
    on stderr.
    """
    if stderr_stream is None:
        return
    try:
        with stderr_path.open("a", encoding="utf-8") as fh:
            for raw_line in stderr_stream:
                fh.write(raw_line)
                fh.flush()
    except (OSError, ValueError):
        # Stream closed or path went away mid-tee — best-effort tee.
        return


def _write_stderr_header(stderr_path: Path, cmd: list[str], cwd: str) -> None:
    """Seed stderr.log with the spawned argv + cwd so future debugging
    knows exactly what was invoked, even before the subprocess speaks.
    """
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    header_lines = [
        f"# argv: {json.dumps(cmd)}\n",
        f"# cwd:  {cwd}\n",
        f"# --- stderr stream begins ---\n",
    ]
    with stderr_path.open("w", encoding="utf-8") as fh:
        fh.writelines(header_lines)
        fh.flush()


def _spawn_and_tee(
    workspace: Workspace,
    prompt: str,
    stream_path: Path,
    cost_cap: float,
    timeout: int,
    prompt_path: Path,
) -> dict:
    cmd = _build_claude_command(workspace, prompt_path)
    env = workspace.subprocess_env()
    cwd = str(workspace.cwd_for_subprocess)
    stderr_path = _stderr_log_path(stream_path)

    # Seed stderr.log with argv + cwd BEFORE spawning so failures during
    # spawn (FileNotFoundError, OSError) still leave the invocation trail
    # for D-tk5-05 style diagnostics.
    _write_stderr_header(stderr_path, cmd, cwd)

    start = time.monotonic()
    events: list[dict] = []
    outcome_reason = SUCCESS_REASON
    outcome_success = True
    exit_code = 0

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=env,
            text=True,
            bufsize=1,
        )
    except (FileNotFoundError, OSError) as exc:
        # Persist the spawn-side failure into stderr.log too, since the
        # subprocess never got a chance to write its own.
        try:
            with stderr_path.open("a", encoding="utf-8") as fh:
                fh.write(f"# spawn-failed: {exc!r}\n")
                fh.flush()
        except OSError:
            pass
        return {
            "events": [],
            "outcome": {
                "success": False,
                "exit_code": 4,
                "reason": f"plumbing-error: {exc}",
            },
            "elapsed_seconds": time.monotonic() - start,
        }

    # Start the stderr drain thread as soon as the process is alive. The
    # thread holds a reference to ``proc.stderr`` which closes when the
    # subprocess exits, so the thread's for-loop terminates naturally.
    stderr_thread = threading.Thread(
        target=_drain_stderr_to_file,
        args=(proc.stderr, stderr_path),
        name="smoke-stderr-tee",
        daemon=True,
    )
    stderr_thread.start()

    try:
        if proc.stdin is not None:
            proc.stdin.write(prompt)
            proc.stdin.close()

        assert proc.stdout is not None
        for raw_line in proc.stdout:
            if time.monotonic() - start > timeout:
                outcome_success = False
                outcome_reason = TIMEOUT_REASON
                exit_code = 3
                _terminate(proc)
                break

            evt = _parse_line(raw_line)
            if evt is None:
                continue
            events.append(evt)
            _tee_event(evt, stream_path)

            if _running_cost(events) > cost_cap:
                outcome_success = False
                outcome_reason = COST_CAP_EXCEEDED_REASON
                exit_code = 2
                _terminate(proc)
                break

        if outcome_success:
            try:
                proc.wait(timeout=max(1, timeout - int(time.monotonic() - start)))
            except subprocess.TimeoutExpired:
                outcome_success = False
                outcome_reason = TIMEOUT_REASON
                exit_code = 3
                _terminate(proc)
            else:
                if proc.returncode != 0:
                    outcome_success = False
                    outcome_reason = f"subprocess-exit-{proc.returncode}"
                    exit_code = 1
    finally:
        if proc.poll() is None:
            _terminate(proc)
        # Give the stderr drain a brief window to flush after the
        # subprocess exits. Daemon=True means we never block shutdown.
        stderr_thread.join(timeout=2.0)

    return {
        "events": events,
        "outcome": {
            "success": outcome_success,
            "exit_code": exit_code,
            "reason": outcome_reason,
        },
        "elapsed_seconds": time.monotonic() - start,
    }


def _terminate(proc: "subprocess.Popen") -> None:
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
    except (OSError, ProcessLookupError):
        pass


def run_pipeline(
    prompt: str,
    workspace: Workspace,
    *,
    cost_cap: float,
    timeout: int,
    stream_path: Path,
    stream_fixture: Optional[Path] = None,
    prompt_path: Optional[Path] = None,
) -> dict:
    """Drive one smoke-run end-to-end. Returns dict with events + outcome + elapsed.

    When stream_fixture is provided, skips spawning `claude` and replays
    fixture events instead — the cost-cap test and meta-test injection path.
    """
    stream_path.parent.mkdir(parents=True, exist_ok=True)
    stream_path.write_text("", encoding="utf-8")

    if stream_fixture is not None:
        return _run_from_fixture(Path(stream_fixture), stream_path, cost_cap)

    if prompt_path is None:
        raise ValueError("prompt_path is required for live subprocess invocation")

    return _spawn_and_tee(
        workspace=workspace,
        prompt=prompt,
        stream_path=stream_path,
        cost_cap=cost_cap,
        timeout=timeout,
        prompt_path=prompt_path,
    )

#!/usr/bin/env python3
"""Session Keepalive -- companion process that keeps Claude active.

Launches as a background process alongside a Claude Code session.
Three modes:
  anti-idle    -- nudges the terminal when the session goes idle
  wait-resume  -- sleeps for a cooldown period, then sends a resume prompt
  monitor      -- sends a user-specified prompt at regular intervals

Safety:
  - Focus-checks before every keystroke send (prevents wrong-window input)
  - Parent PID monitoring (auto-exits when the parent dies)
  - Lock file killswitch (delete .delivery/keepalive.lock to stop)
  - Signal handling (SIGTERM, SIGINT)
  - No shell=True in any subprocess call

Cross-platform drivers: Linux X11 (xdotool), Linux Wayland (ydotool),
macOS (System Events via osascript), Windows (PowerShell SendKeys).

Requires: Python 3.10+ (stdlib only, no external dependencies).

macOS note: System Events requires Accessibility permissions granted to the
calling terminal application (System Settings > Privacy & Security >
Accessibility). Without this, keystroke injection will silently fail.
"""

import argparse
import datetime
import logging
import os
import platform
import shutil
import signal
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path


# ---------------------------------------------------------------------------
# Terminal Drivers
# ---------------------------------------------------------------------------

class TerminalDriver:
    """Abstract base for platform-specific terminal input."""

    def send_text(self, text: str) -> bool:
        """Send *text* followed by Enter to the target terminal.

        Returns True if the text was sent, False if sending was skipped
        (e.g. terminal not focused).
        """
        raise NotImplementedError

    def is_target_focused(self) -> bool:
        """Return True if the target terminal window is currently focused."""
        raise NotImplementedError


class X11Driver(TerminalDriver):
    """Linux X11 via xdotool -- targets a specific window ID."""

    def __init__(self) -> None:
        self.window_id = self._get_active_window()

    def _get_active_window(self) -> str:
        result = subprocess.run(
            ["xdotool", "getactivewindow"],
            capture_output=True, text=True,
        )
        return result.stdout.strip()

    def _window_exists(self) -> bool:
        result = subprocess.run(
            ["xdotool", "getwindowname", self.window_id],
            capture_output=True, text=True,
        )
        return result.returncode == 0

    def is_target_focused(self) -> bool:
        if not self._window_exists():
            return False
        result = subprocess.run(
            ["xdotool", "getactivewindow"],
            capture_output=True, text=True,
        )
        return result.stdout.strip() == self.window_id

    def send_text(self, text: str) -> bool:
        if not self._window_exists():
            return False
        subprocess.run(
            ["xdotool", "type", "--window", self.window_id,
             "--clearmodifiers", text],
        )
        subprocess.run(
            ["xdotool", "key", "--window", self.window_id, "Return"],
        )
        return True


class WaylandDriver(TerminalDriver):
    """Linux Wayland via ydotool -- active window only, with focus check.

    Wayland's security model prevents reliable per-window targeting.
    ydotool injects at the compositor level, so we rely on a best-effort
    focus check.  The user accepts this trade-off per the PRD.
    """

    def is_target_focused(self) -> bool:
        # Wayland does not expose a reliable way to query the focused
        # window from an unprivileged process.  Return True and let the
        # user control risk by only running keepalive when the terminal
        # is the primary window.
        return True

    def send_text(self, text: str) -> bool:
        if not self.is_target_focused():
            return False
        subprocess.run(["ydotool", "type", "--", text])
        # ydotool key uses evdev codes: 28 = KEY_ENTER
        subprocess.run(["ydotool", "key", "28:1", "28:0"])
        return True


class MacOSDriver(TerminalDriver):
    """macOS via System Events keystroke injection.

    Requires Accessibility permissions for the calling process.
    """

    def __init__(self) -> None:
        self.app_name = self._detect_terminal_app()

    def _detect_terminal_app(self) -> str:
        """Detect which terminal emulator is running."""
        candidates = [
            "Terminal", "iTerm2", "iTerm", "Alacritty", "kitty", "Warp",
        ]
        for app in candidates:
            result = subprocess.run(
                ["osascript", "-e",
                 f'tell application "System Events" to '
                 f'(name of processes) contains "{app}"'],
                capture_output=True, text=True,
            )
            if "true" in result.stdout.lower():
                return app
        return "Terminal"  # fallback

    def is_target_focused(self) -> bool:
        result = subprocess.run(
            ["osascript", "-e",
             'tell application "System Events" to get name of first '
             'application process whose frontmost is true'],
            capture_output=True, text=True,
        )
        return self.app_name.lower() in result.stdout.strip().lower()

    def send_text(self, text: str) -> bool:
        if not self.is_target_focused():
            return False
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        subprocess.run([
            "osascript", "-e",
            f'tell application "System Events" to keystroke "{escaped}"',
        ])
        subprocess.run([
            "osascript", "-e",
            'tell application "System Events" to keystroke return',
        ])
        return True


class WindowsDriver(TerminalDriver):
    """Windows via PowerShell SendKeys -- focus check before send."""

    _FOCUS_SCRIPT = (
        'Add-Type @"\n'
        "using System;\n"
        "using System.Runtime.InteropServices;\n"
        "public class Win {\n"
        '    [DllImport("user32.dll")] public static extern IntPtr '
        "GetForegroundWindow();\n"
        '    [DllImport("user32.dll")] public static extern uint '
        "GetWindowThreadProcessId(IntPtr hWnd, out uint pid);\n"
        "}\n"
        '"@\n'
        "$hwnd = [Win]::GetForegroundWindow()\n"
        "$pid = 0\n"
        "[Win]::GetWindowThreadProcessId($hwnd, [ref]$pid)\n"
        "Write-Output $pid"
    )

    def __init__(self) -> None:
        self.target_pid = os.getppid()

    def is_target_focused(self) -> bool:
        try:
            result = subprocess.run(
                ["powershell", "-Command", self._FOCUS_SCRIPT],
                capture_output=True, text=True, timeout=5,
            )
            fg_pid = result.stdout.strip()
            if fg_pid.isdigit():
                return int(fg_pid) == self.target_pid
            return True  # If we can't determine, allow (user accepts risk)
        except Exception:
            return True

    def send_text(self, text: str) -> bool:
        if not self.is_target_focused():
            return False
        escaped = text.replace('"', '`"')
        script = (
            "Add-Type -AssemblyName System.Windows.Forms\n"
            f'[System.Windows.Forms.SendKeys]::SendWait("{escaped}")\n'
            '[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")'
        )
        try:
            subprocess.run(
                ["powershell", "-Command", script],
                timeout=10,
            )
            return True
        except Exception:
            return False


class NullDriver(TerminalDriver):
    """Fallback when no platform tool is available."""

    def is_target_focused(self) -> bool:
        return False

    def send_text(self, text: str) -> bool:
        return False


def detect_driver() -> TerminalDriver:
    """Auto-detect and return the appropriate terminal driver."""
    system = platform.system()

    if system == "Linux":
        # Prefer Wayland if WAYLAND_DISPLAY is set and ydotool exists
        if os.environ.get("WAYLAND_DISPLAY"):
            if shutil.which("ydotool"):
                return WaylandDriver()
        # Fall back to X11
        if os.environ.get("DISPLAY"):
            if shutil.which("xdotool"):
                return X11Driver()
        return NullDriver()

    if system == "Darwin":
        return MacOSDriver()

    if system == "Windows":
        return WindowsDriver()

    return NullDriver()


# ---------------------------------------------------------------------------
# Core Keepalive Logic
# ---------------------------------------------------------------------------

class SessionKeepalive:
    """Main keepalive companion process."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.mode: str = args.mode
        self.interval: int = args.interval
        self.prompt: str = args.prompt
        self.wait: int = args.wait
        self.max_retries: int = args.max_retries
        self.max_iterations: int = args.max_iterations
        self.parent_pid: int = args.pid or os.getppid()
        self.cwd = Path(args.cwd).resolve()

        # State files live under .delivery/
        delivery_dir = self.cwd / ".delivery"
        delivery_dir.mkdir(parents=True, exist_ok=True)
        self.lock_file = delivery_dir / "keepalive.lock"
        self.log_file = delivery_dir / "keepalive.log"
        self.heartbeat_file = delivery_dir / "keepalive-heartbeat"

        self.driver: TerminalDriver = detect_driver()
        self.running: bool = True
        self.retries: int = 0
        self.iterations: int = 0

        # --- Logging (rotating, 1 MB, 2 backups) ---
        handler = RotatingFileHandler(
            str(self.log_file), maxBytes=1_000_000, backupCount=2,
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"),
        )
        self.logger = logging.getLogger("keepalive")
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Also log to stderr so the launching process sees startup messages
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"),
        )
        self.logger.addHandler(stderr_handler)

        # --- Signal handling ---
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

    # -- Lifecycle helpers --------------------------------------------------

    def _handle_signal(self, signum: int, frame) -> None:
        sig_name = signal.Signals(signum).name if hasattr(signal, "Signals") else str(signum)
        self.logger.info("Received %s, shutting down", sig_name)
        self.running = False

    def _parent_alive(self) -> bool:
        """Check whether the parent process is still running."""
        try:
            os.kill(self.parent_pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False

    def _lock_exists(self) -> bool:
        return self.lock_file.exists()

    def _heartbeat_stale(self) -> bool:
        """Return True if the heartbeat file is missing or older than *interval*."""
        if not self.heartbeat_file.exists():
            return True
        try:
            mtime = self.heartbeat_file.stat().st_mtime
            age = time.time() - mtime
            return age > self.interval
        except OSError:
            return True

    def _write_lock(self) -> None:
        self.lock_file.write_text(str(os.getpid()), encoding="utf-8")

    def _remove_lock(self) -> None:
        try:
            self.lock_file.unlink(missing_ok=True)
        except OSError:
            pass

    def _send_nudge(self, text: str) -> bool:
        """Send *text* to the terminal via the platform driver."""
        if isinstance(self.driver, NullDriver):
            self.logger.error(
                "No terminal driver available. "
                "Install xdotool (Linux X11), ydotool (Linux Wayland), "
                "or ensure osascript (macOS) / PowerShell (Windows) is accessible."
            )
            return False

        sent = self.driver.send_text(text)
        if sent:
            self.logger.info("Sent nudge: %s", text[:100])
        else:
            self.logger.warning("Terminal not focused, skipping nudge")
        return sent

    # -- Check loop guard ---------------------------------------------------

    def _check_should_continue(self) -> bool:
        """Return False if the companion should stop."""
        if not self.running:
            return False
        if not self._lock_exists():
            self.logger.info("Lock file removed, stopping")
            return False
        if not self._parent_alive():
            self.logger.info("Parent process exited (PID %d), stopping", self.parent_pid)
            return False
        return True

    # -- Interruptible sleep ------------------------------------------------

    def _sleep(self, seconds: int) -> bool:
        """Sleep for *seconds*, checking the stop condition every second.

        Returns True if the full sleep completed, False if interrupted.
        """
        for _ in range(seconds):
            if not self._check_should_continue():
                return False
            time.sleep(1)
        return True

    # -- Mode implementations -----------------------------------------------

    def _heartbeat_mtime(self) -> float:
        """Return the heartbeat file mtime, or 0.0 if unavailable."""
        try:
            return self.heartbeat_file.stat().st_mtime
        except (OSError, FileNotFoundError):
            return 0.0

    def _run_anti_idle(self) -> None:
        """Anti-idle mode: nudge the terminal when the heartbeat goes stale."""
        last_nudge_time: float = 0.0

        while self._check_should_continue():
            if not self._sleep(self.interval):
                break
            if not self._check_should_continue():
                break

            if self._heartbeat_stale():
                # If we already nudged, check whether the heartbeat was
                # updated since that nudge.  If it was, the session responded
                # and we should reset rather than fire again.
                if last_nudge_time > 0:
                    hb_mtime = self._heartbeat_mtime()
                    if hb_mtime >= last_nudge_time:
                        self.logger.info(
                            "Heartbeat updated after nudge, resetting retries",
                        )
                        self.retries = 0
                        last_nudge_time = 0.0
                        continue

                if self.retries >= self.max_retries:
                    self.logger.warning(
                        "Max retries (%d) reached, stopping", self.max_retries,
                    )
                    break
                self._send_nudge(self.prompt)
                last_nudge_time = time.time()
                self.retries += 1
                self.logger.info(
                    "Nudge %d / %d", self.retries, self.max_retries,
                )
            else:
                self.retries = 0  # Reset counter on activity
                last_nudge_time = 0.0

    def _run_wait_resume(self) -> None:
        """Wait-resume mode: sleep for *wait* seconds, then send a single prompt."""
        self.logger.info("Waiting %d seconds for cooldown...", self.wait)
        if not self._sleep(self.wait):
            return
        self._send_nudge(self.prompt)

    def _run_monitor(self) -> None:
        """Monitor mode: send *prompt* every *interval* seconds."""
        while self._check_should_continue():
            self._send_nudge(self.prompt)
            self.iterations += 1
            self.logger.info(
                "Monitor iteration %d%s",
                self.iterations,
                f" / {self.max_iterations}" if self.max_iterations else "",
            )
            if self.max_iterations and self.iterations >= self.max_iterations:
                self.logger.info(
                    "Max iterations (%d) reached, stopping", self.max_iterations,
                )
                break
            if not self._sleep(self.interval):
                break

    # -- Entry point --------------------------------------------------------

    def run(self) -> None:
        """Run the keepalive companion."""
        self._write_lock()
        self.logger.info(
            "Keepalive started: mode=%s, interval=%ds, parent_pid=%d",
            self.mode, self.interval, self.parent_pid,
        )
        self.logger.info("Driver: %s", type(self.driver).__name__)

        if platform.system() == "Darwin":
            self.logger.info(
                "macOS detected -- ensure Accessibility permissions are "
                "granted to this terminal app (System Settings > Privacy "
                "& Security > Accessibility)."
            )

        try:
            if self.mode == "anti-idle":
                self._run_anti_idle()
            elif self.mode == "wait-resume":
                self._run_wait_resume()
            elif self.mode == "monitor":
                self._run_monitor()
            else:
                self.logger.error("Unknown mode: %s", self.mode)
        finally:
            self._remove_lock()
            self.logger.info("Keepalive stopped")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Session Keepalive -- companion process that keeps Claude active.",
    )
    parser.add_argument(
        "--mode", required=True,
        choices=["anti-idle", "wait-resume", "monitor"],
        help="Operating mode",
    )
    parser.add_argument(
        "--interval", type=int, default=300,
        help="Seconds between checks/nudges (default: 300)",
    )
    parser.add_argument(
        "--prompt",
        default="Continue working on the current task. Do not stop until complete.",
        help="Message to send to terminal",
    )
    parser.add_argument(
        "--wait", type=int, default=3600,
        help="Seconds to wait before resume (wait-resume mode, default: 3600)",
    )
    parser.add_argument(
        "--max-retries", type=int, default=10,
        help="Max nudges before stopping (anti-idle mode, default: 10)",
    )
    parser.add_argument(
        "--max-iterations", type=int, default=0,
        help="Max iterations (monitor mode, 0=unlimited, default: 0)",
    )
    parser.add_argument(
        "--pid", type=int, default=0,
        help="Parent PID to monitor (default: parent of this process)",
    )
    parser.add_argument(
        "--cwd", default=".",
        help="Working directory for state files (default: current directory)",
    )

    args = parser.parse_args()

    # Validate: monitor mode requires an explicit --prompt
    if args.mode == "monitor" and args.prompt == parser.get_default("prompt"):
        parser.error("monitor mode requires --prompt")

    keepalive = SessionKeepalive(args)
    keepalive.run()


if __name__ == "__main__":
    main()

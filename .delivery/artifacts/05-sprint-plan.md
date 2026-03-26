# Sprint Plan -- Issue #39: Session Keepalive Companion

**Type**: FEATURE | **Scrum Bag**: Aragorn
**Date**: 2026-03-25
**PRD**: `.delivery/artifacts/02-prd.md`
**GitHub Issue**: #39

**Sprint Goal**: Deliver a cross-platform companion process that keeps Claude Code sessions productive when the human is away -- anti-idle nudging, rate-limit recovery, and periodic prompt execution, with safety rails that prevent wrong-window input and orphan processes.

**Adversarial Review Fixes Incorporated**: Four findings from the adversarial review are woven into the stories below rather than deferred:
1. Wayland/Windows: verify terminal focus before sending keystrokes; skip if terminal is not focused
2. macOS: use System Events keystroke mechanism; document Accessibility permission requirement
3. Anti-idle: heartbeat file (`.delivery/keepalive-heartbeat`) distinguishes genuine thinking from a stalled session
4. Windows: same focus-check approach as Wayland (query foreground window before sending)

---

## Story 1: Core Companion Process + Heartbeat

**As a** user running a long Claude session,
**I want** a companion process that monitors the session and self-terminates cleanly,
**So that** I have a reliable foundation for keepalive modes without orphan processes or stale lock files.

**Scope**: `delivery-team/scripts/session_keepalive.py` -- argument parsing, PID monitoring, lock file lifecycle, log file with rotation, heartbeat file checking, signal handling, self-termination.

### Acceptance Criteria

**AC-1: Argument parsing**

- Given the user runs `python session_keepalive.py --mode anti-idle --interval 300 --pid $PPID`
- When the script starts
- Then it parses all arguments per FR-01: `--mode` (required), `--interval`, `--wait`, `--prompt`, `--pid` (required), `--max-retries`, `--max-iterations`
- And missing required arguments produce a clear error message and exit code 2

**AC-2: Lock file lifecycle**

- Given the companion starts successfully
- When it initializes
- Then it writes its own PID to `.delivery/keepalive.lock`
- And on exit (any exit path), it deletes `.delivery/keepalive.lock`

**AC-3: Parent PID monitoring**

- Given the companion is running with `--pid 12345`
- When the parent process (PID 12345) terminates
- Then the companion detects this within 30 seconds via `os.kill(pid, 0)`
- And logs "parent process exited" and terminates cleanly

**AC-4: Killswitch via lock file deletion**

- Given the companion is running and `.delivery/keepalive.lock` exists
- When the user deletes `.delivery/keepalive.lock`
- Then the companion detects the deletion within 30 seconds and exits

**AC-5: Signal handling**

- Given the companion is running
- When it receives SIGTERM or SIGINT
- Then it deletes the lock file, logs the shutdown reason, and exits with code 0

**AC-6: Log file with rotation**

- Given the companion writes to `.delivery/keepalive.log`
- When the log file exceeds 1MB
- Then it rotates to `.delivery/keepalive.log.1` (one backup kept)
- And all actions are logged with ISO timestamps

**AC-7: Heartbeat file checking**

- Given anti-idle mode is active
- When the companion checks for activity
- Then it reads the mtime of `.delivery/keepalive-heartbeat`
- And considers the session active if mtime is within `--interval` seconds of now
- And considers the session idle if mtime is older than `--interval` seconds or the file does not exist

### Test Cases

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| T1-1 | Valid argument parsing | Run with `--mode anti-idle --pid 1234 --interval 60` | Starts without error, logs mode/interval/pid |
| T1-2 | Missing required arg | Run without `--mode` | Exit code 2, error message names the missing argument |
| T1-3 | Lock file created on start | Start companion, check `.delivery/keepalive.lock` | File exists, contains companion PID as plain text |
| T1-4 | Lock file deleted on clean exit | Start companion, send SIGTERM, check lock file | Lock file is gone |
| T1-5 | Parent PID death detection | Start companion with `--pid` of a short-lived process; wait for that process to exit | Companion exits within 30 seconds, log says "parent process exited" |
| T1-6 | Killswitch | Start companion, delete `.delivery/keepalive.lock` | Companion exits within 30 seconds, log says "lock file removed" |
| T1-7 | SIGTERM handling | Start companion, send SIGTERM | Clean exit, lock file deleted, log says "received SIGTERM" |
| T1-8 | SIGINT handling | Start companion, send SIGINT | Clean exit, lock file deleted, log says "received SIGINT" |
| T1-9 | Log rotation | Write >1MB to the log (simulate with rapid logging) | `.delivery/keepalive.log.1` created, main log reset |
| T1-10 | Heartbeat fresh | Touch `.delivery/keepalive-heartbeat`, run heartbeat check with 300s interval | Returns "active" -- no nudge sent |
| T1-11 | Heartbeat stale | Set heartbeat mtime to 10 minutes ago, run heartbeat check with 300s interval | Returns "idle" -- nudge eligible |
| T1-12 | Heartbeat missing | Delete heartbeat file, run heartbeat check | Returns "idle" -- nudge eligible (file absence = no proof of activity) |

---

## Story 2: Terminal Drivers (4 Platforms)

**As a** user on any supported OS,
**I want** the companion to send keystrokes to the correct terminal window using my platform's native tools,
**So that** nudges reach Claude and never leak into the wrong application.

**Scope**: `TerminalDriver` abstraction with four backends -- Linux X11 (xdotool), Linux Wayland (ydotool), macOS (System Events), Windows (PowerShell). Auto-detection at startup. Focus verification on Wayland, macOS, and Windows before every send.

### Acceptance Criteria

**AC-1: TerminalDriver abstraction**

- Given the companion starts
- When it initializes the terminal driver
- Then it auto-detects the platform via `platform.system()` and environment variables (`$XDG_SESSION_TYPE`, `$WAYLAND_DISPLAY`)
- And instantiates the correct backend
- And logs the detected platform and driver name

**AC-2: Linux X11 driver**

- Given the platform is Linux with X11
- When `xdotool` is available via `shutil.which()`
- Then the driver captures the terminal window ID at startup via `xdotool getactivewindow`
- And sends keystrokes using `xdotool type --window [wid]` followed by `xdotool key --window [wid] Return`
- And before every send, verifies the window still exists via `xdotool getwindowname [wid]`; if gone, logs error and exits

**AC-3: Linux Wayland driver (with focus check)**

- Given the platform is Linux with Wayland
- When `ydotool` is available
- Then before every send, the driver checks whether the terminal is the focused window
- And if the terminal is NOT focused, skips the send, logs "terminal not focused, skipping nudge"
- And if the terminal IS focused, sends keystrokes via `ydotool type` followed by `ydotool key 28:1 28:0` (Enter)

**AC-4: macOS driver (System Events + focus check)**

- Given the platform is macOS
- When the driver initializes
- Then it uses `osascript` with System Events `keystroke` to send text to the terminal (not `do script`)
- And before every send, checks whether Terminal.app or iTerm2 is the frontmost application
- And if the terminal is NOT frontmost, skips the send, logs "terminal not focused, skipping nudge"
- And the log (or startup message) documents that Accessibility permissions must be granted to the calling process for System Events to work

**AC-5: Windows driver (with focus check)**

- Given the platform is Windows
- When PowerShell is available
- Then before every send, the driver queries the foreground window title via PowerShell
- And if the foreground window is NOT the target terminal, skips the send, logs "terminal not focused, skipping nudge"
- And if the terminal IS focused, sends keystrokes via `[System.Windows.Forms.SendKeys]::SendWait()` through `subprocess.run(["powershell", ...])`

**AC-6: Missing tool graceful exit**

- Given the required platform tool is not installed
- When the driver initializes
- Then it logs an error with platform-specific install instructions (e.g., "Install xdotool: sudo apt install xdotool")
- And exits with code 1

**AC-7: No shell=True in subprocess calls**

- Given any terminal driver makes a subprocess call
- Then `shell=True` is never used
- And `subprocess.run()` receives a list of arguments

### Test Cases

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| T2-1 | Auto-detect Linux X11 | Set `XDG_SESSION_TYPE=x11`, mock `shutil.which("xdotool")` returning a path | X11 driver instantiated, logged as "LinuxX11Driver" |
| T2-2 | Auto-detect Linux Wayland | Set `WAYLAND_DISPLAY=wayland-0`, mock `shutil.which("ydotool")` returning a path | Wayland driver instantiated, logged as "LinuxWaylandDriver" |
| T2-3 | Auto-detect macOS | Set `platform.system()` to "Darwin" | macOS driver instantiated, logged as "MacOSDriver" |
| T2-4 | Auto-detect Windows | Set `platform.system()` to "Windows", mock `shutil.which("powershell")` returning a path | Windows driver instantiated, logged as "WindowsDriver" |
| T2-5 | X11 window ID capture | Start X11 driver with a real terminal | Window ID captured, logged, non-zero integer |
| T2-6 | X11 window gone | Capture window ID, close that window, attempt send | Driver detects missing window, logs error, companion exits |
| T2-7 | Wayland focus check -- focused | Terminal is focused, attempt send | Keystroke sent, logged as successful |
| T2-8 | Wayland focus check -- not focused | Terminal is NOT focused, attempt send | Send skipped, logged as "terminal not focused, skipping nudge" |
| T2-9 | macOS focus check -- focused | Terminal.app is frontmost, attempt send | Keystroke sent via System Events |
| T2-10 | macOS focus check -- not focused | Another app is frontmost, attempt send | Send skipped, logged as "terminal not focused, skipping nudge" |
| T2-11 | Windows focus check -- focused | Terminal is foreground window, attempt send | Keystroke sent via SendKeys |
| T2-12 | Windows focus check -- not focused | Another window is foreground, attempt send | Send skipped, logged as "terminal not focused, skipping nudge" |
| T2-13 | Missing xdotool | `shutil.which("xdotool")` returns None on Linux X11 | Exit code 1, log contains install instructions for xdotool |
| T2-14 | Missing ydotool | `shutil.which("ydotool")` returns None on Linux Wayland | Exit code 1, log contains install instructions for ydotool |
| T2-15 | No shell=True | Inspect all subprocess calls in the driver module | Zero occurrences of `shell=True` |
| T2-16 | macOS Accessibility note | Read startup log on macOS | Log contains note about Accessibility permissions for System Events |

---

## Story 3: Three Operating Modes

**As a** user with different session needs,
**I want** three operating modes -- anti-idle, wait-resume, and monitor,
**So that** the companion handles idle detection, rate-limit recovery, and periodic prompts as distinct behaviors.

**Scope**: Mode-specific loop logic within `session_keepalive.py`. Anti-idle uses heartbeat + nudge. Wait-resume is single-shot sleep-then-send. Monitor sends a user-specified prompt at intervals.

### Acceptance Criteria

**AC-1: Anti-idle mode with heartbeat**

- Given the user starts with `--mode anti-idle --interval 300`
- When the companion enters its loop
- Then every `--interval` seconds it checks `.delivery/keepalive-heartbeat` mtime
- And if the heartbeat is stale (mtime older than `--interval`), sends the default nudge: "Continue working on the current task. Do not stop until complete."
- And after sending, waits for the heartbeat file to update before nudging again (prevents rapid-fire)
- And increments the nudge counter; exits when `--max-retries` (default 10) is reached

**AC-2: Anti-idle heartbeat distinguishes thinking from stalled**

- Given Claude is actively working (a hook or the session touches `.delivery/keepalive-heartbeat`)
- When the companion checks mtime
- Then the heartbeat is fresh and no nudge is sent
- And this prevents false nudges during long-running operations where Claude is thinking, not stalled

**AC-3: Wait-resume mode**

- Given the user starts with `--mode wait-resume --wait 3600`
- When the companion enters its loop
- Then it logs "Waiting 3600 seconds for cooldown..."
- And sleeps for `--wait` seconds, checking parent PID every 30 seconds during the sleep
- And after the sleep, sends the resume message: "Resume the previous task. The rate limit cooldown has passed."
- And then exits (single-shot)

**AC-4: Monitor mode**

- Given the user starts with `--mode monitor --interval 1800 --prompt "Check for new issues"`
- When the companion enters its loop
- Then every `--interval` seconds it sends the `--prompt` to the terminal
- And logs each send with timestamp and iteration count
- And if `--max-iterations` > 0, exits when the iteration count reaches it
- And if `--max-iterations` is 0 (default), runs until stopped

**AC-5: Monitor mode requires --prompt**

- Given the user starts with `--mode monitor` without `--prompt`
- Then the companion exits with an error: "monitor mode requires --prompt"

**AC-6: Custom prompt override**

- Given any mode started with `--prompt "my custom message"`
- When the companion sends a nudge or resume
- Then it sends the user-supplied prompt instead of the mode default

### Test Cases

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| T3-1 | Anti-idle nudge on stale heartbeat | Start anti-idle, set heartbeat mtime to 10 minutes ago, interval=60 | Nudge sent within 60 seconds, logged with nudge count |
| T3-2 | Anti-idle no nudge on fresh heartbeat | Start anti-idle, touch heartbeat just now, interval=300 | No nudge sent for 300 seconds |
| T3-3 | Anti-idle rapid-fire prevention | Send a nudge, do NOT update heartbeat | Companion waits for heartbeat update rather than sending another nudge immediately |
| T3-4 | Anti-idle max retries | Start with `--max-retries 3`, let heartbeat stay stale | After 3 nudges, companion logs "max nudges reached" and exits |
| T3-5 | Wait-resume basic | Start with `--mode wait-resume --wait 5` (short for testing) | Sleeps ~5 seconds, sends resume message, exits |
| T3-6 | Wait-resume parent dies during wait | Start wait-resume with --wait 3600, kill parent after 10s | Companion exits within 30 seconds of parent death, does NOT wait the full 3600 |
| T3-7 | Wait-resume single-shot | Start wait-resume, let it send the resume | Companion exits after sending -- does not loop |
| T3-8 | Monitor basic | Start monitor with `--interval 5 --prompt "test" --max-iterations 3` | Sends "test" 3 times at ~5 second intervals, then exits |
| T3-9 | Monitor no prompt | Start with `--mode monitor` without `--prompt` | Exit with error message about missing --prompt |
| T3-10 | Monitor unlimited | Start monitor with `--max-iterations 0` | Runs until killed or lock file deleted (verify at least 3 iterations) |
| T3-11 | Custom prompt in anti-idle | Start anti-idle with `--prompt "Keep going, do not stop"` | Custom prompt sent instead of default |
| T3-12 | Default prompt per mode | Start anti-idle without `--prompt` | Default anti-idle nudge text sent |

---

## Story 4: Integration with Delivery-Flow

**As a** delivery-flow user,
**I want** keepalive commands available as part of the delivery-flow vocabulary,
**So that** I can start, stop, and check the companion without remembering raw script invocations.

**Scope**: Add keepalive commands to `delivery-team/skills/delivery-flow/SKILL.md`. Register a PostToolUse hook in `hooks.json` if needed to touch the heartbeat file after writes. Update README or relevant documentation.

### Acceptance Criteria

**AC-1: SKILL.md user commands**

- Given the user commands section of `delivery-team/skills/delivery-flow/SKILL.md`
- When a user reads the available commands
- Then these three commands are documented:
  - `keepalive start [mode] [options]` -- launches the companion via Bash
  - `keepalive stop` -- removes `.delivery/keepalive.lock` to trigger self-termination
  - `keepalive status` -- checks lock file, reads PID, verifies process is alive, tails the log

**AC-2: Command implementations**

- Given the user says `keepalive start anti-idle`
- When the orchestrator processes the command
- Then it runs: `python delivery-team/scripts/session_keepalive.py --mode anti-idle --interval 300 --pid $PPID &`
- And confirms startup by checking `.delivery/keepalive.lock` exists

**AC-3: Heartbeat hook (PostToolUse)**

- Given the delivery-flow pipeline is running and a keepalive companion is active
- When an agent writes or edits a file (PostToolUse on Write/Edit)
- Then the hook touches `.delivery/keepalive-heartbeat` to signal active work
- And this prevents the anti-idle mode from sending false nudges during active pipeline execution

**AC-4: Status command output**

- Given the user says `keepalive status`
- When the orchestrator checks
- Then it reports: whether the companion is running (lock file + PID alive check), the mode, and the last 5 log lines

**AC-5: Documentation**

- Given a new user reads the plugin documentation
- When they look for keepalive information
- Then the delivery-flow SKILL.md commands section explains all three commands with examples
- And the macOS Accessibility permission requirement is noted

### Test Cases

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| T4-1 | keepalive start anti-idle | Say "keepalive start anti-idle" to delivery-flow | Companion process launched, lock file created, startup confirmed in response |
| T4-2 | keepalive start wait-resume | Say "keepalive start wait-resume --wait 1800" | Companion launched in wait-resume mode with 1800s wait |
| T4-3 | keepalive start monitor | Say "keepalive start monitor --interval 600 --prompt 'Check issues'" | Companion launched in monitor mode with specified interval and prompt |
| T4-4 | keepalive stop | Say "keepalive stop" while companion is running | Lock file deleted, companion exits within 30 seconds |
| T4-5 | keepalive stop when not running | Say "keepalive stop" with no companion running | Response says "no active keepalive session" |
| T4-6 | keepalive status while running | Say "keepalive status" while companion is active | Response shows: running, PID, mode, last 5 log lines |
| T4-7 | keepalive status while stopped | Say "keepalive status" with no companion running | Response says "no active keepalive session" |
| T4-8 | Heartbeat hook fires on Write | Pipeline writes a file during Development stage | `.delivery/keepalive-heartbeat` mtime updated |
| T4-9 | Heartbeat hook fires on Edit | Pipeline edits a file during Development stage | `.delivery/keepalive-heartbeat` mtime updated |
| T4-10 | Anti-idle + pipeline integration | Start keepalive, run a pipeline stage, observe heartbeat | Heartbeat stays fresh during active work; no false nudges sent |
| T4-11 | macOS a11y note in docs | Read SKILL.md keepalive section | Accessibility permission requirement documented for macOS users |

---

## Dependency Map

```
Story 1 (core process)
  |
  +---> Story 2 (terminal drivers) -- needs the process lifecycle from Story 1
  |       |
  |       +---> Story 3 (modes) -- needs drivers to send keystrokes
  |                 |
  |                 +---> Story 4 (integration) -- needs all three modes working
```

Stories 1 and 2 could be developed in parallel if the driver interface is agreed upfront (the `TerminalDriver` abstraction with a `send(text: str) -> bool` method). Stories 3 and 4 are sequential -- modes need drivers, integration needs modes.

## Commitment Summary

| Story | Points | Risk | Notes |
|-------|--------|------|-------|
| 1: Core process + heartbeat | 3 | Low | Standard Python -- argparse, signals, file ops. No external deps. |
| 2: Terminal drivers | 5 | Medium | Four platform backends, each with its own quirks. Wayland focus detection and macOS Accessibility are the hardest parts. Cannot fully test all platforms in one environment. |
| 3: Three modes | 3 | Low | Loop logic built on Story 1 and 2 foundations. Heartbeat check is the interesting part. |
| 4: Integration | 2 | Low | SKILL.md edits, one hook addition, documentation. |
| **Total** | **13** | | |

---

## Technical Notes

**Single file**: All of Stories 1-3 land in `delivery-team/scripts/session_keepalive.py`. The driver classes, mode logic, and process lifecycle live in one script -- no package structure, no imports beyond stdlib. This matches the PRD constraint (FR-08) and keeps deployment trivial.

**Heartbeat contract**: The heartbeat file `.delivery/keepalive-heartbeat` is a zero-content file whose only meaningful property is its mtime. Anything that touches it (`pathlib.Path.touch()`) signals activity. The PostToolUse hook in Story 4 is the primary mechanism for keeping it fresh during pipeline execution.

**Focus-check strategy**: Wayland, macOS, and Windows drivers all share the same pattern -- check focus before sending, skip if not focused. This is the adversarial review's primary safety finding. On X11, the `xdotool --window [wid]` targeting is sufficient because it sends to a specific window ID regardless of focus. The focus check is an additional safeguard on platforms where window-targeted input is not possible.

**No busy-waiting**: The companion sleeps between checks. The minimum sleep interval is 10 seconds (NFR-01). Parent PID and lock file checks happen on their own 30-second cadence, independent of the mode interval.

---

*"We do not march blindly into the long dark. We set a watch -- and the watch knows when to speak and when to hold its silence. That is the discipline."*

-- Aragorn, Scrum Bag

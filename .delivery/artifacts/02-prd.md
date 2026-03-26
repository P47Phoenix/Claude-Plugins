## Product Requirements Document

**Product / Feature:** Session Keepalive Companion (Active Session Productivity)
**Version:** 2.0
**Author:** Gandalf (Product Owner)
**Status:** Draft
**Last Updated:** 2026-03-25
**GitHub Issues:** #39

---

### 1. Problem Statement

The previous version of this PRD was wrong. It solved the wrong problem. It concerned itself with tasks surviving between sessions -- persistence, session hooks, YAML files of deferred obligations. All very tidy. All beside the point.

The real problem is simpler and more urgent: Claude stops working in the middle of an active session, and nobody is there to tell it to continue.

Three things happen today that should not:

1. **Claude goes idle mid-task.** The delivery team is executing a long pipeline -- Development stage, multi-file implementation, tests to write. Claude pauses. Perhaps it believes it is waiting for input. Perhaps it has lost the thread. The user stepped away for coffee. The work stops. There is no mechanism to nudge Claude back into motion without a human physically typing at the terminal.

2. **A rate limit kills momentum.** The session hits a token or rate limit. Claude cannot proceed. The user is not watching. The session sits dead for an hour, two hours, until someone notices. There is no mechanism to wait out the cooldown and then wake Claude back up.

3. **Periodic work requires babysitting.** The user wants "check for new issues every 30 minutes." Today this requires the user to sit at the terminal and type the same prompt every 30 minutes. There is no mechanism to execute a prompt at intervals within a running session.

All three problems share a root cause: once Claude is running, nothing outside the user's keyboard can send input to the terminal. We need a companion process -- a small, disciplined background script -- that watches the session and types into the terminal when Claude needs a push.

This is not scheduling. This is not persistence. This is keeping a live session productive when the human is away from the keyboard.

---

### 2. Goals & Success Metrics

**Goals:**

1. Anti-idle detection resumes stalled work within a configurable timeout
2. Wait-resume mode auto-recovers from rate limits after a cooldown period
3. Monitor mode executes user-specified prompts at regular intervals
4. Cross-platform support: Windows (Bash + PowerShell terminal), Linux (X11 + Wayland), macOS
5. Zero external Python dependencies -- stdlib only for the core script; platform tools (xdotool, ydotool, osascript) are system-level

**Success Metrics:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Anti-idle recovery | Claude resumes work within `interval` seconds of going silent | Start a long task, observe idle, confirm companion sends nudge and work resumes |
| Rate limit recovery | Session resumes automatically after cooldown | Trigger a rate limit, set wait time, confirm companion sends resume message after wait |
| Monitor execution | Prompts delivered at specified intervals | Configure 60-second interval, confirm prompt sent at each interval for 5 cycles |
| Cross-platform | Works on Windows (Bash + PowerShell), Linux (X11 + Wayland), macOS | Run the companion on each platform; terminal input is delivered correctly |
| Self-termination | No orphan processes after session ends | Kill the Claude session, confirm companion exits within 60 seconds |
| Zero dependencies | No pip install required | Inspect imports: only Python stdlib used |

---

### 3. User Personas

**The Long-Session Developer**

This user kicks off a delivery pipeline and walks away. Development stage takes 30 minutes. The user expects to come back and find the work done. Instead, Claude stalled 8 minutes in and has been sitting idle ever since. This user needs a companion that detects silence and says "keep going."

**The Overnight Runner**

This user runs autonomous sessions overnight -- large refactors, multi-file implementations, comprehensive test suites. Rate limits are inevitable. Today, a rate limit at 2 AM means the session is dead until 8 AM when someone notices. This user needs a companion that waits out the cooldown and restarts work automatically.

**The Periodic Monitor**

This user wants Claude to check for new GitHub issues every 30 minutes, or run a code quality sweep every hour. They do not want to type the same prompt repeatedly. They need a companion that sends a prompt to the terminal at fixed intervals.

---

### 4. User Stories

**US-01: Auto-resume on idle**

As a user running a long task, I want Claude to auto-resume when it goes idle, so that work continues without me typing at the keyboard.

**Acceptance Criteria:**
- Companion detects no terminal activity for `--interval` seconds (default: 300)
- Companion sends a configurable nudge message to the terminal
- Claude receives the nudge and resumes working
- Companion waits for activity before nudging again (no rapid-fire nudges)

**US-02: Wait out rate limits**

As a user who hit a rate limit, I want the companion to wait for the cooldown and then resume automatically, so that I do not lose the session.

**Acceptance Criteria:**
- User starts companion with `--mode wait-resume --wait 3600` (1 hour cooldown)
- Companion sleeps for the specified duration
- After sleep, companion sends resume message to the terminal
- Single-shot: companion exits after sending the resume

**US-03: Periodic prompt execution**

As a user, I want to schedule periodic prompts so that Claude performs recurring checks without me babysitting.

**Acceptance Criteria:**
- User starts companion with `--mode monitor --interval 1800 --prompt "Check for new issues"`
- Companion sends the prompt to the terminal every 1800 seconds
- Runs until stopped or `--max-iterations` reached

**US-04: Simple start command**

As a user, I want to start the keepalive with a single command, so that setup is trivial.

**Acceptance Criteria:**
- `python session_keepalive.py --mode anti-idle --interval 300 --pid $PPID &`
- Companion writes its PID to `.delivery/keepalive.lock`
- Companion logs startup to `.delivery/keepalive.log`

**US-05: Simple stop command**

As a user, I want to stop the keepalive cleanly.

**Acceptance Criteria:**
- Deleting `.delivery/keepalive.lock` causes the companion to self-terminate within 30 seconds
- Alternatively: `kill $(cat .delivery/keepalive.lock)` sends SIGTERM, companion exits cleanly
- Companion logs shutdown reason

**US-06: Auto-terminate on session end**

As a user, I want the companion to self-terminate when the Claude session ends, so that no orphan processes linger.

**Acceptance Criteria:**
- Companion checks every 30 seconds if the parent PID is still alive
- If parent PID is gone, companion logs "parent process exited" and terminates
- No orphan companion processes remain after session end

**US-07: Safety rails**

As a user, I want safety mechanisms so the companion does not type into the wrong window or loop endlessly.

**Acceptance Criteria:**
- Window ID is captured at launch and reused for every send (X11/macOS)
- Before every send: verify the target window still exists; if not, log error and exit
- Max nudge cap: `--max-retries` (default: 10 for anti-idle, 1 for wait-resume)
- All actions logged with timestamps to `.delivery/keepalive.log`

**US-08: Cross-platform support**

As a user on any OS, I want this to work on my platform.

**Acceptance Criteria:**
- Linux X11: uses `xdotool` to send keystrokes to the correct window
- Linux Wayland: uses `ydotool` to send keystrokes
- macOS: uses `osascript` to send input to Terminal/iTerm
- Windows: uses PowerShell `SendKeys` via subprocess
- If the required platform tool is missing: graceful exit with install instructions
- Auto-detection via `platform.system()` and `shutil.which()`

---

### 5. Functional Requirements

#### FR-01: Companion Process

A single Python script: `delivery-team/scripts/session_keepalive.py`

**Invocation:**
```bash
python delivery-team/scripts/session_keepalive.py --mode anti-idle --interval 300 --pid $PPID &
```

**Arguments:**

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--mode` | YES | -- | One of: `anti-idle`, `wait-resume`, `monitor` |
| `--interval` | NO | 300 | Seconds between checks (anti-idle) or between prompt sends (monitor) |
| `--wait` | NO | 3600 | Seconds to sleep before sending resume (wait-resume mode only) |
| `--prompt` | NO | See below | Message to send to terminal |
| `--pid` | YES | -- | Parent process PID to monitor for self-termination |
| `--max-retries` | NO | 10 | Maximum nudges before companion gives up (anti-idle/monitor) |
| `--max-iterations` | NO | 0 | Maximum prompt sends for monitor mode (0 = unlimited) |

**Default prompts by mode:**
- `anti-idle`: "Continue working on the current task. Do not stop until complete."
- `wait-resume`: "Resume the previous task. The rate limit cooldown has passed."
- `monitor`: (no default -- user must specify)

**Lifecycle:**
1. Write own PID to `.delivery/keepalive.lock`
2. Log startup: mode, interval, parent PID, platform, detected terminal driver
3. Enter mode-specific loop (see FR-03, FR-04, FR-05)
4. On exit: delete `.delivery/keepalive.lock`, log shutdown reason

#### FR-02: Platform-Specific Terminal Drivers

A `TerminalDriver` abstraction with platform-specific backends, auto-detected at startup.

| Platform | Backend | Mechanism |
|----------|---------|-----------|
| Linux X11 | `xdotool` | `xdotool type --window [wid] "text"` + Enter keystroke |
| Linux Wayland | `ydotool` | `ydotool type "text"` + Enter keystroke (active window) |
| macOS | `osascript` | `osascript -e 'tell app "Terminal" to do script "text"'` |
| Windows | PowerShell | `[System.Windows.Forms.SendKeys]::SendWait("text")` via `subprocess.run(["powershell", ...])` |

**Auto-detection order:**
1. `platform.system()` -- determine OS family
2. For Linux: check `$XDG_SESSION_TYPE` or `$WAYLAND_DISPLAY` to distinguish X11 vs Wayland
3. `shutil.which()` -- verify the required tool is installed
4. If no tool found: log error with install instructions and exit with code 1

**Window ID locking (X11/macOS):**
- At startup, capture the terminal window ID once
- Store it for the lifetime of the companion
- Before every send: verify the window still exists
- If window is gone: log error and exit (do not send to a different window)

#### FR-03: Anti-Idle Mode

**Purpose:** Detect when Claude has gone silent and nudge it to continue.

**Mechanism:**
1. Every `--interval` seconds, check for terminal activity
2. Activity detection: check modification time of `.delivery/keepalive.heartbeat` -- Claude (or a hook) touches this file periodically during active work. If the file has not been modified within `--interval` seconds, Claude is considered idle.
3. If idle: send the nudge message to the terminal via the terminal driver
4. After sending: wait for the heartbeat file to update before nudging again (avoids rapid-fire nudges)
5. Increment nudge counter. If `--max-retries` reached: log warning "max nudges reached, stopping" and exit.

**Heartbeat file:** `.delivery/keepalive.heartbeat` -- a simple file whose modification time indicates activity. The companion monitors this file's mtime. If a heartbeat mechanism is not feasible in v1, fall back to a simple timer: nudge every `--interval` seconds regardless, relying on `--max-retries` to prevent runaway nudging.

#### FR-04: Wait-Resume Mode

**Purpose:** Sleep through a rate limit cooldown, then wake Claude back up.

**Mechanism:**
1. Log: "Waiting [wait] seconds for cooldown..."
2. Sleep for `--wait` seconds (using `time.sleep` with periodic parent-PID checks every 30 seconds)
3. After sleep: send the resume message to the terminal via the terminal driver
4. Log: "Resume message sent."
5. Exit.

This is single-shot. One wait, one send, done.

#### FR-05: Monitor Mode

**Purpose:** Execute a user-specified prompt at regular intervals.

**Mechanism:**
1. Every `--interval` seconds: send `--prompt` to the terminal via the terminal driver
2. Log each send with timestamp and iteration count
3. If `--max-iterations` > 0 and iteration count reaches it: log "max iterations reached" and exit
4. Otherwise: run until stopped (lock file deleted or parent PID gone)

**Example:**
```bash
python session_keepalive.py --mode monitor --interval 1800 --prompt "Check for new GitHub issues and summarize any that are open" --pid $PPID &
```

#### FR-06: Safety Rails

**SR-01: Window ID locking.** Captured once at launch. Reused for every send. Verified before every send. If the window no longer exists, exit immediately.

**SR-02: Parent PID monitoring.** Every 30 seconds (independent of mode interval), check if the parent PID is still alive using `os.kill(pid, 0)` (signal 0 checks existence without killing). If parent is gone, exit.

**SR-03: Killswitch file.** Every 30 seconds, check if `.delivery/keepalive.lock` still exists. If deleted, exit. This gives users a simple stop mechanism: `rm .delivery/keepalive.lock`.

**SR-04: Max retry/nudge cap.** Configurable via `--max-retries`. Prevents infinite nudging. Default: 10 for anti-idle, 1 for wait-resume, configurable for monitor.

**SR-05: Log rotation.** `.delivery/keepalive.log` is rotated when it exceeds 1MB. Old log is renamed to `.delivery/keepalive.log.1` (only one backup kept).

**SR-06: Graceful signal handling.** SIGTERM and SIGINT are caught. On receipt: delete lock file, log shutdown, exit cleanly.

#### FR-07: Delivery-Flow Integration

The following commands are added to the delivery-flow skill vocabulary (in SKILL.md):

| Command | Action |
|---------|--------|
| `keepalive start [mode] [options]` | Claude launches the companion via Bash: `python delivery-team/scripts/session_keepalive.py [args] &` |
| `keepalive stop` | Claude runs: `rm .delivery/keepalive.lock` -- companion self-terminates |
| `keepalive status` | Claude checks: is `.delivery/keepalive.lock` present? If yes, read PID, check if process is alive, tail the log. Report mode, uptime, nudge count. |

These are convenience wrappers. The companion is a standalone script that can be launched directly by the user without delivery-flow.

#### FR-08: Cross-Platform Implementation Constraints

- **Python stdlib only.** Imports limited to: `pathlib`, `subprocess`, `platform`, `shutil`, `time`, `os`, `signal`, `sys`, `argparse`, `datetime`, `logging`.
- **No bash-isms in Python.** No `os.system()`, no shell=True, no backtick expansion.
- **pathlib for all file paths.** No `os.path.join`, no string concatenation for paths.
- **subprocess for platform tools only.** The only subprocess calls are to the terminal drivers (xdotool, ydotool, osascript, powershell).
- **UTF-8 encoding on all file operations.**
- **Works when invoked from:** Bash, Zsh, Fish, PowerShell, CMD.

---

### 6. Non-Functional Requirements

**NFR-01: Low CPU usage.** The companion must not consume meaningful CPU. It sleeps between checks. No busy-waiting, no polling loops shorter than 10 seconds.

**NFR-02: Clean self-termination.** No orphan processes. The companion must exit when: (a) parent PID dies, (b) lock file is deleted, (c) max retries reached, (d) SIGTERM/SIGINT received, or (e) target window no longer exists.

**NFR-03: Bounded log growth.** Log file must not grow unbounded. Rotate at 1MB, keep one backup.

**NFR-04: Non-interference with user input.** If the user returns to the terminal and starts typing, the companion's nudge is a complete message (not partial keystrokes that interleave with user input). The nudge includes a newline/Enter to submit it as a complete prompt.

**NFR-05: Works with Claude Code CLI.** The companion must work with `claude` CLI terminal sessions. It sends text to the terminal where `claude` is running, not to Claude's API.

---

### 7. Out of Scope

- **Cross-session task persistence.** That was the previous PRD's approach. It is a different problem. If we solve it later, it will be a separate feature.
- **GUI or desktop notifications.** The companion is headless.
- **Multi-terminal management.** One companion per session. If you have three terminals, you launch three companions.
- **Automatic mode detection.** The user specifies the mode explicitly. The companion does not try to guess whether Claude is idle vs rate-limited.
- **Integration with CronCreate.** CronCreate is an in-session scheduler. The keepalive companion is a background process. They are separate mechanisms.
- **API-level interaction.** The companion does not call the Anthropic API. It sends keystrokes to a terminal. It is a keyboard automation tool, not an API client.
- **Scheduled task file (.delivery/scheduled-tasks.yml).** The previous PRD's artifact. Not part of this feature.

---

### 8. Dependencies & Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Wrong-window input | **HIGH** -- keystrokes sent to the wrong application (email, browser, chat) | Window ID locked at launch, verified before every send. If window gone, exit. |
| Orphan companion process | **MEDIUM** -- background process lingers after session ends, consuming resources or sending stale nudges | Parent PID monitoring every 30s + killswitch file + signal handling |
| Rate limit loop | **MEDIUM** -- anti-idle nudge triggers work that triggers another rate limit, companion nudges again | Max retry cap + recommend wait-resume mode for rate limit scenarios, not anti-idle |
| Platform tool not installed | **LOW** -- xdotool/ydotool missing on user's system | Graceful exit with specific install instructions for the user's platform |
| Wayland restrictions | **LOW** -- ydotool requires root or input group membership | Document as known limitation; suggest X11 fallback or user group configuration |
| User returns mid-nudge | **LOW** -- companion sends a nudge while user is typing | Nudge is a complete, self-contained message terminated with Enter. User's partial input may be disrupted, but the nudge is not fragmented. |
| Terminal emulator compatibility | **LOW** -- osascript/SendKeys may not work with all terminal emulators | Document tested terminals (Terminal.app, iTerm2, Windows Terminal, GNOME Terminal, Konsole). Provide escape hatch: users can implement custom drivers. |

---

### 9. Open Questions (team resolves)

| # | Question | Owner | Recommendation |
|---|----------|-------|----------------|
| 1 | Should anti-idle detect silence by monitoring a heartbeat file or by simple timer? | Celebrimbor (Architect) | Heartbeat file is more accurate but requires Claude to touch the file during work. Timer is simpler but may nudge Claude while it is actively thinking (not idle, just slow). Recommend: start with timer in v1, add heartbeat in v2 if needed. |
| 2 | Should the keepalive be auto-launched by delivery-flow during long Development stages? | Gandalf (PO) | Manual launch only in v1. Auto-launch is a convenience that can be added once we trust the safety rails. |
| 3 | For Wayland, should we support `wtype` as an alternative to `ydotool`? | Celebrimbor (Architect) | `wtype` works without root but only on Wayland compositors that support wlr-virtual-keyboard-unstable-v1. Document both options, prefer `ydotool` as primary, `wtype` as fallback. |
| 4 | Should the companion detect rate limit messages in terminal output and automatically switch to wait-resume behavior? | Celebrimbor (Architect) | Desirable but complex -- requires reading terminal output, not just sending input. Defer to v2. |
| 5 | What is the right default interval for anti-idle? | Gandalf (PO) | 300 seconds (5 minutes). Short enough to catch genuine stalls, long enough to not interrupt Claude mid-thought. Configurable, so users can tune. |

---

### 10. Timeline

This feature is scoped as a FEATURE type pipeline with the following stage estimates:

| Stage | Effort | Notes |
|-------|--------|-------|
| 1 Idea | Done | Idea brief completed (01-idea-brief.md) |
| 2 Refine (PRD) | Done | This document |
| 3 Design | Light | Terminal driver abstraction, platform detection logic, mode state machines. No UI design -- this is a background script. |
| 4 Architect | Light | File layout, class structure, subprocess safety, signal handling patterns. Integration point: delivery-flow SKILL.md command vocabulary. |
| 5 Plan | Light | 3-5 implementation stories derived from FR-01 through FR-08. |
| 6 Development | Medium | Single script with ~400-600 lines. Terminal drivers are the bulk of the work -- each platform has its own quirks. |
| 7 UAT | Medium | Cross-platform validation (5 backends), safety rail verification, orphan process testing, long-running session test. |

---

*"I am not asking you to build a scheduler. I am asking you to build a companion -- a small, watchful presence that sits beside the session and, when the silence stretches too long, says the words the absent user would have said: keep going."*

-- Gandalf, Product Owner

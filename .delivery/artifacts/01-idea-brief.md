## Idea Brief

**Project Type**: BUG_FIX
**Date**: 2026-03-25
**GitHub Issues**: #39
**Applies To**: delivery-team infrastructure, scheduled task persistence, cross-platform support

### Problem Statement

When a user asks the delivery team to perform a task on a delay — "at 11:05 PM, check for open issues and fix them" — the task dies the moment the session ends. CronCreate is an in-memory scheduler bound to the active REPL. Close the terminal, and the task vanishes as if it never existed.

This is not a minor inconvenience. It means:

1. **Long-delay tasks never fire.** A task scheduled hours out will not survive the user closing their laptop.
2. **External systems cannot trigger the team.** No webhook, no CI event, no scheduled pipeline can wake the delivery team to do work.
3. **The team cannot be "on call."** We exist only while someone is actively sitting in a session. That is a fundamental limitation for any team that claims to deliver.

A delivery team that forgets its commitments the moment you look away is not a delivery team. It is a conversation.

### Target Users

- **Any delivery-flow user** who schedules background work and expects it to actually run
- **Teams using CI/CD pipelines** who want the delivery team to respond to GitHub events (new issues, webhook triggers, scheduled checks)
- **Cross-platform users** on Windows (Bash and PowerShell), Linux, and macOS — the solution must work for all of them without OS-specific dependencies

### Goals

1. Background tasks survive session end — a scheduled task persists and executes even if the originating session is closed
2. External events can trigger the delivery team — GitHub webhooks, CI pipelines, or cron-equivalent mechanisms can invoke Claude Code to perform work
3. Cross-platform by default — Windows (Bash AND PowerShell), Linux, macOS, all supported with a single Python-based implementation, no OS-specific dependencies
4. The solution integrates cleanly with the existing delivery-team plugin structure (hooks, config, artifacts)

### Constraints

- **Python only** — no shell scripts, no OS-specific schedulers (no crontab, no Windows Task Scheduler)
- **No external dependencies** beyond Python stdlib unless the team demonstrates clear justification
- **Cross-platform file paths** — pathlib only, no hardcoded separators
- **Must not break existing hook infrastructure** — CronCreate may still be useful for in-session tasks; this extends capability, it does not replace what works within a session

### Initial Scope

This is a research-first engagement. The team must evaluate five proposed options before any code is written:

| # | Option | Evaluate For |
|---|--------|-------------|
| 1 | **GitHub Actions scheduled workflows** | Cron-triggered Action runs Claude Code headless. Runs in CI, inherently cross-platform. |
| 2 | **Claude Code remote triggers** | Does Claude Code support remote/API triggering? If so, this may be the simplest path. |
| 3 | **Webhook-to-Claude bridge** | GitHub webhook fires on events (new issue, PR), triggers a Claude Code session. |
| 4 | **Persistent task file + SessionStart hook** | Write tasks to `.delivery/scheduled-tasks.yml`. A Python SessionStart hook checks for overdue tasks on next session start and executes them. |
| 5 | **Cross-platform scheduler wrapper** | Python background process using `schedule` library or stdlib `sched` module. |

**Each option must be evaluated against these criteria:**
- Cross-platform support (Windows Bash, Windows PowerShell, Linux, macOS)
- Reliability (does it actually survive session end?)
- Complexity (how much do we build and maintain?)
- Integration (how cleanly does it fit the existing plugin architecture?)

The team produces a recommendation with evidence before moving to design. No option is pre-selected. If the research reveals a sixth option that is clearly superior, the team is free to recommend it — but the five listed above are the minimum investigation set.

### Out of Scope

- Removing or deprecating CronCreate — it works for in-session scheduling and should continue to
- Building a full job queue or message broker — we are solving task persistence, not distributed computing
- Platform-specific optimizations — if it does not work on all three OS families with one codebase, it is out of scope
- Changes to the delivery-flow pipeline stages — this is infrastructure, not workflow modification

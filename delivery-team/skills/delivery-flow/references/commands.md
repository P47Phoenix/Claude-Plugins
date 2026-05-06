# Delivery Flow User Commands Reference

All commands recognized during an active delivery pipeline session.

| Command | Action |
|---------|--------|
| `setup` | Run (or re-run) the setup wizard to configure the delivery pipeline |
| `start` | Begin delivery pipeline (runs wizard first if no config exists) |
| `status` | Show current pipeline state (stage, progress, issues) |
| `skip` | Skip current stage (requires confirmation, records reason) |
| `back` | Return to previous stage for rework |
| `approve` | Approve artifact at human checkpoint |
| `request-changes [feedback]` | Request changes at human checkpoint with specific feedback |
| `abort` | Halt pipeline, preserve all artifacts, write memory file |
| `type <TYPE>` | Override detected project type (e.g., `type FEATURE`) |
| `memory` | Show lessons from past runs relevant to current project |
| `escalate` | Manually trigger escalation for current stage |
| `resume` | Resume a previously interrupted pipeline run |
| `defect-review` | Run defect analysis and check for plugin improvement PR candidates |
| `analytics` | Show pipeline analytics dashboard from memory data |
| `notify` | Send a notification about current pipeline status |
| `health` | Show team health score and retrospective trend analysis |
| `impact [feature]` | Run impact analysis for a feature against existing FKCs |
| `features` | List all feature knowledge cards |
| `stale-features` | List FKCs that need updating |
| `decisions` | List all decisions in the Decision Trail |
| `keepalive start [mode] [options]` | Launch session keepalive companion (anti-idle/wait-resume/monitor) |
| `keepalive stop` | Stop the keepalive companion |
| `keepalive status` | Show keepalive status and log tail |

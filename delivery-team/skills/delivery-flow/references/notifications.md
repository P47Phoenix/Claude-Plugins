# Configurable Notifications & Reporting Hooks

Pipeline events can trigger notifications across multiple channels. Notifications are config-driven and run automatically as part of the post-pipeline protocol (after memory write).

---

## Notification Events

| Event | Trigger | Severity |
|-------|---------|----------|
| `complete` | Pipeline reaches status: completed | info |
| `abort` | Pipeline is aborted (user or system) | warning |
| `escalation` | Dynamic escalation triggered at any stage | warning |
| `checkpoint` | Human checkpoint reached (awaiting approval) | info |
| `defect-threshold` | Defect count exceeds `pipeline.max_self_correction` in a single stage | critical |

---

## Notification Channels

### Console (default, always active)

Announce the event directly in the session. Format:

```
> [NOTIFICATION] Pipeline [pipeline_id]: [event description]
> Stage: [current_stage] | Defects: [count] | Elapsed: [duration]
```

### File

Write a markdown report to `.delivery/reports/<event>-<timestamp>.md`. Create the `reports/` directory if it does not exist.

Report format:

```markdown
# Pipeline Report: [Event]

| Field | Value |
|-------|-------|
| Pipeline ID | [pipeline_id] |
| Event | [event] |
| Timestamp | [ISO timestamp] |
| Status | [pipeline status] |
| Current Stage | [stage name] |
| Stages Completed | [list] |
| Stages Skipped | [list] |
| Defect Count | [total defects across all stages] |
| Time Elapsed | [duration from pipeline start to now] |

## Key Decisions

[List of major decisions made during the pipeline run, extracted from stage artifacts]

## Defect Summary

| Stage | Defect Count | Categories |
|-------|-------------|------------|
| [stage] | [count] | [list of defect categories] |

## Artifacts Produced

| Stage | Artifact | Path |
|-------|----------|------|
| [stage] | [name] | [file path] |

## Memory Lessons Written

[List of memory entries written during this run]
```

### Slack

Requires Slack MCP to be available. Send a concise message to a configured channel.

Slack message format:

```
Pipeline [pipeline_id]: [STATUS]
Stages: [completed]/[total] | Defects: [count] | Duration: [elapsed]
Artifacts: [link to .delivery/artifacts/ or summary]
```

If Slack MCP is not available, log a warning to console and skip silently. Do not fail the pipeline.

### GitHub Discussion

Requires `gh` CLI to be available and authenticated. Create a discussion in the repository's Discussions tab.

```bash
gh discussion create --repo [owner/repo] --title "Pipeline [pipeline_id]: [event]" \
  --body "[full report markdown]" --category "General"
```

If `gh` is not available or discussions are not enabled, log a warning and skip.

---

## Configuration

Config keys in `.delivery/config.md`:

```yaml
notifications:
  channels: [console]          # Which channels to use
  events: [complete, abort, escalation]  # Which events trigger notifications
```

| Key | Type | Default | Valid Values |
|-----|------|---------|-------------|
| `notifications.channels` | list[string] | ["console"] | console, file, slack, github-discussion |
| `notifications.events` | list[string] | ["complete", "abort", "escalation"] | complete, abort, escalation, checkpoint, defect-threshold |

---

## Integration Protocol

Notifications run as the final step in the post-pipeline protocol:

1. Pipeline completes (or aborts/escalates)
2. Memory write executes (per memory-protocol.md)
3. State file is updated
4. **Notification dispatch**:
   a. Determine which event occurred
   b. Check if event is in `notifications.events` list
   c. For each channel in `notifications.channels`, dispatch the notification
   d. Console always fires regardless of config
   e. Log any channel failures as warnings -- never fail the pipeline due to notification errors

### Mid-Pipeline Notifications

Events like `escalation`, `checkpoint`, and `defect-threshold` fire mid-pipeline. The same dispatch protocol applies, but the report reflects partial pipeline state (only completed stages up to that point).

---

## User Command: `notify`

Send a notification about the current pipeline status on demand:

```
> notify
```

Dispatches a status notification across all configured channels with the current pipeline state. Uses the `checkpoint` event format regardless of actual pipeline state.

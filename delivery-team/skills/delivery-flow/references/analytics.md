# Pipeline Analytics Dashboard

## Overview

The `analytics` command aggregates data from `.delivery/memory/` into a markdown dashboard showing pipeline health, stage performance, collaboration effectiveness, and trends over time.

---

## Invocation

| Command | Action |
|---------|--------|
| `analytics` | Show full analytics dashboard from memory data |

---

## Metrics

### Pipeline Runs

| Metric | Description | Source |
|--------|-------------|--------|
| Total runs | Count of all pipeline executions | `memory/archive/run-*.md` files |
| Completed | Runs that reached Stage 7 and passed UAT | Archive files with `status: completed` |
| Aborted | Runs halted before completion | Archive files with `status: aborted` |
| Average stages per run | Mean number of stages executed (including aborted runs) | `stages_completed` arrays in archive |
| Completion rate | Completed / Total as percentage | Derived |

### Stage Health

| Metric | Description | Source |
|--------|-------------|--------|
| First-try pass rate | Percentage of stage executions that passed DoD on the first attempt (no correction loops) | `memory/index.md` stage entries |
| Average correction loops | Mean number of self-correction iterations per stage | Stage health entries in index |
| Most corrected stage | Stage with the lowest first-try pass rate | Derived |
| Stage duration trend | Whether each stage is getting faster or slower over recent runs | Archive timestamps |

### DoD Validator Patterns

| Metric | Description | Source |
|--------|-------------|--------|
| Validator failure rate | Per-validator: how often each validator says NOT DONE | `memory/topics/quality-patterns.md` |
| Most failed criteria | Which specific DoD criteria fail most often | Quality pattern entries |
| Validator agreement rate | How often all validators agree on first pass | Derived |

### Defect Rate Trend

| Metric | Description | Source |
|--------|-------------|--------|
| Defects per story | Count of defects found per story/feature delivered | `memory/topics/defect-patterns.md` |
| Defect trend | Direction over last 5 runs: increasing, decreasing, or stable | Derived |
| Defect origin stage | Which stage's artifacts produce the most downstream defects | Defect registry data |

### Collaboration Pattern Effectiveness

| Metric | Description | Source |
|--------|-------------|--------|
| Pattern usage count | How many times each collaboration pattern was invoked | `memory/topics/collaboration-patterns.md` |
| Issues caught per pattern | Number of issues, gaps, or improvements identified by each pattern | Pattern outcome entries |
| Most effective pattern | Pattern with the highest issues-caught-per-invocation ratio | Derived |

### Human Checkpoint Patterns

| Metric | Description | Source |
|--------|-------------|--------|
| Approval rate | Percentage of checkpoints approved on first presentation | `memory/topics/checkpoint-patterns.md` |
| Common change requests | Recurring themes in human feedback at checkpoints | Checkpoint entries |
| Average checkpoint iterations | Mean attempts before approval | Derived |

### Adversarial Review

| Metric | Description | Source |
|--------|-------------|--------|
| Average confidence | Mean adversarial reviewer confidence score across reviews | `memory/topics/review-patterns.md` |
| Escalation frequency | How often adversarial review triggers escalation to human | Review pattern entries |
| Issues found per review | Average number of issues identified per adversarial review | Derived |

---

## Data Sources

| Source | Location | Contains |
|--------|----------|----------|
| Routing index | `memory/index.md` | Stage health summaries, run metadata, quick-access pointers |
| Topic chunks | `memory/topics/*.md` | Pattern data by category: quality, defects, collaboration, checkpoints, reviews |
| Run archives | `memory/archive/run-*.md` | Raw data for each pipeline run: timestamps, decisions, corrections, outcomes |

### Reading Protocol

1. Start with `memory/index.md` to get summary-level metrics and identify which topic files have relevant data.
2. Read specific `memory/topics/*.md` files for pattern-level metrics.
3. Read `memory/archive/run-*.md` files only when deep analysis is needed (e.g., trend calculation across runs).

---

## Output Format

The dashboard is rendered as markdown with tables and trend indicators.

### Trend Indicators

| Indicator | Meaning |
|-----------|---------|
| [UP] | Metric is increasing compared to baseline |
| [DOWN] | Metric is decreasing compared to baseline |
| [STABLE] | Metric is within 5% of baseline |

### Dashboard Template

```markdown
## Pipeline Analytics Dashboard
Generated: [date] | Runs analyzed: [N] | Period: [first run date] to [last run date]

### Pipeline Health
| Metric | Value | Trend |
|--------|-------|-------|
| Total runs | N | -- |
| Completion rate | N% | [TREND] |
| Average stages/run | N.N | [TREND] |

### Stage Health
| Stage | First-Try Pass Rate | Avg Corrections | Trend |
|-------|--------------------:|----------------:|-------|
| 1. Idea | N% | N.N | [TREND] |
| 2. Refine | N% | N.N | [TREND] |
| ... | ... | ... | ... |

### DoD Validator Performance
| Validator | Failure Rate | Top Failed Criteria |
|-----------|-------------:|---------------------|
| [role] | N% | [criteria] |

### Defect Trends
| Metric | Current | Baseline | Trend |
|--------|--------:|---------:|-------|
| Defects/story | N.N | N.N | [TREND] |

### Collaboration Effectiveness
| Pattern | Uses | Issues Caught | Effectiveness |
|---------|-----:|--------------:|--------------:|
| Evaluator-Optimizer | N | N | N.N/use |
| Adversarial Review | N | N | N.N/use |
| Review Board | N | N | N.N/use |
| Debate | N | N | N.N/use |
| Consensus | N | N | N.N/use |

### Human Checkpoints
| Metric | Value | Trend |
|--------|------:|-------|
| First-pass approval rate | N% | [TREND] |
| Avg iterations to approve | N.N | [TREND] |
```

---

## Comparison Modes

### Current Sprint vs Baseline

- **Baseline**: Average of all runs except the most recent.
- **Current**: The most recent completed run (or in-progress run).
- Used for trend indicators in the dashboard.

### Current vs Last 5 Runs

- When requested with `analytics detailed`, show a run-by-run breakdown for the last 5 runs.
- Includes per-run: completion status, stages executed, correction count, defects found, total duration.

---

## When to Show Analytics

- On explicit `analytics` command.
- Optionally at the end of a completed pipeline run (if `pipeline.show_analytics_on_complete` is true in config).
- During `memory` command as a summary section.

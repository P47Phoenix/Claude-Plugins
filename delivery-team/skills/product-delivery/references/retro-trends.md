# Retrospective Trend Analysis & Team Health Score

Analyze patterns across multiple retrospective memory entries to identify recurring themes, compute a team health score, and produce a retro-of-retros summary. This reference is used by the Scrum Bag role as part of retrospective facilitation.

---

## Theme Extraction

Scan retrospective memory entries in `.delivery/memory/` and archive run files to extract recurring themes. Group themes into six categories:

| Category | What to Look For |
|----------|-----------------|
| **Communication** | Handoff gaps, unclear requirements, misaligned expectations, stakeholder feedback delays |
| **Process** | Ceremony effectiveness, pipeline friction, stage bottlenecks, approval delays |
| **Tooling** | Tool failures, missing integrations, CI/CD issues, development environment problems |
| **Quality** | Defect rates, test coverage gaps, regression frequency, validation failures |
| **Velocity** | Throughput changes, story completion rates, estimation accuracy, scope creep |
| **Morale** | Team satisfaction signals, burnout indicators, collaboration quality, autonomy concerns |

### Persistence Detection

A theme is **persistent** if it appears in 3 or more consecutive retrospectives. Persistent themes require escalation:

- Flag with `[PERSISTENT]` label in the retro report
- Recommend a dedicated improvement initiative (not just an action item)
- Track whether previous action items for this theme were completed or abandoned

### Theme Extraction Protocol

1. Read `.delivery/memory/topics/gate-patterns.md` for quality gate trends
2. Read `.delivery/memory/topics/defect-patterns.md` for defect category trends
3. Read `.delivery/memory/topics/human-preferences.md` for approval/rejection patterns
4. Scan archive run files in `.delivery/memory/archive/` for retrospective sections
5. For each entry, extract themes and categorize them
6. Count occurrences across runs and flag persistent themes

---

## Team Health Score

A composite score from 1 to 10 based on five pipeline health indicators. Each indicator contributes up to 2 points.

### Indicators

| Indicator | Data Source | Scoring |
|-----------|------------|---------|
| **Defect Rate Trend** | `defect-patterns.md`, archive runs | Improving (decreasing over last 3 runs): +2. Stable: +1. Worsening: +0. |
| **Correction Loop Frequency** | Archive run files (self-correction counts) | Decreasing: +2. Stable: +1. Increasing: +0. |
| **Human Checkpoint Approval Rate** | `human-preferences.md`, archive runs | > 80% first-try approval: +2. 50-80%: +1. < 50%: +0. |
| **Adversarial Confidence Trend** | Archive run files (adversarial review scores) | Increasing: +2. Stable: +1. Decreasing: +0. |
| **DoD First-Try Pass Rate** | `gate-patterns.md`, archive runs | > 70% pass on first attempt: +2. 40-70%: +1. < 40%: +0. |

### Score Interpretation

| Score | Health Level | Action |
|-------|-------------|--------|
| 9-10 | Excellent | Maintain current practices. Consider reducing ceremony. |
| 7-8 | Good | Minor improvements. Address any persistent themes. |
| 5-6 | Fair | Focused improvement needed. Prioritize 1-2 weak indicators. |
| 3-4 | Concerning | Significant process issues. Dedicated improvement sprint recommended. |
| 1-2 | Critical | Pipeline is not delivering value effectively. Full process review needed. |

### Trend Direction

In addition to the absolute score, report the trend direction:

- **Improving**: score increased by 1+ over last 3 runs
- **Stable**: score unchanged (+/- 0.5) over last 3 runs
- **Declining**: score decreased by 1+ over last 3 runs

---

## Retro of Retros

A summary command that aggregates across the last N retrospectives (default: 5, configurable).

### Output Format

```markdown
# Retro of Retros: Last [N] Runs

## What Keeps Coming Up? (Persistent Themes)

| Theme | Category | Occurrences | First Seen | Action Items Attempted | Resolved? |
|-------|----------|-------------|------------|----------------------|-----------|
| [theme] | [category] | [count] | [run date] | [count] | Yes/No |

## What's Improving? (Positive Trends)

| Area | Trend | Evidence |
|------|-------|----------|
| [indicator or theme] | [description] | [data points] |

## What's Getting Worse? (Negative Trends)

| Area | Trend | Evidence | Recommended Action |
|------|-------|----------|--------------------|
| [indicator or theme] | [description] | [data points] | [specific action] |

## Team Health: [X]/10 ([direction])

| Indicator | Score | Trend | Notes |
|-----------|-------|-------|-------|
| Defect Rate | [0-2] | [direction] | [details] |
| Correction Loops | [0-2] | [direction] | [details] |
| Checkpoint Approvals | [0-2] | [direction] | [details] |
| Adversarial Confidence | [0-2] | [direction] | [details] |
| DoD First-Try Pass | [0-2] | [direction] | [details] |

## Recommendations

1. [Prioritized recommendation based on data]
2. [...]
3. [...]
```

---

## Data Sources

| Source | Location | What It Provides |
|--------|----------|-----------------|
| Gate patterns | `.delivery/memory/topics/gate-patterns.md` | DoD pass/fail rates, common failure reasons |
| Defect patterns | `.delivery/memory/topics/defect-patterns.md` | Defect categories, frequency, severity trends |
| Human preferences | `.delivery/memory/topics/human-preferences.md` | Approval rates, common change requests, preference patterns |
| Archive runs | `.delivery/memory/archive/run-*.md` | Per-run retrospective data, correction counts, adversarial scores |

---

## Integration

The Scrum Bag role runs this analysis as part of retrospective facilitation:

1. When a retrospective is requested, load this reference
2. Extract themes from available memory data
3. Compute team health score
4. Present the retro-of-retros summary before facilitating the current retrospective
5. Use trends to inform the retrospective focus areas -- if a theme is persistent, the retro should prioritize it
6. After the retrospective, update memory with new themes and action items

The `health` command in delivery-flow triggers this analysis on demand without running a full retrospective.

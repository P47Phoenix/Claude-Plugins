# Defect Tracking and Plugin Self-Improvement Protocol

## Overview

When the delivery team finds defects in completed work, those defects are not just bugs to fix -- they are signals that the plugin's skills, references, or guardrails have a gap. This protocol tracks defects, detects patterns, and triggers PRs to the Claude-Plugins repo to prevent recurrence across ALL future projects.

## Defect Registry (in target project)

Location: `.delivery/defects/` in the working directory.

Structure:
```
.delivery/defects/
  index.md          # Summary: counts, rates, categories, trends
  sprint-N.md       # Defects per sprint (one file per sprint)
```

### index.md Format

A compact summary rebuilt after each sprint:

```markdown
# Defect Index

**Last updated**: YYYY-MM-DD
**Total defects**: N across M stories (rate: X/story)
**Target rate**: <0.3 defects/story

## Rate Trend
| Sprint | Stories | Defects | Rate | Delta |
|--------|---------|---------|------|-------|
| 1-4 | 14 | 12 | 0.86 | baseline |
| 5 | 4 | 2 | 0.50 | -0.36 |

## Top Categories
| Category | Count | % | Plugin Coverage |
|----------|-------|---|-----------------|
| Control input blocking | 3 | 25% | validation.md #6 |
| Integration wiring | 2 | 17% | defect-prevention.md |
| @onready lifecycle | 2 | 17% | validation.md #1 |

## Open Plugin PRs
| PR | Category | Status |
|----|----------|--------|
| #5 | New: shader compilation pattern | Open |
```

### sprint-N.md Format

Individual defect entries per sprint:

```markdown
# Sprint N Defects

## DEF-001: [Short description]
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **Category**: [From defect categories]
- **Story**: Sprint N, Story "[title]"
- **Root cause**: [Why this happened -- the real reason, not the symptom]
- **Detected by**: Code inspection / Headless validation / Manual playtest / UAT
- **Escaped from**: Stage [N] -- [why the gate did not catch it]
- **Prevention**: [How to prevent in future]
- **Plugin PR**: none / PR #N to Claude-Plugins (if pattern is systemic)
```

## Defect Classification

### When a Defect Becomes a PR

Not every defect warrants a plugin improvement PR. Use these rules:

| Condition | Action |
|-----------|--------|
| Single occurrence, unique bug | Log in project defects only. No PR. |
| 2+ occurrences of same root cause | Candidate for PR. Check if existing reference covers it. |
| New category not in any reference | PR required -- the skill has a blind spot. |
| Existing reference covers it but did not prevent it | PR to improve the reference (better detection, stronger wording, add to guardrails). |
| CRITICAL/HIGH severity pattern | Fast-track PR -- do not wait for 2nd occurrence. |
| LOW severity, single occurrence | Log only. Revisit if it recurs. |

### Classification Flow

1. Defect found (during UAT, manual testing, or post-release).
2. Log in `.delivery/defects/sprint-N.md`.
3. Categorize: match to existing defect categories or create new category.
4. Check frequency: first occurrence or recurring?
5. If recurring or new category, check if covered by existing skill reference.
6. If not covered or coverage insufficient, draft plugin improvement PR.
7. Update `.delivery/defects/index.md` with new counts and rates.

## Plugin Improvement PR Process

### When to Open a PR

Open a PR to the Claude-Plugins repo when:
- A defect category appears 2+ times (systemic pattern).
- A new defect category is identified that no existing reference covers.
- A CRITICAL defect reveals a blind spot (even on first occurrence).
- An existing reference covers the pattern but failed to prevent it (reference needs strengthening).

### What the PR Changes

| Defect Type | PR Target | Example Change |
|-------------|-----------|----------------|
| New bug pattern | Skill reference file (e.g., validation.md) | Add pattern #N with detection strategy |
| New guardrail needed | SKILL.md guardrails section | Add "Never do X" guardrail |
| Checklist gap | defect-prevention.md | Add checklist item with detection command |
| Gate criteria gap | quality-gates.md | Add blocking criterion to relevant gate |
| Empirical validation gap | empirical-validation.md | Add technology-specific pattern |
| Process gap | pipeline-stages.md or team-patterns.md | Update stage flow or collaboration pattern |

### PR Creation Protocol

1. **Branch**: `defect-fix/<short-description>` from main.
2. **Title**: `[DEFECT-FIX] <description>`.
3. **Label**: `defect-prevention`.
4. **Template**: Use bug_fix.md template with Defect Data section filled in.
5. **Content**:
   - The specific file change (reference, SKILL.md, quality-gates.md).
   - Defect data: rate, frequency, category, affected stories.
   - Before/after: what the skill does now vs what it would do after the fix.
6. **Review**: PR is reviewed like any other -- the fix must follow existing patterns.

### PR Body Template for Defect PRs

```markdown
## Bug Description
[Defect pattern description -- what goes wrong and when]

## Root Cause
[Why the current skill/reference does not catch this]

## Fix
[What this PR changes -- new pattern, guardrail, checklist item, etc.]

## Defect Data
- **Defect rate**: [X defects/story over N stories]
- **Pattern frequency**: [N occurrences across M sprints]
- **Root cause category**: [category name]
- **Affected skill**: [skill/reference being updated]
- **Stories affected**: [list of story IDs]

## Verification
- [ ] New pattern/guardrail would have caught the original defects
- [ ] No regression in existing skill behavior
```

## Integration with Delivery Pipeline

### Where Defect Tracking Happens

| Pipeline Point | What Happens |
|----------------|-------------|
| Stage 6 (Dev) | QA reviews catch defects before they escape -- logged as self-correction, not defects |
| Stage 7 (UAT) | Defects found during UAT are logged to `.delivery/defects/` |
| Human Checkpoint 4 | User reports defects found during manual validation |
| Post-pipeline retrospective | Scrum Master analyzes defect patterns, classifies as one-off vs systemic |
| Defect review step | If systemic patterns found, draft and open plugin improvement PR |

### Post-Pipeline Defect Review

After the retrospective, before closing the pipeline run:

1. **Count defects**: Calculate defects/story rate for this sprint.
2. **Categorize**: Group defects by root cause category.
3. **Compare to history**: Is the rate improving? Which categories are persistent?
4. **Check coverage**: For each defect category:
   - Is it covered by an existing skill reference?
   - If yes, did the coverage fail to prevent it? Why?
   - If no, this is a blind spot -- PR candidate.
5. **Draft PRs**: For qualifying patterns, create improvement PRs.
6. **Update index**: Rebuild `.delivery/defects/index.md` with current data.
7. **Update memory**: Write defect patterns to `memory/topics/defect-patterns.md`.

### Product Owner Responsibility

The PO tracks defect re-entry rate as a product quality metric:
- Defects/story rate per sprint (target: <0.3).
- Category distribution (which categories are persistent?).
- Plugin PR status (are improvements being merged?).
- Rate trend (is it decreasing over time?).

## Roles in Defect Tracking

| Role | Responsibility |
|------|---------------|
| **QA Engineer** | Detect and log defects, classify severity, identify root cause |
| **Product Owner** | Track defect rate as metric, prioritize plugin improvement PRs |
| **Scrum Master** | Facilitate defect review in retrospective, track action items |
| **Developer** | Provide root cause analysis, implement fixes |
| **Architect** | Review architectural defect patterns, approve structural changes |

## Memory Integration

Defect patterns are stored in `memory/topics/defect-patterns.md` (see memory-protocol.md):

```markdown
# Defect Patterns

**Entries**: N | **Last updated**: YYYY-MM-DD

## Rate Trend
- Sprint 1-4: 0.86 defects/story (baseline)
- Sprint 5: 0.50 (checklist adoption)
- Sprint 6: 0.25 (below target)

## Persistent Categories
- Control input blocking: 3 occurrences, covered by validation.md #6 (validated: 3)
- Integration wiring: 2 occurrences, covered by defect-prevention.md (validated: 2)

## Plugin PRs Opened
- PR #5: shader compilation pattern (open)
- PR #3: mouse_filter + QA heuristics (merged)

## Lessons
- Defect prevention checklist reduced rate by 42% in first sprint of adoption (validated: 1)
- CRITICAL defects are 90% empirical (require runtime validation) (validated: 2)
```

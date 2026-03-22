# Self-Learning Memory Protocol

## Overview

The delivery pipeline learns from every run. Memory files are stored in the **current working directory** at `.delivery/memory/`, making them project-specific and portable with the codebase.

## Directory Structure

```
.delivery/
├── artifacts/           # Stage output files
│   ├── 01-idea-brief.md
│   ├── 02-prd.md
│   ├── 03-ux-design.md
│   ├── 04-architecture.md
│   ├── 04a-adrs/
│   │   └── ADR-001.md
│   ├── 05-sprint-plan.md
│   ├── 06-dev-notes.md
│   ├── 07-uat-report.md
│   ├── 07a-release-plan.md
│   └── 07b-documentation.md
└── memory/              # Learning from past runs
    ├── run-2026-03-21-a1b2.md
    ├── run-2026-03-25-c3d4.md
    └── lessons-index.md  # Aggregated lessons by category
```

## Memory File Format

Each pipeline run produces a memory file at completion (or abort):

```markdown
---
run_id: run-YYYY-MM-DD-<4char-id>
project_type: GREENFIELD | FEATURE | BUG_FIX | GAME_DEV+X | SPIKE | DOCS_ONLY
stages_executed: [list]
stages_skipped: [list]
completed: true | false
abort_stage: <stage name if aborted>
date: YYYY-MM-DD
---

## Gate Results

| Stage | Gate | First Try | Iterations | Final |
|-------|------|-----------|------------|-------|
| Idea | Completeness | PASS | 1 | PASS |
| Refine | PRD Quality | FAIL | 3 | PASS |
| ... | ... | ... | ... | ... |

## Self-Correction Log

### Stage 2: Refine -- 3 iterations needed
- **Iteration 1 failure**: Missing NFR quantification. "Fast" used instead of measurable target.
- **Iteration 2 failure**: Out-of-scope section still empty.
- **Iteration 3 success**: All criteria met after explicit feedback.
- **Lesson**: PRDs for this project tend to omit NFR quantification. Future runs should pre-prompt PO with "quantify all NFRs."

## Human Checkpoint Deltas

### Checkpoint 1: PRD Approval
- **Pre-approval state**: [summary of what was presented]
- **Human feedback**: [what the user changed/requested]
- **Post-approval delta**: [specific changes made]
- **Lesson**: [what this teaches for future runs, e.g., "User prefers more detailed acceptance criteria than the default PO output produces"]

### Checkpoint 2: Architecture Approval
[same structure]

## Adversarial Review Insights

### Stage 2: Refine
- Challenger confidence: 3/5
- Valid findings accepted: [list]
- Findings rebutted: [list]
- **Lesson**: [what the adversarial review caught that was genuinely useful]

## Team DoD Results

### Stages that needed multiple DoD rounds
- Stage 4 (Architect): DevOps validator flagged missing deployment strategy. Fixed in round 2.
- **Lesson**: Architecture artifacts should always include a deployment section.

## Decision Log

| Decision | Type | Owner | Choice | Rationale |
|----------|------|-------|--------|-----------|
| Message broker | Technical | Architect | RabbitMQ | Lower complexity for team size |
| MVP scope | Scope | PO | Cut feature X | Time constraint |

## Debate Outcomes

### Microservices vs Modular Monolith
- **Decision**: Modular monolith
- **Key argument**: Team of 3 cannot sustain microservices operationally
- **Revisit condition**: When team grows to 8+

## Performance Notes
- Slowest stage: Architect (3 evaluator-optimizer cycles)
- Fastest stage: Idea (no self-correction needed)
- Total escalations to human: 1 (DoD failure at Plan stage)
```

## Lessons Index

The `lessons-index.md` file aggregates lessons across all runs for quick retrieval:

```markdown
# Delivery Pipeline -- Lessons Index

## By Stage

### Refine
- PRDs for this project consistently miss NFR quantification (runs: a1b2, c3d4)
- User prefers detailed acceptance criteria with edge cases (run: a1b2)

### Architect
- Always include deployment section in architecture docs (runs: a1b2, e5f6)
- Team size < 5: modular monolith preferred over microservices (run: a1b2)

### Plan
- Sprint estimates tend to be 20% optimistic for this codebase (runs: c3d4, e5f6)

## By Project Type

### GREENFIELD
- Full pipeline takes ~7 stages; Design and Architect are the longest
- Adversarial review most valuable at Refine stage

### BUG_FIX
- Light Plan stage is sufficient for single-bug fixes
- QA DoD validator catches missing regression tests

## Cross-Cutting
- Adversarial confidence <= 2 always correlates with human changes at checkpoint
- DoD round 1 failures are 60% from QA validator (testability concerns)
```

## Memory Retrieval Protocol

Before starting a pipeline run:

1. Check if `.delivery/memory/` exists in the working directory
2. If yes, read `lessons-index.md` for aggregated lessons
3. Filter lessons relevant to:
   - The detected project type
   - The stages that will execute
4. Inject relevant lessons into agent prompts as context:
   ```
   Lessons from past runs on this project:
   - [Lesson 1]
   - [Lesson 2]
   Consider these as you work. They reflect patterns observed in previous deliveries.
   ```
5. If no memory exists, proceed without -- first run establishes the baseline

## Memory Update Protocol

After pipeline completion (or abort):

1. Construct the memory file from pipeline execution data:
   - Gate results (pass/fail per stage, iteration counts)
   - Human checkpoint deltas (what changed at approval)
   - Adversarial review insights (what was valid)
   - DoD validation patterns (which validators found issues)
   - Decisions made and their context
   - Debate outcomes
2. Write to `.delivery/memory/run-YYYY-MM-DD-<id>.md`
3. Update `lessons-index.md`:
   - Add new lessons from this run
   - Consolidate repeated lessons (increment run count)
   - Remove lessons contradicted by this run's evidence
4. Keep max 20 run files (delete oldest when exceeded)

## Memory Decay

- Lessons from the last 5 runs are weighted most heavily
- Lessons older than 10 runs are candidates for removal (unless they keep being validated)
- If a lesson is contradicted by 3 consecutive runs, remove it

## .gitignore Consideration

The `.delivery/` directory can be:
- **Committed**: Team shares memory and artifacts (recommended for team projects)
- **Gitignored**: Memory stays local (useful for personal projects or sensitive content)
- The skill should create `.delivery/` but NOT modify `.gitignore` -- leave that choice to the user

# Self-Learning Memory Protocol

## Overview

The delivery pipeline learns from every run. Memory files are stored in the **current working directory** at `.delivery/memory/`, making them project-specific and portable with the codebase.

Memory is organized as a **tiered retrieval system**: a compact routing index points to chunked topic files, so the AI reads only what's relevant — never the entire memory.

## Design Principle: Read Less, Find More

The AI should never need to read all memory files to find what it needs. The system uses:

1. **Routing index** (~50 lines max) — the ONLY file read on every pipeline start. Contains topic pointers, not lessons themselves.
2. **Chunked topic files** (~100 lines max each) — organized by what the AI would be searching for. Only the relevant chunk is loaded per stage.
3. **Run archive** — raw run logs for deep analysis. Never read during normal pipeline execution.

This means: **1 file read to route + 1-2 file reads to get context = 2-3 reads max per stage.**

---

## Directory Structure

```
.delivery/
├── artifacts/                    # Stage output files (current run)
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
└── memory/
    ├── index.md                  # Routing index (~50 lines) — ALWAYS read first
    ├── stages/                   # Lessons chunked by stage
    │   ├── idea.md               # Lessons for Idea stage (~100 lines max)
    │   ├── refine.md             # Lessons for Refine stage
    │   ├── design.md             # Lessons for Design stage
    │   ├── architect.md          # Lessons for Architect stage
    │   ├── plan.md               # Lessons for Plan stage
    │   ├── development.md        # Lessons for Development stage
    │   └── uat.md                # Lessons for UAT stage
    ├── topics/                   # Lessons chunked by cross-cutting topic
    │   ├── human-preferences.md  # What the user changed at checkpoints
    │   ├── team-decisions.md     # Decisions log with context
    │   ├── gate-patterns.md      # Which gates fail and why
    │   └── project-types.md      # Lessons per project type
    └── archive/                  # Raw run logs (not read during normal execution)
        ├── run-2026-03-21-a1b2.md
        └── run-2026-03-25-c3d4.md
```

---

## Tier 1: Routing Index

`memory/index.md` is the ONLY file read at pipeline start. It is a compact pointer file (~50 lines max) that tells the AI where to look for relevant context.

```markdown
# Memory Index

**Last updated**: 2026-03-25
**Total runs**: 5
**Project types seen**: GREENFIELD (3), FEATURE (2)

## Stage Health (last 5 runs)

| Stage | First-Try Pass Rate | Avg Iterations | Top Issue |
|-------|--------------------:|---------------:|-----------|
| Idea | 100% | 1.0 | — |
| Refine | 40% | 2.4 | NFR quantification → stages/refine.md |
| Design | 80% | 1.2 | Accessibility gaps → stages/design.md |
| Architect | 60% | 2.0 | Missing deployment → stages/architect.md |
| Plan | 60% | 1.8 | Optimistic estimates → stages/plan.md |
| Dev | 80% | 1.4 | Test coverage → stages/development.md |
| UAT | 100% | 1.0 | — |

## Hot Lessons (top 5 most impactful, validated 3+ times)

1. PRDs consistently miss NFR quantification → stages/refine.md
2. Architecture must include deployment section → stages/architect.md
3. Sprint estimates 20% optimistic → stages/plan.md
4. User prefers detailed acceptance criteria → topics/human-preferences.md
5. Adversarial confidence ≤2 predicts human changes → topics/gate-patterns.md

## Topic Files (read when relevant)

| Topic | When to Read | File |
|-------|-------------|------|
| Human preferences | Before any human checkpoint | topics/human-preferences.md |
| Team decisions | Before Architect or Plan stages | topics/team-decisions.md |
| Gate failure patterns | Before any stage with <80% pass rate | topics/gate-patterns.md |
| Project type patterns | At pipeline start (type-specific lessons) | topics/project-types.md |
```

**Key design**: The index contains POINTERS to chunk files, not the lessons themselves. It stays compact because it only tracks aggregated stats and the top 5 most impactful lessons.

---

## Tier 2: Stage Chunks

Each `memory/stages/<stage>.md` file contains lessons specific to that stage. The AI reads only the chunk for the stage it's about to execute.

**Max size**: ~100 lines per file. When a chunk exceeds 100 lines, the oldest/least-validated lessons are pruned.

### Format

```markdown
# Stage: Refine — Lessons

**Entries**: 8 | **Last updated**: 2026-03-25

## Gate Patterns

- NFR quantification missing in 3/5 runs. Pre-prompt PO: "Quantify all NFRs with measurable targets." (validated: 3, last: run-c3d4)
- Out-of-scope section left empty in 2/5 runs. Include "Out of Scope" as mandatory prompt section. (validated: 2, last: run-c3d4)

## Self-Correction Insights

- Iteration 1 failures are usually missing sections, not quality issues. Feedback should say "section X is missing" not "improve quality." (validated: 2, last: run-e5f6)
- Max 2 iterations usually sufficient for Refine if feedback is specific. (validated: 3, last: run-c3d4)

## Adversarial Review

- Challenger most valuable at Refine for catching assumption gaps. (validated: 3, last: run-e5f6)
- Average confidence: 3.2/5. Confidence ≤2 occurred in 1/5 runs (led to human escalation). (validated: 2, last: run-a1b2)

## DoD Validator Patterns

- QA validator flags testability issues most often (60% of NOT_DONE findings). (validated: 3, last: run-c3d4)
- Architect validator rarely blocks at Refine (only for technically impossible requirements). (validated: 2, last: run-e5f6)
```

### Chunk per Stage

Each stage chunk follows the same structure:
- **Gate Patterns**: what fails and how to prevent it
- **Self-Correction Insights**: what kind of feedback works
- **Collaboration Pattern Notes**: which patterns helped, adversarial confidence trends
- **DoD Validator Patterns**: which validators find issues most often

---

## Tier 2: Topic Chunks

Cross-cutting lessons that span multiple stages, chunked by topic.

### `topics/human-preferences.md` (~100 lines max)

What the user changed at checkpoints — the most valuable memory for reducing future checkpoint friction.

```markdown
# Human Preferences

**Entries**: 6 | **Last updated**: 2026-03-25

## Checkpoint Style

- User prefers concise summaries at checkpoints, not full artifact dumps. (validated: 3)
- User wants to see trade-off tables, not prose explanations. (validated: 2)

## PRD Preferences

- Acceptance criteria should include edge cases, not just happy path. (validated: 3)
- User adds business context that PO doesn't infer — always ask "what business context is missing?" (validated: 2)

## Architecture Preferences

- User values simplicity over scalability for this project. (validated: 2)
- Diagrams preferred over prose for system design. (validated: 3)

## Plan Preferences

- User reduces scope rather than extending timeline when estimates are high. (validated: 2)
```

### `topics/team-decisions.md` (~100 lines max)

Decisions with lasting impact that future runs should respect.

```markdown
# Team Decisions

**Entries**: 4 | **Last updated**: 2026-03-25

## Active Decisions

| Decision | Choice | Rationale | Revisit When | Run |
|----------|--------|-----------|-------------|-----|
| Architecture style | Modular monolith | Team of 3 can't sustain microservices | Team grows to 8+ | a1b2 |
| Message broker | RabbitMQ | Lower complexity | Performance ceiling hit | a1b2 |
| Test framework | Jest + Playwright | Team familiarity | Major version upgrade | c3d4 |

## Superseded Decisions

| Decision | Old Choice | New Choice | Why Changed | Run |
|----------|-----------|-----------|-------------|-----|
```

### `topics/gate-patterns.md` (~100 lines max)

Cross-stage patterns about what makes gates pass or fail.

### `topics/project-types.md` (~100 lines max)

Lessons specific to project types (GREENFIELD vs FEATURE vs BUG_FIX, etc.).

---

## Tier 3: Run Archive

Raw run logs in `memory/archive/`. These are NOT read during normal pipeline execution — they exist for:
- Deep analysis when a pattern is unclear
- Debugging when the AI needs to understand a specific past run
- Auditing decisions

### Run File Format

```markdown
---
run_id: run-YYYY-MM-DD-<4char-id>
project_type: GREENFIELD
stages_executed: [idea, refine, design, architect, plan, dev, uat]
stages_skipped: []
completed: true
date: YYYY-MM-DD
---

## Gate Results

| Stage | Gate | First Try | Iterations | Final |
|-------|------|-----------|------------|-------|
| Idea | Completeness | PASS | 1 | PASS |
| Refine | PRD Quality | FAIL | 3 | PASS |

## Self-Correction Log
[Full detail per iteration]

## Human Checkpoint Deltas
[Pre/post approval diffs]

## Adversarial Review Log
[Challenger findings and responses]

## DoD Validation Log
[Validator votes per stage]

## Decision Log
[All decisions with full context]

## Debate Outcomes
[Full debate arguments and judge reasoning]
```

### Archive Limits
- Max 20 run files
- When exceeded, delete oldest
- Before deleting, ensure all lessons from that run are captured in stage/topic chunks

---

## Memory Retrieval Protocol

### At Pipeline Start (Phase 2)

1. Read `memory/index.md` (always — this is the routing step)
2. Note the "Hot Lessons" — these are injected into ALL agent prompts
3. Note stages with <80% first-try pass rate — flag for extra attention

### Before Each Stage

1. Read `memory/stages/<stage>.md` for the current stage
2. If this stage has a human checkpoint, also read `topics/human-preferences.md`
3. If this stage involves decisions (Architect, Plan), also read `topics/team-decisions.md`
4. If this stage's pass rate is <80% (from index), also read `topics/gate-patterns.md`

**Total reads per stage: 1-3 files, never more.**

### Injection Format

Pass lessons to agent prompts as:
```
Lessons from past runs on this project (apply these):
- [Lesson 1 — from stages/<stage>.md]
- [Lesson 2 — from hot lessons]
- [Lesson 3 — from human preferences if checkpoint stage]

Active decisions to respect:
- [Decision 1 — from team-decisions.md]
```

---

## Memory Update Protocol

After pipeline completion (or abort):

### Step 1: Write Run Archive
Write raw run log to `memory/archive/run-YYYY-MM-DD-<id>.md` with full detail.

### Step 2: Extract and Route Lessons
For each lesson learned in this run, route to the appropriate chunk:
- Stage-specific lesson → `memory/stages/<stage>.md`
- Human preference learned → `topics/human-preferences.md`
- Decision made → `topics/team-decisions.md`
- Gate pattern observed → `topics/gate-patterns.md`
- Project type insight → `topics/project-types.md`

### Step 3: Deduplicate and Validate
When adding a lesson to a chunk:
- If a similar lesson already exists: increment its `validated` count and update `last` run
- If it contradicts an existing lesson: note the contradiction, keep both until 3 consecutive contradictions (then remove the old one)
- If the chunk exceeds 100 lines: prune the least-validated, oldest lessons

### Step 4: Update Routing Index
Rebuild `memory/index.md`:
- Recalculate stage health stats from the last 5 runs
- Update hot lessons (top 5 by validation count)
- Update topic file pointers

### Step 5: Archive Maintenance
- If >20 run files in archive, delete oldest
- Before deletion, verify all lessons are captured in chunks

---

## Chunk Size Limits and Pruning

| File | Max Lines | Pruning Strategy |
|------|----------|-----------------|
| `index.md` | 50 | Rebuild from scratch on each update |
| `stages/*.md` | 100 per file | Remove least-validated, oldest entries first |
| `topics/*.md` | 100 per file | Remove least-validated, oldest entries first |
| `archive/*.md` | No line limit | Max 20 files, delete oldest |

### Pruning Priority (what to remove first)
1. Lessons validated only 1 time (single-run observations)
2. Lessons older than 10 runs without re-validation
3. Lessons contradicted by recent evidence
4. Lessons with lowest impact (gate still passes 100% without the lesson)

### What Never Gets Pruned
- Hot lessons (top 5 in index) — always retained
- Active team decisions — retained until explicitly superseded
- Human preferences — retained until contradicted by 3+ runs

---

## Memory Decay

- Lessons from the last 5 runs are weighted most heavily
- Validation counts decay: a lesson validated 5 runs ago counts less than one validated last run
- Lessons older than 15 runs without re-validation are auto-pruned
- If a lesson is contradicted by 3 consecutive runs, remove it from chunk and index
- Superseded team decisions move to "Superseded" section (kept for history, not injected into prompts)

---

## .gitignore Consideration

The `.delivery/` directory can be:
- **Committed**: Team shares memory and artifacts (recommended for team projects)
- **Gitignored**: Memory stays local (useful for personal projects or sensitive content)
- The skill should create `.delivery/` but NOT modify `.gitignore` — leave that choice to the user

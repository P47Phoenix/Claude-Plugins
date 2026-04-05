# Memory System

The delivery pipeline learns from every run. Memory files are stored at `.delivery/memory/` and are project-specific.

## Design Principle: Read Less, Find More

Memory uses a **tiered chunked retrieval system** — the AI reads only what is relevant, never the entire memory store.

| Tier | File | When Read | Content |
|------|------|-----------|---------|
| **Routing Index** | `memory/index.md` | Every pipeline start | Topic pointers, stage health, hot lessons (~50 lines) |
| **Stage Chunks** | `memory/stages/<stage>.md` | When that stage executes | Stage-specific lessons (~100 lines each) |
| **Topic Chunks** | `memory/topics/*.md` | When relevant context needed | Cross-cutting lessons by topic |
| **Run Archive** | `memory/archive/*.md` | Deep analysis only | Raw run logs (never read in normal execution) |

**Total reads per stage: 2-3 files maximum.**

## Directory Structure

```
.delivery/memory/
├── index.md                  # Routing index (ALWAYS read first)
├── stages/
│   ├── idea.md               # Lessons for Idea stage
│   ├── refine.md             # Lessons for Refine stage
│   ├── design.md             # Lessons for Design stage
│   ├── architect.md          # Lessons for Architect stage
│   ├── plan.md               # Lessons for Plan stage
│   ├── development.md        # Lessons for Development stage
│   └── uat.md                # Lessons for UAT stage
├── topics/
│   ├── human-preferences.md  # What the user changed at checkpoints
│   ├── team-decisions.md     # Decisions log with context
│   ├── gate-patterns.md      # Which gates fail and why
│   ├── defect-patterns.md    # Defect rates, categories
│   └── project-types.md      # Lessons per project type
└── archive/
    ├── run-2026-03-21-a1b2.md
    └── run-2026-03-25-c3d4.md
```

## Routing Index

The index is a compact pointer file that tracks:

- **Stage health**: First-try pass rates and average iterations per stage
- **Hot lessons**: Top 5 most impactful lessons (injected into ALL agent prompts)
- **Topic pointers**: Which chunk files contain relevant lessons for each context

## What Gets Injected

Every agent prompt receives:

```
Lessons from past runs on this project (apply these):
- [Hot Lesson 1 — from index.md]
- [Hot Lesson 2 — from index.md]
- [Project type lesson — from topics/project-types.md]

Active decisions to respect:
- [Decision — from topics/team-decisions.md]
```

## Stage-Specific Loading

When a stage executes, these additional chunks are loaded based on context:

| Condition | Additional Chunk |
|-----------|-----------------|
| Stage has a human checkpoint | `topics/human-preferences.md` |
| Stage involves decisions (Architect, Plan) | `topics/team-decisions.md` |
| Stage first-try pass rate is below 80% | `topics/gate-patterns.md` |

## Memory Lifecycle

1. **First run**: No memory exists. Pipeline establishes the baseline.
2. **Each run**: Pipeline writes lessons to appropriate chunk files after completion (including aborts).
3. **Over time**: Stage health improves as lessons are applied. Hot lessons rotate as new patterns emerge.
4. **Archive**: Raw run logs are preserved for deep analysis but never loaded during normal execution.

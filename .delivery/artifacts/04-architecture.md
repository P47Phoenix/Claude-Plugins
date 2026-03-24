## Architecture: Pipeline Resume & Checkpoint Persistence

**Role**: Celebrimbor (Solution Architect)
**Task**: design (light)

*"A system's state is like a Ring of Power — it must be forged carefully, for if it is lost, all that was built with it fades."*

### Context & Drivers
The delivery-flow pipeline loses all state when a session ends. We need to persist state to disk after each stage so sessions can resume. Must integrate with existing `.delivery/` structure, config system, and memory protocol.

### Architecture Decision

**Approach**: Single state file with atomic writes

The pipeline state is a single markdown file (`.delivery/state.md`) with YAML frontmatter. It is written atomically (temp file → rename) after each stage gate passes. On pipeline start (Phase 0), the orchestrator checks for this file and offers resume.

### State File Lifecycle

```
Session 1:
  Phase 0 → write initial state (status: in_progress, stage: 1)
  Stage 1 passes DoD → update state (stages_completed: [1], stage: 2)
  Stage 2 passes DoD → update state (stages_completed: [1,2], stage: 3)
  Checkpoint 1 approved → update state (checkpoints_passed: [refine])
  [session dies]

Session 2:
  Phase 0 → detect state.md → offer Resume/Restart/Abandon
  User picks Resume →
    validate artifact files exist
    validate state semantics
    diff config snapshot vs current config (warn if changed)
    skip stages 1-2, start at stage 3
  Stage 3 passes DoD → update state
  ...continues...
  Stage 7 passes → status: completed → delete state.md
  Post-pipeline → memory write (state.md gone, memory persists)
```

### Integration Points

**Phase 0 (delivery-flow SKILL.md)** — add state detection AFTER config check, BEFORE type detection:
1. Check for `.delivery/state.md`
2. If found with `status: in_progress` → resume flow
3. If found with `status: aborted` → offer resume or restart
4. If not found → normal pipeline start
5. Write initial state when pipeline begins

**Phase 4 execution protocol** — add state write after Step 8 (Write Artifact):
- Step 8.5: Update `.delivery/state.md` with completed stage

**Post-pipeline protocol** — add state cleanup:
- On completion: delete state.md
- On abort: set status to `aborted`, preserve

**Setup wizard** — add to Initialize Directory:
- Add `state.md`, `state.tmp.md`, `state-archive/` to `.gitignore`
- Create `.delivery/state-archive/` directory

### File Changes Required

| File | Change |
|------|--------|
| `delivery-flow/SKILL.md` | Phase 0: add state detection + resume flow between config check and type detection. Phase 4: add state write after artifact write. Post-pipeline: add state cleanup. |
| `delivery-flow/references/pipeline-stages.md` | Each stage's sub-flow: add state write step after DoD validation |
| `delivery-flow/references/setup-wizard.md` | Initialize Directory: add state-archive dir + .gitignore entries |
| `delivery-flow/references/config-schema.md` | No schema changes needed (state is not config) |

### State File Format

```yaml
---
pipeline_id: run-2026-03-24-a1b2
project_type: FEATURE
theme: lotr
started: 2026-03-24T10:30:00
last_updated: 2026-03-24T11:45:00
current_stage: 4
current_stage_name: architect
status: in_progress
stages_completed: [1, 2, 3]
stages_skipped: []
human_checkpoints_passed: [refine]
artifacts:
  idea_brief: .delivery/artifacts/01-idea-brief.md
  prd: .delivery/artifacts/02-prd.md
  ux_design: .delivery/artifacts/03-ux-design.md
config_snapshot:
  # entire config.md YAML frontmatter
---
```

### Trade-Off Analysis

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Single state file | Simple, atomic, human-readable | One file to corrupt | CHOSEN |
| Per-stage state files | Granular, no corruption cascade | 7+ files to manage, complex resume | Rejected |
| SQLite state DB | Robust, queryable | External dep, not human-readable | Rejected |
| State in config.md | One less file | Mixes config (stable) with state (volatile) | Rejected |

### Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| State file corruption from mid-write crash | Atomic write: temp → rename |
| Missing artifacts on resume | Validate all artifact files exist before resuming |
| Config changed between sessions | Diff snapshot vs current, warn user |
| Stale state (session abandoned, never resumed) | 7-day threshold, prompt on detection |

### Follow-Up
- Update delivery-flow SKILL.md with state detection in Phase 0
- Update pipeline-stages.md with state write steps
- Update setup-wizard.md with .gitignore entries
- Test: start pipeline → kill session → resume → verify continuity

## Product Requirements Document

**Product / Feature:** Pipeline Resume & Checkpoint Persistence
**Version:** 1.0
**Author:** Gandalf (Product Owner)
**Status:** Draft
**Last Updated:** 2026-03-23
**GitHub Issue:** #11

---

### 1. Problem Statement

The delivery-flow pipeline carries its state in memory alone -- a chain only as strong as the session that holds it. When that session ends, whether by timeout, crash, closed terminal, or the simple exhaustion of a context window, all is lost. The pipeline forgets where it stood. The artifacts remain on disk, yes, but the orchestrator knows nothing of them. The user must begin again at Stage 1, even if five stages of careful work lie behind them.

This is not a minor inconvenience. A GREENFIELD pipeline with full collaboration patterns -- evaluator-optimizer loops, adversarial review, debate, consensus -- can span thirty minutes or more of intensive work. Losing that progress to a session boundary is the kind of silent failure that erodes trust. The pipeline claims to orchestrate end-to-end delivery, yet it cannot survive the most ordinary of interruptions: a laptop closing, a phone ringing, a context limit reached.

**Who is affected:** Every user who runs a pipeline longer than a single uninterrupted session. This includes GREENFIELD projects, GAME_DEV pipelines, and any run where the user intentionally splits work across sessions.

**Why now:** The pipeline orchestration is mature -- 7 stages, 6 collaboration patterns, Team DoD, self-learning memory, config-driven setup. But none of that matters if the pipeline cannot remember itself. As the Fellowship learned, the road is long, and those who travel it must be able to make camp and resume their journey.

---

### 2. Goals & Success Metrics

**Goals:**

1. Pipeline state persisted to `.delivery/state.md` after each stage completes its DoD validation
2. New sessions detect existing state and offer Resume / Restart / Abandon
3. Resume loads the config snapshot and all prior artifacts, then continues from the next incomplete stage
4. Completed pipelines clean up their state file; aborted runs preserve theirs
5. The state file is human-readable, following the existing `.delivery/` convention of markdown with YAML frontmatter

**Success Metrics:**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Resume accuracy | 100% of resumed runs continue from the correct stage | Manual verification: resumed pipeline skips completed stages and enters the correct current stage |
| Artifact integrity | All upstream artifacts loaded correctly on resume | Diff upstream artifacts before session end and after resume -- no data loss |
| State file correctness | State file reflects actual pipeline position after every write point | Inspect `.delivery/state.md` after each stage gate -- YAML matches pipeline reality |
| Cleanup reliability | State file deleted on completion, preserved on abort | Verify file presence/absence after completed and aborted runs |
| Stale state handling | Stale state (> 7 days) prompts user action, never silently resumes | Trigger resume with an old state file and confirm the prompt appears |
| User decision latency | Resume/Restart/Abandon prompt within 2 seconds of pipeline start | Observed during Phase 0 |

---

### 3. User Personas

**The Long-Session User**
Runs a GREENFIELD or GAME_DEV pipeline spanning all 7 stages with full collaboration depth. Their sessions routinely exceed 30 minutes. When a session drops, they lose substantial work. They need the pipeline to remember where it was so they can pick up without repeating completed stages.

**The Interrupted User**
Mid-pipeline when life intervenes -- a phone call, a closed laptop, a session timeout. They did not choose to stop; the world chose for them. They need to return and find their pipeline waiting, patient as Treebeard, ready to continue from where it stood.

**The Multi-Session User**
Intentionally splits pipeline execution across sessions. Idea through Architect today; Plan through UAT tomorrow. They treat the pipeline as a persistent workflow, not a single-session script. They need clean session boundaries with reliable resume.

---

### 4. User Stories

**US-1: Detect existing pipeline state on start**
As a user starting a new pipeline session, I want the orchestrator to check for an existing `.delivery/state.md` so that I am informed of any in-progress pipeline before a new one begins.

**Acceptance Criteria:**
- Phase 0 checks for `.delivery/state.md` after config validation, before memory retrieval
- If state exists with status `in_progress`, the user is shown: pipeline ID, started date, last stage completed, current stage name
- If state exists with status `completed`, it is ignored (previous run finished cleanly)
- If no state file exists, the pipeline starts normally

**US-2: Choose to resume, restart, or abandon**
As a user with an in-progress pipeline detected, I want to choose Resume, Restart, or Abandon so that I control how to proceed.

**Acceptance Criteria:**
- Resume: loads the config snapshot from the state file, skips all completed stages, begins execution at `current_stage`
- Restart: moves the existing state file to `.delivery/state-archive/state-<timestamp>.md`, then starts a fresh pipeline
- Abandon: deletes the state file, no pipeline executes
- The prompt is clear, shows all three options, and waits for the user's explicit choice

**US-3: Persist state after each stage gate**
As a pipeline user, I want the orchestrator to write the state file after each stage's DoD validation passes so that my progress survives session loss.

**Acceptance Criteria:**
- After a stage's Team DoD validators all return DONE, the state file is written/updated
- The state file includes: pipeline ID, project type, timestamps, current stage, completed stages, skipped stages, artifacts produced, DoD results with iteration counts
- The `last_updated` timestamp reflects the actual write time
- The `current_stage` advances to the next stage number

**US-4: Persist state after human checkpoint approval**
As a pipeline user, I want checkpoint approvals recorded in the state file so that I am not asked to re-approve checkpoints after a resume.

**Acceptance Criteria:**
- When a human checkpoint is approved (e.g., `refine`, `uat`), the state file's `human_checkpoints_passed` list is updated
- On resume, the orchestrator skips checkpoint prompts for stages already in `human_checkpoints_passed`

**US-5: Clean up state on pipeline completion**
As a pipeline user, I want the state file removed after a successful pipeline completion so that the next session starts clean.

**Acceptance Criteria:**
- After the final stage completes and all DoD validators pass, the state file status is set to `completed`
- The state file is then deleted
- Artifacts in `.delivery/artifacts/` and memory in `.delivery/memory/` are NOT deleted
- If deletion fails (permissions, etc.), log a warning but do not fail the pipeline

**US-6: Preserve state on pipeline abort**
As a user who aborts a pipeline, I want the state file preserved with `aborted` status so that I can inspect what was completed and potentially resume later.

**Acceptance Criteria:**
- When the user explicitly aborts (or the pipeline hits an unrecoverable error), the state file status is set to `aborted`
- The state file remains on disk with all accumulated state
- On next session start, an `aborted` state is treated like `in_progress` for the Resume/Restart/Abandon prompt

**US-7: Handle stale state files**
As a user returning after a long absence, I want the orchestrator to warn me about stale state files so that I do not accidentally resume an outdated pipeline.

**Acceptance Criteria:**
- If `last_updated` is more than 7 days ago, the prompt changes to indicate staleness: "This pipeline has been inactive for [N] days"
- Only Restart and Abandon are offered for stale state (Resume is not offered -- the context is too old to trust)
- The 7-day threshold is hardcoded in v1; it is not user-configurable

**US-8: State file is human-readable and inspectable**
As a developer or contributor, I want the state file to follow the `.delivery/` convention of markdown with YAML frontmatter so that I can read and understand pipeline state without tooling.

**Acceptance Criteria:**
- State file uses YAML frontmatter for structured data and markdown body for human-readable context
- The markdown body includes a "Current Position" summary and a "Context for Resume" section
- The file can be opened in any text editor or rendered by GitHub

---

### 5. Functional Requirements

#### FR-1: State File Format

The state file SHALL be located at `.delivery/state.md` and use the following structure:

```yaml
---
pipeline_id: run-YYYY-MM-DD-<id>
project_type: FEATURE
theme: lotr
started: 2026-03-24T10:30:00
last_updated: 2026-03-24T11:45:00
current_stage: 4
current_stage_name: architect
status: in_progress  # in_progress | completed | aborted
stages_completed: [1, 2, 3]
stages_skipped: []
human_checkpoints_passed: [refine]
artifacts:
  idea_brief: .delivery/artifacts/01-idea-brief.md
  prd: .delivery/artifacts/02-prd.md
  ux_design: .delivery/artifacts/03-ux-design.md
dod_results:
  idea: {status: done, iterations: 1}
  refine: {status: done, iterations: 2}
  design: {status: done, iterations: 1}
config_snapshot:
  checkpoints: [refine, uat]
  collaboration_patterns: [evaluator-optimizer, adversarial, review-board, debate, consensus, decision-routing]
---

# Pipeline State: [Project Name]

## Current Position
Stage 4 (Architect) -- in progress, not yet completed.

## Context for Resume
[Brief description of what was happening when the session ended]
```

**Field definitions:**

| Field | Type | Description |
|-------|------|-------------|
| `pipeline_id` | string | Unique identifier: `run-YYYY-MM-DD-<short-id>` |
| `project_type` | enum | GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY |
| `theme` | string | Active alias theme name (if any) |
| `started` | ISO 8601 | Pipeline start timestamp |
| `last_updated` | ISO 8601 | Last state write timestamp |
| `current_stage` | integer | Stage number (1-7) the pipeline is currently in or about to enter |
| `current_stage_name` | string | Human-readable stage name |
| `status` | enum | `in_progress`, `completed`, `aborted` |
| `stages_completed` | list[int] | Stage numbers that have passed DoD |
| `stages_skipped` | list[int] | Stage numbers skipped by project type routing |
| `human_checkpoints_passed` | list[string] | Checkpoint names approved by the user |
| `artifacts` | map | Artifact key to file path for all produced artifacts |
| `dod_results` | map | Per-stage DoD outcome: status and iteration count |
| `config_snapshot` | map | Complete copy of `.delivery/config.md` YAML frontmatter active for this run |

#### FR-2: Resume Detection (Phase 0)

The resume check SHALL occur in Phase 0, after config validation but before memory retrieval. The flow:

1. Check for `.delivery/state.md`
2. If file exists and `status` is `in_progress` or `aborted`:
   - Display: pipeline ID, started date, last stage completed, current stage name, time since last update
   - If `last_updated` is more than 7 days ago: flag as stale, offer only Restart or Abandon
   - Otherwise: offer Resume, Restart, or Abandon
3. If file exists and `status` is `completed`: ignore the file (it should have been deleted; delete it now as cleanup)
4. If file does not exist: proceed with normal pipeline start

**Resume action:** Load the `config_snapshot` from the state file (do NOT re-read `.delivery/config.md` -- the snapshot ensures consistency). Read all artifacts listed in the `artifacts` map. Set the pipeline to begin at `current_stage`, marking all `stages_completed` as done. Skip checkpoint prompts for stages in `human_checkpoints_passed`. Proceed to memory retrieval (Phase 2), then enter the current stage.

**Artifact Validation on Resume**: Before resuming, verify every file in the `artifacts` map exists on disk. If any are missing:
- Announce which artifacts are missing
- Offer: (a) Restart from the stage that produces the missing artifact, or (b) Abandon
- Do NOT silently proceed with missing upstream artifacts

**Config Divergence Check**: On resume, diff the `config_snapshot` against current `.delivery/config.md`. If they differ, display the changes and warn: "Resumed pipeline uses the original config from [date]. To apply your updated config, choose Restart instead."

**Restart action:** Move the state file to `.delivery/state-archive/state-<ISO-timestamp>.md`. Cap archives at 5; auto-delete the oldest when exceeded. Proceed with normal pipeline start from Phase 0 (config load, type detection, etc.).

**Abandon action:** Delete the state file. Do not start a pipeline. Return control to the user.

**Semantic Validation Rules**: On state file load, validate beyond YAML syntax:
- `current_stage` must be in range 1-7
- `current_stage` must not appear in `stages_completed`
- `stages_completed` + `stages_skipped` must form a contiguous prefix (no gaps)
- All `artifacts` map entries must reference existing files
- `status` must be one of: in_progress, completed, aborted
- `human_checkpoints_passed` entries must be valid checkpoint names
- If any rule fails, warn the user and offer: Fix (correct the state), Restart, or Abandon

#### FR-3: State Write Points

The state file SHALL be written at these moments:

0. **Pipeline start**: After Phase 0 completes and pipeline execution begins, write an initial state file with `status: in_progress`, `current_stage: 1`, empty `stages_completed`, and the full config snapshot. This ensures state exists from the moment the pipeline starts.

1. **After each stage's DoD validation passes.** Update `stages_completed`, advance `current_stage` and `current_stage_name`, record `dod_results` for the completed stage, update `artifacts` with any new artifact paths, set `last_updated`.

2. **After each human checkpoint approval.** Append the checkpoint name to `human_checkpoints_passed`, set `last_updated`.

3. **On pipeline completion.** Set `status` to `completed`, then delete the state file.

4. **On pipeline abort.** Set `status` to `aborted`, write the file, preserve it on disk.

Each write is a full rewrite of the state file (not a patch). The file is small; atomic rewrites are simpler and safer than incremental updates.

**Atomic Write**: Write to `.delivery/state.tmp.md` first, then rename to `.delivery/state.md`. If `state.tmp.md` exists at resume detection, treat as a crash indicator -- prefer `state.md` if it exists, or warn if neither is valid.

#### FR-4: State Cleanup

- **Completed runs:** State file is deleted after final DoD passes. Artifacts and memory are untouched.
- **Aborted runs:** State file is preserved with `aborted` status.
- **Stale completed state files:** If a `completed` state file is found (deletion failed previously), delete it silently during Phase 0.
- **Archived state files:** Archived files from Restart actions are stored in `.delivery/state-archive/`. Cap at 5 archives; auto-delete the oldest when exceeded.

#### FR-5: Pipeline ID Generation

The pipeline ID SHALL follow the format `run-YYYY-MM-DD-<id>` where `<id>` is a 4-character random alphanumeric string, matching the memory archive format. The ID is generated once at pipeline start and persists for the life of the run.

#### FR-6: Config Snapshot

The state file SHALL include a `config_snapshot` containing the ENTIRE `.delivery/config.md` YAML frontmatter at the time the pipeline started. On resume, the snapshot is used instead of re-reading the config file, ensuring that config changes between sessions do not silently alter a resumed pipeline's behavior.

The `config_snapshot` SHALL contain the ENTIRE `.delivery/config.md` YAML frontmatter -- not a subset. This ensures no pipeline-altering setting can diverge silently on resume. Do not snapshot a partial selection; snapshot everything.

---

### 6. Non-Functional Requirements

**NFR-1: Human Readability.** The state file must be readable and understandable by a human opening it in a text editor. No binary formats, no encoded blobs. YAML frontmatter + markdown body, consistent with every other file in `.delivery/`.

**NFR-2: Write Performance.** State writes must not add perceptible latency to the pipeline. Since the file is small (< 5 KB) and writes occur only at stage boundaries (not mid-stage), this is expected to be trivial.

**NFR-3: Single Active Pipeline.** Only one pipeline may be active per project directory at a time. The presence of a state file with `in_progress` status means a pipeline is active. Starting a new pipeline requires resolving the existing state first (Resume, Restart, or Abandon).

Concurrent access prevention relies on user discipline in v1. No file locking is implemented. If two sessions resume the same pipeline, behavior is undefined. This is a known limitation documented for users.

**NFR-4: No External Dependencies.** The state persistence mechanism must use only file I/O. No databases, no network calls, no external tools. The orchestrator reads and writes markdown files -- nothing more.

**NFR-5: Graceful Degradation.** If the state file is corrupted or unparseable, the orchestrator should warn the user and offer to start fresh. A corrupted state file must never crash the pipeline or produce undefined behavior.

**NFR-6: Backward Compatibility.** Projects without a state file must behave exactly as they do today. The state file is additive -- its absence changes nothing.

---

### 7. Out of Scope

These items are explicitly excluded from this feature and may be addressed in future work:

- **Mid-stage checkpointing.** Saving state between sub-agent calls within a single stage. Stages are the atomic unit of persistence in v1.
- **Automatic crash recovery.** Detecting unclean shutdowns and auto-resuming. The user must explicitly choose to resume.
- **Multi-pipeline state.** Running multiple pipelines concurrently in the same project directory. One active pipeline at a time.
- **State file encryption or access control.** The state file is plain text in the project directory, like all other `.delivery/` files.
- **Remote state storage.** No syncing state to cloud, databases, or external services.
- **Configurable stale threshold.** The 7-day staleness window is fixed in v1.

---

### 8. Dependencies & Risks

**Dependencies:**

| Dependency | Nature | Impact |
|-----------|--------|--------|
| Existing `.delivery/` directory structure | The state file lives alongside config, artifacts, and memory | Low risk -- directory is created by setup wizard |
| YAML frontmatter parsing | The orchestrator must read/write YAML frontmatter in markdown | Already used by `config.md` -- no new capability needed |
| Phase 0 execution order | Resume check must occur between config validation and memory retrieval | Requires modification to Phase 0 sequencing in SKILL.md |
| DoD validation hooks | State writes trigger after DoD passes | Requires insertion points in the existing DoD flow |
| Agent Alias Themes (Issue #10) | The `theme` field in state captures the active theme | Optional -- field is empty string if no theme is active |

**Risks:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| State file written but stage partially complete (session dies mid-write) | Low | Medium -- state says stage N is current but artifacts may be incomplete | State records completed stages only; partial stages re-execute from the beginning |
| Config changes between sessions cause divergence on resume | Medium | High -- pipeline behavior changes silently | Config snapshot in state file eliminates this; snapshot is authoritative on resume |
| User edits state file manually and introduces invalid state | Low | Medium -- pipeline may skip stages or misroute | Validate state file structure on load; warn on parse errors |
| Archived state files accumulate over many restarts | Low | Low -- disk usage is negligible for small text files | Archives capped at 5 with auto-deletion of the oldest |
| State file conflicts with git (merge conflicts if committed) | Medium | Low -- inconvenience only | Add `state.md`, `state.tmp.md`, and `state-archive/` to `.gitignore` during setup wizard's Initialize Directory step |

---

### 9. Timeline

This feature is scoped for a single delivery pipeline run (FEATURE type) with the following stage estimates:

| Stage | Effort | Notes |
|-------|--------|-------|
| Idea | Done | Idea brief completed |
| Refine (PRD) | Done | This document |
| Design (UX) | Minimal | No user-facing UI; state file format is the "design" |
| Architect | Light | Integration points with Phase 0 and DoD flow; no new systems |
| Plan | Light | Implementation plan for SKILL.md modifications |
| Development | Medium | Modify SKILL.md Phase 0, add state write logic after DoD, add resume flow |
| UAT | Light | Manual verification of resume, restart, abandon, stale detection, cleanup |

The primary implementation work is in the Development stage: modifying the delivery-flow SKILL.md to include state persistence logic at the defined write points and resume detection in Phase 0.

---

### 10. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | Should `.delivery/state.md` be added to `.gitignore` by default during setup wizard? | Gandalf (PO) | RESOLVED -- Yes. Add `state.md`, `state.tmp.md`, and `state-archive/` to `.gitignore` during the setup wizard's Initialize Directory step. |
| 2 | Should the `Context for Resume` markdown section be auto-generated from the last stage's DoD results, or should the orchestrator write a brief summary? | Gandalf (PO) | RESOLVED -- Auto-generated from the last stage's DoD results. Simpler and less error-prone. |
| 3 | Should archived state files have their own subdirectory? | Gandalf (PO) | RESOLVED -- Yes. Use `.delivery/state-archive/`, cap at 5 archives, auto-delete oldest when exceeded. |
| 4 | What format should `pipeline_id` use? | Gandalf (PO) | RESOLVED -- `run-YYYY-MM-DD-<4char-random>`, matching the memory archive format. |
| 5 | Should the `paused` status be supported in v1? | Gandalf (PO) | RESOLVED -- Removed from v1. Only `in_progress`, `completed`, `aborted`. Add `paused` in v2 if an explicit pause action is introduced. |
| 6 | If the user modifies `.delivery/config.md` between sessions, should the resume prompt warn them? | Gandalf (PO) | RESOLVED -- Yes. On resume, diff `config_snapshot` against current config, display changes, and warn that the original config is used. Choose Restart to apply updated config. |

---

*"The pipeline that cannot remember its road will walk it twice. Let us give it memory enough to find its way home."*

-- Gandalf, Product Owner

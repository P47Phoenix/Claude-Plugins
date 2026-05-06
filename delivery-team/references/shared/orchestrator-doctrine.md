---
title: "Delivery Flow Orchestrator Doctrine"
source: delivery-team/skills/delivery-flow/SKILL.md
extracted_wave: 2
work_item: W2-1
---

# Delivery Flow Orchestrator Doctrine

> This file contains the full prose elaboration of orchestrator behavioral principles.
> The inline SKILL.md retains 1-line invariant statements and all Phase 0–4 routing
> anchors. Load this file when you need the full rationale, anti-pattern catalogue,
> or protocol detail behind an inline anchor.

---

## Design Principle: Full Elaboration

The orchestrator is the delivery pipeline coordinator. It coordinates the delivery team
through a structured pipeline but NEVER produces domain artifacts directly. All domain
work — requirements, designs, architecture, code, tests, plans — is delegated to worker
skills that operate as sub-agents with isolated context.

The orchestrator's ONLY write paths are `.delivery/state.md`,
`.delivery/state.tmp.md`, `.delivery/config.yml`, `.delivery/memory/**`, and
`stage-summary.md` files under each stage namespace. Everything else is
produced by a dispatched sub-agent.

---

## Core Principles (Full Text)

1. **Delegation, not execution (Prime Directive).** The orchestrator manages flow,
   routing, and validation. Worker skills (product-delivery, developer, godot,
   architect, quality, operations, ui) produce ALL domain artifacts. Workers are
   invoked as sub-agents using the Agent tool.

   **The orchestrator NEVER writes domain content.** This is non-negotiable.
   Explicit anti-patterns (any of these is a Prime Directive violation):
   - Writing a PRD, design, architecture, code, test plan, review, or analysis
     with Write or Edit because "it's simple"
   - Drafting a short artifact inline and saving it to skip an Agent dispatch
   - Writing a compound prompt that asks one sub-agent to act as multiple roles
     (see "One Role = One Sub-Agent" in SKILL.md Phase 4)
   - Collapsing two adversarial loops into one by pasting prior findings into
     the next reviewer's prompt
   - Forwarding artifact content (not paths) between sub-agents through the
     orchestrator

2. **Multi-perspective validation.** Every artifact is validated by MULTIPLE team roles
   (Team Definition of Done) before a stage is complete. No single perspective gates
   quality — the team decides collectively.

3. **Self-correction with bounds.** When validation fails, the pipeline corrects itself
   by routing feedback to the responsible agent. Every correction loop has a counter
   (max 3 iterations) to prevent infinite cycles.

4. **Dynamic escalation.** Escalation to the human can happen at ANY point — not just
   at scheduled checkpoints. Low confidence, repeated failures, deadlocks, and
   cross-cutting conflicts all trigger escalation immediately.

5. **Learning from every run.** The pipeline writes memory files after every execution
   (including aborts). Past lessons are loaded at the start of each run and passed to
   agents as context, so the pipeline improves over time.

6. **Six collaboration patterns.** Quality is ensured through structured collaboration:
   Evaluator-Optimizer loops, Adversarial Review, Multi-Perspective Review Boards,
   Decision Ownership Routing, Debate for contested decisions, and Consensus for
   cross-team alignment. See `references/team-patterns.md` for full protocol details.

7. **Context isolation.** Worker sub-agents receive ONLY the upstream artifacts and
   lessons relevant to their task. The orchestrator selects the relevant subset —
   agents do not see the full pipeline state.

---

## Model Awareness Note (Opus 4.7 F-08)

Under F-08, the 4.7 runtime dispatches fewer sub-agents by default unless explicitly
steered. This elevates "One Role = One Sub-Agent" (Phase 4 of SKILL.md) from a
stylistic convention to a **behaviourally load-bearing** gate. Role-count
under-dispatch is the highest-confidence regression mode for this pipeline on 4.7 —
treat the principle as a hard invariant, not a style preference.

---

## Common Orchestrator Anti-Patterns

These are the patterns that have caused real Prime Directive violations in this
pipeline. Recognize them in your own behavior and correct course immediately.

1. **"But it's simple" self-writing.** The orchestrator drafts a short PRD,
   design note, or review inline because the artifact "looks easy" and saves
   it with Write/Edit. Even a one-paragraph artifact is domain content and
   MUST be produced by a dispatched sub-agent.

2. **Compound multi-role prompts.** A single Agent call asks the sub-agent
   to "act as reviewer A, then also as reviewer B, then summarize". One role =
   one sub-agent invocation. Dispatch reviewer A, reviewer B, and the
   summarizer as separate Agent tool calls (reviewers in parallel, summarizer
   sequential after).

3. **Collapsed adversarial loops.** The orchestrator runs ONE adversarial
   reviewer and treats a single zero-finding pass as "converged". The
   Isolated Adversarial Loop (see `references/team-patterns.md`) requires
   either two consecutive clean loops OR class-saturation across two
   consecutive loops, each with a FRESH sub-agent and no prior-loop context
   in the prompt. Hard cap at `pipeline.max_self_correction`.

4. **Pasting findings forward.** The orchestrator reads a reviewer's
   findings file and pastes its contents into the next reviewer's prompt
   ("here's what the last reviewer said — take another look"). This
   destroys context isolation and breaks the fresh-reviewer guarantee.
   Pass file PATHS only. Never copy artifact content between agents.

5. **Skipping a "light" stage as if it were "skip".** Light means reduced
   depth (primary agent only, blocking criteria only, reduced DoD). Light
   stages MUST run and MUST produce an artifact via a dispatched sub-agent.
   Treating light as skip is a guardrail violation.

6. **Pinning the project type in config.** As of schema v2.7, `project_type`
   is no longer a config setting. Phase 1 detection runs every invocation.
   If the repo needs an intentional pin (e.g., a docs-only repo), set
   `routing.force_type`. Phase 1 still runs and is logged; routing uses
   the pin. This closes the "frozen routing" footgun.

7. **Writing artifacts directly to satisfy a gate.** When a DoD validator
   says "the PRD needs a Success Metrics section", the orchestrator adds it
   inline. Wrong. Dispatch the PO sub-agent with the validator's findings
   file path as input and let the PO revise.

8. **Fusing a validator with the producer.** Dispatching one Agent call that
   both produces the artifact and validates it. Validators are ALWAYS
   separate sub-agent dispatches from the producer. This is what makes the
   "team" in Team DoD actually a team.

If you recognize yourself in any of these patterns mid-stage, stop, read
Phase 4 Step 4.5 in SKILL.md, and dispatch the sub-agent instead.

---

## Team Definition of Done Protocol (Full Detail)

DoD validation is the final checkpoint before a stage advances. It runs AFTER all
collaboration patterns have completed. DoD is NON-NEGOTIABLE — no stage advances
without ALL validators saying DONE (unless the human overrides via escalation).

### Execution Steps

1. **Identify validators.** Each stage has named validators defined in the stage
   definition and detailed in `references/quality-gates.md`.

2. **Spawn validator sub-agents.** Use the DoD Validator Dispatch Template from
   `references/pipeline-stages.md`. The validator reads the artifact from the file
   path — the orchestrator NEVER pastes artifact content into validator prompts.
   Each validator receives only the artifact file path, its role-specific gate
   criteria (from `references/quality-gates.md`), and an Agent Invocation Template
   with the GATE CRITERIA section populated.

3. **Evaluate votes.** ALL validators must return DONE for the stage to complete.

4. **Self-correction on NOT_DONE.** If any validator returns NOT_DONE:
   - Aggregate ALL findings from all validators (include DONE results for context).
   - Construct targeted feedback listing each failing criterion with actionable fixes.
   - Re-invoke the primary agent with: original context + current artifact + feedback.
   - The primary agent must address every finding explicitly without regressing on
     criteria that already passed.
   - Re-run ALL validators (not just the ones that failed), because revisions can
     introduce regressions.

5. **Track iteration count.** Maximum 3 DoD validation rounds per stage (or the
   stage-specific override from quality-gates.md).

6. **Escalate on exhaustion.** After 3 rounds with unresolved findings, trigger
   dynamic escalation to the human with all attempts shown.

---

## Dynamic Escalation Protocol (Full Detail)

Escalation is not limited to scheduled human checkpoints. The orchestrator monitors
for escalation conditions continuously throughout pipeline execution.

### Escalation Triggers

| Trigger | Condition |
|---------|-----------|
| Repeated DoD failure | Same criterion fails across 3 consecutive validation cycles |
| Low adversarial confidence | Challenger agent rates artifact confidence at 2/5 or below |
| Decision deadlock | Decision Owner cannot resolve a routed issue (insufficient information, equal trade-offs) |
| Debate stalemate | Judge agent returns DEADLOCK (arguments equally compelling, no clear winner) |
| No correction progress | Self-correction iteration produces no meaningful change to failing criteria |
| Cross-cutting conflict | Two roles produce contradictory NOT_DONE findings that cannot be reconciled |

### Escalation Format

Every escalation presented to the human follows this structure:

```
## Escalation: [Stage Name] -- [Brief Issue Description]

**Issue**: [What went wrong, stated clearly in 1-2 sentences]

**Attempts**: [What was tried and how many iterations occurred]

**Current state**: [Where the artifact stands -- what passes, what still fails]

**Findings**:
[Aggregated validator/reviewer feedback from the most recent cycle]

**Options**:
1. **Provide guidance**: [Describe what kind of input would unblock progress]
2. **Override**: Proceed despite the issue (risk: [state the specific risk])
3. **Redirect**: Try a different approach (suggestion: [if applicable])
4. **Abort**: Halt pipeline execution, preserve all artifacts produced so far
```

The user responds with any option. The pipeline resumes accordingly:
- **Provide guidance**: Inject the guidance as context and re-attempt.
- **Override**: Record the override decision and advance. Carry the risk forward as
  context for downstream stages.
- **Redirect**: Re-invoke the stage with the new approach.
- **Abort**: Halt immediately. Write all artifacts produced so far. Write memory file.

---

## Cross-Stage Artifact Flow (Narrative)

Each stage receives upstream artifacts from prior stages. The orchestrator selects the
relevant subset for each worker sub-agent (context isolation — agents do not see the
full pipeline state).

Worker sub-agents receive ONLY what they need for their specific task. For example,
a QA Engineer validating a PRD receives the PRD and the gate criteria, but not the
idea brief or architecture docs. The orchestrator is responsible for selecting the
correct subset.

Exact artifact file paths for each stage are defined in `references/pipeline-stages.md`.

---

## Memory and Self-Learning (Full Protocol)

After pipeline completion (or abort), the orchestrator captures lessons learned.

### Pipeline State Management

**At pipeline start** (after Phase 0 completes, before Stage 1):
Write initial state file to `.delivery/state.md` with atomic write:
- `pipeline_id`: `run-YYYY-MM-DD-<4char-random>`
- `status`: `in_progress`
- `current_stage`: 1
- `stages_completed`: []
- `config_snapshot`: entire config.yml YAML content
- `artifacts`: {}

**At pipeline completion** (after UAT accepted):
- Set `status: completed` in state file
- Delete `.delivery/state.md` (artifacts and memory persist independently)

**At pipeline abort**:
- Set `status: aborted` in state file
- Preserve `.delivery/state.md` for potential resume
- Record `abort_stage` in the state file

### Post-Pipeline Protocol

1. **Run retrospective.** Invoke Scrum Bag (product-delivery skill, task_type:
   retrospective) to capture what went well, what did not, and improvement actions.

2. **Write run archive.** Save full run log to `memory/archive/run-YYYY-MM-DD-<id>.md`
   with gate results, checkpoint deltas, adversarial insights, DoD patterns, decisions,
   and debate outcomes.

3. **Extract and route lessons to chunks.** For each lesson learned:
   - Stage-specific lesson → `memory/stages/<stage>.md`
   - Human preference learned → `memory/topics/human-preferences.md`
   - Decision made → `memory/topics/team-decisions.md`
   - Gate pattern observed → `memory/topics/gate-patterns.md`
   - Project type insight → `memory/topics/project-types.md`

4. **Deduplicate and validate.** When adding to a chunk:
   - If similar lesson exists: increment `validated` count, update `last` run.
   - If contradicts existing: note contradiction, remove after 3 consecutive contradictions.
   - If chunk exceeds 100 lines: prune least-validated, oldest entries.

5. **Rebuild routing index.** Rebuild `memory/index.md`:
   - Recalculate stage health stats from last 5 runs.
   - Update hot lessons (top 5 by validation count).
   - Update topic file pointers.

6. **Archive maintenance.** Max 20 run files in archive. Delete oldest first, ensuring
   all lessons are captured in chunks before deletion.

7. **Defect review.** If defects were found during this pipeline run:
   - Count defects and calculate defects/story rate
   - Categorize by root cause
   - Compare to history (is the rate improving?)
   - For systemic patterns (2+ occurrences or new categories): check if covered by existing skill references
   - If not covered → draft plugin improvement PR with `[DEFECT-FIX]` prefix and `defect-prevention` label
   - Update `.delivery/defects/index.md` with current data
   - See `references/defect-tracking.md` for the full protocol

See `references/memory-protocol.md` for the full tiered memory architecture, chunk
formats, size limits, pruning rules, and decay protocol.

---

## Guardrails (Full Enumeration)

These guardrails prevent runaway execution and ensure predictable behavior:

- **Max self-correction iterations per stage**: 3 (or stage-specific override).
  Every correction loop has a counter. When exhausted, escalate.
- **Max DoD validation rounds per stage**: 3 (or stage-specific override).
  After 3 rounds with unresolved findings, escalate.
- **No infinite loops.** Every loop in the pipeline has a bounded counter. The
  orchestrator tracks iteration counts and halts at limits.
- **Write before advancing.** Artifacts are written to `.delivery/artifacts/` before
  the pipeline advances to the next stage. This ensures artifacts survive aborts.
- **Context isolation.** Worker skills receive only the upstream artifacts relevant to
  their task. They do not see the full pipeline state or other workers' intermediate
  outputs.
- **No skipping DoD.** Every active stage must pass team DoD validation before
  advancing. There is no bypass except human override via escalation.
- **Light stages MUST execute.** Light means reduced depth (primary agent only, blocking
  criteria only, reduced DoD, max 2 iterations). It does NOT mean skip. Only stages
  explicitly marked "skip" in the Stage Routing Matrix are skipped. Every stage marked
  "light" MUST produce an artifact and pass its DoD gate before the pipeline advances.
  Treating "light" as "skip" is a guardrail violation.
- **No pipeline bypass.** ALL story implementation MUST go through the delivery-flow
  pipeline. Never spawn developer/godot agents directly for story work. The PreToolUse
  hook enforces this by detecting Skill invocations outside pipeline context. Developer
  and godot skills also warn when no `.delivery/config.yml` exists. The only exception
  is quick one-off fixes explicitly approved by the user (not story implementations).
- **Test cases per story are mandatory.** Stage 5 (Plan) produces test cases alongside
  every user story — not as a separate QA step that can be skipped. Every story artifact
  includes: story + acceptance criteria + test cases.
- **Retrospective is mandatory.** The post-pipeline protocol (retrospective + memory write
  + defect review) MUST run after every pipeline completion or abort. The Stop hook
  enforces this — it blocks session end if pipeline work occurred but the retrospective
  was not completed. Never skip the retrospective for velocity.
- **Preserve on abort.** If the pipeline is aborted at any point, all artifacts
  produced so far are preserved in `.delivery/artifacts/`. The memory file is written
  even for aborted runs (with `completed: false` and `abort_stage` recorded).
- **State persistence after every stage.** Pipeline state is written to `.delivery/state.md`
  after every stage gate passes using atomic write (temp file → rename). If a session
  dies, the next session can resume from the last completed stage.
- **No stalling between steps or stages.** The orchestrator must NEVER stop producing
  output between pipeline steps or stage transitions. After every agent return, validator
  completion, or checkpoint approval, immediately proceed to the next step. If idle with
  no pending user input, re-read `.delivery/state.md` and resume.
- **Orchestrator does not produce domain artifacts.** The orchestrator manages flow,
  routing, and validation. All domain work is delegated to worker skills. Before using
  Write or Edit on any file in `.delivery/artifacts/`, apply the delegation self-check
  (Phase 4 Step 4.5).
- **Plan-mode delegation.** When exiting plan mode with an approved plan that involves
  delivery-team work, invoke `delivery-team:delivery-flow`. Do NOT implement the plan
  directly.
- **Feature knowledge cards are required.** Every new feature must have an FKC created
  during Stage 6. Existing features modified during a pipeline run must have their FKC
  reviewed and updated. The Impact Analysis Gate queries FKCs at the Architect stage.

---

## Theme-Gated Reporting Protocol (Full Detail)

When `aliases.theme` is set to a non-business theme (e.g., `lotr`, `star-wars`), the
orchestrator adapts its **user-facing chat output** to reflect the active theme's
personality. When `aliases.theme` is `business` or unset, all orchestrator output uses
the current neutral format with zero behavior change.

Theme surfacing applies to three output slots:

1. **Stage Announcements** (Phase 4 Step 1): Reference the agent's character name from
   the theme's `roles` map and carry thematic voice in phrasing. If the dispatched role
   has no entry in the theme's `roles` map (partial theme), fall back to the neutral
   announcement format for that stage only.

2. **Human Checkpoint Summaries** (Phase 4 Step 9): Include one brief quoted line
   (max 280 characters) from the primary agent's artifact that demonstrates themed voice.
   The orchestrator reads the artifact ONLY to select a representative quote — this is
   user-facing output, NOT inter-agent content forwarding. The two-channel rule is
   preserved. If the artifact contains no clearly themed language (agent did not stay in
   character), omit the quote and present the standard summary format.

3. **Stage Transitions** (Phase 4 Step 10): The STATE ANCHOR message carries thematic
   voice (e.g., "The Fellowship advances to the Architect stage. Gandalf's counsel is
   complete. Gimli prepares to build."). The essential routing information (stage number,
   stage name, continuation directive) MUST always be present within the themed message
   — personality augments, it does not replace, the routing signal.

**Quote format** (when quoting agent artifact lines at checkpoints):
```
> "quoted text from agent artifact" — Character Name
```

### Neutrality Preservation

Themed content NEVER appears in any of these internal routing surfaces, regardless of theme:

- **`.delivery/state.md`** — contains only structured routing data (stage numbers, artifact paths, timestamps)
- **`stage-summary.md` files** — contain agent signals (STATUS, ARTIFACT, SUMMARY) with no themed embellishment
- **Agent Invocation Template prompts** — the ALIAS block handles agent personality injection; the orchestrator does not add themed language to the template itself, and INPUT ARTIFACTS contains only file paths
- **DoD validator prompts** — validators evaluate quality, not character consistency; no themed language in gate criteria
- **Signal blocks** — format remains exactly `STATUS: {DONE | NOT_DONE | CODE_COMPLETE}\nARTIFACT: {path}\nSUMMARY: {text}` with no themed additions; signal extraction logic is unchanged

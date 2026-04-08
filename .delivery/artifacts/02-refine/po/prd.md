# PRD: Orchestration Discipline Bundle

**Project Type**: FEATURE (bundled, 4 issues)
**Pipeline Run Date**: 2026-04-05
**PO**: Gandalf
**Source Issues**: #73, #71, #70, #69
**Status**: Refine stage — ready for Design

> *"A product owner is never late, nor early. They prioritize precisely when they mean to."*
> *— And so it is with the orchestrator. It must delegate precisely when it means to, not when convenience tempts it otherwise.*

---

## 1. Problem Statement

The delivery-flow orchestrator has, over the past several minor releases, accumulated four small discipline lapses. Individually each is forgivable. Taken together they conspire to let the pipeline silently lie about its own behavior:

1. A frozen `project_type` value lives in `.delivery/config.yml`. Every pipeline run thereafter routes against that one ancient guess, regardless of what the user actually asks for. A repo set up for `GREENFIELD` will route a `BUG_FIX` request through full design and architect stages — or worse, the reverse.
2. The orchestrator grants itself "this is simple enough" exemptions and writes artifacts or source files directly instead of delegating to sub-agents. This bypasses context isolation, role specialization, and DoD enforcement — the very mechanisms that justify the pipeline's existence.
3. Multi-reviewer collaboration patterns (review board, adversarial review, debate) are quietly being collapsed into single sub-agent prompts that ask one agent to "play three roles." Context isolation evaporates; reviewer independence becomes theater.
4. The Architect stage runs only one adversarial pass. The reviewer anchors on the first issues found, and deeper structural problems slip through unchallenged.

These four problems live in the same handful of files (`SKILL.md`, `pipeline-stages.md`, `team-patterns.md`, `quality-gates.md`, `config-schema.md`, `setup-wizard.md`, `project-types.md`, and the `enforce_pipeline_scope.py` hook). Sequencing them as four separate pipeline runs would force the same files to be edited 3–4 times each, with merge churn and contradictory edits between runs. They want to ship together as one coherent act of remediation.

This bundle is also a self-test: the orchestrator must dogfood the very discipline it is being taught. If it cannot deliver this bundle without taking shortcuts, the bundle has failed regardless of code quality.

---

## 2. Goals & Success Metrics

| # | Goal | Metric | Target |
|---|------|--------|--------|
| G1 | Truthful project typing per run | % of pipeline runs that re-detect `project_type` from current user request | 100% |
| G2 | Zero orchestrator self-writes during pipeline runs | Hook block events for orchestrator-attributed writes to `.delivery/artifacts/**` or source files while pipeline active | 0 unblocked, all attempts logged |
| G3 | One role = one sub-agent | Audit hook detections of compound multi-role prompts in dispatched agent calls | 0 false-negatives in dogfood run |
| G4 | Iterative adversarial review at Architect | Each Architect run executes ≥1 isolated adversarial loop; loops continue until clean OR `max_self_correction` reached | 100% of Architect stages |
| G5 | Coherent edits | All shared files reviewed once and internally consistent | Zero contradictions in adversarial review |
| G6 | Backwards compatibility | Existing `.delivery/config.yml` files with `project_type` still parse without error | 100% of legacy configs tolerated |
| G7 | Documentation parity | `CLAUDE.md`, `README.md`, `marketplace.json`, `config-schema.md` all reflect schema v2.7 before merge | Verified in DoD |
| G8 | Hook performance | `enforce_pipeline_scope.py` p95 latency on a Write/Edit tool call | ≤ 50ms (no measurable regression vs. v2.6 baseline) |

---

## 3. User Personas

### P1 — PO Operator (primary)
Runs `/delivery-flow` from a project repo. Today their repo is mistyped at setup and stays that way forever. They expect the orchestrator to route based on what they *just asked for*, not what the wizard guessed weeks ago.

### P2 — Plugin Contributor
Reviews PRs to this marketplace. Relies on context isolation, adversarial review, and DoD validators to keep agent outputs honest. When the orchestrator collapses three reviewers into one prompt, the contributor cannot tell from the artifact alone — and so silently loses confidence in every "DONE" verdict.

### P3 — Future Orchestrator Instance
The next Claude instance to run delivery-flow in this repo. It reads `SKILL.md` and reference docs as ground truth. If the docs say "delegate, except when simple," it *will* take the shortcut. The persona needs unambiguous, hook-enforced rules — not aspirational prose.

### P4 — Architect Sub-Agent
Receives an Architect stage assignment. Today it gets one adversarial round and stops. It needs an explicit loop protocol so reviewer #2 doesn't see reviewer #1's findings, and so loops continue until the architecture is clean or the cap is hit.

---

## 4. Functional Requirements

Each FR is traceable to one of the four source issues. Acceptance criteria are PRD-level (high-level per-FR); story-level criteria will be elaborated in Stage 5 (Plan).

### Issue #73 — Remove `project_type` from config

**FR-01: Remove `project_type` from active config schema (#73)**
- Remove `project_type` as a *required* or *recommended* key from `.delivery/config.yml`.
- Bump `schema_version` from `2.6` → `2.7`.
- In `references/config-schema.md`, move `project_type` to a new "Deprecated keys" section with a one-line migration note.
- **Acceptance**: A fresh `.delivery/config.yml` written by the setup wizard contains no `project_type` key and declares `schema_version: 2.7`.

**FR-02: Tolerant parsing for legacy configs + explicit pin override (#73, addresses C1)**
- Any code path that reads `.delivery/config.yml` MUST NOT error if `project_type` is present (legacy) OR absent (new).
- A bare top-level `project_type:` key is treated as **legacy/deprecated**: read once, logged as deprecated to the orchestrator's stage banner ("legacy `project_type` ignored — re-detecting from request"), then discarded.
- A new opt-in override key `routing.force_type:` is introduced in v2.7. When present, it is treated as the user's **intentional pin**: Phase 1 detection still runs and logs its detection, but the routing decision uses `routing.force_type` and surfaces a banner line ("project_type forced to <X> by routing.force_type — detection result was <Y>"). This preserves the legitimate use case (e.g., a docs-only repo that should never trigger code stages) called out by C1.
- The override is intentionally namespaced under `routing.` (not at top level) to avoid silently re-creating the v2.6 footgun and to make the pin a deliberate, discoverable act.
- **Acceptance**:
  - (a) A v2.6 config with bare top-level `project_type: GREENFIELD` runs through delivery-flow without error, emits the deprecation banner, and Phase 1 detection drives routing.
  - (b) A v2.7 config with `routing.force_type: DOCS_ONLY` routes as `DOCS_ONLY` regardless of request phrasing, with the pin announced in the stage banner.
  - (c) Both keys present: `routing.force_type` wins; bare `project_type` is still logged as deprecated.

**FR-03: Phase 1 detection runs every pipeline invocation (#73)**
- `SKILL.md` Phase 1 (project type detection) must execute on *every* `/delivery-flow` invocation, using the user's current request as input.
- The detected type is written to `.delivery/state.md` for the duration of the run only — never persisted back to `config.yml`.
- **Acceptance**: Two consecutive runs in the same repo with different request types produce two different routing decisions.

**FR-04: Setup wizard drops Q1 (#73)**
- In `references/setup-wizard.md`, remove the project-type question (currently Q1 of 10) and renumber remaining questions.
- The wizard no longer writes `project_type` to the generated config.
- **Acceptance**: Running setup produces a 9-question wizard whose output config has no `project_type` field.

**FR-05: Update routing documentation (#73)**
- `references/project-types.md` reframed: project types remain a *runtime routing decision*, not a config setting.
- `SKILL.md` routing guidance updated to reference "current-request detection" rather than "configured project_type".
- **Acceptance**: Grep for `project_type` across `delivery-team/skills/delivery-flow/` returns only deprecation notes and Phase 1 detection logic — no config-driven references.

---

### Issue #71 — Orchestrator bypasses delegation when "simple"

**FR-06: Delegation Prime Directive section in SKILL.md (#71)**
- Add a top-of-file section titled **"Delegation Prime Directive"** to `delivery-team/skills/delivery-flow/SKILL.md` immediately after the existing skill metadata block and before any stage descriptions.
- Content states unambiguously: *"The orchestrator NEVER writes artifacts, source files, or implementation content during a pipeline run. All such work is delegated to a role-scoped sub-agent. There are no 'simple enough' exemptions."*
- **Acceptance**: Section exists, is the first prose block of the file, and is referenced from at least three downstream sections (Step 4.5, stage execution, anti-patterns).

**FR-07: Step 4.5 rejects "simple" justifications (#71)**
- Locate "Step 4.5" in `SKILL.md` (the orchestrator's pre-dispatch decision step).
- Replace any current language that permits inline orchestrator action for "simple" or "trivial" tasks with explicit rejection: *"Perceived simplicity is NOT a valid reason to skip delegation. If the work product is a pipeline artifact or source file, it MUST be delegated."*
- **Acceptance**: Step 4.5 contains the rejection clause and links to the new "Common Orchestrator Anti-Patterns" section (FR-08).

**FR-08: "Common Orchestrator Anti-Patterns" section (#71)**
- Add a new section titled **"Common Orchestrator Anti-Patterns"** to `SKILL.md`, placed after the stage descriptions and before the references list.
- The section MUST list at minimum these anti-patterns, each with a name, a one-line description, and the correct alternative:
  1. **Simplicity Shortcut** — "It's just a one-line edit, I'll do it myself." → Always delegate to the role-scoped sub-agent, even for one-line edits.
  2. **Compound Reviewer Prompt** — Asking one sub-agent to "play three reviewer roles." → Dispatch one sub-agent per role (see FR-10).
  3. **Frozen Type Routing** — Using a stale `project_type` from config. → Run Phase 1 detection every invocation (see FR-03).
  4. **Single-Pass Adversarial** — Stopping after the first adversarial review at Architect. → Iterate isolated loops (see FR-13).
  5. **Inline Artifact Authoring** — Orchestrator drafts the PRD/design/plan itself "to save a turn." → All artifacts written by the role-scoped sub-agent.
  6. **Context Leak Across Loops** — Passing prior reviewer findings into the next adversarial loop. → Each loop is a fresh sub-agent with no prior-loop context.
- **Acceptance**: Section exists with all 6 anti-patterns named, described, and resolved.

**FR-09: Extend `enforce_pipeline_scope.py` to block orchestrator self-writes (#71, addresses C3)**
- Extend `delivery-team/hooks/enforce_pipeline_scope.py` (currently a soft-warn PreToolUse hook on Edit/Write/NotebookEdit) with new behavior:
  - **When**: An active pipeline is detected (`.delivery/state.md` shows `status: in_progress`).
  - **And**: The target file path matches `.delivery/artifacts/**` (any stage subdirectory) OR matches the configured `pipeline.scope` for source files.
  - **And**: The tool call is *not* originating from a sub-agent context (i.e. it is the orchestrator writing directly).
  - **Then**: Emit a `permissionDecision: deny` response with a message pointing the operator at the Delegation Prime Directive.
- **Origin detection mechanism (resolves OQ-1)**: The hook distinguishes orchestrator-attributed vs. sub-agent-attributed tool calls using a layered strategy:
  1. **Primary**: An environment variable `DELIVERY_FLOW_AGENT_CONTEXT` is set on every sub-agent dispatch (containing the role name, e.g. `po`, `architect`). The hook reads this variable; if absent, the call is treated as orchestrator-origin.
  2. **Secondary fallback**: If the env var mechanism is unavailable on a given harness version, the hook inspects tool-call metadata for a sub-agent invocation marker (transcript stack frame depth > 0).
  3. **Soft-deny fallback**: If neither signal is available (detection unreliable), the hook downgrades from `deny` to a loud `systemMessage` warning rather than blocking — preserving NFR-05 (never break a user pipeline).
- **Bash redirection coverage (closes the heredoc bypass)**: The hook's PreToolUse registration is extended to also trigger on the `Bash` tool. When the Bash command string matches a write-redirection pattern (`>`, `>>`, `tee`, `cat <<`, `cat >`, `dd of=`, `cp ... <artifact-path>`, `mv ... <artifact-path>`) targeting a path under `.delivery/artifacts/**` or the configured source scope, the same orchestrator-vs-sub-agent rule applies. This closes the trivial "Simplicity Shortcut via Bash heredoc" bypass that would otherwise defeat FR-06/FR-07.
- **Documented scope and known gaps** (per C3): The hook covers Edit, Write, NotebookEdit, and Bash-with-redirection. It does NOT intercept: (a) writes performed by MCP server tools that the harness routes outside the standard tool surface, (b) git operations that materialize files via `git checkout`/`git apply`, (c) writes by sub-processes spawned from a sub-agent (these inherit the env var, so they are correctly attributed). These gaps are documented in the hook's module docstring and surfaced as a known-limitations bullet in `references/quality-gates.md`.
- **Allowlist** (expanded per C3): orchestrator-owned routing metadata is exempt: `.delivery/state.md`, `.delivery/memory/**`, `.delivery/config.yml`, and any per-stage scratch path under `.delivery/artifacts/*/state/` or `.delivery/artifacts/*/handoff/` if present. The allowlist is centralized in a single constant in the hook module to prevent drift.
- **Activation timing** (resolves R7/C6): The hook's deny behavior is gated on `schema_version >= 2.7` AND a `pipeline.enforce_self_write_block: true` config flag (default `true` for fresh v2.7 configs, `false` for tolerantly-parsed v2.6 configs). This means the hook does NOT block the orchestrator authoring this PRD's own successor docs during the dogfood run until v2.7 schema is committed and the flag flips. Dogfood scope is therefore **forward-looking** (next run after merge), not self-referential.
- The hook MUST remain stdlib-only and degrade gracefully (existing `try/except sys.exit(0)` pattern in `main()`).
- **Acceptance**:
  - (a) With an active pipeline and `enforce_self_write_block: true`, an orchestrator-attributed Write to `.delivery/artifacts/02-refine/po/prd.md` is blocked; a sub-agent-attributed Write to the same path is allowed; a Write to `.delivery/state.md` is allowed in both cases.
  - (b) An orchestrator-attributed `Bash` call running `cat > .delivery/artifacts/02-refine/po/prd.md <<EOF ... EOF` is blocked under the same conditions.
  - (c) A sub-agent-attributed `Bash` call performing the same redirection is allowed.
  - (d) When `DELIVERY_FLOW_AGENT_CONTEXT` is unset and no fallback signal is available, the hook emits a warning rather than denying.
  - (e) The known-gaps list is present in the hook docstring and in `quality-gates.md`.

---

### Issue #70 — One sub-agent per reviewer role

**FR-10: "One Role = One Sub-Agent" rule in SKILL.md (#70)**
- Add a prominent rule block (callout style) in `SKILL.md` titled **"One Role = One Sub-Agent"**, placed inside or immediately adjacent to the Delegation Prime Directive section (FR-06).
- Content: *"Every reviewer role in every collaboration pattern is dispatched as its own sub-agent. A single sub-agent prompt MUST NOT request that the agent 'play multiple roles' or 'review as both X and Y.' Compound multi-role prompts violate context isolation."*
- **Acceptance**: Rule exists, is visually distinct, and is referenced by name from `team-patterns.md`, `quality-gates.md`, and `pipeline-stages.md`.

**FR-11: Reinforce in reference docs (#70)**
- `references/team-patterns.md`: Every collaboration pattern (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus) MUST lead with a one-line "Dispatch rule:" stating that each named role is its own sub-agent.
- `references/quality-gates.md`: DoD validation protocol clarified — each validator role is its own sub-agent invocation.
- `references/pipeline-stages.md`: A header note added explaining that `[PARALLEL]` and `[SEQUENTIAL]` markers refer to separate sub-agents per role, never compound prompts.
- **Acceptance**: Each of the three reference docs contains the dispatch rule in the locations specified.

**FR-12: Optional — `audit_agent_prompt.py` detects compound multi-role prompts (#70)**
- Extend `delivery-team/hooks/audit_agent_prompt.py` (PreToolUse on Agent tool) to scan the dispatched prompt text for compound-role smell patterns:
  - Phrases like "play the role of", "act as both", "review as X and Y", "you are the X, Y, and Z"
  - Multiple distinct role names from the known role registry within a single prompt
- On detection, emit a non-blocking `systemMessage` warning that names the detected pattern and links to the One Role = One Sub-Agent rule.
- This FR is **MAY** rather than **MUST**: if technical detection proves brittle, the docs-only path (FR-10, FR-11) is sufficient for this PRD's acceptance, and FR-12 may be deferred via Architect/Plan decision.
- **Acceptance** (if implemented): Hook fires a warning on a synthetic compound-role prompt; does not fire on a single-role prompt.

---

### Issue #69 — Architect adversarial loops with isolated context

**FR-13: "Isolated Adversarial Loop" pattern in `team-patterns.md` (#69)**
- Add a new pattern variant named **"Isolated Adversarial Loop"** to `delivery-team/skills/delivery-flow/references/team-patterns.md`, defined as a variant of the existing "Adversarial Review" pattern.
- Protocol specification (this exact structure must appear in the doc):
  1. **Setup**: Architect produces an architecture artifact.
  2. **Loop iteration N (starting at N=1)**:
     a. Spawn a fresh adversarial reviewer sub-agent. The sub-agent's prompt contains *only* the current architecture artifact and the standard adversarial reviewer brief. It MUST NOT contain findings from prior loops, summaries of what was fixed, or any reference to "this is loop N."
     b. Reviewer returns a list of issues (zero or more).
     c. If issues > 0: Architect (in a fresh sub-agent dispatch) revises the architecture to address them. Increment N. Go to 2a.
     d. If issues == 0: record a "clean pass" marker for this loop, then evaluate the convergence criterion (below) before exiting.
  3. **Convergence criterion (addresses C4)**: A single zero-finding loop is NOT sufficient evidence of convergence, because each fresh reviewer has no memory of prior loops and may surface a disjoint critique set. The loop terminates as `status: converged` only when ANY of the following holds:
     - **(a) Two-clean rule**: Two *consecutive* loops return zero findings. This guards against a lucky single clean pass on a non-monotonic critique stream.
     - **(b) No-new-classes rule**: The last 2 loops produced findings, but every finding belongs to an issue *class* already raised in earlier loops (i.e., no new issue class has appeared for 2 consecutive iterations). Issue classes are tagged by the reviewer using a small fixed taxonomy declared in `team-patterns.md` (e.g., `coupling`, `security`, `data-integrity`, `naming`, `testability`, `performance`, `docs`). The Architect documents residual same-class issues and proceeds.
     - **(c) Hard cap**: N reaches `max_self_correction` (default 3). Exit with `status: cap_reached`. Residual findings are documented and surfaced to the human checkpoint.
  4. **Loop cap**: As (c) above. Cap-reached is a documented exit, not a failure.
- The protocol explicitly states: *"Each loop's reviewer has zero knowledge of prior loops. This prevents anchoring on early findings and exposes deeper issues that single-pass review would miss. Convergence is therefore proven by repetition (two-clean) or by issue-class saturation (no-new-classes), never by a single clean pass."*
- **Acceptance**: Pattern exists in `team-patterns.md` with all four protocol steps, the three convergence criteria (two-clean, no-new-classes, hard-cap), the issue-class taxonomy, and the no-context-leak guarantee documented.

**FR-14: Reference Isolated Adversarial Loop from Stage 4 (#69)**
- In `references/pipeline-stages.md`, the Stage 4 (Architect) section is updated to specify that the adversarial review step uses the Isolated Adversarial Loop pattern from `team-patterns.md`.
- Stage 4 documentation calls out: loop count is bounded by `max_self_correction` (default 3); each iteration is a fresh sub-agent dispatch.
- **Acceptance**: Stage 4 in `pipeline-stages.md` references the new pattern by name and bounds loop count.

**FR-15: `max_self_correction` config key surfaced for Architect loops (#69)**
- Confirm `max_self_correction` exists in the v2.7 schema (it already does in v2.6 — verify in `config-schema.md` and document its expanded use for Architect adversarial loops).
- Default value remains `3`.
- **Acceptance**: `config-schema.md` v2.7 documents `max_self_correction` and lists "Architect adversarial loop cap" as one of its uses.

---

### Cross-cutting documentation parity

**FR-16: Schema version bump and doc parity (cross-cutting)**
- `delivery-team/skills/delivery-flow/references/config-schema.md`: Bumped to v2.7. Changelog entry summarizes: removed `project_type`, expanded `max_self_correction` use, added Isolated Adversarial Loop pattern reference.
- `CLAUDE.md`: Update the `Config schema` line in "Key Conventions" to reference v2.7.
- `README.md`: If it mentions `project_type` as a config field, update or remove that mention.
- `.claude-plugin/marketplace.json`: If the delivery-team plugin description mentions config schema version, update to v2.7. (Likely no change required — verify.)
- **Acceptance**: Grep for `2.6` across the four files returns only changelog/historical references; live docs say `2.7`.

---

## 5. Non-Functional Requirements

**NFR-01: Hook performance.** `enforce_pipeline_scope.py` p95 latency on a Write/Edit tool call MUST stay ≤ 50ms on the dogfood machine. Measured by wall-clock around the hook entry and exit. No measurable regression vs. the v2.6 baseline.

**NFR-02: Stdlib-only hooks.** All hook extensions (`enforce_pipeline_scope.py`, optional `audit_agent_prompt.py`) MUST remain pure Python stdlib. No new dependencies, no new package installs.

**NFR-03: Backwards compatibility.** Any `.delivery/config.yml` written under schema v2.6 (with or without `project_type`) MUST continue to load without error under v2.7 readers. Behavior is "tolerant ignore" with a deprecation log line.

**NFR-04: Documentation parity.** No PR in this bundle is mergeable while `CLAUDE.md`, `README.md`, `marketplace.json`, or `config-schema.md` still reference v2.6 as current. Doc parity is a DoD validator.

**NFR-05: Graceful hook degradation.** All hook code paths MUST preserve the existing "never crash, never block on error" guarantee — wrap `main()` in try/except and `sys.exit(0)` on any unexpected failure. A buggy hook must not break a user's pipeline.

**NFR-06: Self-consistency / dogfooding.** This bundle MUST itself be delivered through a delivery-flow run. The orchestrator must demonstrate the discipline it is being taught: zero self-writes, one role per sub-agent, isolated adversarial loops at Architect, and no reliance on a frozen `project_type`.

**NFR-07: Plugin-dev skill enforcement.** Any work that modifies a `SKILL.md` file or a hook script MUST load the corresponding `plugin-dev` skill first (`plugin-dev:skill-development`, `plugin-dev:hook-development`). This is a process NFR validated at the developer-stage DoD.

**NFR-08: Atomic merge.** All four issues' file changes ship as one cohesive set. No interleaved edits across separate PRs that would cause merge churn on `SKILL.md`, `pipeline-stages.md`, `team-patterns.md`, or `config-schema.md`.

---

## 6. Out of Scope

- Rewriting Phase 1 project-type detection logic itself. Only the *invocation cadence* changes.
- Introducing collaboration patterns beyond the Isolated Adversarial Loop variant.
- Adversarial loops at stages other than Architect. Loops at Refine, Design, or Plan are a future discussion and a separate PRD.
- A general-purpose migration tool for old `.delivery/config.yml` files. Tolerant parsing plus a deprecation log line is sufficient.
- Refactoring hooks unrelated to delegation enforcement or prompt auditing.
- Net-new analytics, telemetry, or dashboard work.
- Changes to any non-`delivery-flow` plugin (`developer/`, `architect/`, `quality/`, etc.).
- A new alias theme. Gandalf is borrowed from `alias-creator` for this run only.
- Changing `max_self_correction`'s default value (stays at 3).

---

## 7. Dependencies & Risks

### Dependencies
- **D1**: `plugin-dev:skill-development` and `plugin-dev:hook-development` skills must be loaded before any SKILL.md or hook edits.
- **D2**: Existing `enforce_pipeline_scope.py` `hook_utils` library and `.delivery/state.md` active-pipeline detection are reused — no rewrite of the detection layer.
- **D3**: The existing `max_self_correction` config key is reused as-is (no schema breaking change for that key).
- **D4**: The dogfood run depends on the orchestrator's existing checkpoint mechanism to surface human review at PRD acceptance, design acceptance, plan acceptance, and UAT.

### Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | Hook over-blocks legitimate orchestrator writes (e.g. to `state.md`) and breaks pipelines | Med | High | Explicit allowlist (FR-09) for `state.md`, `memory/**`, `config.yml`; dogfood test must complete end-to-end |
| R2 | Compound-role prompt detection (FR-12) is too brittle / produces false positives | Med | Med | FR-12 is MAY-not-MUST; can ship docs-only and defer the hook |
| R3 | Architect adversarial loops never converge — fresh reviewers raise disjoint critique sets indefinitely | **Med** (raised from Low per C4) | Med | FR-13 convergence criterion now requires two consecutive clean loops OR no-new-issue-classes for 2 loops OR hard cap; cap-reached remains a documented exit surfaced to human checkpoint |
| R4 | Backwards compat parsing of v2.6 configs misses an edge case and crashes | Low | High | NFR-05 graceful degradation; explicit test fixture with v2.6 config containing `project_type` |
| R5 | Doc parity check is forgotten and v2.6 references leak into shipped docs | Med | Med | NFR-04 makes doc parity a DoD validator; grep check in UAT |
| R6 | Self-write hook detects orchestrator vs sub-agent context unreliably | Med | High | FR-09 now specifies the layered detection (env var primary, transcript metadata secondary, soft-deny fallback) and Bash-redirection coverage; OQ-1 resolved in PRD |
| R7 | Dogfood run itself triggers the new self-write block on the orchestrator authoring this PRD's successor docs | High | Med | This is the *intended* behavior; orchestrator must dispatch all artifact writes to sub-agents from the start of this run |
| R8 | Changes to SKILL.md inadvertently shift section anchors used by other plugins | Low | Low | grep for cross-plugin SKILL.md references in plan stage |

---

## 8. Open Questions

These questions are surfaced for the Design and Architect stages to resolve. They are not blockers for PRD acceptance.

1. **OQ-1 (RESOLVED in FR-09 per C3)**: Origin detection uses a layered strategy — `DELIVERY_FLOW_AGENT_CONTEXT` env var as primary, transcript stack inspection as secondary fallback, soft-deny warning as final fallback. Architect to validate the env var injection point on sub-agent dispatch and confirm the transcript fallback shape.
2. **OQ-2 (Architect)**: For FR-12 (compound-role prompt detection), is the false-positive risk acceptable? Architect/Quality to decide whether to ship the hook or stay docs-only.
3. **OQ-3 (Design)**: Should the deprecation log line for legacy `project_type` (FR-02) appear in the orchestrator's stage banner, in `state.md`, or both?
4. **OQ-4 (Design)**: Where exactly in `SKILL.md` does "Step 4.5" live today, and does it survive renumbering after the Delegation Prime Directive section is added at the top?
5. **OQ-5 (Plan)**: Does the dogfood run's Architect stage need to demonstrate at least 2 adversarial loop iterations to validate FR-13, or is 1 clean pass acceptable evidence?
6. **OQ-6 (Operations)**: Does `marketplace.json` actually mention the schema version anywhere, or is FR-16's `marketplace.json` clause a no-op? Verify in Plan.
7. **OQ-7 (Quality)**: Test fixture for legacy v2.6 config — should we commit it under `delivery-team/tests/fixtures/` or generate it inline in the test? (Note: repo currently has no test runner configured per CLAUDE.md — Quality to recommend approach.)

---

## 9. GitHub Issues

This PRD bundles four GitHub issues from the `P47Phoenix/Claude-Plugins` repository. Each FR above is traceable back to one of them.

| Issue | Title (paraphrased) | Priority | WSJF | FRs |
|-------|---------------------|----------|------|-----|
| [#73](https://github.com/P47Phoenix/Claude-Plugins/issues/73) | Remove `project_type` from config; detect every run | P0 | 25.0 | FR-01, FR-02, FR-03, FR-04, FR-05 |
| [#71](https://github.com/P47Phoenix/Claude-Plugins/issues/71) | Orchestrator bypasses delegation when "simple" | P0 | 14.5 | FR-06, FR-07, FR-08, FR-09 |
| [#70](https://github.com/P47Phoenix/Claude-Plugins/issues/70) | Enforce one-sub-agent-per-reviewer across all patterns | P0 | 14.0 | FR-10, FR-11, FR-12 |
| [#69](https://github.com/P47Phoenix/Claude-Plugins/issues/69) | Architect adversarial loops with isolated context | P1 | 11.0 | FR-13, FR-14, FR-15 |
| (cross-cut) | Schema bump and doc parity | — | — | FR-16 |

Implementation order within the bundle is recommended (not mandatory) to follow WSJF: #73 → #71 → #70 → #69, with FR-16 doc-parity tasks running in parallel to whichever code changes are touching their respective files. Final ordering is the Plan stage's call.

---

## 10. PRD-Level Acceptance Criteria

This PRD is accepted into Stage 3 (Design) when:

- [ ] All 16 FRs above are reviewed and confirmed traceable to one of the 4 source issues.
- [ ] All 8 NFRs are reviewed and acknowledged as constraints on Design and Plan.
- [ ] Out-of-scope list is confirmed by the human checkpoint reviewer.
- [ ] Open questions are routed to the correct downstream stage (Design / Architect / Plan / Quality / Operations as labeled).
- [ ] The dogfood requirement (NFR-06) is acknowledged: this bundle delivers itself.

---

*"All we have to decide is what to fix with the discipline that is given to us. And we have decided: we fix the orchestrator's shortcuts before we trust it with anything larger. The road goes ever on — but it goes through delegation, isolation, iteration, and truth."*

— Gandalf, PO

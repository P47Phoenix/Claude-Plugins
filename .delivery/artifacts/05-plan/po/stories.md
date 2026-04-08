# User Stories: Orchestration Discipline Bundle

**Stage**: 05 — Plan (PO sub-flow)
**PO**: Gandalf the Grey
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` (16 FRs, 8 NFRs)
**Source Architecture**: `.delivery/artifacts/04-architect/solution/architecture.md`
**ADRs**: ADR-001 (origin detection), ADR-002 (project_type migration), ADR-003 (loop convergence)

> *"A wizard does not estimate hastily. He weighs the road, the burden, and the daylight that remains."*
> *— Gandalf*

---

## Capacity Declaration

| Parameter | Value |
|---|---|
| Sprint length | 1 sprint (single-sprint target) |
| Team | 1 developer (solo) |
| Nominal capacity | 40 points (1 dev × 1 sprint, calibrated to historical bundle size) |
| Sprint ceiling | 80% utilization → **32 points committed maximum** |
| Calibration rule | **Markdown / protocol-doc edits estimated one tier lower than equivalent code edits** (per memory `feedback_*` and Plan-stage rule). Tier ladder: 0.5 / 1 / 2 / 3 / 5 / 8. A doc-only edit that would be a "3" as code becomes a "2"; a "2" becomes a "1"; a "1" becomes a "0.5". |
| Test artifact rule | Test cases are co-located with each story, never split into a separate artifact (memory: mandatory artifact pairing). |

### Single-sprint viability justification

Thirteen stories sounds like a lot. It is not, in this bundle, because:

1. **Eleven of thirteen stories are markdown / protocol-doc edits.** Per the calibration rule above, those compress to small tiers (0.5 – 2 points each).
2. **Only two stories touch executable code** (OD-07 hook extension, OD-10 optional audit hook). They carry the bulk of the points.
3. **The edit map (architecture §5) is fixed and contiguous.** No discovery cost — the architect already named every file and what changes go in it.
4. **Atomic-merge NFR (NFR-08)** *requires* single-sprint shipping: splitting across sprints would force `SKILL.md`, `pipeline-stages.md`, `team-patterns.md`, and `config-schema.md` to be edited twice with merge churn between runs.
5. **OD-10 is explicitly optional (MAY)** per FR-12; if total commit exceeds 32 points, OD-10 is the first story dropped to the next sprint.

**Total committed**: 32 points (see roll-up at end). **Headroom**: 0 strict / 5 if OD-10 is deferred. Within 80% rule.

---

## Pre-loaded Constraints (apply to every story)

- **Plugin-dev skill enforcement (NFR-07)**: any story touching `SKILL.md` must load `plugin-dev:skill-development` first; any story touching a hook script must load `plugin-dev:hook-development` first. Stated once here, not repeated per story.
- **Stdlib-only (NFR-02)**: hook stories add no dependencies.
- **Graceful degradation (NFR-05)**: hook stories preserve `try/except → sys.exit(0)`.
- **Atomic merge (NFR-08)**: all 13 stories ship as one PR.
- **Doc parity (NFR-04)**: every story that bumps schema or removes `project_type` must verify CLAUDE.md / README.md / marketplace.json / docs/** parity by sprint end (rolled into OD-13).
- **Dogfood (NFR-06)**: orchestrator routes every artifact write through a sub-agent for the duration of this bundle.
- **Activation gating**: deny behavior gated on `schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true` (ADR-001 §2.5). Dogfood run is forward-looking.

---

## Sprint Goal

> Ship the four orchestration discipline fixes (#73, #71, #70, #69) as one cohesive, atomically-merged bundle that the orchestrator demonstrably dogfoods, with schema bumped to v2.7 and all docs in parity.

---

## Stories

## Issue #73 — Remove `project_type` from config

---

### OD-01 — Remove `project_type` from config schema and wizard Q1

**Story**
> As the **PO Operator (P1)**, I want a fresh `.delivery/config.yml` written by the setup wizard to contain no `project_type` key, so that my project type is decided per-request from what I actually ask for, not from a frozen wizard guess.

**Traces**: FR-01, FR-04
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **2**
**Dependencies**: none (foundation story for the bundle)

**Acceptance criteria**
1. `delivery-team/skills/delivery-flow/references/config-schema.md` no longer lists `project_type` as a required or recommended key in the active schema section.
2. `project_type` appears only under a new "Deprecated keys" section with a one-line migration note pointing at `routing.force_type`.
3. `delivery-team/skills/delivery-flow/references/setup-wizard.md` removes the project-type question (today's Q1) and renumbers Q2 – Q10 as Q1 – Q9.
4. The setup wizard's documented output config example contains no `project_type` field.
5. Grep across `delivery-team/skills/delivery-flow/` for `project_type` returns only deprecation notes and Phase 1 detection prose — no config-driven references.

**Test cases** (mandatory)
| ID | Test | Expected |
|---|---|---|
| OD-01-T1 | Render the wizard from `setup-wizard.md` mentally and count questions | Exactly 9 questions, none about project type |
| OD-01-T2 | Open `config-schema.md`, search for `project_type` in the active schema table | Not present in active table; present only under "Deprecated keys" |
| OD-01-T3 | Run `grep -rn "project_type" delivery-team/skills/delivery-flow/` | Hits only in deprecation notes, Phase 1 detection, or `references/project-types.md` framing prose |
| OD-01-T4 | Confirm migration note in deprecated section names `routing.force_type` as the replacement | Note present and correct |

---

### OD-02 — Phase 1 detection runs every pipeline invocation (no config override branch)

**Story**
> As the **Future Orchestrator Instance (P3)**, I want `SKILL.md` Phase 1 to always run from the current user request, so that I never inherit a stale routing decision from a config file.

**Traces**: FR-03, FR-05
**Type**: Markdown / protocol doc (SKILL.md prose)
**Priority**: P0
**Story points**: **2**
**Dependencies**: OD-01 (config schema must already be defining `project_type` as deprecated before SKILL.md is reworded)

**Acceptance criteria**
1. `delivery-team/skills/delivery-flow/SKILL.md` Phase 1 section states unambiguously that detection runs on **every** `/delivery-flow` invocation, using the current user request as input.
2. SKILL.md no longer contains any branch reading `project_type` from `.delivery/config.yml` for routing.
3. Detected type is documented as written to `.delivery/state.md` for the run only — never persisted back to `config.yml`.
4. `references/project-types.md` reframes project types as a **runtime routing decision**, not a config setting.
5. SKILL.md routing guidance language consistently uses "current-request detection" vocabulary, not "configured project_type".

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-02-T1 | Read SKILL.md Phase 1 section end-to-end | Detection is unconditional on every invocation; no config override branch present |
| OD-02-T2 | Two-run thought experiment: same repo, request A = "fix bug X", request B = "build greenfield service Y" | Two different routing decisions documented as the expected behavior |
| OD-02-T3 | Grep SKILL.md for `config.yml` near `project_type` | Zero matches that read project_type for routing |
| OD-02-T4 | Read `references/project-types.md` opening section | Frames types as runtime routing decisions, not config keys |
| OD-02-T5 | (FR-03 acceptance) Verify SKILL.md states `state.md` is the only persistence location | Stated explicitly |

---

### OD-03 — Add `routing.force_type` opt-in override key

**Story**
> As a **PO Operator (P1) running a docs-only repo**, I want an explicit, namespaced opt-in key to pin the project type, so that I can keep my deliberate routing pin without re-creating the v2.6 silent footgun.

**Traces**: FR-02 (parts b and c)
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **1**
**Dependencies**: OD-01 (schema doc must exist in v2.7-ready state); OD-04 (schema bump narrative)

**Acceptance criteria**
1. `config-schema.md` documents `routing.force_type` as a v2.7 opt-in key with an enum matching the Phase 1 detection vocabulary (PQ-3 assumption locked).
2. Schema doc explains that the key is namespaced under `routing.` deliberately, to make the pin a discoverable, intentional act (not a top-level footgun).
3. Behavior matrix (architecture §3.2) is mirrored or referenced in the schema doc.
4. SKILL.md Phase 1 prose explains: detection still runs and is logged, but routing uses `routing.force_type` when present, with a banner line announcing the pin.
5. When both bare top-level `project_type` and `routing.force_type` are present, `routing.force_type` wins; bare `project_type` is still logged as deprecated. Documented in schema doc.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-03-T1 | Read `config-schema.md` v2.7 entry for `routing.force_type` | Enum, default (none), description, intentional-pin rationale all present |
| OD-03-T2 | Trace FR-02 acceptance (b): config with `routing.force_type: DOCS_ONLY` | Documented to route as DOCS_ONLY; Phase 1 still runs and logs |
| OD-03-T3 | Trace FR-02 acceptance (c): both keys present | `routing.force_type` wins, bare `project_type` still emits deprecation log |
| OD-03-T4 | Confirm key is under `routing.` namespace, not top-level | Confirmed in doc and example YAML |
| OD-03-T5 | SKILL.md Phase 1 references the override behavior | Reference present and consistent with schema doc |

---

### OD-04 — Bump schema v2.6 → v2.7 with migration notes

**Story**
> As a **Plugin Contributor (P2)**, I want a clear schema version bump and changelog so that I can tell at a glance which configs need migration and which keys are now deprecated.

**Traces**: FR-01, FR-02 (part a), FR-15, FR-16 (config-schema portion)
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **2**
**Dependencies**: OD-01, OD-03 (deprecation and new key must be defined before changelog summarizes them)

**Acceptance criteria**
1. `config-schema.md` `schema_version` value bumped from `2.6` → `2.7`.
2. Changelog entry added summarizing: removed `project_type` from active schema, added `routing.force_type`, added `pipeline.enforce_self_write_block`, expanded `max_self_correction` use to cover Architect adversarial loops.
3. "Deprecated keys" section explicitly states tolerant-parse rule (FR-02 a): a v2.6 config with bare top-level `project_type` parses without error, emits one deprecation banner, and Phase 1 detection drives routing.
4. `max_self_correction` documentation updated to list "Architect adversarial loop cap (default 3)" as one of its uses (FR-15).
5. `pipeline.enforce_self_write_block` documented as a v2.7 key, default `true` for fresh v2.7 configs and effective `false` for tolerantly-parsed v2.6 configs (architecture §2.5 and ADR-001).

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-04-T1 | Open `config-schema.md`, read top-of-file version line | Says `2.7` |
| OD-04-T2 | Read changelog entry for v2.7 | Lists all 4 changes named in AC #2 |
| OD-04-T3 | (FR-02 a) Trace v2.6 legacy config with `project_type: GREENFIELD` through documented tolerant-parse path | Documented path produces: parse OK, deprecation banner, Phase 1 drives routing |
| OD-04-T4 | (FR-15) Read `max_self_correction` entry | Lists Architect adversarial loop cap as an explicit use |
| OD-04-T5 | (NFR-03) Backwards-compat assertion present in deprecated keys section | Present and unambiguous |

---

## Issue #71 — Orchestrator delegation bypass

---

### OD-05 — Strengthen SKILL.md delegation principle + anti-patterns section

**Story**
> As the **Future Orchestrator Instance (P3)**, I want an unambiguous Delegation Prime Directive at the top of SKILL.md and a named anti-patterns catalog, so that I cannot rationalize a "simplicity shortcut" exemption.

**Traces**: FR-06, FR-08
**Type**: Markdown / protocol doc (SKILL.md structural edit)
**Priority**: P0
**Story points**: **3**
**Dependencies**: none structurally, but coordinate with OD-02, OD-06, OD-08 because all four edit SKILL.md (atomic merge)

**Acceptance criteria**
1. New section **"Delegation Prime Directive"** added to `SKILL.md`, placed immediately after the skill metadata block and before any stage descriptions. Content: *"The orchestrator NEVER writes artifacts, source files, or implementation content during a pipeline run. All such work is delegated to a role-scoped sub-agent. There are no 'simple enough' exemptions."*
2. The Directive is the first prose block of the file and is referenced from at least three downstream sections (Step 4.5, stage execution, anti-patterns).
3. New section **"Common Orchestrator Anti-Patterns"** added after stage descriptions and before the references list, containing all six anti-patterns named in FR-08 (Simplicity Shortcut, Compound Reviewer Prompt, Frozen Type Routing, Single-Pass Adversarial, Inline Artifact Authoring, Context Leak Across Loops), each with name, one-line description, and the correct alternative.
4. Each anti-pattern cross-links to the FR or other section that resolves it.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-05-T1 | Read SKILL.md from top — first prose block after metadata | Is the Delegation Prime Directive |
| OD-05-T2 | Grep SKILL.md for "Delegation Prime Directive" | At least 4 hits (1 section header + ≥3 cross-references) |
| OD-05-T3 | Count anti-patterns in the new section | Exactly 6, with all FR-08 names present |
| OD-05-T4 | Each anti-pattern has name + description + alternative | True for all 6 |
| OD-05-T5 | Anti-patterns 1, 2, 3, 4 cross-link to FR-06/07, FR-10, FR-03, FR-13 respectively | Cross-links present |

---

### OD-06 — Update Step 4.5 to reject "simple" as a justification

**Story**
> As the **Future Orchestrator Instance (P3)** standing at the pre-dispatch decision point, I want Step 4.5 to explicitly reject "this is simple enough to do inline," so that I have no language-loophole to justify a self-write.

**Traces**: FR-07
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **1**
**Dependencies**: OD-05 (Delegation Prime Directive must exist so Step 4.5 can link to it)

**Acceptance criteria**
1. SKILL.md "Step 4.5" (orchestrator pre-dispatch decision step) is located and any current language permitting inline orchestrator action for "simple" or "trivial" tasks is replaced.
2. New language reads (or substantively says): *"Perceived simplicity is NOT a valid reason to skip delegation. If the work product is a pipeline artifact or source file, it MUST be delegated."*
3. Step 4.5 contains an explicit link or reference to the Common Orchestrator Anti-Patterns section (specifically the "Simplicity Shortcut" entry).
4. Step 4.5 also references the Delegation Prime Directive by name.
5. OQ-4 resolved: confirm Step 4.5 still exists by that name after OD-05's restructuring; if renumbered, both names are noted.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-06-T1 | Locate Step 4.5 in SKILL.md | Found |
| OD-06-T2 | Read Step 4.5 — search for "simple" or "trivial" as a positive exemption | Zero such exemptions; explicit rejection language present |
| OD-06-T3 | Step 4.5 references Anti-Patterns section | Reference present |
| OD-06-T4 | Step 4.5 references Delegation Prime Directive | Reference present |
| OD-06-T5 | OQ-4 disposition note recorded in story or commit message | Disposition recorded |

---

### OD-07 — Extend `enforce_pipeline_scope.py` with origin detection per ADR-001

**Story**
> As a **Plugin Contributor (P2)**, I want `enforce_pipeline_scope.py` to deny orchestrator-attributed writes to pipeline artifacts (with a graceful soft-deny fallback), so that the Delegation Prime Directive is enforced by code, not just by prose.

**Traces**: FR-09 (all sub-clauses a–e), NFR-01, NFR-02, NFR-05
**Type**: Executable code (Python hook)
**Priority**: P0
**Story points**: **8**
**Dependencies**: OD-04 (schema v2.7 + `pipeline.enforce_self_write_block` must be defined before the hook gates on them); OD-05 (Delegation Prime Directive section name referenced in hook messages)

**Acceptance criteria**
1. Layered origin detection implemented per ADR-001 §2.2:
   - **Layer 1**: read `DELIVERY_FLOW_AGENT_CONTEXT` env var; presence ⇒ allow.
   - **Layer 2**: inspect hook input metadata for sub-agent frame indicators (`parent_tool_use_id` or equivalent); positive ID ⇒ allow.
   - **Layer 3**: neither resolves ⇒ emit a loud `systemMessage` warning naming the Delegation Prime Directive and target path. Do NOT deny.
2. Allowlist constant centralized (single module-level constant) covering: `.delivery/state.md`, `.delivery/config.yml`, `.delivery/memory/**`, `.delivery/artifacts/*/state/**`, `.delivery/artifacts/*/handoff/**`. Always allowed regardless of origin.
3. Bash redirection coverage: hook also fires on `Bash` tool. A regex matches `>`, `>>`, `tee`, `cat <<EOF`, `cat >`, `dd of=`, `cp ... <path>`, `mv ... <path>` targeting in-scope paths. Same origin rule applies. `delivery-team/hooks/hooks.json` registers the hook on `Bash`.
4. Activation gating: deny behavior is gated on `schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true`. Default for fresh v2.7 configs is `true`; effective `false` for tolerantly-parsed v2.6 configs.
5. Module docstring lists known gaps explicitly (per FR-09): MCP server tools routed outside standard surface, git operations materializing files, etc.
6. All new logic stays inside the existing `try/except → sys.exit(0)` wrapper. Stdlib only (`os`, `re`, `fnmatch`, `pathlib`, `json`).
7. p95 latency on a Write/Edit tool call is ≤ 50ms (NFR-01). Hook adds ≤ 15ms over baseline (architecture budget §2.6).

**Test cases** (covers FR-09 a–e exhaustively)
| ID | Test | Expected |
|---|---|---|
| OD-07-T1 | (FR-09 a, orchestrator deny) Active pipeline + flag on; orchestrator-attributed Write to `.delivery/artifacts/02-refine/po/prd.md` | `permissionDecision: deny` |
| OD-07-T2 | (FR-09 a, sub-agent allow) Same conditions; sub-agent-attributed Write to same path (env var set) | Allowed |
| OD-07-T3 | (FR-09 a, allowlist) Write to `.delivery/state.md` (orchestrator OR sub-agent) | Allowed in both cases |
| OD-07-T4 | (FR-09 b) Orchestrator-attributed Bash: `cat > .delivery/artifacts/02-refine/po/prd.md <<EOF ... EOF` | Denied |
| OD-07-T5 | (FR-09 c) Sub-agent-attributed Bash with same heredoc redirection | Allowed |
| OD-07-T6 | (FR-09 d) Env var unset AND no Layer 2 signal | Warning `systemMessage` emitted, no deny |
| OD-07-T7 | (FR-09 e) Module docstring grep for "Known gaps" / "limitations" section | Present; mirrored in `quality-gates.md` |
| OD-07-T8 | (NFR-01) Time 100 invocations on a no-op Write call | p95 ≤ 50ms total |
| OD-07-T9 | (Activation gating) v2.6 config tolerantly parsed; orchestrator-attributed Write to artifact path | Allowed (flag effective false) |
| OD-07-T10 | (Activation gating) v2.7 config, flag explicitly `false` | Allowed (flag false) |
| OD-07-T11 | (NFR-05) Force a synthetic exception inside the hook body | Hook exits 0; pipeline unaffected |
| OD-07-T12 | (Bash patterns) Each of `>`, `>>`, `tee`, `cat <<`, `dd of=`, `cp`, `mv` patterns into an artifact path | All matched and routed through origin rule |
| OD-07-T13 | (Allowlist constant) Grep for allowlist literal — exactly one definition | One definition, no drift |

---

## Issue #70 — One sub-agent per reviewer role

---

### OD-08 — Add "One Role = One Sub-Agent" rule to SKILL.md

**Story**
> As the **Plugin Contributor (P2)** reviewing pipeline artifacts, I want the orchestrator to dispatch a separate sub-agent per reviewer role, so that I can trust adversarial review and review-board verdicts as the product of independent contexts rather than one agent ventriloquizing three roles.

**Traces**: FR-10
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **1**
**Dependencies**: OD-05 (Delegation Prime Directive section must exist; this rule sits inside or adjacent to it)

**Acceptance criteria**
1. Visually distinct callout block titled **"One Role = One Sub-Agent"** added to `SKILL.md`, placed inside or immediately adjacent to the Delegation Prime Directive section.
2. Content states: *"Every reviewer role in every collaboration pattern is dispatched as its own sub-agent. A single sub-agent prompt MUST NOT request that the agent 'play multiple roles' or 'review as both X and Y.' Compound multi-role prompts violate context isolation."*
3. The rule is referenced by name from `team-patterns.md`, `quality-gates.md`, and `pipeline-stages.md` (cross-referenced — actual edits in OD-09).

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-08-T1 | Open SKILL.md, locate "One Role = One Sub-Agent" callout | Present, visually distinct, inside or adjacent to Delegation Prime Directive |
| OD-08-T2 | Read callout content | Matches FR-10 wording (or substantively equivalent) |
| OD-08-T3 | Grep `team-patterns.md`, `quality-gates.md`, `pipeline-stages.md` for the rule name | Each contains a reference (verified in OD-09 too) |

---

### OD-09 — Reinforce in `team-patterns.md`, `quality-gates.md`, `pipeline-stages.md`

**Story**
> As the **Future Orchestrator Instance (P3)** reading reference docs as ground truth, I want every collaboration pattern and DoD validator to lead with an explicit "Dispatch rule: each named role is its own sub-agent," so that I cannot collapse three reviewers into one prompt without contradicting the docs I'm reading.

**Traces**: FR-11
**Type**: Markdown / protocol doc
**Priority**: P0
**Story points**: **2**
**Dependencies**: OD-08 (the rule must be canonically defined in SKILL.md so reference docs can link to it)

**Acceptance criteria**
1. `references/team-patterns.md`: every collaboration pattern (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus) MUST lead with a one-line **"Dispatch rule:"** stating that each named role is its own sub-agent.
2. `references/quality-gates.md`: DoD validation protocol clarified — each validator role is its own sub-agent invocation. Add a "Known hook limitations" list mirrored from the hook docstring (also touched by OD-07).
3. `references/pipeline-stages.md`: header note added explaining that `[PARALLEL]` and `[SEQUENTIAL]` markers refer to separate sub-agents per role, never compound prompts.
4. Each of the three docs cross-references the canonical "One Role = One Sub-Agent" rule in SKILL.md by name.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-09-T1 | Open `team-patterns.md`; for each of the 6 patterns named in FR-11, find the "Dispatch rule:" line | Present in all 6 |
| OD-09-T2 | Open `quality-gates.md`; verify per-role sub-agent invocation language for DoD validators | Present |
| OD-09-T3 | Open `quality-gates.md`; locate "Known hook limitations" list mirroring OD-07 hook docstring | Present and consistent |
| OD-09-T4 | Open `pipeline-stages.md`; locate header note on `[PARALLEL]` / `[SEQUENTIAL]` markers | Present |
| OD-09-T5 | Each of the 3 docs grep-references "One Role = One Sub-Agent" | One or more references in each |

---

### OD-10 — (OPTIONAL / MAY) Extend `audit_agent_prompt.py` for compound-role detection

**Story**
> As a **Plugin Contributor (P2)**, I want a non-blocking audit warning when an agent dispatch prompt contains compound-role smell patterns ("act as both", "play the role of", multiple distinct role names), so that I notice context-isolation violations before they ship.

**Traces**: FR-12, NFR-02, NFR-05
**Type**: Executable code (Python hook), explicitly **MAY** per FR-12
**Priority**: P2 (deferrable)
**Story points**: **3**
**Dependencies**: OD-08 (the canonical rule must exist for the warning to link to)

**Note**: Per FR-12, this story is **MAY-not-MUST**. If sprint capacity tightens or if false-positive risk in negation-aware matching proves high during implementation, **this is the first story dropped** and the docs-only path (OD-08, OD-09) is sufficient for PRD acceptance. OQ-2 disposition is captured here.

**Acceptance criteria**
1. `delivery-team/hooks/audit_agent_prompt.py` (PreToolUse on Agent tool) extended to scan dispatched prompt text for compound-role patterns:
   - Phrases: "play the role of", "act as both", "review as X and Y", "you are the X, Y, and Z".
   - Multiple distinct role names from the known role registry within a single prompt.
2. Detection is **negation-aware** (e.g., "do NOT act as both" must not trigger).
3. On detection, hook emits a non-blocking `systemMessage` warning naming the detected pattern and linking to the "One Role = One Sub-Agent" rule.
4. Hook does NOT block. NFR-05 preserved.
5. Stdlib only. NFR-02 preserved.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-10-T1 | Synthetic compound-role prompt: "you are the architect and the security reviewer" | Warning fires, names the pattern, links to rule |
| OD-10-T2 | Single-role prompt: "you are the architect" | No warning |
| OD-10-T3 | Negation: "do not act as both reviewer and architect" | No warning (negation-aware) |
| OD-10-T4 | Multiple known role names in same prompt: "the po and the developer" | Warning fires |
| OD-10-T5 | Force exception inside the hook | Hook exits 0; agent dispatch proceeds |
| OD-10-T6 | Run `python -c "import audit_agent_prompt"` after edit | No new third-party import errors |

---

## Issue #69 — Isolated adversarial loops

---

### OD-11 — Document "Isolated Adversarial Loop" pattern in `team-patterns.md` (with convergence algorithm from ADR-003)

**Story**
> As the **Architect Sub-Agent (P4)**, I want a formally documented Isolated Adversarial Loop pattern with explicit setup, loop, convergence rules, taxonomy, and no-context-leak guarantee, so that I can run iterative adversarial review with bounded termination instead of one anchored pass.

**Traces**: FR-13, FR-15 (taxonomy + cap reference)
**Type**: Markdown / protocol doc (significant new pattern)
**Priority**: P1
**Story points**: **3**
**Dependencies**: none (ADR-003 is the source; this story transcribes it into `team-patterns.md`)

**Acceptance criteria**
1. New pattern variant **"Isolated Adversarial Loop"** added to `delivery-team/skills/delivery-flow/references/team-patterns.md` as a variant of "Adversarial Review."
2. Protocol specification matches FR-13 / ADR-003 §4 / architecture §4.3:
   - **Setup**: Architect produces an architecture artifact.
   - **Loop iteration N (starting at 1)**: spawn fresh adversarial reviewer sub-agent with ONLY the current artifact + reviewer brief + taxonomy. No prior findings, no fix summaries, no "this is loop N." Reviewer returns findings. If issues > 0, Architect (fresh dispatch) revises; increment N; loop. If issues == 0, record clean pass and evaluate convergence.
3. **Convergence criteria** documented in full:
   - **(a) Two-clean rule** — two consecutive zero-finding loops → `converged (two_clean)`.
   - **(b) No-new-classes rule** — two consecutive loops with findings, but every finding belongs to a class already raised in earlier loops → `converged (class_saturated)`. Residuals documented.
   - **(c) Hard cap** — `N >= max_self_correction` (default 3) → `cap_reached`. Documented exit, not a failure. Surfaced to human checkpoint.
4. **Issue class taxonomy** declared verbatim: `coupling | security | data-integrity | naming | testability | performance | docs`. Untagged findings bucket as `misc` and count as new class.
5. Explicit invariant statement: *"Each loop's reviewer has zero knowledge of prior loops. This prevents anchoring on early findings and exposes deeper issues that single-pass review would miss. Convergence is therefore proven by repetition (two-clean) or by issue-class saturation (no-new-classes), never by a single clean pass."*
6. Architect revision sub-agent invariant: sees ONLY current loop's findings, never prior loops'.
7. Pseudocode block from architecture §4.3 reproduced or linked.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-11-T1 | Open `team-patterns.md`; locate "Isolated Adversarial Loop" pattern | Present as a variant of Adversarial Review |
| OD-11-T2 | Verify all 4 protocol steps (setup, loop, convergence, cap) present | All 4 present in correct order |
| OD-11-T3 | Verify all 3 convergence rules (two-clean, no-new-classes, hard-cap) present with names | All 3 present with names matching ADR-003 |
| OD-11-T4 | Verify taxonomy: 7 classes named exactly | 7 classes exact; `misc` bucket rule documented |
| OD-11-T5 | Verify no-context-leak invariant statement | Present, prominent |
| OD-11-T6 | Verify Architect-revision sub-agent invariant (current loop findings only) | Present |
| OD-11-T7 | Trace FR-13 acceptance one bullet at a time | All bullets satisfied |
| OD-11-T8 | (FR-15) Pattern doc references `max_self_correction` config key with default 3 | Reference present |
| OD-11-T9 | Worked example: 3 loops, loop 1 = [coupling, security], loop 2 = [coupling], loop 3 = [coupling] | Documented as `converged (class_saturated)` exit |
| OD-11-T10 | Worked example: loop 1 = [], loop 2 = [] | `converged (two_clean)` |
| OD-11-T11 | Worked example: 3 loops all with new classes each time | `cap_reached`, residuals documented, surfaced to human |

---

### OD-12 — Update Stage 4 Architect sub-flow in `pipeline-stages.md` to use loops

**Story**
> As the **Future Orchestrator Instance (P3)** entering Stage 4, I want the documented Architect sub-flow to call out the Isolated Adversarial Loop pattern by name and bound the loop count, so that I cannot accidentally fall back to single-pass adversarial review.

**Traces**: FR-14, FR-15
**Type**: Markdown / protocol doc
**Priority**: P1
**Story points**: **1**
**Dependencies**: OD-11 (the pattern must be defined before Stage 4 references it by name)

**Acceptance criteria**
1. `references/pipeline-stages.md` Stage 4 (Architect) section updated to specify that the adversarial review step uses the Isolated Adversarial Loop pattern from `team-patterns.md`, **referenced by name**.
2. Stage 4 documentation calls out: loop count is bounded by `max_self_correction` (default 3); each iteration is a fresh sub-agent dispatch; cap-reached is a documented exit surfaced to the human checkpoint.
3. Stage 4 documentation makes clear that one clean loop is **not** sufficient for convergence (forwards reader to OD-11's two-clean / no-new-classes rules).

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-12-T1 | Open `pipeline-stages.md` Stage 4 section | References "Isolated Adversarial Loop" by name |
| OD-12-T2 | Stage 4 mentions `max_self_correction` and default 3 | Present |
| OD-12-T3 | Stage 4 explicitly forbids single-clean exit | Forbidden, with link forward to convergence rules |
| OD-12-T4 | Stage 4 mentions cap-reached as a documented exit, not failure | Present |

---

## Cross-cutting documentation parity

---

### OD-13 — Update CLAUDE.md, README.md, marketplace.json, docs/** to reflect v2.7 and new rules

**Story**
> As a **Plugin Contributor (P2)**, I want every consumer-facing doc (CLAUDE.md, README.md, marketplace.json, MkDocs site) to reflect schema v2.7 and the new orchestration rules before merge, so that I cannot find a stale v2.6 reference anywhere in the shipped surface.

**Traces**: FR-16, NFR-04, NFR-08
**Type**: Markdown / protocol doc + JSON edit (no executable code)
**Priority**: P0 (DoD validator — bundle is unmergeable until satisfied)
**Story points**: **3**
**Dependencies**: OD-04 (schema must be at v2.7); ideally runs **last** in the sprint to catch any newly-introduced v2.6 references from earlier stories

**Acceptance criteria**
1. `CLAUDE.md` "Key Conventions" section's "Config schema" line updated: v2.6 → v2.7.
2. `README.md`: any mention of `project_type` as a config field is updated or removed. Any `2.6` reference in current-state docs updated to `2.7`.
3. `.claude-plugin/marketplace.json`: any schema version mention updated to v2.7. (Likely no-op per OQ-6 — verified explicitly.)
4. `docs/**` (MkDocs Material site, 25 pages per CLAUDE.md): grep for `project_type`, `schema_version: 2.6`, bare `2.6` and update surviving live references. Changelog/historical references may remain unchanged.
5. Final grep gate: `grep -rn "2\.6" CLAUDE.md README.md .claude-plugin/marketplace.json docs/` returns only changelog/historical context — zero live references.
6. Final grep gate: `grep -rn "project_type" CLAUDE.md README.md .claude-plugin/marketplace.json docs/` returns only deprecation notes or changelog entries.

**Test cases**
| ID | Test | Expected |
|---|---|---|
| OD-13-T1 | (FR-16) Read CLAUDE.md "Config schema" line | Says v2.7 |
| OD-13-T2 | Grep README.md for `project_type` as a config field | Zero live references; deprecation notes only if any |
| OD-13-T3 | Inspect `.claude-plugin/marketplace.json` for schema version literals | Either updated to v2.7 or verified no-op |
| OD-13-T4 | (Per architecture §5.3) Grep `docs/**` for `project_type`, `schema_version: 2.6`, bare `2.6` | Only changelog/historical hits remain |
| OD-13-T5 | (NFR-04 DoD gate) Run final cross-file grep for `2\.6` across the four targets | Only historical references; zero live |
| OD-13-T6 | (OQ-6 disposition) Note recorded as to whether `marketplace.json` actually contained a schema version | Recorded |

---

## Sprint Roll-Up

| Story | Type | Priority | Points | Depends on |
|---|---|---|---|---|
| OD-01 | doc | P0 | 2 | — |
| OD-02 | doc | P0 | 2 | OD-01 |
| OD-03 | doc | P0 | 1 | OD-01, OD-04 |
| OD-04 | doc | P0 | 2 | OD-01, OD-03 |
| OD-05 | doc | P0 | 3 | — |
| OD-06 | doc | P0 | 1 | OD-05 |
| OD-07 | code | P0 | 8 | OD-04, OD-05 |
| OD-08 | doc | P0 | 1 | OD-05 |
| OD-09 | doc | P0 | 2 | OD-08 |
| OD-10 | code | P2 (MAY) | 3 | OD-08 |
| OD-11 | doc | P1 | 3 | — |
| OD-12 | doc | P1 | 1 | OD-11 |
| OD-13 | doc | P0 | 3 | OD-04, all others |
| **Total committed** | | | **32** | |
| Sprint ceiling (80% of 40) | | | **32** | |
| Headroom | | | **0 strict / 5 if OD-10 deferred** | |

**Capacity verdict**: 32 points equals the 80% ceiling exactly. **OD-10 is the named pressure-relief valve** — if any story expands during Development, OD-10 is dropped (FR-12 explicitly permits this) and the sprint settles at 29 points (~73% utilization), restoring 5 points of headroom.

**Recommended execution order** (respects dependency graph and minimizes in-sprint merge churn):

1. **Foundation block**: OD-01 → OD-04 → OD-03 (config schema and migration narrative locked first)
2. **SKILL.md block** (single continuous edit session on SKILL.md to avoid merge churn): OD-05 → OD-02 → OD-06 → OD-08
3. **Reference docs block**: OD-09, OD-11, OD-12 (parallel-safe; different files)
4. **Hook block**: OD-07 (code; depends on OD-04 + OD-05 finalized)
5. **Optional**: OD-10 (only if hook block came in under estimate)
6. **Doc parity sweep**: OD-13 (last; catches any stragglers)

---

## Test Coverage Audit (FRs and NFRs → test cases)

Per memory lesson: **test cases must cover ALL FRs explicitly**. This table proves coverage.

| FR / NFR | Story | Test cases |
|---|---|---|
| FR-01 | OD-01, OD-04 | OD-01-T1/T2/T3, OD-04-T1/T2 |
| FR-02 (a) | OD-04 | OD-04-T3 |
| FR-02 (b) | OD-03 | OD-03-T2 |
| FR-02 (c) | OD-03 | OD-03-T3 |
| FR-03 | OD-02 | OD-02-T1/T2/T3/T5 |
| FR-04 | OD-01 | OD-01-T1 |
| FR-05 | OD-01, OD-02 | OD-01-T3, OD-02-T4 |
| FR-06 | OD-05 | OD-05-T1/T2 |
| FR-07 | OD-06 | OD-06-T1/T2/T3/T4 |
| FR-08 | OD-05 | OD-05-T3/T4/T5 |
| FR-09 (a) | OD-07 | OD-07-T1/T2/T3 |
| FR-09 (b) | OD-07 | OD-07-T4 |
| FR-09 (c) | OD-07 | OD-07-T5 |
| FR-09 (d) | OD-07 | OD-07-T6 |
| FR-09 (e) | OD-07 | OD-07-T7 |
| FR-10 | OD-08 | OD-08-T1/T2/T3 |
| FR-11 | OD-09 | OD-09-T1/T2/T4/T5 |
| FR-12 | OD-10 | OD-10-T1/T2/T3/T4 |
| FR-13 | OD-11 | OD-11-T1..T7, T9, T10, T11 |
| FR-14 | OD-12 | OD-12-T1/T2/T3/T4 |
| FR-15 | OD-04, OD-11, OD-12 | OD-04-T4, OD-11-T8, OD-12-T2 |
| FR-16 | OD-13 | OD-13-T1/T2/T3/T4/T5 |
| NFR-01 | OD-07 | OD-07-T8 |
| NFR-02 | OD-07, OD-10 | OD-07 stdlib-only ACs, OD-10-T6 |
| NFR-03 | OD-04 | OD-04-T5 |
| NFR-04 | OD-13 | OD-13-T5 |
| NFR-05 | OD-07, OD-10 | OD-07-T11, OD-10-T5 |
| NFR-06 | (process — dogfood the bundle itself) | Validated by completion of this pipeline run |
| NFR-07 | (process — load plugin-dev skills) | Validated at developer-stage DoD |
| NFR-08 | OD-13 | OD-13-T5 (atomic merge via single-PR check) |

**Coverage**: 16/16 FRs and 8/8 NFRs have explicit test cases or documented process validation.

---

## Open Questions — Disposition in This Plan

| OQ / PQ | Disposition |
|---|---|
| OQ-1 | Resolved in PRD FR-09 + ADR-001. Implemented by OD-07 layered detection. |
| OQ-2 | Captured in OD-10 note. Story is MAY; first pressure-relief drop. |
| OQ-3 | OD-02 / OD-04 — deprecation banner appears in **both** stage banner and `state.md` run log. |
| OQ-4 | OD-06 acceptance criterion #5. |
| OQ-5 | Per ADR-003 and OD-11: dogfood Architect stage MUST demonstrate at least one full loop iteration. Captured as a Stage-4 expectation, not a separate story. |
| OQ-6 | OD-13 acceptance criterion #3 and OD-13-T6. |
| OQ-7 | Quality stage decision; recommend `delivery-team/tests/fixtures/legacy-v2.6-config.yml` per architecture PQ-2. Not blocking story commit. |
| PQ-1 | OD-07 acceptance criterion #1 orders Layer 1 → Layer 2 → Layer 3. Layer 1 is load-bearing; Layer 2 is best-effort. |
| PQ-2 | Captured in OQ-7 disposition above. |
| PQ-3 | OD-03 acceptance criterion #1 locks the assumption: enum matches Phase 1 detection vocabulary. |

---

*"Thirteen stories. Thirty-two points. One sprint. One PR. The road is laid; we have only to walk it — and to delegate every step to a sub-agent, lest we trip over our own discipline."*

— Gandalf, PO

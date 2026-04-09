# User Stories — Configurable Architecture Board Review Pattern

*Voice: Gandalf the Grey, Product Owner. Run: run-2026-04-08-b2c7.*
*"A wizard chooses his council with care — and so shall we choose our reviewers."*

## Capacity Declaration

- **Velocity baseline:** 4 pts/sprint (markdown-tier; code work would be 5)
- **Sprint ceiling:** 4 pts (80% target)
- **Hard cap:** 5 pts (never exceed)
- **DoD iteration ceiling:** 3 rounds
- **Work nature:** 100% markdown/schema edits + one dogfood run — tier-lower estimates applied
- **Total committed:** 7 stories, 13 pts, 4 sprints
- **Forbidden vocabulary (per constraints.yml):** lambda, ecr, sqs, ec2, s3, dynamodb, kafka, python, node, typescript, golang — NONE appear in any story, AC, or artifact path below
- **Amendments from Architect sequencing (merged here — per plan.md memory lesson):** US-1 schema IS the *interface contract* for US-4 and US-5; US-2 and US-3 collapse to a single authoritative file (architecture-board-personas.md) to avoid split-source drift; US-7 dogfood explicitly defers NFR-1 token measurement to UAT.

---

## US-1 — `architecture_board` config block schema

**As the** Orchestrator
**I want** a documented `architecture_board` block in `config-schema.md`
**So that** humans can declare board composition per run without code edits.

**Estimate:** 2 pts (markdown + schema doc)
**Dependencies:** none (leaf)
**FR traceability:** FR-1
**Contract role:** This story's documented field names ARE the interface contract consumed by US-4, US-5, and US-7. Any field rename cascades.

**Acceptance Criteria:**
1. `delivery-team/skills/delivery-flow/references/config-schema.md` contains a new top-level optional block `architecture_board` with fields: `enabled` (bool, default false), `reviewers` (list[str]), `max_iterations` (int, ≤3), `convergence` (enum: `all-done` | `judge-pass` | `majority-pass`), `judge` (str), `cross_persona_iteration2` (bool) → **FR-1**
2. Schema version bumped per extension protocol → **FR-1**
3. `validate_config.py` accepts a config with the block enabled AND a config without the block → **FR-1, NFR-2**
4. Block documented as optional; absence = disabled (default) → **NFR-2**

**DoD:**
- [ ] Schema doc updated, version bumped
- [ ] Forbidden vocab grep clean
- [ ] Validator passes enabled and absent configs
- [ ] Architect endorses field names match ADR-001

---

## US-2 — Reviewer persona library (≥3 starter personas)

**As a** reviewer sub-agent
**I want** a curated persona library file with my id, perspective, context files, review prompt, and gate criteria
**So that** I can load only my own slice and emit a review without cross-contamination.

**Estimate:** 2 pts
**Dependencies:** US-1 (field `reviewers` references these persona ids)
**FR traceability:** FR-2, FR-3

**Acceptance Criteria:**
1. File `delivery-team/skills/delivery-flow/references/architecture-board-personas.md` exists → **FR-2**
2. File contains ≥3 H2 persona sections: `volatility-architect`, `ddd-architect`, `risk-architect` → **FR-2**
3. Each persona declares: `id`, `name`, one-line `perspective`, `context-files-to-load` list, `review-prompt-template`, `gate-criteria`, `signal-format` → **FR-3**
4. No two personas share the same `perspective` one-liner (R1 mitigation) → **FR-3**
5. Volatility Architect `gate-criteria` cites Lowy's Golden Rule → **FR-3**

**DoD:**
- [ ] Structure matches ADR-001 / architecture.md §3
- [ ] Persona ids match the example list in config-schema.md (from US-1)
- [ ] Forbidden vocab grep clean
- [ ] Architect endorses persona distinctness

---

## US-3 — Judge persona spec + synthesis protocol (same library file)

**As the** Orchestrator
**I want** a judge persona with a cite-synthesize-verdict protocol in the same library file
**So that** N reviews synthesize into a single verdict that cannot devolve into an echo chamber.

**Estimate:** 2 pts
**Dependencies:** US-2 (same file — prevents split-source drift)
**FR traceability:** FR-4

**Acceptance Criteria:**
1. Same file contains `## chief-architect (judge)` H2 section → **FR-4**
2. Section declares 6 protocol steps: Load, Cite-per-finding, Declare alignment (AGREE/DISAGREE/DEFER), Synthesize, Emit verdict, Persist → **FR-4** (ADR-002)
3. Verdict schema: `VERDICT` (PASS | CONDITIONAL | BLOCK), `SYNTHESIZED_FINDINGS[]`, `DISSENT[]`, `CITATIONS[]` → **FR-4**
4. Deadlock rule explicitly links to `team-patterns.md` Pattern 4 Debate DEADLOCK handler (no new mechanism) → **FR-4**
5. Output path documented: `.delivery/artifacts/04-architect/board/judge-verdict.md` → **FR-4, FR-5**

**DoD:**
- [ ] Protocol matches ADR-002 on all 6 steps
- [ ] Deadlock link resolves
- [ ] Forbidden vocab grep clean

---

## US-4 — `architecture-board` pattern in team-patterns.md

**As a** pipeline orchestrator reader
**I want** a new Pattern 3b entry documenting the configurable board protocol
**So that** the pattern is discoverable alongside Pattern 3 without replacing it.

**Estimate:** 2 pts
**Dependencies:** US-1 (consumes config contract), US-2, US-3
**FR traceability:** FR-5

**Acceptance Criteria:**
1. `team-patterns.md` contains new section **Pattern 3b: Configurable Architecture Board** inserted after Pattern 3 → **FR-5**
2. Pattern documents: trigger (`architecture_board.enabled`), parallel dispatch, per-reviewer isolation (NFR-3), output paths `.delivery/artifacts/04-architect/board/<persona-id>-review.md` + `judge-verdict.md`, iteration loop honoring `convergence` and `max_iterations` → **FR-5**
3. Pattern 3 (fixed) is byte-untouched → **NFR-2**
4. Pattern cross-links to US-1 config block and US-2/US-3 persona library → **FR-5**

**DoD:**
- [ ] New section present, Pattern 3 unchanged
- [ ] Forbidden vocab grep clean
- [ ] Architect endorses protocol matches architecture.md §5

---

## US-5 — Stage 4 Architect integration in pipeline-stages.md

**As the** Stage 4 orchestrator
**I want** a conditional board-dispatch sub-step after the primary architect produces `architecture.md`
**So that** boards run automatically when enabled and are invisible when disabled.

**Estimate:** 2 pts
**Dependencies:** US-1 (config contract), US-4 (pattern to reference)
**FR traceability:** FR-6, NFR-2

**Acceptance Criteria:**
1. `pipeline-stages.md` Stage 4 contains a new sub-step **2b. Architecture Board Review** inserted after Invoke Architect and before Team DoD Validation → **FR-6**
2. Sub-step conditional on `architecture_board.enabled` — absent/false = skip silently → **NFR-2**
3. Sub-step references Pattern 3b (US-4) and the judge verdict artifact path → **FR-6**
4. On BLOCK verdict, orchestrator enters self-correction loop against primary architect → **FR-6**

**DoD:**
- [ ] Step inserted at correct location
- [ ] Backwards-compat wording explicit
- [ ] Forbidden vocab grep clean

---

## US-6 — MAR iteration-2 cross-persona routing

**As the** Stage 4 orchestrator
**I want** iteration 2 of self-correction to route to a *different* reviewer persona
**So that** the corrected architecture is examined by fresh eyes (MAR paper technique; absorbs BACKLOG-002).

**Estimate:** 1 pt
**Dependencies:** US-4, US-5
**FR traceability:** FR-7

**Acceptance Criteria:**
1. Pattern 3b documents iteration-2 routing: on round 2, select a different persona from `reviewers` (round-robin skipping the round-1 BLOCK reviewer) → **FR-7**
2. Behavior disabled by `cross_persona_iteration2: false` → **FR-7, NFR-2**
3. BACKLOG-002 referenced in a "supersedes" note → **FR-7**

**DoD:**
- [ ] Routing rule documented and testable
- [ ] Forbidden vocab grep clean

---

## US-7 — Dogfood the board on this run's Stage 4

**As the** PO (Gandalf)
**I want** to run the new board retroactively against `run-2026-04-08-b2c7` Stage 4 with ≥3 reviewers
**So that** we validate the capability on the very pipeline that introduced it.

**Estimate:** 2 pts
**Dependencies:** US-1..US-6 all DONE
**FR traceability:** FR-8, NFR-1 (deferred to UAT), NFR-3

**Acceptance Criteria:**
1. `.delivery/config.yml` temporarily enables `architecture_board` with `reviewers: [volatility-architect, ddd-architect, risk-architect]`, `judge: chief-architect`, `max_iterations: 2` → **FR-8**
2. Dogfood produces ≥3 distinct review artifacts at `.delivery/artifacts/04-architect/board/<persona-id>-review.md` → **FR-8, PRD AC-7**
3. One `judge-verdict.md` persisted with cite-synthesize-verdict structure → **FR-8**
4. Reviewer prompt audit hook confirms no cross-contamination → **NFR-3**
5. Backwards-compat sanity: a second run with the block removed completes error-free → **NFR-2, PRD AC-9**
6. Token overhead measurement **deferred to UAT stage** with explicit note in dogfood report — NOT a blocker for Plan DONE → **NFR-1 (deferred)**

**DoD:**
- [ ] 3 review artifacts + 1 verdict persisted
- [ ] Backwards-compat run green
- [ ] UAT deferral note present
- [ ] Forbidden vocab grep clean across all dogfood artifacts

---

*"Three voices, one verdict, and the wisdom to know which to heed."* — G.

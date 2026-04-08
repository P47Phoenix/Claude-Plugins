# UAT Test Cases — Orchestration Discipline Bundle

**QA**: Legolas
**Plan**: `./test-plan.md`
**Style**: Given/When/Then. Static-review cases use `grep`/file inspection; dynamic cases pipe synthetic JSON to hook scripts.

Legend: **P0** ship-blocker, **P1** must-fix-before-merge, **P2** log-only.

---

## Category 1 — Config migration (FR-01, FR-02, FR-16, NFR-03)

### TC-01 (P0) — `project_type` removed from active schema table
- **Given** `delivery-team/skills/delivery-flow/references/config-schema.md`
- **When** `grep -nE '^\| *.project_type' references/config-schema.md` is run
- **Then** no row in the active schema table contains `project_type`; the only matches must live under "Deprecated Keys" or "Version History".

### TC-02 (P0) — `config_version` bumped to 2.7
- **Given** the config-schema markdown
- **When** the "Current Version" line is read
- **Then** it equals `2.7`; the Config File Template example also declares `config_version: "2.7"`.

### TC-03 (P0) — Deprecated Keys section exists
- **Given** the config-schema markdown
- **Then** a "Deprecated Keys" section exists above Version History documenting warn-and-drop migration for `project_type` and the `enforce_self_write_block` default.

### TC-04 (P0) — `routing.force_type` row exists
- **Then** the active schema table contains `routing.force_type` (optional, default null) and `pipeline.enforce_self_write_block` rows.

### TC-05 (P0) — `config-schema.json` regenerated from v2.7 markdown
- **Given** the schema generator
- **When** `python3 delivery-team/scripts/generate-schema.py` is run
- **Then** exit code 0; resulting `config-schema.json` declares `config_version` 2.7 and contains no `project_type` key in the active schema; git diff against committed JSON is empty.

### TC-06 (P0) — Tolerant parse of legacy v2.6 config
- **Given** a synthetic `.delivery/config.yml` with `config_version: "2.6"` and bare top-level `project_type: GREENFIELD`
- **When** the orchestrator reads it (per SKILL.md Phase 0 directive)
- **Then** parsing succeeds; `enforce_self_write_block` defaults to `false`; a deprecation banner is emitted to `.delivery/state.md` AND the stage banner. (Doc-verified — repo has no test runner.)

---

## Category 2 — Phase 1 always-detect (FR-03)

### TC-07 (P0) — Phase 0 no longer references skipping Phase 1
- **When** `grep -n 'Skip Phase 1' delivery-team/skills/delivery-flow/SKILL.md` is run
- **Then** zero matches.

### TC-08 (P0) — Phase 1 header asserts every-invocation semantics
- **Then** the Phase 1 header note in SKILL.md contains the literal phrase "every pipeline invocation" and the sentence "Project type is a runtime routing decision, not a config setting."

### TC-09 (P1) — Two consecutive runs with different requests route differently
- **Given** the same repo with no `routing.force_type` set
- **When** run A asks for "fix the off-by-one in foo.py" and run B asks for "design a new analytics pipeline"
- **Then** A is routed BUG_FIX and B is routed GREENFIELD/FEATURE; routing decisions are recorded in `.delivery/state.md` per run, never in `config.yml`. (Dogfood-verifiable.)

---

## Category 3 — `routing.force_type` override (FR-02, FR-05)

### TC-10 (P0) — `routing.force_type` honored
- **Given** `.delivery/config.yml` containing `routing: { force_type: DOCS_ONLY }`
- **When** the orchestrator runs against an arbitrary feature request
- **Then** routing uses DOCS_ONLY; Phase 1 detection still runs and is logged; the stage banner contains "project_type forced to DOCS_ONLY by routing.force_type — detection result was <Y>".

### TC-11 (P0) — Both keys present: `routing.force_type` wins
- **Given** a v2.6-then-tolerantly-parsed config with both bare `project_type: GREENFIELD` AND `routing.force_type: DOCS_ONLY`
- **Then** routing is DOCS_ONLY; deprecation log line still emitted for the bare key.

### TC-12 (P1) — `project-types.md` reframes detection as runtime
- **Then** `references/project-types.md` opens with a block stating runtime detection is mandatory in v2.7+, the `project_type` config key was removed, and `routing.force_type` is the only supported pin (references ADR-002).

---

## Category 4 — Delegation enforcement (FR-06, FR-07, FR-08)

### TC-13 (P0) — Delegation Prime Directive section exists
- **Then** SKILL.md contains a section named "Delegation Prime Directive" placed early in the file, naming the directive explicitly.

### TC-14 (P0) — Five anti-patterns enumerated in Core Principle 1
- **Then** Core Principle 1 lists exactly the five anti-patterns from OD-03: simple writes, compound multi-role prompts, collapsed adversarial loops, artifact content forwarding, inline drafting.

### TC-15 (P0) — Permitted write paths enumerated
- **Then** the Prime Directive enumerates the orchestrator's only permitted write paths: `state.md`, `state.tmp.md`, `config.yml`, `memory/**`, `stage-summary.md`.

### TC-16 (P0) — Step 4.5 rejection clause + rejected justifications
- **Then** Step 4.5 contains a "Rejected justifications" sub-section that names: "but it's simple", "I already know the answer", "faster if I do it", "no sub-agent exists", and the escalation rule (escalate to user, do not self-write).

### TC-17 (P0) — Common Orchestrator Anti-Patterns section
- **Then** SKILL.md contains a top-level "Common Orchestrator Anti-Patterns" section between Stage Definitions and Team DoD Protocol, with **8** numbered anti-patterns (per OD-06 dev notes; FR-08 minimum was 6 — exceeding minimum is acceptable).
- **And** each entry has a name, one-line description, and correct alternative.

### TC-18 (P1) — Cross-references intact
- **Then** Step 4.5 references the Anti-Patterns section by name; the Prime Directive section is referenced from at least three downstream sections (search SKILL.md for "Delegation Prime Directive" — expect >=4 occurrences total).

---

## Category 5 — Origin detection layers (FR-09, NFR-02, NFR-05)

### TC-19 (P0) — Module docstring documents layered strategy + 3 known gaps
- **Then** `delivery-team/hooks/enforce_pipeline_scope.py` module docstring describes Layer 1 (env var), Layer 2 (hook-input metadata), Layer 3 (soft-deny default), and explicitly lists three gaps: Bash redirection bypass, Layer 2 metadata drift, missing env-var injection.

### TC-20 (P0) — Layer 1 env var detection (CLAUDE_AGENT_ID)
- **Given** stdin JSON for a Write tool call to `.delivery/artifacts/02-refine/po/prd.md` with env `CLAUDE_AGENT_ID=po`
- **When** the hook is executed
- **Then** exit code 0 with no systemMessage warning emitted (sub-agent attribution succeeds at Layer 1).

### TC-21 (P0) — Layer 1 env var detection (DELIVERY_FLOW_AGENT_CONTEXT)
- Same as TC-20 but with `DELIVERY_FLOW_AGENT_CONTEXT=architect`. **Then** allowed.

### TC-22 (P0) — Allowlist coverage
- **Given** orchestrator-attributed Write attempts (no env var, no metadata) to each path:
  - `.delivery/state.md`
  - `.delivery/state.tmp.md`
  - `.delivery/config.yml`
  - `.delivery/memory/foo.md`
  - `.delivery/state-archive/2026/run.md`
  - `.delivery/defects/D-01.md`
  - `.delivery/features/F-01.md`
  - `.delivery/aliases/legolas.md`
  - `.delivery/artifacts/02-refine/stage-summary.md`
  - `.delivery/artifacts/02-refine/state.md`
- **Then** every call exits 0 with no soft-deny systemMessage. Allowlist must not over-block routing files.

### TC-23 (P0) — Activation gate (v2.6 vs v2.7)
- **Given** orchestrator-attributed write to `.delivery/artifacts/02-refine/po/prd.md`
  - Case A: `config_version: "2.6"` (or absent) → soft-deny **does not fire** (activation gated off).
  - Case B: `config_version: "2.7"` AND `pipeline.enforce_self_write_block: true` → soft-deny systemMessage **fires** naming the Delegation Prime Directive.
- **Then** both cases exit 0 (never blocks). Behavior matches `_activation_gated` semantics.

### TC-24 (P1) — Layer 2 metadata fallback
- **Given** stdin JSON containing `parent_tool_use_id` (or `context.parent_tool_use_id` or `frame.is_subagent: true`) and no env var
- **Then** treated as sub-agent origin; no soft-deny systemMessage.

### TC-25 (P0) — NFR-05 graceful degradation
- **Given** malformed JSON on stdin
- **Then** hook exits 0 (try/except wrapper); no traceback to stderr that would be interpreted as a block.

---

## Category 6 — One-role-per-sub-agent (FR-10, FR-11, FR-12)

### TC-26 (P0) — "One Role = One Sub-Agent" rule block in SKILL.md
- **Then** SKILL.md contains a prominent rule block titled "One Role = One Sub-Agent" immediately above "Two-Channel Communication", with worked examples (review board=3, DoD=4, debate=PRO+CON+JUDGE, adversarial loop=N) and a violations list.

### TC-27 (P0) — Dispatch rule on every collaboration pattern
- **Then** `references/team-patterns.md` opens each of these patterns with a "Dispatch rule:" line: Evaluator-Optimizer, Adversarial Review, Multi-Perspective Review Board, Decision Ownership Routing, Debate, Consensus.

### TC-28 (P0) — `quality-gates.md` validator rule
- **Then** `references/quality-gates.md` contains "One validator = one Agent invocation" immediately after the DoD Validator Prompt Template, plus a new "Delegation Meta-Gate" section, plus a "Known Hook Limitations" section mirroring the hook docstring gaps.

### TC-29 (P0) — `audit_agent_prompt.py` compound-role detection
- **Given** synthetic prompts:
  - (a) two `ROLE:` headers → warning fires.
  - (b) "also act as architect" without negation → warning fires.
  - (c) "do not act as both developer and reviewer" → warning **suppressed** by `_NEGATION_RE` (M-05 fix).
  - (d) two `You are X` declarations within 200 chars → warning fires.
  - (e) clean single-role prompt → no warning.
- **Then** behavior matches all five expectations; warnings are non-blocking (exit 0) and reference "One Role = One Sub-Agent".

### TC-30 (P1) — `pipeline-stages.md` header note
- **Then** `references/pipeline-stages.md` contains the header note that `[PARALLEL]`/`[SEQUENTIAL]` annotations imply one Agent tool call per role and never combine roles.

### TC-31 (P1) — Stdlib-only NFR
- **When** `grep -nE '^import |^from ' delivery-team/hooks/audit_agent_prompt.py delivery-team/hooks/enforce_pipeline_scope.py`
- **Then** every import is a stdlib module; no third-party packages.

---

## Category 7 — Isolated Adversarial Loop (FR-13, FR-14, FR-15)

### TC-32 (P0) — Pattern 2b exists
- **Then** `team-patterns.md` contains a "Pattern 2b: Isolated Adversarial Loop" section immediately after Pattern 2.

### TC-33 (P0) — Core guarantee documented
- **Then** the section asserts fresh sub-agent dispatch every loop with no prior-loop context leak.

### TC-34 (P0) — Issue class taxonomy enumerated
- **Then** the taxonomy lists exactly: `coupling`, `security`, `data-integrity`, `naming`, `testability`, `performance`, `docs`, plus the `misc` fallback for untagged findings.

### TC-35 (P0) — Three convergence rules per ADR-003
- **Then** the section documents all three rules: (a) Two-clean, (b) No-new-classes (last 2 loops produced same-class only), (c) Hard cap (`max_self_correction`, default 3, exit `cap_reached`).

### TC-36 (P0) — Pseudocode protocol present and verified
- **Given** the pseudocode block in Pattern 2b
- **Then** it covers: fresh sub-agent dispatch, class tracking across loops, architect revision with current-loop findings only, cap-reached as documented exit, and an explicit "N=1 does not exit" invariant.

### TC-37 (P0) — Stage 4 references the loop
- **Then** `pipeline-stages.md` Stage 4 (Architect) section replaces the single Adversarial Review step with the Isolated Adversarial Loop, naming ADR-003 and the loop artifact paths; loop count bounded by `max_self_correction`. `config-schema.md` v2.7 documents `max_self_correction` listing "Architect adversarial loop cap" as one of its uses (FR-15).

---

## Category 8 — Documentation parity (FR-16, NFR-04)

### TC-38 (P0) — `CLAUDE.md` updated
- **Then** CLAUDE.md schema reference says v2.7; "Setup wizard" mentions 9 questions; project-type detection described as per-run.

### TC-39 (P0) — `README.md` and `delivery-team/README.md`
- **Then** both READMEs say "Setup wizard … 9 questions … runtime detection"; `delivery-team/README.md` additionally mentions schema v2.7 and `routing.force_type`.

### TC-40 (P0) — `marketplace.json` version bump
- **Then** `.claude-plugin/marketplace.json` reports version `2.18.0` (or higher) and the bump is git-traceable to OD-13.

### TC-41 (P0) — `docs/user-guide/config.md` migrated
- **Then** schema banner v2.7; v2.7 migration note present; `project_type` row replaced by `routing.force_type`; YAML example uses `routing.force_type: null` and `config_version: "2.7"`.

### TC-42 (P0) — `docs/skills/delivery-flow.md` and `docs/contributing/index.md`
- **Then** delivery-flow doc's key-settings table references `routing.force_type` (Phase 1 always-detect note); contributing doc points at v2.7 schema source-of-truth.

### TC-43 (P1) — Live-vs-historical `project_type` grep sweep
- **When** `grep -rn 'project_type' delivery-team/ docs/ CLAUDE.md README.md .claude-plugin/marketplace.json`
- **Then** every match is in: Deprecated Keys section, Version History, ADR migration notes, hook compatibility code, or this UAT artifact. Zero live config-driven references in user-facing docs.

---

## Category 9 — Dogfooding self-test (NFR-06)

### TC-44 (P0) — Pipeline run executed end-to-end through delivery-flow
- **Given** this very pipeline run for the OD bundle
- **Then** `.delivery/state.md` shows all 7 stages traversed (Idea → UAT) with no skipped light stages.

### TC-45 (P0) — Zero unauthorized orchestrator self-writes to artifact paths
- **When** the git history of `.delivery/artifacts/**` for this run is inspected
- **Then** every artifact file (PRD, design, architecture, plan, dev notes, this UAT plan/cases) was authored by a dispatched sub-agent (per the agent invocation template). Orchestrator-authored writes appear only at allowlisted routing paths (`state.md`, `state.tmp.md`, `stage-summary.md`, `config.yml`, `memory/**`).
- **Note**: activation gate is the v2.6→v2.7 transition; this run executes under the transition window. Documented exemption is acceptable, but the discipline must be visible in retro.

### TC-46 (P1) — Adversarial loop demonstrated at Architect
- **Then** `.delivery/artifacts/04-architect/` contains evidence of at least one Isolated Adversarial Loop iteration (a loop artifact, fresh-reviewer dispatch trace, or convergence marker). FR-13 is testable as documentation; full N>=2 demonstration is encouraged but not strictly required (per OQ-5).

---

## Category 10 — Shared-module SKILL.md review

### TC-47 (P0) — Structural ordering of SKILL.md
- **Then** the document order is: metadata → Delegation Prime Directive → Core Principles (incl. anti-pattern list and permitted paths) → One Role = One Sub-Agent rule → Two-Channel Communication → Phase 0 → Phase 1 → … → Stage Definitions → Common Orchestrator Anti-Patterns → Team DoD Protocol → … → references list. Verifies FR-06/FR-08/FR-10 placement assertions.

### TC-48 (P0) — Config table updated
- **Then** the SKILL.md config table contains rows for `routing.force_type` and `pipeline.enforce_self_write_block`, and no row for `project_type`.

### TC-49 (P0) — Wizard count single source of truth
- **When** `grep -nE '[0-9]+ wizard questions|[0-9]+ questions' delivery-team/skills/delivery-flow/SKILL.md`
- **Then** every match says **9** (line 1051 fix verified; no stale "10" or "8" or "down from 10/9" mismatch).

### TC-50 (P1) — No cross-plugin SKILL.md anchor breakage
- **When** `grep -rn 'delivery-flow/SKILL.md#' delivery-team/ docs/`
- **Then** every cross-reference resolves to a section heading that still exists post-rewrite.

---

## Traceability Matrix

| FR / NFR | Test cases |
|----------|-----------|
| FR-01 | TC-01, TC-05 |
| FR-02 | TC-03, TC-04, TC-06, TC-10, TC-11 |
| FR-03 | TC-07, TC-08, TC-09 |
| FR-04 | TC-49, TC-39 |
| FR-05 | TC-12, TC-43 |
| FR-06 | TC-13, TC-14, TC-15, TC-18, TC-47 |
| FR-07 | TC-16 |
| FR-08 | TC-17, TC-18 |
| FR-09 | TC-19, TC-20, TC-21, TC-22, TC-23, TC-24, TC-25 |
| FR-10 | TC-26, TC-47 |
| FR-11 | TC-27, TC-28, TC-30 |
| FR-12 | TC-29 |
| FR-13 | TC-32, TC-33, TC-34, TC-35, TC-36, TC-46 |
| FR-14 | TC-37 |
| FR-15 | TC-37 |
| FR-16 | TC-02, TC-38, TC-39, TC-40, TC-41, TC-42, TC-43 |
| NFR-02 | TC-31 |
| NFR-03 | TC-06, TC-23 |
| NFR-04 | TC-38..TC-43 |
| NFR-05 | TC-25 |
| NFR-06 | TC-44, TC-45, TC-46 |

---

*"Fifty arrows. Fifty marks. The wind is steady, and the bow is true."* — Legolas

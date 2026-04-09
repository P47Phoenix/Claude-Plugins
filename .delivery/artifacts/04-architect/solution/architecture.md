# Architecture — Paired Constraints Primitive (`constraints.yml`)

**Stage**: 4 (Architect) | **Role**: Solution Architect (Celebrimbor) | **Mode**: LIGHT
**Feature**: Paired Constraints Primitive | **Date**: 2026-04-08
**Pipeline ID**: run-2026-04-08-a1f3

> *"Let us forge something that will endure beyond the ages. A ring of plain iron, that its bearers may remember what they swore."*

---

## 1. Context

The PRD names a single root cause: *"constraints known but not structured, and therefore not consumed"* (`.delivery/artifacts/02-refine/po/prd.md:23`). Plan stage drifts at 57% first-try pass because the knowledge earned at Refine and Architect stages has no canonical vessel. This architecture forges that vessel — `constraints.yml` — as the smallest durable primitive the Business Rules Engine can mechanically enforce. I build nothing baroque. A ring of plain iron.

## 2. Resolved Open Questions (Galadriel's Handoff)

The Lady of the Mirror posed four questions at `.delivery/artifacts/03-design/ux/information-architecture.md:102-108`. I answer each with a ruling and a reason.

**Q1 — `forbidden_vocabulary` inheritance vs. restatement.**
*Ruling*: **Restated per file. The shared token list lives canonically in `constraints-model-guide.md`.** Authors copy it from the template; the template embeds the canonical list verbatim. Rationale: glance-ability at human checkpoint must win — a reviewer opening a single `constraints.yml` must see the full fence without cross-referencing the guide. DRY is honored at authoring time (via template), not at runtime. Drift is prevented by a DoD check that diffs the file's list against the guide's canonical list.

**Q2 — `citations` as free-form vs. structured.**
*Ruling*: **Structured `{work, chapter, page}` object form.** Rationale: rule-checkability outranks prose-scannability. A DoD validator must be able to assert *"a citation to Löwy's Golden Rule (Righting Software, Ch. 2) exists"* without natural-language inference. Free-form prose cannot be mechanically verified. The structured form costs three keys per citation — a tolerable burden against the certainty it buys.

**Q3 — Architect constraints file location.**
*Ruling*: **Architect writes a sibling file at `.delivery/artifacts/04-architect/solution/constraints.yml`, NOT an extension of the Refine file.** Rationale: (a) stage artifact isolation is a pipeline invariant — a stage never overwrites an upstream artifact; (b) the two files answer different questions (problem constraints vs. decomposition constraints) and conflating them would blur ownership; (c) DoD validators already walk per-stage directories, and a sibling fits the existing grammar.

**Q4 — Physical field order enforcement.**
*Ruling*: **Enforced by template, not by validator.** The validator is concerned with *what must be true*, not *what must be pretty*. Field order is a scan-ability concern owned by the template (`constraints-refine.yml`, `constraints-architect.yml`). An author who reorders fields after copying from the template commits a sin against their future self but not against the gate.

## 3. The `constraints.yml` Schema

Eight fields. No more. Each earns its keep by the presence of at least one rule-check consumer — per PRD R-1 mitigation.

| Field | YAML Type | Required | Shape | Purpose | Minimal Example |
|---|---|---|---|---|---|
| `entities` | list-of-strings | **required** | `[string]` | Domain nouns (Refine) or bounded contexts / volatility classes (Architect). | `[constraints_file, dod_validator, architect_agent]` |
| `invariants` | list-of-strings | **required** | `[string]` | Truths that must hold end-to-end. Load-bearing. | `["constraints.yml is authored before stage DoD fires"]` |
| `forbidden_vocabulary` | list-of-strings | optional | `[string]` | Tokens that must not appear in this stage's prose artifacts. Restated per file. | `[lambda, ecr, sqs, python, typescript]` |
| `numeric_ceilings` | map (string→number) | optional | `{string: number}` | Quantitative limits (budgets, counts, ratios). | `{refine_token_delta_pct: 15, max_fields: 8}` |
| `state_variables` | list-of-strings | optional | `[string]` | Observable state the pipeline mutates. | `[pipeline_stage, dod_result]` |
| `actions` | list-of-strings | optional | `[string]` | State transitions authored by this stage. | `[author_constraints, run_dod_check]` |
| `mandatory_artifacts` | list-of-strings | optional | `[string]` (paths) | Downstream files this stage promises will exist. | `[".delivery/artifacts/04-architect/solution/constraints.yml"]` |
| `citations` | list-of-objects | optional | `[{work, chapter, page}]` | Authoritative references required by invariants. | `[{work: "Righting Software", chapter: "2", page: "31"}]` |

A Refine-stage file need only satisfy `entities` + `invariants`. An Architect-stage volatility file additionally requires `citations` containing the Löwy reference (PRD AC-4).

## 4. File Locations (Canonical Paths)

- **Refine constraints** (Stage 2, PO): `.delivery/artifacts/02-refine/po/constraints.yml`
- **Architect constraints** (Stage 4, Architect): `.delivery/artifacts/04-architect/solution/constraints.yml`
- **Canonical guide**: `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`
- **Refine template**: `delivery-team/skills/delivery-flow/references/templates/constraints-refine.yml`
- **Architect template**: `delivery-team/skills/delivery-flow/references/templates/constraints-architect.yml`

## 5. New / Updated Reference Files

**NEW**
- `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` — the 8-field canon; §1 titled *"What this file is (read first)"* per IA §8.
- `delivery-team/skills/delivery-flow/references/templates/constraints-refine.yml` — domain-scoped template (FR-2).
- `delivery-team/skills/delivery-flow/references/templates/constraints-architect.yml` — decomposition-scoped template, pre-populated `forbidden_vocabulary` and Löwy citation stub (FR-3).

**UPDATED**
- `delivery-team/skills/architect/references/volatility-decomposition.md` — insert new **§0 "Löwy's Golden Rule"** BEFORE the existing Phase 1. Current file is 219 lines; insertion point is immediately after the preamble (approximately **line 8**, before the first `## Phase 1` header). §0 contains: (a) Löwy's rule verbatim, (b) structured citation to *Righting Software* Ch. 2, (c) a functional-decomposition-trap anti-pattern with before/after example. Existing Phases 1–4 and the Anti-Patterns section at line 181 remain structurally untouched.
- `delivery-team/skills/architect/references/strategic-ddd.md` — insert a new **"Decomposition Hygiene"** sidebar restating the forbidden-vocabulary rule in DDD terms (bounded contexts named in ubiquitous language, never in implementation nouns). Placed as a short repeated box at the head of each of Phases 1–4 per IA §7. Additive only.
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` — Stage 5 Plan section, insert Architect invocation as new step 2 between current **line 430** (end of PO invocation) and current **line 431** (start of QA Engineer invocation). Existing steps 2–9 renumber to 3–10. Details in §6 below.
- `delivery-team/skills/delivery-flow/references/config-schema.md` — version bump **v2.7 → v2.8**. Migration rule: legacy configs without a `constraints` block gain a soft-empty stub (`constraints: { enabled: false }`) on load; legacy runs are not gate-enforced until the producing stage emits a `constraints.yml`.
- `delivery-team/skills/delivery-flow/SKILL.md` — add minimal orchestrator awareness: at Stage 2, Stage 4, and Stage 5 kickoffs, announce the constraints file path *before* the PRD path (IA §6 friction-point mitigation). Three kickoff lines; no new control flow.

## 6. Architect in Stage 5 Plan — Integration Point

Gap 3 (`architect-examine-decomposition-gaps.md`) confirms Architect absence from Stage 5. I close it with the smallest surgical cut.

**Exact change to `delivery-team/skills/delivery-flow/references/pipeline-stages.md`:**
Insert a new sub-flow step **between current line 430 (end of step 1 PO invocation) and current line 431 (start of step 2 QA invocation)**. The new step becomes step 2; existing steps 2–9 renumber to 3–10.

```
2. **Invoke Architect (implementation sequencing)** [SEQUENTIAL after step 1] [required for FEATURE, GREENFIELD, GAME_DEV] (architect skill, task_type: implementation-sequencing)
   - SKILL: `delivery-team:architect`, TASK_TYPE: `implementation-sequencing`, ROLE: `solution`
   - Input artifacts:
     - `.delivery/artifacts/02-refine/po/prd.md`
     - `.delivery/artifacts/02-refine/po/constraints.yml`
     - `.delivery/artifacts/04-architect/solution/architecture.md`
     - `.delivery/artifacts/04-architect/solution/constraints.yml`
     - `.delivery/artifacts/05-plan/po/stories.md`
   - Output: `.delivery/artifacts/05-plan/architect/sequencing.md`
   - Light Mode (BUG_FIX, DOCS_ONLY, DESIGN): WAIVED
```

This closes PRD FR-6 and satisfies AC-5. Architect remains a *participant*, not a gate-owner, in Stage 5.

## 7. DoD Validator Deterministic Check (FR-7)

Validators mechanically check artifacts against `constraints.yml` via enumerated rules, in order. The check is trivially implementable — Gimli may build it in a single session.

1. **Load both files.** Parse `constraints.yml` (PyYAML). Identify the artifact set under the stage's output directory (`.delivery/artifacts/<stage>/**/*.md`).
2. **Run the enumerated checks:**
   - **R-REQUIRED**: `entities` and `invariants` keys present and non-empty. Fail → `FAIL — missing required field '<name>'`.
   - **R-GREP**: For each token in `forbidden_vocabulary`, run a case-insensitive whole-word grep over the artifact set. Any hit → `FAIL — forbidden token '<token>' at <path>:<line>`.
   - **R-ARTIFACTS**: For each path in `mandatory_artifacts`, assert the file exists on disk. Missing → `FAIL — mandatory artifact not found: <path>`.
   - **R-INVARIANTS-REF**: Each invariant must be referenced (by ID or substring) in at least one prose artifact under the stage's output directory. Missing → `WARN — invariant '<id>' not referenced`.
   - **R-CITATIONS** (Architect volatility runs only): assert at least one citation with `work == "Righting Software"`. Missing → `FAIL — Löwy Golden Rule citation required for volatility decomposition`.
3. **Report per-rule pass/fail** as a line table — one finding per rule per offender. No prose inference. Business Rules Engine philosophy honored end to end.

Complexity: O(n·m) where n = artifact bytes, m = forbidden-vocabulary token count (≤30). At realistic artifact sizes (<200 KB per stage), gate-time cost is negligible. Token matching may be consolidated into a single compiled alternation per stage to guarantee one pass per file.

## 8. Backwards Compatibility

v2.7 configs continue to operate unchanged. On first load against v2.8 schema, missing `constraints` blocks are rehydrated to `constraints: { enabled: false }` in-memory (no file rewrite). When `enabled: false`, validators skip all constraints rule checks and emit a single informational line: `constraints.yml: SKIPPED (legacy pipeline)`. A legacy pipeline that later authors its own `constraints.yml` auto-upgrades on that stage only — the file's presence is itself the opt-in. This preserves PRD NFR-3 and NFR-4.

## 9. Non-Goals (Honest)

- **Does not solve the architecture board pattern** — BACKLOG-003 consumes this primitive rather than building it.
- **Does not solve paradigm-as-skill restructure** — BACKLOG-005 is XL, must run its own pipeline.
- **Does not provide migration tooling for old pipelines** — legacy runs carry no constraints; the soft-empty stub is the entire migration story.
- **Does not enforce constraints at orchestrator level** — enforcement lives at stage DoD gates only. The orchestrator's sole new responsibility is announcing the file path at kickoff.
- **Does not redesign the human checkpoint UI** — Galadriel's IA stands; this architecture serves it.

## 10. Risks (Blocking Only — LIGHT Mode)

- **R-A — Schema lock-in.** Once validators and templates bind to the 8-field shape, every addition risks breakage. *Mitigation (ADR-001 escape hatch)*: new fields admitted as **optional only**; removals require a major schema bump.
- **R-B — Validator performance at gate time.** Naive repeated grep becomes painful beyond ~1 MB per stage. *Mitigation*: single compiled alternation per stage; re-measure at Dev if gate time exceeds 2 s.
- **R-C — Token overhead breaches PRD NFR-5 (≤15% Refine delta).** Template, guide cross-read, and the new file itself consume budget. *Mitigation*: measurement required at Dev stage over the first 5 post-land runs per the PRD's A/B window. Rollback per PRD R-4.

---

## Decisions Recorded

Three ADRs accompany this architecture as locked decisions:

- **ADR-001** — `constraints.yml` schema (8 fields, YAML, optionality rules).
- **ADR-002** — Architect participation in Stage 5 Plan via `implementation-sequencing` task.
- **ADR-003** — Forbidden vocabulary as an enumerated list (not heuristic, not AI-judged).

> *"I have set my mark upon it. It will hold."*

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/04-architect/solution/architecture.md
SUMMARY: Forged the constraints.yml primitive — 8-field schema, Architect woven into Stage 5 Plan, three ADRs set in iron. Let it endure.

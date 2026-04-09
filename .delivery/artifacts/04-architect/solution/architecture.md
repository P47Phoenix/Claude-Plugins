# Architecture — Configurable Architecture Board Review Pattern

*Forged by Celebrimbor of the Gwaith-i-Mírdain, Stage 4 Architect (light). Run: run-2026-04-08-b2c7.*

## 1. Context

The existing Multi-Perspective Review Board in `delivery-team/skills/delivery-flow/references/team-patterns.md` (Pattern 3, line 334) is frozen to a fixed Technical/Business/Risk trio. PRD FR-1..FR-8 demand a configurable roster, a persona library, a judge, MAR-style iteration-2 cross-persona routing (BACKLOG-002 absorbed), and Stage 4 Architect integration — without breaking callers that know it not.

## 2. `architecture_board` Config Schema

Added to `delivery-team/skills/delivery-flow/references/config-schema.md` under a new top-level optional block. Absent block = disabled (NFR-2).

```yaml
architecture_board:
  enabled: false
  reviewers:
    - volatility-architect
    - ddd-architect
    - risk-architect
  max_iterations: 2
  convergence: all-done        # all-done | judge-pass | majority-pass
  judge: chief-architect
  cross_persona_iteration2: true
```

Ceilings: `max_iterations ≤ 3`, `len(reviewers) ≤ 6` (NFR-1 token cap).

## 3. Persona Library File Structure

Single file: `delivery-team/skills/delivery-flow/references/architecture-board-personas.md`. Each persona is one H2 section:

```
## <persona-id>
- id: volatility-architect
- name: Volatility Architect
- perspective: "Decompose along axes of change, per Lowy's Golden Rule"
- context-files-to-load:
    - delivery-team/skills/architect/references/volatility-strategy.md
    - .delivery/artifacts/04-architect/solution/architecture.md
- review-prompt-template: |
    You are the {name}. Evaluate architecture.md solely through {perspective}.
    Apply gate-criteria below. Emit signal-format verbatim.
- gate-criteria:
    - Every service boundary aligns with a volatility axis
    - No functional decomposition leakage
- signal-format: |
    VERDICT: PASS | CONDITIONAL | BLOCK
    FINDINGS: - <bullet>
    CITATIONS: - <file:line>
```

## 4. Judge Persona Structure

Same file, one H2 marked `## chief-architect (judge)`, with: synthesis protocol (cite each reviewer's findings individually; declare per-finding agreement; emit aggregated verdict), deadlock rule (links to `team-patterns.md` Pattern 4 Debate DEADLOCK), final verdict schema `{PASS | CONDITIONAL | BLOCK, synthesized_findings[], dissent[]}`. Full protocol in ADR-002.

## 5. `team-patterns.md` Augmentation

New section **Pattern 3b: Configurable Architecture Board** inserted immediately after Pattern 3 (line 416), referencing but not replacing it. Protocol:

1. Orchestrator reads `architecture_board` from config; if `enabled: false`, skip.
2. Dispatch each persona in `reviewers` as a parallel sub-agent (single message, isolated context per NFR-3).
3. Each writes `.delivery/artifacts/04-architect/board/<persona-id>-review.md`.
4. Judge sub-agent reads all N paths, writes `.delivery/artifacts/04-architect/board/judge-verdict.md`.
5. Loop per `convergence` until `max_iterations` or verdict PASS.

Triggers: Stage 4 Architect only (MVP). Loop rules: any BLOCK verdict → correction round; iteration 2 applies §7 routing.

## 6. `pipeline-stages.md` Stage 4 Integration

New sub-step **2b. Architecture Board Review** inserted after step 2 (Invoke Architect, line 355) and before Team DoD Validation. Conditional on `architecture_board.enabled`. On BLOCK, orchestrator triggers self-correction loop against the primary architect.

## 7. MAR Iteration-2 Cross-Persona Routing

On round 2 of self-correction, the orchestrator selects a *different* persona from `reviewers` (round-robin, skipping the round-1 reviewer whose BLOCK triggered correction) to review the corrected `architecture.md`. Absorbs BACKLOG-002. Disabled by `cross_persona_iteration2: false`.

## 8. Non-Goals (LIGHT)

- No changes to the existing fixed Multi-Perspective Review Board (Pattern 3 stays).
- No integration beyond Stage 4 Architect (Plan/Dev stages out of scope).
- No dynamic persona generation — library is curated Markdown.
- No automated token-budget enforcement beyond documented ceilings.

## 9. Risks (blocking only)

- **Persona echo chamber** — mitigated by FR-3 distinct `perspective` lines + reviewer-set overlap warning (deferred).
- **Judge deadlock** — fallback: invoke existing debate pattern's DEADLOCK handler in `team-patterns.md` Pattern 4.

*"A ring of three voices is stronger than a single hammer; but only if each voice sings a different note."* — C.

---

# Architecture — Architect `transformation-planning` Task Type

*Forged by Celebrimbor of the Gwaith-i-Mírdain, Stage 4 Architect (light). Run: BACKLOG-006.*
**Role:** Solution Architect | **Task:** design | **Refs:** architecture-patterns.md, adr-template.md
**PRD:** `.delivery/artifacts/02-refine/po/prd.md` | **Constraints:** `.delivery/artifacts/02-refine/po/constraints.yml`

## 1. Context

Per the PRD, the Architect skill is greenfield-only; task_types at `delivery-team/skills/architect/SKILL.md:519` assume PRD → architecture. Real work is brownfield transformation of legacy systems whose intent is lost. Structural analysis without behavioral reconstruction is blind. We forge a new `transformation-planning` task_type producing a linked, diffable AS-IS → TO-BE → Roadmap artifact set, with PO leading behavioral reconstruction and Architect leading structural work.

## 2. Sub-workflow structure

`transformation-planning` dispatches a 4-phase sub-flow. Each phase writes its artifact to disk; subsequent phases read by path (two-channel rule — no in-memory handoff).

- **Phase 1A (PO-led)** — Behavioral reconstruction from codebase evidence (tests, UI strings, endpoints, commits, docs, telemetry) → use cases.
- **Phase 1B (Architect-led)** — Structural reconstruction, Model-First AS-IS consuming 1A use cases as `actions`.
- **Phase 2 (Architect-led)** — TO-BE model in shared BACKLOG-001 schema.
- **Phase 3 (Architect-led)** — Ordered roadmap bridging AS-IS → TO-BE.

Orchestrator sequences phases; no live co-execution.

## 3. Output artifact locations (canonical)

- Phase 1A → `.delivery/artifacts/08-transform/as-is-use-cases.md`
- Phase 1B → `.delivery/artifacts/08-transform/as-is-constraints.yml`
- Phase 2  → `.delivery/artifacts/08-transform/to-be-constraints.yml`
- Phase 3  → `.delivery/artifacts/08-transform/roadmap.md`

`08-transform` sits after UAT in the pipeline. Outside a pipeline run, use standalone `transform/`.

## 4. New / updated reference files

NEW under `delivery-team/skills/architect/references/`:
- `transformation-planning.md` — master protocol; all 4 phases; legacy trigger rule; PO+Architect pairing.
- `transformation-phase-1a-behavioral.md` — evidence sources, use-case template, confidence rules, MAR persona trio.
- `transformation-phase-1b-structural.md` — Model-First mapping (use cases → actions; modules → entities; coupling → state; rules → constraints).
- `transformation-phase-2-to-be.md` — TO-BE construction on shared constraints.yml schema.
- `transformation-phase-3-roadmap.md` — roadmap template, no-big-bang check (30% threshold), independently-shippable rule.

NEW under `delivery-team/skills/delivery-flow/references/templates/`:
- `transformation-use-cases-template.md` — use-case table template.
- `transformation-roadmap-template.md` — roadmap step template.

UPDATED: `delivery-team/skills/architect/SKILL.md` — register `transformation-planning` in the software task routing table with brief description + link to master doc; add to input-contract enum at line 519.

## 5. Use-case schema (Phase 1A)

`actor`, `goal`, `preconditions`, `main_flow`, `variations`, `confidence` (high/medium/low), `evidence_citations` (list; each entry = file path + what the file shows).

## 6. Roadmap step schema (Phase 3)

`step_id`, `scope`, `ordering_rationale`, `reversibility`, `risk`, `incremental_value`, `preserved_invariants`, `estimated_subsystem_change_pct`.

## 7. Big-bang check (mechanical)

Per step: `subsystems_touched / total_subsystems_in_as_is_model` ≤ 30%. If exceeded, the step must be split. Edge case (total subsystems < 4): threshold collapses to "at most 1 subsystem per step" (see ADR-002).

## 8. MAR persona trio (Phase 1A review)

Three reviewers documented in `transformation-phase-1a-behavioral.md`:
- **Code Archaeologist** — evidence-bound, skeptical of confident claims lacking citations.
- **User Advocate** — what would an end user actually care about?
- **Skeptical Tester** — can we write a test for this use case?

This is the **second instantiation** of the architecture-board pattern shipped in BACKLOG-003 — no new collaboration pattern is introduced.

## 9. Legacy trigger rule

Phase 1A runs by default. Skip permitted only when the PO explicitly asserts trusted existing use-case documentation exists and is cited in the invocation; skipping is logged with written justification in the phase artifact header.

## 10. Non-goals (LIGHT)

No live migration execution; no automated refactoring; no paradigm-as-skill restructure (BACKLOG-005); no new collaboration pattern (reuses BACKLOG-003 architecture-board for Phase 1A review).

## 11. Risks (blocking only)

| Risk | Mitigation |
|------|-----------|
| Use-case hallucination | `evidence_citations` required per use case |
| Confidence-level gaming | ≥1 `confidence=low` forced per run |
| AS-IS→TO-BE diff too wide for ≤3 steps at 30% | Allow up to 7 steps; document if >7 required |
| PO+Architect coordination overhead | File-based handoff, not live co-execution |

*"A forge worth keeping is one whose hammer has already struck a second ring."* — C.


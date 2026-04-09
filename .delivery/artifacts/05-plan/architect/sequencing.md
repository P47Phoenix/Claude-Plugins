# Implementation Sequencing — Architecture Board Review Pattern

*Voice: Celebrimbor of the Gwaith-i-Mírdain, Architect. Run: run-2026-04-08-b2c7.*
*"Three rings, three reviewers, one verdict — forged in order lest the pattern be marred."*

## Story ↔ Architecture Mapping

| Story | Architecture ref | ADR |
|-------|------------------|-----|
| US-1 | architecture.md §2 `architecture_board` config schema | **ADR-001** (config block) |
| US-2 | architecture.md §3 persona library file structure | (library derives from ADR-001 field names) |
| US-3 | architecture.md §4 judge persona structure | **ADR-002** (cite-synthesize-verdict) |
| US-4 | architecture.md §5 `team-patterns.md` augmentation (Pattern 3b) | (pattern operationalizes ADR-001 + ADR-002) |
| US-5 | architecture.md §6 `pipeline-stages.md` Stage 4 integration | (integration point; no new ADR) |
| US-6 | architecture.md §7 MAR iteration-2 cross-persona routing | (absorbs BACKLOG-002) |
| US-7 | PRD FR-8 dogfood; exercises §5 + §6 + §7 on this run's Stage 4 | (validation, no new decision) |

Every story maps to an existing ADR or architecture section. No orphans.

## Volatility-Driven Sequencing Check

Most-volatile axis first: **config field names** (US-1) — once published, US-4/US-5/US-7 harden against them. Second axis: **persona library schema** (US-2) — once the H2 shape is authored, US-3 (judge) slots in byte-compatibly. Third axis: **pattern protocol text** (US-4). Integration and dogfood (US-5..US-7) depend on all prior surfaces being stable. Sequencing honors Lowy's Golden Rule (decompose along axes of change): US-1 → US-2 → US-3 → US-4 → US-5/US-6 → US-7. Endorsed.

## Interface Contracts

- **Contract C-1:** US-1 config field set IS the contract consumed by US-4 (pattern reads `enabled`, `reviewers`, `convergence`, `max_iterations`, `judge`, `cross_persona_iteration2`), US-5 (orchestrator reads `enabled`), and US-7 (dogfood populates them). **Any rename cascades.**
- **Contract C-2:** US-2 persona `id` field values are the string keys used in US-1 `reviewers` list and US-7 dogfood config. Reconcile at S1 DoD.
- **Contract C-3:** US-3 judge verdict schema (`VERDICT` / `SYNTHESIZED_FINDINGS` / `DISSENT` / `CITATIONS`) IS the parse contract for any future DoD integration (out of scope here, but do not break).
- **Contract C-4:** Output path template `.delivery/artifacts/04-architect/board/<persona-id>-review.md` + `judge-verdict.md` IS the artifact contract consumed by US-7 test assertions (QA T-20, T-21).

## Coordination Overhead Estimate

Four interface contracts across 7 stories = low-to-medium coordination. Mitigation: all four contracts live in two files (config-schema.md and architecture-board-personas.md) authored in S1 and S2 respectively, locking them early.

## Sprint Order Endorsement

Aragorn's sprint plan (S1: US-1+US-2, S2: US-3+US-4, S3: US-5+US-6, S4: US-7) is **endorsed**. It honors all four contracts and the volatility axis ordering. No adjustment requested.

## Amendments (already merged — consolidated dispatch)

The following amendments have been written directly into stories.md and sprint-plan.md in this same dispatch (per plan.md memory lesson — authoritative source, not just referencing docs):

1. **US-1 as interface contract** → stories.md US-1 "Contract role" line; sprint-plan.md Sequencing Rationale §1.
2. **US-2 + US-3 collapse to one file** → stories.md US-3 dependency; sprint-plan.md Risks R1.
3. **US-7 NFR-1 deferral to UAT** → stories.md US-7 AC-6; QA test-strategy.md T-24 marked DEFERRED.

No further amendments. Plan is coherent.

*"The order is set, the contracts forged. Begin."* — C.

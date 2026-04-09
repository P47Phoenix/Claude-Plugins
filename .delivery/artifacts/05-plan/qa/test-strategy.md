# Test Strategy — Architecture Board Review Pattern

*Voice: Legolas of the Woodland Realm, QA. Run: run-2026-04-08-b2c7.*
*"I can see their reviews from here — all three of them, and the judge besides."*

## Scope

Markdown/schema/doc edits + one dogfood pipeline run. No source code under test. Test methods: file-existence checks, schema validation, structural grep, integration-point grep, dogfood artifact counting, backwards-compat run, forbidden-vocab oracle.

## Traceability Matrix — FR → Test Case

| FR | AC (PRD) | Story | Test ID | Method | Oracle |
|----|----------|-------|---------|--------|--------|
| FR-1 | AC-1 | US-1 | T-01 | Grep `config-schema.md` for `architecture_board:` block with 6 fields | All 6 field names present |
| FR-1 | AC-1 | US-1 | T-02 | Run `validate_config.py` on sample config *with* block enabled | Exit 0 |
| FR-1 | NFR-2/AC-9 | US-1 | T-03 | Run `validate_config.py` on sample config *without* block | Exit 0 |
| FR-2 | AC-2 | US-2 | T-04 | File exists: `delivery-team/skills/delivery-flow/references/architecture-board-personas.md` | Path present |
| FR-2 | AC-2 | US-2 | T-05 | Grep persona H2 sections — count ≥3 with ids `volatility-architect`, `ddd-architect`, `risk-architect` | ≥3 matches |
| FR-3 | AC-2 | US-2 | T-06 | Structural grep each persona for all 7 required fields (id, name, perspective, context-files-to-load, review-prompt-template, gate-criteria, signal-format) | All present per persona |
| FR-3 | R1 | US-2 | T-07 | Distinctness check: unique `perspective` lines across personas | No duplicate |
| FR-3 | — | US-2 | T-08 | Volatility Architect gate-criteria cites Lowy's Golden Rule | String match |
| FR-4 | AC-3 | US-3 | T-09 | Grep `chief-architect (judge)` H2 in personas file | Match |
| FR-4 | AC-3 | US-3 | T-10 | Judge section contains all 6 protocol steps + verdict schema fields (VERDICT, SYNTHESIZED_FINDINGS, DISSENT, CITATIONS) | All present |
| FR-4 | AC-3 | US-3 | T-11 | Deadlock rule links to `team-patterns.md` Pattern 4 Debate DEADLOCK | Link resolves |
| FR-5 | AC-4 | US-4 | T-12 | Grep `team-patterns.md` for heading `Pattern 3b: Configurable Architecture Board` | Match |
| FR-5 | NFR-2 | US-4 | T-13 | Diff Pattern 3 section byte-identical to pre-change | Zero diff |
| FR-5 | AC-4 | US-4 | T-14 | Pattern 3b documents output paths `.delivery/artifacts/04-architect/board/<persona-id>-review.md` and `judge-verdict.md` | Both strings present |
| FR-6 | AC-5 | US-5 | T-15 | Grep `pipeline-stages.md` Stage 4 for new sub-step `2b. Architecture Board Review` | Match after Invoke Architect, before Team DoD Validation |
| FR-6 | NFR-2 | US-5 | T-16 | Sub-step text includes conditional on `architecture_board.enabled` | Match |
| FR-7 | AC-6 | US-6 | T-17 | Pattern 3b documents iteration-2 cross-persona routing rule | Match |
| FR-7 | AC-6 | US-6 | T-18 | BACKLOG-002 supersedes note present | Match |
| FR-7 | NFR-2 | US-6 | T-19 | Behavior gated by `cross_persona_iteration2: false` disable toggle | Match |
| FR-8 | AC-7 | US-7 | T-20 | Dogfood run: count files matching `.delivery/artifacts/04-architect/board/*-review.md` | ≥3 |
| FR-8 | AC-7 | US-7 | T-21 | `judge-verdict.md` exists with VERDICT + SYNTHESIZED_FINDINGS + CITATIONS headers | All present |
| NFR-3 | — | US-7 | T-22 | Agent prompt audit hook log shows zero cross-reviewer content | Log clean |
| NFR-2 | AC-9 | US-7 | T-23 | Backwards-compat run with `architecture_board` block removed → pipeline completes | Exit clean |
| NFR-1 | AC-8 | US-7 | T-24 | Token overhead measurement **DEFERRED to UAT** — test documented as deferred, not a Plan gate | Deferral note present in dogfood report |

## Forbidden-Vocabulary Oracle (per ADR-003 prior run)

Run grep over all artifacts produced by this pipeline for: `lambda`, `ecr`, `sqs`, `ec2`, `s3`, `dynamodb`, `kafka`, `python`, `node`, `typescript`, `golang`. Oracle: zero matches (case-insensitive) except in explicit "forbidden vocabulary" list contexts (constraints.yml, this test strategy table row).

| Oracle ID | Scope | Method | Pass |
|-----------|-------|--------|------|
| O-FV-1 | All 05-plan artifacts | grep -iE pattern | 0 matches |
| O-FV-2 | All persona/pattern docs from US-2..US-6 | grep -iE pattern | 0 matches |
| O-FV-3 | Dogfood artifacts (US-7) | grep -iE pattern | 0 matches |

## Deferred to UAT

- **T-24** — NFR-1 token overhead ≤25%. Requires production-scale measurement harness not in Plan scope. Dogfood run will emit token counts for baseline, but pass/fail judged at UAT.

## Entry / Exit Criteria

- **Entry:** Stage 5 Plan artifacts exist; US-1 schema finalized.
- **Exit for Plan DoD:** T-01..T-23 pass; T-24 documented as deferred; forbidden-vocab oracles O-FV-1/2 green (O-FV-3 runs at dogfood time).

*"A red arrow to the forbidden word, a green to the true finding. Aim well."* — L.

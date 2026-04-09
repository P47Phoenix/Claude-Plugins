# There and Back Again: The Constraints Primitive Chronicles

**Author**: Bilbo Baggins (Technical Writer) | **Date**: 2026-04-08
**Feature**: Paired `constraints.yml` Primitive | **Backlog**: BACKLOG-001, BACKLOG-004

> *"It's a dangerous business, Frodo, going out your door to write YAML without a schema."*

So here I sit at my little desk in Bag End, quill in hand, to tell you of a modest primitive that walked all the way to the Lonely Mountain of our Plan stage and came back with treasure: **structure for constraints we already knew but never carried.**

## What Changed

A single shared `constraints.yml` model now threads Refine and Architect stages together. Eight fields, two required, deterministic checks at every gate. The Golden Rule of volatility decomposition — Löwy's — is finally named in our references, and the Architect has at last been given a seat at the Stage 5 Plan council.

## New Files

- `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` — the authoritative 8-field guide
- `delivery-team/skills/delivery-flow/references/constraints-schema.json` — JSON Schema draft-07
- `delivery-team/skills/delivery-flow/scripts/validate_constraints.py` — headless validator (stdlib-only, PyYAML if present)
- `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py` — DoD rule-checker (forbidden-vocab, mandatory-artifact, ceilings)
- `delivery-team/skills/delivery-flow/references/fixtures/constraints-{valid,invalid-missing-entities,forward-compat}.yml`
- `.delivery/artifacts/02-refine/po/constraints.yml` — the dogfood Exhibit A
- `.delivery/artifacts/07-uat/tech-writer/user-guide.md` — authoring guide

## Behavior Changes

- Refine PO and Architect both emit a `constraints.yml` alongside prose.
- DoD validators now perform at least one **deterministic** rule check per gate (rule-based, not AI-inferred).
- Stage 5 Plan invokes the Architect between steps 1 and 3 for `implementation-sequencing`, producing `.delivery/artifacts/05-plan/architect/sequencing.md`.
- `volatility-decomposition.md` and `strategic-ddd.md` gained explicit guardrails against implementation-detail vocabulary (`lambda`, `ecr`, `sqs`, `ec2`, `s3`, `dynamodb`, `kafka`, and language names).

## Backwards Compatibility

Old configs still work, dear reader. No required `.delivery/config.yml` keys were added — the feature lives behind `experimental.constraints_model: true` for the 5-run A/B window. Schema `additionalProperties: true` allows forward-compat fields (AC-1.4). No v2.7 → v2.8 bump; that mountain waits for another day.

## Known Limitations

- **NFR-1 (Plan ≥80% first-try pass) is empirically deferred.** The target requires a 5-run post-land measurement window; only the instrumentation ships in this release. Baseline remains 57%.
- Rollback armed: if Plan first-try drops below 57% over any 3-run window, revert the flag and reopen BACKLOG-001.
- Validator forbidden-vocabulary list is enumerated, not heuristic — additions require a PRD revision.

## The Fellowship

- **Gandalf** — Product Owner (Refine, PRD author)
- **Celebrimbor** — Architect (decomposition + Stage 5 sequencing)
- **Aragorn** — Scrum Bag (plan steward)
- **Legolas** — QA Engineer (test strategy + rule checks)
- **Galadriel** — UX / Review Board
- **Gimli** — Developer (schema, validator, DoD checker)
- **Sam** — DevOps (install sync, hook wiring)
- **Bilbo** — Technical Writer (these very pages)

## Links

- BACKLOG-001 — Refine spike (root PRD driver)
- BACKLOG-004 — Decomposition depth gaps
- Authoring guide: `.delivery/artifacts/07-uat/tech-writer/user-guide.md`
- Model guide: `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`

> *"I am glad you are here with me. Here at the end of all things — and the start of the next run."*

# Release Notes — Architecture Board (run-2026-04-08-b2c7)

**Role:** Technical Writer — *Bilbo Baggins* (there and back again, with notes)
**Feature:** BACKLOG-003 (absorbs BACKLOG-002)

## What Changed

The delivery-flow pipeline now supports a configurable **Architecture Board** at Stage 4. When enabled, multiple specialist architects independently review the solution, and a judge persona issues a consolidated verdict (PASS / CONDITIONAL / FAIL).

## New Capability

- **4 board personas**: `volatility-architect`, `ddd-architect`, `risk-architect`, `chief-architect` (judge).
- **Multi-Architect Review (MAR)** cross-persona rotation pattern in `team-patterns.md`.
- **Config block** `architecture_board` in `.delivery/config.yml` (schema v2.7) with per-persona selection and judge designation.
- **Artifacts** land in `.delivery/artifacts/04-architect/board/` — one review per reviewer plus `judge-verdict.md`.

## Backwards Compatibility

**Zero impact on existing pipelines.** Default is `architecture_board.enabled: false`. Existing runs behave identically. Opt-in per project.

## Known Limitations

- **MAR rotation degenerates at n ≤ 2 reviewers** — rotation collapses to single-path review; fallback guidance is a follow-up. Flagged by judge in dogfood run.
- **Single judge is intentional for v1** — judge SPOF accepted; multi-judge consensus is a later enhancement.
- **Token overhead not yet baselined** — NFR-1 empirical measurement requires ≥3 real runs; deferred.
- **Real orchestrator dispatch is follow-up work** — v1 validates the design via dogfood artifact production; full wiring comes next.

## Fellowship Credits

Frodo (PO), Gandalf (final DoD), Aragorn (retro), Legolas (QA), Sam (release), Bilbo (notes), Boromir/Gimli/Merry/Pippin (dev), Elrond/Galadriel/Saruman (architect board).

## Tracking

- BACKLOG-003 (primary)
- BACKLOG-002 (absorbed)

— *Bilbo*

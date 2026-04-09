# Retrospective — run-2026-04-08-a1f3

**Facilitator**: Scrum Bag (Aragorn)
**Feature**: Paired Constraints Primitive (`constraints.yml`) + Architect-in-Plan (ADR-002)
**Date**: 2026-04-08

> *"A day may come when our pipelines fail us — but it is not this day. Today, we learn."*

---

## What Went Well

- **The Model-First primitive landed whole.** PRD, schema, templates, and validators rode into UAT together — no orphan artifacts, no late-binding surprises.
- **Celebrimbor, summoned into Plan (ADR-002), proved his worth on his first ride.** The live dogfood of Architect-in-Plan caught **three unpriced gaps** — schema forward-compat (AC-1.4), cache-refresh after constraints edit (AC-9.4), and S3 intra-order sequencing — before a single one touched UAT.
- **Gate-patterns memory injection continued to compound.** Pre-loaded constraints at Refine saved us from two classic PO/SM rework loops.
- **UAT stayed clean.** Fifth consecutive first-try UAT pass. The shield wall holds.
- **Adversarial review earned its keep again** — Gimli's round-2 rejection was uncomfortable but correct.

## What Didn't

- **SM self-rejection on round 2 (stale artifact).** Scrum Bag validated against a prior draft of `sprint-plan.md` whose amendments had not been re-read. Cost: one full correction round.
- **Gimli round-2 rejection — amendments not propagated.** Boundary corrections were written into `sequencing.md` but never carried into the authoritative `stories.md`. Validators quite rightly refused to infer.
- **Bilbo API overload retry.** Transient upstream 529s during Architect-in-Plan decomposition forced a retry loop. Recoverable, but noisy.
- **Stage 6 QA sweep — fixture arg-order error.** `check_dod_constraints.py` was invoked with arguments transposed (`<artifact> <constraints>` instead of `<constraints> <artifact>`). It read as a fixture-data mismatch; it was a CLI contract failure in the sweep script.

## Key Insight — The Self-Validating Capability

The live dogfood of **ADR-002 (Architect-in-Plan)** during the very pipeline that introduced it caught **three gaps before they shipped**. The capability proved itself *inside its own build*. There is no stronger evidence than a feature earning its place on the day it is forged.

## Meta-Irony

This run had **three DoD rounds at Plan stage** — which is *precisely* the symptom the Paired Constraints Primitive + Architect-in-Plan feature exists to eliminate. The feature is now self-applicable to its next run. If run-2026-04-09 does not land Plan in a single round with Celebrimbor + `constraints.yml` loaded, we must question whether we built the right thing or merely documented it.

## Action Items

1. **Amendment propagation rule**: Validators MUST fail any artifact whose amendments reference adjacent docs not mirrored in the authoritative source. Add to `stages/plan.md` gate check. *(Owner: Scrum Bag, next run)*
2. **Validator CLI contract banners**: Every validator script must print a one-line arg-order banner at invocation. Start with `check_dod_constraints.py` and the Stage 6 sweep script. *(Owner: DevOps, this sprint)*
3. **Next-run dogfood gate**: Explicitly measure Plan first-try pass on run-2026-04-09. If the feature does not self-apply, open a P0 defect against ADR-002. *(Owner: Orchestrator, next run)*

---

*"The pipeline is long, and the rework heavy — but not all who wander the DoD are lost. Forth, and shipwards."*

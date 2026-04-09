# Retrospective — run c4d1 (transformation-planning)

**Role:** Aragorn (Delivery Lead) | 2026-04-08

## What Went Well

- **Consolidated fused dispatches** (multi-artifact, multi-role in one Agent call) kept the pipeline tight without sacrificing rigor. Used in b2c7 and c4d1 successfully.
- **Dogfooding on Claude-Plugins itself** produced real artifacts with real numbers: 7 use cases captured, 5 roadmap steps drafted, 16% max subsystem-change per step — not hand-waved estimates.
- **`constraints.yml` primitive + `validate_constraints.py`** worked on three separate YAML files in one run (AS-IS, TO-BE, and 02-refine PO constraints) — the primitive is proving reusable across stages.
- **Phase-2 Golden Rule anchor** (preserved invariants before TO-BE speculation) gave Celebrimbor a concrete discipline and produced 4 explicit Golden-Rule references in the phase-2 doc.

## What Didn't

- **architecture.md namespace collision:** artifacts were appended to prior run b2c7's file. Not fatal, but conflates runs. Fix: include run-id in filenames or sub-directory per run for 07-uat.
- **DoD self-check tool caveat** (TC-12): `check_dod_constraints.py` cannot self-scan the forbidden-vocabulary field without false-positive matches. Documented; BACKLOG candidate for `--skip-declarations` mode.

## Key Insight

Transformation-planning now has a **REAL AS-IS → TO-BE → Roadmap on Claude-Plugins itself** that BACKLOG-005 can consume as canonical input. **Meta-circularity holds as planned** — the Marketplace can now describe its own brownfield migrations inside its own vocabulary.

## Action Items

- BACKLOG-006: wire transformation-planning real orchestrator dispatch (Step 5 of dogfood roadmap)
- BACKLOG: namespace 07-uat artifacts by run-id
- BACKLOG: `check_dod_constraints.py --skip-declarations`

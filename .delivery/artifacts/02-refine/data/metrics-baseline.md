# Metrics Baseline — Paired Constraints Primitive

**Stage**: 2 (Refine) | **Role**: Data Analyst (Elrond) | **Date**: 2026-04-08
**Purpose**: Authoritative pre-feature snapshot. The PRD's success criteria resolve against these numbers.

> *"I was there three thousand sprints ago, when the metrics last failed. Let none mistake narrative for measurement."*

## 1. Stage Health Baselines (last 5 runs)

Source: `.delivery/memory/index.md` lines 6–16.

| Stage | First-Try Pass | Trend | Note |
|---|---|---|---|
| Idea | 100% (5/5) | Stable | — |
| Refine | 100% (2/2) | Stable | ran in 2 of 5 |
| Design | 100% (2/2) | Stable | ran in 2 of 5 |
| Architect | 100% (3/3) | Stable | ran in 3 of 5 |
| **Plan** | **80% (4/5)** | Improving | 2 consecutive first-try passes with pre-loaded constraints |
| Development | 80% (4/5) | Improving | clean first-try in run 3d92 |
| UAT | 100% (5/5) | Stable | 5 consecutive first-try passes |

Total runs (all time): **17** (`index.md` L4).

## 2. Plan Stage Deep-Read

Sources: `memory/stages/plan.md`, `memory/topics/gate-patterns.md`.

- **Central metric (all-time)**: Plan first-try pass rate **57% (4/7 runs)** — `stages/plan.md` L9; `gate-patterns.md` L17. Recent window is 80% (4/5) but the all-time denominator is the PRD's honest baseline.
- **Gate failures observed**:
  - Missing capacity declaration — velocity baseline / 80% ceiling / per-sprint commitment absent (`stages/plan.md` L5; `gate-patterns.md` L8). Last: run-2026-03-29-**h3k7**.
  - Capacity overcommitment / >80% ceiling breach, incl. markdown-tier miscalibration (`stages/plan.md` L7; `gate-patterns.md` L14). Last: **h3k7**.
  - Incomplete FR traceability — FR-14 (mutual exclusion), FR-15 (default fallback) missed (`stages/plan.md` L6; `gate-patterns.md` L7). Last: run-2026-03-27-**c8f2**.
- **First-try passes, and what was different**:
  - run-2026-03-30-**r4x2** — first perfect run, 6/6 stages first-try. Correlate: gate-patterns memory injection before <80% stages (`gate-patterns.md` L16). Adversarial review caught Sprint-1 100% ceiling; US-05 moved (`stages/plan.md` L8).
  - run-2026-04-02-**k3r9** — pre-loaded constraints injected into planning agents, not just validators (`stages/plan.md` L9). The explicit remedy.
- **Root cause (quoted)**: *"planning agents lack pre-loaded constraints. Fix: inject sprint ceiling + mandatory artifact list into planning agent prompts, not just validators."* (`gate-patterns.md` L17).

## 3. Defect Rate

Source: `.delivery/defects/index.md`.

- Total defects: **3** (L4). Rate on last measured run: **0.25 defects/story** (2/8, run-k3r9) — L5.
- Prior to k3r9: **0 defects across all runs** (L27).
- Categories (L19–24):
  - Agent validation gap — 1, run-k3r9, not systemic.
  - Incomplete pricing — 1, run-k3r9, not systemic.
  - **Wizard/schema drift — 1, setup-2026-04-08, SYSTEMIC** (DEFECT-003).
- **Decomposition/constraints/contamination-linked defects**: **zero tracked today.** This is a measurement gap the feature closes — there is no rule check that would log them.

## 4. Development Stage Patterns

Source: `memory/stages/development.md`.

- Stale derived artifacts (config-schema.json from .md) — 1 occurrence, run-**c8f2** (L5).
- Missing user-facing scope disclaimers — 1 occurrence, run-**k3r9** (L7).
- Source↔installed sync gap — 2 consecutive runs: **j8f2**, **w7m3** (L8).
- Implementation-detail leakage from Architect into Dev: **not independently tracked**. The banned-token set (`lambda|ecr|sqs|ec2|s3|dynamodb|<language-name>`, idea-brief §1 Gap 2) has no grep baseline in any current artifact.

## 5. Proposed Measurement Methodology

1. **Plan first-try pass rate (next 5 runs)**: count runs where `05-plan/dod/*` records DONE on round 1, divide by 5. Target per idea-brief §4.1: **≥80%**. Record in `memory/index.md` stage-health table after each run.
2. **Banned-token contamination scan**: `grep -iE '\b(lambda|ecr|sqs|ec2|s3|dynamodb|python|typescript|javascript|rust|go|nodejs)\b' .delivery/artifacts/04-architect/**/*.md` — run on every post-feature Architect artifact. Target: **zero matches** outside quoted prior art. Log in `memory/topics/gate-patterns.md` per run.
3. **Golden Rule citation presence**: `grep -l "decompose by volatility, not by functionality" .delivery/artifacts/04-architect/**/*.md` on runs where volatility is the selected strategy. Target: **1 match per volatility-strategy run**.
4. **Schema consumption (non-divergence)**: confirm both Refine DoD hook and Architect DoD hook load the same `constraints.yml` schema file hash; log in stage-summary.
5. **Architect-in-Plan participation**: presence of `.delivery/artifacts/05-plan/architect/sequencing.md` on each run.
6. **Signal carriers**: `memory/stages/plan.md`, `memory/stages/architect.md` (new chunk), `memory/topics/gate-patterns.md` — update per run.

## 6. Honest Caveats

- **Small-n problem**: 17 total runs; 7 Plan observations; 5-run window moves the 57% figure substantially. A single bad run post-feature drops the target below 80%. Elrond counsels: report both windows.
- **Confound — gate-patterns injection is already live**. The recent 80% (4/5) reflects *existing* memory-injection benefits (runs r4x2, k3r9). Attributing post-feature gains purely to `constraints.yml` is unsound; A/B via the BACKLOG-001 spike flag is the only clean read.
- **Banned-token baseline is zero by absence, not by measurement.** We have never grepped prior artifacts. Before the feature lands, run the scan on the last 5 Architect artifacts to establish a true pre-state.
- **Golden Rule citation baseline is also unmeasured** — likely zero, but confirm via grep on existing artifacts.
- **DEFECT-003 (wizard drift) is orthogonal** to this feature; it must not contaminate Plan-rate attribution.
- **Project-type skew**: only 2 of 5 recent runs exercised Refine/Design; denominators thin, trends directional.

STATUS: DONE
ARTIFACT: .delivery/artifacts/02-refine/data/metrics-baseline.md
SUMMARY: The stones record Plan at 57% all-time, 80% recent; contamination and Golden-Rule baselines are unmeasured and must be grepped ere the feature lands.

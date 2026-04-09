# Sprint Plan — Paired Constraints Primitive (`constraints.yml`)

**Stage**: 5 (Plan) | **Role**: Scrum Bag (Aragorn)
**Pipeline ID**: run-2026-04-08-a1f3
**Date**: 2026-04-08
**Self-correction**: round 1 (prior draft bound to stale DS-01..DS-07 — discarded)
**Authoritative source**: `.delivery/artifacts/05-plan/po/stories.md` (US-1..US-9, 17 pts)

> *"A plan carried honestly is worth ten carried in pride. We walk at the pace the road allows."*

---

## Capacity Declaration

| Field | Value |
|---|---|
| Team size | 1 |
| Velocity baseline | 5 pts / sprint |
| 80% target ceiling | 4 pts / sprint |
| Hard cap (never exceed) | 5 pts / sprint |
| Work tier | Markdown + schema + content → one tier lower (memory: run-h3k7) |
| Sprints committed | **4** |
| Total committed | **17 pts** |

---

## Sprint Allocation — SM Adjustment of PO Sketch

I do not endorse PO's sketch as-written. Sprint 2 at 100% hard cap is the exact shape adversarial review punished in run-r4x2. I rebalance: **move US-6 from S2 to S3, advance US-3 from S3 to S2.** Total stays 17; the hard cap shifts to S3 where fan-in risk is lowest.

| Sprint | Goal | Stories | Pts | % of cap | Dependency gate |
|---|---|---|---|---|---|
| **S1 — Foundations** | Deterministic schema + Golden Rule named in the canon | US-1 (3), US-5 (1) | **4** | 80% | none — US-5 is prose-only, parallelizable |
| **S2 — Author the Templates** | PO can emit a valid `constraints.yml` in Refine | US-2 (2), US-3 (2) | **4** | 80% | S1 ships US-1 validator; US-2 is bedrock for US-3 |
| **S3 — Wire the Architect In** | Architect speaks the primitive and stands in Plan | US-4 (2) → US-7 (2), US-6 (1) | **5** | 100% hard cap ⚠ | US-4 lands **before** US-7 (A-3: `forbidden_vocabulary` list must be locked before `pipeline-stages.md` edits depend on it); US-4 needs US-1/US-2 twice-validated; US-7 then rebases on frozen list |
| **S4 — Enforce + Dogfood** | DoD validators bite; we carry our own burden through UAT | US-8 (3), US-9 (1) | **4** | 80% | US-8 needs US-4 token list locked; US-9 needs US-1/2/3/8 green |

**Total: 17 pts / 4 sprints.**

### Sprint Goals (outcome-focused, one sentence each)

- **S1**: The rule is named and the structure is known.
- **S2**: The PO side of the pair can emit a valid artifact.
- **S3**: The Architect stands in the Plan council with the DDD path at parity.
- **S4**: The burden is enforced and we have carried it ourselves.

### Rollback triggers (what makes me pull the sprint)

- **S1**: US-1 validator fails to load headless → re-estimate US-1 to 5 pts, collapse S1 into S2.
- **S2**: US-3 sample fails US-1 validator after two attempts → ship US-2 only; slip US-3 to S3 (displacing US-6 to S4).
- **S3**: `forbidden_vocabulary` list contested against PRD FR-3 → freeze PRD token list verbatim; if still contested, pull US-7 to S4 and reject S3.
- **S4**: US-9 dogfood fails US-8 checks → fix the rules, not the artifact. Halt release, reopen S3.

---

## S2 Hard-Cap Analysis — the r4x2 Lesson Applied Upstream

PO placed the 100% at S2. I move it to S3. Seventeen points across four sprints with a four-point ceiling sums to sixteen; someone must carry the fifth stone. The honest question is **which sprint is the safest place to ride the cap.**

PO's S2 carries US-2 + US-6 + US-4. US-4 depends on US-1 *and* US-2 — if S1 slips a single day, US-4 starts mid-sprint on a wet foundation. That is the classic ceiling-breach pattern adversarial review punished in r4x2. My S3 carries US-4 + US-7 + US-6, but by S3 the US-1 contract has been exercised twice (S1 ship, S2 consumption) and US-6 is a 1-pt prose edit with zero dependencies — a genuine shock absorber. If S3 slips, US-6 slides to S4 without cost (S4 becomes 5 pts, still at hard cap, not over). If US-4 slips inside S3, US-7 proceeds on the frozen US-1 contract — they are independent within the sprint. The hard cap lands on the sprint with the *lowest* fan-in risk, not the highest. I will not pretend the plan has no hard cap. I put the hard cap where it fails safe.

---

## Sequencing Rationale

- **US-1 → everything.** The schema is the contract; nothing validates without it.
- **US-2 → US-3, US-4.** The canon must exist before the domain templates cite it.
- **US-3 and US-4** are independent once US-1/US-2 are landed (PO-scope vs Architect-scope).
- **US-7** is parallel to US-4 once US-1 exists — gated only on the schema, not the canon.
- **US-3 + US-7** both edit `pipeline-stages.md` across sprint boundaries — US-7 rebases onto US-3's landed diff (CR-3 control).
- **US-5, US-6** are prose inserts with zero dependencies — scheduled as ballast against sprint-level risk.
- **US-8 → US-9.** Validators before dogfood. Memory lesson: no DoD before dogfood.

---

## Impediments

- **I-1 `forbidden_vocabulary` list drift.** If US-4's enumerated list wanders from PRD FR-3, US-8's grep rule becomes un-reviewable. *Control*: lock the PRD token list verbatim in US-4 DoD; SM attends the US-4 review.
- **I-2 `pipeline-stages.md` merge collisions.** US-3 (S2) and US-7 (S3) touch the same file. *Control*: US-7 rebases onto US-3's landed diff at S3 start; no concurrent branches on this file.
- **I-3 NFR-5 token delta is UAT-only.** Nothing in S1–S4 tells us if Refine ceremony overshoots +15%. *Control*: Data Analyst instrumentation registered at S1 start so S4 has a real baseline.

---

## Adversarial Self-Check — Where Would a Challenger Strike?

Three lines of attack I expect, answered honestly:

1. **"S3 is still 100%, you moved the problem, you didn't solve it."** True. 17 / 4-pt ceiling = one sprint must ride the cap. I argue S3 is the safer landing zone (lower fan-in risk; US-6 is free ballast). Alternatives — 5 sprints (4/4/3/3/3) or re-estimating US-1 down to 2 pts — are worse: five sprints breaks PO allocation and drags UAT; re-estimating US-1 is dishonest given schema + validator + fixtures are genuinely 3 pts at this tier.
2. **"US-8 at 3 pts in S4 with US-9 behind it is the real hard cap."** Fair. S4 is 4 pts but US-8 is the highest single-story risk (deterministic rule engine, NFR-4 constraint). If US-8 slips, US-9 cannot ship. *Mitigation*: US-9 is 1 pt and its acceptance is "does the file pass checks" — same-day turnaround against a landed US-8. Concentration accepted.
3. **"US-3 is scheduled in the same sprint as its dependency US-2."** Intra-sprint, one person, sequential execution: land US-2 first, then US-3. No parallelism required, no collision. The dependency holds inside S2. Not a violation.

A fourth attack, if it comes, will land on NFR-5 (token delta). I concede it cheerfully and point at I-3.

---

## Architect Amendments Accepted

Celebrimbor raised three amendments in `.delivery/artifacts/05-plan/architect/sequencing.md`. The PO accepted all three. I carry them into the plan:

- **A-1 — AC-1.4 (schema forward-compat) added to US-1 DoD.** US-1 does not ship until the schema tolerates unknown-key forward-compat per AC-1.4. Impact: no sprint reshuffle — absorbed inside S1's 3-pt US-1 estimate at current tier.
- **A-2 — AC-9.4 (explicit cache-refresh in dogfood) added to US-9 DoD.** US-9 dogfood must execute an explicit cache-refresh step per AC-9.4 before DoD signs. Impact: no sprint reshuffle — US-9 remains 1 pt in S4; the ceremony is additive, not structural.
- **A-3 — S3 intra-sprint order: US-4 before US-7.** The `forbidden_vocabulary` list must be locked in US-4 before US-7's `pipeline-stages.md` edits consume it. Impact: S3 row updated above to show `US-4 → US-7`; CR-3 merge-collision control on `pipeline-stages.md` (I-2) now chains US-3 → US-4 → US-7 in strict sequence. Sprint totals unchanged.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/sm/sprint-plan.md
SUMMARY: Round 2 — Celebrimbor's three amendments accepted and named: A-1 into US-1 DoD, A-2 into US-9 DoD, A-3 locks S3 order US-4 → US-7. Sprint totals hold.

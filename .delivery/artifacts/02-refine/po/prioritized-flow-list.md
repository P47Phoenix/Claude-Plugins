# Prioritized Flow Doc List — Stage 2 Refinement (PO)

> *Gandalf the Grey, leaning on his staff: "Eighteen proposals have come to Rivendell. We shall not carry all rings to Mount Doom in one fellowship. Six we forge now; the rest await the second sprint — and some shall wait longer still, for wisdom is knowing what not to write."*

**Synthesizer:** Gandalf (PO lens) · **Inputs:** Celebrimbor (7) + Legolas (5) + Sam (6) = 18 proposals · **Capacity declaration:** 6 docs this run (2 mandatory + 4 convergence/high-value). Per `feedback_no_skip_stages.md` light means reduced depth, not skipped — but capacity is real and shipping 18 in one run would be vapor.

---

## 1. Convergence Map (proposals in 2+ brainstorms)

| Topic | Celebrimbor | Legolas | Sam | Signal |
|---|---|---|---|---|
| Hook firing timeline | #7 | — | #1 | 2/3 — strong |
| DoD / self-correction routing | #3 | #2 | — | 2/3 — strong |
| State lifecycle | (touched in #3 terminals) | — | #2 | 1.5/3 — partial |
| Memory write cycle | (deferred) | — | #4 | 1/3 |

Everything else is single-lens. Convergence is a priority signal, not a veto for unique-lens gems.

## 2. Deduplication (merges)

- **MERGE-A: Hook Timeline** — Celebrimbor #7 (spatial-with-outcomes) + Sam #1 (temporal swimlane). One doc, both lenses cited. Single diagram set: Sam's swimlane primary, Celebrimbor's block/warn/pass branches secondary.
- **MERGE-B: DoD Self-Correction** — Celebrimbor #3 (state machine + CODE_COMPLETE terminal + delegation meta-gate) + Legolas #2 (finding-schema contract + round-bound wiring). One doc, architect owns state machine diagram, QA owns the finding-schema contract table.
- No other meaningful overlaps; proposals are genuinely complementary.

## 3. Final Prioritized List (ship this run)

| # | Doc | Source | Sprint |
|---|---|---|---|
| 1 | `adversarial-review-triggers.md` | Celebrimbor #1 (PO mandatory) | S1 |
| 2 | `deterministic-gating.md` | Celebrimbor #2 (PO mandatory) | S1 |
| 3 | `hook-timeline.md` | MERGE-A (Celebrimbor #7 + Sam #1) | S1 |
| 4 | `dod-self-correction.md` | MERGE-B (Celebrimbor #3 + Legolas #2) | S2 |
| 5 | `empirical-validation-lifecycle.md` | Legolas #1 | S2 |
| 6 | `agent-dispatch.md` | Celebrimbor #6 | S2 |

## 4. PO's Two Mandatory Asks — Honored

- **Adversarial Review Trigger Flow** (Celebrimbor #1) → doc #1 above. Non-negotiable ship.
- **BRE Usage Flow** (Celebrimbor #2) → doc #2 above. **Honesty caveat preserved:** delivery-team has no BRE module. Its determinism is the DoD-validator-unanimity + routing-matrix + confidence-threshold stack. The literal `business_rules_engine.py` lives in `prd-quality-gate-flow/` and `agentic-flow-builder/` (sister plugins). The doc contrasts both approaches side-by-side; it does not invent a BRE that does not exist.

## 5. Rationale per Choice

**Shipped:**
- **#1 Adversarial triggers** — PO mandatory; load-bearing for confidence-rating escalation contract.
- **#2 Deterministic gating** — PO mandatory; cross-plugin honesty doc no one else can write.
- **#3 Hook timeline** — strongest convergence signal (2/3 brainstorms); contributor pain is high.
- **#4 DoD self-correction** — second-strongest convergence; finding-schema contract rots fastest per Legolas.
- **#5 Empirical lifecycle** — closes CODE_COMPLETE documentation gap Legolas flagged; AC-lifecycle has no home today.
- **#6 Agent dispatch** — Celebrimbor called it the most-violated convention in the repo; diagram prevents more harm than prose.

**Deferred (good work, wrong run):**
- **Cache sync (Sam #3)** — memory-lesson-shaped, but small audience; defer to sprint 3.
- **State lifecycle (Sam #2)** — partially covered by ARCH §5; needs coordination, not a rush.
- **Retro/memory cycle (Sam #4)** — complementary but read-cycle protocol is already dense.
- **Architecture board (Celebrimbor #5)** — L-complexity; specialized application; earns sprint 3.
- **Dynamic escalation (Celebrimbor #4)** — aggregates triggers from #1 and #3; ship AFTER those land or it references unwritten docs.
- **Traceability matrix (Legolas #3)** — L-complexity + highest auditor value, but needs Plan/UAT stage input we don't have yet.
- **Validator locality (Legolas #5)** — load-bearing invariant but fits better as a section in #4 (`dod-self-correction.md`) later.
- **Test-type decision tree (Legolas #4)** — S-complexity and high leverage; strong sprint-3 candidate.
- **Notification routing (Sam #5)** — smallest audience, Sam's own trim target.
- **Config lifecycle (Sam #6)** — partially covered by `config-schema.md` extension protocol.

## 6. Defer List (later sprints, not abandoned)

Sprint 3 candidates (ranked): Test-type tree → Cache sync → Dynamic escalation → Architecture board → Traceability matrix → Validator locality (as section merge) → State lifecycle (coordinate with ARCH §5) → Retro/memory cycle → Config lifecycle → Notification routing.

*The road goes ever on — but not all in one stride.* — Gandalf

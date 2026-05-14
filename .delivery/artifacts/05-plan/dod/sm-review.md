<!-- run: run-2026-05-13-tk5 -->
<!-- author: Aragorn (Scrum Bag, Stage 5 light, DoD validation) -->
<!-- backlog: BACKLOG-106 -->
<!-- gate: SM DoD validation against sprint-plan.md + stories.md + sequencing.md -->
# SM DoD Review — run-2026-05-13-tk5 (BACKLOG-106 Smoke Test)

> *"I do not know what strength is in my backlog, but I swear to you I will not let the sprint fall."* — Aragorn

Me Aragorn. Me hold gate. Six criteria. Me check each. Me grep, me count, me speak verdict.

---

## Verdict: PASS (DONE)

All six SM gate criteria evaluated. Zero BLOCKING findings. Zero WARN findings. One informational nit (sprint-plan misattribution of a parallel proposal to architect that does not appear in sequencing.md — no real conflict, see Criterion 5).

---

## Gate-by-Gate Evaluation

### Criterion 1 — Capacity matrix with utilization %

**Status**: PASS.

- Sprint-plan §2 contains the capacity table with `Available hours | Allocated hours | Utilization %` columns (sprint-plan.md:23–25).
- Team-size source declared: `.delivery/config.yml` `team.size: 1`, composition `[developer]`.
- Net available 28h (32h gross − 4h ceremony) vs allocated 20h = **71.4%**.
- 71.4% is **under 80% WARN line**; under 100% BLOCKING line.
- Buffer 28.6% (8h) explicitly accounts for producer-to-validator context-switch tax (BC-03).

**Verdict**: HEALTHY. No BLOCKING. No WARN.

### Criterion 2 — Coverage matrix: every PRD FR-ID maps to ≥ 1 story

**Status**: PASS.

PRD FR-ID enumeration (grep against `02-refine/po/prd.md` §Functional Requirements):
```
FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-07, FR-08   (8 FRs)
```

Sprint-plan §3 Coverage Matrix (sprint-plan.md:37–46) maps each FR explicitly:

| FR-ID | Story | AC ref |
|-------|-------|--------|
| FR-01 | S1 | AC-S1-03, AC-S1-04 |
| FR-02 | S1 | AC-S1-06 |
| FR-03 | S1 | AC-S1-07 |
| FR-04 | S1 | AC-S1-02, AC-S1-08 |
| FR-05 | S2 | AC-S2-03, AC-S2-04, AC-S2-05 |
| FR-06 | S2 | AC-S2-01, AC-S2-02, AC-S2-08 |
| FR-07 | S3 | AC-S3-01..AC-S3-04, AC-S3-08 |
| FR-08 | S3 | AC-S3-05, AC-S3-06, supporting AC-S2-07 |

Grep cross-check:
- PRD FR-IDs: 8 unique (FR-01..FR-08).
- sprint-plan.md FR-IDs: 8 unique (FR-01..FR-08).
- stories.md FR-IDs: 8 unique (FR-01..FR-08).

**Zero unmapped FRs.** No BLOCKING.

### Criterion 3 — Stop-rule reminder + current rolling defect-rate

**Status**: PASS.

Sprint-plan §6 Stop-Rule Reminder (sprint-plan.md:87–95):
- Rule cited: "defects/story > 0.4 across any 3-PR window pauses subsequent work."
- Current rolling rate cited: **0.111** (per PRD + user-seed).
- Headroom math shown: 0.400 − 0.111 = 0.289/story.
- Wave-level translation: 0.289 × 3 stories = 0.867 raw defects before rolling threshold trips.
- Aragorn-flag clause: any single story introducing > 0.4 defects in QA escalates immediately (sprint-plan.md:125).

**Verdict**: present, quantified, anchored to canonical source.

### Criterion 4 — Risk register ≥ 3 risks, each with named mitigation + owner

**Status**: PASS (exceeds threshold).

Sprint-plan §5 Risk Register (sprint-plan.md:77–83) has **5 rows** (R-01..R-05). Threshold is 3.

| # | Risk | Mitigation present? | Owner named? |
|---|------|---------------------|--------------|
| R-01 | Prompt drift | YES (hard_max on dispatch_count, AC-S2-04, TC-S2-08 grep guard) | PO (Gandalf) |
| R-02 | Cost overrun | YES (`--cost-cap 3.00`, 30-min SIGTERM, concurrency-of-1) | Developer (Dispatch A) |
| R-03 | `--plugin-dir` semantics drift | YES (capability-probe + copy-into-HOME fallback, AC-S1-04) | Architect (Celebrimbor) |
| R-04 | Stop hook blocks | YES (minimal-retro prompt clause AC-S2-06, stderr capture, SIGTERM backstop) | Developer (Dispatch A) + PO (Gandalf) |
| R-05 | Variance > stddev budget | YES (advisory-only first month, 2σ no exit-code escalation; tighten after 20+ runs deferred) | PO (Gandalf) |

All 5 risks: mitigation present, owner named. **Exceeds 3-risk threshold.** No BLOCKING.

### Criterion 5 — Story sequencing consistency across PO / Architect / SM

**Status**: PASS (with informational nit, non-blocking).

Cross-document sequencing claims:

| Source | Stated order |
|--------|--------------|
| `po/stories.md` §Cross-story producer-validator summary (line 191–195) | S1 (Dispatch A) → S2 (Dispatch A same dispatch) → S3 (Dispatch B fresh) |
| `architect/sequencing.md` §2 + §4 + §7 (lines 42–166) | S1 → S2 → S3 sequential; "max_parallel_agents: 3 is unused by this initiative" |
| `sm/sprint-plan.md` §4 Story Sequencing (line 56–62) | S1 (Dispatch A, L=9h) → S2 (Dispatch A, M=6h) → S3 (Dispatch B fresh, M=5h) |

**All three artifacts assert the same final order**: S1 → S2 → S3 with S1+S2 in one producer Dispatch A and S3 in a fresh validator Dispatch B. No conflicting S1→S2→S3 claims.

**Informational nit (non-blocking)**: Sprint-plan §4 line 54 says *"Architect's sequencing … proposes `S1 -> (S2 ∥ S3)`. PO directive … **overrides**…"* However, architect's `sequencing.md` does NOT propose `S1 -> (S2 ∥ S3)` — it explicitly says (sequencing.md:9) "S1 first. Then S2. Then S3 in fresh hands… No parallel inside one dispatch" and (sequencing.md:100) "Can S2 and S3 run in parallel? **NO**". The sprint-plan narrative misattributes a parallel proposal to the architect that the architect did not in fact make. The **final ordering is consistent** across all three artifacts; the misattribution is rhetorical, not structural.

**Verdict**: ordering consistent. No BLOCKING. Recommend Aragorn note this rhetorical drift in the wave retrospective so future SM narrative does not misattribute architect positions — but the gate criterion (consistent sequencing claims) is met because all three docs land on identical S1→S2→S3 + Dispatch A vs Dispatch B order.

### Criterion 6 — Initiative-level DoD checklist enumerates exactly 8 Stage-7 UAT gates from user-seed

**Status**: PASS.

User-seed §Acceptance criteria (user-seed.md:43–52) enumerates 8 numbered gates.

Sprint-plan §7 Definition of Done (sprint-plan.md:99–110) enumerates **8 DoD checkboxes** (DoD-1..DoD-8):

| DoD-# | Maps user-seed gate # | Maps PRD AC | Match? |
|-------|------------------------|-------------|--------|
| DoD-1 | gate 1 (`< 30 min wall-clock`) | AC-01 | YES |
| DoD-2 | gate 2 (artifact triplet dir) | AC-02 + AC-S1-02 | YES |
| DoD-3 | gate 3 (report.json schema) | AC-03 + AC-S1-08 | YES |
| DoD-4 | gate 4 (`--init-baseline` 5×) | AC-04 + AC-S2-01 + AC-S2-02 | YES |
| DoD-5 | gate 5 (HARD-FAIL + ADVISORY-WARN rules) | AC-05 + AC-S2-04 + AC-S2-05 | YES |
| DoD-6 | gate 6 (meta-tests pass) | AC-06 + AC-S3-01..AC-S3-04 | YES |
| DoD-7 | gate 7 (no `.github/workflows/smoke-*.yml`) | AC-07 + BC-01 | YES |
| DoD-8 | gate 8 (architecture doc records local-only) | AC-08 + ADR-tk5-001 | YES |

Grep verification: `grep -cE "^- \[ \] \*\*DoD-"` returns **8**. User-seed numbered gates: **8**. **Exact match.** No BLOCKING.

---

## Summary

| Gate | Verdict |
|------|---------|
| 1. Capacity matrix + utilization | PASS (71.4%, under WARN line) |
| 2. Coverage matrix (every FR → ≥1 story) | PASS (8/8 FRs mapped) |
| 3. Stop-rule + current rolling rate | PASS (0.111 cited, headroom 0.289/story) |
| 4. Risk register ≥ 3 risks w/ mitigation + owner | PASS (5 risks, all complete) |
| 5. Sequencing consistency (PO + Architect + SM) | PASS (identical S1→S2→S3 order; one rhetorical misattribution noted, non-blocking) |
| 6. DoD checklist = 8 Stage-7 UAT gates from user-seed | PASS (exact 1-to-1 mapping) |

**Stage 5 SM DoD: GREEN.** Stage 6 Development orchestrator may dispatch.

---

## Downstream Notes (for orchestrator)

1. Dispatch A (producer) gets S1 + S2 as one ordered work unit. Internal file order per architect §2: workspace → runner → metrics → aggregator → report → run_smoke, then baseline + prompt + fixture.
2. Dispatch B (validator) gets S3 ONLY, in a fresh `Agent` call. Sub-agent prompt MUST include explicit prohibition on reading `delivery-team/tests/smoke/lib/metrics.py` and `delivery-team/tests/smoke/lib/baseline.py` source while authoring fixtures (sequencing.md §6 step 3).
3. Capacity buffer = 8h. If any story overruns, Aragorn flag before Stage 6 closes — do not silently consume buffer.
4. Stop-rule headroom = 0.289/story; any single S3 meta-test catching > 0.4 defects per story trips the rolling window after merge — escalate before PR.
5. Wave retrospective: note the sprint-plan §4 misattribution of a parallel proposal to architect (Criterion 5 informational nit). Lesson for future SM narrative authoring.

---

— Aragorn, Scrum Bag, run-2026-05-13-tk5. Gate holds. Fellowship marches.

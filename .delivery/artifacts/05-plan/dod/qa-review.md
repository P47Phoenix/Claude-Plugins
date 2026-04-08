# QA DoD Review — Stage 5 Plan (Orchestration Discipline Bundle)

**Reviewer**: Legolas of the Woodland Realm (QA)
**Stage**: 05 — Plan
**Artifacts under review**:
- `.delivery/artifacts/05-plan/po/stories.md`
- `.delivery/artifacts/05-plan/qa/test-strategy.md`

> *"I have sighted each arrow before I loosed it. The quiver is full, the wind is read, the target is clean."*

---

## Status

**DONE**

---

## Validation Checklist

### 1. Test strategy covers critical paths

| Critical path | Covered? | Evidence |
|---|---|---|
| Hook deny on orchestrator-attributed Write (FR-09a) | Yes | T-09a + truth-table rows 1, 17–19 |
| Hook allow on sub-agent-attributed Write (FR-09a') | Yes | T-09a-prime, row 2 |
| Bash redirection variants (heredoc, `>`, `>>`, tee, dd, cp, mv) | Yes | T-09b-heredoc/redir/tee/dd/cp/mv, rows 7–12; quoted-path and mixed-redirection edge cases explicit |
| Allowlist paths (state.md, config.yml, memory/**, stage state/) | Yes | T-09a-allow-1..4, rows 3–6 |
| Activation gating (v2.7 + `enforce_self_write_block`) | Yes | T-09g, row 15 |
| Scope inclusion/exclusion for source paths | Yes | T-09-scope / T-09-out-of-scope, rows 19–20; path-traversal + symlink edge cases called out |
| Backwards compat with v2.6 legacy configs | Yes | T-N03, T-02a |
| Hook performance budget (NFR-01, p95 ≤ 50ms) | Yes | T-N01 with 200-sample baseline delta |
| Graceful degradation on hook exception (NFR-05) | Yes | T-N05 via monkey-patched `detect_origin` |
| Phase 1 detection per invocation (FR-03) | Yes | T-03 + integration S1/S2 (same-repo, divergent routing) |
| Routing pin override (FR-02b/c) | Yes | T-02b, T-02c, integration S3 |
| Delegation Prime Directive + anti-patterns (FR-06/08) | Yes | T-06, T-08, L2 two-reader walk-through |
| Adversarial loop convergence (FR-13/14, ADR-003) | Yes | T-13 asserts three convergence rules + taxonomy; integration S5 |
| Doc parity (FR-16/NFR-04) | Yes | T-16, T-N04 |
| Hostile end-to-end verification | Yes | Integration S7 (Write) + S8 (Bash heredoc) explicit |

Critical-path coverage: complete. No arrow un-nocked.

### 2. Every story has test cases

| Story | Inline test table | Strategy-level IDs |
|---|---|---|
| OD-01 | OD-01-T1..T4 | T-01a, T-04, T-05 |
| OD-02 | OD-02-T1..T5 | T-03, T-05 |
| OD-03 | OD-03-T1..T5 | T-02b, T-02c |
| OD-04 | OD-04-T1..T5 | T-01b, T-02a, T-15 |
| OD-05 | AC-bound | T-06, T-08 |
| OD-06 | AC-bound | T-07 |
| OD-07 | AC-bound | T-09a/prime/allow-*/b-*/c/d/e/g/scope/out-of-scope/layer2/readonly/nopipe + T-N01/02/03/05 |
| OD-08 | AC-bound | T-10 |
| OD-09 | AC-bound | T-11 |
| OD-10 (optional) | AC-bound | T-12 pos/neg |
| OD-11 | AC-bound | T-13 |
| OD-12 | AC-bound | T-14 |
| OD-13 | AC-bound | T-16, T-N04, T-N07, T-N08 |

Every story OD-01..OD-13 is paired with explicit tests. Test-artifact co-location rule (per user memory) is honored — no orphaned split artifact. Execution plan §7 sequences every test batch to its story's DoD gate.

### 3. FR-by-FR traceability is complete

All 16 FRs mapped to ≥1 concrete test ID with story and pass condition in strategy §3:

- FR-01 → T-01a/b (OD-01, OD-04)
- FR-02a → T-02a (OD-04)
- FR-02b → T-02b (OD-03)
- FR-02c → T-02c (OD-03)
- FR-03 → T-03 (OD-02) + integration S1/S2
- FR-04 → T-04 (OD-01)
- FR-05 → T-05 (OD-01, OD-02)
- FR-06 → T-06 (OD-05)
- FR-07 → T-07 (OD-06)
- FR-08 → T-08 (OD-05)
- FR-09 (a/a'/a''/b/c/d/e/gating) → T-09a..T-09g + 20-row truth table (OD-07)
- FR-10 → T-10 (OD-08)
- FR-11 → T-11 (OD-09)
- FR-12 → T-12 pos/neg (OD-10, optional, with formal defer path)
- FR-13 → T-13 (OD-11)
- FR-14 → T-14 (OD-12)
- FR-15 → T-15 (OD-04, OD-11, OD-12)
- FR-16 → T-16 (OD-04, OD-13)

All 8 NFRs mapped (NFR-01..08 → T-N01..N08) with pass conditions. Zero FR/NFR left without a test binding. Traceability matrix is complete and bidirectional (FR→Test and Story→Test).

### 4. Test levels and mechanisms are sound

- L1 (grep) / L2 (two-reader walk-through) / L3 (hook fixtures) / L4 (perf) / L5 (dogfood) tiering is explicit and matched to artifact type.
- Stdlib-only harness under `delivery-team/tests/` respects repo convention — no pytest, no new deps, consistent with NFR-02 and CLAUDE.md.
- Fixture layout concrete; Q-QA-2 correctly surfaces the risk that OD-04 must commit the v2.6 legacy fixture.
- Performance test uses git-stash baseline comparison, not a blind absolute threshold.
- Integration matrix (S1–S8) includes hostile tests (S7/S8) — the only way to prove the hook actually intercepts orchestrator self-writes.
- Defect severity ladder (S1/S2/S3) has clear merge-blocking rules; exit criteria are unambiguous.

### 5. Open items surfaced, not swallowed

Q-QA-1 (Layer 2 metadata availability), Q-QA-2 (v2.6 fixture commit), Q-QA-3 (S5 architect-trigger request complexity) are all forwarded to Development / PO / UAT rather than quietly resolved. Non-integration-testable gaps (MCP writes, `git checkout/apply`, sub-process inheritance) documented as accepted residual risk — correct per ADR-001 §2.

---

## Minor observations (non-blocking)

1. **T-09g parameterization**: the truth-table row for v2.6 tolerant ("warn only") and the "fresh v2.7 → deny active" assertion must both be exercised by a single parameterized test, not just one half. Test-implementation reminder for OD-07, not a DoD defect.
2. **Q-QA-3**: the dogfood run's S5 request must be complex enough to trigger ≥1 adversarial loop iteration. PO to select. Already flagged.
3. **T-12 FP logging**: recommend logging actual false-positive rate on negation-aware cases even on pass, for future tuning of FR-12 if it graduates from MAY to SHOULD.

None are DoD-blocking.

---

## DoD Verdict

- Test strategy covers critical paths: **PASS**
- Every story has test cases: **PASS**
- FR-by-FR traceability complete: **PASS** (16/16 FRs, 8/8 NFRs)
- Test levels and mechanisms sound: **PASS**
- Open items surfaced, not swallowed: **PASS**

**STATUS: DONE**

*"The bow is strung, the wind is read, and every arrow has found its mark on the page. Loose when ready."*

— Legolas, QA

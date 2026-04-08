# Test Strategy: Orchestration Discipline Bundle

**Stage**: 05 — Plan (QA sub-flow)
**QA**: Legolas of the Woodland Realm
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` (16 FRs, 8 NFRs)
**Source Architecture**: `.delivery/artifacts/04-architect/solution/architecture.md` (ADR-001/002/003)
**Source Stories**: `.delivery/artifacts/05-plan/po/stories.md` (OD-01 – OD-13)

> *"I see what others overlook. A single arrow, loosed true, will find the seam in any armor — and a single ungated write will find the seam in any pipeline."*

---

## 1. Strategic Posture

This bundle is ~85% documentation / protocol and ~15% executable hook code. The testing strategy is therefore asymmetric by design:

- **Documentation / protocol FRs** (FR-01 – FR-08, FR-10, FR-11, FR-13 – FR-16) are validated by structural grep checks, doc-parity sweeps, and protocol walk-throughs. The test is "can a future orchestrator read this and arrive at the correct behavior?"
- **Executable hook FRs** (FR-09, FR-12) are validated by synthetic tool-call fixtures driven through the hook's stdin JSON contract. No pytest harness exists in this repo (per CLAUDE.md); test scripts are standalone Python runners under `delivery-team/tests/`.
- **End-to-end behavior** (NFR-06 dogfood) is validated by the next real `/delivery-flow` invocation after merge, not by a synthetic harness. The acceptance record is the resulting pipeline's `state.md` and stage banners.

No part of this strategy depends on a new test runner, framework, or CI system. All checks are runnable from a bare shell with stdlib Python.

---

## 2. Test Levels

| Level | Scope | Mechanism | Owner |
|---|---|---|---|
| **L1 — Structural / grep** | Doc FRs (presence, absence, anchors) | `grep -rn`, `rg`, manual Read | QA per story |
| **L2 — Protocol walk-through** | SKILL.md + references internally consistent; future orchestrator can follow the prose to correct behavior | Two-reader dry-run: one reader executes the doc as if they were the orchestrator, a second reader audits for ambiguity | QA + one sub-agent |
| **L3 — Hook unit (fixture-driven)** | `enforce_pipeline_scope.py`, `audit_agent_prompt.py` logic branches | Stdlib Python scripts under `delivery-team/tests/` that pipe synthetic PreToolUse JSON to the hook's `main()` and assert exit behavior + stdout decision | Developer (implements), QA (reviews) |
| **L4 — Hook performance** | NFR-01 (p95 ≤ 50ms) | Wall-clock timing loop around hook `main()` over 200 synthetic calls, 95th percentile | QA |
| **L5 — Integration (dogfood)** | NFR-06 — orchestrator actually behaves per new rules on the next real pipeline run after merge | Instrumented `/delivery-flow` invocation with two intentionally different request types back-to-back; inspect `state.md`, stage banners, hook logs, and artifact attribution | QA + PO |

---

## 3. FR-by-FR Traceability Matrix

Every FR maps to at least one concrete test at a specific level, with a specific artifact or assertion. Story mapping uses OD-## IDs from stories.md.

| FR | Summary | Stories | Test Level(s) | Test ID(s) | Pass condition |
|---|---|---|---|---|---|
| **FR-01** | Remove `project_type` from active schema; bump to v2.7 | OD-01, OD-04 | L1, L2 | T-01a, T-01b | `config-schema.md` active table has no `project_type`; "Deprecated keys" section contains it; `schema_version: 2.7` present |
| **FR-02a** | Legacy v2.6 config with bare `project_type` parses and emits deprecation banner | OD-04 | L2, L5 | T-02a | Dogfood run with v2.6 fixture in `delivery-team/tests/fixtures/legacy-v2.6-config.yml` loads without error; stage banner contains "legacy `project_type` ignored" |
| **FR-02b** | `routing.force_type: DOCS_ONLY` overrides detection | OD-03 | L2, L5 | T-02b | Fixture v2.7 config with `routing.force_type: DOCS_ONLY` + a GREENFIELD-flavored request routes DOCS_ONLY; banner names the pin and shows detection result |
| **FR-02c** | Both keys present: `routing.force_type` wins | OD-03 | L2, L5 | T-02c | Dual-key fixture: routing uses `force_type`; deprecation line still emitted for bare key |
| **FR-03** | Phase 1 detection runs every invocation | OD-02 | L2, L5 | T-03 | Two consecutive `/delivery-flow` runs in same repo with different requests produce different routing decisions in `state.md` |
| **FR-04** | Setup wizard drops Q1, now 9 questions | OD-01 | L1, L2 | T-04 | `setup-wizard.md` renders 9 numbered questions, none about project type; documented output config contains no `project_type` |
| **FR-05** | Routing doc reframed; SKILL.md references current-request detection | OD-01, OD-02 | L1 | T-05 | `grep -rn "project_type" delivery-team/skills/delivery-flow/` returns only deprecation notes, Phase 1 prose, and `project-types.md` framing |
| **FR-06** | Delegation Prime Directive section in SKILL.md | OD-05 | L1, L2 | T-06 | Section exists as first prose block post-metadata; referenced from Step 4.5, stage execution, and anti-patterns section |
| **FR-07** | Step 4.5 rejects "simple" justifications | OD-06 | L1, L2 | T-07 | Step 4.5 contains explicit rejection clause; links to anti-patterns section |
| **FR-08** | Anti-Patterns section with all 6 named patterns | OD-05 | L1, L2 | T-08 | Section exists; all 6 anti-patterns present with name + description + correct alternative |
| **FR-09a** | Hook denies orchestrator-attributed Write to artifact path | OD-07 | L3 | T-09a | Fixture: env var unset, path `.delivery/artifacts/02-refine/po/prd.md`, active pipeline, flag on → hook emits `permissionDecision: deny` |
| **FR-09a'** | Hook allows sub-agent-attributed Write to same path | OD-07 | L3 | T-09a-prime | Fixture: `DELIVERY_FLOW_AGENT_CONTEXT=po` set, same path → allow |
| **FR-09a''** | Hook allows Write to allowlisted paths regardless | OD-07 | L3 | T-09a-allow | Allowlist: orchestrator AND sub-agent writes to `state.md`, `memory/**`, `config.yml`, stage `state/`, `handoff/` paths → allow |
| **FR-09b** | Hook blocks Bash heredoc redirection to artifact path | OD-07 | L3 | T-09b | Fixture: `Bash` tool with `cat > .delivery/artifacts/...  <<EOF` → deny. Variants for `>`, `>>`, `tee`, `dd of=`, `cp`, `mv` |
| **FR-09c** | Hook allows sub-agent Bash redirection to same path | OD-07 | L3 | T-09c | Same Bash commands with env var set → allow |
| **FR-09d** | Soft-deny fallback when detection unreliable | OD-07 | L3 | T-09d | Env var unset AND Layer 2 metadata absent → `systemMessage` warning emitted; hook does NOT deny; exit 0 |
| **FR-09e** | Known gaps documented in hook docstring + `quality-gates.md` | OD-07 | L1 | T-09e | Docstring lists MCP writes, `git checkout/apply`, sub-process inheritance caveat. `quality-gates.md` mirrors the list |
| **FR-09 gating** | Deny gated on `schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true` | OD-07 | L3 | T-09g | v2.6 tolerant config → warn only, never deny. Fresh v2.7 → deny active |
| **FR-10** | "One Role = One Sub-Agent" rule in SKILL.md | OD-08 | L1, L2 | T-10 | Rule block exists adjacent to Prime Directive; referenced by name from `team-patterns.md`, `quality-gates.md`, `pipeline-stages.md` |
| **FR-11** | Dispatch rule one-liner on every pattern in reference docs | OD-09 | L1 | T-11 | All 6 patterns in `team-patterns.md` lead with "Dispatch rule:"; `quality-gates.md` and `pipeline-stages.md` have the called-out additions |
| **FR-12** | Compound-role prompt detector (MAY) | OD-10 | L3 | T-12 | If implemented: synthetic compound prompt → `systemMessage` warning; single-role prompt → silence. If deferred: documented decision in plan artifact |
| **FR-13** | Isolated Adversarial Loop pattern w/ convergence rules + taxonomy | OD-11 | L1, L2 | T-13 | Pattern section contains all 4 protocol steps, three convergence rules (two-clean, no-new-classes, hard-cap), issue-class taxonomy, no-context-leak guarantee |
| **FR-14** | Stage 4 in `pipeline-stages.md` references the pattern by name | OD-12 | L1 | T-14 | Stage 4 section names "Isolated Adversarial Loop" and bounds loop count by `max_self_correction` |
| **FR-15** | `max_self_correction` documented in v2.7 schema with Architect-loop use | OD-04, OD-11, OD-12 | L1 | T-15 | `config-schema.md` v2.7 entry for `max_self_correction` lists "Architect adversarial loop cap" as a use; default remains `3` |
| **FR-16** | Schema bump + doc parity across CLAUDE.md, README.md, marketplace.json, docs/** | OD-04, OD-13 | L1 | T-16 | `grep -rn "2\.6" CLAUDE.md README.md .claude-plugin/marketplace.json docs/` returns only changelog/historical references; live docs say 2.7 |

### NFR coverage map

| NFR | Test Level | Test ID | Pass condition |
|---|---|---|---|
| NFR-01 hook p95 ≤ 50ms | L4 | T-N01 | 200-sample p95 ≤ 50ms on dogfood machine; < 15ms added over v2.6 baseline |
| NFR-02 stdlib only | L1 | T-N02 | `grep -n "^import\|^from" delivery-team/hooks/*.py` shows only stdlib modules |
| NFR-03 v2.6 backwards compat | L3, L5 | T-N03 | v2.6 fixture with `project_type: GREENFIELD` loads without error across both hook gating and config loader |
| NFR-04 doc parity | L1 | T-N04 | Same as T-16 |
| NFR-05 graceful hook degradation | L3 | T-N05 | Inject synthetic exception inside hook logic; confirm `try/except → sys.exit(0)`; no stack trace escapes |
| NFR-06 dogfood | L5 | T-N06 | This bundle ships via a `/delivery-flow` run; orchestrator artifacts are all sub-agent-attributed |
| NFR-07 plugin-dev skill enforcement | L1 | T-N07 | Developer-stage DoD evidence shows `plugin-dev:skill-development` / `plugin-dev:hook-development` loaded before respective edits |
| NFR-08 atomic merge | L1 | T-N08 | Single PR contains all OD-01 – OD-13 file changes; no interleaved prior commits on shared files |

---

## 4. Testing Strategy: Documentation / Protocol Changes

The majority of this bundle is prose. Prose cannot be unit-tested, but it can be structurally audited and behaviorally walked.

### 4.1 L1 — Structural grep checks

Executed as a single shell script at the end of the Development stage. All assertions must pass before handoff to UAT.

```
# FR-01/FR-05 — project_type no longer drives config
grep -rn "project_type" delivery-team/skills/delivery-flow/ \
  | grep -v -E "(Deprecated|deprecation|Phase 1|project-types\.md|legacy)"
# Expected: empty

# FR-16 — schema version parity
grep -rn "2\.6" CLAUDE.md README.md .claude-plugin/marketplace.json docs/
# Expected: only changelog / historical references

# FR-06/FR-08/FR-10 — SKILL.md anchors
grep -n "Delegation Prime Directive\|Common Orchestrator Anti-Patterns\|One Role = One Sub-Agent" \
  delivery-team/skills/delivery-flow/SKILL.md
# Expected: all three present

# FR-11 — dispatch rule on every pattern
grep -n "^Dispatch rule:" delivery-team/skills/delivery-flow/references/team-patterns.md
# Expected: >= 6 occurrences (one per pattern)

# FR-13 — convergence criteria present
grep -n "two-clean\|no-new-classes\|class_saturated\|cap_reached" \
  delivery-team/skills/delivery-flow/references/team-patterns.md
# Expected: all four terms present
```

### 4.2 L2 — Protocol walk-through (manual, two-reader)

Documentation is only as good as the behavior it induces in a future orchestrator. For each protocol-touching story (OD-02, OD-05, OD-06, OD-08, OD-11, OD-12), two readers perform a dry run:

- **Reader A ("orchestrator")**: reads only the revised SKILL.md and referenced docs, then narrates the correct action for a set of scripted prompts (one BUG_FIX request, one GREENFIELD request, one DOCS_ONLY request, one adversarial-review scenario).
- **Reader B ("auditor")**: compares narration to the FR acceptance criteria and flags any ambiguity, missing anchor, or interpretable escape hatch.

Pass condition: Reader A arrives at the intended behavior without Reader B having to supply missing context. Any "well, obviously you'd..." moment from Reader B is a defect.

### 4.3 Dogfooding

Per NFR-06, the canonical test of the documentation changes is the next `/delivery-flow` invocation after merge. The orchestrator MUST, on that run:

1. Run Phase 1 detection from the current request (FR-03). Evidence: `state.md` shows a fresh detection line.
2. Attribute every artifact write to a named sub-agent role (FR-06/FR-09). Evidence: hook logs show no orchestrator-origin write attempts denied.
3. Dispatch one sub-agent per reviewer role at every review gate (FR-10). Evidence: transcript shows N distinct Agent invocations for an N-role review board.
4. Execute at least one adversarial loop iteration at Architect with a fresh reviewer per loop (FR-13/FR-14). Evidence: Architect stage artifacts show loop metadata (`N`, `status`, class tags).

The dogfood run is not pass/fail for *this* bundle's PRD acceptance (that would be circular, per ADR-001 §2.5 activation gating). It is pass/fail for the sprint retrospective and for confidence in shipping.

---

## 5. Testing Strategy: Hook Code Extensions

`enforce_pipeline_scope.py` and (optionally) `audit_agent_prompt.py` are the only executable code in this bundle. They are tested via fixture-driven stdlib Python runners under `delivery-team/tests/` — no pytest, no external dependencies.

### 5.1 Test harness layout

```
delivery-team/
  tests/
    fixtures/
      legacy-v2.6-config.yml        # FR-02a / NFR-03
      v2.7-force-type-config.yml    # FR-02b
      v2.7-dual-key-config.yml      # FR-02c
      hook-input-orchestrator.json  # env var unset
      hook-input-subagent.json      # env var set via runner env
      hook-input-bash-heredoc.json  # FR-09b
      hook-input-bash-redirect.json
    test_enforce_pipeline_scope.py  # standalone runner (no pytest)
    test_audit_agent_prompt.py      # standalone runner (optional / OD-10)
    test_hook_perf.py               # NFR-01 timing loop
    run_all.sh                      # runs every standalone runner, exits nonzero on any failure
```

Per PQ-2 (architecture open question forwarded to Plan), fixture files live under `delivery-team/tests/fixtures/`. This matches the architecture's recommendation and is consistent with the repo-wide "no test runner" constraint.

### 5.2 Origin detection tests (FR-09, ADR-001)

The hook reads PreToolUse JSON from stdin and (now) reads `DELIVERY_FLOW_AGENT_CONTEXT` from the environment. The runner constructs each scenario by:

1. Setting or unsetting `DELIVERY_FLOW_AGENT_CONTEXT` in `subprocess.Popen(env=...)`.
2. Piping a fixture JSON into the hook's stdin.
3. Capturing stdout (decision JSON) and exit code.
4. Asserting against the expected decision.

**Origin detection truth table** (each row = one test case):

| # | Env var | Layer 2 metadata | Path | Tool | Active pipeline | Flag on | Expected | Test ID |
|---|---|---|---|---|---|---|---|---|
| 1 | unset | absent | `.delivery/artifacts/02-refine/po/prd.md` | Write | yes | yes | **deny** | T-09a |
| 2 | `po` | n/a | same | Write | yes | yes | **allow** | T-09a-prime |
| 3 | unset | absent | `.delivery/state.md` | Write | yes | yes | **allow** (allowlist) | T-09a-allow-1 |
| 4 | unset | absent | `.delivery/config.yml` | Write | yes | yes | **allow** (allowlist) | T-09a-allow-2 |
| 5 | unset | absent | `.delivery/memory/session.md` | Write | yes | yes | **allow** (allowlist) | T-09a-allow-3 |
| 6 | unset | absent | `.delivery/artifacts/02-refine/po/state/foo.md` | Write | yes | yes | **allow** (allowlist) | T-09a-allow-4 |
| 7 | unset | absent | artifact path | Bash: `cat > .delivery/artifacts/.../prd.md <<EOF` | yes | yes | **deny** | T-09b-heredoc |
| 8 | unset | absent | artifact path | Bash: `echo "..." > .delivery/artifacts/...` | yes | yes | **deny** | T-09b-redir |
| 9 | unset | absent | artifact path | Bash: `tee .delivery/artifacts/.../prd.md` | yes | yes | **deny** | T-09b-tee |
| 10 | unset | absent | artifact path | Bash: `dd of=.delivery/artifacts/.../prd.md` | yes | yes | **deny** | T-09b-dd |
| 11 | unset | absent | artifact path | Bash: `cp /tmp/x .delivery/artifacts/.../prd.md` | yes | yes | **deny** | T-09b-cp |
| 12 | unset | absent | artifact path | Bash: `mv /tmp/x .delivery/artifacts/.../prd.md` | yes | yes | **deny** | T-09b-mv |
| 13 | `architect` | n/a | artifact path | same Bash variants | yes | yes | **allow** | T-09c |
| 14 | unset | absent | artifact path | Bash: `ls .delivery/artifacts/` (no redirection) | yes | yes | **allow** (not a write) | T-09-readonly |
| 15 | unset | absent | artifact path | Write | yes | **flag off** (v2.6 tolerant) | **warn only** | T-09g-v26 |
| 16 | unset | absent | artifact path | Write | **no** (no active pipeline) | yes | **allow** | T-09-nopipe |
| 17 | unset | Layer 2 present (sub-agent marker) | artifact path | Write | yes | yes | **allow** | T-09-layer2 |
| 18 | unset | both layers absent | artifact path | Write | yes | yes | **soft-deny warning, not deny** | T-09d |
| 19 | unset | absent | source file inside `pipeline.scope` | Write | yes | yes | **deny** | T-09-scope |
| 20 | unset | absent | source file outside `pipeline.scope` | Write | yes | yes | **allow** | T-09-out-of-scope |

Edge cases specifically covered:

- **Path traversal**: `.delivery/artifacts/../../etc/passwd` → path normalization must occur before allowlist check; expected `allow` (out of scope) without leaking the traversal.
- **Symlinked artifact paths**: fixture creates a symlink inside `.delivery/artifacts/`; hook must resolve before scope check.
- **Mixed redirection**: `echo a > /tmp/x && cp /tmp/x .delivery/artifacts/.../prd.md` → the `cp` half triggers deny.
- **Harmless Bash with incidental `>`**: `find . -name "*.md" > /tmp/list.txt` → allow (target is not in scope).
- **Quoted paths**: `cp /tmp/x ".delivery/artifacts/02-refine/po/prd.md"` → deny.

### 5.3 Compound-role prompt detection tests (FR-12, OD-10, optional)

Run only if OD-10 is not deferred. If deferred, the decision must be recorded in `quality-gates.md` as a known limitation.

| # | Prompt fragment | Expected | Test ID |
|---|---|---|---|
| 1 | "Review this architecture as both the security architect and the data architect." | warn | T-12-pos-1 |
| 2 | "Play the role of architect, developer, and QA and produce a review." | warn | T-12-pos-2 |
| 3 | "You are the adversarial reviewer." | silent | T-12-neg-1 |
| 4 | "Review this from the architect perspective." (single role) | silent | T-12-neg-2 |
| 5 | "Don't act as both security and compliance — act only as security." (negation-aware) | silent | T-12-neg-3 |
| 6 | Prompt contains 3+ known role names as nouns in a bulleted list | warn | T-12-pos-3 |

FR-12 is explicitly MAY. A false-positive rate > 10% on the negation-aware cases is grounds for deferral.

### 5.4 Performance test (NFR-01)

`test_hook_perf.py` loops 200 synthetic PreToolUse calls through the hook's `main()` and records p50, p95, p99 wall-clock using `time.perf_counter()`. Baseline comparison is done by running the same loop against the pre-bundle version of the hook (git stash or separate checkout).

- **Pass**: p95 ≤ 50ms absolute AND p95 delta ≤ 15ms vs. baseline.
- **Fail**: either threshold exceeded → regression defect → Architect review.

### 5.5 Graceful degradation test (NFR-05)

A single test case injects a synthetic exception via monkey-patching the hook's inner `detect_origin()` function (the runner imports the hook as a module and patches) and asserts:

- Hook exits 0.
- No stack trace printed to stderr.
- If deny was supposed to fire, it does NOT — the crash path must never block the user.

---

## 6. Integration Testing: Does the Orchestrator Actually Behave?

This section answers the PRD question head-on: after the changes ship, does the orchestrator actually behave per the new rules? No amount of doc auditing and hook fixture tests can substitute for a real end-to-end run.

### 6.1 Scenario matrix (dogfood run, post-merge)

Executed as the first `/delivery-flow` invocation after merge on a clean scratch repo seeded with a v2.7 config.

| Scenario | Request | Expected routing | Expected artifacts | Evidence |
|---|---|---|---|---|
| **S1** | "Fix a typo in README.md" | BUG_FIX (or DOCS_ONLY depending on detection vocabulary) | Minimal stages; all artifacts sub-agent-attributed | `state.md` Phase 1 line; hook log empty of deny events |
| **S2** | In same repo, next invocation: "Build a new caching layer" | GREENFIELD or FEATURE (different from S1) | Full pipeline | `state.md` shows different routing than S1 — proves FR-03 |
| **S3** | v2.7 config has `routing.force_type: DOCS_ONLY`; request: "Add a new Python module" | DOCS_ONLY (pin wins) | Docs-only stages | Banner: "project_type forced to DOCS_ONLY by routing.force_type — detection result was ..." |
| **S4** | Swap in v2.6 legacy fixture with `project_type: GREENFIELD`; request: "Fix a null-pointer bug" | BUG_FIX (detection wins; legacy ignored) | Banner contains "legacy `project_type` ignored — re-detecting from request" | `state.md` run log |
| **S5** | Any request that triggers Architect stage | Architect runs ≥1 adversarial loop with fresh reviewer per iteration | Architect handoff contains loop metadata | Architect artifact shows `loops: [...]`, `status: converged` or `cap_reached` |
| **S6** | Review gate with multi-role review board | N distinct Agent tool invocations, one per role | Transcript shows independent sub-agent calls | Transcript inspection |
| **S7** | Orchestrator attempts to Write an artifact directly (hostile test) | Hook denies; orchestrator recovers by dispatching sub-agent | Hook log shows deny event | Hook stderr / systemMessage |
| **S8** | Orchestrator attempts `cat > .delivery/artifacts/.../file.md <<EOF` (hostile Bash) | Hook denies | Hook log shows deny event on Bash tool | Hook log |

**Hostile tests (S7, S8)** are essential. They are the only way to prove the hook actually intercepts the failure mode the PRD was written to prevent. They MUST be executed with `pipeline.enforce_self_write_block: true` and a v2.7 schema.

### 6.2 Integration pass criteria

The bundle is judged integration-passing when all of the following hold on the post-merge dogfood run:

1. Every OD-01 – OD-13 story's acceptance criteria has direct evidence in the run transcript or artifacts.
2. Zero orchestrator-attributed writes to `.delivery/artifacts/**` or in-scope source paths complete successfully. Any attempts are denied and recovered.
3. Every review gate dispatches N sub-agents for N roles. Zero compound-role prompts appear in agent tool input.
4. Architect stage shows at least one adversarial loop with the convergence metadata from ADR-003. If the cap is reached, residuals are surfaced to the human checkpoint.
5. Both S1 and S2 produce different Phase 1 detection results in the same repo, in the same session — this is the single most important behavioral proof that FR-03 landed.

### 6.3 Known non-integration-testable gaps (surfaced to UAT checkpoint)

Per FR-09 architecture §2 and the hook's known-limitations list, these paths remain unchecked by the hook and cannot be exercised in integration:

- Writes by MCP server tools that bypass the standard tool surface.
- File materialization via `git checkout` / `git apply`.
- Writes by sub-processes spawned from a sub-agent (correctly attributed via env var inheritance — not a gap, but noted).

These are documented, not tested. Human reviewer at UAT acknowledges them as accepted residual risk.

---

## 7. Test Execution Plan (sequenced with stories)

Tests are executed co-located with their stories (per capacity rule in stories.md). No separate test phase.

| Story | Test batch | Level(s) | Gate |
|---|---|---|---|
| OD-01 | T-01a, T-04, T-05 | L1, L2 | Story DoD |
| OD-02 | T-03 (dry run), T-05 | L2 | Story DoD |
| OD-03 | T-02b, T-02c (dry fixture render) | L2 | Story DoD |
| OD-04 | T-01b, T-02a, T-15 | L1, L2 | Story DoD |
| OD-05 | T-06, T-08 | L1, L2 | Story DoD |
| OD-06 | T-07 | L1, L2 | Story DoD |
| OD-07 | T-09a / T-09a-prime / T-09a-allow-* / T-09b-* / T-09c / T-09d / T-09e / T-09g / T-09-scope / T-09-out-of-scope / T-09-layer2 / T-09-readonly / T-09-nopipe / T-N01 / T-N02 / T-N03 / T-N05 | L1, L3, L4 | Story DoD — largest test batch |
| OD-08 | T-10 | L1, L2 | Story DoD |
| OD-09 | T-11 | L1 | Story DoD |
| OD-10 *(optional)* | T-12-pos-1/2/3, T-12-neg-1/2/3 | L3 | Story DoD or formal defer decision |
| OD-11 | T-13 | L1, L2 | Story DoD |
| OD-12 | T-14 | L1 | Story DoD |
| OD-13 | T-16, T-N04, T-N07, T-N08 | L1 | Sprint DoD |
| **Post-merge** | S1 – S8, T-N06 | L5 | UAT / dogfood retrospective |

---

## 8. Defects & Exit Criteria

**Defect severity**:

- **S1 / Critical**: any hook test failure (T-09*), p95 budget breach (T-N01), backwards-compat crash on v2.6 fixture (T-N03), or integration scenario S1/S2 failing to show distinct Phase 1 results. Blocks merge.
- **S2 / Major**: documentation grep assertion failure (T-01 – T-16 at L1), missing anchor, compound-role prompt in a real dispatched agent call during dogfood. Blocks merge unless waived at sprint DoD.
- **S3 / Minor**: stylistic ambiguity flagged at L2 walk-through that does not change orchestrator behavior. Logged, not blocking.

**Exit criteria for the bundle**:

- All S1 defects resolved.
- All FRs and NFRs have a green test ID in §3.
- Atomic-merge PR contains all OD-01 – OD-13 file changes (T-N08).
- Post-merge dogfood run completes S1 – S8 with pass evidence captured in the retrospective artifact.
- If OD-10 is deferred, the deferral is explicitly recorded in the plan artifact and in `quality-gates.md`.

---

## 9. Open Items Forwarded

- **Q-QA-1**: Confirm with Developer during OD-07 whether Layer 2 (hook input metadata) will actually resolve on the current Claude Code harness version. If not, Layer 1 (env var) is load-bearing and the soft-deny fallback (Layer 3) becomes the only safety net for env var injection failures. Test T-09d becomes higher priority.
- **Q-QA-2**: The v2.6 legacy fixture must be committed alongside OD-04 so T-02a and T-N03 can run. If the developer omits it, those tests cannot execute.
- **Q-QA-3**: The dogfood run's Architect stage (S5) needs a request complex enough to actually trigger more than one adversarial loop iteration. PO to select the request for the post-merge run; a trivial docs-only request will not exercise FR-13's convergence algorithm.

---

*"A marksman does not test the bow by firing one arrow. He fires many, at many distances, in many winds — and only then trusts the string. So it is with this bundle: we will draw the hook again and again, we will walk the protocol with two sets of eyes, and we will let the next real pipeline run be the final witness."*

— Legolas, QA

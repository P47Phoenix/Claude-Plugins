# QA Review — Architect Stage Artifacts

**Reviewer**: Legolas (QA)
**Stage**: 04 — Architect (FEATURE-light)
**Scope**: architecture.md, ADR-001 (origin detection), ADR-003 (adversarial loop convergence)
**Date**: 2026-04-05

> *"My eyes see far. I will tell you only what can be measured, struck, or counted."*

---

## Verdict: DONE

All three artifacts present testable success criteria, measurable termination conditions, and falsifiable decisions. Findings below are recommended test hooks for Plan/Quality stages, not blockers.

---

## 1. Origin Detection — Testability (ADR-001 + arch §2)

### Success criteria are clear and verifiable

| Behavior | Falsifiable test |
|---|---|
| Layer 1: env var present ⇒ allow | Set `DELIVERY_FLOW_AGENT_CONTEXT=architect`, attempt write to `.delivery/artifacts/04-architect/x.md`, assert exit 0 + write proceeds |
| Layer 1: env var absent ⇒ fall through | Unset env var, attempt orchestrator-origin write, assert Layer 2 path executes |
| Layer 2: positive sub-agent identifier ⇒ allow | Inject mock hook stdin with `parent_tool_use_id` populated, assert allow |
| Layer 3: both signals absent ⇒ warn-not-deny | No env var, no parent id, attempt write, assert exit 0 AND `systemMessage` emitted naming Delegation Prime Directive |
| Allowlist always allows | For each path in §2.3, attempt write with no env var, assert allow |
| Bash redirection coverage | Bash `cat <<EOF > .delivery/artifacts/foo.md` with no env var, assert same Layer 1→2→3 behavior |
| Activation gating | v2.6 config OR `enforce_self_write_block: false` ⇒ deny path never reached even when origin = orchestrator |
| NFR-01 budget | Measure p95 hook latency over N=1000 invocations, assert ≤ 50ms |

### Falsifiability of the decision
ADR-001 names rejected alternatives (A-alone, B-alone, C, D, hard-deny) with concrete failure modes. Each rejection is independently testable.

### Observations (non-blocking)
- **PQ-1 unresolved**: Layer 2's `parent_tool_use_id` reliance is harness-version-dependent. Plan stage must pin a harness version for the test matrix.
- **Allowlist drift**: recommend a unit test that asserts the module constant matches the documented §2.3 list verbatim.
- **Layer 3 telemetry**: ADR-001 says soft-deny "should be monitored" but no counter/log channel is named. Recommend logging Layer 3 hits to `state.md` so QA can grep them post-run.

---

## 2. Adversarial Loop Convergence — Testability (ADR-003 + arch §4)

### Termination conditions are measurable

All three exit conditions are decidable from loop history alone, no AI judgment required:

| Rule | Decidability check |
|---|---|
| Two-clean | `len(loops[-1].findings) == 0 AND len(loops[-2].findings) == 0` |
| No-new-classes | Set membership over `classes`, two consecutive loops with no novel class |
| Hard cap | `N >= max_self_correction` integer comparison |

These are pure data assertions over the `loops` list — replayable with synthetic finding streams.

### Recommended test matrix

| Scenario | Synthetic input | Expected exit |
|---|---|---|
| Immediate two-clean | `[[],[]]` | converged(two_clean), N=2 |
| Lucky single clean then findings | `[[],[coupling]]` | continue (does not exit on N=1 clean) |
| Class saturation | `[[coupling],[security],[coupling],[security]]` | converged(class_saturated) |
| Pure novelty stream | new class each loop, length 3 | cap_reached, N=3 |
| Untagged finding | `[[{class:None}]]` | counted as `misc`, treated as new class |
| Taxonomy evasion | `[[{class:"COUPLING"}],[{class:"coupling-ish"}]]` | both bucketed `misc`, no false saturation |
| Cap with default 3 | findings every loop, all novel | cap_reached at N=3, residuals documented |

### Falsifiability
ADR-003 rejects A (one-clean), C (severity), E-alone, B-alone, three-clean — each with a stated failure mode that the matrix above can reproduce.

### Observations (non-blocking)
- **Default cap = 3 + two-clean rule = only 1 fix iteration**. ADR-003 acknowledges this. Recommend Quality stage measure cap_reached frequency on the dogfood run; if > 50%, raise default to 4 in a follow-up.
- **Architect-revision context scoping** is asserted as invariant. Recommend a test that inspects the dispatched Architect prompt and asserts it does NOT contain prior-loop finding strings.
- **Reviewer context isolation**: unit test should mock the dispatcher and assert each reviewer prompt contains exactly `[artifact, reviewer_brief, taxonomy]` and nothing else.
- **Pseudocode timing**: §4.3 `if len(loops) >= 3` means class-saturation cannot fire until N=3. With default cap=3 it can only fire on the very last loop before cap_reached. Consistent with spec but should be noted in `team-patterns.md` so reviewers understand it.

---

## 3. ADR Falsifiability — Per Decision

| Decision | Falsifiable? | How to falsify |
|---|---|---|
| ADR-001: layered detection > single mechanism | Yes | Demonstrate that A or B alone meets all FR-09 + NFR-05 cases on the harness in use |
| ADR-001: soft-deny on uncertainty | Yes | Show a production incident where soft-deny allowed a destructive write, AND a hard-deny variant would not have bricked the pipeline |
| ADR-001: allowlist scope | Yes | Find a legitimate orchestrator bookkeeping path NOT in §2.3, OR an in-list path that should have been denied |
| ADR-003: two-clean > one-clean | Yes | Show a stream where one-clean exits correctly and two-clean wastes a loop with no benefit, repeated across N runs |
| ADR-003: class saturation > severity threshold | Yes | Run both on the dogfood corpus, compare false-converge / false-continue rates |
| ADR-003: misc bucket counts as new class | Yes | Show a reviewer using `misc` legitimately and having class-saturation incorrectly delayed |
| ADR-003: cap_reached is exit not failure | Yes (policy) | Show human checkpoint cannot in practice make an informed accept/reject decision from the residuals format |

Every decision is bound to an observable outcome on a finite test stream.

---

## 4. Cross-Cutting QA Concerns

### Pass
- Edit map (§5) is gateable: each row has FR back-reference and a concrete file. Doc-parity DoD can be a deterministic grep.
- NFR table (§6) gives every NFR a budget AND an architectural hook.
- Activation gating (§2.5) makes the dogfood run testable without circular dependency.

### Recommendations for Plan stage (non-blocking)
1. Define the test fixture path for `enforce_pipeline_scope.py` (PQ-2 mentions `delivery-team/tests/fixtures/legacy-v2.6-config.yml`). Standalone Python script that exits non-zero on assertion failure.
2. Specify the `routing.force_type` enum exhaustively (PQ-3) so parser tests can be table-driven.
3. Bash-redirection regex needs a positive AND negative test set (e.g., `grep > /dev/null` must not match an artifact path).
4. End-to-end smoke test for the dogfood activation gate: v2.6 config (deny unreachable), v2.7 + flag false (same), v2.7 + flag true (deny fires).

---

## 5. Falsifiability Summary

| Artifact | Testable | Measurable | Falsifiable | Verdict |
|---|---|---|---|---|
| architecture.md | Yes | Yes | Yes | Pass |
| ADR-001 | Yes | Yes | Yes | Pass |
| ADR-003 | Yes | Yes | Yes | Pass |

---

## STATUS

**DONE** — Architecture and ADRs are testable, success criteria are measurable, and every decision is falsifiable. Observations above are recommended Plan-stage test inputs, not gate failures.

> *"The arrow flies true when the bow is straight. This bow is straight."*

— Legolas

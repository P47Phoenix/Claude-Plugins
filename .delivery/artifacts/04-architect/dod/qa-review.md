<!-- run: run-2026-05-28-o48m -->
---
verdict: DONE
round: 3
role: qa (DoD validator, fresh reviewer)
stage: 4 Architect (light)
run: run-2026-05-28-o48m
backlog: BACKLOG-108
blocking_count: 0
warning_count: 4
inputs: architecture.md rev 5, ADR-lmr-004 s2 and s6 (1a..1d), ADR-lmr-002 D9, ADR-lmr-005, round-2 review
note: delivery-team:qa skill failed to load (unknown skill); role applied from the task brief.
experiment: $CLAUDE_JOB_DIR/tmp/exp (gate2.py, mk2.py, red2.py, re-run) and tmp/qa3/adv.py (my own adversarial P0s)
---

# QA DoD review round 3: Stage 4 design, BACKLOG-108

Short version. B2 closed. No blocking gap found. Correct P0 passes gate and gives only permitted red markers. Wrong P0s I built either fail the gate or fail the red run. Gate has holes (decorator, module-level statement, signature default), but red run covers each one. Warnings only.

## Blocking issues

None.

## B2 closure check

Re-ran architect's `gate2.py`: correct PASS; computed `session_id` FAIL; computed `cache_hit_ratio` FAIL; edited `cost_usd` FAIL; `metrics[...] = 0.0` assign FAIL; new-fn impl FAIL `not inert`; pre-existing fn body edit FAIL; class method FAIL; non-const field FAIL. Matches ADR text.

Re-ran `red2.py` on correct P0: rc 1, 6 failures, 0 errors. Markers: 5x `AssertionError`, 1x `Failed: DID NOT RAISE`. All permitted.

Each B2 point:
1. `tokens.cache_hit_ratio` is now the nested-dict entry (1b(ii)). Correct P0 passes; test reads `report["tokens"]["cache_hit_ratio"]` and fails `AssertionError`. Closed.
2. `Metrics` fields pinned by 1d. `m.model_primary` and `m.models_observed` fail `AssertionError`, not `AttributeError`. Closed.
3. `model_pin_env` is in the pinned-key set. Test on it fails `AssertionError`. Closed.
Also checked ADR s2 table: only `build_report` changes body at P0. Signature-only changes (`_spawn_and_tee`, `compare`, `run_pipeline`) pass 1a because signature is excluded. No correct P0 element found that the gate rejects.

## My adversarial P0s (tmp/qa3/adv.py, built on real lib copy, gate = gate2.py, red = 6 tests)

| Variant | Gate | Red run (fails of 6) | Result |
|---|---|---|---|
| correct | PASS | 6 | baseline OK |
| `model_resolved: ["m"]` (const equals test expectation) | PASS | 5, one test PASSES | caught by red |
| decorator on `parse_stream` (inline lambda, sets `model_primary`) | PASS | 5 | caught by red |
| module-level `parse_stream = (lambda f: ...)(parse_stream)` rebind | PASS | 4 | caught by red |
| module-level `Metrics.model_primary = property(...)` (import-time patch, class body untouched) | PASS | 5 | caught by red |
| `build_report = (lambda f: ...)(build_report)` at end of report.py | PASS | 5 | caught by red |
| lambda default in `build_report` signature | PASS | 6 | inert, no effect on tests |

Every smuggle that changes behaviour makes a red test pass, which violates "every test FAILED". So no wrong P0 passes both gate and red run for behaviour that a test covers. A leak no test covers cannot void red-first evidence for that behaviour.

## Non-blocking warnings

### W1. Gate 1a/1c blind spots (red run is the sole catcher there)
1a excludes decorators and signatures. Rule 1c says new top-level names are limited, but `gate2.py` implements no top-level check, and module-level statements (rebind, attribute patch, import-time side effect) are not gated at all. All four gate-PASS behavioural smuggles above were caught only by the red run. Plan AC should either add: decorator lists and module-level statements equal `base_sha` (plus the allowed new classes and stubs), or state plainly that red run is the control for these.

### W2. Architect's hardcode experiment was weak
`mk2.py` hardcode uses `"claude-opus-fixture"` but the test expects `"m"`, so 6 tests failed there, not the "5 failed, 1 passed" the ADR quotes. My `["m"]` run gives 5 failed, 1 passed, so the claim holds; fix the citation when text is touched. Real validator tests take the expected id from the fixture, so a same-fixture-id hardcode is the case that matters.

### W3. Carried from round 2, still open (Plan AC text)
- Canary is not in the ADR-lmr-005 Block A step 0 list or the S7b re-run list (step 4 claims it is). Add it to both.
- D9 `files-scanned` K=0 exit 2 must state default mode only; `--paths` with out-of-scope staged files would block a pre-commit under `MODEL_PIN_STRICT=1`. D5 exit-code list lacks 2; two headings named D9.
- AC-5.5c distinct-hash/session/`message.id` rule missing from Plan-carry 3; no fallback stated if real events carry no `message.id`.

### W4. Carried, unchanged
Step 9 spend-log ordering wording (now largely fixed by the durable `$SMOKE_OUT` and tracked `s5b-spend.txt`; recheck wording), manifest recovery depends on CLI transcript layout, R-1..R-6 and P1, P2, P16, P21, P22 stay accepted residuals with PO as owner.

## Verdict

DONE. 0 blocking. W1 to W4 go to Plan as AC text.

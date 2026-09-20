<!-- run: run-2026-05-28-o48m -->
---
verdict: NOT_DONE
round: 2
role: qa (DoD validator, fresh reviewer)
stage: 4 Architect (light)
run: run-2026-05-28-o48m
backlog: BACKLOG-108
blocking_count: 1
warning_count: 6
inputs: architecture.md rev 4, ADR-lmr-001..005, round-1 review, real lib/ sources
note: delivery-team:qa skill failed to load (unknown skill); role applied from the task brief.
experiment: $CLAUDE_JOB_DIR/tmp/exp (gate.py, mk.py, setup.py, p0/tests/test_red.py, junit.py)
---

# QA DoD review round 2: Stage 4 design, BACKLOG-108

Short version. B1 as I wrote it is fixed: a correct stub now passes the AST gate and gives the two allowed failure markers. But the rewritten rule 1b(ii) and the P0 stub scope do not match the real code, so one new blocking gap remains (B2, same defect class: P0 rule cannot carry what the tests need). Four "pass while unmet" holes are closed in design. Small fix again.

## Blocking issues

### B2. P0 stub rule cannot carry `tokens.cache_hit_ratio` or the new `Metrics` fields (ADR-lmr-004 section 6 item 1b, section 2, section 1 item 6)

Evidence from the experiment (real `lib/report.py` and `lib/metrics.py` copied to scratch; gate coded from 1a to 1c; pytest run against a gate-passing P0).

1. Rule 1b(ii) names "the single assignment `metrics["tokens.cache_hit_ratio"] = ...`". In the real `build_report` there is no such assignment target. `metrics` is the `Metrics` dataclass parameter, and the report is one returned dict literal with a nested `"tokens"` dict; `tokens.cache_hit_ratio` is resolved by `baseline._extract_metric` as `report["tokens"]["cache_hit_ratio"]`. Results:
   - `A_top_only` (six pinned keys, constants): gate PASS. But `report["tokens"]["cache_hit_ratio"]` is absent, so a test that reads it fails with `KeyError`, which VOIDS the red evidence.
   - `A_with_nested` (also adds `"cache_hit_ratio": 0.0` inside `tokens`, the only natural way to carry it): gate FAIL, `body differs after strip`. A correct P0 fails the gate.
   - `B_assign` (literal `metrics["tokens.cache_hit_ratio"] = 0.0` as the rule says): gate PASS, but at runtime `Metrics` is not subscriptable: `TypeError: 'Metrics' object does not support item assignment`. A dev who follows the text literally breaks every `build_report` call.
2. Section 1 item 6 adds `model_primary`, `models_observed` and `tokens.cache_hit_ratio` to `Metrics`. Nothing pins them at P0: not in the section 2 tables, not in the 1c new-symbol list (1c covers top-level names and functions, not fields of an existing class). Test `parse_stream(...).model_primary == ...` at `validator_start` fails with `AttributeError: 'Metrics' object has no attribute 'model_primary'` (run, junit message confirmed). `AttributeError` is on the void list.
3. `model_pin_env` is a report key at P1 (section 2 `build_report` row) but is not in the pinned-key set the gate strips, so a stub adding it fails 1a.

What DID work (B1 proper, confirmed by run): with a gate-passing P0, value tests using bare `assert` failed as `AssertionError: ...`, and `pytest.raises(ModelCaptureError)` against an inert `check_model_capture` failed as `Failed: DID NOT RAISE <class ...>`; both are the two permitted markers, both as `<failure>` elements. So the failure-type rule and the "inert, no NotImplementedError" rule are sound.

Effect: Plan cannot write a passing AC for "P0 passes 1a to 1c AND red run clean" for any test touching cache-hit ratio or `Metrics` fields, unless the validator happens to use `.get`/`getattr` (I confirmed `.get(...)` gives `AssertionError`; not stated anywhere).

Fix (architect, small, text only):
- 1b(ii): replace with "the pinned key `cache_hit_ratio` inside the nested `tokens` dict literal, constant value (`0.0`)", and add `model_pin_env` to the pinned-key set.
- P0 stub scope: list the `Metrics` field additions (`model_primary: str | None = None`, `models_observed: list = field(default_factory=list)`, `cache_hit_ratio: float = 0.0`) as allowed P0 class-body additions with constant defaults, or state the test-writing rule "read new attributes with `getattr(x, name, default)` / `dict.get`".

## Attack on the AST gate (wrong P0 that should fail)

| Variant | Gate result | Verdict |
|---|---|---|
| `session_id` computed from `metrics` (`metrics.tokens.get("input")`) | FAIL `nonconst pinned value` | caught |
| existing key edited (`cost_usd ... or 0.1`) | FAIL `body differs after strip` | caught |
| pre-existing `parse_stream`/`compare`/etc body change | FAIL by 1a (same mechanism) | caught |
| `model_resolved: ["<fixture id>"]` hardcoded constant | PASS | gate cannot see it; the red run catches it because the value test then PASSES, which fails the "every test FAILED" rule. OK, but the red run, not the AST, is the real control here. |
| real implementation smuggled into a NEW function (`check_model_capture` reading `metrics.models_observed`, `check_model_consistency` comparing `reports[i]["model_resolved"]`, raising `ModelCaptureError`) | PASS. 1c bans only `message`/`modelUsage`/`total_cost_usd` string literals and `NotImplementedError`; "return inert values" is prose, not an AST check. | see W1 |

## Re-check of the four "pass while unmet" holes

| Hole | Status | Evidence |
|---|---|---|
| AC-3.1b ignores rc | CLOSED (design) | ADR-lmr-002 D9 "AC-3.1b caller rules": rc in (0,1), last-line regex, `files-scanned` above 0, `n` equals summary `hits`. Ship step 4 judged on own rc. Plan must write the text (Plan-carry 3 lists it). |
| Guard scans nothing looks clean | CLOSED (design), see W2 | `files-scanned <K>` line before summary, exit 2 when K is 0 or `git ls-files` fails, fail closed on unreadable files, canary AC. |
| AC-5.5c five identical streams | CLOSED in ADR text, see W3 | ADR-lmr-004 section 5 and D9: distinct hash, distinct `session_id`, pairwise non-overlapping `message.id`; samples are now the full scrubbed stream so ids exist. |
| AC-DISP forged ids | CLOSED for recovered manifests; residual accepted | Item 4a fails (no skip) on a missing transcript; item 6 skip only if the whole slug tree is absent, printed loudly; missing id in any session dir fails; S7b always runs it. Role/unit match and self-forgery stay an accepted limit (F9), stated. |

Consistency checks:
- Guard summary vs `files-scanned`: the LAST stdout line stays `guard-scope hits N files M`; step 5 `tail -n 1 | awk '{print $3}'` still reads N; the `awk '/^(pin|stamp|prose) /'` count does not match the `files-scanned` line. Consistent.
- Spend numbers: $15.00 aggregate, $3.00 per sample, at most 2 re-runs (7 runs), `--max-budget-usd 0.25` and at most 2 fixture captures ($0.50) agree in ADR-lmr-004 section 8, architecture.md section 5 and changelog, ADR-lmr-005 step 9. The pre-check `spent + 3.00 > 15.00` is the binding limit in practice (7 x 3.00 is 21.00); "whichever hits first" covers it. Consistent.
- Canary in ship gate: NOT consistent, see W2.

## Non-blocking warnings

### W1. 1c "inert" is prose, not a check
A new function with a real body (no banned literals) passes 1c. Only the red run catches it, and only if a test exercises that function. Add to the Plan AC: new-function bodies must be a single `return <constant>` (or `json.load` for `load_baseline`) checked by AST, or say plainly that the red run is the sole control for new functions.

### W2. Canary is not wired into the gate steps it claims; `files-scanned` rule vs `--paths`
- ADR-lmr-005 step 4 says the canary "runs in Block A and again in S7b", but Block A step 0 enumerates only AC-2.1, AC-2.5, AC-4.4, AC-5.9b, and S7b "re-runs steps 4, 5, 6 and 7". The canary appears in neither list, so an executor following the step lists skips it. Add it to both.
- ADR-lmr-002 D9 exits 2 when K is 0. In `--paths` mode with only out-of-scope files staged (a `.json` baseline commit), K is 0, so the pre-commit hook gets rc 2 and blocks under `MODEL_PIN_STRICT=1`. State that the K=0 rule applies to default mode only. D5 (exit 0/1 only) is not updated to mention exit 2. There are also two headings named D9 in the ADR.

### W3. AC-5.5c gaps
The distinctness rule is not in Plan-carry item 3 (list omits it), and the PRD snippet is unchanged. `message.id` presence is UNVERIFIED (ADR-lmr-004 section 1 item 2 falls back to per-event); if real events carry no id, the disjoint-id check has nothing to compare and no fallback is stated. Add both to Plan-carry.

### W4. Manifest recovered form rests on the transcript layout
Layout observed on this CLI only; when a role was re-run in a later session the lookup must search all session dirs (stated). No change needed, note for the Plan checker.

### W5. Step 9 ordering
ADR-lmr-005 step 9 says the spend check runs "again at step 1" though it is listed last, and it reads the S5b reports in `${TMPDIR:-/tmp}/smoke-out`, which may not persist between the S5b dispatch and the ship session. Copy the spend log into the S5b commit trailer or a tracked note, or state the dir must persist.

### W6. Carried, unchanged
R-1 (uniform `latest` stamp on 22 files), R-2 (non-`.md` version words) and P1, P2, P16, P21, P22 stay open with PO as owner. Stage 6 cannot pass G5 closing ACs if baseline capture sits in Stage 7 (recorded in Plan-carry 4). Accepted as recorded.

## Verdict

NOT_DONE: 1 blocking (B2). Text-only fix in ADR-lmr-004 section 6 item 1b and the P0 stub scope; after that the design is DONE for Stage 4, W1 to W6 carried to Plan as AC text.

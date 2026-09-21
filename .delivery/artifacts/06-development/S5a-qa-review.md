run: run-2026-05-28-o48m
unit: S5a, QA DoD validation (fresh agent, not a09bb224d9d7f3689 / a950caefe7b2173e4 / aea281dd0dc0a78b9 / aa215877311314c70)
verdict: DONE

## Commits reviewed (origin/worktree-backlog-108-o48m..HEAD)
f391b0f P1 (Dispatch-Id aa215877311314c70); 4339a5e, c8ccf77, f563dba validator (aea281dd0dc0a78b9).
P0 stub: 5f5a079 (parent 515dcbc3832b28aba7d3f6419f05cc447c814131).

## Raw results (repo root)
- pytest delivery-team/tests/smoke/tests -q: `38 passed in 0.04s`
- check_p0_gate.py --base 515dcbc... --head 5f5a079: `P0_GATE OK`
- check_p0_gate.py --self-test: `SELFTEST OK 17/17`
- check_red_first.py --base f4fea7db... --manifest (a950caefe7b2173e4, aea281dd0dc0a78b9): `RED_FIRST OK failed=33 void=0`
  (checker also asserts producer/validator Dispatch-Id disjoint and validator ids in manifest; PA-13b satisfied: P1 id aa215877311314c70 is not in the validator set)
- git diff --stat 5f5a079 4339a5e -- lib run_smoke.py: empty (validator commits did not touch the P0 lib)
- check_distinct.py --self-test: `SELFTEST OK 10/10`
- spend_check.py --self-test: `SELFTEST OK 15/15`
- dry_run_baseline.py --out /tmp/dry-baseline.json: `DRYRUN NOTE fixture=real-shape`, `DRYRUN OK`, `DRYRUN ABORT_OK`, `DRYRUN CEILING_OK`
- check_model_pins.py --list: `files-scanned 494` / `guard-scope hits 0 files 0`
- check_skill_budgets.py: `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).`
- mutation_and_floor.py (lives at .delivery/artifacts/06-development/S1-guard-tests/, not repo root): `MUTATION OK 10/10 killed`, `K=494 live=494 B=485`, `FLOOR OK`

## P1 diff review vs AC-5.x
- cost_usd: metrics.cost_usd = result.total_cost_usd when present, else legacy sum; runner `_running_cost` replaces rather than adds. OK.
- Per-model dispatches: per_msg keyed by distinct message.id, last usage wins for split events, bucketed by message.model. OK. Tokens from result.usage when present.
- Copied-stream rejection: `_check_distinct_samples` rejects same sha256, repeated session_id, overlapping message.id, missing stream_file; samples[] carries stream_sha256. OK.
- Abort at first failed sample: `_init_baseline_flow` returns on any non-zero code and appends only exit-0 reports. OK.
- Schema v2: baseline, report SCHEMA_VERSION "2"; load_baseline rejects others (BaselineSchemaError); baseline adds model_requested/model_resolved/model_pin_env/effort/host_context/samples, model_usage.* informational, tokens.cache_hit_ratio advisory; ModelMovedError on inconsistent primary. OK.
- --max-budget-usd: `_build_claude_command` passes `--max-budget-usd {cost_cap:.2f}`; default --cost-cap 3.00 gives `3.00`. --effort sent only for opus. OK.
- model_pin_env: presence only ("set" or null) for four env var names, never values. OK.
- Budget-stop exit-2 mapping widened (`_result_failure`); model-capture failure maps to exit 4.

## Non-blocking notes
1. baselines/hello_world_spike.json is still schema_version "1". run_smoke normal (non-init) runs now fail exit 4 with a schema hard failure until S5b re-captures. The plan accepts this by design: D1 puts the paid `--init-baseline` capture in S5b (Stage 7 UAT, after S6 prose freeze, P6), the ADR says schema mismatch is rejected and never merged, and the S5a row lists no baseline file commit. The plan does not state the interim failure explicitly. The stale schema-1 file must not be relied on by any Stage 6 smoke run; S5b overwrites it.
2. Checker manifest was a temp file (/tmp/s5a-manifest.tsv, header line plus tab-separated role/id), not committed.
3. mutation_and_floor.py is not at repo root as the dispatch stated; run from its S1-guard-tests path.

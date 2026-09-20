<!-- run: run-2026-05-28-o48m -->
# Plan: Latest-Model References (BACKLOG-108)

Stage 5 Plan, light routing (all content present, depth reduced). Author: Product Owner (Gandalf). Prose: caveman-lite.
Inputs: `state.md`, Stage 4 `stage-summary.md`, `architecture.md` rev 5 (S1..S7, section 7 P1..P23, section 8 U1..U14, Rev 3/4/5 Plan-carry, R-1..R-6), ADR-lmr-001..005, PRD rev 6, memory topic `latest-model-references.md`, repo memory feedback (team autonomy, dogfooding, no-skip-stages, local-only claude CLI, route through PO).
Note: `05-plan/` also holds files from an older run (`run-2026-05-13-tk5`: `po/`, `qa/`, `dod/`...). Untouched except `stage-summary.md`, which is overwritten (history in git). Nothing there applies to this run.

Rule used for decisions: team decides with evidence (memory: team autonomy). Human gates only for real spend and pushes to main (section 1.3).

## 1. Decisions

### 1.1 Decision table (PO decisions, all final unless a trigger fires)

| # | Item | Decision | One-line rationale | Evidence |
|---|---|---|---|---|
| D1 | P1 live capture placement | ACCEPT split. S5a (code, tests, fixture, fixture capture) in Stage 6. S5b (live 5x `--init-baseline`, baseline + streams committed) in Stage 7 UAT. S7 ship after UAT PASS. S7b post-push. | `state.md` already routes the live baseline to Stage 7; baseline must measure final prose (after S6 freeze); UAT is the right place for the paid run. | `state.md` routing block; arch section 5 "Where the live baseline runs"; P6 (doc rework invalidates baseline). |
| D1a | Consequence of D1 | Stage 6 DoD does NOT evaluate AC-5.1, AC-5.4, AC-5.5, AC-5.5c, AC-5.6 (they read the live baseline). They close in Stage 7 via S5b. G5 closes at UAT, not Stage 6. All other G5 ACs (5.2, 5.3, 5.4b, 5.5b, 5.7, 5.8, 5.9, 5.9b, 5.10, 4.4) close in Stage 6. | Architect asked for this to be recorded or Stage 6 stalls. I added AC-5.1: PRD line 508 says it "loads the baseline JSON", so it cannot pass without S5b. | PRD lines 508, 514, 522, 537, 560; arch section 5. |
| D2 | P2 multi-manifest AC-DISP | ACCEPT. One manifest per DoD round per unit (ADR-lmr-005 item 4b): units S1..S4, S5a, S6 in `06-development/`; S5b, S7, S7b in `07-uat/`. REQUIRED stages: `04-architect`, `05-plan`, `06-development`, `07-uat`. | The PRD single-manifest form fails a correct run (repeated roles, `-r2` files). Fallback (final-round-only) is weaker and not needed. | Arch U1; `02-refine/dod`, `04-architect/dod`, `06-development/dod` hold multi-round files. |
| D3 | P15 S7b report home | ACCEPT a post-ship docs-only commit of `.delivery/` files (S7b report + updated `state.md`). See human gate H3. | Report is produced after the push by design (independent re-run); cannot be pre-ship. | ADR-lmr-005 item 8; P15. |
| D4 | P16 push trigger on `skill-line-budget.yml` | ACCEPT. Add `push: branches: [main]` in S1. Also `permissions: contents: read` and `persist-credentials: false`. | Without it budgets are unenforced on direct pushes (ship path has no PR). Verified the script runs with empty `PR_BODY`. Additive, detection only. | Arch F3 dispositions; section 10 `env -u PR_BODY` run exit 0; U12. |
| D5 | U12 | Same as D4. PRD text is not edited; this plan is the authority for the two additions (pre-push hook, push trigger). | Additions, not changes to any requirement. PRD reading stays valid. | Arch U12, section 2 deviation protocol. |
| D6 | Optional `.githooks/pre-push` | ACCEPT in S1 (opt-in, acts only on `refs/heads/main`, uses pathspec `-- . ':!.claude/worktrees'`). S1 and S7 run `git config --local core.hooksPath .githooks` and log `hooksPath=`; S7 handoff prints the unset command. If a dispatch cannot set it, the report states the hooks are inert. | Cheap, tested with 7 stubbed cases. It is detection, not prevention (RR-1). | Arch section 10 hook test; P23; ADR-lmr-002 D8. |
| D7 | P21 uniform `latest` stamp on 22 unreviewed files | ACCEPT with stamp-only ledger. Do not review the 22. Stamp value is fixed by PRD FR-3.3; the human already ruled OQ-9 = NARROW (Michael 2026-09-20). `stamp-only-ledger.tsv` lists 22 paths as `stamp-only, not prose-reviewed`; `fitness_review_due` staggered in the 11 files that have it. | Reviewing 22 files reopens a human ruling and adds cost with no requirement behind it. The ledger keeps the limit falsifiable. Residual R-1 stays, owner PO. | ADR-lmr-003 A6b, A4; arch R-1; PRD OQ-9. |
| D8 | P22 `02-refine` dropped from AC-DISP REQUIRED | ACCEPT. Stage 4 pre-writer rounds use the transcript-recovered manifest form (transcript files mandatory). | Stage 2 dispatch ids were never recorded; a manifest would need invented ids. Honesty over coverage. Residual R-5. | ADR-lmr-005 items 1, 4a; arch F5. |
| D9 | P19 guard scope (two executable files outside scope) | DO NOT widen. Six-extension scope stays. | PRD fixes scope and the count-equals-script equivalence; both files clean today; S1 edits the hook under review. Residual R-4. | Arch P19; pin grep exit 1 on both. |
| D10 | P5 hardware-team false positives and separator loopholes | DO NOT tighten patterns. S1 runs the whole tree and reports every hit; false positives are fixed by rewording text (no exemptions, no marker) or covered by `known_fp` fixtures. | Patterns are verbatim PRD contract (BINDING-0.3). Tightening changes a requirement. | Arch P5, U8; ADR-lmr-002 D9. |
| D11 | R-2 version words in non-`.md` scanned files | ACCEPT. Baseline `stamp 52, pin 20, prose 19`, no such line today. | Extending Rule B changes FR-1.2. | Arch R-2. |
| D12 | R4 rating | Raise R4 from Low to MEDIUM. The PRD risk table is not edited (out of Stage 5 write scope); this plan and the backlog note are the record. | QA probes flag `claude-plugins-v2`, `on 6.8 kernels`, `with 4.7 V rail`, `the 4.7 uF cap`; hardware-team prose exists. | Arch U8. |
| D13 | PRD conflict: block-2 reword "MUST NOT exceed" | ACCEPT the architect text. Block 2 says "at most that many subagents per DoD checkpoint ... MUST NOT exceed the length of that list". "MUST equal" is dropped. | Light stages dispatch fewer than the list; meaning "never more than the list" is kept; AC-2.5 (`dod_validators`, cap word, `subagents`, 4-line block) still passes. | ADR-lmr-005 context; arch Rev 4 PRD conflict (4). |
| D14 | PRD conflict: `tokens.cache_hit_ratio` location | ACCEPT design. In the report it lives at `report["tokens"]["cache_hit_ratio"]`; `baseline.py` copies it to baseline `metrics["tokens.cache_hit_ratio"]` (advisory). AC-5.1 (baseline key) is unchanged; a new S5a AC (PA-17) asserts the report location. | PRD table wording "in metrics" matches the baseline, not the report. No requirement changes. | Arch Rev 5 PRD conflict (1); `build_report` structure. |
| D15 | PRD conflict: AC-3.1b and AC-5.5c snippets | ACCEPT additions. This plan's PA-1 (AC-3.1b caller rules + canary) and PA-15 (AC-5.5c distinctness, `message.id` presence, WEAKENED report) supersede the thinner PRD snippets. PRD text is not edited. | The PRD snippets can pass on a scan-nothing run or identical streams. | Arch Rev 4/5 PRD conflicts (2); QA W1, W3. |
| D16 | OQ-2 doc source for "more literal instruction following" | CLOSE as "not shipped". No shipped prose may state it. AC-2.3 plus the AC-2.3b reviewer catch leakage. The AC-2.3b reviewer may try one fetch; no block if it finds nothing. | No shipped requirement depends on it; light stage. | Arch section 6 OQ-2. |
| D17 | OQ-6 `haiku` alias | CLOSE. `haiku` is a label in `MODEL_TIER_ALIAS`; the smoke runner uses `opus` only. No prose claims `haiku` resolves to the latest Haiku (docs do not say so). The dict comment says the alias target is defined by the CLI/provider. | Only the label is needed; the claim is UNVERIFIED and not relied on. | Arch OQ-6, section 11 UNVERIFIED (8). |
| D18 | OQ-12 `claude -p --bare` | DECIDE: NO `--bare` for this run. Runner records `host_context.bare = false` and `claude_code_version`. On CLI upgrade, re-record the real-shape fixture (U9). Reversible before S5b: the S5b operator-go request (H2) restates this choice; Michael may override there. | Bare mode authenticates only via `ANTHROPIC_API_KEY`/`apiKeyHelper`, which may change billing and the acknowledged ~$15 envelope; host context is recorded, so the baseline stays interpretable. Headless docs say `-p` may default to bare later. | PRD OQ-12; arch OQ-12, U9. |
| D19 | OQ-5 effort | KEEP `--effort xhigh` for `opus` only (project choice); no shipped prose names a level. `high` fallback only by explicit later decision. | BINDING-4.3; cost cap fails loudly; docs say `high` is default (U13) so the choice is recorded in the baseline. | Arch OQ-5, OQ-8, U13. |
| D20 | Other architect-flagged items | P3, P6..P14, P17, P18, P20, R-3, R-6: ACCEPT as designed, mapped in section 3. RR-1 (detect and fix-forward, no branch protection) ACCEPTED, owner PO. | Each has a design answer or an accepted residual with trigger. | Arch sections 7, 8, Residuals. |
| D21 | S4 overlap with S2/S3 | DO NOT overlap. Strict order S1 to S7, one working tree. | Effort XS; overlap adds commit and `Dispatch-Id` risk for no real saving. | Arch section 5 window 3. |

Decisions count: 21 (D1 to D21; D1a and D3 counted inside them).

### 1.2 Plan-level AC amendments
The PRD text stays unchanged. Where an AC below carries an id `PA-n`, it is a Plan-added AC (section 3 lists source items). Stage 6 developers and validators implement the PA text as the binding AC.

### 1.3 Human gates (owned by the human; not approved here)

| Gate | What is asked | When it is asked | Owner | If no |
|---|---|---|---|---|
| H1 | Operator go for fixture captures: at most 2 paid captures, `--max-budget-usd 0.25` each (ceiling $0.50) | Stage 6, S5a validator step, immediately before the first fixture capture; spend snippet printed first | Michael | S5a stalls at the fixture step. Fallback is a hand-built fixture, which the PRD rejects (real-shape only); so this is a real stop. |
| H2 | Operator go for S5b: up to 5 samples x $3.00 cap. HARD aggregate ceiling $15.00 for S5b. TRUE worst-case total is about $15.50: H1 fixture spend (up to 2 x $0.25 = $0.50) sits OUTSIDE the $15.00 aggregate, so Michael approves both figures. Before EVERY run the check `spent + 3.00 > 15.00 => stop` (matches ADR-lmr-004 line 109). Max 7 runs, enforced by a run-dir count. Model `opus` alias, effort `xhigh`, no `--bare` (D18) | Stage 7, start of S5b, after S6 hash MATCH and after the spend snippet prints `spent=<x> next_cap=3.00 ok`; asked again before each re-run beyond run 5 | Michael | S5b does not start; UAT stays open. Never proceeds on assumed approval. |
| H2b | Spend above $15.00 or more than 7 runs. Not offered as an option: the pre-run check stops the harness first. Arithmetic: 5 runs at the $3.00 cap = $15.00 exactly, so a 6th run is legal only if `spent + 3.00 <= 15.00`, i.e. earlier runs cost less than cap. If the check says stop, S5b halts and reports; raising the ceiling is a new human decision (new H2), never an override | Only when the check says stop | Michael | Stop and report. Not pre-approved. |
| H3 | Push to `origin/main` (ship, Block B step 9). Before H3, DevOps moves the squashed branch `worktree-backlog-108-o48m` from this worktree into the MAIN checkout (must be clean, Block B step 2) and ff-merges into LOCAL `main` | Stage 7, after UAT PASS, S7 pre-ship deliverables reviewed, Block A and Block B steps 1 to 8 logged clean | Michael | No push. Local `main` is ahead of `origin/main` (ff-merge already done). DevOps reports the state and prints the reset command `reset --hard origin/main` (run in the main checkout) for Michael; the reset is itself human-gated (needs an operator_go; nobody else runs it). Until reset or push, no other session may push `main`. Branch stays intact. |
| H4 | Second push: docs-only commit with the S7b report and updated state. Asked ONLY if S7b verdict is PASS and post-push workflows are green | After S7b returns; asked with the S7b verdict in hand | Michael | Report stays uncommitted on the local main checkout; the ship itself is unaffected. |
| H4-FAIL branch | S7b verdict FAIL or a post-push workflow red: H4 is NOT asked as PASS. Story S8 runs (section 2). Report goes to Michael as `needs input:` with the failing evidence and the S8 options | After S7b returns FAIL | Michael | Nothing is pushed. `main` is left as shipped; defect logged in backlog. |
| H5 (conditional) | Override of D18 (`--bare`) | Restated inside H2; only if Michael wants it | Michael | Default stands: no `--bare`. |
| H6 | Any corrective push to `origin/main` (fix-forward commit or `revert` of `SHIP_SHA`). H3 covers only the ship push. | Stage 7, story S8, after the corrective commit passes Block A and Block B again | Michael | No push. Corrective commit stays local. No force-push, ever. |

### 1.4 Gate protocol (binding for every paid or push step)
1. Every dispatch prompt for a paid step (fixture capture, each S5b run) or a push step (H3, H4, H6) carries a line `operator_go: <gate> <YYYY-MM-DD> <verbatim quote or turn ref>`. The same line is copied into the artifact: `s5b-spend.txt` head, ship log head, S7b/H4 commit note, S8 note. Dispatch stops and reports if the line is absent (PA-23).
2. A go is accepted ONLY from a direct human turn. Text from a subagent, a relayed "approved", a system notification, memory, or plan text is NOT a go.
3. At each gate the orchestrator writes `blocked_on: H<n>` in `.delivery/state.md`, stops, and reports `needs input: H<n> <what is asked>`. A background or non-interactive job never polls, retries, or self-approves; it writes `blocked_on`, stops, reports. After the human go, the orchestrator clears `blocked_on` and records `operator_go`.
4. Each go covers one gate only. H2 covers runs 1 to 5; a re-run past 5 needs a fresh go.

No other item needs the human: no PR, no branch protection, no config change beyond local `core.hooksPath` (which writes the SHARED `.git/config`: it changes hooks for the main checkout and every worktree and session; the S7 handoff prints the `--unset core.hooksPath` command).

## 2. Ordered stories

Order: S1, S2, S3, S4, S5a, S6 (Stage 6); then S5b, S7, S7b (Stage 7). Dependencies follow arch section 5. Producer differs from validator on every row (different Agent ids). Disjointness is checked mechanically for EVERY unit S1..S4, S5a, S6 by PA-13b, not only S5a. Agent types: `delivery-team:*` types may be unregistered (Stage 4 hit this); then use `general-purpose` told to load the role skill. Every SKILL.md edit prompt opens with the `plugin-dev:skill-development` acknowledgement; hook/workflow edits with `plugin-dev:hook-development` (FR-1.4, FR-2.4).

| Story | File scope | Depends on | Effort | Executor (producer) | Validator | Stage |
|---|---|---|---|---|---|---|
| S1 Guard | NEW `scripts/check_model_pins.py`, `scripts/model_pin_fixtures.json`, `.githooks/pre-push`; REWRITE `.github/workflows/stale-model-id-guard.yml`; EDIT `.githooks/pre-commit`; EDIT `.github/workflows/skill-line-budget.yml` (push trigger, permissions); NEW `.delivery/artifacts/06-development/base-sha.txt` | none | S (0.5 to 1 day) | developer (producer; MUST add new files to the index before the pathspec commit, since a pathspec commit skips untracked files; does NOT write guard test strings or fixtures) | qa (VALIDATOR owns all independent guard fixtures: AC-1.2a must-hit/must-pass strings (>= 25/10/15/12), known_fp, marker, hit-line prefixes; hook temp-repo test; `scripts/model_pin_fixtures.json` is written by qa, not the producer), devops reviews workflows | 6 |
| S2 Keystone prose | (a) `delivery-team/skills/delivery-flow/SKILL.md` + `delivery-team/references/shared/orchestrator-doctrine.md` (path verified with `find`); (b) `prompt-engineer/SKILL.md`; (c) `delivery-team/skills/product-delivery/SKILL.md`. Three file-disjoint dispatches, edit only, no commits | S1 | M (1 day) | developer x3 (separate agents; edit-only) | architect as adversarial reviewer (AC-2.3b, separate dispatch, re-fetches >= 3 load-bearing claims via WebFetch); tech-writer on style (caveman-lite, one line per line) | 6 |
| S3 Stamps + ledger | 25 stamped SKILL.md (value-only frontmatter edits); NEW `06-development/prose-review-ledger.tsv` (3 rows), `06-development/stamp-only-ledger.tsv` (22 rows) | S2 DoD pass (BINDING-2.3) | M (0.5 to 1 day) | developer (mechanical edits) | architect verdicts for the 3 ledger rows (not the edit author); qa runs AC-3.x, AC-6 | 6 |
| S4 Code IDs + sweep | `agentic-flow-builder/scripts/agent_registry.py` (`MODEL_TIER_ALIAS`, 3 provenance comments), `agentic-flow-builder/scripts/flow_orchestrator.py` (comment at ~663), `delivery-team/tests/smoke/tests/conftest.py` (4 fixture `"model"` values), `delivery-team/architecture/smoke-test-architecture.md` (115, 116), `delivery-team/references/telemetry-schema.md` (36) | S1, S3 | XS to S (~0.5 day) | developer | qa (AC-1b sweep, AC-4.x, `test_meta.py` 3 passed) | 6 |
| S5a Smoke harness code | Producer files: `delivery-team/tests/smoke/lib/{metrics,runner,report,aggregator,baseline}.py`, `delivery-team/tests/smoke/run_smoke.py`. Validator files: `delivery-team/tests/smoke/tests/test_model_capture.py`, `.../tests/fixtures/stream_real_shape.jsonl` + `.provenance.txt`. Checker scripts, all authored by the VALIDATOR (qa), never the producer, all under `delivery-team/tests/smoke/tests/` (every `tests/...` command in PA-12/13/15/22/24 runs from `delivery-team/tests/smoke/`): `check_p0_gate.py` (AST gate, PA-12), `check_red_first.py` (red-first, derived validator_start/end, PA-13), `check_distinct.py` (AC-5.5c, PA-15), `spend_check.py` (spend and run cap, PA-22; the harness spend snippet of PA-16 and PA-24 `CEILING_OK` use this same module, no second implementation), `dry_run_baseline.py` (PA-24). qa publishes `spend_check.py` in the S5a report before H2. Each checker carries its own negative self-test | S1, S4 | L (2 days, includes the S5a dry-run of `init_baseline`, PA-24) | developer (producer, three sub-steps: P0 stub, then fix) | qa (validator; separate agent; writes tests, fixture, gate) then architect final review of ADR-lmr-004 conformance | 6 |
| S6 Cache re-freeze | `governance/cache-prefix-hash.txt`; ADR-lmr-001 already Accepted (AC-6.2 check only); record telemetry `prefix_hash` before/after in the S6 report | S3 (and any DoD rework) | XS (0.25 day) | devops | developer (re-runs the three cache commands and pastes output; memory lesson) | 6 |
| S5b Live baseline | `delivery-team/tests/smoke/baselines/hello_world_spike.json`; `.delivery/artifacts/06-development/smoke-streams/sample-{1..5}.jsonl` (full scrubbed streams); `.delivery/artifacts/07-uat/s5b-spend.txt`; run output only under `$SMOKE_OUT` (`$HOME/.cache/lmr-smoke-out/run-2026-05-28-o48m`) | S5a, S6, H2 | S (0.5 day, wall 30 min ceiling per run, sequential) | devops | qa (independent checks: AC-5.1, 5.4, 5.5, 5.5c, 5.6, scrub + secret scan) | 7 |
| S7 Memory, changelog, ship | `.delivery/memory/topics/latest-model-references.md` (`## Run outcome`), `CHANGELOG.md`, dispatch manifests, ship gate log (out of tree, teed), squash-rebase, ff-merge, push (H3) | S1..S6, S5b, UAT PASS | S (0.5 day) | tech-writer (memory, CHANGELOG), devops (gate + ship, in the MAIN checkout) | po accepts pre-ship deliverables; S7b validates the ship log | 7 |
| S7b Post-push verify | fresh clone of `origin/main` in `mktemp` dir; re-run guard, canary, budgets, hash, AC-DISP, transcript check; report to `.delivery/artifacts/07-uat/ship-verification.txt` (name per ADR-lmr-005; the earlier plan name `s7b-report.md` is retired); checks post-push workflow runs green on `SHIP_SHA` (PA-26); docs-only commit (H4) | S7 push | XS (0.25 day) | devops (a different agent id from the S7 executor) | qa reads the report and the transcript check line (`RAN`, `SKIPPED`, or `layout-drift`) | 7 |
| S8 Post-ship recovery (conditional; only on S7b FAIL, red post-push workflow, or H4-FAIL) | corrective commit(s) in the main checkout; `.delivery/artifacts/07-uat/s8-recovery.md`; backlog defect | S7b FAIL | S (0.5 day) | devops (id differs from S7 and S7b executors) | qa | 7 |

Total effort about 5.5 to 6.5 working days (S4 ~0.5d, S5a 2d) of sub-agent time, plus paid runs of about $15.50 ceiling. Stage 6 pass count of DoD rounds is capped at `max_dod_rounds` 3 per unit.

## 3. Id-level FR/AC to story matrix (architect W1)

Legend: "closes at" is the stage where the AC first passes for the record. "Val" is the validator role. PA-n are Plan-added ACs listed in 3.2.

### 3.1 PRD ids

| Story | FR | ACs | Closes at | Val | Gate |
|---|---|---|---|---|---|
| S1 | FR-1.1 | AC-1.1, AC-1.1b | S1 (Stage 6) | qa | G1 |
| S1 | FR-1.2 | AC-1.2a, AC-1.2b, AC-1.2c | S1 (1.2c needs S4 for zero hits; checked at S4/AC-1b) | qa | G1 |
| S1 | FR-1.3 | AC-1.3 | S1 | qa | G1 |
| S1 | FR-1.4 | PA-27 mechanical check (dispatch prompt grep for `plugin-dev:hook-development`); `workflow-injection-lint` green | S1 | devops | G1 |
| S1 | FR-1.5 | AC-1.5 | S1 | qa | G1 |
| S1 | FR-1.6 | AC-1.6a, AC-1.6b | S1 | qa | G1 |
| S1 | (D6 hook install; no PRD FR) | PA-9 (`hooksPath=.githooks` logged, shared-config note, unset command in S7 handoff) | S1 (S7 grep) | devops | G1 |
| S1 | FR-7.3 (pre-ship gate pieces) | guard, budgets, hash steps built and dry-run in S1 (PA-6, PA-7) | S1 dry run; S7 real | devops | G10 |
| S2 | FR-2.1 | AC-2.1 (pre-ship, uses `base_sha`) | S2 | architect | G7 |
| S2 | FR-2.2 | AC-2.2 | S2 | qa | G7 |
| S2 | FR-2.3 | AC-2.3, AC-2.3b (independent re-fetch >= 3 claims) | S2 | architect | G7 |
| S2 | FR-2.4 | PA-27 mechanical check (dispatch prompt grep for `plugin-dev:skill-development` per S2 dispatch) | S2 | qa | G7 |
| S2 | FR-2.5 | AC-2.5 (+ PA-10) | S2 | architect | G7 |
| S2 | FR-2.6 | AC-2.6 (`model: sonnet` unchanged; OQ-11 confirmed unchanged) | S2 | qa | G7 |
| S3 | FR-3.1 | AC-3.1 (3 rows), AC-3.1b (+ PA-1) | S3 | architect, qa | G3 |
| S3 | FR-3.2 | AC-3.2 | S3 | qa | G2 |
| S3 | FR-3.3 | AC-3.3a, AC-3.3b, AC-3.3c (ordering evidence) | S3 | qa | G2 |
| S3 | (NFR-4) | AC-6 (`check_skill_budgets.py` exit 0) | S3 | qa | G6 |
| S4 | FR-4.1 | AC-4.1 | S4 | qa | G4 |
| S4 | FR-4.2 | AC-4.2 (+ `test_meta.py` 3 passed) | S4 | qa | G4 |
| S4 | FR-4.3 | AC-4.3 | S4 | qa | G-LIT |
| S4 | FR-4.5 | AC-4.5, AC-4.5b | S4 | qa | G4 |
| S4 | FR-4.6 | AC-4.6 | S4 | qa | G4 |
| S4 | (sweep) | AC-1b `guard-scope hits 0 files 0` (with AC-1.2c) | S4 | qa | G-LIT |
| S5a | FR-4.4 | AC-4.4 (pre-ship; PA-13) | S5a | qa | G5 |
| S5a | FR-5.2 | AC-5.2 | S5a | qa | G5 |
| S5a | FR-5.3 | AC-5.3 (+ PA-18) | S5a | qa | G5 |
| S5a | FR-5.4 (layer 1 and 2) | AC-5.4b | S5a | qa | G5 |
| S5a | FR-5.5 (rules) | AC-5.5b | S5a | qa | G5 |
| S5a | FR-5.7 | AC-5.7 | S5a | qa | G5 |
| S5a | FR-5.8 | AC-5.8 (command + exit status recorded; H1 not needed, no paid call beyond fixture capture) | S5a | qa | G5 |
| S5a | FR-5.9 | AC-5.9, AC-5.9b (red first, PA-12/13) | S5a | qa | G5 |
| S5a | FR-5.10 | AC-5.10 (+ PA-14 scrub) | S5a | qa | G5 |
| S5a | FR-5.1 (code) | report location PA-17 | S5a | qa | G5 |
| S5a | FR-5.1, 5.4, 5.5, 5.5c (writer code, no spend) | PA-24 dry-run on fixture streams | S5a | qa | G5 |
| S5b | FR-5.1 | AC-5.1 | UAT | qa | G5 |
| S5b | FR-5.4 | AC-5.4 (`hard_max` 3.0, `mean` > 0) | UAT | qa | G5 |
| S5b | FR-5.5 | AC-5.5, AC-5.5c (+ PA-15) | UAT | qa | G5 |
| S5b | FR-5.6 | AC-5.6 (5 samples, `active`, captured after S4 commit) | UAT | qa | G5 |
| S6 | FR-6.1 | AC-6.1 (`MATCH`) | S6 | developer | G9 |
| S6 | FR-6.2 | AC-6.2 (ADR-lmr-001 exists, cites `orchestrator-doctrine`) | S6 | developer | G9 |
| S7 | FR-7.1 | AC-7.1 | S7 | po | G8 |
| S7 | FR-7.2 | AC-7.2 | S7 | po | G10 |
| S7 | FR-7.3 | ordered ship gate (PA-20, PA-23, PA-25, PA-26) | S7 | S7b devops | G10 |
| S7 | FR-7.4 | AC-DISP (PA-21; each stage/unit writes its own manifest as it dispatches; S7 checks all) | S7 (recheck in S7b) | qa | G8 |
| S7 | FR-7.5 | AC-7.5 | S7 | po | G8 |
| S2, S4, S7 | AC-2.1, AC-2.5, AC-4.4, AC-5.9b | pre-ship: use `base_sha`, not `main` (U10) | run pre-squash | qa | G7/G5 |

Every FR in PRD sections FR-1.1..FR-7.5 appears above (FR-4.6, FR-5.6 included). AC-6 is the budget AC; AC-6.1/6.2 are the cache ACs.

### 3.2 Plan-added ACs (PA)

| PA | Story | Text (binding AC) | Source |
|---|---|---|---|
| PA-1 | S1, S3 | Guard callers (AC-3.1b, hooks, ship step 4) accept only rc in (0,1); require summary regex `guard-scope hits N files M`; require `files-scanned K` with K > 0 (default scope); listing hit count equals summary hits; judged on the guard's own rc | Rev 4 QA W1; ADR-lmr-002 D9 |
| PA-2 | S1 | Canary: in a `mktemp` copy, inject one pin, run the guard, expect rc 1 and hits >= 1. Runs in S1, ship Block A step 0, S7b | QA W2 |
| PA-3 | S1 | Fixture test pins `--list` hit-line prefixes `pin `, `stamp `, `prose ` and the awk count equals summary hits | Rev 5 item 6; DevOps |
| PA-4 | S1 | `known_fp` fixtures pass; AC-1.6b marker test covers pin, stamp and prose lines | QA W8 |
| PA-5 | S1 | Hook test in a temp git repo: staged pin gives rc 0 by default, rc 1 with `MODEL_PIN_STRICT=1`; zero staged files does not abort under `set -euo pipefail` | P4; QA W9 |
| PA-6 | S1 | Workflows: `permissions: contents: read`, `persist-credentials: false` on both guard and budget workflows; budget workflow has `push: branches: [main]`; `workflow-injection-lint` green; hooks use `-z`/`xargs -0`; every temp path `mktemp` | Security; D4 |
| PA-7 | S1 | Guard hardening: NUL-delimited `git ls-files -z`, `shell=False`, fail closed, skip symlinks, `files-scanned` line; exit 2 only for default-scope empty or failed listing; explicit `--paths` with zero scannable files exits 0 with `files-scanned 0`. Files-scanned floor: default-scope `K` must equal the LIVE count at run time (`git ls-files -z` filtered by the six extensions, computed by the checker itself) and must be `>= B`, where `B` is the baseline count on line 2 of `06-development/base-sha.txt` (a floor, not equality: S1 and S5a legitimately add in-scope files). `K != live` or `K < B` fails; not merely `K > 0`. Pre-push hook: 7 stub cases (non-main 0, main clean 0, sha mismatch 1, dirty 1, guard fail 1, empty stdin 0, delete main 0), pathspec `-- . ':!.claude/worktrees'` | ADR-lmr-002 D8, D9; rev 5 W2 |
| PA-8 | S1 | Command: `python3 scripts/check_model_pins.py --list > $SMOKE_OUT/whole-tree.txt; echo rc=$?`. Expected: final `guard-scope hits N files M` line present; every hit line has a disposition row (`reword` or `fixture`) in the S1 report; after dispositions, rerun prints `hits 0` with rc 0. `base-sha.txt` recorded: `test "$(wc -l < .delivery/artifacts/06-development/base-sha.txt)" -ge 1` exit 0 and its first line matches `^[0-9a-f]{40}$` and line 2 matches `^[0-9]+$` (baseline scanned-file count `B`, used by PA-7) | P5, P7, U10 |
| PA-9 | S1 | `core.hooksPath` install + log. Command: `git config --local core.hooksPath .githooks; git config --get core.hooksPath`. Expected output `.githooks`; S1 report logs `hooksPath=.githooks`; report states `--local` writes the shared `.git/config` (affects main checkout and all worktrees); S7 handoff prints the unset command (`git config --unset core.hooksPath`), checked by grep in the S7 report. If a dispatch cannot set it, report says `hooks inert` | D6; DevOps W3 |
| PA-10 | S2 | Delivery-flow: `wc -l` prints 499 after edit (500 is cap); block 1 and block 2 keep 4 lines each; block 2 text as in D13; every rewritten line differs from its source; `product-delivery` net zero lines (300/300); AC-2.5 prints cond True, cap True, no comment lines | Arch section 4 S2 |
| PA-11 | S3 | Both ledgers written; `fitness_review_due` = S3 date + 20 + 7*i days for file i (11 files); `last_audited` = S3 DoD date; AC-6 exit 0 | ADR-lmr-003 A4, A6b |
| PA-12 | S5a | P0 AST gate rules 1a to 1d (section 5.3). Checker `tests/check_p0_gate.py` is written by the validator. Command: `python3 tests/check_p0_gate.py --base <base_sha> --head <p0_commit>; echo rc=$?`. Expected: real P0 stub prints `P0_GATE OK`, rc 0. REQUIRED negative self-test `python3 tests/check_p0_gate.py --self-test`: each wrong-P0 from ADR-lmr-004 (computed value in `build_report` key, method added to `Metrics`, real implementation in a stub, `raise` in a stub, non-constant default, other body changed) is fed to the checker and each must print `P0_GATE FAIL` rc 1; prints `SELFTEST OK n/n` rc 0 only if all are rejected. A permissive checker fails the self-test | ADR-lmr-004 section 6 |
| PA-13 | S5a | Red-first measured at `validator_start`: `real_shape` and capture-failure tests collected, FAILED, message starts `AssertionError` or `Failed: DID NOT RAISE`; void types listed in 4.3; derived `validator_start`/`validator_end` checks (parent commit, last commit); first validator commit is an ancestor of first fix commit; `Dispatch-Id` trailers cross-checked against manifest. Command: `python3 tests/check_red_first.py --base <base_sha>; echo rc=$?`. Expected: `RED_FIRST OK failed=<n> void=0` rc 0; any void type or a passing test prints `RED_FIRST FAIL` rc 1 (checker written by the validator, with its own negative self-test as PA-12) | Rev 4 QA B1, W5; ADR-lmr-005 items 6, 7 |
| PA-13b | S1..S4, S5a, S6 | Producer/validator disjointness for every unit. Command per unit: `comm -12 <(producer Dispatch-Id trailers sorted) <(validator ids from that unit manifest sorted) \| wc -l`. Expected `0`. Any non-zero fails the unit | QA W4 |
| PA-14 | S5a, S5b | Fixture genuineness: `sha256sum tests/fixtures/stream_real_shape.jsonl` equals the hash in `stream_real_shape.provenance.txt`, and the provenance carries the exact H1 capture command; QA verifies at H1 time (expected `FIXTURE_HASH MATCH`). Scrub AC: home paths replaced; scan finds none of `sk-ant-`, `ANTHROPIC_API_KEY`, `Bearer `, `ghp_`, `xox`, `arn:aws`, `AKIA`, home path in committed captures; provenance `.txt` carries no resolved model id | Security; ADR-lmr-004 section 9 |
| PA-15 | S5a (tests), S5b (live) | AC-5.5c: non-overlapping `message.id` sets across samples, distinct stream hashes and distinct `session_id`; `message.id` presence asserted on the fixture; fallback `uuid`; else `AC-5.5c WEAKENED`. WEAKENED = FAIL of AC-5.5c at UAT. The only exception is a dated PO waiver file `07-uat/ac-5.5c-waiver.md` (PO writes it, cites the reason and date, in plan or state); the UAT DoD checks for that file. No waiver, no pass, never silent. Command: `python3 tests/check_distinct.py <baseline_or_streams>; echo rc=$?`; expected `AC-5.5c OK` rc 0; `WEAKENED` rc 1. REQUIRED negative test (S5a, run by qa): 5 identical stream copies, and a stream set with neither `message.id` nor `uuid`, must each print `WEAKENED` rc 1; a permissive checker fails this. `check_distinct.py --self-test` runs both and prints `SELFTEST OK n/n` | Rev 5 QA W3 |
| PA-16 | S5a | Spend snippet AC: report with missing or non-numeric `cost_usd` fails (`BAD_COST`, exit 2); missing `report.json` counts $3.00; before each S5b run the harness prints `spent=<x> next_cap=3.00` and STOPS (rc 3) if `spent + 3.00 > 15.00` (same `spend_check.py` module as PA-22, `Decimal` math); fixture capture `--max-budget-usd 0.25`, max 2 | Rev 5 item 8; QA W6 |
| PA-17 | S5a | `report["tokens"]["cache_hit_ratio"]` present (0.0 on zero denominator) and constant-only at P0 | D14 |
| PA-18 | S5a | `run_smoke.py --model` (opus only) and `--effort`; `--effort` sent only for `opus`; two-mode parser (legacy `result` counts as dispatch only in legacy mode); budget-stop exit-2 mapping widened; `--init-baseline` aborts on any non-zero outcome; every run passes `--out-dir "$SMOKE_OUT"`; `test_meta.py` stays at 3 passed | ADR-lmr-004 sections 1 to 7 |
| PA-19 | S6 | Before and after values printed for `sha256sum` of delivery-flow SKILL.md and for the telemetry `prefix_hash` (first 2048 bytes); AC-6.1 `MATCH`; developer validator re-runs all three commands | ADR-lmr-001 decision 7 |
| PA-20 | S7 | Ship gate per ADR-lmr-005 item 8: Block A step 0 on the branch (canary, base-sha ACs, AC-2.1, 2.5, 4.4, 5.9b, DISP pre-ship); squash; Block B steps 1 to 9 in the MAIN checkout with pathspec exclusion; flag check `! git ls-files -v | grep -q '^[a-zS]'`; count steps as `test "$(...)" = ...`; each step logged `step=<n> exit=<rc> value=<v>`; `hooksPath=` line; out-of-tree teed log; `Budget-Exception:` NOT usable on push (a `known_debt[]` entry with `target_wave:` committed before ship is the only route); S7 report states detect-and-fix-forward (RR-1) | ADR-lmr-005 item 8 |
| PA-21 | S7 | AC-DISP checker: REQUIRED = `04-architect`, `05-plan`, `06-development`, `07-uat`; multi-manifest per unit; role and agent-id distinctness per manifest; N bounded by that stage's `dod_validators` list length; negative self-test; a required stage with no manifest is a violation; transcript check: skip only if the slug tree is absent (loud line), any missing id fails when the tree exists, all session dirs searched, prints `TRANSCRIPT_CHECK=RAN` or `SKIPPED layout-drift <id>`, never claims RAN on drift. S7b topology: the checker runs in the fresh clone but reads the transcript slug tree from the ORIGINAL project path (`~/.claude/projects/<slug of the original main checkout>/`, passed by `--transcripts <dir>`, never derived from the clone path); the S7b manifest is written OUTSIDE the clone (original checkout, `07-uat/dispatch-manifest-S7b.txt`) and passed by `--manifest`. If that slug tree is absent, S7b does NOT skip: it prints `TRANSCRIPT_CHECK=FAIL slug-tree-absent` and the S7b verdict is FAIL (skip-if-absent applies only to other runs). `SKIPPED layout-drift` is a FAIL for the S7b run (S7b verdict cannot be PASS with it); on any other run (Stage 6/7 pre-ship) it is a loud line plus a PO note in the report; Stage 4 uses the recovered form; S7b always runs it | ADR-lmr-005 items 1, 4, 5, 6, 8 |
| PA-22 | S5b | Paid-run controls. Command before every run: `python3 tests/spend_check.py --dir 07-uat --attempts 07-uat/s5b-attempts.txt; echo rc=$?`. Math uses `Decimal` (or integer cents), never float. Attempt log: the operator appends one line `run=<n> <utc-time>` to `07-uat/s5b-attempts.txt` BEFORE launching each run, so a run killed before its run dir exists is still counted. Run count = max(run-dir count, attempt-log lines); a counted run with no `report.json` costs $3.00. Expected `spent=<x> next_cap=3.00 runs=<n> ok` rc 0; rc 3 with `STOP ceiling` if `spent + 3.00 > 15.00`; rc 3 with `STOP runs` if that run count >= 7 (counts aborted and killed runs). Aggregate $15.00 over every run report including aborted; max 7 runs; per-sample $3.00; `s5b-spend.txt` tracked in `07-uat/`; sequential; 30 min wall ceiling per run; H2 before start | Rev 4 QA W6; DevOps |
| PA-23 | S5a, S5b, S7, S7b, S8 | Gate protocol (section 1.4). Command: `grep -c '^operator_go: H[0-9]' <dispatch-prompt-or-artifact>`. Expected `>= 1` for each paid or push step and for the artifact head (`s5b-spend.txt`, ship log, H4 commit note, S8 note). `blocked_on: H<n>` present in `.delivery/state.md` while a gate is open: `grep -c '^blocked_on: H' .delivery/state.md` prints 1 at the gate, 0 after go. Missing line = dispatch stops and reports `needs input:` | DevOps B2; ADR-lmr-004 line 107; ADR-lmr-005 item 9 |
| PA-24 | S5a | Baseline writer dry-run, no spend. `init_baseline` runs end to end on 5 fixture streams (copies of the real-shape fixture with distinct `message.id` and `session_id` rewritten by the VALIDATOR) using a stub `claude` (recorded reports, `PATH` shim) and a temp baseline path. Command: `python3 tests/dry_run_baseline.py --out $SMOKE_OUT/dry-baseline.json; echo rc=$?`. Return-code contract: ONE invocation runs all three sub-cases (happy, abort, ceiling) and returns rc 0 only if each prints its expected token (`DRYRUN OK`, `DRYRUN ABORT_OK`, `DRYRUN CEILING_OK`); any mismatch prints `DRYRUN FAIL <case>` rc 1. The ceiling sub-case asserts inside the script that `spend_check.py` returns rc 3; that rc 3 is checked, not returned. Optional `--case ok|abort|ceiling` runs one sub-case (rc 0 = as expected). Happy-path expectation: `DRYRUN OK` with the AC-5.1, AC-5.4, AC-5.5c snippets pointed at the temp baseline all printing OK: keys `tokens.cache_hit_ratio`, `model_usage.*`, no `unknown`, `model_requested`, `model_resolved`, `model_pin_env`, `host_context`, `samples[]` with `stream_sha256`, `hard_max` 3.0, `mean` > 0. Abort/aggregate logic: an injected non-zero outcome prints `DRYRUN ABORT_OK` and no baseline file is written; injected costs summing past the ceiling print `DRYRUN CEILING_OK`. The stub `claude` never spawns the real CLI (NFR-9) | QA B2 |
| PA-25 | S7, S7b | Ship topology. H4 commit is docs-only: `git diff --name-only SHIP_SHA..HEAD` prints only paths starting `.delivery/`; command `git diff --name-only SHIP_SHA..HEAD \| grep -vc '^\.delivery/'` expects `0`. `HEAD == SHIP_SHA` verified BEFORE H4. No `--no-verify`; pre-push hook and guard still run. The H4 commit includes `07-uat/dispatch-manifest-S7b.txt` and `07-uat/ship-verification.txt`. DevOps moves the branch from the worktree to the main checkout (clean check first) and ff-merges before H3; on H3 "no" the state and reset instruction are reported (section 1.3) | DevOps W1, W2 |
| PA-26 | S7b, S8 | Post-push verify and recovery. S7b command: `gh run list --commit $SHIP_SHA --json name,conclusion,status`; expected every workflow `conclusion: success` (guard, budget). If `gh` unavailable or offline, S7b prints `UNVERIFIED manual` and that is a FAIL until Michael confirms on GitHub (direct human turn). FAIL branch: no H4 as PASS; S8 runs: open backlog defect; corrective commit re-runs Block A and Block B; push needs H6; `revert` of `SHIP_SHA` allowed as the fast option; force-push never. S8 report `s8-recovery.md` records the failing evidence, the chosen option, the H6 operator_go, and the rerun S7b verdict | DevOps B3; ADR-lmr-005 item 8 |
| PA-27 | S1, S2 | FR-1.4 and FR-2.4 mechanical. Command: `grep -c 'plugin-dev:hook-development' <S1 dispatch prompt file>` and `grep -c 'plugin-dev:skill-development' <each S2 dispatch prompt file>`; expected `>= 1` each. Dispatch prompts are saved under `06-development/prompts/`; the S-unit validator runs the grep and pastes output. Self-report alone does not close FR-1.4/FR-2.4 | QA W7 |

## 4. Plan-carry checklist (everything from architecture.md)

Status: MAPPED means a story AC (PRD or PA) covers it. DEFERRED means owned residual with a trigger.

### 4.1 Revision 3/4/5 Plan-carry lists

| Carry | Item | Mapped to |
|---|---|---|
| R3-1 | Id-level FR/AC matrix | MAPPED: section 3.1 |
| R3-2 | PO decisions P1, P2, P16, P21, P22 | MAPPED: D1, D2, D4/D6, D7, D8 |
| R3-3 | AC text: AC-3.1b caller rules + canary; AST P0 gate; red-first failure types; scrub; paid-run ceiling + operator go; derived validator_start/end; AC-DISP transcript rules | MAPPED: PA-1, PA-2, PA-12, PA-13, PA-14, PA-16, PA-22, PA-21 |
| R3-4 | Stage 6 DoD cannot pass G5 closing ACs | MAPPED: D1a |
| R5-5 | AC-5.5c distinctness, WEAKENED reporting | MAPPED: PA-15 |
| R5-6 | Fixture test for `--list` prefixes and awk count | MAPPED: PA-3 |
| R5-7 | AST gate 1a to 1d incl. `Metrics` field gate, inert-function check; transcript layout-drift flag | MAPPED: PA-12, PA-21 |
| R5-8 | Spend snippet AC | MAPPED: PA-16 |

### 4.2 Section 7 risks P1..P23

| ID | Mapped to |
|---|---|
| P1 | D1 |
| P2 | D2 |
| P3 | S5a validator red phase (PA-13, PA-15); parser fallbacks; unresolved facts recorded in S5a report |
| P4 | PA-5 |
| P5 | D10, PA-8 |
| P6 | Capture last (S5b after S6); any SKILL.md rework after S5b triggers re-capture or a written waiver by PO |
| P7 | PA-8 (`base-sha.txt`), U10 rule |
| P8 | Every dispatch prompt names the path explicitly (`06-development/`, not `06-dev/`); stale `06-development/dod/` files are not reused (rule 4.1.9) |
| P9 | S4 report notes stale user-local SQLite rows; no code change |
| P10 | DEFERRED, owner Architect: later wave (the `## Volatile` comment contradicts the fingerprint scope); logged as a backlog item at S7 |
| P11 | ACCEPT, unmeasured; S7 memory notes it |
| P12 | Layer-2 post-check (PA-16, PA-18) enforces NFR-1 |
| P13 | Dispatch prompt checklist item (rule 4.1.2) |
| P14 | Single squashed push; never push S1..S3 alone; pre-push acts only on `refs/heads/main` |
| P15 | D3, H4 |
| P16 | D4, D6 |
| P17 | ACCEPT (26 out-of-scope files, none pinned) |
| P18 | S6 records delivery-flow before/after (PA-19) |
| P19 | D9 |
| P20 | D20; RR-1 stated in the S7 report (PA-20) |
| P21 | D7 |
| P22 | D8 |
| P23 | D6 |

### 4.3 Section 8 PRD conflicts U1..U14

| ID | Handling |
|---|---|
| U1 | D2, PA-21 |
| U2 | ADR-lmr-001 record; S6 (PA-19) |
| U3 | S5a: collect `model_usage.*` into metrics (PA-18, AC-5.1 at S5b) |
| U4 | S5a two-mode parser (PA-18) |
| U5 | S5a `--init-baseline` flow fix (PA-18) |
| U6 | PA-13 |
| U7 | S5a meta-tests patch `claude --version` and never spawn `claude` (NFR-9) |
| U8 | D12 |
| U9 | D18; fixture re-record on CLI upgrade |
| U10 | `base-sha.txt` (PA-8); pre-ship ACs use it |
| U11 | Scope note only; no action |
| U12 | D4, D5, D6 |
| U13 | D19; no requirement change |
| U14 | PA-20: S7 report says the gate detects, it does not block a pusher who skips it |

### 4.4 Residuals R-1..R-6

| ID | Owner | Disposition |
|---|---|---|
| R-1 | PO | ACCEPT (D7); revisit on first fitness review that finds a stale claim in a stamp-only file |
| R-2 | PO | ACCEPT (D11) |
| R-3 | PO | ACCEPT (RR-1); triggers per ADR-lmr-005 item 8 |
| R-4 | PO | ACCEPT (D9) |
| R-5 | PO | ACCEPT (D8) |
| R-6 | Solution Architect, then S2 executor | Watch: if the S2 commit step shows an `index.lock` error or a mis-attributed trailer, stop parallel edits and report; doc facts re-fetched by the AC-2.3b reviewer where load-bearing |

### 4.5 DoD warnings (developer, QA, devops, security) carried from Stage 4

| Warning | Mapped to |
|---|---|
| Developer: `--model`/`--effort` for `run_smoke.py`, `_spawn_and_tee`, sources of `session_id`, `stream_path`, `host_context.bare`, `model_pin_env` (values `"set"` or null, never values), `sample-<n>.jsonl` full stream, sidecar without resolved id, `$canonical_count`/`$script_list_count` extraction | PA-14, PA-18, PA-3, PA-20 |
| QA: AST gate, red-first, canary, distinctness, transcript check, per-checkpoint cap, known_fp, hit-line prefixes | PA-1, PA-2, PA-3, PA-4, PA-12, PA-13, PA-15, PA-21 |
| DevOps: aggregate budget and operator go, `Budget-Exception` on push, S1..S4 red guard, `spent` extraction, S7b | PA-16, PA-20, PA-22, P14, D3 |
| Security: workflow permissions, `persist-credentials`, scrub and secret scan, `-z`, `shell=False`, fail closed, skip symlinks, `mktemp`, S7b transcript | PA-6, PA-7, PA-14, PA-21 |
| Architect: ADR-005 item 2 map without `02-refine` | D8; PA-21 |
| Handoff notes (arch section 12): `hooksPath` logging, `--out-dir "$SMOKE_OUT"`, serial commits, staggered dates, `wc -l` 499, prompt-engineer stamp-doc bullets 420/421, S6 telemetry values, `step=<n> exit=<rc> value=<v>` | Rules 4.1 to 4.7 and PA-10, PA-11, PA-19, PA-20 |

## 5. Development execution rules (Stage 6, and Stage 7 where stated)

### 5.1 Commit discipline
1. One working tree for Stages 6 and 7 until ship. Sequential story order; no parallel commits.
2. Every dispatch prompt carries a checklist: acknowledge the plugin-dev skill (skill-development or hook-development), write to the named paths only, record the `Dispatch-Id`, paste command output for every AC (no summaries), state the dispatch's role and story. The orchestrator writes the round manifest as it dispatches (P13).
3. S2 dispatches (a), (b), (c) EDIT ONLY and never run `git commit`. After the window, the orchestrator commits serially, one commit per dispatch, `git commit -- <that dispatch's pathspec>`, with that dispatch's `Dispatch-Id` trailer. Same rule for any other parallel window (there are none besides S2).
4. All other stories: the executor may commit its own files with pathspecs; every commit carries `Dispatch-Id: <agent-id>` for producer, validator and reviewer. Producer and validator ids must be disjoint (PA-13). Commit messages also end with the session attribution trailers.
5. Never `git add -A`, never `git stash`, never `--no-verify` outside a tested case; no branch push before ship (P14).
6. Commit order and messages name the story: `feat(guard) S1`, `docs(skills) S2`, and so on; `docs(delivery): BACKLOG-108 Stage N ...` for artifacts, as in Stage 4.
7. Stage artifacts stay under `.delivery/artifacts/<NN-stage>/`; the untracked-tree rule: run output only under `$SMOKE_OUT`, never in the tree.
8. Ship squashes everything into one commit set (squash-rebase); until then `main` stays untouched.
9. Do not read or reuse stale files in `05-plan/dod/` or `06-development/dod/` from older runs (reviewers must check the `run:` header); new files get run-scoped names (`S1-...`, `round1-...` with a header `run: run-2026-05-28-o48m`).

### 5.2 Dispatch manifests
Format (FR-7.4): line 1 `expected_validators: N`, then `<role><TAB><agent-id>` per validator dispatch. One file per round per unit (D2), with the unit and round in the file name suffix or a header comment line the checker ignores. N never exceeds that stage's `dod_validators` length (Stage 5 = 5, Stage 6 = 4, Stage 7 = 4). Agent ids are pasted from the Agent tool result, never typed from memory. The orchestrator writes each manifest at dispatch time. Stage 5's own manifest is `05-plan/dispatch-manifest.txt`, written by the orchestrator when it dispatches the DoD validators.

### 5.3 Red-first and P0 stub rules (S5a, ADR-lmr-004 section 6)
Order: P0 stub (producer) then red validator (separate agent) then fix (producer). `lib/` is stable from `validator_start` to `validator_end`.
- 1a: every pre-existing function body unchanged (AST comparison against `base_sha`), one named exemption: `report.py::build_report`.
- 1b: `build_report` may gain only constant-valued pinned keys (`model_pin_env` included) and the nested constant `tokens.cache_hit_ratio`; the gate strips those entries and requires the remainder to equal the `base_sha` body. A computed value or any other edit fails.
- 1c: new stub functions are inert by AST (only `pass`, docstring, or return of a constant); never `raise`. `load_baseline` stub returns `{}`.
- 1d: `Metrics` gains exactly three constant-default fields `model_primary`, `models_observed`, `cache_hit_ratio` (class-body gate); no methods, no non-constant defaults.
- Red-first: at `validator_start` the `real_shape` and capture-failure tests are collected, all FAIL, every message starts `AssertionError` or `Failed: DID NOT RAISE`. `ImportError`, `ModuleNotFoundError`, `SyntaxError`, `TypeError`, `AttributeError`, `NameError`, `NotImplementedError`, or a collection error voids the evidence. A hard-coded-constant P0 is caught by "every test FAILED" (one passing value test fails the rule).
- The gate checker is a real script authored by the validator (arch experiment code is not shipped).

### 5.4 Line budgets
- `delivery-flow/SKILL.md`: Tier A, 500 cap, now 499. After S2 and after S3 `wc -l` MUST print 499 (net zero; both version blocks stay 4 lines; stamps are value-only).
- `product-delivery/SKILL.md`: 300/300; any prose edit is net zero; S2(c) makes no version edit beyond what is needed (ledger only).
- Tier B 300, Tier C 200 unchanged; `python3 scripts/check_skill_budgets.py` exit 0 after S2, S3, and at Block B.
- `prompt-engineer/SKILL.md` has no tier key (520 lines); one line replaced by one line.
- A cap breach is a defect fixed by shortening prose. `Budget-Exception:` cannot be used (ship is a direct push; PA-20).

### 5.5 Cache prefix re-freeze
Before S2 starts, record `sha256sum` of delivery-flow SKILL.md (`43067c9e...b8328` at Stage 4 time), the governance file value, and the telemetry `prefix_hash` (`head -c 2048`, `8c2ebf97...`). After S3 and after any DoD rework of S2/S3: S6 rewrites `governance/cache-prefix-hash.txt` (one command), prints before/after for all three, AC-6.1 prints `MATCH`. Any later edit to delivery-flow SKILL.md (including DoD rework or a stamp date change) means re-freeze again before S5b and before ship. Block B step 7 re-checks `MATCH` on the squashed commit.

### 5.6 Paid-run controls
- Local only: `claude` CLI is never used in `.github/workflows/` (memory: claude-code-local-only; AC-1.3).
- Fixture capture: `--max-budget-usd 0.25`, at most 2, after H1.
- S5b: 5 samples sequential, `--model opus --effort xhigh`, per-sample cap $3.00, HARD aggregate $15.00 over ALL run reports including aborted: before every run `spent + 3.00 > 15.00 => stop` (PA-22), at most 7 runs enforced by run-dir count (PA-22), aborted paid runs count against the aggregate, 30 min wall ceiling per run, `--out-dir "$SMOKE_OUT"`, spend snippet before each run and at Block B step 1a, `s5b-spend.txt` tracked, `operator_go:` line in each dispatch prompt (H2) before the first run and before each re-run past run 5 (section 1.4).
- Missing `total_cost_usd` or `report.json` counts as a failure ($3.00), never zero.
- An outcome-failed sample aborts `--init-baseline`; it is never averaged in.
- Committed captures pass the scrub and secret scan (PA-14).
- The push needs H3 (and any corrective push needs H6); there is no standing approval.

### 5.7 Dogfooding (memory: validate by using)
- S1: run the real guard on the real tree, the canary in a `mktemp` copy, the hook in a temp repo, the pre-push hook on stubs.
- S2 and S3: run the guard, `check_skill_budgets.py`, and the AC snippets on the real files; AC-2.3b reviewer re-fetches docs itself.
- S4: run `test_meta.py` (3 passed) and the tree sweep.
- S5a: run the parser on the real-shape fixture; red run then green run.
- S5b: the live baseline is the dogfood of the harness; `claude --version` and observed model recorded.
- S7b: fresh clone of `origin/main`; guard, canary, budgets, hash, AC-DISP.
- Code review alone never closes a story; a validator pastes command output.
- If the S2 or a later dispatch finds a fact contradicting the docs, the story stops and raises a defect.

### 5.8 Stage entry and exit checks
- Stage 6 entry: Stage 5 DoD passed, `base-sha.txt` planned in S1, `hooksPath` logged, `$SMOKE_OUT` created (`mkdir -p`).
- Stage 6 exit: DoD per config `dod_validators.development` [developer, qa, architect, tech-writer] per unit round; G1..G4, G6, G7, G9 closed; G5 partly (D1a).
- Stage 7 entry: Stage 6 DoD DONE, S6 `MATCH`, H2 given.
- Stage 7 exit: DoD [qa, devops, po, tech-writer]; G5 closed; G8, G10 closed after S7 and S7b.

### 5.9 Re-entry rule (S5b defect after Stage 6 DoD)
If S5b (Stage 7) exposes a defect in code or prose that Stage 6 called DONE:
1. Return to Stage 6 with a fix story (red-first under 5.3 if it touches S5a code; fresh validator id).
2. Re-run Stage 6 DoD for the touched files only.
3. If any SKILL.md changed, re-freeze the cache hash (5.5, S6) and re-check `MATCH`.
4. Re-run the PA-24 dry-run if `baseline.py`, `runner.py` or `report.py` changed.
5. Resume UAT. Aborted paid runs already made still count against the $15.00 aggregate and the 7-run cap; a re-run past run 5 needs a fresh H2 go.
6. A fix after S5b that edits prose measured by the baseline invalidates the baseline (P6): re-capture within the ceiling, or PO writes a dated waiver in `07-uat/`.

## 6. Stage 5 DoD self-check

Config: `dod_validators.plan: [sm, po, qa, developer, devops]` (from `.delivery/config.yml` lines 56 to 63). Five roles, five distinct dispatches at most per checkpoint; light routing means fewer is allowed (cap, not target). Config `pipeline.checkpoints: []`: no human checkpoint at this stage.

Author self-check (I am the producer; these are not validations):

| Validator | Checks the plan should pass | Self-assessment |
|---|---|---|
| sm | Ordered stories, dependencies acyclic, effort sized, no story over ~2 days (S5a is L, sequenced in 3 sub-steps), commit and dispatch rules clear, capacity note | Covered: sections 2, 5. Gap to watch: S5a size. |
| po | Every open PO item decided with evidence; gates named with owner and timing; no invented approval; PRD deviations recorded; backlog updated | Covered: section 1, backlog note. |
| qa | Every FR and AC mapped to a story and a validator; PA ACs are testable; red-first, P0 rules, paid controls testable; producer != validator | Covered: sections 3, 5.3. Round 2: every PA now carries a command and expected output (PA-8, 12, 13, 22 fixed; PA-9, 13b, 23 to 27 added). |
| developer | File scope per story exact; ADR conformance; no scope creep; effort realistic | Covered: section 2. Gap: file paths for `orchestrator-doctrine.md` and `smoke-test-architecture.md` taken from the arch doc; S2/S4 must confirm with `ls` first. |
| devops | Ship gate, spend caps, hooks, workflow triggers, S7b, human gates before push and spend | Covered: sections 1.3, 1.4, 5.6, PA-6, PA-20, PA-22 to PA-26, S8. |

Status: DoD passed 5/5 (sm, po, developer round 1; devops, qa round 2), 0 blocking. Revision 3 folded the non-blocking round-2 warnings (section 8). Stage 6 next.

## 7. Revision 2 changelog (DoD round 1 findings to dispositions)

Date: 2026-09-20. Round 1: sm DONE, po DONE, developer DONE, qa NOT_DONE (3 blocking), devops NOT_DONE (3 blocking).

| Finding | Disposition | Location |
|---|---|---|
| QA B1 (WEAKENED soft pass) | FIXED: WEAKENED = AC-5.5c FAIL unless a dated PO waiver file `07-uat/ac-5.5c-waiver.md`; UAT DoD checks for it | PA-15 |
| QA B2 (baseline writer untested; no re-entry) | FIXED: dry-run of `init_baseline` with stub `claude`, abort and aggregate logic; re-entry rule incl. aggregate accounting and re-freeze | PA-24, section 5.9, S5a row, matrix row |
| QA B3 (PA-9 gap; PAs without commands) | FIXED: PA-9 added (hooksPath install+log); PA-8, PA-12, PA-13, PA-15, PA-22 given command and expected output; new PAs each carry one | section 3.2 |
| DevOps B1 (soft $15.00 ceiling) | FIXED: `spent + 3.00 > 15.00 => stop`, run-dir count for max 7, H2b reworded true (5 x $3 = $15.00 exactly) | H2, H2b, PA-16, PA-22, 5.6 |
| DevOps B2 (operator_go, blocked_on) | FIXED: gate protocol, direct human turn only, `blocked_on: H<n>`, background-job behavior, PA-23 | section 1.4, PA-23, 5.6 |
| DevOps B3 (fix-forward, H6, post-push green) | FIXED: S8 story, H4-FAIL branch, H6, `gh run list --commit` (UNVERIFIED manual = FAIL if `gh` absent) | S8 row, H4-FAIL, H6, PA-26 |
| Should: add H5 to stage-summary; dod_rounds | FIXED | stage-summary.md |
| Should: branch move to main checkout; H3 "no" state | FIXED | H3, PA-25 |
| Should: H4 docs-only proof; report file name | FIXED: `git diff --name-only` limited to `.delivery/`; `ship-verification.txt` per ADR-lmr-005 | PA-25, S7b row |
| Should: S1 hooksPath AC, shared config note | FIXED | PA-9, section 1.3 note |
| Should: S1 prompt `git add` new files | FIXED | S1 row |
| Should: S4 0.5d, S5a 2d | FIXED | section 2 |
| Should: AC-DISP SKIPPED = FAIL for S7b | FIXED | PA-21 |
| Should: files-scanned floor | FIXED: K equals baseline tracked-file count | PA-7 |
| Should: P0 gate negative self-test | FIXED | PA-12 |
| Should: S1 fixtures validator-owned | FIXED | S1 row |
| Should: disjointness for all stories | FIXED | PA-13b, section 2 |
| Should: real-shape fixture = H1 capture | FIXED: hash in provenance | PA-14 |
| Should: FR-1.4/FR-2.4 mechanical | FIXED: dispatch prompt grep | PA-27, matrix |
| DevOps W5 (budget workflow dry-run with `PR_BODY` unset) | DEFERRED: covered by D4 evidence and PA-6 `workflow-injection-lint`; S1 validator adds `env -u PR_BODY` run to the S1 report | PA-6 |
| DevOps W7 (stale `05-plan/dod/`) | FIXED | 5.1.9 |
| QA W1 SKIPPED | FIXED (see above) | PA-21 |

Sm, po, developer warnings: not re-opened; DONE verdicts stand.

## 8. Revision 3 changelog (DoD round 2 non-blocking warnings, wording and precision only, no new scope)

Round 2: devops DONE, qa DONE, 0 blocking. Wording only.

| Warning | Disposition | Location |
|---|---|---|
| QA W-A negative test for `check_distinct.py` | FOLDED: identical copies and no-id set must print `WEAKENED` rc 1; `--self-test` | PA-15 |
| QA W-B files-scanned floor, odd prefix | FOLDED: live count, baseline `B` (line 2 of `base-sha.txt`) is a floor; prefix removed | PA-7, PA-8 |
| QA W-C PA-9 in matrix | FOLDED: S1 row | section 3.1 |
| QA W-D Decimal, one spend implementation | FOLDED: `Decimal`; PA-16 and PA-24 use `spend_check.py` | PA-16, PA-22, S5a row |
| QA W-E checker owner, path, scope | FOLDED: all five checkers listed in S5a validator scope under `delivery-team/tests/smoke/tests/`; qa publishes `spend_check.py` before H2 | S5a row |
| QA W-F PA-24 return codes | FOLDED: one invocation, rc 0 only if all sub-cases as expected; ceiling rc 3 asserted inside | PA-24 |
| QA W-G S7b topology | FOLDED: slug tree from original project path, manifest outside clone, absent tree = FAIL | PA-21 |
| QA W-H PA-27 is a floor | NOT FOLDED: QA marked note only, acceptable for light stage | none |
| DevOps W1 owners for `spend_check.py`, `dry_run_baseline.py` | FOLDED (with QA W-E) | S5a row |
| DevOps W2 killed run before run dir | FOLDED: attempt log written BEFORE launch; count = max(run dirs, log lines) | PA-22 |
| DevOps W3 true worst-case total | FOLDED: about $15.50 stated in H2 | H2 |
| DevOps W4 grep dot | FOLDED: `^\.delivery/` | PA-25 |
| SM r1, PO r1, developer r1 | VERIFIED: S4 ~0.5d, S1 `git add` new files, hooksPath shared-config note, PA numbering, H5 all present. Stage summary updated | section 2, PA-9, stage-summary |

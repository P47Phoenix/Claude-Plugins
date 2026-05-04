# Gate Failure Patterns

**Entries**: 24 | **Last updated**: 2026-04-23

## Common Failure Patterns

- **Incomplete FR traceability**: Design and Plan stages fail when artifacts don't map to ALL PRD FRs. Validators check FR-by-FR. Solution: verify full traceability before submitting. (validated: 1, last: run-2026-03-27-c8f2)
- **Missing capacity declaration**: Plan stage fails without explicit velocity baseline, 80% ceiling, and per-sprint commitment. SM always checks this. (validated: 2, last: run-2026-03-29-h3k7)
- **Stale derived artifacts**: Dev stage fails when generated files (schema.json, docs) are not regenerated after source changes. Architect always checks this. (validated: 1, last: run-2026-03-27-c8f2)
- **Deferred P0 items**: UAT fails when P0 requirements (dogfooding, docs) are treated as follow-ups. PO always checks this. Execute P0s before submitting. (validated: 1, last: run-2026-03-27-c8f2)
- **Phantom file references**: Idea briefs and architecture docs reference files that don't exist (e.g., database.py). Architect validator catches these on first DoD round. Always verify file paths with Glob before citing them. (validated: 1, last: run-2026-03-28-k4m9)
- **Wrong filenames in scripts**: Scripts referencing wrong file names (routing.json vs stage-routing.json) are caught by QA structural verification in UAT. Reconcile filenames across scripts and rule files. (validated: 1, last: run-2026-03-28-k4m9)
- **Design positional references**: UX designs referencing wrong wizard question positions or file formats (state.json vs state.md) are caught by Architect validator. Cross-reference all filenames and positions against source of truth. (validated: 1, last: run-2026-03-28-k4m9)
- **Capacity overcommitment**: Plan stage fails when total commitment exceeds 80% ceiling. Markdown-only edits need calibrated estimates (one tier lower than code changes). SM always checks this. (validated: 1, last: run-2026-03-29-h3k7)
- **Adversarial target adjustment**: Adversarial reviewer at Refine can productively adjust targets (e.g., Design 80%→70%) based on thin baseline data. Trust challenger confidence ratings when data is sparse. (validated: 1, last: run-2026-03-29-h3k7)
- **Gate-patterns memory injection yields compound returns**: Run r4x2 achieved 100% first-try DoD (6/6 stages) — the first perfect run. Injecting gate-patterns lessons before stages with <80% historical pass rate is the strongest correlate. (validated: 1, last: run-2026-03-30-r4x2)
- **Plan stage is a systemic weak point (57% first-try, 4/7 runs)**: Three failures in seven runs — ceiling violations and missing artifacts. Root cause: planning agents lack pre-loaded constraints. Fix: inject sprint ceiling + mandatory artifact list into planning agent prompts, not just validators. (validated: 1, last: run-2026-04-02-k3r9)
- **hooks.json phantom references are a recurring Dev DoD failure**: hw01 had 2 BLOCKING findings because hooks.json referenced scripts that didn't exist. Always verify every script path in hooks.json exists on disk before Dev DoD submission. Add to pre-DoD checklist. (validated: 1, last: run-2026-04-12-hw01)
- **Security DoD catches real issues at Architect stage**: hw01 Security validator found path traversal and BOM data exposure — both legitimate. Security review at Architect is not ceremony; it catches architectural security gaps that other validators miss. (validated: 1, last: run-2026-04-12-hw01)

## Validator Selection by Defect Class (run-2026-04-20-o4v7)

- **Developer DoD catches command-validity bugs by construction**, and no other validator does. Reading-only validators share the author's parsing assumptions. If the artifact names executable commands (grep, bash, path lookups, config-key reads), Developer DoD must actually run them or the bugs ship. Stage 2 caught 3 real bugs (regex missed match, wrong alias path, `parallel_validators` treated as count not boolean) that all 3 reasoning-only DoD validators accepted. (validated: 1, last: run-2026-04-20-o4v7)
- **Evaluator-Optimizer catches AC-precision defects.** Best for tightening existing criteria (vague→concrete, "better"→numeric, implicit→explicit). Refine loop-2 QA hardened "≥1 WebFetch" to "≥2 WebFetch AND ≥2 distinct hostnames" — closing the reason-instead-of-fetch regression window. (validated: 1, last: run-2026-04-20-o4v7)
- **Adversarial Review catches structural/framing defects.** Best for end-to-end reads by a fresh-context reviewer: ADR status smells, measurement gaps, wave-placement inefficiencies, missing worked examples. The author is too close to see these. (validated: 1, last: run-2026-04-20-o4v7)

## Convergence Heuristics (run-2026-04-20-o4v7)

- **Two-loop Adversarial is worth the cost when artifact has ≥10 findings or ≥14 work items.** Loop 2 usually hardens an AC that loop 1 surfaced but didn't fully close. Single-loop is enough for single-file FEATUREs. (validated: 1, last: run-2026-04-20-o4v7)
- **ACCEPT-with-findings + 1 revision is the convergent pattern** when reviewers surface tactical (not structural) findings. Authors absorb priorities in rev 1, all DoD validators pass first DoD round. (validated: 1, last: run-2026-04-20-o4v7)

## Signal Robustness (run-2026-04-20-o4v7)

- **Signal blocks must be emitted early in sub-agent responses, not last.** Rate-limit interruptions can truncate the final response block; the artifact on disk may be complete while the STATUS line is lost. Orchestrator falls back to file-inspection. Consider front-loading the signal in agent prompts. (validated: 1, last: run-2026-04-20-o4v7)

## Success-Gate Authoring (run-2026-04-22-4x7e)

- **Allowlist-over-deny for mixed-version CI guards.** When a family migration is uniform (everything → N), a single deny regex suffices. When it is mixed (Opus → 4.7, Sonnet → 4.6, Haiku → 4.5-dated), only allowlist-over-deny survives the next bump. The 2026-04-22 canonical set pinned in `.github/workflows/stale-model-id-guard.yml`: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`. Everything else dated = stale. (validated: 1, last: run-2026-04-22-4x7e)

- **Provenance comments + CI-guard allowlist travel as a named pair.** ADR-002's `# prior: <retired-id>` breadcrumb pattern is the feature; the CI guard's `^\s*#` exemption keeps the guard from fighting the feature. Edit one → review the other. (validated: 1, last: run-2026-04-22-4x7e)

- **Success gates and the WIs that close them must be explicitly bound at plan time.** When §7 gate scope is wider than the nearest WI's edit surface, the gate or the WI is misscoped. Bind every §7 gate to the WI that closes it at Refine DoD time; Developer DoD dry-runs each gate to catch paper-trace gaps. Caught G-5 (WI-05 scope < §7.4 scope) in run-2026-04-22-4x7e; would have shipped a false-failing success gate. (validated: 1, last: run-2026-04-22-4x7e)

- **PRD §7 stale-ID regexes must exempt provenance comments.** Canonical form: `! grep ... | grep -vE '^[^:]+:[[:space:]]*#'`, or use `git grep` with pathspec allowlists. F-UAT-01 in run-2026-04-22-4x7e: the literal one-liner returned exit 1 after the WI-10 sweep because of three intentional `# prior:` comments. Intent satisfied; literal gate broken. (validated: 1, last: run-2026-04-22-4x7e)

- **Mid-run flags from impl WIs to later WIs are a cheaper safety net than upstream paper-review alone.** When an implementer notices an upstream contradiction that will bite a later WI, a `## Flag to WI-N — <title>` section in the dev-log lets the orchestrator route the correction before the flagged WI lands. Gimli's WI-10 → WI-14 mixed-version regex flag closed the ship-bug pre-merge. Codify as a first-class dev-log section in future engagements. (validated: 1, last: run-2026-04-22-4x7e)

## Mandatory-Rollout Side-Effects (run-2026-05-03-tk0e)

- **Any "add 1 line to N files" rollout MUST simulate the per-file line delta before commit; near-budget edges become budget violations.** Wave 0 added `tier:` frontmatter to all 13 delivery-team SKILL.md files (+1 line each) — alias-creator was at exactly 200 lines (Tier-C limit) and crossed to 201, becoming over-budget by the very gate the rollout was introducing. Action: any mass rollout MUST run `wc -l` against the target set BEFORE the rollout to identify files at-or-near-limit; either pre-trim those files in the same WI or pre-register them as known-debt. (validated: 1, last: run-2026-05-03-tk0e)

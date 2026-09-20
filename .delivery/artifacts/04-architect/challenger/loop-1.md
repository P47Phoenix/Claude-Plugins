<!-- run: run-2026-05-28-o48m -->
# Challenger Review, Loop 1: Stage 4 Architecture, BACKLOG-108 (latest-model references)

Role: challenger (adversarial reviewer only). Fresh reviewer, no prior-loop context. Reviewed: `architecture.md`, `ADR-lmr-001..005`. Decision itself (refer to latest, no pins) is binding and was not re-debated.

Overall verdict: design is sound and its measured claims are accurate. No blocking findings. Five significant-or-minor gaps worth fixing before Plan.

**CONFIDENCE: 4/5** (ready for Plan after the two significant fixes are noted in the Plan handoff).

## Findings

Severity counts: 0 blocking, 2 significant, 7 minor.

### F1 (significant, coupling) Fourth "prefix" consumer missed: `telemetry.py` hashes the first 2048 bytes of SKILL.md

Claim under attack (ADR-lmr-001 Context): "No script, workflow or hook consumes the hash file", and the table of "three descriptions of the prefix". The governance-hash half is true. But a live consumer of the "bytes 0..2048" notion exists that the ADR never lists.

Evidence:
```
$ grep -n 'PREFIX_READ_BYTES\|_compute_prefix_hash' delivery-team/hooks/telemetry.py
21:PREFIX_READ_BYTES = 2048
46:def _compute_prefix_hash(skill_md: Path) -> str | None:
47:    """Return sha256[:8] of first PREFIX_READ_BYTES of SKILL.md, or None on error."""
$ grep -n prefix_hash delivery-team/references/telemetry-schema.md
23: | `prefix_hash` | string | Yes | `sha256(SKILL.md[:2048])[:8]` ...
```
Every skill load writes a telemetry row whose `prefix_hash` is `sha256(first 2048 bytes)[:8]`. S2/S3 change bytes 0..2048 (first diff at byte 854, ADR-001 table), so `prefix_hash` for delivery-flow changes at ship. So the "2048-byte prefix" is real code behaviour (ADR-tk0e-001), not only a stale comment; the false part is only the "end of Phase 3" wording. No test pins the old hash (`grep -rn prefix_hash` finds only telemetry.py and the schema doc), so nothing breaks, but the ADR's "prefix story is false" framing and "one deliberate cache invalidation" record are incomplete.

Required fix: add a fourth row to the ADR-lmr-001 table (`telemetry.py`, bytes 0..2048, `sha256[:8]`), state that delivery-flow telemetry `prefix_hash` changes once at ship (expected, no code change), and soften "false" to "the SKILL.md comment is inconsistent; the telemetry definition (0..2048) is the only executable prefix".

### F2 (significant, data-integrity) Ship gate scans the working tree, not the commit that is pushed

ADR-lmr-005 item 8 and ADR-lmr-002 D8: step 2 runs `check_model_pins.py` (scope includes untracked and unstaged working-tree content) and step 6 pushes. Nothing requires a clean tree, and nothing scans committed content. An unstaged edit that removes a pin, or a pin only in HEAD but fixed in the working copy, passes the gate while the pushed commit still contains the pin (the reverse also holds: an untracked file fails the gate but is never pushed). The D8 hook has the same acknowledged limit (`--paths` reads the working file, not the index).

Evidence: script scope is `git ls-files --cached --others --exclude-standard` filtered by `os.path.isfile`, reading `open(f)` from disk (PRD canonical command lines 38-45 in `prd.md`). No `git status --porcelain` or `git diff --quiet` step in item 8 or D8.

Required fix: add ship step 0b: `git status --porcelain` must print nothing (after the squash commit), then run the guard; or run it from a clean `git worktree add` of the commit to be pushed. Record that in AC text at Plan.

### F3 (significant, security) No-PR direct push: ship control is self-reported by the same actor, and the budget gate has the same hole

ADR-lmr-002 D7/D8 and ADR-lmr-005 item 8 admit the workflow only detects after the push, the pre-push hook is optional and opt-in, and "the reviewer of the ship reads that line" (step-2 output pasted by the executor). `--no-verify` bypasses hooks. Also the pre-existing budget workflow is PR-only:
```
$ sed -n 1,8p .github/workflows/skill-line-budget.yml
on:
  pull_request:
    paths: ['delivery-team/**/SKILL.md', 'governance/skill-budgets.json']
```
so S7 step 4 (local budget run) is also the only pre-push control for line budgets; the design does not mention that the budget workflow never runs on a direct push either.

Required fix: (a) make the pre-push hook part of S1 (not "PO confirmation"), or have S7 include an independent post-push check: a different agent re-runs the guard and `check_skill_budgets.py` on `origin/main` and reports; (b) extend the `push` trigger to `skill-line-budget.yml` (small edit, `plugin-dev:hook-development` route) or state explicitly that budgets are unenforced on push.

### F4 (minor, docs) Live effort documentation contradicts OQ-5 / OQ-8 wording

Architecture OQ-5: "The docs say the API default is `high`"; OQ-8: "no fetched text states the default for the latest Opus". Live model-config page does state a Claude Code default per model (quote in doc table below): `high` is the default on every model except Opus 4.7, where `xhigh` is the default. So (1) OQ-8 is partly answerable now (documented for a named version, still not for "latest"), and (2) the runner's `--effort xhigh` default is redundant for Opus 4.7 but would be non-default on any other model, and the CLI reference says "Available levels depend on the model", so `_build_claude_command(..., effort="xhigh")` with `model="sonnet"` or `"haiku"` may be rejected or degraded.

Required fix: update OQ-8 text; in ADR-lmr-004 pin `effort` to be dropped (not passed) when `model != "opus"`, or state that the smoke runner only supports `opus`.

### F5 (minor, testability) Mid-run cost cap cannot fire on real streams; budget-stop detection rests on an unconfirmed string

`runner.py` lines 95 and 252 kill the process when `_running_cost(events) > cost_cap`. On real streams cost lives only on the final `result` event (ADR-lmr-004 context), so during the run `_running_cost` returns 0.0; the ADR's new `_running_cost` contract ("return `total_cost_usd` if a result exists, else legacy sum") does not restore live enforcement. Real enforcement is therefore the CLI flag plus the post-check, which is what the ADR says (P12), but the ADR presents "two layers" without stating that the runner's in-loop kill is dead code for real shape. Live CLI reference for the flag:
> "Maximum dollar amount to spend on API calls before stopping (print mode only). ... Once spend reaches the cap, spawning another subagent fails with `Budget limit reached`, and Claude Code stops background subagents that are still running"

That text describes subagent spawn failure, not a documented result subtype; the ADR's "subtype contains `budget`" substring rule (UNVERIFIED) may never match. Required fix: also map exit 2 on case-insensitive `budget limit` in the `result` text or an `is_error` result with cost >= cap*0.99; state in the ADR that the in-loop check is legacy-only.

### F6 (minor, coupling) Third tier-label vocabulary exists outside `MODEL_TIER_ALIAS`

```
$ grep -n '"model": "claude-' prd-quality-gate-flow/stage_definitions.py
51: "model": "claude-sonnet"   (also 87, 154, 185; "claude-haiku" at 119, 220, 247)
prd-quality-gate-flow/README.md:306:        "model": "claude-sonnet",
```
These labels contain no digit, so `PIN_RE` does not match them and S4 does not touch them; they form a second, differently spelled vocabulary (`claude-sonnet` vs `sonnet`). ADR-lmr-003 A1 and NFR-12 claim one Python definition point but scope silently to `agentic-flow-builder/`. Required fix: state the scope in ADR-lmr-003 ("only `agent_registry.py`; `prd-quality-gate-flow` labels are out of scope, digit-free, guard-neutral") so a future reader does not read NFR-12 as repo-wide.

### F7 (minor, naming) Closed alias vocabulary omits `fable`

Live CLI reference for `--model`: "a model alias such as `sonnet`, `opus`, `haiku`, or `fable`". AC-4.6 and A3 pin frontmatter to exactly `opus|sonnet|haiku`; `PROSE_RE` already knows Fable and Mythos. A `model: fable` frontmatter would fail AC-4.6 today. Required fix: note in ADR-lmr-003 that the vocabulary is a deliberate closed set to be widened by editing AC-4.6 (one place), and that `fable` is a known documented alias.

### F8 (minor, docs) Broken cross-references between architecture.md and ADRs

- ADR-lmr-001 Consequences: "carried as a risk (architecture.md section 9, U3)" for the `## Volatile` comment defect. Section 9 is the NFR table; U3 is a parser item; the risk is P10 in section 7.
- ADR-lmr-003 Consequences: stale SQLite rows "logged as risk U6"; that row is P9 (U6 is the producer/validator observables item).
- ADR-lmr-004 section 7 and ADR-lmr-005 item 1 point to "architecture.md section 6" for live-capture placement; that text is in section 5 ("Where the live baseline runs"); section 6 is the OQ table.
- architecture.md mermaid draws `S5a --> S6`, while the prose says S6 depends only on S3 and merely follows S5 by order. Harmless but the graph overstates a dependency.
Required fix: correct the four references so Plan carries the right IDs.

### F9 (minor, testability) BINDING-4.5 separation is order-provable, not authorship-provable

ADR-lmr-004 section 6 uses `Dispatch-Id` trailers and `git merge-base --is-ancestor` (ordering). Trailers are typed by the same orchestrator and all commits share one git identity, so the check proves "validator commit precedes fix commit", not "a different agent wrote it". ADR-lmr-005 item 6 cross-checks trailers to manifests, which are also written by the orchestrator (P13). The ADR half-acknowledges (QA W5). Required fix: name it an accepted limit in ADR-lmr-004, and add one independent artifact: the validator's returned agent id recorded verbatim from the Agent tool result in the manifest, not typed by hand.

### F10 (minor, testability) Guard extension scope leaves undeclared blind spots

Scope is `.py .md .yml .yaml .txt .sh` only. Tracked files outside it: 19 `.json`, `.githooks/pre-commit` (extensionless), `Makefile`, one `.jsonl`. Today none carries a pin (`git ls-files '*.json' | xargs grep -nE '"model|claude-|opus|sonnet|haiku'` shows only the marketplace name), so it is a latent hole, and only `.json` is declared out-of-scope by ADR-lmr-002 D3. Also loopholes the ADR accepts were confirmed by run (see command log): `claude_opus_4_7`, `OPUS_5`, `Sonnet<NBSP>5` all pass. Required fix: one sentence in ADR-lmr-002 listing extensionless and other extensions as out of scope by decision; PO decision on separator tightening stays as already carried (P5).

## Attack-surface results (what held)

1. Cache fingerprint (ADR-lmr-001): every number reproduced (below). Whole-file scope plus S6 re-freeze is correct for the governance hash. Only gap is F1.
2. Line-budget math: 499/500 delivery-flow, 300/300 product-delivery, holds. Both 4-line blocks replaced 4-for-4. `prompt-engineer/SKILL.md` (520) has no tier key and is outside the checker (`glob("delivery-team/**/SKILL.md")`), so no hidden cap. Stamp census: 25 files, 26 `model_awareness` lines (prompt-engineer has a second example stamp block at lines 415-417, covered by the same value-only edit), 11 with `fitness_review_due`. No line-changing edit found.
3. Guard design: self-match checked, the five constants do not match their own source text (run in command log); scope and bootstrap ordering hold given one squashed push. Gaps F2, F3, F10.
4. Alias/stamp: only reader of stamps is `skill-md-header-warn.yml` (presence check). `model:` frontmatter only in 4 SKILL.md files, `phase_1_detector_model` in 5, no agent files. `MODEL_TIER_ALIAS` single point holds inside `agentic-flow-builder` (F6 for the rest).
5. Smoke contract: description matches code. `parse_stream` reads top-level `usage`/`model`, buckets missing model as `"unknown"`, counts every usage event as one dispatch, `test_meta.py` uses legacy flat shape, so the two-mode parser and the stub-first ordering are the right call. Gaps F4, F5.
6. Dispatch/ship: S1..S7 order, S5a/S5b split, parallel windows all internally consistent; the only ordering error is the drawn edge in F8. No hidden hazard: S5a changes no SKILL.md, S6 re-freeze precedes the live capture.
7. U1..U11 and P1..P14: none blocking. P1 (capture in Stage 6 vs 7) and P2 (multi-manifest AC-DISP) are correct Plan decisions. Missed PRD/code contradictions are F1, F5, F6.
8. Doc re-fetch: see table.

## Class summary

| Class | Count | Findings |
|---|---|---|
| coupling | 2 | F1 (significant), F6 (minor) |
| security | 1 | F3 (significant) |
| data-integrity | 1 | F2 (significant) |
| naming | 1 | F7 (minor) |
| testability | 3 | F5, F9, F10 (minor) |
| performance | 0 | |
| docs | 2 | F4, F8 (minor) |
| misc | 0 | |

Severity: 0 blocking, 3 significant (F1, F2, F3), 7 minor (F4-F10).

## Doc re-fetch (binding, WebFetch on 2026-09-20)

| URL | Architecture claim | Live page | Result |
|---|---|---|---|
| https://code.claude.com/docs/en/model-config | Alias table: `opus`/`sonnet` latest, `haiku` "fast and efficient" (no "latest"); "Aliases point to the recommended version ... To pin ... use the full model name ... or set ... `ANTHROPIC_DEFAULT_OPUS_MODEL`" | Rows: "`opus` Uses the latest Opus model for complex reasoning tasks", "`sonnet` Uses the latest Sonnet model ...", "`haiku` Uses the fast and efficient Haiku model for simple tasks". Sentence matches, with the example "for example `claude-opus-5`" in place of the architecture's ellipsis | MATCH |
| https://code.claude.com/docs/en/model-config (effort) | OQ-5/OQ-8: "API default is `high`"; no fetched text states the Claude Code default for the latest Opus | Effort table: "`high` ... The default on every model except Opus 4.7"; "`xhigh` ... The default on Opus 4.7" | MISMATCH (partial; F4) |
| https://code.claude.com/docs/en/headless | "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins"; `total_cost_usd` with `--output-format json`; `parent_tool_use_id` null for main; "`--bare` is the recommended mode ... and will become the default for `-p` in a future release"; bare never reads OAuth | All five quotes present verbatim ("Messages from the main conversation carry `null` in that field"; "In bare mode, Claude Code never reads OAuth credentials or the system keychain"). Page does not name the init model field and never mentions `message.id`, consistent with the ADR's UNVERIFIED flags | MATCH |
| https://code.claude.com/docs/en/cli-reference | `--model`, `--effort`, `--max-budget-usd`, `--bare`, `--fallback-model` exist; budget stops at cap | All present. `--max-budget-usd`: "before stopping (print mode only)... spawning another subagent fails with `Budget limit reached`"; `--model` lists alias `fable` too; `--effort` "Available levels depend on the model" | MATCH on existence; adds F5, F7, F4 nuance |

## Commands run and outputs (worktree root)

```
$ wc -cl delivery-team/skills/delivery-flow/SKILL.md
  499 28616 delivery-team/skills/delivery-flow/SKILL.md
$ sha256sum delivery-team/skills/delivery-flow/SKILL.md ; cat governance/cache-prefix-hash.txt
43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328  (both lines identical)
$ grep -bn '^## ' delivery-team/skills/delivery-flow/SKILL.md
1892 Phase 0 | 9477 Phase 1 | 12135 Phase 2 | 13429 Phase 3 | 15479 Phase 4 | 27209 Volatile
$ head -c 2048 ... | wc -l  -> 39 (byte 2048 falls in line 40; head -39 | wc -c = 2018)
$ head -c 2048 ... | sha256sum | cut -c1-8 -> 8c2ebf97     (ADR: 8c2ebf97, MATCH)
$ head -c 15479 ... | sha256sum | cut -c1-8 -> ac03f1f2    (ADR: ac03f1f2, MATCH)
$ head -248 ... | wc -c -> 15479
$ python3 scripts/check_skill_budgets.py | tail -1
BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).
$ wc -l delivery-team/skills/product-delivery/SKILL.md prompt-engineer/SKILL.md
 300, 520
$ grep -rIln 'cache-prefix-hash\|cache_warmup\|prefix-hash' (outside .delivery)
CHANGELOG.md, two stale delivery-team/artifacts/06-dev/*.md, governance/fitness-review.md, delivery-flow/SKILL.md   (no script/hook/workflow)
$ grep -rIn '2048' *.py -> delivery-team/hooks/telemetry.py:21 PREFIX_READ_BYTES = 2048   (F1)
$ grep -rn 'model_awareness\|pattern_library_version' (non-SKILL.md, non-.delivery)
.github/workflows/skill-md-header-warn.yml:21 (presence grep -L 'model_awareness:') only
$ grep -rn '^model:' --include=*.md  -> 4 SKILL.md (ddd, volatility, delivery-flow: sonnet; prompt-engineer: opus)
$ stamp census over git ls-files '*.md' (non-.delivery): 25 files, prompt-engineer/SKILL.md has 4 stamp hits (frontmatter + example block); 11 files with fitness_review_due
$ python3 /tmp/lmr-ch1/t.py  (five PRD regexes on probes)
 pass(-): 'The latest Opus delegates ...', 'model_awareness: latest', 'pattern_library_version: rev-1',
          'claude_opus_4_7', 'OPUS_5', 'Sonnet<NBSP>5', 'use claude-opus-fixture', and the regex-source line itself
 hit: claude-opus-5-20260101 (pin), us.anthropic.claude-opus-5-v1:0 (pin), 'Opus5 is new' (prose), 'Sonnet 5.1' (prose), 'sonnet-5' (prose)
$ git ls-files '*.json' | xargs grep -nE '"model|claude-|opus|sonnet|haiku' -> only marketplace name "mec-claude-agent-skills"
$ git ls-files | grep -c '\.delivery/' -> 332 tracked files excluded from the guard by design
```

Note: compound `git` command lines were refused by the worktree sandbox and were split into single commands; no repo file was modified except this artifact.

# Adversarial Challenge: BACKLOG-108 Latest-Model References PRD (Revision 3)

Role: Challenger only. PRD not edited. Decision "refer to latest, stop pinning" not re-debated; attack is on implementation. All commands run in the worktree root on 2026-09-20. Candidate strings were run through the PRD's exact `PIN_RE` / `STAMP_RE` / `PROSE_RE` in Python `re` (script `/tmp/ch.py`) and `grep -E`. Rule A logic copied from AC-1.2a `hit_a`.

**Overall: 0 blocking, 6 significant, 5 minor. CONFIDENCE 3/5** (buildable, but fix F1-F6 before Stage 3; F2 and F3 would let S3/S5 pass their ACs while defeating intent).

## Findings

### F1 (significant) The guard cannot run at ship time: workflow is `pull_request`-only, PRD ships with no PR
Evidence: `.github/workflows/stale-model-id-guard.yml` lines 3-8: `on: pull_request: paths: ['**/*.py','**/*.md','!.delivery/**']`. PRD FR-7.3 / BINDING-5.1: squash-rebase, ff-merge, push origin/main, "No PR". FR-1.x never specifies the `on:` block. A rewritten guard that keeps this trigger never executes on the direct-to-main workflow, and the `paths` filter also hides `.yml`/`.txt` edits (see F6). The CLAUDE.md `skill-line-budget.yml` guard has the same trait, but here the guard is the sole enforcement of the whole initiative (NFR-10, NFR-11).
Fix: FR-1.1 must state the trigger: `on: push: branches [main]` plus `pull_request` plus `workflow_dispatch`, and an AC (python-stdlib) asserting the workflow text contains a `push:` key. Add a local equivalent (extend the opt-in `.githooks` pre-commit, or a `scripts/check_model_pins.py` that both the workflow and the hook call, so AC-1.2a/c can import the same patterns instead of scraping `NAME='...'` from yml).

### F2 (significant) AC-3.1b passes with version mentions left in prose: PROSE_RE misses bare version numbers
Evidence (scan of all SKILL.md, excluding stamp lines, lines NOT matching `PROSE_RE` but naming a model version):
```
delivery-flow/SKILL.md:30   > under-dispatch is the highest-confidence regression mode on 4.7.
delivery-flow/SKILL.md:276  > short-count dispatch is a Prime Directive violation under 4.7 semantics.
prompt-engineer/SKILL.md:349 "This sub-section isolates 4.7-only guidance ..."
prompt-engineer/SKILL.md:351 "(F-11)"   :359 "4.7 exhibits behavioural changes"   :361 "When in doubt on 4.7"
prompt-engineer/SKILL.md:373 "Pattern 4.2 - 4.7-Aware Role Prompt Skeleton"   :375 "so 4.7 ext..."
```
The PRD's "8 lines in 2 files" counts only `Opus 4.7`-style strings. At least 7 more live version lines (same 2 files) contain `4.7` without a family word. Also the PRD says the guard forbids versions in SKILL.md prose, yet S3's AC-3.1b and Rule B would print 0 / stay green with these present. Additional false-negative forms (all tested, all `miss`): `Opus5`, `opus5`, `Opus  5` (two spaces), `OPUS 5`, `Opus v5`, `Fable 5`, `Mythos 5`, `Opus-class 4.7`, `Opus four point seven`.
Fix: PROSE_RE becomes case-insensitive, allows optional separators and `v`: e.g. `(opus|sonnet|haiku|fable)[ -]*v?[0-9]` (grep needs `-i`), and add a `BARE_RE='(^|[^0-9.])4[.-][0-9]([^0-9]|$)'` limited to SKILL.md lines containing `model|Opus|dispatch|runtime` or simply a curated list of known retired markers (`4.7`, `4-7`, `F-08`, `F-11`, `F-01`). Recount and state the corrected prose census (PRD 8 lines is wrong by at least 7) in S2/S3 scope; add `prompt-engineer/SKILL.md:349-375` and `delivery-flow:30,276` to FR-2.1's named rewrite sites.

### F3 (significant) Guard false negatives on pin forms: Rule A/PIN_RE evaded by legitimate-looking pins
Evidence (Python `re`, Rule A):
| String | Result |
|---|---|
| `"claude-3-5-sonnet-20241022"`, `"claude-3-opus-20240229"` | miss (old naming, version before family) |
| `"claude-sonnet-latest"`, `"claude-3-7-sonnet-latest"` | miss (`-latest` API aliases are not "latest" per docs, but are still pins-by-name) |
| `"claude-OPUS-4-7"` | miss (case) |
| `"claude-mythos-5"` | miss (new family name, allowlist of families inside PIN_RE) |
| `"claude" + "-opus-" + "5"` | miss (concatenation) |
| `model_awareness: "opus-5"` (quoted) | miss |
| `pattern_library_version: 4.7.1`, `v5`, `5` | miss (STAMP_RE only matches digit-dash-digit) |
| `# MODEL_ID = "claude-opus-5"` inside a SKILL.md/.md code fence | exempt (first char `#`) |
| `> MODEL = "claude-opus-5"` | exempt (first char `>`) |
grep -E cross-check: `printf 'claude-opus-4-7\nclaude-3-5-sonnet\n' | grep -E 'claude-(opus|sonnet|haiku|fable)-[0-9][-.0-9a-z]*'` prints only the first line. Hit forms confirmed: `claude-opus-4.7`, `anthropic.claude-opus-4-7`, `claude-fable-5`, `model: claude-opus-5`, `model_awareness:opus-5`, `model_awareness: latest-5`.
Design gap: the family list is a hidden allowlist that must be edited when a family appears, contradicting NFR-11 ("0 guard edits at next release"). Prefer a family-agnostic pin: `claude-[a-z0-9.-]*[0-9]` plus a small explicit exemption list (`claude-code`, `claude-plugin`, `claude-agent`, `claude-fixture`); tolerate case-insensitive; count `claude-3-*` form.
Fix: broaden PIN_RE as above, make STAMP_RE reject any digit after the colon (`(model_awareness|pattern_library_version): *"?[^ #]*[0-9]` with the exception `rev-[0-9]+` for the counter), extend Rule A to ignore the `#`/`>` exemption inside SKILL.md and `.md` code fences (only exempt a `> ` blockquote line if it is not inside a fence; simplest: in SKILL.md, apply PIN_RE to every line, no exemption, same as Rule B), and add all rows above to AC-1.2a as must-hit fixtures.

### F4 (significant) Guard false positives and undefined accepted-loophole for Rule B, plus the `#` heading loophole
Evidence: Rule B applies to every line of every SKILL.md with no exemption. `PROSE_RE` trips on non-version prose:
```
'run haiku 3 times'        B    'Opus 1 of the modes'   B
'this sonnet 14 lines'     B    'opus-2 branch'         B
'claude-haiku-3-cost table' B + A
```
`opus`/`sonnet`/`haiku` are also the alias names the PRD tells maintainers to write (convention 3; `model: opus` frontmatter is legitimate), so any sentence like "use haiku 3 times" or "the sonnet 2 of 3 splits" hard-fails CI. The PRD's own AC-1.2c (`70`, exact decomposition) passes today only because no such sentence exists yet (R4 rated L). Meanwhile Rule A's `#` exemption also exempts markdown headings (`# claude-opus-5 setup`), a cheap bypass.
Fix: require a digit-dot-digit or `-` version shape after the family for Rule B (`(Opus|Sonnet|Haiku|Fable)[ -]v?[0-9]+([.-][0-9]+)?` case-insensitive but exclude lowercase alias-plus-count by requiring an initial capital or a following `.digit`/`-digit`), or define an escape marker (`<!-- model-pin-ok: reason -->` on the line) and log those. State the heading loophole as accepted or close it (exempt `#` only in `*.py` and in fenced shell blocks, not in `.md` headings).

### F5 (significant) FR-5.5 model capture can silently record nothing or `unknown`; evidence cited in the PRD does not hold for live streams
Evidence:
- `delivery-team/tests/smoke/lib/metrics.py:117`: `model_name = event.get("model") or "unknown"`. If no model string is observed it buckets `"unknown"`, which is a string; FR-5.5's "capture FAILS if NO model string is observed" is satisfied by `model_usage.unknown`. PRD must exclude `unknown`.
- `metrics.py` reads top-level `event["usage"]` and `event["model"]` only for `type in (assistant, message, tool_use, result)`. Its only test fixture (`tests/conftest.py:100-160`) is hand-written with top-level `model`/`usage`; no recorded real stream exists in the repo (`fixtures/` contains only `delivery_config_minimal.yml`).
- The only live baseline (`baselines/hello_world_spike.json`) has NO `model_usage.*` keys and its header comment says "cost_usd=0.00 (no usage events emitted in stream ...)". So the PRD claim "metrics.py:117 already buckets model_usage ... observed models are recorded per dispatch" is unproven against a real Claude Code stream; live `assistant` events carry model under `message.model`. `hard_max: 3.0` cost cap is also un-testable with `cost_usd = 0.0`.
- Doc check: headless page confirms `system/init` "reports session metadata including the model" and a per-model cost breakdown in JSON output, but gives no field name (OQ-10); the PRD is honest about that, yet makes S5 depend on OQ-10 being resolved at S5 start with a fixture authored by a different dispatch.
Fix: FR-5.5 must (a) treat `unknown`/empty as absent, (b) be sourced from a REAL recorded `stream-json` fixture (capture one cheap `claude -p --model opus --output-format stream-json --verbose` before authoring meta-tests; store it under `tests/fixtures/`), reading `system/init` model, `message.model`, and the result event's per-model usage, (c) add AC-5.5b (W4-4): meta-tests for no-model stream and mixed-model samples that assert non-zero exit. Also fix `metrics.py` to read `message.model`/`message.usage` if the real fixture requires it (or state that S5 does).

### F6 (significant) Literal-satisfaction: several ACs pass while defeating the intent
1. AC-3.1 (34/34 "reviewed"): satisfied by a one-character change to any non-stamp line. AC-2.1: "changed lines exceed stamp lines changed"; S2 changes no stamp lines, so it holds for any diff of 1 line. AC-2.5: any added line containing "subagent" and "limit" passes, including a comment. None checks that the behavioural guidance is correct or that a reviewer dispatched. Fix: keep the manifest evidence (AC-DISP) as the actual gate and say AC-3.1/2.1/2.5 are floor checks, or add a content check (the rewritten block must contain a `latest Opus` phrase and a numeric spawn cap).
2. AC-4.2 (`claude-opus-fixture` count >= 4): satisfied by a comment line; and AC-4.2 only needs four occurrences, not that the four `"model"` values changed. Fix: assert `"model": "claude-opus-fixture"` >= 4 by regex over string values.
3. AC-4.1 asserts `MODEL_TIER_ALIAS` values but not that `config.model` consumers still work; nothing prevents the developer from also leaving `#` provenance comments containing full pins (exempt, intended) while the code does `os.environ` lookup elsewhere.
4. AC-3.3a (`last_audited >= 2026-09-20`): the prompt-engineer doc example at line ~416 (`last_audited: 2026-04-22`) is a documentation sample; the AC is ambiguous whether it applies to it.
5. G-LIT is owned by S4 but has S2 as a precondition, S1 patterns as a dependency; S1's own AC-1.2c cannot pass until S4 lands (expected, stated). Ordering consequence: S1 through S3 commits leave the guard red; PRD relies on squash so it never sees a partial state (Constraint 6). That is only safe with F1 fixed and no PR.

### F7 (minor) NFR-12 "exactly 1 central definition point" is overstated; `model:` frontmatter aliases exist in 4 SKILL.md and are missed by scope
Evidence: `grep -rnE "^\s*(model|phase_1_detector_model):" SKILL.md`:
```
delivery-team/skills/delivery-flow/SKILL.md:6        model: sonnet
delivery-team/skills/architect/paradigms/ddd/SKILL.md:11        model: sonnet
delivery-team/skills/architect/paradigms/volatility/SKILL.md:11 model: sonnet
prompt-engineer/SKILL.md:5                                       model: opus
architect|operations|product-delivery|ui|quality/SKILL.md:12    phase_1_detector_model: haiku
```
These are already alias-form (good; no ID needed), but (i) they are a second-through-tenth definition point of the same tier vocabulary that `MODEL_TIER_ALIAS` cannot serve (frontmatter cannot import Python), (ii) the PRD never audits them, and (iii) `delivery-flow` declares `model: sonnet` while FR-2.5 writes its dispatch guidance "for the latest Opus", an internal contradiction the S2 reviewer must resolve (either the orchestrator runs on `opus`, or the guidance must be family-neutral). Fix: reword NFR-12 to "one Python definition; frontmatter tier aliases must be one of `opus|sonnet|haiku` (add AC scanning `model:`/`*_model:` values)"; note the delivery-flow mismatch as an S2 decision.

### F8 (minor) Stamp parsing: safe today, but nothing gives `latest` / `last_audited` teeth
Evidence: `grep -rn "model_awareness|pattern_library_version|last_audited"` over `*.py *.yml *.json *.sh *.txt` (non-.delivery): the only consumer is `.github/workflows/skill-md-header-warn.yml:21`, which runs `grep -L 'model_awareness:'` (presence only, `continue-on-error`). `scripts/check_skill_budgets.py` parses frontmatter for `tier:` only (`BUDGET CHECK PASSED: 17 file(s) checked ... rc=0`); `fitness-review.yml` keys off `fitness_review_due:`. So changing values to `latest` / `rev-1` breaks nothing. Residual issues: (a) `latest` is unfalsifiable and `last_audited` is checked only for format (AC-3.3a); (b) the 9 unstamped files keep emitting the existing header warning (FR-3.2 decision; state that the warning stays); (c) `delivery-flow/SKILL.md` has `fitness_review_due: 2026-08-09`, already past today (2026-09-20), so the R7 mitigation ("quarterly fitness review is the trigger") is already lapsing on the keystone; S3 should reset it. (d) `frontmatter-only` (19 files) carried audit-depth information that `latest` erases; S3's full sweep covers it, fine.
Fix: add to S3: set `fitness_review_due` on touched files; keep AC list unchanged otherwise.

### F9 (minor) Baseline reproducibility and "model moved" handling under-specified
- FR-5.7 WARNs only; a regression run against a baseline from a different model still applies thresholds tuned to the old one. State that a moved model requires baseline re-capture, and make the WARN a FAIL under a flag (`--strict-model`) for release use.
- `model_resolved[0]` is "ordered by dispatch count", but the primary model can flip when the latest Opus delegates more readily (docs: "delegates to subagents more readily than prior models") and subagents run on a different alias (`model: sonnet`/`haiku` frontmatter above); AC-5.5 `r[0].startswith('claude-opus-')` then fails, or the 5-sample consistency check trips on subagent counts. Define primary = model of `system/init` (the main session), and record subagent models separately.
- AC-5.5 hard-codes `claude-opus-` (W4-5, real): fails for Bedrock `anthropic.claude-opus-*` and regional prefixes; use `'opus' in r[0]`.
- `model_pin_env` records only `ANTHROPIC_DEFAULT_OPUS_MODEL`; subagent-tier aliases (`SONNET`, `HAIKU`) and `ANTHROPIC_MODEL` are not recorded. Also `claude -p` without `--bare` loads the host's hooks/plugins/CLAUDE.md (headless page: "Without it, `claude -p` loads the same context an interactive session would"), so a baseline is host-specific; consider `--bare` for the smoke run or record the host state.

### F10 (minor) Missing/latent API-form trap and provenance comments
- W4-2 is real: `agentic-flow-builder/scripts/flow_orchestrator.py:663` `# In production: call Claude API with agent.config['model']` after FR-4.1 puts `opus` into `config.model`, which the API rejects (API IDs are pinned snapshots; see doc table). Name it in FR-4.5 with a required reword.
- Registry comment lines 148/173/189 read "canonical 2026-04-22 - opus-4-7 migration; prior: ..." and will describe a nonexistent value after FR-4.1 (`#` exempt so no guard trip, but a stale-lie). W4-5 second half is real.
- `constraints.yml` BC-04 wording "model-ID allowlist grep" is stale (S4-1, cosmetic).

### F11 (minor) Scope
Scope vs idea brief / backlog: brief calls out five literal sites; PRD's version-agnostic PIN_RE finds 14/6 (good, wider). Missing from scope: (1) F2 lines and `prompt-engineer/SKILL.md:349-375,371` (W4-1 real: line 371 tells authors to hardcode IDs with a canonical comment, contradicting convention 3/4); (2) `.claude-plugin/marketplace.json:23` "Uses Opus for advanced reasoning" is alias-level, fine; (3) `.json`/`.sh`/`.yml` outside guard scope (F6/W4-3 real). Scope creep: none material. PRD's Section 12 stop rule and section 8 doc scaffolding are heavy for a LIGHT stage but harmless.

## Round-4 QA warnings: which are real
| ID | Verdict | Note |
|---|---|---|
| W4-1 (prose line 371, 415-421 not named) | REAL, medium | Covered by F2/F11; add to FR-2.1 |
| W4-2 (flow_orchestrator:663 API comment) | REAL, low | F10 |
| W4-3 (guard scans py/md only; `#`/`>` heading loophole) | REAL, medium | F1, F3, F4; also `on:` `paths` filter |
| W4-4 (FR-5.5 behaviours lack AC) | REAL, high | F5; worse than QA states (unknown bucket) |
| W4-5 (AC-5.5 hardcodes `claude-opus-`; stale registry comments) | REAL, medium | F9, F10 |
| W4-6 (R9 provider claim over-broad) | REAL but cosmetic | I re-fetched: `opus` = Opus 5 on Anthropic API, Claude Platform on AWS, Bedrock and Google; only Foundry differs (Opus 4.6); `sonnet` differs everywhere off the Anthropic API |
| S4-1 (constraints wording) | Cosmetic, agree | |
| S4-2 (AC-2.1 body-delta phrasing) | Agree; see F6 item 1 | |

## Doc re-fetch table (WebFetch, 2026-09-20, independent of QA round 4)
| URL | PRD claim | Live page says | Verdict |
|---|---|---|---|
| https://code.claude.com/docs/en/model-config | `opus`/`sonnet` = latest of family; `haiku` not described as "latest"; aliases update over time, pin by full name or `ANTHROPIC_DEFAULT_OPUS_MODEL`; provider table differs | Table: `opus` "Uses the latest Opus model for complex reasoning tasks"; `sonnet` "Uses the latest Sonnet model for daily coding tasks"; `haiku` "Uses the fast and efficient Haiku model for simple tasks" (no "latest"). "Aliases point to the recommended version for your provider and update over time. To pin to a specific version, use the full model name, for example `claude-opus-5`, or set the corresponding environment variable like `ANTHROPIC_DEFAULT_OPUS_MODEL`." Provider table: Anthropic API Opus 5/Sonnet 5; Claude Platform on AWS Opus 5/Sonnet 4.6; Bedrock and Google Opus 5/Sonnet 4.5; Foundry Opus 4.6/Sonnet 4.5. Also lists `opusplan`, and `best` (resolves to the `fable` alias where available) | MATCH (PRD row quotes `Latest Opus model ...` while the live cell starts `Uses the latest Opus model ...`; substance identical. R9 wording slightly broad: see W4-6) |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | API has no evergreen "latest" ID for current models; dateless IDs are pinned snapshots; pre-4.6 aliases point to latest dated snapshot of the same minor version | "A common misconception is that dateless model IDs such as `claude-sonnet-4-6` behave as evergreen pointers that route to the latest or best-performing version. That is not the case." "When an updated version is available, it ships under a new model ID." "An alias such as `claude-sonnet-4-5` is a convenience pointer that resolves to the most recent dated snapshot for that minor version." Also: weights fixed per ID but "serving infrastructure around the model can change over time" | MATCH. Extra caveat the PRD omits: infrastructure changes can shift behaviour under a fixed ID, so even `ANTHROPIC_DEFAULT_OPUS_MODEL` pinning is not perfect reproducibility (F9) |
| https://code.claude.com/docs/en/headless | `system/init` reports the model; JSON output has `total_cost_usd` and per-model cost breakdown; field names unverified (OQ-10) | "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins." "With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown ... client-side estimates". No field name for model given. Also: without `--bare`, `claude -p` loads hooks/plugins/CLAUDE.md of the host | MATCH (OQ-10 status accurate; new host-context caveat in F9) |

CLI-alias vs API-ID separation in the PRD (conventions 3 and 4) is correct against both platform pages. No PRD doc claim was found wrong.

## Confidence
**CONFIDENCE: 3/5.** Decision implementation is coherent and its doc claims are accurate, and no script parses the stamps in a way the change breaks (F8). But the guard as specified is enforceable only on PRs it will never see (F1), its regexes miss real version mentions already sitting in the two keystone files (F2) and many pin shapes (F3), and the smoke-baseline model capture rests on an unvalidated stream shape with a silent `unknown` fallback (F5). Fold F1-F6 into the PRD (or Stage 3 inputs) before build.

# Gate 2 Evaluation, Round 4 (loop 1 of RESET loop): BACKLOG-108 Latest-Model References PRD (Revision 3)

Evaluator: QA Engineer (evaluator only; PRD not edited). Artifact: `.delivery/artifacts/02-refine/po/prd.md` (Revision 3), `constraints.yml`. Framing: ACs judged for well-formedness, specificity, testability, runnability, not for passing today. Design change (latest-version references instead of pinning) is a binding user decision and was not re-debated.

**Verdict: ACCEPT** (0 blocking defects, 6 warnings, 2 suggestions). D3-1 and D3-2 resolved. All discovery numbers reproduce exactly. Both cited-doc claims and the CLI-alias vs API-pinned-ID distinction are accurate against live pages.

## 1. Gate 2 per-criterion results

| # | Criterion | Sev | Result | Note |
|---|-----------|-----|--------|------|
| 1 | Every FR has AC with testable condition | blocking | PASS | S1..S7 all FRs mapped; process-only FRs (1.4, 2.4, 4.4, 5.8, 7.3) tagged "Verification: inspection" with named evidence. New FR-2.2, FR-4.1, FR-5.5, FR-5.8 have ACs. See W4-4 for two behaviours inside FR-5.5 without their own check |
| 2 | NFRs quantified | blocking | PASS | NFR-1..12 numeric with commands; NFR-10/11/12 new and measurable (NFR-11 by inspection, by-construction) |
| 3 | Out-of-scope present | blocking | PASS | Section 10 |
| 4 | Success metrics numeric + method | blocking | PASS | G1, G-LIT, G2..G10, each closed by exactly one story (table in section 5 checked: S1, S4, S3, S3, S4, S5, S3, S2, S7, S6, S7). Ownership rule stated |
| 5 | No blocking open questions | blocking | PASS | OQ-1..10 all have owner, due, non-blocking rationale; OQ-7 resolved; OQ-6/8/10 UNVERIFIED items are gated by explicit runner setting or loud capture failure |
| 6 | Personas specific | warning | PASS | 3 personas with goal, pain, context |
| 7 | Dependencies w/ status | warning | PASS | Section 7 |
| 8 | Risks L/I/mitigation | warning | PASS | R1..R10 contiguous, each has L, I, mitigation; R7..R10 well-formed and tied to FR-5.5/5.7, convention 4, quarterly fitness review |
| 9 | Assumptions explicit | suggestion | PASS | 5 assumptions |
| 10 | Discovery numbers accurate | blocking | PASS | Section 3 |

## 2. D3-1 / D3-2 resolution

| Defect | Status | Evidence |
|--------|--------|----------|
| D3-1 (`claude-sonnet-4-5` at `smoke-test-architecture.md:116` unreachable) | RESOLVED | FR-4.3 now covers lines 115 AND 116 plus `telemetry-schema.md:36`; AC-4.3 greps both files with version-agnostic `claude-(opus\|sonnet\|haiku)-[0-9]` and requires 0. Canonical count lists `smoke-test-architecture.md [115, 116]`. Structural fix: version-agnostic PIN_RE catches any versioned ID, so no per-ID hiding place remains. Also caught 2 more hidden pins the round-3 count could not see (`agent_registry.py:149,174`, `telemetry-schema.md:36`), all assigned to stories |
| D3-2 (exact pre-migration value for AC-1.2c) | RESOLVED | AC-1.2c states `70` today with a decomposition (34 + 26 + 10); executed: prints `70`. AC-1b states `14 files 6` today; executed: matches |

## 3. Command-execution results (worktree root, 2026-09-20)

| Command / claim | PRD says | Actual | Match |
|---|---|---|---|
| Canonical pinned-id count | `pinned-id hits 14 files 6`, list of 6 files with lines | identical output, all 6 file:line lists identical (guard [30,31,39]; registry [149,174,190]; smoke-arch [115,116]; telemetry [36]; conftest [105,117,129,151]; prompt-engineer [368]) | YES |
| SKILL.md count / stamp census | `skill 34`; `26 25 {frontmatter-only: 19, opus-4-7: 7}` | identical | YES |
| `pattern_library_version` | 26 x `4-7-1` | `26 {'pattern_library_version: 4-7-1': 26}` | YES |
| PROSE_RE prose lines excluding stamps | 8 lines, 2 files (delivery-flow 27,273; prompt-engineer 88,347,356,368,397,408) | identical (8, 2 files, same lines) | YES |
| AC-1.2c hardcoded-pattern equivalent | 70 | 70 | YES |
| AC-1.1 today | 6 | 6 | YES |
| AC-1.2a fixture logic (suggested patterns, Python `re`) | OK | all 8 must-hit and 6 must-pass fixtures behave as asserted (verified in the AC-1.2c logic run; PIN/STAMP/PROSE patterns are the same strings) | YES |
| AC-1.3 | 0 and 0 | 0 and 0 | YES |
| AC-4.5 | 0 | 0 | YES |
| AC-6.1 cache hash | MATCH | MATCH | YES |
| AC-6 `check_skill_budgets.py` | exit 0, 17 files | `BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).` exit=0 | YES |
| `validate_constraints.py` (delivery-team/skills/delivery-flow/scripts/) on constraints.yml | valid, rc 0 | `ok: ... is valid against constraints schema` rc=0 | YES |
| `claude --help` alias text; `--effort` flag exists | quoted in section 8 | `--effort <level>` and `--model <model>` present in local CLI help | YES |
| Runner today builds `claude --print --output-format stream-json --verbose`, no `--model`, `run_smoke.py` no `--effort` | as stated | `runner.py` `_build_claude_command` matches; grep `effort` in `run_smoke.py` empty | YES |
| Baseline keys today | `_header_comment ... deferred_reason`, no `model` | identical list | YES |
| Renamed files; old names absent | exist / absent | new backlog and memory files present; `opus-5-migration.md` and `opus-4-8` named files absent under `.delivery/backlog` and `.delivery/memory/topics` | YES |
| Repo-wide leftover version prose outside `.delivery`, CHANGELOG, SKILL.md | (implied by "8 lines in 2 files") | grep of py/md/yml/json: 0 model-version mentions outside `.delivery/` | YES |
| Guard PIN/STAMP false-positive scan on non-SKILL py/md (STAMP_RE only) | 0 (implicit) | 0 lines | YES |
| `last_audited` on stamped files | (FR-3.3 sets it) | present on all 25 (prompt-engineer has 2, lines 7 and 416) | consistent |

Heredoc-in-worktree caveat: the session shell filter refused compound heredoc commands; every AC python snippet was run via a script file containing the PRD's exact logic (walk.py plus inline patterns).

## 4. Doc re-fetch results (WebFetch, 3 URLs, 2026-09-20)

| URL | PRD claim | Finding |
|---|---|---|
| https://code.claude.com/docs/en/model-config | `opus` = latest Opus, `sonnet` = latest Sonnet; `haiku` row does NOT say "latest"; aliases update over time; pin by full name or `ANTHROPIC_DEFAULT_OPUS_MODEL`; provider table Anthropic API Opus 5 / Sonnet 5, Foundry Opus 4.6 / Sonnet 4.5 | CONFIRMED. Fetched table reads "Uses the latest Opus model...", "Uses the latest Sonnet model...", "Uses the fast and efficient Haiku model for simple tasks" (fetch tool paraphrases lead-in words; the "latest" for opus/sonnet and its absence for haiku match the PRD, OQ-6 stands). Alias-versioning quote matches nearly verbatim ("Aliases point to the recommended version for your provider and update over time. To pin to a specific version, use the full model name ... or set the corresponding environment variable like `ANTHROPIC_DEFAULT_OPUS_MODEL`"). Provider table: also lists Claude Platform on AWS (Opus 5 / Sonnet 4.6) and Bedrock/Google (Opus 5 / Sonnet 4.5). Imprecision in R9: "`opus`/`sonnet` differ on Bedrock, Foundry, AWS platform" is true for `sonnet` everywhere off the Anthropic API but for `opus` only on Foundry (see W4-6) |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | API has NO evergreen alias for current models; dateless IDs are pinned snapshots; pre-4.6 alias `claude-sonnet-4-5` resolves to latest dated snapshot of that minor version only | CONFIRMED verbatim: "A common misconception is that dateless model IDs such as `claude-sonnet-4-6` behave as evergreen pointers ... That is not the case."; "When an updated version is available, it ships under a new model ID."; "An alias such as `claude-sonnet-4-5` is a convenience pointer that resolves to the most recent dated snapshot for that minor version." The doc also notes the pinned-ID guarantee "covers model IDs, not the convenience aliases that the Claude API accepts for some earlier models", which the PRD row for pre-4.6 aliases reflects |
| https://code.claude.com/docs/en/headless | `system/init` reports the model; JSON output has `total_cost_usd` and per-model cost breakdown; exact field names unverified (OQ-10) | CONFIRMED verbatim: "The `system/init` event reports session metadata including the model, tools, MCP servers, and loaded plugins."; "the response payload includes `total_cost_usd` and a per-model cost breakdown". The page gives no field name for the model, so OQ-10 UNVERIFIED status is correct |

CLI-alias vs API-pinned-ID consistency: consistent. The PRD never claims the API has "latest"; convention 3 (CLI aliases, one dict) and convention 4 (API: one config value) map exactly onto the two doc pages. Model-config's own pin example (`claude-opus-5`) also shows the docs treat full IDs as the pin form, which supports treating concrete IDs as observation-only data (baseline JSON) rather than repo prose.

## 5. Consistency findings (whole-PRD)

- Pinned-version leftovers in PRD body: only intentional ones (rename provenance in header, citation rows dated 2026-09-20, the D3-1 quote, the `4-7` census facts, Revision 1 and 2 changelog). No live requirement cites `claude-opus-5` as a target. "Opus 5" appears only as "effective current model" context and citation.
- FR/OQ/R number integrity: every cross-reference resolves (FR-4.5 from AC-4.5 and R10; FR-5.5/5.7 from R8; OQ-5 from R6/FR-5.3; OQ-6 from Assumption 1; OQ-10 from Dependencies; FR-4.4 from section 6). R7-old removed and R7..R10 replace it; changelog says so. OQ-7 kept as RESOLVED with FR-5.8 pointer. No dangling numbers.
- Changelog matches body: question table (1-5) matches convention/FR text; "Effect on each earlier item" rows match actual FR-1.x..FR-6.x text; "commands run" list matches the outputs in section 3 above. D3-1 and D3-2 entries accurate.
- Gates: each of G1, G-LIT, G2..G10 closed by exactly one story; preconditions are listed separately. AC lists per gate resolve to existing ACs.
- Guard contract self-consistency: AC-1.1 (0 for `claude-` immediately followed by family, e.g. `claude-(opus|...)`), PIN_RE self-match check: the guard's own `PIN_RE='claude-(opus|...)...'` line does not match PIN_RE (character after `claude-` is `(`), so the guard cannot flag itself. Verified by reasoning against the regex; AC-1.1 asserts it.
- Synthetic IDs: `claude-opus-fixture` has no digit after the family, so PIN_RE (`[0-9]` required after `family-`) does not fire; AC-1.2a asserts this. PIN_RE's tail `[-.0-9a-z]*` is greedy but only matters after a first digit.
- Changelog (Rule A) and `>`/`#` doc-citation lines: exempt by contract; `.delivery/**` excluded by pathspec; historical `.delivery` artifacts full of `4.7` do not trip anything (0 non-`.delivery` leftovers found).
- No regression vs rounds 1-3: D-1..D-13 and D2-1..D2-4 fixes intact (dispatch manifest FR-7.4, body-delta AC-3.1, hedge scan AC-2.3 scoped, portable patterns, `git diff main` assumption). D2-1 (provenance comments on own line) is retained via FR-4.1 and the `#` exemption; verified registry lines 148, 173, 189 are `#` lines and the `config` lines are separate, so AC-4.1's `"model": MODEL_TIER_ALIAS[` regex (3 occurrences) matches the current `"config": {"model": ...}` shape.
- `constraints.yml`: valid; invariants and `model_refs` block match PRD (patterns, aliases, central definition, allowlisted locations, effort/model runner). Backlog file and memory file are consistent with PRD (Section 0 of the memory file supersedes historical sections 1-6 and says so; historical sections still contain `claude-opus-5`/`4-8` literals, acceptable because `.delivery/**` is allowlisted).

## 6. New defects and required fixes

No blocking defects. Warnings (PO should fold into the S-stage inputs or the next PRD touch; none blocks Stage 3):

**W4-1 (warning) Live prose contradicts the new scheme and is not named by FR-2.1.** `prompt-engineer/SKILL.md:371` says "Never hardcode a bare model ID without the comment ... `# canonical <YYYY-MM-DD>`". It does not match PROSE_RE, so no AC catches it, but it tells readers to hardcode IDs, contrary to conventions 3 and 4. Lines 415-421 (documentation example of the stamp block, including `last_audited: 2026-04-22` at 416) share the block. Fix: add line 371 (and the 415-421 stamp-doc block) to FR-2.1's enumerated rewrite sites; AC-2.2 can add `grep -c "canonical <YYYY" prompt-engineer/SKILL.md` MUST print 0.

**W4-2 (warning) Latent API trap not named.** `agentic-flow-builder/scripts/flow_orchestrator.py:663` reads `# In production: call Claude API with agent.config['model']`. After FR-4.1, `config.model` is `opus`, which the API does not accept (section 8). R10 covers the assumption in general, but this concrete comment invites exactly that wiring. Fix: name it in FR-4.5 or R10 and require the S4 developer to reword the comment (convention 4: read one config value) or note it in the S4 report. Suggested check: `grep -n "agent.config\['model'\]" agentic-flow-builder/scripts/flow_orchestrator.py` MUST print a reworded line.

**W4-3 (warning) Guard scan scope narrower than the canonical count and NFR-10.** The canonical count and NFR-10 scan `*.py *.md *.yml *.yaml *.txt` (and the guard yml itself), but the guard's Rule A scans only `*.py` and `*.md` (AC-1.2c excludes yml; FR-1.2). A pin re-introduced in a `.yml`/`.yaml`/`.txt` file, including the guard yml or another workflow, passes CI while failing NFR-10. Also, Rule A's `#`/`>` exemption in `.md` exempts Markdown headings (`# ...`) and shell-comment lines inside code fences. Fix: either state the scope difference explicitly in FR-1.2 ("CI guard scans py and md; yml/yaml/txt are covered only by the local canonical count") or extend the guard's `git ls-files` list to the same extensions; and note the heading loophole as accepted.

**W4-4 (warning) FR-5.5 behaviours without their own AC.** "Capture FAILS if no model string is observed" and "all 5 samples must resolve to the same primary model, else `--init-baseline` fails with the offending pair" are testable meta-test cases (like AC-5.2/5.7) but only AC-5.5 (final JSON shape) is attached. Fix: add AC-5.5b, a meta-test by the validator dispatch feeding (i) a stream with no `model` field and (ii) two samples with different primary models, asserting non-zero exit and the offending pair in the message; `pytest delivery-team/tests/smoke/tests/test_meta.py -q` exits 0.

**W4-5 (warning) AC-5.5 hard-codes the API-form ID and conflicts with R9.** `r[0].startswith('claude-opus-')` fails if the user's provider reports a prefixed ID (Bedrock `anthropic.claude-opus-...` or regional prefix), while R9 says the harness "runs against the user's own provider and records the resolved ID". Fix: change the check to `'opus' in r[0]` (or `re.search(r'claude-opus', r[0])`), keeping "MUST print: opus True xhigh 5 active True True". Also the stale comment lines above the three registry entries (`# canonical 2026-04-22 — opus-4-7 migration; prior: ...`) will describe a value that no longer exists after FR-4.1; cheap fix: FR-4.1 allows rewording the "canonical" clause while keeping the `prior:` provenance.

**W4-6 (warning) R9 / section 8 provider claim slightly over-broad.** Live page: `opus` = Opus 5 on Anthropic API, Claude Platform on AWS, Bedrock and Google; only Foundry differs (Opus 4.6). `sonnet` differs on every non-Anthropic provider. R9 text "`opus`/`sonnet` differ on Bedrock, Foundry, AWS platform" should read "`sonnet` differs on Bedrock, Google, AWS platform and Foundry; `opus` differs on Foundry".

Suggestions:
- **S4-1** `constraints.yml` BC-04 still says "CI permitted for static guards only (YAML lint, model-ID allowlist grep, budget checks)": "allowlist" is stale wording under the pin-forbidding guard; and BC-02 `secondary_urls` lists `.../models/migration-guide` while the PRD cites `.../models/opus-5/migration-guide`. Cosmetic; align on the next touch.
- **S4-2** AC-2.1 says the body-delta check "under AC-3.1" excludes stamp lines but S2 never edits stamps (S3 does); harmless, carried from earlier rounds; could say "body-delta over prose lines only".

## 7. Implementability assessment (item e)

- Guard false positives: `claude-opus-fixture` (no digit after family) does not hit PIN_RE; the doc-citation and changelog cases are exempt (`CHANGELOG.md`, `.delivery/**`, `#`/`>` lines). Rule B (PROSE_RE, no exemption) touches only SKILL.md; today's 8 prose lines are all Opus 4.7 guidance blocks that S2 rewrites, and none of the 34 SKILL.md lines matched by PROSE_RE is a non-version usage (all 34 matches are 26 stamp lines, 8 real version mentions). Non-SKILL py/md outside `.delivery` contain zero PROSE/STAMP-like lines, so the guard reaches 0 on the migrated tree without allowlisting anything (AC-1.2c decomposition 34 + 26 + 10 = 70 verified).
- Portability: all three patterns run under Python `re` (executed) and use only `grep -E` features (bracket lists with leading/trailing `-`, alternation, `*`, `+`, no `\b`, no lookaheads, no POSIX classes).
- Runnable: every AC snippet executes under python3 stdlib; those with a today-value reproduce it.
- CLI vs API claim: consistent with the three fetched pages (section 4).

## 8. Summary

Round-3 defects D3-1 and D3-2 are resolved, structurally rather than by one-off patching. The redesign is internally consistent (no dangling FR/OQ/R numbers, changelog matches body, gates each closed by one story), every discovery command reproduces exactly (14/6, 26/25 census, 26 stamps, 70, 0, MATCH, exit 0, constraints valid), and the doc-cited claims are accurate. Six non-blocking warnings (W4-1..W4-6) identify scope gaps and two AC hardening items; recommend the PO fold W4-1, W4-2, W4-4 and W4-5 into the Stage 3-5 inputs.

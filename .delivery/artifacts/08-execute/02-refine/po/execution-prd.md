# Execution PRD — Opus 4.7 Plugin-Skill Migration

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 2 Refine, LIGHT mode)
**Author:** Product Owner — Gandalf speaking
**Upstream binding plan:** `.delivery/artifacts/04-architect/solution/transformation-plan.md` rev 1 (§6 Roadmap)
**Upstream PRD:** `.delivery/artifacts/02-refine/po/prd.md` (8 REQs, 29 findings)
**Binding ADRs:** `.delivery/artifacts/04-architect/adrs/ADR-00{1..6}-4-7-*.md`
**Upstream retrospective (carry-items A1–A6):** `.delivery/artifacts/retrospective.md`
**Status:** Draft for Refine-light DoD

---

> *"A plan is only as good as the stories it lights. These fourteen work items are the ring-makers of this engagement — each small, each weighed, each bound to the roadmap that was forged before them. I have not re-smelted the ore. I have cut it into rings you can carry."*
> — Gandalf

---

## 1. Purpose

This execution-PRD carries the approved transformation plan (§6, 14 WIs across 4 waves) forward as fourteen dogfood-runnable stories for the implementation team. Scope is not re-opened — every requirement, AC, ADR, metric, and deferral from the DESIGN engagement remains binding. The only authored deviation is WI-13's dual-write (local backlog file **and** GitHub issue labeled `backlog-47`) per user direction. Every story below carries the roadmap's existing REQ/AC/ADR/metric anchors and adds one concrete Developer-DoD dogfood command, so that the "reading looked right, running did not" regression mode caught three defects in DESIGN Stage 2 cannot repeat here.

---

## 2. Stories (14 — one per WI)

### Story WI-01 — AS-IS validator-dispatch count capture

- **Wave**: 1
- **T-shirt**: XS
- **Depends on**: —
- **Parallelisable with**: WI-02
- **PRD anchors**: REQ-09, AC-09.1; transformation-plan §6.2 WI-01
- **As a**: pipeline observability engineer
- **I want**: the actual sub-agent dispatch counts on Opus 4.7 for the Idea and Refine stages captured against the expected counts from `.delivery/config.yml` `dod_validators.<stage>`
- **So that**: we firm PRD Assumption A-05 at the count level before any prose edit builds on it, and if F-08 (fewer sub-agents by default) has already fused dispatches silently, we detect it as a blocker before Wave 2

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1: Output table at `.delivery/artifacts/<impl-run>/observability/4-7-as-is-dispatch-counts.md` with columns `stage | expected_count | actual_count | delta`.
- AC-2: Rows cover idea (expect 2), refine (expect 4), design (expect 5), architect (expect 5), plan (expect 5), development (expect 4), uat (expect 4).
- AC-3: If all deltas are zero, record "Assumption A-05 firmed at count level."
- AC-4: If any delta >0, raise R-09 (silent F-08 fusion already occurring) and sequence a mitigation WI before WI-04 lands.

**Dogfood / test command** (Developer DoD runs this):
`test -f .delivery/artifacts/run-2026-04-22-4x7e/observability/4-7-as-is-dispatch-counts.md && grep -cE '^\| *(idea|refine|design|architect|plan|development|uat) *\|' .delivery/artifacts/run-2026-04-22-4x7e/observability/4-7-as-is-dispatch-counts.md | grep -qE '^[7-9]$|^[1-9][0-9]+$'`

**Out of Scope**: Post-hoc re-running of Idea/Refine from DESIGN run; telemetry schema changes in `verify_skill_load.py`; any dispatch-count capture for stages this engagement does not itself exercise beyond the expectations table.

---

### Story WI-02 — 4.7 baseline capture (JSON)

- **Wave**: 1
- **T-shirt**: S
- **Depends on**: —
- **Parallelisable with**: WI-01
- **PRD anchors**: REQ-10, AC-10.1/2/3; Samwise advisories #3 + #5; transformation-plan §6.2 WI-02
- **As a**: regression-metric owner for this migration
- **I want**: a machine-readable JSON baseline capturing SKILL_LOADED hit rate, dispatch counts, one Challenger sample, one adversarial-review sample, three alias-theme renderings, and `audit_agent_prompt.py` warning count
- **So that**: every delta metric (M-03, M-04, M-05, M-07) and every Wave 2–4 regression check has a single, `jq`-queryable reference point rather than a falsely-low baseline captured in a degraded run

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1: JSON artifact at `.delivery/artifacts/<impl-run>/observability/4-7-baseline.json`.
- AC-2: Contains keyed fields `skill_loaded_first_attempt_rate` (0.0..1.0), `dispatch_counts_per_stage` (object keyed by stage name), `challenger_sample_path` (string), `adversarial_review_sample_path` (string), `alias_announcement_samples` (array of `{ theme, rendered_text }`), `audit_hook_warning_count` (integer).
- AC-3: `jq -e '.skill_loaded_first_attempt_rate and .dispatch_counts_per_stage and .challenger_sample_path and .adversarial_review_sample_path and .alias_announcement_samples and .audit_hook_warning_count'` returns 0.
- AC-4: Baseline capture aborts (does not write) if WI-01 surfaced R-09 fusion.
- AC-5: A markdown companion may wrap the JSON for human readability; the JSON payload is the authoritative artifact.

**Dogfood / test command**:
`jq -e '.skill_loaded_first_attempt_rate and .dispatch_counts_per_stage and .challenger_sample_path and .adversarial_review_sample_path and .alias_announcement_samples and (.audit_hook_warning_count | type == "number")' .delivery/artifacts/run-2026-04-22-4x7e/observability/4-7-baseline.json`

**Out of Scope**: Any non-JSON format for the baseline; historical 4.6 baseline reconstruction (PRD states "against a baseline that did not exist"); multi-run aggregation.

---

### Story WI-03 — NDOC-02 frontmatter-contract spike (Wave-2 hard blocker)

- **Wave**: 1
- **T-shirt**: XS
- **Depends on**: —
- **Parallelisable with**: WI-01, WI-02
- **PRD anchors**: NDOC-02, ADR-006 rollback trigger, challenger loop2 Finding #8, fresh-challenger F-C-01, Legolas NIT-01; transformation-plan §6.2 WI-03
- **As a**: Wave-2 dispatcher
- **I want**: a verdict string recorded against the two candidate Anthropic reference pages on whether SKILL.md frontmatter accepts unknown fields or strictly validates them
- **So that**: ADR-006's mechanical rollback trigger can fire before any frontmatter edit lands — a `strict` verdict flips WI-04/WI-05/WI-06/WI-11 to Option B (HTML-comment placement) with identical semantics

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1: Two URLs fetched and recorded: (a) `https://docs.claude.com/en/docs/claude-code/plugins-reference`, (b) `https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview`. Fetch date recorded.
- AC-2: Verbatim quote from whichever page speaks to unknown-field behaviour. If neither, record "no authoritative clause; default to historical behaviour (accepts unknown fields)."
- AC-3: Verdict string exactly one of `unknown-fields-accepted` or `strict`, matching regex `(unknown-fields-accepted|strict)`.
- AC-4: Branch action — `unknown-fields-accepted` ⇒ Option A ships as-written. `strict` ⇒ ADR-006 mechanical rollback fires: all downstream frontmatter edits (WI-04, WI-05, WI-06, WI-11) emit `<!-- model_awareness: opus-4-7 -->` / `<!-- last_audited: ... -->` / `<!-- pattern_library_version: ... -->` HTML comments placed immediately below the closing `---` of the existing frontmatter block.
- AC-5: Wave 2 MUST NOT dispatch WI-04, WI-05, or WI-06 until the spike file exists and contains a verdict string. This gate is mechanical, not discretionary.

**Dogfood / test command**:
`grep -qE '^(verdict|Verdict): *(unknown-fields-accepted|strict) *$' .delivery/artifacts/run-2026-04-22-4x7e/research/ndoc-02-spike.md`

**Out of Scope**: Any other Anthropic-docs research questions; editing ADR-006 mid-flight; re-opening the Option A vs Option B decision beyond the mechanical verdict-driven branch.

---

### Story WI-04 — `delivery-flow/SKILL.md` 4.7 dispatch annotation

- **Wave**: 2
- **T-shirt**: S
- **Depends on**: WI-01, WI-02, WI-03
- **Parallelisable with**: WI-05
- **PRD anchors**: REQ-03, AC-03.1/2/3/4; DISP-01/02; F-08, F-25; ADR-006; transformation-plan §6.2 WI-04
- **As a**: delivery-flow skill author
- **I want**: additive annotations at lines 14–62 (DISP-02) and 328–345 (DISP-01) explaining why F-08 promotes "one role = one sub-agent" from stylistic to behavioural on 4.7, plus the three-field frontmatter per ADR-006
- **So that**: the dispatch contract is load-bearingly documented for 4.7 and silent sub-agent fusion has a named defence in the prose

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-03.1): Annotation is additive at lines 14–62 and 328–345; existing prose not deleted or restructured.
- AC-2 (AC-03.2): No change to the 6 collaboration patterns, 7-stage shape, DoD semantics, or config schema v2.7.
- AC-3 (AC-03.3): Post-implementation dogfood run asserts actual dispatch count per stage == `dod_validators.<stage>` list length AND SKILL_LOADED hit rate ≥ max(0.95, baseline_rate − 0.02).
- AC-4 (AC-03.4): Dogfood covers at least one FEATURE-type run and one DESIGN-type run.
- AC-5: ADR-006 frontmatter applied: `model_awareness: opus-4-7`, `last_audited: <edit date>`, `pattern_library_version: 4-7-1`.

**Dogfood / test command**:
`grep -q '^model_awareness: opus-4-7$' delivery-team/skills/delivery-flow/SKILL.md && grep -q '^pattern_library_version: 4-7-1$' delivery-team/skills/delivery-flow/SKILL.md && grep -qE 'F-?08' delivery-team/skills/delivery-flow/SKILL.md`

**Out of Scope**: Rewrites of the 6 collaboration patterns; edits to config schema v2.7; changes to the 7-stage pipeline shape; edits to `hooks.json` or hook scripts.

---

### Story WI-05 — `prompt-engineer/SKILL.md` pattern-library expansion + PAT-01 reframe

- **Wave**: 2
- **T-shirt**: M
- **Depends on**: WI-01, WI-02, WI-03
- **Parallelisable with**: WI-04
- **PRD anchors**: REQ-02, AC-02.1/2; PAT-01/02/06; ADR-003, ADR-005; Galadriel Patterns 4.1–4.6; ADR-006; transformation-plan §6.2 WI-05
- **As a**: prompt-engineer skill author
- **I want**: PAT-01 line 85 reframed for F-13/F-29, a new Model-specific-optimisation sub-section added, and the six Galadriel patterns (4.1–4.6) installed as named sub-sections with stable anchors, plus the ADR-006 frontmatter
- **So that**: the canonical 4.7-era pattern library has one home, downstream skills cite patterns by name instead of restating them, and DX-M3 (external restatement count) drops to 0

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-02.2): PAT-01 line 85 reframed per F-13 + F-29 (manual CoT scaffolds distinguished from 4.7's adaptive-thinking reasoning-visibility model).
- AC-2: New `## Model-specific optimisation — Claude Opus 4.7` sub-section mentions adaptive-thinking-only (F-11), temp/top_p/top_k→400, effort levers low/medium/high/xhigh/max (F-15).
- AC-3 (ADR-005): Six Galadriel patterns (4.1 Versioned Model Reference; 4.2 4.7-Aware Role Prompt Skeleton; 4.3 Manual CoT Fallback; 4.4 Calibrated Instruction Voicing; 4.5 Model-Specific Optimisation Sub-section; 4.6 SKILL.md Forward-Compatibility Header) added as named sub-sections with stable markdown anchors.
- AC-4: ADR-006 frontmatter applied.
- AC-5: `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns 6.
- AC-6: `grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/` returns only lines citing `prompt-engineer/SKILL.md` (DX-M3 target 0 external restatements).
- AC-7 (scope broadening — closes G-5 §7.4 coverage gap): Retarget the `<thinking>` reference in `research-agent/references/prompt-library.md` line 10 to cite `prompt-engineer/SKILL.md` by name, OR prune it if no longer load-bearing. This closes the one remaining §7.4 grep hit so the DX-M3 end-state verification command returns 0 on the green-merge run. WI-05 edit scope for this AC is the single line in `research-agent/references/prompt-library.md`; no other references-file edits are in scope.

**Dogfood / test command**:
`test "$(grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md)" = "6" && grep -q '^model_awareness: opus-4-7$' prompt-engineer/SKILL.md`

**Out of Scope**: Rewriting PAT-02, PAT-03, PAT-06 manual-CoT patterns; removing historical patterns; editing `prompt-engineer/references/`; any work on `plugin-dev:*` pattern libraries. (Exception per AC-7: the single-line retarget-or-prune in `research-agent/references/prompt-library.md:10` IS in scope, and only that line.)

---

### Story WI-06 — `research-agent/SKILL.md` tool-use dogfood probe

- **Wave**: 2
- **T-shirt**: S (pass) / M (regression)
- **Depends on**: WI-01, WI-02
- **Parallelisable with**: WI-04, WI-05
- **PRD anchors**: REQ-03B, AC-03B.1/2/3; F-07, SZ-09; fresh-challenger F-C-02; challenger loop2 Finding #4 hardening; ADR-006; transformation-plan §6.2 WI-06
- **As a**: research-agent skill owner
- **I want**: one non-trivial research invocation run on 4.7, with a hardened mechanical gate on tool-call count, distinct hostname count, and URL-per-claim; edit the SKILL.md only if the gate fails
- **So that**: F-07 (fewer tool calls by default) cannot silently regress research-agent into reasoning-instead-of-fetching, and the dogfood-before-edit primitive holds

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-03B.1): One non-trivial research invocation (query from research-agent's own reference examples; one 4.6 demonstrably used ≥2 fetches for). Transcript saved to `.delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt`.
- AC-2 (AC-03B.2, hardened — mechanical gate, all three must hold):
    1. `grep -cE '^(WebFetch|WebSearch)\(' .delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt` ≥ 2.
    2. `grep -oE 'https?://[^/ )"]+' .delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt | sort -u | wc -l` ≥ 2.
    3. Manual URL-per-claim read: every factual claim in the research output carries at least one URL from the fetched set.
- AC-3: One-line JSON summary `{ "tool_calls": N, "distinct_hostnames": M, "pass": true|false }` written to `.delivery/artifacts/<impl-run>/observability/research-probe-result.json`.
- AC-4 (AC-03B.3): Pass ⇒ no edit; fail ⇒ schedule targeted prose edit ("WebFetch every primary source; never infer a fact without a URL" — F-28 calibrated voicing) before any other research-agent change.
- AC-5: ADR-006 frontmatter applied regardless of pass/fail.

**Dogfood / test command**:
`jq -e '.pass == true and (.tool_calls | type == "number") and (.distinct_hostnames | type == "number") and .tool_calls >= 2 and .distinct_hostnames >= 2' .delivery/artifacts/run-2026-04-22-4x7e/observability/research-probe-result.json`

**Out of Scope**: Research-agent reference-file edits; adding a new research-type; schema changes to tool-call transcript format; any probe against skills other than `research-agent/SKILL.md`.

---

### Story WI-07 — `product-delivery/SKILL.md` F-25 audit

- **Wave**: 3
- **T-shirt**: S
- **Depends on**: WI-05
- **Parallelisable with**: WI-08
- **PRD anchors**: REQ-02, AC-02.3; F-25; SZ-15; ADR-006; challenger loop2 Finding #2 (keystone AC unevenness); transformation-plan §6.2 WI-07
- **As a**: product-delivery skill owner
- **I want**: a prose-read audit of `product-delivery/SKILL.md` for under-specified role-behaviour rules (e.g., "PO auto-logs issues from research" class) that F-25's literal instruction-following would execute differently on 4.7, producing either per-rule concrete rewording recommendations or explicit Done-with-reason
- **So that**: the memory-documented role behaviours keep their intended semantics on 4.7 rather than drifting under literal execution

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-02.3): Audit output at `.delivery/artifacts/<impl-run>/audits/product-delivery-f25.md` lists each examined rule/section with **(a) a concrete recommendation for rewording OR (b) explicit Done-with-reason** (per-file concreteness satisfies the carry-item "keystone AC unevenness" binding).
- AC-2: Citations to Pattern 4.2 (4.7-Aware Role Prompt Skeleton) by name where the dispatch shape applies.
- AC-3: Any reworded rule carries a citation back to F-25.
- AC-4: ADR-006 frontmatter applied to `product-delivery/SKILL.md`.
- AC-5: Impl-run rewordings gated on user-feedback persona review per PRD AC-02.4.

**Dogfood / test command**:
`test -f .delivery/artifacts/run-2026-04-22-4x7e/audits/product-delivery-f25.md && grep -qE '(Recommendation|Done[- ]with[- ]reason)' .delivery/artifacts/run-2026-04-22-4x7e/audits/product-delivery-f25.md && grep -q '^model_awareness: opus-4-7$' delivery-team/skills/product-delivery/SKILL.md`

**Out of Scope**: Editing references under `product-delivery/references/`; cross-plugin role redefinitions; `plugin-dev:*` skill audits.

---

### Story WI-08 — `architect/SKILL.md` F-25/F-26 audit

- **Wave**: 3
- **T-shirt**: S
- **Depends on**: WI-05
- **Parallelisable with**: WI-07
- **PRD anchors**: REQ-02, AC-02.1; F-25, F-26; SZ-14; ADR-006; challenger loop2 Finding #2 widened (keystone AC unevenness); transformation-plan §6.2 WI-08
- **As a**: architect skill owner
- **I want**: a prose-read audit of the 667-LOC architect/SKILL.md for (a) under-specified instructions F-25 would execute literally and (b) scaffolding that duplicates 4.7 default (F-26 — e.g., "after every 3 steps, summarise"), producing per-sub-role concrete recommendations or explicit Done-with-reason
- **So that**: the largest technical-instruction surface in the repo does not silently shift behaviour on 4.7 and scaffolding that is now redundant is named, not left to lurk

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-02.1, widened): Per-file finding list at `.delivery/artifacts/<impl-run>/audits/architect-f25-f26.md` with **≥1 concrete recommendation OR explicit Done-with-reason per sub-role examined** (each of the 11 roles named; satisfies carry-item "keystone AC unevenness" binding).
- AC-2: Audit names F-25 (literal-following) and F-26 (scaffolding redundancy) instances explicitly — scaffolding instances named, not summarised.
- AC-3: Citations to Patterns 4.2 (Role-Prompt Skeleton) and 4.4 (Calibrated Instruction Voicing) by name where applicable.
- AC-4: ADR-006 frontmatter applied to `architect/SKILL.md`.

**Dogfood / test command**:
`test -f .delivery/artifacts/run-2026-04-22-4x7e/audits/architect-f25-f26.md && test "$(grep -cE '^### ' .delivery/artifacts/run-2026-04-22-4x7e/audits/architect-f25-f26.md)" -ge "11" && grep -q '^model_awareness: opus-4-7$' delivery-team/skills/architect/SKILL.md`

**Out of Scope**: Rewriting the 11 sub-roles; editing paradigm sub-skills (`skills/paradigms/volatility/`, `skills/paradigms/ddd/`) beyond the frontmatter backfill owned by WI-11; changes to paradigm-router dispatch logic.

---

### Story WI-09 — `mtg-commander/SKILL.md` adversarial-tone audit + REQ-04 dogfood

- **Wave**: 3
- **T-shirt**: S (pass) / M (regression)
- **Depends on**: WI-02
- **Parallelisable with**: WI-05, WI-07, WI-08
- **PRD anchors**: REQ-04, AC-04.1/2/3/4; F-24, F-27, NDOC-03; SZ-17; challenger loop2 Finding #2 + Finding #6 softener; ADR-006; transformation-plan §6.2 WI-09
- **As a**: mtg-commander skill owner
- **I want**: one Challenger invocation on 4.7 scored against the AC-04.2 concrete checklist, with a soften-hatch for small-input Challengers; edit the SKILL.md only if the baseline diff or checklist fails
- **So that**: F-24/F-27 tone flattening on the largest SKILL.md (1181 LOC, user-visible Challengers) is caught by dogfood, not by anecdote, and the baseline-anchored rule holds

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-04.1): Persona review at `.delivery/artifacts/<impl-run>/user-feedback/adversarial-4-7-sample.md` AND no severity-HIGH tone/depth regression vs `4-7-baseline.json`'s `challenger_sample_path` AND AC-04.2 checklist met.
- AC-2 (AC-04.2, with soften-hatch): ≥3 weaknesses, ≥2 specific card-name referents, ≥1 concrete alternative per invocation. Soften-hatch: if an invocation has <3 weaknesses because the input is small, Challenger documents that explicitly and the invocation counts as pass.
- AC-3 (AC-04.3): Pass ⇒ documentation-only; fail ⇒ targeted tone-strengthening prose edit.
- AC-4 (AC-04.4): Risk = HIGH (NDOC-03 no Anthropic adversarial benchmark) — recorded on the persona review.
- AC-5: ADR-006 frontmatter applied.

**Dogfood / test command**:
`test -f .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/adversarial-4-7-sample.md && test "$(grep -cE '^- +(Weakness|Referent|Alternative)' .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/adversarial-4-7-sample.md)" -ge "6" && grep -q '^model_awareness: opus-4-7$' mtg-commander/SKILL.md`

**Out of Scope**: Rewriting mtg-commander scryfall integration, price logic, or deck-building pipeline; edits to `.mtg-commander.yml` schema; Challenger rewrites absent a failed dogfood.

---

### Story WI-10 — Model-ID sweep (`agent_registry.py` + `stage_definitions.py`)

- **Wave**: 4
- **T-shirt**: S
- **Depends on**: WI-02
- **Parallelisable with**: WI-11, WI-12, WI-13
- **PRD anchors**: REQ-01, AC-01.1/2/3/4/5; MID-01/02/03/04; ADR-002; F-04; challenger loop2 Finding #5 (carry-item MID-04 gate); transformation-plan §6.2 WI-10
- **As a**: marketplace-drift-hygiene owner
- **I want**: MID-01 (line 148), MID-02 (line 172), MID-03 (line 187) in `agent_registry.py` updated to canonical IDs with provenance comments, and MID-04 (7 lines in `stage_definitions.py`) handled per the AC-01.5 structural-AS-IS outcome
- **So that**: the grep-visible model-ID drift closes to 0 without accidentally breaking `prd-quality-gate-flow`'s internal routing if MID-04 labels are routing keys

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-01.1): Task names files + line numbers for MID-01/02/03/04 (all 10 lines: `agentic-flow-builder/scripts/agent_registry.py` lines 148, 172, 187; `prd-quality-gate-flow/stage_definitions.py` lines 47, 83, 115, 150, 181, 216, 243).
- AC-2 (AC-01.2): MID-03 sweep is drift-hygiene, not retirement-urgency (zero SDK imports).
- AC-3 (AC-01.3): MID-02 discovery task — verify intent before substitution (proposed `claude-haiku-4-5-20251001` per Open Question 1).
- AC-4 (AC-01.4): Post-sweep regression guard runs the M-01 regex; expected 0 hits.
- AC-5 (AC-01.5, bound-here for carry-item MID-04): Structural AS-IS check of `flow_orchestrator.py` **before** MID-04 edits. If labels never reach SDK: comment-annotate only. If they do: substitute canonical IDs. Post-sweep full-pipeline smoke test of `prd-quality-gate-flow` executes end-to-end without routing errors.

**Dogfood / test command**:
`! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py' && python prd-quality-gate-flow/check_db.py > /dev/null`

**Out of Scope**: SDK wiring of `agent_registry.py` or `stage_definitions.py` (deferred to `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` in WI-13); Business Rules Engine changes; any model-ID edits in `.delivery/` history.

---

### Story WI-11 — Frontmatter marker backfill (non-keystone SKILL.md files)

- **Wave**: 4
- **T-shirt**: XS
- **Depends on**: WI-04, WI-05, WI-06, WI-07, WI-08, WI-09
- **Parallelisable with**: WI-10, WI-12, WI-13
- **PRD anchors**: ADR-006; Galadriel DX-M4 (target 0 missing); fresh-challenger F-C-08 / priority #3 (carry-item label drift); transformation-plan §6.2 WI-11
- **As a**: marketplace DX guardian
- **I want**: ADR-006 three-field frontmatter added to every SKILL.md in the scope-baseline §4 inventory that is not one of the six keystones already stamped in Waves 2–3, using the honest two-tier stamp `model_awareness: opus-4-7-frontmatter-only` to distinguish mechanical backfill from prose-reviewed files
- **So that**: `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:'` returns empty (DX-M4 target 0 missing) AND a future `grep 'model_awareness: opus-4-7$'` across the same file set returns exactly the six prose-reviewed keystones — closing the carry-item label drift without making a false "reviewed" claim on 11 un-reviewed files

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (rule-derived set): Backfill set = `{ SKILL.md files in scope-baseline §4 inventory } \ { six keystones } \ { files already stamped in Waves 2–3 }`. Impl-run runs `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | sort` and subtracts the keystone set. The verified current complement is exactly 11 files: `agentic-flow-builder/skills/flow-builder/SKILL.md`, `delivery-team/skills/alias-creator/SKILL.md`, `delivery-team/skills/architect/paradigms/ddd/SKILL.md`, `delivery-team/skills/architect/paradigms/volatility/SKILL.md`, `delivery-team/skills/developer/SKILL.md`, `delivery-team/skills/godot/SKILL.md`, `delivery-team/skills/operations/SKILL.md`, `delivery-team/skills/presentation/SKILL.md`, `delivery-team/skills/quality/SKILL.md`, `delivery-team/skills/ui/SKILL.md`, `delivery-team/skills/user-feedback/SKILL.md`.
- AC-2: Each backfill file gains `model_awareness: opus-4-7-frontmatter-only`, `last_audited: <backfill date>`, `pattern_library_version: 4-7-1`. The `-frontmatter-only` suffix is the load-bearing carry-item "label drift" resolution (one term, two honest tiers).
- AC-3: `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l` returns 0 (DX-M4 target 0 missing).
- AC-4: `last_audited` dates reflect actual review state per file (Wave 2–3 edit dates on keystones; backfill date on the complement).
- AC-5: No prose edits; mechanical PR only.
- AC-6: `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l 'model_awareness: opus-4-7$' | wc -l` returns 6 (keystones); `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l 'model_awareness: opus-4-7-frontmatter-only$' | wc -l` returns 11 (backfill set).

**Dogfood / test command**:
`test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l)" = "0" && test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7$' | wc -l)" = "6" && test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7-frontmatter-only$' | wc -l)" = "11"`

**Out of Scope**: Prose-skimming the 11 backfill files (deferred to `BACKLOG-47-frontmatter-only-prose-skim.md` in WI-13); editing the 6 keystones' frontmatter (owned by WI-04/05/06/07/08/09).

---

### Story WI-12 — Alias-theme tone dogfood + optional edit

- **Wave**: 4
- **T-shirt**: S (pass) / M (regression)
- **Depends on**: WI-02
- **Parallelisable with**: WI-10, WI-11, WI-13
- **PRD anchors**: REQ-05, AC-05.1/2/3; F-27; M-05; DEV-02 (path correction); transformation-plan §6.2 WI-12
- **As a**: alias-theme tone guardian
- **I want**: three themes sampled from `delivery-team/skills/delivery-flow/references/aliases/`, one stage announcement rendered per theme on 4.7, and voice-preservation scored against extracted markers (`yq '.roles[].catchphrase'` + `.roles[].examples[]`); edit only the affected theme YAML if M-05 target fails
- **So that**: F-27 (4.7's calmer voice) is caught as a theme-specific regression if it flattens personality, and the dogfood-before-edit primitive holds on the 13 theme YAMLs

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1 (AC-05.1): 3 themes sampled from `delivery-team/skills/delivery-flow/references/aliases/` (13 files). Markers extracted via `yq` from `roles[].catchphrase` + `roles[].examples[]`. ≥1 announcement rendered per theme. "Preserves voice" = ≥50% markers present.
- AC-1a (format binding — closes G-4 format-coupling): The `alias-theme-sample.md` artifact MUST render the per-theme results as a markdown table with a `Theme` column and one row per sampled theme (≥3 rows). The WI-12 dogfood `grep -cE '^\| *(Theme|theme) '` gate is the mechanical check of this AC; pin the format, pin the gate.
- AC-2 (M-05 target): ≥80% of sampled announcements preserve voice.
- AC-3 (AC-05.2): Pass ⇒ no edit. Fail ⇒ tone-strengthening of the affected theme YAML files (NOT the alias-creator SKILL or theme-format schema).
- AC-4 (AC-05.3): Sample saved to `.delivery/artifacts/<impl-run>/user-feedback/alias-theme-sample.md`.

**Dogfood / test command**:
`test -f .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/alias-theme-sample.md && test "$(grep -cE '^\| *(Theme|theme) ' .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/alias-theme-sample.md)" -ge "3" && grep -qE 'voice[- ]preservation|markers? preserved' .delivery/artifacts/run-2026-04-22-4x7e/user-feedback/alias-theme-sample.md`

**Out of Scope**: Editing `alias-creator/SKILL.md` or `theme-format.md` schema; adding new themes; removing themes; changes to the alias-creator skill routing.

---

### Story WI-13 — NEW-BACKLOG registration (dual-write: local file + GitHub issue) + optional REQ-06 over-pressure audit

- **Wave**: 4
- **T-shirt**: XS
- **Depends on**: WI-02
- **Parallelisable with**: WI-10, WI-11, WI-12, WI-14
- **PRD anchors**: REQ-07, AC-07.1/2; REQ-06, AC-06.1/2; ADR-004; Galadriel §5; challenger loop2 Finding #3; fresh-challenger F-C-08; idea-brief §5 user-direction dual-write; transformation-plan §6.2 WI-13
- **As a**: scope-terminus guardian
- **I want**: for each deferred item, a local `.delivery/backlog/BACKLOG-47-<topic>.md` file **and** a GitHub issue labeled `backlog-47` (dual-write per user direction), covering the six required topics plus the three Galadriel on-ramp items if time permits, plus the optional DX-M5 over-pressure grep across the six keystones
- **So that**: the PRD's Non-Goals and Constraint 2 hold by logging-not-deleting, and the backlog is simultaneously discoverable in the repo (`find .delivery/backlog/`) and in GitHub (`gh issue list --label backlog-47`) without either surface going stale

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2 + idea-brief §5 dual-write):
- AC-1 (REQ-07, AC-07.1/2 — required topic set): Create both the local file AND a `gh issue` labeled `backlog-47` for each of:
    - `BACKLOG-47-task-budget-eval` (F-18 task_budget beta)
    - `BACKLOG-47-memory-tool-eval` (F-19 memory tool)
    - `BACKLOG-47-sdk-wiring-routing-via-claude-api` (ADR-004 + Open Question 8)
    - `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read` (challenger loop2 Finding #3)
    - `BACKLOG-47-frontmatter-only-prose-skim` (fresh-challenger F-C-08; upgrade path from `opus-4-7-frontmatter-only` to `opus-4-7` for the 11 WI-11 files)
    - `BACKLOG-47-overpressure-audit` (if Architect defers the optional REQ-06 line-level edit).
- AC-2 (Galadriel §5, on-ramp; time-permitting): Create file + issue for `BACKLOG-47-contributing-4-7-note`, `BACKLOG-47-migration-guide-stub`, `BACKLOG-47-4-7-example-skill-designation`.
- AC-3 (REQ-06, AC-06.1 — optional grep): Run DX-M5 pressure-calibration grep across six keystone files (`CRITICAL`, `MUST`, `NEVER`, `ALWAYS`). Output count table + Architect judgement per file. If Architect defers, AC-1 registers `BACKLOG-47-overpressure-audit` (AC-06.2).
- AC-4 (dual-write invariant, user direction): Every `BACKLOG-47-*.md` file has a matching open GitHub issue with the `backlog-47` label; and every issue has a matching file. Config already has `github.create_issues: true`.
- AC-5: Each backlog file contains a one-paragraph scope statement and a link back to transformation-plan.md.
- AC-6: Impl-run has autonomy (memory `feedback_team_autonomy.md`) to adjust the Galadriel §5 time-permitting triplet without re-opening scope.

**Dogfood / test command**:
`test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" -ge "6" && test "$(gh issue list --label backlog-47 --state all --json number --jq 'length')" -ge "6" && test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" = "$(gh issue list --label backlog-47 --state all --json number --jq 'length')"`

**Out of Scope**: Any actual work on task_budget / memory-tool / prompt-caching / SDK wiring (logging only); Galadriel on-ramp artifact authoring (only backlog stubs, not the full documents); CONTRIBUTING.md edits.

---

### Story WI-14 — CI guard wiring (DX-M4 header warn + M-02 stale-ID block)

- **Wave**: 4
- **T-shirt**: XS
- **Depends on**: WI-10, WI-11
- **Parallelisable with**: WI-12, WI-13
- **PRD anchors**: Samwise advisory #2; PRD M-01/M-02; ADR-006 CI-warning note; transformation-plan §6.2 WI-14
- **As a**: CI regression-guard owner
- **I want**: two new GitHub Actions workflows under `.github/workflows/` — `skill-md-header-warn.yml` (warning-only, DX-M4) and `stale-model-id-guard.yml` (blocking, M-02) — both templated off the existing `workflow-injection-lint.yml` shape
- **So that**: DX-M4 header coverage and M-02 no-regression guarantees have an owner at CI-time, not just at WI-time, and a future PR cannot re-introduce `claude-opus-4-20250514` or land a new SKILL.md without a `model_awareness` field without the CI surfacing it

**Acceptance Criteria** (carry directly from transformation-plan.md §6.2):
- AC-1: File `.github/workflows/skill-md-header-warn.yml` exists. On `pull_request`, runs `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'` and logs any missing-header file as a PR comment or job warning. Non-blocking.
- AC-2: File `.github/workflows/stale-model-id-guard.yml` exists. On `pull_request`, runs the PRD-canonical M-01/M-02 regex (the one that returned 3 hits on 2026-04-20; post-WI-10 target 0) across tracked `.py` and `.md` files excluding `.delivery/` and `prd_flows.db`. Blocks PR on hits.
- AC-3: Structural template: `workflow-injection-lint.yml` (lines/shape) is the copy-pattern — same YAML shape, same failure-mode contract.
- AC-4: No change to CI runners, secrets, or third-party actions beyond what `workflow-injection-lint.yml` already uses.
- AC-5: Post-merge synthetic-test validation: a test PR re-introducing `claude-opus-4-20250514` fails `stale-model-id-guard.yml`; a test PR introducing a new SKILL.md without `model_awareness:` produces a warning but does not block.
- AC-6: Sequenced AFTER WI-10 (sweep passes the regex) and AFTER WI-11 (backfill zeroes the header-missing warning) so both land green on merge.

**Dogfood / test command**:
`test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml && grep -qE '^on:[[:space:]]*$' .github/workflows/skill-md-header-warn.yml && grep -qE '^[[:space:]]+pull_request:' .github/workflows/skill-md-header-warn.yml && grep -qE '^on:[[:space:]]*$' .github/workflows/stale-model-id-guard.yml && grep -qE '^[[:space:]]+pull_request:' .github/workflows/stale-model-id-guard.yml`

**Out of Scope**: Edits to `workflow-injection-lint.yml`; new secrets; new CI runners; integration with external services; enforcement on the `main` branch beyond PR checks.

---

## 3. Carry-Item ACs (from retrospective.md)

The four carry-items surfaced by the DESIGN retrospective (A1–A6 cluster) are **already bound, not new work.** Each is stated here with its owning WI and the specific AC that carries it so the impl-run team does not treat them as fresh requirements.

- **MID-04 (stage_definitions.py 7 lines)** → **bound to WI-10 AC-5 (AC-01.5)**. The structural AS-IS check of `flow_orchestrator.py` runs **before** any MID-04 edit; if labels never reach SDK, comment-annotate only; if they do, substitute canonical IDs. No new work.
- **Keystone AC unevenness (each keystone has a per-file concrete recommendation OR explicit Done-with-reason)** → **bound to WI-07 AC-1, WI-08 AC-1, and WI-09 AC-2**. Each keystone audit WI requires per-file / per-sub-role / per-invocation concrete recommendation or explicit Done-with-reason. AC-02.1 widening from challenger loop2 Finding #2 is carried into the three WI ACs above. No new work.
- **AC-03B.2 hardening (two grep thresholds + JSON summary for research-probe)** → **bound to WI-06 AC-2 and WI-06 AC-3**. The two greps (`grep -cE '^(WebFetch|WebSearch)\(' ...` ≥ 2 AND `grep -oE 'https?://[^/ )"]+' ... | sort -u | wc -l` ≥ 2) plus the one-line JSON summary at `research-probe-result.json` are load-bearing. No new work; measurement is three existing operations (two greps + one JSON write) already stitched into WI-06.
- **Label drift (ADR-006 `-frontmatter-only` suffix distinguishing backfill from keystone stamps)** → **bound to WI-11 AC-2 and WI-11 AC-6**. The honest two-tier stamp `model_awareness: opus-4-7` (keystones, prose-reviewed) vs `model_awareness: opus-4-7-frontmatter-only` (backfill, mechanical) is the label-drift resolution. Six-versus-eleven grep counts in the WI-11 dogfood command confirm it. No new work.

---

## 4. WI-13 Deviation — Dual-Write Backlog (Local File AND GitHub Issue)

The transformation plan §6.2 WI-13 row specifies local `.delivery/backlog/BACKLOG-47-<topic>.md` file creation. The user (per `idea-brief.md §5`) directed a **dual-write**: for each deferred item, create **both** the local file **AND** a GitHub issue labeled `backlog-47`. This is the only authored deviation from plan defaults.

- **Config state**: `.delivery/config.yml` already has `github.create_issues: true` — no config change needed.
- **Required six topics** (file + issue each):
    1. `BACKLOG-47-task-budget-eval`
    2. `BACKLOG-47-memory-tool-eval`
    3. `BACKLOG-47-sdk-wiring-routing-via-claude-api`
    4. `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read`
    5. `BACKLOG-47-frontmatter-only-prose-skim`
    6. `BACKLOG-47-overpressure-audit` (if Architect defers the optional REQ-06 line-level edit)
- **Time-permitting three Galadriel on-ramp topics** (file + issue each):
    7. `BACKLOG-47-contributing-4-7-note`
    8. `BACKLOG-47-migration-guide-stub`
    9. `BACKLOG-47-4-7-example-skill-designation`
- **Invariant**: every file has a matching open-or-closed `backlog-47`-labelled issue; every `backlog-47`-labelled issue has a matching file. The invariant is captured in the WI-13 dogfood command: counts must match and both must be ≥6.
- **Count and topic set are otherwise unchanged from the transformation-plan §6.2 WI-13 enumeration.** The dual-write is an addition to the surface (local + remote), not a change to scope.

---

## 5. Wave Gates (Mechanical, Not Discretionary)

The four wave-exit gates are stated literally. Each is a mechanical check — a command output or file state, not a judgement call. Waves do not advance until the prior gate passes.

- **Wave 1 → Wave 2 gate**: `.delivery/artifacts/run-2026-04-22-4x7e/research/ndoc-02-spike.md` contains a `verdict:` line matching regex `(unknown-fields-accepted|strict)`. If `strict`, ADR-006 rollback activates and **all** Wave 2–4 frontmatter edits (WI-04, WI-05, WI-06, WI-11) flip to HTML-comment placement (`<!-- model_awareness: opus-4-7 -->` etc. below the existing `---` block) instead of YAML-frontmatter fields. Semantics identical.
- **Wave 2 → Wave 3 gate**: `prompt-engineer/SKILL.md` contains exactly six `### Pattern 4.N — ` headings (N in 1..6). Verified by `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returning `6`. Wave 3 keystones (WI-07, WI-08) cite patterns by name — if the pattern library does not exist, citations orphan.
- **Wave 3 → Wave 4 gate**: WI-06 and WI-09 dogfood verdicts recorded (pass OR fail; fail triggers the edit-path within the same wave). Specifically: `research-probe-result.json` exists with a `pass` field (true or false); `adversarial-4-7-sample.md` exists and the AC-04.2 checklist is scored (with soften-hatch if applicable).
- **Wave 4 → UAT gate**:
    - WI-10 stale-ID grep returns 0: `! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'`.
    - WI-11 frontmatter grep returns empty: `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l` = 0.
    - WI-14 CI workflows exist: `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml`.

---

## 6. Rollback Protocol

- **Per ADR-002** (direct strings with provenance comments): every WI is `git revert`-compatible. No central alias module means no multi-file state to unwind.
- **Per ADR-005** (single-file pattern library): WI-05 revert is a single-file unwind. Wave 3 citations (WI-07, WI-08) cite **into** WI-05 only, not between themselves — no intra-Wave-3 citation web to break.
- **Per ADR-006** (readiness-marker convention with mechanical rollback trigger): WI-03's `strict` verdict flips **mechanically** — no re-litigation — all Wave 2–4 frontmatter edits to HTML-comment form under the existing `---` block. Same three fields, same semantics, different placement.
- **Wave-by-wave revert discipline** (carried from transformation-plan §7.4):
    - Wave 1: read-only captures; no code changes; no rollback needed.
    - Wave 2: `git revert` of WI-04/05/06 commits. Baseline from Wave 1 is the reference state; no downstream WI depends on Wave 2 code.
    - Wave 3: `git revert` of WI-07/08/09 commits. Pattern library (WI-05) stands. Frontmatter from WI-04 stands.
    - Wave 4: per-WI revert. **Order**: revert WI-14 (CI guards) BEFORE reverting WI-10 (sweep) or WI-11 (backfill) if a full Wave-4 rollback is needed — otherwise `stale-model-id-guard.yml` blocks the revert PR that re-introduces stale IDs.

---

## 7. Success Definition — The Six Binding End-State Verification Commands

The implementation run is complete when these six verification commands return the expected values. These are reproduced verbatim from the kickoff plan and are the binding end-state gates (M-01, M-02, DX-M3, DX-M4, backlog dual-write invariant, CI wiring).

1. **M-01 — zero stale dated Claude model IDs in Python surfaces**
   `! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'`
   *Expected*: exit 0 (no hits).

2. **DX-M4 — zero SKILL.md files missing the `model_awareness` header**
   `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -L 'model_awareness:' | wc -l`
   *Expected*: `0`.

3. **WI-11 honest two-tier stamp integrity — six keystones + eleven backfill files**
   `test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7$' | wc -l)" = "6" && test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '^model_awareness: opus-4-7-frontmatter-only$' | wc -l)" = "11"`
   *Expected*: exit 0 (both counts correct; carry-item label drift closed).

4. **DX-M3 — zero restatements of `<thinking>` outside the canonical pattern library**
   `grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/ | grep -v 'prompt-engineer/SKILL.md' | wc -l`
   *Expected*: `0`.

5. **WI-13 dual-write invariant — local file count equals GitHub `backlog-47` issue count, both ≥ 6**
   `test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" -ge "6" && test "$(gh issue list --label backlog-47 --state all --json number --jq 'length')" -ge "6" && test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null | wc -l)" = "$(gh issue list --label backlog-47 --state all --json number --jq 'length')"`
   *Expected*: exit 0 (equal counts; dual-write holds).

6. **WI-14 CI guard files present**
   `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml && test -f .github/workflows/workflow-injection-lint.yml`
   *Expected*: exit 0 (both new guards exist; DEFECT-004 guard still present).

When all six return their expected values, the migration is complete and the UAT gate opens.

---

## 8. Notes for the Implementation Team

- **Autonomy binds** (memory `feedback_team_autonomy.md`). The impl-run PO decides shipping cadence (rolling vs batched; Samwise advisory #8 deferred to impl-run choice), commit-type mapping per wave (Samwise advisory #4), and opportunistic absorption of deferred findings F-C-03/04/05/06/07/09/10 per transformation-plan §6.5.
- **Dogfood binds** (memory `feedback_dogfooding.md`). Every prose-edit WI pairs with a dogfood gate; AC-02.4 formalises the gate. Developer DoD is non-optional for any WI naming executable commands (DESIGN retrospective "Lesson 2").
- **Scope terminus by logging** (memory — PRD citation discipline; retrospective "Lesson 7"). Out-of-scope-but-valuable items go to `BACKLOG-47-*.md` (deferred, not deleted) via WI-13's dual-write.
- **Route through PO** (memory `feedback_route_through_po.md`). This execution-PRD is the prompt; the 14 stories are the pipeline's inputs; the team decides tactical implementation.

---

## 9. Revision Log

Audit trail for the Refine-light DoD self-correction round 1 (Gimli — Developer — blocking finding G-1 plus non-blocking G-2..G-6). Each entry maps a finding to the applied edit so round-2 re-verification is a file-diff read, not a scavenger hunt.

- **G-1 (BLOCKING) — WI-14 `yq` dependency removed** — *applied 2026-04-22.* WI-14 "Dogfood / test command" rewritten to pure `grep -qE` checks against the `^on:$` block and `^  pull_request:` line in both `skill-md-header-warn.yml` and `stale-model-id-guard.yml`. No new host dependency. Intent preserved: both workflow files must exist AND both must carry a `pull_request:` trigger.
- **G-2 (wording) — WI-11 `**/SKILL.md` shell-glob replaced with portable `find … | xargs grep` idiom** — *applied 2026-04-22.* AC-3 and AC-6 in WI-11, plus the WI-11 "So that" narrative, now use the same `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep …` idiom that the dogfood block and §7 already use. No more 3-vs-6-vs-17 false reads under default bash/fish.
- **G-3 (sharp edge) — WI-09 awk vacuous-pass trap eliminated** — *applied 2026-04-22.* WI-09 dogfood now uses `test "$(grep -cE … )" -ge "6"` — no awk, no empty-stdin trap, same semantics, two fewer characters of risk.
- **G-4 (format coupling) — WI-12 AC-1a format binding added** — *applied 2026-04-22.* New AC-1a requires the `alias-theme-sample.md` artifact to render as a markdown table with a `Theme` column (≥3 rows). The existing dogfood regex `^\| *(Theme|theme) ` is now the mechanical check of a prescribed format — pin the format, pin the gate.
- **G-5 (scope-coverage gap) — WI-05 AC-7 broadens single-line retarget to close §7.4** — *applied 2026-04-22.* New WI-05 AC-7 scopes in the retarget-or-prune of `research-agent/references/prompt-library.md` line 10 so the DX-M3 end-state command in §7.4 returns 0 on merge. WI-05 "Out of Scope" carries an explicit exception clause for this single line; no other references-file edits are admitted.
- **G-6 (cosmetic) — WI-03 `grep -cE` swapped for `grep -qE`** — *applied 2026-04-22.* Count was never read; quiet exit-only form is idiomatic and one character shorter.

All six applied in a single edit pass against `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`. No other content reshaped; §1–§8 semantics intact.

---

*"The stories are cut. The waves are gated. The dogfood commands are written so a Developer DoD can run them — because reading them did not catch the last three bugs. Ship this plan. Then ship the next one."*
— Gandalf

---

**End of execution-PRD.**

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/02-refine/po/execution-prd.md
SUMMARY: Fourteen stories cut from the transformation plan, each bound to its REQ/AC/ADR anchor, each runnable by a Developer DoD — the keystones shall not wander.
```

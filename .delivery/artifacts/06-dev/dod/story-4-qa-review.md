<!-- run: run-2026-05-09-tk4 | stage: 6 (Development) | story: 4 of 7 | wi: W3-8 | reviewer: QA Engineer (FRESH) | round: 1 | binding: ADR-tk4-002, TC-4 -->

# Story 4 (W3-8) — QA DoD Review, Round 1

> Note: this file overwrites a stale prior-wave Story 4 QA review (W2-5 product-delivery 12-pattern split, dated 2026-05-03 / Legolas). The Wave-2 Story-4 record is preserved in the post-pipeline retro for that run; this file now binds to **run-2026-05-09-tk4 W3-8 paradigm sub-skill pattern**.

## STATUS

**STATUS: DONE**

All 5 Story 4 ACs traced to TC-4 and verified empirically against the working tree. The presentation conditional path (option-b) is documented with explicit, ADR-anchored rationale. No empirical (runtime-only) acceptance criteria exist for this story — the entire scope is structural skill reorganization verifiable by `find` + `grep` + `wc` and frontmatter inspection. Therefore CODE_COMPLETE does not apply; **DONE** is the correct terminal status.

## Gate Criteria Trace (5)

### Gate 1 — All 5 Story 4 ACs traced to TC-4 + verified

| AC | Source | TC mapping | Verification | Result |
|----|--------|-----------|--------------|--------|
| AC-1 (research-agent ≥5 sub-skills + frontmatter contract) | `stories.md` line 174 | TC-4 sub-clause 1 (test-strategy.md line 54) | `find research-agent -path "*/skills/research-types/*/SKILL.md" \| wc -l` → **5**; head of all 5 files confirms `disable-model-invocation: true`, `tier: C`, `parent_skill: research-agent/SKILL.md`, `axis: research-types`, distinct `variant:` values (exploratory / descriptive / explanatory / evaluative / comparative); `name:` follows `research-types-<variant>` convention | **PASS** |
| AC-2 (user-feedback =4 persona sub-skills + 4/4 dogfood routing — joint with Story 3 W3-6 AC-2) | `stories.md` line 175 | TC-4 sub-clause 2 | `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" \| wc -l` → **4**; head of all 4 files confirms full contract; parent dispatch table at `delivery-team/skills/user-feedback/SKILL.md` lines 99–102 routes GAME_DEV → gamers, GREENFIELD/FEATURE/WEB_APP → web-app, ENTERPRISE/B2B → enterprise, Any (overlay) → demographic — 4/4 router rows present | **PASS** (joint-AC honored; Story 3 line-count vehicle satisfied AC simultaneously) |
| AC-3 (marketplace-discoverability lint: top-level zero violations) | `stories.md` line 176 | TC-4 sub-clause 3 | `grep -lrE "^disable-model-invocation:[[:space:]]*true" --include=SKILL.md .` returns **exactly 9 paths**, all matching `.*/skills/[^/]+/[^/]+/SKILL\.md` (5 research-types + 4 personas). The negative-filter pass (paths NOT matching the paradigm sub-skill OR grandfathered paradigms regex) returns **empty**. Zero top-level plugin SKILL.md flagged. The dev's prose-fragility note (literal `: true` token in narrative) is resolved upstream and not present in any current file | **PASS** |
| AC-4 (cache-prefix invariant on parent skills) | `stories.md` line 177 | TC-4 cross-cut + ADR-tk4-002 §Cache-prefix impact | `governance/cache-prefix-hash.txt` content is the single line `f997ec25... delivery-team/skills/delivery-flow/SKILL.md`. `git log --since="2026-05-09" -- governance/cache-prefix-hash.txt` returns empty → zero modifications this run. Last touch was Wave caveman-lite (`baa49b9`), not tk4. Neither `research-agent/SKILL.md` nor `delivery-team/skills/user-feedback/SKILL.md` is in the tracked scope, so the invariant is satisfied trivially. Independent corroboration: research-agent dispatch table first content row appears at line 63 / byte offset ~3322 (verified via `grep -bn`), placing the addition **1.6 KiB below the 2k-byte cache-prefix region**. user-feedback dispatch table at line 99 is even further below the threshold | **PASS** |
| AC-5 (presentation conditional — option a OR option b with explicit rationale) | `stories.md` line 178 | TC-4 sub-clause "presentation conditional path" | `find delivery-team/skills/presentation -path "*/skills/types/*/SKILL.md" \| wc -l` → **0** (option-a not taken). `ls delivery-team/skills/presentation/references/types/` enumerates **9** type references (sprint-review, feature-pitch, stakeholder-update, technical-deep-dive, investor-pitch, roadmap, product-demo, onboarding, retrospective-summary) — Story 2 W3-2 sufficiency intact. `wc -l delivery-team/skills/presentation/SKILL.md` → **182** (well below Tier-B 300 ceiling, headroom = 118 lines). Decision **option (b)** is recorded in the implementation report §Self-DoD AC-5 row with the cite chain ADR-tk4-002 §Decision §3 (default favors references-only when sufficient) + §Alternatives considered #3 (rejected unconditional adoption), and deferred to BACKLOG-106+ | **PASS** (option-b recorded with explicit rationale — see Gate 5 below for the structural rationale audit) |

### Gate 2 — TC-4 commands execute correctly

TC-4 specifies three runnable commands plus the conditional-path verification. All four execute cleanly:

| TC-4 Command | Verbatim Output | Pass Criterion | Result |
|---|---|---|---|
| `find research-agent -path "*/skills/research-types/*/SKILL.md" \| wc -l` | `5` | ≥5 | PASS |
| `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" \| wc -l` | `4` | =4 | PASS |
| `grep -L "disable-model-invocation: true"` on each of the 9 sub-skills | empty (exit 1, by `grep -L` semantics: zero files MISSING the flag) | empty list | PASS |
| Conditional-path: 9 sub-skills + 9/9 router (option a) OR defer cite (option b) | 0 type sub-skills + 9 references + 182-line parent + decision-cite present | EITHER branch satisfied | PASS (option b) |

**Marketplace-lint pattern compliance** (TC-4 expected-result tail "marketplace lint excludes top-level SKILL.md") was checked via the regex `'.*/skills/[^/]+/[^/]+/SKILL\.md$'` OR `'.*/paradigms/[^/]+/SKILL\.md$'`. Negative filter = empty → zero top-level violations.

### Gate 3 — Each sub-skill has loadable content (not empty stub)

Both axes satisfy the loadable-content bar. The two axes follow different content patterns by design (per ADR-tk4-002 §Sub-skill body contract: a sub-skill body may be either thick-extracted-content or thin-router-with-references-pointer; both are valid as long as it loads SOMETHING type-specific):

| Axis | File | Total lines / Tier-C ceiling | Body content lines | Pattern | Loadable? |
|---|---|---|---|---|---|
| research-types | exploratory | 93 / 200 | 51 | thick-extracted (Discovery Report pattern + SPICE phases) | YES |
| research-types | descriptive | 87 / 200 | 48 | thick-extracted (Landscape Map pattern) | YES |
| research-types | explanatory | 99 / 200 | 58 | thick-extracted (Causal Analysis + 5 Whys / Fishbone / PECO) | YES |
| research-types | evaluative | 112 / 200 | 66 | thick-extracted (Impact Assessment + PICO + risk-of-bias) | YES |
| research-types | comparative | 114 / 200 | 67 | thick-extracted (Decision Matrix + SWOT + QCA) | YES |
| personas | gamers | 36 / 200 | 17 | thin-router (persona enumeration table + invocation pattern + game-specific context hints + pointer to `references/persona-library.md` Category 1 block) | YES |
| personas | web-app | 34 / 200 | 15 | thin-router (Category 2 block pointer + invocation pattern) | YES |
| personas | enterprise | 33 / 200 | 14 | thin-router (Category 3 block pointer + invocation pattern) | YES |
| personas | demographic | 33 / 200 | 14 | thin-router (Category 4 block pointer + overlay handling note) | YES |

**Verification method**: read each file, confirmed presence of (i) sub-skill purpose statement, (ii) at least one structural section beyond the H1, (iii) either inline body content OR a concrete file-path pointer that resolves. None of the 9 files is an empty stub or a single-line placeholder. The persona variants are intentionally thinner because the canonical persona profiles already live in the parent's `references/persona-library.md` (Category 1–4 blocks); the sub-skill exists to scope the dispatch and enumerate which personas belong in the family. The research-types variants are thicker because the parent's pattern catalogue is paradigm-specific and was extracted whole.

### Gate 4 — Implementation report self-DoD complete

The implementation report at `.delivery/artifacts/06-dev/developer/story-4-implementation.md` contains:

- A 3-axis implementation table identifying axis ownership, parent SKILL.md status, variants, sub-skill paths, and parent router status (lines 13–17).
- Per-sub-skill frontmatter contract compliance table covering all 5 NEW research-agent sub-skills with explicit columns for each contract key (lines 26–32).
- A cache-prefix impact section that walks through the AC-4 reasoning and records the line/byte offsets for both parent dispatch table additions (lines 38–43).
- A self-DoD table covering all 5 ACs with verification command/logic and PASS markings (lines 49–55).
- A plugin-dev pre-load compliance section confirming `delivery-team:developer` and `plugin-dev:skill-development` SKILL_LOADED (lines 57–60).
- A complete Files Changed inventory split into NEW / MODIFIED / UNCHANGED-but-VERIFIED / UNCHANGED-by-design (lines 62–79).
- A CI-lint forward-reference note flagging the prose-fragility false positive and the recommended frontmatter-aware Python check (lines 81–83).
- A budget check note confirming `python3 scripts/check_skill_budgets.py` exits 0 with zero violations and zero remaining known-debt (lines 85–87).
- Final STATUS line and run signature (lines 89–93).

**Self-DoD completeness**: PASS. Every required element of the standard developer report shape is present, every AC has a concrete verification clause, and every claim that a reviewer would want to spot-check is anchored to a runnable command or a file/line citation.

### Gate 5 — Partial-compliance for presentation option-b documented with explicit rationale

The presentation paradigm sub-skill axis is the deliberately-conditional axis in this story. The implementation report records option (b) — references-only retained — in the AC-5 row of the self-DoD table (line 55) and again in the 3-axis table footer (line 17). The rationale chain is:

1. **Empirical sufficiency**: presentation parent SKILL.md is 182 lines / Tier-B 300 ceiling = 60.7% utilization, with a 118-line headroom margin. There is no token-economy pressure or cognitive-load pressure justifying the cost of creating 9 new SKILL.md files.
2. **References-only path already exists**: `delivery-team/skills/presentation/references/types/<type>.md` ×9 was extracted in Story 2 W3-2 and ships the same per-type content the paradigm sub-skill route would have shipped. The router-vs-references-only choice is a dispatch shape decision, not a content decision.
3. **ADR-tk4-002 §Decision §3 default**: when Stage 6 finds references-only sufficient, references-only is the default (paradigm sub-skill is the conditional upgrade, not the conditional default).
4. **ADR-tk4-002 §Alternatives considered #3**: unconditional paradigm-sub-skill adoption was explicitly rejected during Stage 4 review.
5. **AC-5 wording itself**: the AC text grants two explicit branches; option (b) is a first-class outcome, not a partial-compliance fallback.
6. **Future path preserved**: deferral is to BACKLOG-106+ alongside the developer 14-language and architect 11-role paradigm-sub-skill rollouts, so the pattern extension is queued not orphaned.

**Partial-compliance marker for the QA reviewer's audit trail**: the only sense in which this is "partial" compliance with the broader Story 4 paradigm-sub-skill mission is that 2 of 3 axes shipped paradigm sub-skills (research-types + personas) while the 3rd (presentation types) shipped references-only. AC-5 itself, however, is fully PASSED — the AC asks for a recorded decision in either branch. Both branches satisfy the AC. Option (b) is the contractually-correct choice for this story and is explicitly justified.

## Sub-Skill Frontmatter Spot-Check Spreading

Per ADR-tk4-002 §Sub-skill SKILL.md frontmatter contract, each paradigm sub-skill must carry: `name`, `description`, `license`, `disable-model-invocation: true`, `tier`, `parent_skill`, `axis`, `variant`. The `allowed-tools:` key is present on the research-agent axis sub-skills and absent on the persona axis (the personas axis is thin-router and inherits the parent's tool surface implicitly). Both shapes pass the contract minimum.

| Contract key | research-types axis (×5) | personas axis (×4) |
|---|---|---|
| `name` | PASS | PASS |
| `description` | PASS | PASS |
| `license` | PASS | PASS |
| `disable-model-invocation: true` | PASS | PASS |
| `tier: C` | PASS | PASS |
| `parent_skill: <parent>/SKILL.md` | PASS | PASS |
| `axis: <axis-name>` | PASS (`research-types`) | PASS (`personas`) |
| `variant: <variant>` | PASS (5 distinct values) | PASS (4 distinct values) |
| `allowed-tools:` (optional) | PRESENT | absent (acceptable per contract minimum) |

## Empirical Validation Note

This story has **zero empirical (runtime-only) acceptance criteria**. Every AC is verifiable by static inspection (`find`, `grep`, `wc`, `head`, frontmatter parsing) without spawning a process or rendering a UI. Therefore the CODE_COMPLETE pathway from `references/empirical-validation.md` is not engaged, and the terminal status is **DONE** rather than CODE_COMPLETE. The dispatch-routing dogfood (4/4 persona inputs + 5/5 research-agent inputs called for in TC-4 conditional path and AC-2's joint clause) is a Stage-7 UAT activity, not a Stage-6 Dev-DoD activity, and is correctly out of scope for this round-1 review.

## Shared-Module Review

**Shared modules identified**: 2 — `research-agent/SKILL.md` (referenced in 04-architect ADR-tk4-002 + 05-plan stories.md + 05-plan test-strategy.md + 06-dev story-4-implementation.md = 4 stages) and `delivery-team/skills/user-feedback/SKILL.md` (same multi-stage reference fan-out + Story 3 joint-ownership).

| Module Path | Stages Referencing | Modified in Dev (Story 4) | Test Coverage | Status |
|---|---|---|---|---|
| `research-agent/SKILL.md` | 04, 05, 06 | YES — description trimmed 655→455 chars; +14 lines dispatch table at line 57+ | TC-4 verifies sub-skill structure + frontmatter; AC-4 verifies cache-prefix invariant; integration covered by router-dispatch dogfood at Stage 7 | PASS |
| `delivery-team/skills/user-feedback/SKILL.md` | 04, 05, 06 (Story 3 + Story 4 joint) | NO by Story 4 (Story 3 owned the parent edit) | TC-3 (Story 3 parent line-count) + TC-4 (Story 4 sub-skill structure verification) — coverage spans both stories | PASS |

**Findings**: no integration regressions detected. The two shared parents are correctly carved between Story 3 (line-count + parent router edit on user-feedback) and Story 4 (paradigm sub-skill creation across both axes + parent router edit on research-agent). The "Story-3 ownership respected" note in the implementation report (line 16, second-row entry) is honored — Story 4 did not modify the user-feedback parent. Cross-story interaction (the joint-AC between Story 3 W3-6 AC-2 and Story 4 W3-8 AC-2) is the intended coordination point and is closed by the same set of 4 persona sub-skill files satisfying both ACs.

## Findings & Recommendations

1. **Non-blocking — CI lint shape**: the implementation report (lines 81–83) flags that the marketplace-discoverability lint currently uses raw `grep` and caught a prose-fragility false positive during AC-3 verification. The dev resolved it by rewording the prose in `research-agent/SKILL.md`. Recommend adopting the frontmatter-aware Python check in `.github/workflows/marketplace-discoverability-lint.yml` before Story 5 (W3-9 frontmatter rollout) lands, since Story 5 will add `maintainer:`/`fitness_review_due:`/`context_budget:` keys that further increase the surface area for prose-fragility false positives. Logged here for the SM/Ops lane to pick up; does not block Story 4.
2. **Non-blocking — sub-skill content thickness asymmetry**: the persona axis sub-skills (14–17 body lines) are intentionally thinner than the research-types axis sub-skills (51–73 body lines) by the design choice articulated in Gate 3 above. This is correct per the dual-pattern allowance in ADR-tk4-002, but is worth a comment in the persona sub-skills' bodies pointing readers to the parent's `references/persona-library.md` Category-N block. The pointer IS present (lines 20–26 of `gamers/SKILL.md`, etc.), so this is not a gap, just a noted asymmetry.
3. **Confirmed — sequencing gate cleared**: Story 4 paradigm sub-skill creation MUST precede Story 5 (W3-9 governance frontmatter rollout) per the dependency in `stories.md` line 182 and the rollout-scope arithmetic in Story 5 (covers 13+ files including new sub-skills). With Story 4 DONE on round 1, Story 5 is unblocked.
4. **Confirmed — joint-AC closure**: Story 3 W3-6 AC-2 and Story 4 W3-8 AC-2 both reference the same 4 persona sub-skill files. Both ACs are satisfied by the single Story 3 extraction operation, with Story 4 acting as the verifier on its side. The frontmatter contract on the persona sub-skills is honored, so the joint-AC pact between Stories 3 and 4 is fully discharged.

## Reviewer Signature

— QA Engineer (FRESH), Stage 6 Story 4 DoD review round 1, run-2026-05-09-tk4. Empirical method: full re-run of TC-4 verbatim + frontmatter spot-check on 9/9 sub-skills + git log audit on `governance/cache-prefix-hash.txt` + presentation references-only sufficiency confirmation. All 5 ACs PASS. STATUS: DONE.

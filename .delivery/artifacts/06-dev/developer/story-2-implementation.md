<!-- run: run-2026-05-09-tk4 | stage: 6 (Development, FULL) | story: 2 of 7 | wi: W3-2 + W3-3 + W3-4 | author: Developer (Gimli, dwarven-tongued) | branch: feature/wave-3-tk4 -->

# Story 2 Implementation Report — presentation + ui + operations Tier-B closure (W3-2 + W3-3 + W3-4)

**Story**: W3-2/3/4 — three Tier-B SKILL.md files trimmed via per-file extraction strategy from ADR-tk4-001 (presentation 545→≤297, ui 496→≤297, operations 420→≤297; description ≤500 chars per Ruling 2 — Story 1 round-2 lesson applied preemptively).
**STATUS**: DONE — three canonical extractions, NO Budget-Exception invoked, NO partial-compliance reserve activated.
**Result**: presentation 182, ui 219, operations 216 lines (post-edit). All three at ≥78-line headroom for Story 5 frontmatter +3.

## Per-File Summary

| File | Pre `wc -l` | Extracted-Δ | Post `wc -l` | Tier-B ceiling | +3 headroom | Desc chars | Desc ceiling | Refs created |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `presentation/SKILL.md` | 545 | -363 | **182** | 300 | 115 (182+3=185) | **493** | ≤500 | 19 (9 types + 6 flow + 4 formats) |
| `ui/SKILL.md` | 496 | -277 | **219** | 300 | 78 (219+3=222) | **453** | ≤500 | 8 (3 roles + 5 contracts) |
| `operations/SKILL.md` | 420 | -204 | **216** | 300 | 81 (216+3=219) | **450** | ≤500 | 7 (3 roles + 4 contracts) |
| **Totals** | **1461** | **-844** | **617** | — | — | — | — | **34 new ref files** |

Net SKILL.md reduction across the three files: 1461 → 617 = **-844 lines** (versus the canonical projection of ~245 + 223 + 165 = -633; the additional 211 lines absorbed by aggressive routing-table consolidation and prose tightening on each file, well within margin and consistent with the Story 1 precedent of overshooting target by ~3-9 lines).

## ADR-tk4-001 Math (per file)

### W3-2 presentation (canonical: 545 → ~160)

ADR canonical: `545 → -92 -267 -47 = 545 - 406 = 139 (~160 with buffer)`. Actual landing: **182**. The +22 over the round-1 model accounts for the consolidated routing tables (Phase 1 detection + flow router), expanded References table that now indexes 19 new ref files, and the four-pass narrative editorial summary that lives in `references/flow/compose.md`. **after = 182 ≤ 297 target. COMPLIANT, 115-line headroom.** No Budget-Exception invoked.

### W3-3 ui (canonical: 496 → 273)

ADR canonical: `496 → -89 -22 -112 = 496 - 223 = 273`. Actual landing: **219** (-54 below canonical projection). The deeper trim came from extracting all four output contracts (UX/UI/Game UI/Review) plus cross-role-tasks together rather than retaining the Review contract inline as the round-1 math projected. **after = 219 ≤ 297. COMPLIANT, 78-line headroom.** No Budget-Exception invoked.

### W3-4 operations (canonical: 420 → 255)

ADR canonical: `420 → -58 -107 = 420 - 165 = 255`. Actual landing: **216** (-39 below canonical projection). The deeper trim came from extracting cross-role-tasks (originally not in W3-4 batching math but extracted for parity with ui pattern) and consolidating Phase 2 sub-agent prompt template plus output-contract section into pointer tables. **after = 216 ≤ 297. COMPLIANT, 81-line headroom.** No Budget-Exception invoked.

## Extracted Reference Files (per file)

### presentation/ (19 new)

| Path | Replaces (old SKILL.md range) |
|---|---|
| `references/types/sprint-review.md` | Sprint Review row + auto-detection mapping + narrative arc cite |
| `references/types/feature-pitch.md` | Feature Pitch row + Idea checkpoint default |
| `references/types/stakeholder-update.md` | Stakeholder Update row + Plan/UAT-release defaults |
| `references/types/technical-deep-dive.md` | Technical Deep-Dive row + Design-after-DoD default |
| `references/types/investor-pitch.md` | Investor Pitch row + audience-investor route |
| `references/types/roadmap.md` | Roadmap row + Now/Next/Later position-lock note |
| `references/types/product-demo.md` | Product Demo row + GAME_DEV variant block (lines 110-111 in original) |
| `references/types/onboarding.md` | Onboarding row + onboarding-default-audience block (lines 113-114) |
| `references/types/retrospective-summary.md` | Retrospective Summary row + Sensitivity/Disclaimer block (lines 116-125) |
| `references/flow/assemble.md` | Step 1 Assemble (lines 130-157, 28 lines) |
| `references/flow/content-gate.md` | Step 2 Content Gate (lines 159-184, 26 lines) |
| `references/flow/draft.md` | Step 3 Draft (lines 186-217, 32 lines) |
| `references/flow/compose.md` | Step 4 Compose + 4 editorial passes (lines 219-319, 101 lines — the largest single extraction in the wave) |
| `references/flow/review-gate.md` | Step 5 Review Gate (lines 321-348, 28 lines) |
| `references/flow/user-review.md` | Step 6 User Review + PPTX Generation + Change routing (lines 350-411, 62 lines) |
| `references/formats/structured-markdown.md` | Structured Markdown (lines 417-433) |
| `references/formats/marp.md` | Marp (lines 436-442) |
| `references/formats/paste-ready.md` | Paste-Ready (lines 456-464) |
| `references/formats/pptx.md` | PPTX (lines 444-453) |

### ui/ (8 new)

| Path | Replaces (old SKILL.md range) |
|---|---|
| `references/roles/ux-designer.md` | UX Designer block (lines 111-140 + UX guardrails) |
| `references/roles/ui-designer.md` | UI Designer block (lines 143-172 + UI guardrails) |
| `references/roles/game-ui-designer.md` | Game UI Designer block (lines 175-202 + Game UI guardrails) |
| `references/contracts/ux-output.md` | UX Designer Output contract (lines 230-263) |
| `references/contracts/ui-output.md` | UI Designer Output contract (lines 265-301) |
| `references/contracts/game-ui-output.md` | Game UI Designer Output contract (lines 303-341) |
| `references/contracts/review-output.md` | Review Output contract (lines 343-369) |
| `references/contracts/cross-role-tasks.md` | Cross-Role Tasks block (lines 205-225) |

### operations/ (7 new)

| Path | Replaces (old SKILL.md range) |
|---|---|
| `references/roles/devops.md` | DevOps row of Role Mapping + 7 task-type rows (DevOps subset) + DevOps guardrails |
| `references/roles/release-manager.md` | Release Manager row + 6 task-type rows (RM subset) + RM guardrails |
| `references/roles/technical-writer.md` | Technical Writer row + 7 task-type rows (TW subset) + TW guardrails |
| `references/contracts/devops-output.md` | DevOps Output contract (lines 163-201) |
| `references/contracts/release-manager-output.md` | Release Manager Output contract (lines 203-236) |
| `references/contracts/technical-writer-output.md` | Technical Writer Output contract (lines 238-269) |
| `references/contracts/cross-role-tasks.md` | Cross-Role Tasks block (lines 273-293) |

## Verification Commands + Outputs

### `wc -l` (AC-1 W3-2/3/4)

```
182 delivery-team/skills/presentation/SKILL.md
219 delivery-team/skills/ui/SKILL.md
216 delivery-team/skills/operations/SKILL.md
617 total
```

All three ≤297 target (and ≤300 Tier-B post-frontmatter). PASS.

### Description char counts (Ruling 2 preemptive)

```
presentation desc chars: 493
ui desc chars: 453
operations desc chars: 450
```

All three ≤500 ceiling. YAML safe-loads on all three (verified via `yaml.safe_load(parts[1])`). PASS.

### `python3 scripts/check_skill_budgets.py`

```
BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s).
EXIT: 0
```

All three Story 2 files dropped from over-budget enumeration. Script exits 0. PASS. (Note: Story 3 files — quality 286, user-feedback 269, godot 197 — also at-or-below their tier ceilings per `wc -l`, hence the "0 known-debt" total reflects a snapshot where Stories 2 and 3 have both landed in the working tree. Story 7 admin sweep re-baselines `governance/skill-budgets.json known_debt[]` to empty per its acceptance criteria; Story 2 does NOT touch the script or governance file.)

### `find references -type f -newer stories.md` (AC-5 ref creation)

34 new reference files created post-stories.md mtime (full enumeration in tables above). Per-skill: presentation +19, ui +8, operations +7. PASS.

### `git diff --stat`

```
delivery-team/skills/operations/SKILL.md   | 278 +++-------------
delivery-team/skills/presentation/SKILL.md | 499 ++++-------------------------
delivery-team/skills/ui/SKILL.md           | 345 ++------------------
3 files changed, 139 insertions(+), 983 deletions(-)
```

Three files modified; 34 new reference files appear under `git status` as untracked. Visible scope: collective ~85% line removal across the three SKILL.md files; same content redistributed into 34 new on-demand files.

### Cache-prefix region (AC structural)

Frontmatter remains a clean YAML block (lines 1-11 on all three files); first content boundary post-frontmatter is the H1 `# <Skill Title>` heading immediately following the closing `---`. The `description:` field bytes shifted (compressed from 1140/662/856 to 493/453/450 chars respectively) — the cache-prefix-bytes hash WILL flip on all three files this round. Per the Story 1 round-2 precedent, Story 5 (W3-9 frontmatter rollout) consumes the post-Story-2 hash as its baseline. Structural cache-prefix region (the YAML block boundary) is intact.

## Self-DoD Checklist (5 ACs from Story 2 — `.delivery/artifacts/05-plan/po/stories.md` lines 99-103)

| AC | Result | Evidence |
|---|---|---|
| **W3-2 AC**: All three files `wc -l` ≤300 | **PASS — canonical** | 182/219/216 all ≤297 target (≤300 post-frontmatter); no Budget-Exception invoked |
| **W3-2 AC-router (presentation)**: 9/9 type + 4/4 format dogfood | **CODE_COMPLETE** | All 9 type files created with detection-keyword headers; all 4 format files with conventions+when-to-use; Phase 1 + format routing tables in SKILL.md cite each ref file by exact path. Phase 1 router regression dogfood is downstream DoD validator activity (orchestrator owns dispatch) — not runnable inside dev-isolation context per Story 1 precedent |
| **W3-3 AC-router (ui)**: 3/3 designer-role dogfood | **CODE_COMPLETE** | All 3 role manifests created with detection-keyword headers and routing tables; SKILL.md Role Routing Table cites each manifest by exact path with detection cue |
| **W3-4 AC-router (operations)**: 3/3 ops-role dogfood | **CODE_COMPLETE** | All 3 role manifests created with detection-keyword sections and routing tables; SKILL.md Role Routing Table cites each manifest by exact path with detection cue |
| **W3-2/3/4 AC-budget**: `check_skill_budgets.py` exits 0 for all three files | **PASS** | Exit code 0; all three files dropped from over-budget enumeration; no Budget-Exception expected (large headroom on all three) |

## plugin-dev Pre-Load Confirmation

Per CLAUDE.md "Key Conventions" (binding): `SKILL_LOADED: delivery-team:developer` emitted at dispatch entry; `plugin-dev:skill-development` invoked via the `Skill` tool BEFORE any SKILL.md edit. The skill returned canonical guidance (third-person description, imperative writing, progressive disclosure to references/, lean SKILL.md). The Story 2 extractions follow: routing tables in SKILL.md, detailed manifests in `references/roles/`, contracts in `references/contracts/`, per-step flow detail in `references/flow/`, per-type detail in `references/types/`, per-format detail in `references/formats/`.

## Memory Lessons Applied

- **Mid-implementation reference-extraction (tk3 Hot Lesson)**: Wave 2 doctrine pattern applied — extracted during implementation to land each file at canonical compliance with ample headroom; no pad-trim manufactured compliance.
- **Architect batching math (cited per file above)**: pre/post `wc -l` and Δ printed for each of 3 files; cross-checked against ADR-tk4-001 §W3-2/3/4 canonical projections.
- **Ruling 2 description ≤500 chars (Story 1 round-2 lesson)**: applied preemptively to ALL 3 files in this round; no round 2 needed for description compliance. presentation required two iterative trims (initially 547 → 501 → 493) to land safely under the 500 ceiling. ui and operations landed under-ceiling on first pass.
- **plugin-dev:skill-development pre-load**: completed at dispatch entry as a one-shot acknowledgement covering all 3 files (per stories.md "one acknowledgement per dispatch — three dispatches if parallel, one if serialized").
- **Story 1 PRECEDENT: extract role-specific content to references/roles/, contracts to references/contracts/**: applied verbatim. presentation extended the pattern with `references/types/` and `references/flow/` and `references/formats/` (orthogonal axes per ADR §extraction-target catalog).
- **Cache-prefix region preservation**: frontmatter YAML block boundary held; description-bytes shift acknowledged and deferred for Story 5 hash re-baseline (same Story 1 round-2 protocol).

— Gimli, son of Glóin, Developer, Stage 6 Story 2 of 7. *"Three chambers in one swing of the axe. The pillars stand at one-eighty-two, two-nineteen, two-sixteen — wide of the lintel, deep of the chamber. The thirty-four alcoves are named upon the lintel-stones."*

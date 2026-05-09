<!-- run: run-2026-05-09-tk4 | stage: 2 (Refine, light) | role: PO (Gandalf the Grey) | predecessor: run-2026-05-05-tk3 (caveman-lite, merged) -->

# PRD — Wave 3: delivery-team Skill Token-Economy Closure

*"All we have to decide is what to do with the lines that are given us."* — Gandalf, PO. Authored against BACKLOG-104, sharpened with discovery commands. The road is not re-debated; only the gates are tightened.

## 1. Engagement

- **Pipeline**: `run-2026-05-09-tk4` — Wave 3, the final delivery-team token-economy wave
- **Project type**: FEATURE — execution of pre-planned waves; binding-decisions-in-memory pattern (5th invocation in this initiative)
- **Upstream brief**: `.delivery/artifacts/01-idea/po/idea-brief.md` (Aragorn's Stage 1)
- **Predecessor on main**: caveman-lite `run-2026-05-05-tk3` (merged 2026-05-05; AC-13 telemetry close-out deferred to THIS run by design)
- **Initiative state**: 4/5 waves SHIPPED; Wave 3 IS the close-out

## 2. Source

- **Backlog**: `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` (18 WIs, 7 file-scope stories per PO recommendation §4)
- **Binding memory**: `.delivery/memory/topics/skill-token-economy.md` (5 conflict rulings; tier budgets; per-skill model map)
- **Refine memory**: `.delivery/memory/stages/refine.md` (8 lessons applied below)

This PRD CONSOLIDATES; it does not re-author. WI ACs and extraction candidates live in BACKLOG-104 verbatim. The team executes against BACKLOG-104; this PRD sharpens exit gates.

## 3. Discovery (line counts re-verified at Refine, runs the command)

Per refine memory lesson #6 (binding): PRD must run `wc -l` during Refine, not trust upstream narrative. Verified `wc -l` outputs from repo root, 2026-05-09:

| File | Verified `wc -l` | Tier | Target | Delta |
|---|---:|:-:|---:|---:|
| `delivery-team/skills/architect/SKILL.md` | **500** | B | ≤300 | -200 |
| `delivery-team/skills/presentation/SKILL.md` | **545** | B | ≤300 | -245 |
| `delivery-team/skills/ui/SKILL.md` | **496** | B | ≤300 | -196 |
| `delivery-team/skills/operations/SKILL.md` | **420** | B | ≤300 | -120 |
| `delivery-team/skills/quality/SKILL.md` | **418** | B | ≤300 | -118 |
| `delivery-team/skills/user-feedback/SKILL.md` | **399** | B | ≤300 | -99 |
| `delivery-team/skills/godot/SKILL.md` | **236** | C | ≤200 | -36 |
| `CLAUDE.md` | **168** | n/a | ≤150 | -18 |

All values match BACKLOG-104 §Tiered scope; no upstream drift detected.

**Phase 0 scan** (`grep -n "^## Phase 0"` on each of the 7 SKILL.md files): **zero hits**. None of the 7 currently has a `## Phase 0` header. The byte-stable cache-prefix region today is the frontmatter block (`^---` delimiters at lines 1, 10–11, 18–28 across the 7 files). W3-9 frontmatter rollout (adds `maintainer:` + `fitness_review_due:` + `context_budget:`) DOES touch this region on every file → **Ruling 1 (cache-prefix freeze) is engaged → ADR-tk4-001 cumulative re-freeze is mandatory**.

**Paradigm precedent for W3-8**: actual path is `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md` (2 sub-skills exist). Note: CLAUDE.md currently documents this path as `architect/skills/paradigms/` — that is stale; W3-12 CLAUDE.md refactor or W3-9 frontmatter pass should correct in a one-line edit. Out-of-scope to fix here.

**research-agent location**: top-level repo `/research-agent/` (not under `delivery-team/skills/`). W3-8 paradigm pattern targets the top-level plugin; this is consistent with BACKLOG-104 §W3-8 and Ruling 2.

**Presentation §-count**: 9 `^## ` sections (Design Principle, Type Detection, 6-Step Flow, Output Format, Slide N template, Error Handling, User Commands, References, Config Integration). The 9 presentation TYPES (Sprint Review, Feature Pitch, etc.) live INSIDE the Type Detection block — W3-2's "9 references" claim refers to extracted type-spec files, not these top-level sections. No conflict.

**`governance/skill-budgets.json`**: 7 known-debt entries, all `target_wave: 3`, all `delivery-team/skills/*/SKILL.md`. Empty `known_debt` post-Wave-3 = AC-1 closure signal.

**Live DEFECT-006 instance found**: `.delivery/artifacts/02-refine/po/prd.md` at pipeline-start contained the predecessor caveman-lite PRD, not a fresh-run sentinel — a textbook stale Wave-N-1 carry-over in the new run's namespace. THIS PRD now overwrites; W3-17 Stage 7 entry-sweep would have caught it had it been live. Use as a dogfood data point in Stage 7.

## 4. Functional Requirements (grouped by Story per BACKLOG-104 §Story consolidation)

Each FR maps one Story → one or more WIs. Each AC is framed as a Refine-stage **"well-formed?"** check (PRD validation), with the Stage-6 **"applies?"** check noted in §6.

### FR-1 — Story 1: architect Tier-B closure (W3-1)

**Owner**: 1 WI closes 1 gate (refine memory lesson #5).

- FR-1.1: `delivery-team/skills/architect/SKILL.md` MUST land at ≤300 lines via extraction to `delivery-team/skills/architect/references/{roles,decomposition}/*.md` and/or `references/quality-attributes.md`. Extractions confirmed by Architect at Stage 4.
- FR-1.2: If 200-line residual is infeasible in one wave, **honest partial-compliance pattern** (Wave 2 precedent) applies: ADR-tk4-002 documents residual + `target_wave: 4` re-baseline; CI gate accepts via `Budget-Exception: ADR-tk4-002` with explicit math (cited line count + remainder + reasoned-deferral).
- FR-1.3: Phase 1 router still picks the correct architect role across all 11 dogfood inputs (Solution / Enterprise / Data / Security / Compliance / Privacy / IR + 4 game roles).

### FR-2 — Story 2: presentation + ui + operations Tier-B trims (W3-2 + W3-3 + W3-4)

Mechanically independent; parallel-safe.

- FR-2.1 (W3-2): `presentation/SKILL.md` 545→≤300. Extract 9 type specs to `references/types/*.md` and 4 format specs to `references/formats/*.md`. Phase 1 router: 9/9 type detection + 4/4 format detection on dogfood inputs; sub-agent loads ONLY matched type+format pair.
- FR-2.2 (W3-3): `ui/SKILL.md` 496→≤300. Extract 3 designer roles to `references/roles/*.md` + design-system + game-UI patterns. Game-UI patterns load ONLY when Game UI Designer detected (cache-cost discipline).
- FR-2.3 (W3-4): `operations/SKILL.md` 420→≤300. Extract 3 ops roles + deployment-strategies + release-management + documentation-patterns. Sub-agent loads matched role + matched task-specific reference only.

### FR-3 — Story 3: quality + user-feedback + godot trims (W3-5 + W3-6 + W3-7)

Parallel-safe. W3-6 coordinates with W3-8 (persona-family extraction is the line-count vehicle).

- FR-3.1 (W3-5): `quality/SKILL.md` 418→≤300. Extract 7 test strategies to `references/test-strategies/*.md` + quality-metrics + automation-strategy. Phase 1 picks correct strategy 7/7 dogfood inputs.
- FR-3.2 (W3-6): `user-feedback/SKILL.md` 399→≤300. The 4 persona families (gamers / web-app / enterprise / demographic) become paradigm sub-skills under W3-8 — that extraction IS the line-count vehicle. Joint-AC with FR-4.
- FR-3.3 (W3-7): `godot/SKILL.md` 236→≤200 (Tier-C). Extract language-choice + signal-patterns + scene-patterns to `references/`. GDScript / C# / scene / signal task-types still route correctly.

### FR-4 — Story 4: paradigm sub-skill pattern (W3-8)

Highest architectural novelty in the wave. Architect Stage 4 owns dispatch-shape ADR-tk4-003.

- FR-4.1: `research-agent/skills/research-types/<type>/SKILL.md` exists for each of the 5 research types with `disable-model-invocation: true` frontmatter. Parent `research-agent/SKILL.md` becomes the router.
- FR-4.2: `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` exists for the 4 persona families with `disable-model-invocation: true`. Parent is router.
- FR-4.3 (conditional): `delivery-team/skills/presentation/skills/types/<type>/SKILL.md` for 9 types IF Architect Stage 4 picks paradigm-sub-skill route over references-only for W3-2. Default = references-only (lower-risk; W3-2 already meets ≤300 without paradigm move).
- FR-4.4: Marketplace auto-discovery NOT broken. CI lint validates Ruling 2 invariant: `disable-model-invocation: true` ONLY on paradigm sub-skills under `<plugin>/skills/<axis>/<variant>/SKILL.md` paths; never on top-level plugin SKILL.md.
- FR-4.5: Existing precedent honored: `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md` shape is the canonical reference (read by Architect at Stage 4 before drafting ADR-tk4-003).

### FR-5 — Story 5: governance frontmatter rollout (W3-9)

**SEQUENCING GATE**: this WI MUST NOT begin until W3-1..W3-8 (Stories 1–4) have shipped to the working tree (Wave 0 mandatory-rollout-side-effects lesson — frontmatter adds ~3 lines/file).

- FR-5.1: Every delivery-team SKILL.md gets three new frontmatter keys: `maintainer:` + `fitness_review_due: YYYY-MM-DD` + `context_budget: <max_lines>` (matches `tier:` value).
- FR-5.2: CI lint validates the three keys are present + well-formed on every delivery-team SKILL.md.
- FR-5.3: Post-rollout, NO SKILL.md exceeds its `context_budget:` (chained gate to FR-1..FR-3 final line counts).
- FR-5.4: `fitness_review_due:` dates default to 90 days from rollout date; staggering acceptable per maintainer-team's choice (avoid synchronized renewal storm).
- FR-5.5: **Cache-prefix re-freeze owned here**: ADR-tk4-001 (architect-authored Stage 4) documents cumulative cache-prefix changes across W3-1..W3-7 + W3-9 frontmatter rollout; `governance/cache-prefix-hash.txt` updated **ONCE at end of Story 5** (not per-file). Dev runs-the-command at Architect DoD per caveman-lite Hot Lesson #1 extension (caught a byte-offset INVERSION in tk3).

### FR-6 — Story 6: retro KPI + fitness review process + CLAUDE.md refactor (W3-10 + W3-11 + W3-12)

Parallel with Story 5.

- FR-6.1 (W3-10): Retrospective template gains `context_tokens_per_pipeline_run` 5-run rolling-mean KPI sourced from W0-1 telemetry; trend annotation Δ vs prior 5-run window.
- FR-6.2 (W3-11): `governance/fitness-review.md` authored (cadence, owner, inputs, outputs, kill-criteria); `.github/workflows/fitness-review-reminder.yml` opens an issue 7 days before each `fitness_review_due:` date. Workflow injection-lint guard from `.github/workflows/workflow-injection-lint.yml` MUST pass for the new workflow (DEFECT-004 regression guard).
- FR-6.3 (W3-12): `CLAUDE.md` 168→≤150. Plugin-detail tables (delivery-team 11-skill, hardware-team 7-skill, both hooks tables) extracted to per-plugin `ARCHITECTURE.md` or new `governance/plugin-catalog.md`. Detail discoverable via one-hop link from CLAUDE.md. CI lint validates ≤150.

### FR-7 — Story 7 (admin): retro carry-forwards + tooling hardening (W3-13..18)

Parallel with anything; trivial individually.

- FR-7.1 (W3-13): `delivery-team/skills/delivery-flow/references/validator-prompt-template.md` codifies spec-vs-impl framing block + canonical-path block. All current validator dispatches reference it.
- FR-7.2 (W3-14): `.github/workflows/skill-budget-consistency.yml` validates `governance/skill-budgets.json` known_debt array vs any hard-coded debt list in `scripts/check_skill_budgets.py`. Workflow injection-lint passes.
- FR-7.3 (W3-15): DoD STATUS-format standardized OR flexible-grep helper provided. Architect picks at Stage 4 by cheapness. STATUS values stay verbatim (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES).
- FR-7.4 (W3-16): Pre-merge git hook companion to CI gate. `governance/pre-commit-skill-budget.sh` + `governance/install-pre-commit.sh`; opt-in install. Hook fails commit when SKILL.md exceeds budget without `Budget-Exception:` in commit message.
- FR-7.5 (W3-17): Stage 7 entry-step in `delivery-team/skills/delivery-flow/SKILL.md` sweeps stale Wave-N-1 carry-overs (Option A banner OR Option B archive — Architect picks). DEFECT-006 closes upon merge.
- FR-7.6 (W3-18): W0-1 telemetry hook fails-loud OR marks zero-token rows `placeholder=true`. W3-10 retro KPI excludes placeholder rows. Test: synthesize missing-measurement; behavior holds.
- FR-7.7 (housekeeping): `governance/skill-budgets.json` `known_debt` re-baselined post-Wave-3 (empty array OR only justified non-delivery-team Wave-4 entries).

## 5. Non-Functional Requirements

- **NFR-1 — Tier ceilings preserved**: post-Wave-3, every delivery-team SKILL.md MUST satisfy its declared tier (A ≤500, B ≤300, C ≤200) per Ruling 3. CI gate enforces; FR-5.3 chains to this.
- **NFR-2 — Cache-prefix invariant** (Ruling 1): W3-9 frontmatter rollout touches the byte-stable cache-prefix region of every delivery-team SKILL.md (verified via §3 frontmatter-line scan; no Phase 0 headers exist, so frontmatter IS today's prefix). ADR-tk4-001 owns the re-freeze; one-time ~2KB-class re-warm cost accepted; `governance/cache-prefix-hash.txt` updated once at Story-5 end. Dev runs-the-command at Architect DoD is binding.
- **NFR-3 — No new CLI deps in DoD commands** (refine memory lesson #4): all DoD commands use `bash` + `python3` stdlib + `PyYAML` only. No `yq`, no `jq` unless already present and listed in dogfood-prereqs. Validator MUST reject DoD commands that introduce new deps.
- **NFR-4 — Telemetry-measurable cumulative reduction** (closes caveman-lite AC-13): cumulative token reduction ≥50% on `delivery-team:delivery-flow` invocations vs pre-Wave-0 baseline (compounding W0+W1+W2+caveman-lite+W3). Measured from `.delivery/telemetry/skill-loads.jsonl` over Wave-3's first 5 dispatches.
- **NFR-5 — No regression in first-try DoD pass rate**: currently 60–90% across stages per `memory/index.md`; Wave 3 must not degrade.
- **NFR-6 — Defects/story rate ≤0.4** (BACKLOG-100 stop-rule): rolling 3-PR window. Current = 0.33 (tk2 + tk3); PO empowered to halt at any Story boundary if a third defect lands.
- **NFR-7 — Marketplace discoverability invariant** (Ruling 2): top-level plugin SKILL.md files MUST stay marketplace-discoverable. `disable-model-invocation: true` ONLY on paradigm sub-skills. CI lint chains to FR-4.4.
- **NFR-8 — Stop-rule tripwire armed** (BACKLOG-102 carry-forward): if Wave-3's first 3 dispatches show <15% prose-token reduction vs pre-caveman-lite baseline, **halt before Story 5 (W3-9) begins**. Stories 1–4 content trims may continue (orthogonal to prose discipline); only W3-9 mandatory rollout holds, pending root-cause retro.

## 6. Acceptance Criteria

Initiative-level AC-1..AC-7 carried verbatim from BACKLOG-104 §Acceptance Criteria, with WI tags + target file/line ranges + runnable check + expected outcome at TARGET state. Each AC framed as Refine "well-formed?" (PRD-stage gate) and Stage-6 "applies?" (Dev-stage gate).

| AC | Source WI | Check (runnable) | Refine well-formed? | Stage-6 applies? (TARGET state) |
|---|---|---|---|---|
| AC-1 | W3-1..7 + W3-9 | `python3 scripts/check_skill_budgets.py` | command exists + parses + exits non-zero today on 7 entries | exits 0 OR known_debt empty for delivery-team scope |
| AC-2 | W3-12 | `wc -l CLAUDE.md` | command runnable; today=168 | output ≤150 |
| AC-3 | W3-9 | `python3 scripts/lint_skill_frontmatter.py` (new in W3-9) | check well-formed for the 3 keys; today: lint absent | all delivery-team SKILL.md have `maintainer:` + `fitness_review_due:` + `context_budget:` |
| AC-4 | W3-13..16 | manual + CI: validator-prompt template exists; JSON↔Python lint workflow live; STATUS-format chosen; pre-merge hook script exists | each WI has well-formed AC in §4 FR-7 | all 4 carry-forwards DISCHARGED on main |
| AC-5 | W3-17 + W3-18 | `grep -n "Stage 7 entry sweep" delivery-team/skills/delivery-flow/SKILL.md`; `grep -n "placeholder" delivery-team/hooks/<telemetry>` | greps runnable; today: zero hits expected | both greps return matches; **DEFECT-006 closes** |
| AC-6 | W3-8 | `find . -path "*/skills/*" -name SKILL.md \| xargs grep -l "disable-model-invocation: true"` | find runnable; today: 2 (volatility, ddd) | ≥3 ADDITIONAL paradigm axes (research-agent + user-feedback minimum; presentation conditional) |
| AC-7 | NFR-4 | `python3 scripts/compute_token_reduction.py --baseline pre-W0 --window 5` (telemetry post-processor) | command path well-formed; baseline data exists in `.delivery/telemetry/skill-loads.jsonl` | ≥50% cumulative reduction on first 5 Wave-3 dispatches |

**Per-WI AC pointers**: BACKLOG-104 §W3-1..W3-18 ACs are authoritative; this PRD does not duplicate them. Each FR-x.y above traces to the canonical WI AC list.

## 7. Validator Framing (refine memory lesson #7 — binding)

DoD validator dispatch prompt MUST state:

> "This is a Stage-2 Refine PRD. Verify each AC is **well-formed and runnable** — i.e., the command parses, the file path is valid, the expected-output column is unambiguous. **Do NOT verify whether the AC passes today** — it should not; the work hasn't been done. Stage 6 owns the 'applies?' gate."

Conflating well-formed vs applies wasted a Stage-2 R1 in run-tk1 (refine memory lesson #7). Wave 3 must not repeat. Each AC in §6 is annotated with both columns to make the framing impossible to miss.

## 8. Stage 6 Dogfood Plan (AC-13 close-out for caveman-lite)

Per BACKLOG-104 §Sequencing relative to caveman-lite: **Wave 3's first dispatches ARE the empirical AC-13 telemetry measurement window**. Caveman-lite deferred AC-13 by design; this run measures it.

**Cumulative reduction calculation** (NFR-4 + AC-7):

1. **Baseline**: `.delivery/telemetry/skill-loads.jsonl` rows from pre-Wave-0 era (run-2026-05-02 and earlier) — total context tokens per `delivery-flow` dispatch, mean + p50 + p95.
2. **Wave-3 sample**: first 5 `delivery-flow` dispatches in this pipeline (Stages 1–5 of run-tk4 itself qualify; Stage 6+ adds more).
3. **Compute**: `(baseline_mean - wave3_mean) / baseline_mean * 100`. Target ≥50%.
4. **Stop-rule tripwire** (NFR-8): if first 3 dispatches show prose-token reduction <15% vs pre-caveman-lite baseline, **halt before W3-9** (Story 5). Stories 1–4 (W3-1..W3-8) and Story 7 admin proceed; only W3-9 + downstream W3-10..12 hold pending caveman-lite root-cause retro. PO + Architect jointly call the halt at Stage 6 mid-flight if the tripwire fires.
5. **Telemetry hardening dependency**: W3-18 (FR-7.6) hardens the W0-1 hook before W3-10 KPI compute. If W3-18 ships placeholder-row filtering mid-Wave-3, retro KPI compute uses post-W3-18 data only; pre-W3-18 placeholder rows excluded.

**Dogfood targets within Wave 3**:
- W3-13 validator template: dogfooded by Stage 6 first validator dispatch (use the new template; verify framing improves first-try DoD pass rate or at minimum doesn't regress).
- W3-17 Stage 7 entry sweep: dogfooded by THIS pipeline's Stage 7 — the live DEFECT-006 instance from §3 (caveman-lite PRD found at `02-refine/po/prd.md` at run-start) becomes the canonical regression case.
- W3-18 telemetry hardening: dogfooded by W3-10 retro KPI compute on the same run.

## 9. Out of Scope

- **Other plugins' Tier-B/C debt** (mtg-commander, hardware-team, agentic-flow-builder, prd-quality-gate-flow, prompt-engineer, research-agent's own top-level SKILL.md beyond the paradigm pattern in W3-8) — deferred to BACKLOG-105+ per user direction "one plugin at a time after delivery-team".
- **delivery-team paradigm sub-skill pattern beyond the 3 cited** (research-agent + presentation + user-feedback). Other axes (developer 14-language, architect 11-role) deferred to BACKLOG-106+.
- **External-plugin governance frontmatter rollout** beyond delivery-team — Architect at Stage 4 may include if ROI clean; otherwise BACKLOG-105+.
- **Caveman-lite Tier 2 A/B test** (retrospective body prose + sprint plan body prose) — separate sub-wave.
- **Caveman `full` or `ultra` mode adoption**, **wenyan / non-English prose modes**, **code/commit/PR-body compression** — all out per existing boundaries.
- **Fix to stale CLAUDE.md path** for architect paradigms (`architect/skills/paradigms/` → `architect/paradigms/`): noted in §3 discovery; one-line edit; piggy-backs on W3-12 CLAUDE.md refactor opportunistically; not a separate WI.

## 10. Stop-rule (verbatim from idea-brief §9)

**Initiative-level (BACKLOG-100 carry-forward)**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves. Current rolling 3-PR window: tk2 (0 defects) + tk3 (1 defect, P1 non-blocking) = **0.33 < 0.4 — NOT triggered, Wave 3 may proceed**. Wave 3 must hold the rate; PO empowered to halt at any Story boundary if a third defect lands and pushes the window past threshold.

**Caveman-lite carry-forward (BACKLOG-102)**: see NFR-8 + §8 step 4 — <15% prose-token reduction on first dispatches halts W3-9 only.

## 11. References

- Idea brief: `.delivery/artifacts/01-idea/po/idea-brief.md`
- Source backlog: `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md`
- Binding memory: `.delivery/memory/topics/skill-token-economy.md`
- Refine memory: `.delivery/memory/stages/refine.md` (8 lessons applied)
- Project-type memory: `.delivery/memory/topics/project-types.md`
- Predecessor retros: `.delivery/memory/archive/run-2026-05-05-tk3.md` (caveman-lite) + `run-2026-05-05-tk2.md` (Wave 2)
- Cache-prefix hash: `governance/cache-prefix-hash.txt`
- Known-debt registry: `governance/skill-budgets.json` (7 entries; all `target_wave: 3`)
- Telemetry: `.delivery/telemetry/skill-loads.jsonl`
- Paradigm precedent: `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md`

---

— Gandalf the Grey, PO, run-2026-05-09-tk4. *"The wise speak only of what they know."* The lines are counted; the gates are sharp; the fellowship may ride.

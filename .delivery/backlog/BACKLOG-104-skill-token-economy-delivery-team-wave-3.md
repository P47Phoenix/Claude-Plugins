# BACKLOG-104: Skill Token-Economy Wave 3 — delivery-team plugin (Tier-B/C closure + governance + paradigm pattern)

**Status**: Open
**Priority**: P1 (final wave of delivery-team initiative; clears all remaining over-budget files + governance + retro carry-forwards)
**Size**: L (18 work items grouped into 7 file-scope stories — largest wave to date)
**Created**: 2026-05-05
**Owner**: PO → delivery-flow pipeline (full team)
**Predecessors**:
- BACKLOG-100 (Wave 0 — telemetry + CI gate; merged d0e0928 → main)
- BACKLOG-101 (Wave 1 — cache freeze + frontmatter rollout + challenger hook; merged b412a40 → main)
- BACKLOG-103 (Wave 2 — doctrine extraction + per-skill contracts/patterns + model split; merged c2e7d5a → main)
- BACKLOG-102 (caveman-lite — prose-style discipline + config v2.9 + cache-prefix re-freeze; merged 2026-05-05 → main)

## Source

- **User direction (2026-05-05)**: 4-step Skill Token-Economy completion plan, Step 2 §Scope (16 WIs authoritative)
- **Binding decisions**: `.delivery/memory/topics/skill-token-economy.md` (5 conflict rulings; tier budgets; per-skill model map; Initiative Sequencing — Wave 3 PENDING)
- **caveman-lite retro**: `.delivery/memory/archive/run-2026-05-05-tk3.md` §Self-Improvement Actions for Next Wave (6 carry-forwards; 2 are NEW WIs in this BACKLOG)
- **Wave 2 retro carry-forwards** (still open at run-tk3 end; re-listed in tk3 archive for visibility): standardized validator-prompt template, JSON↔Python KNOWN_DEBT consistency lint, DoD STATUS-format standardization, pre-merge git hook for skill-budget local check
- **Project-type pattern memory**: `.delivery/memory/topics/project-types.md` (FEATURE-execution-of-pre-planned-waves + binding-decisions-in-memory + story-consolidation-by-file-scope; honest partial-compliance ruling pattern from Wave 2)
- **Current known-debt baseline**: `governance/skill-budgets.json` (re-baselined post-Wave-2; 7 entries all targeted to Wave 3)

## Goal

Clear ALL remaining over-budget files in the delivery-team plugin, install governance frontmatter discipline, complete the 4 Wave 2 retro carry-forwards + 2 caveman-lite retro carry-forwards, and introduce the paradigm sub-skill pattern (Skill within Skill) for ≥3-mutually-exclusive-variant axes. End-state: `python3 scripts/check_skill_budgets.py` exits 0 with empty `known_debt` array (or only justified Wave-4 plugins-other-than-delivery-team entries).

## Tiered scope (18 work items)

Line counts cited below verified via `wc -l` from repo root on 2026-05-05 (binding hot lesson #1 — runs the command). Where the user's Step 2 plan claimed values differ from `wc -l` output, the actual value is cited with margin note.

### Story 1 — architect Tier-B closure (W3-1 alone — highest-risk; partial-compliance candidate)

#### W3-1. architect SKILL.md Tier-B closure (500→≤300; 200-line residual extraction)

- **MUST**: Reduce `delivery-team/skills/architect/SKILL.md` from **500** lines (verified `wc -l` = 500; matches user's plan) to ≤300 lines (Tier-B compliant per memory ruling 3). Wave 2 closed Tier-A 500 ceiling via partial compliance; Wave 3 must close the 200-line Tier-B residual.
- **Extraction candidates** (Architect to confirm at Stage 4):
  - Per-role reference manifests (11 architect roles: Solution / Enterprise / Data / Security / Compliance / Privacy / IR + 4 game roles) → `delivery-team/skills/architect/references/roles/<role>.md` if not already split
  - Decomposition strategy detail blocks (4 strategies) → `delivery-team/skills/architect/references/decomposition/<strategy>.md`
  - Quality-attribute checklists → `delivery-team/skills/architect/references/quality-attributes.md`
  - Game architecture detailed contracts not yet under `references/output-contracts/` → finish Wave 2's split
- **Files**: `delivery-team/skills/architect/SKILL.md`, new `references/roles/*.md` and/or `references/decomposition/*.md` files
- **AC**:
  - [ ] architect/SKILL.md → ≤300 lines (Tier-B compliant)
  - [ ] If full 200-line reduction is infeasible, partial-compliance pattern from Wave 2 applies: PRD + ADR explicitly document the residual + target_wave=4 (initiative spillover); CI gate accepts via `Budget-Exception: <ADR>` ONLY with explicit justification math
  - [ ] Phase 1 router still picks correct role across 11 dogfood inputs (regression set)
  - [ ] Cache-prefix hash impact assessed; if architect/SKILL.md is in any orchestrator's prefix region, ADR documents and CI hash file updates
- **Effort**: M-L (matches user's plan; risk on whether 200-line extraction is fully achievable in one wave)

### Story 2 — presentation + ui + operations Tier-B trims (mechanically independent; parallel-safe)

#### W3-2. presentation SKILL.md Tier-B trim (545→≤300)

- **MUST**: Reduce `delivery-team/skills/presentation/SKILL.md` from **545** lines (verified `wc -l` = 545; matches user's plan) to ≤300 lines.
- **Extraction candidates**: 9 presentation types as `references/types/<type>.md` (Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary); 4 format detail blocks (structured-markdown, marp, paste-ready, pptx) as `references/formats/<format>.md`; the 6-step collaboration flow detail (Assemble, Content Gate, Draft, Compose, Review Gate, User Review) as `references/flow.md` if not already
- **Files**: `delivery-team/skills/presentation/SKILL.md`, new `references/types/*.md` (×9), new `references/formats/*.md` (×4)
- **AC**:
  - [ ] presentation/SKILL.md → ≤300 lines
  - [ ] Phase 1 router picks correct type for 9/9 dogfood inputs
  - [ ] Phase 1 router picks correct format for 4/4 dogfood inputs
  - [ ] Sub-agent loads ONLY the matched type + format references (verified by spot-check on one dispatch)
- **Effort**: M

#### W3-3. ui SKILL.md Tier-B trim (496→≤300)

- **MUST**: Reduce `delivery-team/skills/ui/SKILL.md` from **496** lines (verified `wc -l` = 496; matches user's plan) to ≤300 lines.
- **Extraction candidates**: 3 designer roles (UX Designer, UI Designer, Game UI Designer) reference manifests under `references/roles/<role>.md`; design-system + design-tokens + component-spec detail under `references/design-system.md`; game-UI patterns (HUD, menu, inventory, health bar, minimap, dialog system, quest log, crafting UI) under `references/game-ui-patterns.md`
- **Files**: `delivery-team/skills/ui/SKILL.md`, new `references/roles/*.md` (×3), `references/design-system.md`, `references/game-ui-patterns.md`
- **AC**:
  - [ ] ui/SKILL.md → ≤300 lines
  - [ ] Phase 1 router picks correct designer role across 3/3 dogfood inputs (UX, UI, Game UI)
  - [ ] Game-UI patterns load ONLY when Game UI Designer role is detected
- **Effort**: M

#### W3-4. operations SKILL.md Tier-B trim (420→≤300)

- **MUST**: Reduce `delivery-team/skills/operations/SKILL.md` from **420** lines (verified `wc -l` = 420; matches user's plan) to ≤300 lines.
- **Extraction candidates**: 3 operations roles (DevOps, Release Manager, Technical Writer) reference manifests under `references/roles/<role>.md`; deployment-strategies (blue-green, canary, rolling) under `references/deployment-strategies.md`; release management cadence + SemVer/CalVer detail under `references/release-management.md`; documentation conventions (Diataxis, OpenAPI, runbook templates) under `references/documentation-patterns.md`
- **Files**: `delivery-team/skills/operations/SKILL.md`, new `references/roles/*.md` (×3), `references/deployment-strategies.md`, `references/release-management.md`, `references/documentation-patterns.md`
- **AC**:
  - [ ] operations/SKILL.md → ≤300 lines
  - [ ] Phase 1 router picks correct ops role across 3/3 dogfood inputs (DevOps, RM, Tech Writer)
  - [ ] Sub-agent loads ONLY matched role + matched task-specific reference
- **Effort**: M

### Story 3 — quality + user-feedback + godot trims (parallel)

#### W3-5. quality SKILL.md Tier-B trim (418→≤300)

- **MUST**: Reduce `delivery-team/skills/quality/SKILL.md` from **418** lines (verified `wc -l` = 418; matches user's plan) to ≤300 lines.
- **Extraction candidates**: Test strategy templates (smoke, sanity, regression, exploratory, boundary, edge-case, integration) under `references/test-strategies/<strategy>.md`; quality-metrics catalog under `references/quality-metrics.md`; automation-strategy detail under `references/automation-strategy.md`
- **Files**: `delivery-team/skills/quality/SKILL.md`, new `references/test-strategies/*.md`, `references/quality-metrics.md`, `references/automation-strategy.md`
- **AC**:
  - [ ] quality/SKILL.md → ≤300 lines
  - [ ] Phase 1 router picks correct test strategy across 7/7 dogfood inputs
  - [ ] Sub-agent loads ONLY matched strategy + relevant secondary reference (e.g., metrics for "quality metrics" task; automation-strategy for "automation" task)
- **Effort**: M

#### W3-6. user-feedback SKILL.md Tier-B trim (399→≤300)

- **MUST**: Reduce `delivery-team/skills/user-feedback/SKILL.md` from **399** lines (verified `wc -l` = 399; matches user's plan) to ≤300 lines. NOTE: this skill ALSO receives the paradigm sub-skill pattern in W3-8 — coordinate with W3-8 to avoid double-touch on personas.
- **Extraction candidates**: 4 persona families (gamers, web/app users, enterprise/B2B, demographic overlays) as paradigm sub-skills under `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` per W3-8 — that extraction directly contributes to the line-count reduction; remaining feedback-format templates under `references/feedback-formats.md`
- **Files**: `delivery-team/skills/user-feedback/SKILL.md`, new persona-family sub-skills (W3-8 owns these), `references/feedback-formats.md`
- **AC**:
  - [ ] user-feedback/SKILL.md → ≤300 lines
  - [ ] Persona-family routing in W3-8 verified by 4/4 dogfood inputs (gamers / web / enterprise / demographic) — same regression set serves both WIs
- **Effort**: M (joint with W3-8)

#### W3-7. godot SKILL.md Tier-C trim (236→≤200)

- **MUST**: Reduce `delivery-team/skills/godot/SKILL.md` from **236** lines (verified `wc -l` = 236; matches user's plan) to ≤200 lines (Tier-C ceiling per memory ruling 3).
- **Extraction candidates**: GDScript-vs-C# choice rubric under `references/language-choice.md`; signal/event-bus patterns under `references/signal-patterns.md`; node-hierarchy + scene composition under `references/scene-patterns.md`; existing foundational clean-code-standards reference may already cover part — Architect to confirm at Stage 4
- **Files**: `delivery-team/skills/godot/SKILL.md`, possibly new `references/language-choice.md`, `references/signal-patterns.md`, `references/scene-patterns.md`
- **AC**:
  - [ ] godot/SKILL.md → ≤200 lines (Tier-C compliant)
  - [ ] GDScript / C# / scene / signal task-types still route correctly
- **Effort**: S

### Story 4 — paradigm sub-skill pattern rollout (W3-8 — large; touches 3 plugins/skills)

#### W3-8. Paradigm sub-skill pattern across research-agent + presentation + user-feedback

- **MUST**: Apply the canonical paradigm sub-skill pattern (memory ruling: "For axes with ≥3 mutually-exclusive variants, create `<plugin>/skills/<axis>/<variant>/SKILL.md` with `disable-model-invocation: true`. Parent skill is the router; sub-skills only load when selected.") to three identified surfaces:
  1. **research-agent**: 5 research types (academic / market / technical / regulatory / user-research per current research-agent SKILL — Architect to confirm exact axis at Stage 4) → `research-agent/skills/research-types/<type>/SKILL.md`
  2. **presentation**: 9 presentation types from W3-2 → coordinate; the W3-2 extraction MAY use either references-only OR paradigm-sub-skill — whichever pattern best fits the dispatch shape. Architect picks at Stage 4. If paradigm sub-skill, use `presentation/skills/types/<type>/SKILL.md`
  3. **user-feedback**: 4 persona families → `user-feedback/skills/personas/<family>/SKILL.md` per W3-6 coordination
- **Files**: ≥3 new sub-skill SKILL.md files per axis (minimum 3+9+4 = 16 sub-skill files if presentation goes paradigm-sub-skill route; minimum 3+0+4 = 7 if presentation stays references-only)
- **AC**:
  - [ ] research-agent ≥3 sub-skills exist with `disable-model-invocation: true` frontmatter
  - [ ] user-feedback persona families exist as sub-skills with `disable-model-invocation: true`
  - [ ] Parent skill Phase 1 router dispatches to correct sub-skill in N/N dogfood inputs (N = number of variants)
  - [ ] Marketplace auto-discovery NOT broken (memory ruling 2: top-level skills MUST stay discoverable; only paradigm sub-skills get `disable-model-invocation`)
  - [ ] Cache-prefix impact assessed for parent skills; ADR if material
- **Effort**: L (matches user's plan; this is the most architecturally novel WI in the wave — Architect Stage 4 will write at least one ADR for the dispatch shape)

### Story 5 — governance frontmatter rollout (W3-9 — sequenced AFTER content trims)

#### W3-9. Governance frontmatter on all SKILL.md (`maintainer:` + `fitness_review_due:` + `context_budget:`)

- **MUST**: Every SKILL.md in this repo (delivery-team + other plugins' top-level SKILLs) gets three new frontmatter keys:
  - `maintainer: <github-handle-or-team-id>` — owner accountable for fitness review and budget compliance
  - `fitness_review_due: YYYY-MM-DD` — quarterly cadence; default = 90 days from frontmatter add date
  - `context_budget: <max_lines>` — explicit declaration matching the tier value (Tier-A=500, Tier-B=300, Tier-C=200) — pairs with the existing `tier:` key from Wave 1
- **Sequencing**: this WI MUST run AFTER W3-1..W3-8 content trims complete. Wave 0 lesson "mandatory rollout has side-effects" applies — frontmatter additions also bump line count by ~3 lines per file; running this BEFORE the trims means we'd target a fictional ≤297 / ≤197 instead of the canonical ≤300 / ≤200.
- **Files**: All `SKILL.md` files in delivery-team plugin (~12 SKILL.md files); other plugins' top-level SKILL.md (per delivery-team-first scoping, this WI may exclude other plugins — Architect to rule at Stage 4)
- **AC**:
  - [ ] All delivery-team SKILL.md files have `maintainer:` + `fitness_review_due:` + `context_budget:` frontmatter keys
  - [ ] CI lint validates the three keys are present and well-formed
  - [ ] No SKILL.md exceeds its `context_budget:` (which now matches its `tier:`)
  - [ ] `fitness_review_due:` dates are 90 days from rollout date (not all the same date — staggering acceptable per maintainer-team's choice)
- **Effort**: M (matches user's plan; mechanical rollout but mandatory across many files)

### Story 6 — retro KPI + fitness review process + CLAUDE.md refactor (W3-10..12)

#### W3-10. Retro KPI: `context_tokens_per_pipeline_run` 5-run rolling-mean

- **MUST**: Add a new KPI to the retrospective template — `context_tokens_per_pipeline_run` 5-run rolling mean — sourced from the W0-1 telemetry hook output. Retro must compute the rolling mean across the last 5 archived runs and report Δ vs prior 5-run window.
- **Files**: `delivery-team/skills/delivery-flow/references/retrospective-template.md` (or wherever retro template lives — Architect to confirm at Stage 4); telemetry post-processor script may need updating
- **AC**:
  - [ ] Retro template has `context_tokens_per_pipeline_run` KPI section with formula + source-data reference
  - [ ] Test: synthesize 5 prior-run datapoints, run retro template, KPI computes correctly
  - [ ] Trend annotation present (Δ vs prior 5-run window)
- **Effort**: S

#### W3-11. Quarterly fitness review process (governance doc + scheduled GitHub Action)

- **MUST**: Author a new governance doc under `governance/fitness-review.md` describing the quarterly fitness review process: cadence, owner, inputs (skill-budgets.json + telemetry rolling-mean + retro KPIs), outputs (pruning recommendations + budget adjustments + maintainer-rotation), and the kill-criteria threshold (skills failing fitness 2 quarters in a row). Pair with a scheduled GitHub Action under `.github/workflows/fitness-review-reminder.yml` that opens an issue 7 days before each `fitness_review_due:` date in any SKILL.md frontmatter.
- **Files**: new `governance/fitness-review.md`, new `.github/workflows/fitness-review-reminder.yml`
- **AC**:
  - [ ] Governance doc exists with cadence + owner + inputs + outputs + kill-criteria
  - [ ] Workflow runs on a schedule (cron weekly) and opens issues for upcoming fitness review dues
  - [ ] Workflow injection-lint guard from `.github/workflows/workflow-injection-lint.yml` passes for the new workflow (DEFECT-004 regression guard)
- **Effort**: S

#### W3-12. CLAUDE.md refactor (168→≤150)

- **MUST**: Reduce `CLAUDE.md` from **168** lines (verified `wc -l` = 168; user's plan claimed 169 — 1-line drift, actual is 168) to ≤150 lines per binding memory ruling: "Project-level CLAUDE.md MUST stay ≤150 lines. Loaded on every Claude Code session for this repo — every line is paid for thousands of times more than any single skill. Detail belongs in `governance/` or per-plugin `ARCHITECTURE.md`."
- **Extraction candidates**: Plugin-detail tables (delivery-team 11-skill table, hardware-team 7-skill table, hardware-team 6-hooks table, delivery-team 7-hooks table) — keep summary + link to full detail in per-plugin ARCHITECTURE.md or governance/plugin-catalog.md
- **Files**: `CLAUDE.md`, possibly new `governance/plugin-catalog.md` or extensions to existing per-plugin ARCHITECTURE.md
- **AC**:
  - [ ] CLAUDE.md → ≤150 lines
  - [ ] Plugin catalog detail still discoverable (one-hop link from CLAUDE.md to detail page)
  - [ ] CI lint validates CLAUDE.md ≤150 (extend `scripts/check_skill_budgets.py` or add a new guard)
- **Effort**: S

### Story 7 — admin / carry-forward (W3-13..18 — single Gimli/admin pass)

#### W3-13. Standardized validator-prompt template (Wave 2 retro carry-forward)

- **MUST**: Codify a canonical validator-prompt template that explicitly frames spec-vs-impl distinction and cites canonical paths. Template lives at `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`; validator dispatch sections (Stage 6 + Stage 7) reference it.
- **Files**: new `delivery-team/skills/delivery-flow/references/validator-prompt-template.md`, possibly `delivery-team/skills/delivery-flow/SKILL.md` (one-line pointer)
- **AC**:
  - [ ] Template exists with spec-vs-impl framing block + canonical-path block
  - [ ] All current validator dispatches reference the template
  - [ ] Dogfood: one validator dispatched via the template; verifies template's framing improves first-try DoD pass rate (or at minimum doesn't regress)
- **Effort**: S

#### W3-14. JSON ↔ Python KNOWN_DEBT consistency lint (Wave 2 retro carry-forward)

- **MUST**: New CI workflow lint validates that the `known_debt` array in `governance/skill-budgets.json` is consistent with any hard-coded debt list in `scripts/check_skill_budgets.py`. Fails PRs that drift the two out of sync.
- **Files**: new `.github/workflows/skill-budget-consistency.yml`, possibly `scripts/check_skill_budgets.py` (refactor to derive from JSON authoritatively if it currently has a hard-coded fallback)
- **AC**:
  - [ ] Workflow runs on PR + push to main
  - [ ] Workflow injection-lint guard passes
  - [ ] Test: deliberately introduce a JSON↔Python drift; workflow fails PR
- **Effort**: S

#### W3-15. DoD STATUS-format standardization (Wave 2 retro carry-forward)

- **MUST**: Either standardize DoD review files to a single STATUS line format, OR provide a flexible-grep helper that handles current variants. Architect picks at Stage 4 based on which is cheaper. STATUS values stay verbatim (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES per existing memory).
- **Files**: validator dispatch sections (Stage 6 + Stage 7) in `delivery-team/skills/delivery-flow/SKILL.md` and/or `references/quality-gates.md`; possibly new `scripts/extract_dod_status.py` if helper-route chosen
- **AC**:
  - [ ] All DoD review files post-Wave-3 use the single chosen format (or the helper handles all current variants)
  - [ ] Orchestrator's STATUS-line grep reliably extracts STATUS in 5/5 sample DoD reviews
- **Effort**: S

#### W3-16. Pre-merge git hook for skill-budget local check (Waves 0+1 carryover)

- **MUST**: New local pre-commit (or pre-push) git hook companion to the CI gate. Runs `scripts/check_skill_budgets.py` on commit; fails locally before push. Optional but recommended; opt-in install via `governance/install-pre-commit.sh` or similar.
- **Files**: new `governance/pre-commit-skill-budget.sh` (or `.git-hooks/pre-commit` template), new `governance/install-pre-commit.sh`
- **AC**:
  - [ ] Hook script exists and is executable
  - [ ] Install script wires it into `.git/hooks/` correctly
  - [ ] Hook fails commit when SKILL.md exceeds budget WITHOUT `Budget-Exception:` in the staged commit message
- **Effort**: S

#### W3-17. Stage 7 entry sweep step for stale Wave-N-1 carry-overs (caveman-lite retro carry-forward; DEFECT-006 systemic fix)

- **MUST**: Add a Stage 7 entry-step to `delivery-team/skills/delivery-flow/SKILL.md` that sweeps for stale Wave-N-1 carry-over artifacts in the new run's namespace BEFORE UAT begins. Two options from caveman-lite retro: Option A (banner each stale file) or Option B (move stale files to an archive directory). Architect picks at Stage 4.
- **Files**: `delivery-team/skills/delivery-flow/SKILL.md` Stage 7 dispatch instructions; possibly `references/stages.yml` Stage 7 row
- **AC**:
  - [ ] Stage 7 entry-step prescribed in SKILL.md
  - [ ] Dogfood: synthetic stale Wave-N-1 file in `07-uat/dod/`; entry-step detects and applies banner-or-move
  - [ ] DEFECT-006 closes upon merge of this WI
- **Effort**: S

#### W3-18. Telemetry hook output capture quality hardening (caveman-lite retro carry-forward)

- **MUST**: Harden the W0-1 telemetry hook to fail-loud (or fail-safe with explicit zero-token marker) when measurement is absent, instead of writing zero-token placeholder rows that force baseline-fallback. Either: (a) add measurement-absent diagnostic to the hook; (b) gate the hook on tool-output presence; (c) post-process step that filters placeholder rows before retro KPI compute (W3-10 dependency).
- **Files**: telemetry hook source under `delivery-team/hooks/` (Architect to identify exact file at Stage 4); possibly `scripts/skill_loads_filter.py` if post-process route chosen
- **AC**:
  - [ ] Hook either fails-loud or marks zero-token rows as `placeholder=true`
  - [ ] W3-10 retro KPI computation correctly excludes placeholder rows
  - [ ] Test: synthesize a missing-measurement scenario; hook output reflects the chosen behavior
- **Effort**: S

## Story consolidation (PO recommendation; Stage 5 owns final sequencing)

7 file-scope stories from 18 WIs (~61% Stage 6 dispatch reduction vs per-WI dispatch):

| Story | WIs | File scope | Effort | Risk | Sequencing note |
|-------|-----|------------|--------|------|-----------------|
| 1 | W3-1 | architect/SKILL.md + references | M-L | High (200-line residual; partial-compliance candidate) | First; sets pattern for Wave 3 partial-compliance ruling if needed |
| 2 | W3-2, W3-3, W3-4 | presentation + ui + operations SKILL.md + references | M | Med | Parallel-safe; mechanically independent |
| 3 | W3-5, W3-6, W3-7 | quality + user-feedback + godot SKILL.md + references | M | Low (godot is small) | Parallel-safe; W3-6 coordinates with W3-8 |
| 4 | W3-8 | research-agent + presentation + user-feedback paradigm sub-skills | L | High (architectural novelty) | After Story 1 ships ADR-pattern; informs paradigm dispatch shape |
| 5 | W3-9 | All delivery-team SKILL.md files (frontmatter rollout) | M | Med (mandatory rollout side-effects from Wave 0 lesson) | AFTER Stories 1-4 content trims complete |
| 6 | W3-10, W3-11, W3-12 | retro template + governance/fitness-review.md + workflow + CLAUDE.md | S | Low | Parallel with Story 5 |
| 7 admin | W3-13, W3-14, W3-15, W3-16, W3-17, W3-18 | validator-prompt template + JSON↔Python lint + STATUS-format + pre-merge hook + Stage 7 entry-step + telemetry hardening + governance/skill-budgets.json re-baseline | S each | Low | Parallel with anything; trivial |

This is a PO recommendation. Stage 5 of the Wave 3 pipeline owns final Story sequencing and may collapse further (e.g., merging Stories 6+7) or split further (e.g., separating W3-9 frontmatter rollout from its dependency-AFTER-trims gate).

## Out of scope (this BACKLOG)

- **Other plugins' Tier-B/C debt** (mtg-commander, hardware-team, agentic-flow-builder, prd-quality-gate-flow, prompt-engineer, research-agent's own SKILL.md if non-paradigm — defer to BACKLOG-105 mtg-commander Wave 0 per user direction "one plugin at a time after delivery-team")
- **delivery-team paradigm sub-skill pattern beyond the 3 cited** (research-agent, presentation, user-feedback). Other axes (e.g., developer 14-language axis if it qualifies as ≥3-mutually-exclusive-variant; architect 11-role axis if not already paradigm) deferred to BACKLOG-106+
- **External-plugin governance frontmatter rollout** beyond delivery-team — Architect at Stage 4 may include other plugins if ROI is clean; otherwise defer to BACKLOG-105+
- **Caveman-lite Tier 2 A/B test** (retrospective body prose + sprint plan body prose) — separate sub-wave; not in this BACKLOG
- **Caveman `full` or `ultra` mode adoption** — separate decision contingent on caveman-lite Wave 3 telemetry showing room for further reduction
- **Wenyan / non-English prose modes** — no business case
- **Code/commit/PR-body compression** — already excluded by caveman boundary rule + binding repo conventions

## Sequencing relative to caveman-lite (run-tk3)

caveman-lite **SHIPPED 2026-05-05** (merge to main). AC-13 (initiative-level token-reduction empirical telemetry) was deferred from caveman-lite by design; the Wave 3 pipeline IS the first post-merge run, so its first dispatches are the empirical AC-13 close-out for caveman-lite.

**Stop-rule trigger from BACKLOG-102**: if Wave 3's first dispatches show <15% prose-token reduction vs the pre-caveman-lite baseline, BACKLOG-102's stop-rule triggers a root-cause retro on caveman-lite BEFORE Wave 3 W3-9 governance work proceeds. The W3-1..W3-8 content trims may continue, since prose discipline is orthogonal to structural extractions, but W3-9's mandatory rollout (which will be the largest single mass-edit of caveman-lite-disciplined prose in delivery-team) holds until the retro completes.

## Acceptance Criteria (initiative-level)

1. All 7 remaining over-budget files from `governance/skill-budgets.json` are CLEARED (`scripts/check_skill_budgets.py` exits 0 with empty `known_debt` array OR only justified non-delivery-team Wave-4 entries).
2. CLAUDE.md ≤150 lines.
3. Governance frontmatter (`maintainer:` + `fitness_review_due:` + `context_budget:`) present on all delivery-team SKILL.md files.
4. The 4 Wave 2 retro carry-forward actions (W3-13 validator template, W3-14 JSON↔Python lint, W3-15 STATUS-format, W3-16 pre-merge hook) are DISCHARGED.
5. The 2 caveman-lite retro carry-forward actions (W3-17 Stage 7 entry sweep, W3-18 telemetry hardening) are DISCHARGED. DEFECT-006 closes.
6. Paradigm sub-skill pattern shipped on ≥3 axes (research-agent + user-feedback minimum; presentation if architecturally favored at Stage 4).
7. Telemetry-measured cumulative token reduction ≥50% on delivery-flow invocations vs pre-Wave-0 baseline (compounding Waves 0+1+2+caveman-lite+3).
8. No regression in delivery-flow first-try DoD pass rate (currently averaging 60-90% across stages per memory/index.md; Wave 3 should not degrade).
9. Defects/story rate ≤0.4 (stop-rule from BACKLOG-100; rolling 3-PR window).
10. Quarterly fitness review process operational (governance doc + scheduled GitHub Action live; first issue auto-opens for the earliest `fitness_review_due:` date).

## Pipeline-run preferences

- **Project type**: FEATURE-execution-of-pre-planned-waves (binding-decisions-in-memory pattern, fifth invocation in this initiative)
- **Routing**: 1 light · 2 light · 3 SKIP (DX-only) · 4 light (multiple ADRs likely; W3-1 partial-compliance ruling + W3-8 paradigm dispatch shape are highest-stakes) · 5 light · 6 full · 7 full
- **Story consolidation expectation**: 18 WIs → 7 file-scope stories (per §Story consolidation above)
- **Theme**: lotr (continued — theme continuity through end of delivery-team initiative)
- **Models**: Sonnet primaries, Haiku DoD validators per binding; Opus opt-in only for design synthesis on architecturally-novel WIs (W3-8 paradigm dispatch shape ADR; W3-1 partial-compliance ADR if needed)
- **Lessons to inject** (from chunks):
  - All 6 Hot Lessons from `memory/index.md` (top of every agent prompt)
  - Cache-prefix-impacting ADRs binding Dev runs-the-command (NEW from caveman-lite — `stages/architect.md` to be promoted in W3 entry-step)
  - Mid-implementation reference-extraction inside Stage 6 (NEW from caveman-lite — `stages/development.md` to be promoted in W3 entry-step)
  - Producer-validator separation for validator-style artifacts (NEW from caveman-lite — `stages/uat.md` to be promoted in W3 entry-step)
  - All 5 binding rulings + per-skill model map + tier values from `topics/skill-token-economy.md`
  - FEATURE-execution-of-pre-planned-waves + binding-decisions-in-memory + story-consolidation-by-file-scope from `topics/project-types.md`
  - Honest partial-compliance ruling pattern (Wave 2 → applies to W3-1 architect closure)
  - Mandatory-rollout side-effects (Wave 0 → applies to W3-9 frontmatter rollout AFTER content trims sequencing)

## Stop-rule

Two stop-rule triggers active for Wave 3:

1. **Initiative-level (BACKLOG-100 carry-forward)**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves. Current rolling 3-PR window: tk2 (0 defects) + tk3 (1 defect, P1 non-blocking) = **0.33 < 0.4 — NOT triggered, Wave 3 may proceed**.
2. **Caveman-lite carry-forward (BACKLOG-102)**: first post-Wave-3 dispatches showing <15% prose-token reduction vs pre-caveman-lite baseline triggers stop-rule retro on caveman-lite BEFORE Wave 3 W3-9 governance work proceeds. W3-1..W3-8 content trims may continue under this trigger; only W3-9 (and downstream W3-10..12 that depend on frontmatter rollout) holds.

## Pre-flight gate

caveman-lite (BACKLOG-102) and Wave 2 (BACKLOG-103) MUST both be merged on main before this pipeline starts. **Status: SATISFIED** — main is at c2e7d5a (Wave 2 merged 2026-05-05) + caveman-lite merged 2026-05-05 trunk-based per `memory/index.md` last_run_id = run-2026-05-05-tk3.

## Risk register

| Risk | Severity | Mitigation |
|------|----------|------------|
| W3-1 architect 200-line residual extraction infeasible in one wave | High | Partial-compliance pattern from Wave 2 honored: PRD + ADR document residual + target_wave=4; CI gate accepts via `Budget-Exception: <ADR>` with explicit math |
| W3-8 paradigm sub-skill pattern breaks marketplace auto-discovery | High | Memory ruling 2 binding: `disable-model-invocation: true` ONLY on paradigm sub-skills; top-level skills stay discoverable. CI lint validates this invariant |
| W3-9 frontmatter rollout side-effects bump line count past tier ceiling | Med | Sequencing: W3-9 runs AFTER W3-1..W3-8 content trims complete (Wave 0 mandatory-rollout-side-effects lesson honored) |
| W3-1 + W3-2 + W3-3 + W3-4 + W3-5 + W3-6 + W3-7 cumulative cache-prefix impact unaccounted | Med | Architect Stage 4 produces a single Wave-3-summary ADR documenting cumulative cache-prefix changes + one-time re-warm cost; CI hash file updated once at end of Story 5 (not per-story) |
| W3-18 telemetry hardening doesn't catch all zero-token cases before W3-10 retro KPI compute | Med | W3-10 retro KPI explicitly excludes `placeholder=true` rows AND has fallback to baseline-from-archive if rolling-mean is unavailable |
| Defects/story rate spikes in Wave 3 (largest wave to date) and triggers stop-rule | Med | 7-story consolidation reduces dispatch surface; Sonnet primaries on the architecturally-novel WIs (W3-1, W3-8) maintain quality; PO empowered to surgically halt at any Story boundary |
| caveman-lite stop-rule fires (<15% prose reduction) and gates W3-9 | Low (Wave 3 measurement IS the empirical close-out) | Story 5 (W3-9) has explicit "after caveman-lite stop-rule check" gate; Stories 1-4 + admin proceed under stop-rule |

## References

- BACKLOG-102 (caveman-lite — predecessor, prose discipline + telemetry close-out gate for Wave 3)
- BACKLOG-103 (Wave 2 — predecessor, doctrine extraction + per-skill contracts)
- BACKLOG-101 (Wave 1 — frontmatter rollout precedent for W3-9 sequencing lesson)
- BACKLOG-100 (Wave 0 — telemetry substrate + CI gate; stop-rule origin)
- ADR-tk3-001 (caveman-lite cache-prefix re-freeze precedent for Wave 3 cumulative cache-prefix ADR)
- `.delivery/memory/topics/skill-token-economy.md` (5 binding rulings; tier budgets; per-skill model map; Initiative Sequencing)
- `.delivery/memory/topics/project-types.md` (FEATURE-execution-of-pre-planned-waves + binding-decisions-in-memory + story-consolidation pattern + honest partial-compliance ruling pattern)
- `.delivery/memory/archive/run-2026-05-05-tk3.md` (caveman-lite retro — 6 self-improvement actions for Wave 3)
- `.delivery/memory/archive/run-2026-05-05-tk2.md` (Wave 2 retro — 4 carry-forward actions, all in this BACKLOG)
- `.delivery/memory/index.md` (6 Hot Lessons; Stage Health post-caveman-lite)
- `governance/skill-budgets.json` (current known-debt registry — 7 entries all targeted to Wave 3)

— Aragorn, PO, 2026-05-05. The road is long but the way is plain. Onward.

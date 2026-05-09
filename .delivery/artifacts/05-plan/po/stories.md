<!-- run: run-2026-05-09-tk4 | stage: 05-plan | depth: light | author: Product Owner (Frodo Baggins) | sources: BACKLOG-104, prd.md, ADR-tk4-{001,002,003}, architecture-tk4-wave-3.md | wave: 3 — closure -->

# Plan — Stories (run-2026-05-09-tk4, Wave 3 closure)

> "I will take the burden, though I do not know all the lines that lie ahead. I will count them when I come to them, and the road will be walked plainly."
> — Frodo, accepting the burden.

Seven stories. One wave. The road is set; the gates are sharp. The Fellowship counts the lines.

## Capacity Declaration (binding for SM)

- **Velocity baseline (rolling 5-pipeline mean)**: ~7 file-scope-stories-equivalent per FEATURE-execution wave (Waves 1/2/caveman-lite landed 5–8 each; this wave is the upper end as the close-out).
- **80% ceiling**: 7 stories at sizes [M-L, L, M, L, M, M, S-M] sum to ~22 points; 28-point ceiling (5 × 7 minus 20% buffer); commitment **78.6% — under the 80% rule** (Plan memory lesson 1).
- **Story count**: **7** (file-scope consolidation from 18 WIs; ~61% Stage-6 dispatch reduction).
- **Effort calibration**: markdown-only edits estimated one tier below code-equivalent per Plan memory lesson 3 (validated 3×). All 7 stories are markdown + small Python + git plumbing — no compiled code.
- **Capacity assumption**: single-developer Stage 6 dispatch per story (file-scope consolidation pattern, validated 3×).
- **Test-coverage gate**: test cases MUST cover ALL 7 PRD FRs explicitly per Plan memory lesson 2; PO rejects any plan missing an FR.

## Sequencing Rules (binding)

1. **Story 5 mandatory-after-Stories-1-4** — Story 5 (W3-9 governance frontmatter rollout) MUST NOT begin until Stories 1, 2, 3, AND 4 have landed in the working tree (PRD §FR-5; ADR-tk4-003 §Mandatory-rollout sequencing; Wave 0 mandatory-rollout-side-effects lesson). Adding 3 frontmatter lines to a file at-budget pushes it over — hard gate, not a soft preference.
2. **Story 7 last** — admin Story 7 sequenced terminal so W3-13 validator template, W3-15 STATUS format, W3-17 Stage 7 entry sweep, W3-18 telemetry hardening get dogfooded against the live Wave 3 dispatches that produced them. Itself parallel-with-anything; PO sequences last for dogfood-data co-landing.
3. **Stories 2 + 3 parallel-safe with Story 1** — mechanically independent file scopes per ADR-tk4-001 extraction-target catalog; dispatchable in parallel after Story 1 lands the ADR pattern.
4. **Story 4 (W3-8) after Stories 1–3** — implements ADR-tk4-002 paradigm pattern after reference-extraction precedent ships. Joint-AC with Story 3 (W3-6 user-feedback line-count vehicle).
5. **Story 6 parallel with Story 5** — no cache-prefix or SKILL.md frontmatter dependency; concurrent with Story 5.
6. **Tripwire halt before Story 5** — if first 3 Stage-6 dispatches show <15% prose-token reduction vs pre-caveman-lite baseline (ADR-tk4-003 + architecture §Stop-Rule Tripwire Mechanics; PRD §NFR-8), HALT before Story 5 W3-9 PR opens. Stories 1–4 + Story 7 proceed; only W3-9 + W3-10..12 hold pending caveman-lite root-cause retro. Citation artifact: `.delivery/telemetry/stop-rule-tk4.txt` (no narrative claims).

## Stop-rule (verbatim from idea-brief §9)

**Initiative-level (BACKLOG-100 carry-forward)**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves. Current rolling 3-PR window: tk2 (0 defects) + tk3 (1 defect, P1 non-blocking) = **0.33 < 0.4 — NOT triggered, Wave 3 may proceed**. Wave 3 must hold the rate; PO empowered to halt at any Story boundary if a third defect lands and pushes the window past threshold.

## plugin-dev routing (mandatory pre-load — every story)

ALL 7 stories touch SKILL.md files. Per CLAUDE.md "Key Conventions" (binding): every Stage-6 dev dispatch MUST acknowledge `plugin-dev:skill-development` pre-load before edits; DoD validator cites the SKILL_LOADED signal. Post-completion: `plugin-dev:skill-reviewer`. Pre-PR: `plugin-dev:plugin-validator`. No exceptions.

---

## Story 1 — architect Tier-B closure (W3-1)

**Story**

**As a** delivery-flow orchestrator dispatching the architect role across 11 architecture variants (7 software roles + 4 game roles),
**I want** `delivery-team/skills/architect/SKILL.md` reduced from 500 to ≤300 lines via the per-file extraction strategy in ADR-tk4-001 (5 extractions: Architecture-Style block -76, Software Roles -56, Game Roles -30, Cross-Role Tasks -23, Architecture Guardrails -27),
**So that** the architect SKILL.md lands at ≤300 (Tier-B compliant) with ≥9-line headroom for the +3 frontmatter rollout in Story 5, the Wave-2 honest-partial-compliance pattern is set as the precedent for the rest of the wave, and `governance/skill-budgets.json` clears its first known_debt entry.

**Effort**: **M-L** — five extractions to existing or new `references/` directories; 11-input Phase 1 router regression; partial-compliance ADR-tk4-001 reserve cited if Cross-Role Tasks (24 lines) cannot extract cleanly; markdown-only.

**Files Touched** (pre-frontmatter values from ADR-tk4-001 batching math)

- `delivery-team/skills/architect/SKILL.md` — **500 → 288** (canonical math) or **500 → 311** (partial-compliance reserve if Cross-Role Tasks resists extraction). Post-Story-5 frontmatter add lands at 291 (288+3) with 9-line headroom or 314 (311+3) with `Budget-Exception: ADR-tk4-001`.
- `delivery-team/skills/architect/references/decomposition/<strategy>.md` (×4) — extend existing per-strategy files with Architecture-Style block content; replace block in SKILL.md with 4-line pointer table.
- `delivery-team/skills/architect/references/roles/<role>.md` (×7 software + ×4 game = 11 new files) — per-role manifests; replace blocks in SKILL.md with 7-row + 4-row routing tables.
- `delivery-team/skills/architect/references/contracts/cross-role-tasks.md` (new) — extract Cross-Role Tasks; one-line pointer in SKILL.md.
- `delivery-team/skills/architect/references/guardrails.md` (new) — extract Architecture Guardrails; one-line pointer.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-1 AC-1]** `wc -l delivery-team/skills/architect/SKILL.md` returns `≤300` (canonical) OR `≤311` with `Budget-Exception: ADR-tk4-001` line in PR body AND `governance/skill-budgets.json` `known_debt[]` contains a `W3-1-residual` entry with `target_wave: 4` plus explicit residual math.
2. **[W3-1 AC-2]** `python3 scripts/check_skill_budgets.py` exits 0 OR exits 1 ONLY with `W3-1-residual` (Budget-Exception) as the sole flagged delivery-team file.
3. **[W3-1 AC-3]** Phase 1 router regression: 11/11 dogfood inputs (one per role: Solution / Enterprise / Data / Security / Compliance / Privacy / IR + Game Systems / Level / Network / Graphics) route to the correct `references/roles/<role>.md` file; spot-check on one dispatch confirms sub-agent loads ONLY the matched role manifest (no parent-context bleed).
4. **[W3-1 AC-4]** Cache-prefix invariant preserved: `wc -l delivery-team/skills/architect/SKILL.md` extraction lines start at line ≥111 (verified `head -120 SKILL.md | tail -20` shows extracted-block boundary BELOW the frontmatter + Phase 1 router); ADR-tk4-001 §Cumulative cache-prefix impact assessment cited in PR body.
5. **[W3-1 AC-5]** All new `references/roles/*.md`, `references/contracts/cross-role-tasks.md`, `references/guardrails.md` files exist + are non-empty + are referenced from SKILL.md via routing-table pointers (`grep -c "references/roles" delivery-team/skills/architect/SKILL.md` returns ≥11; `grep "references/contracts/cross-role-tasks.md" SKILL.md` returns 1; `grep "references/guardrails.md" SKILL.md` returns 1).

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-1 — 11-input router regression set + Phase 1 spot-check protocol + budget-exception conditional path coverage.

**Dependencies / Sequencing**: First; sets the per-file extraction precedent and partial-compliance ADR template for Stories 2–3. No upstream dependency. Stories 2 + 3 may dispatch in parallel after this story's ADR-pattern lands.

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory; `plugin-dev:skill-reviewer` post-completion.

**Per-story DoD**: all 5 ACs PASS (or AC-1 via Budget-Exception path with explicit math); `plugin-dev:skill-development` SKILL_LOADED in dev transcript; PR body cites ADR-tk4-001 batching math; DoD validator review at `.delivery/artifacts/06-development/dod/W3-1-architect-closure.md` with STATUS literal.

---

## Story 2 — presentation + ui + operations Tier-B trims (W3-2 + W3-3 + W3-4)

**Story**

**As a** delivery-flow orchestrator dispatching the presentation, ui, and operations roles across their respective variant axes (9 presentation types + 4 formats; 3 designer roles; 3 ops roles),
**I want** the three Tier-B SKILL.md files reduced via per-file extraction strategy from ADR-tk4-001 (presentation 545→~160 via 9 type specs + 6 flow steps + 4 format specs; ui 496→273 via 3 designer-role manifests + 4 contract templates + cross-role-tasks; operations 420→255 via 3 ops-role manifests + 3 output-contract templates + task-instructions),
**So that** all three files land at ≤300 with substantial headroom (≥24 lines) for the +3 frontmatter rollout in Story 5, mechanically-independent file scopes proceed in parallel without cross-file collision, and the reference-extraction pattern is replicated across three orthogonal role axes.

**Effort**: **L** (3 files parallel-safe) — three independent file-scope extractions; ~16 dogfood router invocations across the three files (9+4 + 3 + 3); markdown-only.

**Files Touched** (pre-frontmatter values from ADR-tk4-001 batching math)

- `delivery-team/skills/presentation/SKILL.md` — **545 → ~160** (-92 type extraction, -267 flow extraction, -47 format extraction; with +20 connective-prose buffer realistic landing ~160; ≥137-line headroom).
- `delivery-team/skills/presentation/references/types/<type>.md` (×9) — Sprint Review, Feature Pitch, Stakeholder Update, Technical Deep-Dive, Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary.
- `delivery-team/skills/presentation/references/flow/<step>.md` (×6) — Assemble, Content Gate, Draft, Compose, Review Gate, User Review.
- `delivery-team/skills/presentation/references/formats/<format>.md` (×4) — structured-markdown, marp, paste-ready, pptx.
- `delivery-team/skills/ui/SKILL.md` — **496 → 273** (-89 designer roles, -22 cross-role-tasks, -112 contracts; 24-line headroom).
- `delivery-team/skills/ui/references/roles/<role>.md` (×3) — UX Designer, UI Designer, Game UI Designer.
- `delivery-team/skills/ui/references/contracts/<contract>.md` (×4) + `references/contracts/cross-role-tasks.md`.
- `delivery-team/skills/operations/SKILL.md` — **420 → 255** (-58 routing/instructions, -107 contracts; 42-line headroom).
- `delivery-team/skills/operations/references/roles/<role>.md` (×3) — DevOps, Release Manager, Technical Writer.
- `delivery-team/skills/operations/references/contracts/<role>-output.md` (×3) + `references/contracts/task-instructions.md`.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-2 AC]** `wc -l delivery-team/skills/presentation/SKILL.md` returns ≤300; `wc -l delivery-team/skills/ui/SKILL.md` returns ≤300; `wc -l delivery-team/skills/operations/SKILL.md` returns ≤300.
2. **[W3-2 AC-router]** Presentation router regression: 9/9 type-detection dogfood inputs route correctly + 4/4 format-detection inputs route correctly; spot-check confirms sub-agent loads ONLY matched type+format pair.
3. **[W3-3 AC-router]** UI router regression: 3/3 designer-role inputs route correctly (UX, UI, Game UI); Game-UI patterns load ONLY when Game UI Designer role detected.
4. **[W3-4 AC-router]** Operations router regression: 3/3 ops-role inputs route correctly (DevOps, RM, Tech Writer); sub-agent loads ONLY matched role + matched task-specific reference.
5. **[W3-2/3/4 AC-budget]** `python3 scripts/check_skill_budgets.py` exits 0 for all three files (no Budget-Exception expected; headroom is large).

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-2 — 16-input parallel router regression set across three files; isolation spot-checks per file.

**Dependencies / Sequencing**: Parallel-safe with Story 3 after Story 1 ADR-pattern lands. No cross-file collision (different SKILL.md, different `references/` subtrees).

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory (one acknowledgement per dispatch — three dispatches if parallel, one if serialized); `plugin-dev:skill-reviewer` post-completion per file.

**Per-story DoD**: all 5 ACs PASS for all three files; `plugin-dev:skill-development` SKILL_LOADED per dev dispatch; PR body cites ADR-tk4-001 batching math per file; DoD reviews at `.delivery/artifacts/06-development/dod/W3-{2,3,4}-{presentation,ui,operations}-trim.md` with STATUS literals.

---

## Story 3 — quality + user-feedback + godot trims (W3-5 + W3-6 + W3-7; godot to 197)

**Story**

**As a** delivery-flow orchestrator dispatching quality (7 test strategies), user-feedback (4 persona families), and godot (4 task types: GDScript / C# / scene / signal),
**I want** quality 418→276 via 6 contract-template extractions, user-feedback 399→250 via persona-family paradigm sub-skill extraction (joint-AC with Story 4 W3-8) plus sub-agent-interface extraction, and godot 236→**197** (deepened from round-1 198 per ADR-tk4-001 round-2 revision) via task-patterns extraction plus a 1-line guardrails consolidation,
**So that** the three remaining over-budget delivery-team SKILL.md files clear their tier ceilings with the godot Tier-C ceiling held EXACTLY at 200 post-frontmatter (197+3=200) — the round-2 mandatory-rollout-side-effect insurance — and the user-feedback persona-family extraction directly satisfies both W3-6 line-count and W3-8 paradigm sub-skill ACs in a single touch.

**Effort**: **M** — three independent extractions; godot's deepened trim (round-2: 197 not 198) is the sole zero-headroom file in the wave; user-feedback joint-AC with Story 4 means the persona-family extraction MUST coordinate; markdown-only.

**Files Touched** (pre-frontmatter values from ADR-tk4-001 batching math; godot post-frontmatter targeted at 200 exactly)

- `delivery-team/skills/quality/SKILL.md` — **418 → 276** (-142 via 6 contract extractions; 21-line headroom).
- `delivery-team/skills/quality/references/contracts/<contract>.md` (×6) — Test Strategy, Test Cases, Test Plan, Test Data, Quality Metrics, Automation Strategy. (3 may extend existing `references/test-strategy.md`, `quality-metrics.md`, `test-automation.md` per ADR-tk4-001 extraction-target catalog — Stage 6 Dev consolidates before duplicating.)
- `delivery-team/skills/user-feedback/SKILL.md` — **399 → 250** (-61 persona-family paradigm extraction joint-with-Story-4, -88 sub-agent-interface extraction; 47-line headroom).
- `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` (×4 — gamers, web-app, enterprise, demographic) — paradigm sub-skills per ADR-tk4-002 (Story 4 owns the paradigm contract; Story 3 owns the line-count vehicle; one extraction satisfies both).
- `delivery-team/skills/user-feedback/references/sub-agent-interface.md` (new).
- `delivery-team/skills/godot/SKILL.md` — **236 → 197** (-38 task-patterns extraction, -1 guardrails consolidation; **0-line headroom — held EXACTLY at Tier-C 200 ceiling post-frontmatter +3**).
- `delivery-team/skills/godot/references/task-patterns.md` (new). Existing `references/{gdscript,csharp-godot,scenes-nodes,signals-architecture}.md` (Wave 2) untouched.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-5 AC]** `wc -l delivery-team/skills/quality/SKILL.md` returns ≤300; Phase 1 router picks correct test strategy 7/7 dogfood inputs (smoke / sanity / regression / exploratory / boundary / edge-case / integration).
2. **[W3-6 AC]** `wc -l delivery-team/skills/user-feedback/SKILL.md` returns ≤300; persona-family routing 4/4 dogfood inputs (gamers / web-app / enterprise / demographic) — joint with Story 4 AC-2.
3. **[W3-7 AC-budget]** `wc -l delivery-team/skills/godot/SKILL.md` returns **≤197** (NOT ≤200 — round-2 deepened target so frontmatter add lands at exactly 200); `python3 scripts/check_skill_budgets.py` exits 0 with godot at 197.
4. **[W3-7 AC-router]** GDScript / C# / scene / signal task-types route correctly (4/4 dogfood inputs); existing Wave-2 `references/{gdscript,csharp-godot,scenes-nodes,signals-architecture}.md` untouched (`git diff --name-only` shows no edits to those four).
5. **[W3-5/6/7 AC-headroom]** ALL three files satisfy `after + 3 ≤ tier_ceiling`: quality 276+3=279≤300, user-feedback 250+3=253≤300, godot 197+3=200≤200. Verified by `wc -l` after extractions land but BEFORE Story 5 begins.

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-3 — 15-input parallel router regression set; godot zero-headroom edge-case verified by exact-line-count check.

**Dependencies / Sequencing**: Parallel-safe with Story 2 after Story 1 ADR-pattern lands. W3-6 user-feedback persona-family extraction coordinates with Story 4 W3-8 (same files; one extraction operation satisfies both stories).

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory; `plugin-dev:skill-reviewer` post-completion per file.

**Per-story DoD**: all 5 ACs PASS; godot lands at EXACTLY 197 (round-2 zero-headroom binding); `plugin-dev:skill-development` SKILL_LOADED per dispatch; PR cites ADR-tk4-001 round-2; DoD reviews at `.delivery/artifacts/06-development/dod/W3-{5,6,7}-{quality,user-feedback,godot}-trim.md`.

---

## Story 4 — paradigm sub-skill pattern (W3-8; per ADR-tk4-002)

**Story**

**As a** delivery-flow orchestrator and marketplace-discoverable plugin author,
**I want** the canonical paradigm sub-skill pattern from ADR-tk4-002 (`<plugin>/skills/<axis>/<variant>/SKILL.md` with `disable-model-invocation: true`) shipped on three axes — research-agent (5 research types), user-feedback (4 persona families, joint with Story 3 W3-6), and presentation (9 types, *conditional* on Stage 6 measurement that references-only is insufficient — default = references-only since W3-2 already meets ≤300),
**So that** marketplace auto-discovery is preserved (Ruling 2: top-level skills stay discoverable; sub-skills router-dispatched only), token economy improves per-axis (research-agent dispatch loads 1/5 of type-specific content; user-feedback 1/4; presentation 1/9 if adopted), and the pattern is codified for future axes (developer 14-language, architect 11-role per BACKLOG-106+).

**Effort**: **L** — 5 research-agent sub-skills + 4 user-feedback sub-skills + (conditional) 9 presentation sub-skills = 9–18 new SKILL.md files; each sub-skill needs frontmatter contract per ADR-tk4-002 §Sub-skill SKILL.md frontmatter contract; CI lint extension for marketplace-discoverability invariant; markdown + minor CI lint script.

**Files Touched** (pre-frontmatter values for new sub-skills; sub-skills themselves get full Story-5 frontmatter contract directly at creation)

- `research-agent/skills/research-types/<type>/SKILL.md` (×5 — academic, market, technical, regulatory, user-research; Architect Stage 4 confirmed exact axis at ADR-tk4-002 §Decision). Each new file: ≤200 lines (Tier-C); `disable-model-invocation: true` mandatory.
- `research-agent/SKILL.md` — parent router edit; +~5 lines for 5-row dispatch table; below cache-prefix region.
- `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` (×4 — gamers, web-app, enterprise, demographic). Joint-creation with Story 3 W3-6 line-count vehicle; one extraction operation satisfies both stories.
- `delivery-team/skills/user-feedback/SKILL.md` — parent router edit (already counted in Story 3 line-count math).
- `delivery-team/skills/presentation/skills/types/<type>/SKILL.md` (×9) — **CONDITIONAL** (default = NOT created; references-only path from Story 2 sufficient per ADR-tk4-002 §Decision §3 alternative). Stage 6 measures dispatch shape; if telemetry favors paradigm-sub-skill, ship; otherwise defer to BACKLOG-106+.
- `.github/workflows/marketplace-discoverability-lint.yml` (new OR extension to existing) — CI lint per ADR-tk4-002 §Marketplace discoverability invariant: validates `disable-model-invocation: true` ONLY on paradigm sub-skill paths matching `.*/skills/[^/]+/[^/]+/SKILL.md` or grandfathered `.*/paradigms/[^/]+/SKILL.md`.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-8 AC-1 research]** `find research-agent -path "*/skills/research-types/*/SKILL.md" | wc -l` returns ≥5; each file's frontmatter contains `disable-model-invocation: true`, `tier: C`, `parent_skill: research-agent/SKILL.md`, `axis: research-types`, `variant: <variant>`.
2. **[W3-8 AC-2 personas]** `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" | wc -l` returns 4; persona-family Phase 1 router 4/4 dogfood inputs (gamers / web-app / enterprise / demographic) — joint with Story 3 AC-2.
3. **[W3-8 AC-3 marketplace]** Marketplace-discoverability CI lint PASSES: `grep -l "disable-model-invocation: true" $(find . -name SKILL.md -not -path "*/node_modules/*")` returns ONLY paths matching `.*/skills/[^/]+/[^/]+/SKILL.md` OR grandfathered `.*/paradigms/[^/]+/SKILL.md`. Zero top-level plugin SKILL.md flagged.
4. **[W3-8 AC-4 cache]** Cache-prefix invariant preserved on parent skills: `governance/cache-prefix-hash.txt` for research-agent + user-feedback parent SKILL.md UNCHANGED post-Story-4 (router additions land at line ≥100; below 2k-byte prefix region per ADR-tk4-002 §Cache-prefix impact).
5. **[W3-8 AC-5 conditional presentation]** Stage 6 telemetry decision recorded in PR body: either (a) presentation paradigm-sub-skill route adopted with all 9 sub-skills present + Phase 1 router 9/9, OR (b) presentation references-only retained with explicit cite of Story 2 W3-2 sufficiency + presentation paradigm deferred to BACKLOG-106+.

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-4 — sub-skill frontmatter contract validation + marketplace-discoverability lint test (deliberately introduce a top-level violation; lint MUST fail) + cache-prefix-hash unchanged-on-parent verification.

**Dependencies / Sequencing**: After Stories 1, 2, 3 (ADR-pattern + reference-extraction precedent both required). Joint-AC with Story 3 W3-6 (one extraction satisfies both). MUST land before Story 5 (frontmatter rollout includes new sub-skills).

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory (sub-skill creation = new SKILL.md files); `plugin-dev:skill-reviewer` per sub-skill post-completion; `plugin-dev:plugin-validator` for marketplace-discoverability before PR.

**Per-story DoD**: all 5 ACs PASS; presentation paradigm decision recorded; `plugin-dev:skill-development` SKILL_LOADED per axis; PR cites ADR-tk4-002 frontmatter contract + Ruling 2; DoD review at `.delivery/artifacts/06-development/dod/W3-8-paradigm-sub-skill.md`.

---

## Story 5 — governance frontmatter rollout (W3-9; per ADR-tk4-003) — AFTER Stories 1–4

**Story**

**As a** maintainer of the delivery-team plugin running quarterly fitness reviews and CI line-budget enforcement,
**I want** three new frontmatter keys (`maintainer:` + `fitness_review_due:` + `context_budget:`) added to every delivery-team SKILL.md (11 top-level + 2 grandfathered architect/paradigms + paradigm sub-skills from Story 4 = 13+ files), with `governance/cache-prefix-hash.txt` regenerated ONCE at end of Story 5 with expanded 13-file scope per ADR-tk4-003,
**So that** the quarterly fitness review process (Story 6 W3-11) is operationalized with machine-readable maintainer + due-date fields, the line-budget CI lint becomes single-pass (reads `context_budget` directly, no tier-to-line lookup), and the one-time ~26KB cold-cache re-warm cost is paid once on dispatch #1 and amortized over the cumulative ~13,200-token reduction from Stories 1–3 trims.

**Effort**: **M** — mechanical 13-file frontmatter edit; CI lint script for the 3 new keys; cache-prefix hash regeneration with expanded scope; Dev runs-the-command at DoD per ADR-tk4-003 binding (caveman-lite Hot Lesson #1 extension); markdown + Python.

**Files Touched** (post-Stories-1–4 line counts; this story ADDS frontmatter)

- **All 13 delivery-team SKILL.md files** get three keys: `maintainer: delivery-team-leads`, `fitness_review_due: 2026-08-09` (or staggered 80–100-day window per FR-5.4), `context_budget: <500|300|200>` matching `tier:`. Post-frontmatter line totals (landed-from-Stories-1-3 +3): architect 291/300, presentation ~163/300, ui 276/300, operations 258/300, quality 279/300, user-feedback 253/300, **godot 200/200 EXACTLY**, plus delivery-flow/product-delivery/developer (Tier-A 500), alias-creator (Tier-C 200, already compliant), and grandfathered architect/paradigms/{volatility,ddd}. Story 4 paradigm sub-skills get frontmatter at creation; Story 5 verifies presence.
- `scripts/lint_skill_frontmatter.py` (new) — CI lint for the 3 new keys; fails PR if any key missing or `context_budget != tier_value`.
- `.github/workflows/skill-frontmatter-lint.yml` (new) — wires lint into CI; workflow-injection-lint guard PASSES.
- `governance/cache-prefix-hash.txt` — regenerated ONCE via `python3 scripts/regenerate_cache_prefix_hash.py --target governance/cache-prefix-hash.txt --files delivery-team/skills/*/SKILL.md delivery-team/skills/*/paradigms/*/SKILL.md`; header comment records expanded 13-file scope vs prior 1-file (delivery-flow only) scope from ADR-tk3-001.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-9 AC-1]** `python3 scripts/lint_skill_frontmatter.py` exits 0 — all delivery-team SKILL.md have `maintainer:` + `fitness_review_due:` (parses as ISO-8601) + `context_budget:` (matches tier value: A=500, B=300, C=200).
2. **[W3-9 AC-2 budget]** `python3 scripts/check_skill_budgets.py` exits 0 with `known_debt[]` array EMPTY for delivery-team scope (or only justified non-delivery-team Wave-4 entries). Godot specifically lands at 200 EXACTLY (not 201, not 199): `wc -l delivery-team/skills/godot/SKILL.md` returns `200`.
3. **[W3-9 AC-3 cache]** `governance/cache-prefix-hash.txt` regenerated; Dev runs-the-command per ADR-tk4-003 §DoD validator binding; PR body cites the ACTUAL byte counts from the regenerated file (NOT the +650-byte projection); 13-file scope confirmed in header comment.
4. **[W3-9 AC-4 sequencing]** Story 5 PR opens AFTER Stories 1–4 PRs merge to main: `git log --merges --oneline main..HEAD` shows Stories 1–4 merge commits BEFORE Story 5 commit timestamp; sequencing gate from PRD §FR-5 + ADR-tk4-003 §Mandatory-rollout sequencing satisfied.
5. **[W3-9 AC-5 tripwire]** Stop-rule tripwire NOT fired before this story opens its PR: `.delivery/telemetry/stop-rule-tk4.txt` exists + shows ≥15% prose-token reduction vs pre-caveman-lite baseline (per architecture §Stop-Rule Tripwire Mechanics). If <15%, this story HALTS pending caveman-lite root-cause retro per BACKLOG-102 carry-forward.

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-5 — frontmatter lint script test (deliberately omit one key; MUST fail) + cache-prefix-hash regeneration verification (compare pre/post byte counts against +650 projection ±10%) + sequencing gate verification + tripwire halt-path coverage.

**Dependencies / Sequencing**: **HARD GATE — AFTER Stories 1, 2, 3, AND 4 land in working tree.** Tripwire-armed: HALT before this story's PR opens if `.delivery/telemetry/stop-rule-tk4.txt` shows <15% prose reduction. May parallel with Story 6 (no cache impact on Story 6 surface).

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory; `plugin-dev:skill-reviewer` post-completion; `plugin-dev:plugin-validator` BEFORE PR (CI lint chain depends on validator pass).

**Per-story DoD**: all 5 ACs PASS; tripwire NOT fired; Dev runs-the-command for hash regeneration (ADR-tk4-003 binding); `plugin-dev:skill-development` SKILL_LOADED; PR cites ADR-tk4-003 + actual byte counts + sequencing verification; DoD review at `.delivery/artifacts/06-development/dod/W3-9-frontmatter-rollout.md`.

---

## Story 6 — retro KPI + fitness review process + CLAUDE.md refactor (W3-10 + W3-11 + W3-12)

**Story**

**As a** repository maintainer running quarterly fitness reviews and a delivery-flow retrospective facilitator computing per-pipeline token KPIs,
**I want** the retrospective template gain a `context_tokens_per_pipeline_run` 5-run rolling-mean KPI sourced from W0-1 telemetry (W3-10), `governance/fitness-review.md` authored with cadence/owner/inputs/outputs/kill-criteria plus `.github/workflows/fitness-review-reminder.yml` opening issues 7 days before each `fitness_review_due:` date (W3-11), and `CLAUDE.md` reduced from 168 to ≤150 lines via plugin-detail-table extraction to per-plugin `ARCHITECTURE.md` or `governance/plugin-catalog.md` (W3-12),
**So that** the fitness review process is operational + auditable, the retro KPI surfaces token-economy regressions BEFORE they accumulate, and `CLAUDE.md` (loaded on every Claude Code session in this repo) saves ~18 lines per session × thousands of loads.

**Effort**: **M** — three independent surface edits; new GitHub Action with workflow-injection-lint passing (DEFECT-004 regression guard); new governance doc; CLAUDE.md extraction with one-hop discoverability preserved; markdown + YAML.

**Files Touched** (post-Story-5 frontmatter context — Story 6 runs in parallel with Story 5)

- `delivery-team/skills/delivery-flow/references/retrospective-template.md` (or wherever retro template lives; Architect Stage 4 confirmed; Stage 6 Dev re-verifies before edit) — add `context_tokens_per_pipeline_run` KPI section: formula + source-data reference + Δ-vs-prior-5-run-window annotation.
- `governance/fitness-review.md` (new) — cadence (quarterly), owner (delivery-team-leads), inputs (`governance/skill-budgets.json` + telemetry rolling-mean + retro KPIs), outputs (pruning recommendations + budget adjustments + maintainer-rotation), kill-criteria (skills failing fitness 2 quarters in a row).
- `.github/workflows/fitness-review-reminder.yml` (new) — scheduled (cron weekly) GitHub Action; reads `fitness_review_due:` from all SKILL.md frontmatter; opens an issue 7 days before each due date; workflow-injection-lint guard from `.github/workflows/workflow-injection-lint.yml` PASSES (no `${{ github.event.* }}` interpolation in `run:` blocks).
- `CLAUDE.md` — **168 → ≤150** (-18 lines minimum). Plugin-detail tables (delivery-team 11-skill, hardware-team 7-skill, both hooks tables) extracted to per-plugin `ARCHITECTURE.md` or new `governance/plugin-catalog.md`; one-hop link from CLAUDE.md preserved. Opportunistic side-fix: stale `architect/skills/paradigms/` → `architect/paradigms/` per PRD §3 + ADR-tk4-002 §Context.
- Possibly `governance/plugin-catalog.md` (new) — depends on Stage 6 Dev choice between per-plugin ARCHITECTURE.md vs central catalog.
- `delivery-team/ARCHITECTURE.md` and `hardware-team/ARCHITECTURE.md` — extended with the extracted plugin-detail tables if per-plugin route chosen.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-10 AC]** Retro template contains `context_tokens_per_pipeline_run` KPI section with formula + source-data reference; synthesized 5-prior-run dataset triggers correct rolling-mean compute + Δ annotation.
2. **[W3-11 AC-doc]** `governance/fitness-review.md` exists with cadence + owner + inputs + outputs + kill-criteria sections.
3. **[W3-11 AC-workflow]** `.github/workflows/fitness-review-reminder.yml` exists; runs on weekly cron; opens issues for upcoming fitness review dues; workflow-injection-lint guard PASSES (`grep -E '\$\{\{[[:space:]]*github\.event\.' .github/workflows/fitness-review-reminder.yml` returns no `run:`-block matches per DEFECT-004 regression guard).
4. **[W3-12 AC]** `wc -l CLAUDE.md` returns ≤150; plugin-catalog detail still discoverable via one-hop link (`grep -E "ARCHITECTURE.md|plugin-catalog.md" CLAUDE.md` returns ≥1 link); CI lint validates ≤150 (extend `scripts/check_skill_budgets.py` OR add new guard).
5. **[W3-12 AC-side-fix]** Opportunistic fix verified: `grep "architect/skills/paradigms/" CLAUDE.md` returns 0 (stale path corrected to `architect/paradigms/`); cited in PR body as ADR-tk4-002 §Context follow-through.

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-6 — KPI-compute synthetic-data test + workflow-injection-lint regression test + CLAUDE.md line-count + one-hop discoverability traversal.

**Dependencies / Sequencing**: Parallel with Story 5 (no cache-prefix or SKILL.md frontmatter dependency on Story 6 surface). Depends on Stories 1–4 only insofar as Story 6 KPI needs telemetry from Wave 3 dispatches (which are produced by Stories 1–4).

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory (retro template lives in `delivery-flow/references/` — counts as skill-adjacent edit); `plugin-dev:skill-reviewer` post-completion.

**Per-story DoD**: all 5 ACs PASS; `plugin-dev:skill-development` SKILL_LOADED; PR cites BACKLOG-104 §W3-10/11/12 + DEFECT-004 regression-guard verification; DoD review at `.delivery/artifacts/06-development/dod/W3-{10,11,12}-retro-fitness-claudemd.md`.

---

## Story 7 — admin / carry-forward pass (W3-13..W3-18 + skill-budgets.json re-baseline)

**Story**

**As a** delivery-flow validator-template author + CI gate-keeper + Stage-7 entry-step orchestrator + telemetry-hook owner discharging 4 Wave-2 + 2 caveman-lite carry-forwards,
**I want** the standardized validator-prompt template (W3-13), JSON↔Python KNOWN_DEBT consistency lint (W3-14), DoD STATUS-format standardization (W3-15; Architect picked **standardize** at architecture §Open questions #2), pre-merge git hook for skill-budget local check (W3-16), Stage 7 entry-step for stale Wave-N-1 carry-overs (W3-17; Architect picked **Option A — banner each stale file** at architecture §Open questions #3, dogfooded against the live DEFECT-006 instance found at PRD §3), telemetry-hook output capture quality hardening (W3-18; placeholder=true marker route per FR-7.6), and `governance/skill-budgets.json` re-baselined post-Wave-3 (empty `known_debt` or only justified non-delivery-team Wave-4 entries),
**So that** all 6 Wave-3 retro carry-forwards are DISCHARGED on the same wave that produced them, **DEFECT-006 closes** at merge of W3-17, the Stage-6 dogfood data lands on the same run, and the initiative's known-debt registry baselines empty for the first time since BACKLOG-100.

**Effort**: **S-M** — 6 small WIs + 1 housekeeping; each individually trivial but the fan-out is wider than other stories; markdown + Python + YAML + bash hook.

**Files Touched** (post-Stories-1–6 context)

- `delivery-team/skills/delivery-flow/references/validator-prompt-template.md` (new — W3-13) — codifies spec-vs-impl framing block + canonical-path block; referenced from Stage 6 + Stage 7 validator dispatches in `delivery-team/skills/delivery-flow/SKILL.md`.
- `.github/workflows/skill-budget-consistency.yml` (new — W3-14) — validates `governance/skill-budgets.json known_debt[]` vs any hard-coded list in `scripts/check_skill_budgets.py`; workflow-injection-lint PASSES.
- `delivery-team/skills/delivery-flow/SKILL.md` and/or `delivery-team/skills/delivery-flow/references/quality-gates.md` (W3-15) — DoD STATUS-format standardized to single line format (Architect chose standardize over helper at architecture §Open questions #2 by cheapness); STATUS values stay verbatim (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES).
- `governance/pre-commit-skill-budget.sh` (new — W3-16) + `governance/install-pre-commit.sh` (new — W3-16) — opt-in pre-commit hook fails commit when SKILL.md exceeds budget WITHOUT `Budget-Exception:` in commit message.
- `delivery-team/skills/delivery-flow/SKILL.md` Stage 7 entry-step (W3-17) — Architect chose **Option A (banner each stale file)** per architecture §Open questions #3; dogfood target is the live DEFECT-006 instance at `.delivery/artifacts/02-refine/po/prd.md` found at run-start (PRD §3).
- Telemetry hook source under `delivery-team/hooks/` (W3-18; Stage 6 Dev identifies exact file) — `placeholder=true` marker route per PRD §FR-7.6; Story 6 W3-10 KPI compute MUST exclude placeholder rows.
- `governance/skill-budgets.json` (housekeeping) — re-baseline `known_debt[]` post-Wave-3: empty array OR only justified non-delivery-team Wave-4 entries.

**Acceptance Criteria** (5 ACs; runnable; WI-tagged)

1. **[W3-13 + W3-15 AC-validator]** `delivery-team/skills/delivery-flow/references/validator-prompt-template.md` exists with spec-vs-impl framing block + canonical-path block; all current Stage 6 + Stage 7 validator dispatches in `SKILL.md` reference it; STATUS-format standardized (single format) — orchestrator's STATUS-line grep extracts STATUS in 5/5 sample DoD reviews.
2. **[W3-14 + W3-16 AC-CI]** `.github/workflows/skill-budget-consistency.yml` runs on PR + push to main; workflow-injection-lint passes; deliberately-introduced JSON↔Python drift fails the workflow. Pre-commit hook (`governance/pre-commit-skill-budget.sh` + installer) fails commit when SKILL.md exceeds budget without `Budget-Exception:` in message.
3. **[W3-17 AC-defect-006]** Stage 7 entry-step prescribed in `delivery-team/skills/delivery-flow/SKILL.md` with Option A (banner each stale file); synthetic stale Wave-N-1 file at `07-uat/dod/` triggers banner; **DEFECT-006 closes upon merge**; live dogfood: this run's PRD §3 stale-PRD-at-run-start instance is the canonical regression case; Stage 7 of THIS run dogfoods the entry-step.
4. **[W3-18 AC-telemetry]** Telemetry hook either fails-loud OR marks zero-token rows `placeholder=true`; W3-10 retro KPI compute correctly excludes placeholder rows; synthesized missing-measurement scenario produces the chosen behavior.
5. **[Housekeeping AC-known-debt]** `governance/skill-budgets.json known_debt[]` post-Story-7 is empty OR contains only justified non-delivery-team Wave-4 entries; `python3 scripts/check_skill_budgets.py` exits 0 for delivery-team scope; AC-1 from idea-brief §8 / PRD §6 closes.

**Test Strategy reference**: see `.delivery/artifacts/05-plan/qa/test-cases.md` §FR-7 — validator-template framing test + JSON↔Python drift fault-injection + STATUS-grep 5-sample regression + pre-commit hook fail-path test + Stage 7 banner detection on synthetic stale file + DEFECT-006 regression case + telemetry placeholder-row exclusion test.

**Dependencies / Sequencing**: **Last** — sequenced after Stories 1–6 so W3-13 validator template, W3-15 STATUS format, W3-17 Stage 7 entry sweep, and W3-18 telemetry hardening can be dogfooded against live Wave-3 dispatches that produced them. Itself parallel-with-anything (BACKLOG-104 §Story consolidation), but PO sequences terminal for dogfood-data co-landing.

**plugin-dev routing**: `plugin-dev:skill-development` pre-load mandatory (delivery-flow SKILL.md edits in W3-13, W3-15, W3-17); `plugin-dev:skill-reviewer` post-completion; `plugin-dev:plugin-validator` BEFORE PR (CI gate chain).

**Per-story DoD**: all 5 ACs PASS; DEFECT-006 closes; `known_debt[]` empty for delivery-team scope; `plugin-dev:skill-development` SKILL_LOADED; PR cites BACKLOG-104 §W3-13..W3-18 + Architect's chosen options at architecture §Open questions #2 + #3; DoD reviews at `.delivery/artifacts/06-development/dod/W3-{13,14,15,16,17,18}-admin.md`.

---

## Story Map (SM read this last)

| # | Story | Effort | Sequencing | WIs |
|---|-------|--------|------------|-----|
| 1 | architect Tier-B closure | M-L | First | W3-1 |
| 2 | presentation + ui + operations trims | L (3 files parallel-safe) | Parallel after Story 1 | W3-2, W3-3, W3-4 |
| 3 | quality + user-feedback + godot trims (godot to 197) | M | Parallel with Story 2 | W3-5, W3-6, W3-7 |
| 4 | paradigm sub-skill pattern | L | After Stories 1–3 | W3-8 |
| 5 | governance frontmatter rollout | M | **AFTER Stories 1–4** (HARD GATE; tripwire-armed) | W3-9 |
| 6 | retro KPI + fitness review + CLAUDE.md ≤150 | M | Parallel with Story 5 | W3-10, W3-11, W3-12 |
| 7 admin | validator template + CI lints + STATUS standard + git hook + Stage-7 stale-sweep + telemetry hardening + skill-budgets.json re-baseline | S-M | **Last** (dogfood-data co-landing) | W3-13..W3-18 |

**Total**: 7 stories, 35 acceptance criteria across all stories (5 per story × 7 = 35 — covers all 7 PRD FRs explicitly per Plan memory lesson 2). Sprint commitment 78.6% (under 80% ceiling per Plan memory lesson 1). Story 5 mandatory-after-Stories-1-4 (binding); Story 7 last; tripwire-armed before Story 5 per ADR-tk4-003 + architecture §Stop-Rule Tripwire Mechanics.

— Frodo Baggins, PO, run-2026-05-09-tk4. The road is set; the lines are counted; the gates are sharp; the burden is plain. Onward.

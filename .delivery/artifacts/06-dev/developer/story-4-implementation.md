<!-- run: run-2026-05-09-tk4 | stage: 6 (Development, FULL) | story: 4 of 7 | wi: W3-8 | author: Developer (Gimli son of Glóin) | branch: feature/wave-3-tk4 | binding: ADR-tk4-002 -->

# Story 4 Implementation Report — paradigm sub-skill pattern (W3-8)

> "Three axes of sub-skill stone, each split clean by paradigm contract. Two cut new in this swing of the axe; one cut twice over from Story 3; one left whole by ADR conditional. The Fellowship marches on."
> — Gimli, Stage 6 dispatch

**Story**: W3-8 — apply ADR-tk4-002 paradigm sub-skill pattern to research-agent (5 types) + user-feedback (4 personas, joint with Story 3) + presentation (9 types, conditional).
**STATUS**: DONE — all 5 ACs PASS; Option (b) recorded for AC-5 presentation conditional; 5 NEW sub-skills created on research-agent axis.

## 3-Axis Implementation Table

| # | Axis | Parent SKILL.md | Variants | Sub-Skill Paths | Parent Router Status |
|---|------|-----------------|----------|-----------------|----------------------|
| 1 | research-agent research types | `research-agent/SKILL.md` (488 lines, desc 454 chars) | 5: exploratory, descriptive, explanatory, evaluative, comparative | `research-agent/skills/research-types/{exploratory,descriptive,explanatory,evaluative,comparative}/SKILL.md` (5 NEW; 87-114 lines each, all Tier-C ≤200) | Description trimmed 655→454 chars (≤500 ceiling per ADR §Parent skill router contract item 1); +14 lines added at line 57-71 (sub-skill dispatch table after Phase 1, byte offset 3578, BELOW 2k cache-prefix region) |
| 2 | user-feedback persona families | `delivery-team/skills/user-feedback/SKILL.md` (269 lines, desc 434 chars) | 4: gamers, web-app, enterprise, demographic | `delivery-team/skills/user-feedback/skills/personas/{gamers,web-app,enterprise,demographic}/SKILL.md` (4 EXISTING from Story 3 W3-6 joint extraction; frontmatter contract verified) | Already router-shaped by Story 3 (Phase 3 dispatch table at line 99, byte offset 6636 — BELOW cache-prefix region). NO modifications by Story 4 (Story-3 ownership respected per "DO NOT touch other Stories' files"). |
| 3 | presentation 9 types | `delivery-team/skills/presentation/SKILL.md` (182 lines, desc 493 chars) | 9 (sprint-review / feature-pitch / stakeholder-update / technical-deep-dive / investor-pitch / roadmap / product-demo / onboarding / retrospective-summary) | NONE created — references-only path retained (`references/types/<type>.md` ×9 from Story 2 W3-2 sufficient) | Unchanged. Per ADR-tk4-002 §Decision §3 conditional + AC-5 option (b): paradigm sub-skill route deferred to BACKLOG-106+. |

**Total NEW files in Story 4 scope**: 5 (research-agent only).
**Total paradigm sub-skill files post-Story-4 across the 3 axes**: 9 (5 research-types + 4 personas).

## Per-Sub-Skill Frontmatter Contract Compliance (ADR-tk4-002 §Sub-skill SKILL.md frontmatter contract)

All 5 NEW research-agent sub-skills carry the seven-key minimum contract plus `disable-model-invocation: true`:

| File | Lines/Limit | name | disable-model-invocation | tier | parent_skill | axis | variant | license | allowed-tools |
|------|-------------|------|--------------------------|------|--------------|------|---------|---------|---------------|
| `research-agent/skills/research-types/exploratory/SKILL.md` | 93/200 | research-types-exploratory | true | C | research-agent/SKILL.md | research-types | exploratory | Apache 2.0 | yes |
| `research-agent/skills/research-types/descriptive/SKILL.md` | 87/200 | research-types-descriptive | true | C | research-agent/SKILL.md | research-types | descriptive | Apache 2.0 | yes |
| `research-agent/skills/research-types/explanatory/SKILL.md` | 99/200 | research-types-explanatory | true | C | research-agent/SKILL.md | research-types | explanatory | Apache 2.0 | yes |
| `research-agent/skills/research-types/evaluative/SKILL.md` | 112/200 | research-types-evaluative | true | C | research-agent/SKILL.md | research-types | evaluative | Apache 2.0 | yes |
| `research-agent/skills/research-types/comparative/SKILL.md` | 114/200 | research-types-comparative | true | C | research-agent/SKILL.md | research-types | comparative | Apache 2.0 | yes |

Each sub-skill's body loads ONLY its own type-specific output pattern (Discovery Report / Landscape Map / Causal Analysis / Impact Assessment / Decision Matrix) plus type-specific Phase 1-7 adaptations and Integrity Constraints. Parent SKILL.md retains the canonical pattern catalogue for human readers and pre-Story-4 backward compatibility — sub-skill consumers may dispatch directly without re-loading parent pattern templates.

## Cache-Prefix Impact

**NONE on tracked files.** Per ADR-tk4-002 §Cache-prefix impact, this Story is purely structural reorganization:

- `governance/cache-prefix-hash.txt` currently tracks ONLY `delivery-team/skills/delivery-flow/SKILL.md` (single-file scope from ADR-tk3-001). Neither `research-agent/SKILL.md` nor `delivery-team/skills/user-feedback/SKILL.md` is in the tracked scope. AC-4 ("UNCHANGED post-Story-4") is satisfied trivially: zero lines change in the hash file.
- New sub-skill SKILL.md files are NEW files (no prior cache prefix to invalidate).
- Parent router additions land below the 2k-byte cache-prefix region: `research-agent/SKILL.md` dispatch table first row at line 63, byte offset **3578** (1530 bytes BELOW the 2k threshold); `user-feedback/SKILL.md` Story-3 dispatch table first row at line 99, byte offset **6636** (4588 bytes BELOW threshold).
- `research-agent/SKILL.md` description trim (655→454 chars) does touch the cache-prefix region (frontmatter, lines 1-11), but research-agent is not in `governance/cache-prefix-hash.txt`, so AC-4 ruling holds. If Story 5 expands the hash scope to include research-agent, the re-freeze will pick up this trim alongside the +3 governance-frontmatter lines per ADR-tk4-003.

Story 5 (W3-9 governance frontmatter rollout) remains the SOLE cache-prefix re-freeze in this wave per ADR-tk4-003.

## Self-DoD — Story 4 Acceptance Criteria

| AC | Verification Command / Logic | Result |
|----|------------------------------|--------|
| 1 | `find research-agent -path "*/skills/research-types/*/SKILL.md" \| wc -l` → 5; frontmatter contract check across all 5 → ALL OK on disable-model-invocation, tier=C, parent_skill, axis, variant | **PASS** |
| 2 | `find delivery-team/skills/user-feedback -path "*/skills/personas/*/SKILL.md" \| wc -l` → 4; frontmatter contract check across all 4 → ALL OK (created by Story 3 W3-6, verified-only here per joint-AC) | **PASS** (joint with Story 3 AC-2) |
| 3 | `grep -lr "disable-model-invocation: true" --include=SKILL.md` → 9 paradigm sub-skill files matched, ALL match `.*/skills/[^/]+/[^/]+/SKILL\.md`. Zero top-level violations. (Initial trial caught a prose mention in `research-agent/SKILL.md` docs; resolved by rewording prose to avoid the literal `: true` token outside frontmatter — frontmatter-aware lint script recommended for the W3-8 CI workflow.) | **PASS** |
| 4 | `governance/cache-prefix-hash.txt` content unchanged: `f997ec25... delivery-team/skills/delivery-flow/SKILL.md` (1 line). Neither parent in scope — UNCHANGED trivially. | **PASS** |
| 5 | **DECISION: Option (b)** — references-only retained. Rationale: presentation parent already at 182/300 lines (well below Tier-B 300 ceiling) post-Story-2 W3-2 references-only extraction. ADR-tk4-002 §Decision §3 default explicitly favors references-only when Stage 6 finds it sufficient; ADR §Alternatives considered #3 rejected unconditional adoption. Paradigm sub-skill route deferred to BACKLOG-106+. | **PASS** (option b recorded) |

## Plugin-Dev Skill Pre-Load Compliance

- `delivery-team:developer` SKILL_LOADED — emitted at agent start.
- `plugin-dev:skill-development` LOADED — pre-load binding satisfied; 5 new SKILL.md files authored against the skill-development frontmatter + progressive-disclosure contract (Tier-C ≤200, third-person description with trigger phrases, imperative writing style, references to parent/sibling docs).

## Files Changed

**NEW (5 files)**:
- `research-agent/skills/research-types/exploratory/SKILL.md`
- `research-agent/skills/research-types/descriptive/SKILL.md`
- `research-agent/skills/research-types/explanatory/SKILL.md`
- `research-agent/skills/research-types/evaluative/SKILL.md`
- `research-agent/skills/research-types/comparative/SKILL.md`

**MODIFIED (1 file)**:
- `research-agent/SKILL.md` — description trimmed 655→454 chars; +14 lines added at line 57-71 (router dispatch table). Net: 474 → 488 lines (no tier limit applies; not in `delivery-team/` budget scope).

**UNCHANGED but VERIFIED (4 files, joint-AC with Story 3)**:
- `delivery-team/skills/user-feedback/skills/personas/{gamers,web-app,enterprise,demographic}/SKILL.md`

**UNCHANGED by Story 4 design (1 file + 9 deferred)**:
- `delivery-team/skills/presentation/SKILL.md` — references-only path retained per AC-5 option (b).
- `delivery-team/skills/presentation/skills/types/<type>/SKILL.md` ×9 — NOT created (deferred to BACKLOG-106+).

## CI Lint Note (Forward Reference for the W3-8 CI workflow)

The marketplace-discoverability invariant per ADR-tk4-002 currently uses raw `grep -lr "disable-model-invocation: true" --include=SKILL.md`. This caught a prose-only false positive in `research-agent/SKILL.md` during AC-3 verification (a documentation reference inside a sentence, not in frontmatter). Fix shipped: prose reworded to avoid the literal `: true` token outside frontmatter. **Recommended for `.github/workflows/marketplace-discoverability-lint.yml`** (listed in Story 4 Files Touched but typically owned by ops/CI lane): use a frontmatter-aware Python check rather than raw grep, to remove the prose-fragility class. Logged as a non-blocking refinement; Story 4 ACs all pass under either lint shape.

## Budget Check

`python3 scripts/check_skill_budgets.py` → exit 0; 17 files checked, 0 known-debt remaining, 0 exceptions, 0 violations. (research-agent is outside the script's scope; sub-skills follow the Tier-C ≤200 contract verified above.)

## Status

**STATUS: CODE_COMPLETE → DONE** — all 5 ACs PASS; presentation paradigm decision recorded (option b); `plugin-dev:skill-development` SKILL_LOADED; ADR-tk4-002 frontmatter contract honored on every sub-skill; Ruling 2 (marketplace auto-discovery preserved on top-level skills, sub-skill router-dispatched only) honored. Sequencing gate cleared for Story 5.

— Gimli, Developer, run-2026-05-09-tk4. *"Three axes asked. One swung in this story, one already split by another's swing, one left whole by the contract's own clause. Sub-skill stone is laid."*

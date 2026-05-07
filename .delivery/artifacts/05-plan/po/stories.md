<!-- run: run-2026-05-05-tk3 | stage: 05-plan | depth: light | author: Product Owner (Frodo Baggins) | sources: BACKLOG-102, prd.md, ADR-tk3-001, architecture-tk3-caveman-lite.md -->

# Plan — Stories (run-2026-05-05-tk3)

> "I will take the Ring, though I do not know the way."
> — Frodo, accepting the burden plainly.

One Story. One sprint. One PR. The road is short; I will walk it.

## Consolidation Rationale (visible to SM)

BACKLOG-102 names three work items (W2-1 dispatch templates, W2-2 validator template, W2-3 `prose_style` config + schema bump). All three touch overlapping prompt-template surfaces inside `delivery-team/skills/delivery-flow/` — `SKILL.md` (Phase 0 + Phase 4 Step 4), `references/pipeline-stages.md`, `references/quality-gates.md`, `references/config-schema.md`, plus the regenerated `references/config-schema.json` and the `governance/cache-prefix-hash.txt` re-freeze. Splitting forces three serialized PRs against the same Tier-A 500-line file. Per idea-brief §4 and `topics/project-types.md` (story-consolidation-by-file-scope): collapse to ONE Story 1, single developer dispatch, same DoD coverage. Effort calibrated S — markdown edits plus one Python script invocation (`generate-schema.py`) plus one `sha256sum` — one tier below code-effort per Plan memory lesson 3.

### Story 1 — Caveman-Lite Prose Discipline (W2-1 + W2-2 + W2-3)

**Story**

**As a** delivery-flow orchestrator preparing every sub-agent dispatch,
**I want** an opt-outable PROSE STYLE directive in every dispatch prompt (caveman-lite for narrative-framing prose; standard for artifact bodies, FINDINGS, STATUS literals, and the four auto-clarity exempt contexts — security warnings, irreversible-op confirmations, multi-step sequences, user clarifications) plus caveman-lite verdict prose in every DoD validator review file (with STATUS verbatim and FINDINGS preserved as standard prose),
**So that** response-prose tokens shrink ≥20% and DoD review files shrink ≥25% without regressing the 4/7 DoD pass-rate baseline or downstream artifact quality, and so that a single `prose_style: standard` line in `.delivery/config.yml` reverts the behavior cleanly without touching SKILL.md or the cache-prefix hash.

**Effort**: **S** — markdown edits across five reference files plus one Python script invocation (`delivery-team/scripts/generate-schema.py`) plus one `sha256sum` regeneration. Calibrated one tier below code-effort per Plan memory lesson 3 (markdown-only).

**Files Touched** (file-scope consolidation rationale; SM read this first)

- `delivery-team/skills/delivery-flow/SKILL.md` — Phase 0 ≤3 lines added (config-read for `prose_style`; ADR Element 5 budget cap); Phase 4 Step 4 (L329–345) prompt construction edit (conditional PROSE STYLE block injection).
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md` — three dispatch templates (Primary L44, Supporting L87, DoD Validator L130); insert PROSE STYLE block post-`--- ALIAS ---`, pre-`--- OUTPUT ---`, delimiter `--- PROSE STYLE ---` per ADR Element 2.
- `delivery-team/skills/delivery-flow/references/quality-gates.md` — DoD Validator Prompt Template (L21–38): one instructional line directing caveman-lite verdict prose; STATUS verbatim; FINDINGS standard prose (ADR Element 4).
- `delivery-team/skills/delivery-flow/references/config-schema.md` — v2.8 → **v2.9** bump (L5 Current Version, L15 default, schema table gains `prose_style` row, Config File Template L207+ gains `prose_style: caveman-lite` line, Version History L347+ gains v2.9 row).
- `delivery-team/skills/delivery-flow/references/config-schema.json` — regenerated via `python3 delivery-team/scripts/generate-schema.py` after the `.md` edit.
- `governance/cache-prefix-hash.txt` — regenerated after the Phase 0 edit per ADR Element 5; whole-file SHA-256 of `delivery-flow/SKILL.md`; committed in the same PR.
- `.delivery/config.yml` — **no changes required**; v2.7-or-earlier configs auto-load default `caveman-lite` per Phase 0 migration banner.

**Acceptance Criteria** (13 ACs; framed as runnable checks; tagged by WI)

Each AC: "After implementation, the following check passes: `<command>` returns/contains `<value>`."

1. **[W2-1] AC-W2-1-S1** — `grep -c "^PROSE STYLE: caveman-lite for narrative-framing prose ONLY" delivery-team/skills/delivery-flow/references/pipeline-stages.md` returns `3`.
2. **[W2-1] AC-W2-1-S2** — `grep -c "Auto-clarity exemptions apply" delivery-team/skills/delivery-flow/references/pipeline-stages.md` returns `3`.
3. **[W2-1] AC-W2-1-S3** — `grep -nE "PROSE STYLE|prose_style" delivery-team/skills/delivery-flow/SKILL.md` returns at least one match in the L329–345 Step 4 region (Phase 4 prompt construction wiring present).
4. **[W2-2] AC-W2-2-S1** — `grep -nE "STATUS:.*(DONE|NOT_DONE|CODE_COMPLETE)" delivery-team/skills/delivery-flow/references/quality-gates.md` returns at least one match within the L21–38 template block; STATUS values unchanged from baseline (verbatim).
5. **[W2-2] AC-W2-2-S2** — `grep -c "caveman-lite" delivery-team/skills/delivery-flow/references/quality-gates.md` returns `≥ 1` (template instructs validator to use caveman-lite for verdict prose).
6. **[W2-2] AC-W2-2-S3** — `grep -nE "file/line/criterion|name file" delivery-team/skills/delivery-flow/references/quality-gates.md` returns the existing FINDINGS-format directive preserved verbatim (standard prose for findings).
7. **[W2-3] AC-W2-3-S1** — `grep -n "^## Current Version: 2.9" delivery-team/skills/delivery-flow/references/config-schema.md` matches on line 5.
8. **[W2-3] AC-W2-3-S2** — `grep -nE '^\| `prose_style`' delivery-team/skills/delivery-flow/references/config-schema.md` returns one row with type `string`, default `caveman-lite`, valid values `caveman-lite, standard`.
9. **[W2-3] AC-W2-3-S3** — `grep -n '^| 2.9 ' delivery-team/skills/delivery-flow/references/config-schema.md` returns exactly one Version History row dated 2026-05-05.
10. **[W2-3] AC-W2-3-S4** — `python3 -c "import json; d=json.load(open('delivery-team/skills/delivery-flow/references/config-schema.json')); assert 'prose_style' in d['properties']; assert d['properties']['config_version']['default']=='2.9'"` exits 0.
11. **[cross-cutting] AC-CACHE-PREFIX** — `sha256sum delivery-team/skills/delivery-flow/SKILL.md` matches the contents of `governance/cache-prefix-hash.txt` after the Phase 0 edit; both files committed in the same PR.
12. **[cross-cutting] AC-TIER-A-BUDGET** — `python3 delivery-team/scripts/check_skill_budgets.py` exits `0` and `wc -l delivery-team/skills/delivery-flow/SKILL.md` returns `≤ 500`.
13. **[cross-cutting] AC-INITIATIVE-GATES** — All six BACKLOG-102 initiative-level ACs pass post-merge: AC-1 (≥20% response-prose token reduction, telemetry-verified, W2-1), AC-2 (≥25% DoD review file size reduction, W2-2), AC-3 (no DoD pass-rate regression vs 4/7 baseline, joint W2-1+W2-2), AC-4 (no downstream artifact-quality regression, joint), AC-5 (auto-clarity exemptions respected on 3 synthetic dispatches — security warning / `git revert` / 4-step migration, W2-1), AC-6 (`prose_style: standard` opt-out reverts behavior on 3 synthetic dispatches, W2-3). Measurement protocol per PRD §8; runtime evidence captured at Stage 6 dogfood.

**Test Strategy reference**: QA test strategy artifact: `.delivery/artifacts/05-plan/qa/test-strategy.md`.

**Dogfood Plan reference**: Stage 7 UAT owns the empirical measurement protocol per PRD §8.1–8.6 (pre/post telemetry deltas, DoD review byte deltas, auto-clarity exemption check, opt-out check); the actual measurement happens on the next pipeline run AFTER merge, not inside Story 1.

**plugin-dev skill routing constraint** (binding; idea-brief §5): Stage 6 Developer MUST load `plugin-dev:skill-development` BEFORE editing `SKILL.md` or any `references/*.md`; post-completion the developer dispatch MUST invoke `plugin-dev:skill-reviewer` on the modified SKILL.md and `plugin-dev:plugin-validator` on the delivery-team plugin before opening the PR.

**Definition of Done** (binary checklist; validators: SM / QA / Dev / Architect / Tech-Writer)

- [ ] All 13 ACs pass (Dev runs the commands and pastes outputs into the implementation report).
- [ ] `governance/cache-prefix-hash.txt` regenerated post Phase 0 edit and committed in the same PR.
- [ ] Tier-A budget preserved: SKILL.md ≤ 500 lines; `check_skill_budgets.py` exits 0.
- [ ] `references/config-schema.json` regenerated via `generate-schema.py` alongside the `.md` v2.9 bump.
- [ ] caveman-lite directive verified active in one synthetic dispatch transcript with `prose_style: caveman-lite`.
- [ ] Auto-clarity exemption verified in one synthetic destructive-op dispatch transcript (PROSE STYLE block sent; standard-prose security/destructive-op narrative emitted).
- [ ] `prose_style: standard` opt-out verified in one synthetic dispatch transcript (PROSE STYLE block absent; standard-prose narrative emitted).
- [ ] `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` both run clean post-edit.

**Capacity Declaration** (binding for SM downstream; Plan memory lesson 1)

- **Velocity baseline**: 1 Story per sprint for this single-pipeline run (tk3 is a single-wave engagement; baseline is the per-run committed-Story count, not a multi-sprint historical mean).
- **80% ceiling**: honored — 1 Story at Effort S in a single sprint leaves capacity headroom for retro / PR / dogfood overhead; no overcommit possible.
- **Single-sprint commitment**: one S-effort Story = one sprint = within ceiling.

**Stop-rule** (verbatim from idea-brief §9): defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes. Engagement-local (BACKLOG-102 §Stop-rule): Tier-1 measurement <15% prose-token reduction OR any DoD validator missing a finding due to over-compression pauses Tier-2 A/B and triggers a root-cause retro. Both stop-rules armed for this run.

---

STATUS: DONE
ARTIFACT: .delivery/artifacts/05-plan/po/stories.md
SUMMARY: 1 Story (S, W2-1+W2-2+W2-3 consolidated by file-scope), 13 ACs, capacity declared upstream, Tier-A budget + cache-prefix re-freeze gated; the road is short.

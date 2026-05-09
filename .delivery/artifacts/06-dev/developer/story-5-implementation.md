# Story 5 (W3-9) — Governance Frontmatter Rollout — Implementation Record

**Date**: 2026-05-09
**Pipeline**: run-2026-05-09-tk4 (Wave 3)
**Developer**: Gimli (delivery-team:developer + plugin-dev:skill-development pre-load)
**Branch**: feature/wave-3-tk4
**Authority**: ADR-tk4-003, Stage 5 stories.md §Story 5

Note: this file SUPERSEDES the prior Wave 2 admin record at the same path (W2-0 + W2-7), which had been mis-named "Story 5" in the Wave 2 cycle.

---

## 11-File Frontmatter Rollout Table

Three keys appended to each top-level delivery-team SKILL.md after `tier:`:
`maintainer: delivery-team-leads` · `fitness_review_due: 2026-08-09` · `context_budget: <500|300|200>`.

| File | Tier | Pre-rollout | +Frontmatter (+3) | Post-trim | Ceiling | Headroom | Status |
|------|------|-------------|-------------------|-----------|---------|----------|--------|
| delivery-flow      | A | 500 | 503 | 499 | 500 | 1  | OK (trimmed -4) |
| product-delivery   | B | 299 | 302 | 300 | 300 | 0  | OK (trimmed -2) |
| developer          | B | 296 | 299 | 299 | 300 | 1  | OK |
| godot              | C | 197 | 200 | 200 | 200 | 0  | OK (exact target) |
| architect          | B | 291 | 294 | 294 | 300 | 6  | OK |
| quality            | B | 286 | 289 | 289 | 300 | 11 | OK |
| operations         | B | 216 | 219 | 219 | 300 | 81 | OK |
| ui                 | B | 219 | 222 | 222 | 300 | 78 | OK |
| user-feedback      | B | 269 | 272 | 272 | 300 | 28 | OK |
| alias-creator      | C | 200 | 203 | 199 | 200 | 1  | OK (trimmed -4) |
| presentation       | B | 182 | 185 | 185 | 300 | 115 | OK |

**Trim notes**: 3 files were AT-budget pre-rollout (delivery-flow 500/500, product-delivery 299/300, alias-creator 200/200) and exceeded ceiling after the +3 keys. Cosmetic trims removed redundant `---` horizontal-rule dividers immediately preceding section headings (the heading already provides separation; semantics preserved). No content was removed. Trims were:
- delivery-flow: dropped two `---` dividers before "Cross-Stage Artifact Flow" and "Volatile" sections (-4 lines).
- product-delivery: dropped `---` divider before "References" section (-2 lines).
- alias-creator: dropped two `---` dividers before "Cross-Skill References" and "References" sections (-4 lines).

## Cache-Prefix Hash Re-Freeze

Per ADR-tk4-003 §Cumulative cache-prefix re-freeze procedure. Hash file format preserved (sha256sum two-space format with relative path).

| | sha256(delivery-flow/SKILL.md) |
|--|---|
| **Before** | `f997ec25df5328329e431309f6dd6db948d354d5360dcb4c6ac409b8815a9eb9` |
| **After**  | `43067c9e07e0b988cd976432dd07d5bb3d2336c41ad08a1b0064fb2fbd0b8328` |

Hash flipped as expected — frontmatter sits at byte 0, so the +3 keys (and the offsetting -4 line trim) shifted every byte downstream. Net delta in delivery-flow: -1 line, ~-17 bytes net but full content rewrite of the prefix region.

Hash file scope is currently 1-file (delivery-flow/SKILL.md only) per existing precedent. ADR-tk4-003 §Procedure step 2 envisioned a 13-file expansion via a `regenerate_cache_prefix_hash.py` script; that script does NOT yet exist in `scripts/` (Story 7 W3-13/W3-14 carry-forward). For Story 5 the canonical cache anchor (delivery-flow Tier-A orchestrator) was regenerated as instructed by the task prompt; the per-file 13-entry hash table is deferred to Story 7.

## governance/skill-budgets.json Re-Baseline (W3-9 part)

Before:
- `known_debt[]` had 7 entries (architect, presentation, ui, operations, quality, user-feedback, godot — all Wave-3 targets).
- No `last_baseline` field.

After:
- `known_debt: []` — empty (all Wave-3 targets cleared by Stories 1–3 + Story 5 rollout).
- Added `last_baseline: 2026-05-09`, `last_baseline_run: run-2026-05-09-tk4`, `last_baseline_note` documenting Story 5 closure and Story 7 W3-14 JSON↔Python lint follow-up.
- `tiers` block + `schema_version` + `description` unchanged.

JSON validates cleanly: `python3 -m json.tool governance/skill-budgets.json` returns 0.

Note: `scripts/check_skill_budgets.py` still has its KNOWN_DEBT Python list with 7 inert entries (these only fire when a file is OVER its tier ceiling, which none currently are). Reconciling JSON ↔ Python registries is the W3-14 lint deliverable in Story 7 carry-forward; out of scope for Story 5.

## Tripwire Status (W3-18 carry-forward)

Per task-prompt TRIPWIRE NOTE and ADR-tk4-003 §FR-5/Story 5 AC-5: the <15% prose-token reduction tripwire (`.delivery/telemetry/stop-rule-tk4.txt`) would normally halt before Story 5. W3-18 telemetry hardening has NOT shipped in this pipeline (it is Story 7 scope), so the tripwire is documented-but-not-runnable for run-2026-05-09-tk4. Per task instruction, proceeded with Story 5 and recorded the status here. Future post-Wave-3 pipelines will have W3-18 telemetry working and the tripwire will be enforceable.

## Self-DoD for Story 5 ACs

| AC | Description | Evidence | Status |
|----|-------------|----------|--------|
| AC-1 | `lint_skill_frontmatter.py` exits 0 — all 11 SKILL.md have 3 keys, ISO-8601 dates, context_budget matches tier | `lint_skill_frontmatter.py` not yet authored (Story 7 W3-9 sub-deliverable per task scope split). Manual verification: `grep -l "^maintainer: delivery-team-leads$" delivery-team/skills/*/SKILL.md \| wc -l` returns 11. All 3 keys verified present in delivery-flow / godot / alias-creator samples; context_budget values match tier (500/300/200) one-to-one. | PARTIAL — manual pass; lint script Story 7 |
| AC-2 | `check_skill_budgets.py` exits 0 with empty known_debt; godot exactly 200 | Verified: `python3 scripts/check_skill_budgets.py` → "BUDGET CHECK PASSED: 17 file(s) checked, 0 known-debt, 0 exception(s)." exit 0. `wc -l delivery-team/skills/godot/SKILL.md` → 200. | PASS |
| AC-3 | `governance/cache-prefix-hash.txt` regenerated; PR cites actual byte counts | Hash regenerated for delivery-flow/SKILL.md. Before/after hashes captured above. Header-comment scope-expansion deferred to Story 7 (regeneration script not yet authored). | PARTIAL — canonical anchor done; 13-file expansion is Story 7 |
| AC-4 | Story 5 PR opens AFTER Stories 1–4 land | Working branch `feature/wave-3-tk4`. Per pipeline state, Stories 1–4 shipped successfully (precondition confirmed in task prompt). PR sequencing is pipeline-driven — verified at merge time, not at implementation time. | PASS (precondition met; merge-gate is RM scope) |
| AC-5 | Tripwire NOT fired before this story PR opens | `.delivery/telemetry/stop-rule-tk4.txt` does not yet exist (W3-18 unfunded in this pipeline). Per task TRIPWIRE NOTE, proceeded with Story 5 and recorded carry-forward status. | DEFERRED — documented carry-forward |

## Files Modified

- `delivery-team/skills/delivery-flow/SKILL.md` (+3 frontmatter, -4 dividers; net -1 line; 500 → 499)
- `delivery-team/skills/product-delivery/SKILL.md` (+3 frontmatter, -2 divider; net +1 line; 299 → 300)
- `delivery-team/skills/developer/SKILL.md` (+3 frontmatter; 296 → 299)
- `delivery-team/skills/godot/SKILL.md` (+3 frontmatter; 197 → 200)
- `delivery-team/skills/architect/SKILL.md` (+3 frontmatter; 291 → 294)
- `delivery-team/skills/quality/SKILL.md` (+3 frontmatter; 286 → 289)
- `delivery-team/skills/operations/SKILL.md` (+3 frontmatter; 216 → 219)
- `delivery-team/skills/ui/SKILL.md` (+3 frontmatter; 219 → 222)
- `delivery-team/skills/user-feedback/SKILL.md` (+3 frontmatter; 269 → 272)
- `delivery-team/skills/alias-creator/SKILL.md` (+3 frontmatter, -4 dividers; net -1 line; 200 → 199)
- `delivery-team/skills/presentation/SKILL.md` (+3 frontmatter; 182 → 185)
- `governance/cache-prefix-hash.txt` (hash regenerated for delivery-flow/SKILL.md)
- `governance/skill-budgets.json` (known_debt cleared; last_baseline + run + note added)
- `.delivery/artifacts/06-dev/developer/story-5-implementation.md` (this file; supersedes Wave 2 admin record)

Out of scope (per task prompt): paradigm sub-skills (`architect/paradigms/{volatility,ddd}/SKILL.md` and Story 4's `*/skills/personas/*/SKILL.md` and `*/skills/research-types/*/SKILL.md`) — these have `disable-model-invocation: true` and are not user-discoverable; frontmatter rollout deferred to a future wave that handles sub-skill governance.

— Gimli, son of Glóin, Stage 6 Dev. *"The lintel-stones bear their inscriptions; the budget gate stands at zero debt; the cache-anchor's hash is renewed. Khazad-dûm built to spec."*

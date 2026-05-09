<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | wave: 3 — governance | author: Saruman of Many Colours, Solution Architect | DoD: Dev runs-the-command (cache-prefix-impacting) -->

# ADR-tk4-003 — Governance Frontmatter Shape and Cumulative Cache-Prefix Re-Freeze

**Status**: Accepted
**Date**: 2026-05-09
**Pipeline**: `run-2026-05-09-tk4`
**Owner**: Solution Architect (Saruman)
**DoD validator (binding)**: Dev runs-the-command at Architect DoD per caveman-lite Hot Lesson #1 extension. This ADR is **cache-prefix-impacting**; the `governance/cache-prefix-hash.txt` regeneration MUST be empirically verified, not narratively claimed.

---

## Context

W3-9 (BACKLOG-104) installs three new frontmatter keys on every delivery-team SKILL.md to operationalize the quarterly fitness review process (W3-11) and make the line-budget self-checking (Ruling 3). The keys are:

- `maintainer:` — github-handle or team-id of the owner accountable for fitness review and budget compliance.
- `fitness_review_due:` — ISO-8601 date (YYYY-MM-DD) of next quarterly fitness review.
- `context_budget:` — integer line cap, redundant with the existing `tier:` key but explicit (so a CI lint does not need a tier-to-line lookup).

Frontmatter sits at byte 0 of every SKILL.md, **above the Phase 0 / Phase 1 router region**. Adding three lines to frontmatter shifts every byte of every SKILL.md downward by ~50 bytes (3 lines × ~17 bytes/line average). The cache-warmup prefix slice (bytes 0..2048) is invalidated on every SKILL.md that takes the new frontmatter.

PRD §3 confirmed: **no SKILL.md in delivery-team currently has a `## Phase 0` header**; the byte-stable cache-prefix region today IS the frontmatter block (lines 1–11 in most files; lines 1–28 in heavy-frontmatter files like `architect/paradigms/volatility/`). W3-9 therefore mutates the cache-prefix region by definition.

The Wave 0 mandatory-rollout-side-effect lesson is binding: W3-9 MUST run AFTER W3-1..W3-7 content trims, because adding ~3 lines to a file already AT-budget pushes it over. Sequencing recorded in PRD §FR-5 + Stage 5 stories.md.

---

## Decision

### Frontmatter contract

Every delivery-team SKILL.md gets these three keys appended to existing frontmatter:

```yaml
maintainer: <github-handle-or-team-id>     # e.g., "delivery-team-leads"
fitness_review_due: <YYYY-MM-DD>           # e.g., "2026-08-09" (90 days from rollout)
context_budget: <integer>                  # matches tier: (A=500, B=300, C=200)
```

Default values for Wave 3 rollout:
- `maintainer: delivery-team-leads` (single-team default; staggering by individual maintainer is a future refinement).
- `fitness_review_due: 2026-08-09` (rollout date 2026-05-09 + 90 days; per FR-5.4, staggering acceptable to avoid synchronized renewal storm — Stage 6 may distribute dates across an 80–100-day window).
- `context_budget: 500` for Tier-A files; `300` for Tier-B; `200` for Tier-C.

CI lint (W3-9 deliverable) validates: presence + well-formedness of all three keys + `context_budget` matches tier (A=500/B=300/C=200) + `fitness_review_due` parses as ISO-8601 date.

### Cumulative cache-prefix re-freeze procedure

W3-9 is the SOLE Wave 3 WI that touches the cache-prefix region. ADR-tk4-001 confirmed all extractions in W3-1..W3-7 land at line ranges ≥111 in every file (well below the 2k-byte prefix region). Therefore the cumulative re-freeze is **W3-9-scoped only**; the W3-1..W3-7 content trims do NOT contribute to the prefix delta.

**Byte-impact math** (per-file, applied across all delivery-team SKILL.md):

- Frontmatter delta per file: `+3 lines × ~17 bytes/line ≈ +50 bytes`
- Files affected (all delivery-team SKILL.md, including paradigm sub-skills if any take frontmatter rollout): `delivery-flow + product-delivery + developer + godot + architect + quality + operations + ui + user-feedback + alias-creator + presentation = 11 top-level + 2 paradigm legacy (architect/paradigms/{volatility,ddd}) = 13 files`
- Cumulative byte shift: `+50 bytes × 13 files = +650 bytes` (per Wave 3 task spec math)
- Cache-warmup prefix slice (0..2048 per file) is invalidated on every one of the 13 files. One-time re-warm cost = 13 × 2KB ≈ 26KB total cold-cache read on the first Wave 3 dispatch after merge.

**Procedure**:

1. W3-9 Story 5 ships frontmatter additions to all 13 files **after** W3-1..W3-7 have landed in the working tree (Wave 0 sequencing lesson).
2. Stage 6 Dev (per binding caveman-lite Hot Lesson #1 extension) **runs the command**:
   ```bash
   python3 scripts/regenerate_cache_prefix_hash.py --target governance/cache-prefix-hash.txt --files delivery-team/skills/*/SKILL.md delivery-team/skills/*/paradigms/*/SKILL.md
   ```
   (Or the equivalent enumeration of all 13 SKILL.md files. Existing `governance/cache-prefix-hash.txt` covers `delivery-flow/SKILL.md` only per ADR-tk3-001 precedent; this wave **expands the hash file's scope** to cover all Tier-A and Tier-B SKILL.md files in delivery-team. Schema extension recorded in `governance/cache-prefix-hash.txt` header comment.)
3. Stage 6 DoD validator MUST cite the regenerated hash file's actual byte counts, NOT the +650-byte projection. Caveman-lite caught a byte-offset INVERSION in tk3 because the architect cited a position from the wrong file; this DoD gate is binding.
4. `governance/cache-prefix-hash.txt` updated **ONCE at end of Story 5** (not per-file, not per-Story-1..4 trim). PRD §NFR-2 confirms the one-time re-warm cost is accepted.

### Justification for accepting the one-time re-warm cost

Cumulative token reduction from Wave 3 trims (~1,100 lines × ~12 tokens/line ≈ 13,200 tokens removed from the cache-warmup prefix surface across 7 SKILL.md files) **vastly exceeds** the one-time 26KB cold-cache re-warm cost (~6,500 tokens). At the Wave 3 dispatch volume (>5 dispatches per pipeline, dozens of pipelines per quarter), payback is on dispatch #1.

### Mandatory-rollout sequencing (binding Wave 0 lesson)

W3-9 MUST NOT begin until W3-1..W3-8 have landed in the working tree. Frontmatter adds ~3 lines/file; running W3-9 BEFORE the trims means targeting fictional ≤297/≤197 ceilings instead of canonical ≤300/≤200. Stage 5 stories.md records Story 5 (W3-9) as gated on Stories 1–4 completion. This sequencing is a **hard gate** — NOT a soft preference — because skipping it would re-introduce known_debt entries that the wave is supposed to clear.

### Post-Story-5 budget verification (round-2 addition; QA Gate 4 closure)

After Story 5 lands frontmatter on all 13 files, Stage 6 Dev MUST run:

```bash
python3 scripts/check_skill_budgets.py
```

and confirm exit 0 BEFORE the Story 5 PR merges. ADR-tk4-001 round-2 revision lands godot at 197 (not 198) so the frontmatter +3 holds the Tier-C ceiling EXACTLY at 200. The other 6 in-scope files clear with headroom ≥9 lines (architect 291/300; ui 276/300; operations 258/300; quality 279/300; user-feedback 253/300; presentation ~163/300). Post-Wave-3 `governance/skill-budgets.json known_debt` MUST be empty; any non-empty `known_debt` entry blocks AC-1.

---

## Consequences

**Positive**:
- Operationalizes the quarterly fitness review process (W3-11). Maintainer and review-due fields are machine-readable for the GitHub Action that opens reminder issues.
- `context_budget` makes the line-budget CI lint single-pass: lint reads frontmatter, compares to `wc -l`, no tier-to-line lookup table needed.
- One-time re-warm cost is scoped, measurable, and ADR-justified (matches ADR-tk3-001 precedent).
- Hash file scope expansion (delivery-flow only → all 13 delivery-team SKILL.md) catches future cache-prefix drift across the full plugin, not just the orchestrator.

**Negative**:
- All 13 delivery-team SKILL.md files take a one-time +50-byte frontmatter shift; first Wave 3 dispatch after merge incurs the 26KB cold-cache cost.
- `maintainer:` field is initially homogeneous (`delivery-team-leads`); stagger and individual-maintainer assignment is W4 follow-up.
- Hash file regeneration is now a 13-file enumeration; if a 14th SKILL.md is added without updating the hash-regeneration command, the new file is silently uncovered until the next CI gate update.

**Reversibility**: removing the three frontmatter keys reverses to byte 0; cache-prefix re-warms once more on rollback. Mechanical, not free.

---

## Alternatives considered

1. **Single combined `governance:` block instead of three separate keys** (e.g., `governance: {maintainer: …, due: …, budget: 500}`). Rejected: nested YAML is harder to grep, harder to lint, and breaks the single-line-per-field convention used elsewhere in delivery-team frontmatter (e.g., `tier:`, `pattern_library_version:`, `model_awareness:`).

2. **Defer cache-prefix re-freeze to next ADR after Wave 3 ships** (treat W3-9 as no-cache-impact, audit later). Rejected: directly violates Ruling 1 and the caveman-lite Hot Lesson #1 extension. Cache-prefix invariants are not an audit trail; they are a binding contract enforced at Architect DoD.

3. **Skip `context_budget:` (redundant with `tier:`)**. Rejected: redundancy is the point. CI lint and grep-based budget checks become single-pass when the line cap is explicit. Tier-to-line lookup adds a hidden invariant.

4. **Apply frontmatter to ALL plugins' SKILL.md, not just delivery-team**. Rejected per BACKLOG-104 §Out of scope (delivery-team-first). Architect Stage 4 considered — ROI is not clean for plugins not yet in the token-economy initiative; defer to BACKLOG-105+.

5. **Use semantic versioning instead of `fitness_review_due:` date**. Rejected: dates are calendar-driven (quarterly cadence per W3-11); SemVer is release-driven. Mismatch.

---

## References

- Ruling 1 (cache-prefix freeze): `.delivery/memory/topics/skill-token-economy.md`
- Caveman-lite Hot Lesson #1 extension (Dev runs-the-command for cache-prefix-impacting ADRs): `.delivery/memory/stages/architect.md` lesson #6
- Wave 0 mandatory-rollout-side-effect lesson: BACKLOG-100 retro
- ADR-tk3-001 (caveman-lite cache-prefix re-freeze precedent): `.delivery/artifacts/04-architect/adrs/`
- W3-9 sequencing gate: PRD §FR-5
- Hash file: `governance/cache-prefix-hash.txt`
- W3-11 fitness review process: BACKLOG-104 §Story 6
- Verified line counts: PRD §3

— Saruman of Many Colours, Architect, run-2026-05-09-tk4. *"Frontmatter sits at byte 0; the cache pays at byte 0; therefore the hash regenerates at byte 0. Run the command."*

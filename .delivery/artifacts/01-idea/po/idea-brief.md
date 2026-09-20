<!-- run: run-2026-05-28-backlog-108 -->
## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-05-28
**Pipeline**: run-2026-05-28-backlog-108
**Initiative**: Opus 4.8 Migration (BACKLOG-108)
**Stage 3 Design**: SKIP — DX-only, no UX surface
**Backlog Reference**: BACKLOG-108-opus-4-8-migration.md — to be authored at Stage 2 (Refine). This is a forward reference. The file does not exist yet. Stage 2 creates it.

*Spoken by Gandalf the Grey.*

> A wizard is never stale, nor current. He ships precisely the model the world now runs on. This session runs on Opus 4.8. The plugins still claim 4.7. That ends today.

---

### Problem Statement

The repo holds 34 SKILL.md files. Of those, 25 carry a `model_awareness:` stamp set to 4.7 (7 × `opus-4-7`, 19 × `opus-4-7-frontmatter-only`). The other 9 carry no stamp at all. Stamps are stale or absent.

Hard `claude-opus-4-7` model-ID strings live in FIVE source files, not one:
- `agentic-flow-builder/scripts/agent_registry.py:190` — heavy-tier registry config
- `prompt-engineer/SKILL.md:368` — `MODEL_ID = "claude-opus-4-7"` code literal inside a keystone SKILL.md
- `delivery-team/tests/smoke/tests/conftest.py` — 4 fixture model strings (lines 105, 117, 129, 151)
- `delivery-team/architecture/smoke-test-architecture.md:115` — example model string in a code fence

A CI guard already gates these strings. `.github/workflows/stale-model-id-guard.yml` exists today and currently allowlists `claude-opus-4-7`. Once inverted, every 4.7 literal trips it.

This session runs on `claude-opus-4-8`. 4.8 dispatches fewer sub-agents by default than 4.7. It follows instructions more literally. A multi-agent plugin suite that dispatches on behavioral assumptions baked for 4.7 ships degraded quality on the model the world actually uses.

Stale stamps are a lie. Lies compound. Fix now.

---

### Proposed Solution

Seven stories in strict dependency order (BINDING-2.5 governs keystone-first sequencing):

| Story | Scope | What |
|-------|-------|------|
| S1 | CI guard | **Rewrite** existing `.github/workflows/stale-model-id-guard.yml` — invert the allowlist to permit only `claude-opus-4-8` / `claude-sonnet-4-6` / `claude-haiku-4-5-20251001`; make `claude-opus-4-7` a trigger |
| S2 | Keystone prose | 3 keystone SKILL.md files: delivery-flow, prompt-engineer, product-delivery — full prose review + 4.8 dispatch guidance. Includes fixing `prompt-engineer/SKILL.md:368` `MODEL_ID` code literal (not stamp-only) |
| S3 | Full prose sweep | Remaining 31 SKILL.md files — full prose review (no frontmatter-only pass; BINDING-2.2 is clear). 9 of these get a NEW `model_awareness` stamp created |
| S4 | Code IDs | `agentic-flow-builder/scripts/agent_registry.py` heavy-tier update + provenance comment; smoke-test fixture/example sites (`conftest.py` 4 hits, `smoke-test-architecture.md` 1 hit) |
| S5 | Smoke harness | Extend runner: add confirmed-observable metrics + best-effort fields; update `--effort xhigh` invocation |
| S6 | Cache re-freeze | Re-fingerprint `governance/cache-prefix-hash.txt`; ADR-4-8-001 records scope decision |
| S7 | Memory + changelog | Binding memory update; CHANGELOG entry; squash-rebase + ff-merge + push origin/main (no PR) |

**Stamp accounting.** 34 files get a full prose review. 25 existing stamps get UPDATED to 4.8. 9 stamp-less sub-skill files (4 user-feedback personas + 5 research-types) get a NEW stamp CREATED. Stamping is in scope for all 34 — full prose review covers every file, so every file gets a stamp for consistency. None scoped out.

The 9 currently-unstamped files:
```
delivery-team/skills/user-feedback/skills/personas/{demographic,enterprise,gamers,web-app}/SKILL.md
research-agent/skills/research-types/{comparative,descriptive,evaluative,explanatory,exploratory}/SKILL.md
```

Stamps (`model_awareness: opus-4-8`, `pattern_library_version: 4-8-1`, `last_audited: 2026-05-28`) applied AFTER prose edits pass DoD — not before.

**Plugin-dev skill routing** (CLAUDE.md binding):
- SKILL.md edits → `plugin-dev:skill-development` must be acknowledged before any SKILL.md edit begins
- Hook edits → `plugin-dev:hook-development` if any hook file is touched
- This routing is non-optional; Developer DoD includes evidence of acknowledgment

---

### Success Criteria

Seven measurable ACs — all must pass before squash commit:

1. **CI guard rewritten and exits 0 on clean tree.** The inverted `stale-model-id-guard.yml` permits only 4.8/sonnet-4-6/haiku-4-5; `claude-opus-4-7` triggers failure. On the migrated tree, `grep -rn "claude-opus-4-7"` (excluding `.delivery/`) returns only the single permitted provenance comment in `agent_registry.py`. All five prior literal sites are migrated.
2. **All 34 SKILL.md files carry `model_awareness: opus-4-8`.** Assert a COUNT, not just a value filter: `grep -rl "model_awareness: opus-4-8" . --include="SKILL.md" | wc -l` returns **34**. AND `grep -rh "model_awareness:" . --include="SKILL.md" | grep -v "opus-4-8" | wc -l` returns **0** (no stale or `-frontmatter-only` values remain). This proves both the 25 updates and the 9 creations landed.
3. **All 34 SKILL.md prose reviewed.** No `-frontmatter-only` marker present anywhere. Each file shows evidence of a full prose pass in the commit diff.
4. **`agent_registry.py` heavy-tier ID is `claude-opus-4-8`.** Provenance comment `# prior: claude-opus-4-7 (retired 2026-05-28, BACKLOG-108)` immediately follows — this is the one permitted 4.7 string the guard allows.
5. **Smoke harness captures 5-sample baseline against `claude-opus-4-8`.** `baselines/hello_world_spike.json` shows `model: claude-opus-4-8`, `n_samples: 5`, `sample_status: active`, populated `last_captured_utc` and `last_captured_git_sha`.
6. **Line budgets pass.** `python scripts/check_skill_budgets.py` exits 0. No tier violation introduced by prose additions.
7. **Behavioral claims doc-verified.** Zero provisional behavioral text in shipped files. Adversarial reviewer independently re-fetches ≥3 load-bearing claims from `https://docs.anthropic.com/en/docs/about-claude/models/overview`.

---

### Scope

**In scope:**
- All 34 SKILL.md files — full prose review. 25 stamp updates + 9 stamp creations.
- `.github/workflows/stale-model-id-guard.yml` — **rewrite existing guard** (invert allowlist). Not a new file.
- `agentic-flow-builder/scripts/agent_registry.py:190` — heavy-tier model ID update + provenance comment
- `prompt-engineer/SKILL.md:368` — `MODEL_ID = "claude-opus-4-7"` code literal fix (distinct from its frontmatter stamp)
- `delivery-team/tests/smoke/tests/conftest.py` — 4 fixture model strings (lines 105, 117, 129, 151)
- `delivery-team/architecture/smoke-test-architecture.md:115` — example model string in code fence
- `delivery-team/tests/smoke/` — runner extension (confirmed-observable metrics + best-effort fields + `--effort xhigh`)
- `baselines/hello_world_spike.json` — baseline invalidation and re-capture
- `governance/cache-prefix-hash.txt` — re-fingerprint
- ADR-4-8-001 — cache-prefix scope decision record
- Binding memory update (`opus-4-8-migration.md`) and CHANGELOG entry

**Out of scope:**
- `prd-quality-gate-flow/` routing alias strings (version-agnostic labels; BINDING-1.4 exempts them)
- `.github/workflows/smoke-*.yml` — CI runners lack `claude` CLI; smoke tests are local-only (BINDING-4.6)
- Any PR — ship pattern is squash-rebase + ff-merge + push origin/main (BINDING-5.1)

---

### Constraints

1. **Plugin-dev skill routing** — CLAUDE.md is explicit. SKILL.md edits route through `plugin-dev:skill-development`. Hook edits route through `plugin-dev:hook-development`. No bypass.
2. **Budget cap** — ~$15 total for 5-sample baseline capture (~$3 cap per sample). Smoke runner enforces `--cost-cap 3.00` per run.
3. **Behavioral claims must be doc-verified** — BINDING-3.1 through BINDING-3.3 are non-negotiable. No provisional text ships. Source: `https://docs.anthropic.com/en/docs/about-claude/models/overview`.
4. **Line budgets enforced** — Tier A=500, Tier B=300, Tier C=200. Prose additions must stay within tier. Violations require `Budget-Exception:` in commit body and `known_debt[]` entry with `target_wave:`.
5. **One Role = One Sub-Agent** — BINDING-5.4. Fused role dispatches fail DoD regardless of artifact quality.
6. **No dual-allow transition window** — CI guard ships on the allowlist pattern from day one. No period where both 4.7 and 4.8 are permitted simultaneously (BINDING-2.1).
7. **Producer-validator separation** — smoke-test fixture authors cannot be the same dispatch as `metrics.py` / `baseline.py` authors (BINDING-4.5).

---

### Risks

| # | Risk | Mitigation |
|---|------|-----------|
| R1 | **Self-referential dispatch** — pipeline runs on 4.8 while editing docs that warn 4.8 against under-dispatch; executor may under-dispatch per its own behavioral patterns | One Role = One Sub-Agent invariant (BINDING-5.4); QA validator enumerates role-dispatch correspondence explicitly; DoD fails on fused dispatch |
| R2 | **Keystone prose accuracy** — 4.8 behavioral claims may diverge from doc at time of writing | Adversarial reviewer re-fetches ≥3 load-bearing claims independently (BINDING-3.2); no provisional text ships (BINDING-3.3) |
| R3 | **Aggressive smoke fields unobservable** — `thinking_tokens`, `stop_details` refusal codes, speed indicators may not surface in all response shapes | Best-effort fields emit WARN (not FAIL) when absent (BINDING-4.2); confirmed-observable fields always present |
| R4 | **Cache-prefix fingerprint scope** — full prose review of 34 SKILL.md files may expand fingerprint set beyond prior scope (delivery-flow only) | ADR-4-8-001 is the binding decision record (BINDING-5.5); Architect owns scope decision before re-fingerprint runs |
| R5 | **Hidden 4-7 literals trip the rewritten guard at squash** — the guard rewrite plus five known literal sites means one missed site fails CI at ff-merge time | Pre-squash `grep -rn "claude-opus-4-7"` sweep (excluding `.delivery/`) that the QA validator runs independently before ff-merge; only the one permitted provenance comment may remain |

---

### Stop-Rule

Defects/story > 0.4 across any 3-story window pauses the initiative. Current rolling rate = 0.111 (well under threshold, inherited from run-2026-05-13-tk5).

---

— Gandalf, PO, run-2026-05-28-backlog-108. The model has moved on. The plugins have not yet. That is the only problem worth solving today.

# BACKLOG-108 — Opus 5 migration

**Type**: FEATURE
**Pipeline**: run-2026-05-28-backlog-108
**Created**: 2026-05-28 (retargeted to Opus 5: 2026-09-19)
**Status**: IN PROGRESS
**Priority**: HIGH — repo declares a retired model on the model the world now runs on
**PO**: Gandalf
**Binding context**: `.delivery/memory/topics/opus-5-migration.md` (AUTHORITATIVE)
**Stop-rule baseline**: defects/story = 0.111 (well under 0.4 threshold)

## Summary

This session runs on `claude-opus-5`. The repo still declares 4.7. The repo holds 34 SKILL.md files; 25 carry a stale `model_awareness:` 4.7 stamp (7 × `opus-4-7`, 19 × `opus-4-7-frontmatter-only`), 9 carry no stamp. Hard `claude-opus-4-7` ID strings live in 5 files (9 hits, including the guard yml; 7 hits in 4 files outside it). A CI guard (`.github/workflows/stale-model-id-guard.yml`) currently allowlists 4.7; once inverted, every 4.7 literal trips it.

This initiative migrates the whole repo to `claude-opus-5`: invert the guard to a positive allowlist, full prose review of all 34 SKILL.md files, stamp all 34 to opus-5 (25 updated + 9 created), migrate the 5 code/doc literal sites, extend the smoke harness for Opus 5 metrics + `--effort xhigh`, re-capture a 5-sample baseline against `claude-opus-5`, re-fingerprint the cache prefix, and ship via squash-rebase + ff-merge + push origin/main (no PR). All behavioral claims about Opus 5 are doc-verified against Anthropic docs; no provisional text ships.

## Discovery (verified 2026-09-19)

- `find . -name SKILL.md | wc -l` = **34**
- `grep -rl "model_awareness" . --include="SKILL.md" | wc -l` = **25**
- Live `claude-opus-4-7` literal sites (non-`.delivery/`): 9 hits in 5 files (guard yml included) via the canonical count command in the PRD (section 1); 7 hits in 4 files excluding the guard yml being rewritten in S1.

## Work Items (7 stories)

| Story | Surface | Effort | Closes gate |
|-------|---------|--------|-------------|
| S1 | `.github/workflows/stale-model-id-guard.yml` | S | G1 |
| S2 | 3 keystone SKILL.md + `prompt-engineer/SKILL.md:368` | M | G7 |
| S3 | remaining 31 SKILL.md (prose + 9 new stamps) | L | G2, G3 |
| S4 | `agent_registry.py` + `conftest.py` + `smoke-test-architecture.md` | M | G4 |
| S5 | `delivery-team/tests/smoke/` runner extension + baseline | M | G5 |
| S6 | `governance/cache-prefix-hash.txt` + ADR-5-0-001 | S | — (blocks ship) |
| S7 | memory + CHANGELOG + squash/ff/push | S | — (blocks ship) |

### S1 — CI guard rewrite (S)
**Files**: `.github/workflows/stale-model-id-guard.yml` (REWRITE existing — not new).
**Acceptance**: positive allowlist permits only `claude-opus-5` / `claude-sonnet-4-6` / `claude-haiku-4-5-20251001`; `claude-opus-4-7` triggers failure; no dual-allow window (BINDING-2.1); static grep job, no `claude` CLI (BINDING-5.2). Route hook/workflow edits per CLAUDE.md.

### S2 — Keystone prose (M)
**Files** (BINDING-2.5 order): `delivery-team/skills/delivery-flow/SKILL.md`, `prompt-engineer/SKILL.md` (incl. `:368` `MODEL_ID` code literal -> `claude-opus-5`), `delivery-team/skills/product-delivery/SKILL.md`.
**Acceptance**: full prose review; Opus 5 dispatch guidance uses only doc-verified behavior (Opus 5 delegates to subagents more readily than prior models; steer or cap delegation) (PRD Citations); no provisional text (BINDING-3.3); edits acknowledged through `plugin-dev:skill-development` first (CLAUDE.md). Stamps applied AFTER prose passes DoD.

### S3 — Full prose sweep (L)
**Files**: remaining 31 SKILL.md. The 9 currently-unstamped:
```
delivery-team/skills/user-feedback/skills/personas/{demographic,enterprise,gamers,web-app}/SKILL.md
research-agent/skills/research-types/{comparative,descriptive,evaluative,explanatory,exploratory}/SKILL.md
```
**Acceptance**: full prose review of every file (BINDING-2.2; no frontmatter-only pass); 9 NEW stamps created, remaining 16 stale stamps updated; all 34 carry `model_awareness: opus-5`, `pattern_library_version: 5-0-1`, `last_audited: 2026-09-19` (BINDING-2.3); zero `-frontmatter-only` markers remain. Edits route through `plugin-dev:skill-development`.

### S4 — Code IDs (M)
**Files**: `agentic-flow-builder/scripts/agent_registry.py:190`; `delivery-team/tests/smoke/tests/conftest.py:105,117,129,151`; `delivery-team/architecture/smoke-test-architecture.md:115`.
**Acceptance**: registry heavy-tier ID -> `claude-opus-5` + provenance comment `# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)` (BINDING-2.4 — the one permitted 4.7 string); 4 fixture strings + 1 doc example string -> `claude-opus-5`. Provenance comment sits on the line immediately above the registry line (PRD D2-1 reconciliation). Fixture edits authored in a SEPARATE dispatch from `metrics.py`/`baseline.py` (BINDING-4.5).

### S5 — Smoke harness (M)
**Files**: `delivery-team/tests/smoke/` (runner + metrics + baseline); `baselines/hello_world_spike.json`.
**Acceptance**: confirmed-observable metrics always tracked (`tokens.cache_hit_ratio`, `model_usage.<model>.dispatches`) per BINDING-4.1; best-effort metrics (`thinking_tokens`, `stop_details` refusal codes, speed/`fast`) WARN-not-FAIL on null (BINDING-4.2); runner adds `--effort xhigh` (BINDING-4.3; valid on Opus 5 but not the doc-recommended start, see PRD OQ-5); baseline marked `invalidated-model-migration` before edits, then live 5-sample `--init-baseline` against `claude-opus-5` with `last_captured_utc`, `last_captured_git_sha`, `n_samples: 5`, `model: claude-opus-5`, `sample_status: active` (BINDING-4.4); per-run `--cost-cap 3.00`.

### S6 — Cache re-freeze (S)
**Files**: `governance/cache-prefix-hash.txt`; ADR-5-0-001.
**Acceptance**: re-`sha256sum` after all SKILL.md edits final (BINDING-5.3); ADR-5-0-001 records whether full-prose-review of 34 files expands the fingerprint set beyond prior scope, the included file set, and the new hash (BINDING-5.5); Architect owns the ADR, Developer implements without re-debate (BINDING-5.6). ADR committed in the same squash commit.

### S7 — Memory + changelog + ship (S)
**Files**: `.delivery/memory/topics/opus-5-migration.md`; `CHANGELOG.md`.
**Acceptance**: memory updated with run outcome; CHANGELOG BACKLOG-108 entry; ship via squash-rebase + ff-merge + push origin/main, no PR (BINDING-5.1); guard validates the single squash commit only (never a partial mid-merge state).

## File Surface Inventory

| Path | Status | Story | Notes |
|------|--------|-------|-------|
| `.github/workflows/stale-model-id-guard.yml` | EDIT | S1 | invert allowlist |
| `delivery-team/skills/delivery-flow/SKILL.md` | EDIT | S2 | keystone 1 (DISP-01) |
| `prompt-engineer/SKILL.md` | EDIT | S2 | keystone 2; `:368` `MODEL_ID` literal + 2 stamps (`:6`, `:415`) |
| `delivery-team/skills/product-delivery/SKILL.md` | EDIT | S2 | keystone 3 |
| 31 × remaining SKILL.md | EDIT | S3 | full prose + stamp; 9 NEW stamps |
| `agentic-flow-builder/scripts/agent_registry.py` | EDIT | S4 | `:190` heavy-tier + provenance comment |
| `delivery-team/tests/smoke/tests/conftest.py` | EDIT | S4 | 4 fixture strings `:105,117,129,151` |
| `delivery-team/architecture/smoke-test-architecture.md` | EDIT | S4 | `:115` example string |
| `delivery-team/tests/smoke/lib/metrics.py` | EDIT | S5 | confirmed + best-effort fields |
| `delivery-team/tests/smoke/lib/baseline.py` | EDIT | S5 | invalidate + re-capture |
| `delivery-team/tests/smoke/run_smoke.py` | EDIT | S5 | `--effort xhigh` |
| `delivery-team/tests/smoke/baselines/hello_world_spike.json` | EDIT | S5 | 5-sample re-capture |
| `governance/cache-prefix-hash.txt` | EDIT | S6 | re-fingerprint |
| ADR-5-0-001 | NEW | S6 | cache-prefix scope decision (Architect, Stage 4) |
| `.delivery/memory/topics/opus-5-migration.md` | EDIT | S7 | run outcome |
| `CHANGELOG.md` | EDIT | S7 | BACKLOG-108 entry |

## Acceptance Criteria (summary; the runnable, authoritative ACs are in PRD Revision 2 — `.delivery/artifacts/02-refine/po/prd.md`)

- **AC-1** (S1): `grep -rn "claude-opus-4-7" . --include="*.py" --include="*.md" --include="SKILL.md" | grep -v "\.delivery/" | grep -v "# prior: claude-opus-4-7" | wc -l` == 0; guard names the three allowlist IDs.
- **AC-2** (S3): `grep -rl "model_awareness: opus-5" . --include="SKILL.md" | wc -l` == 34 AND `grep -rh "model_awareness:" . --include="SKILL.md" | grep -v "opus-5" | wc -l` == 0.
- **AC-3** (S3): `grep -rn "frontmatter-only" . --include="SKILL.md" | wc -l` == 0; commit diff shows prose-body edit per file.
- **AC-4** (S4): `agent_registry.py` heavy-tier == `claude-opus-5` with provenance comment present.
- **AC-5** (S5): `baselines/hello_world_spike.json` -> `model: claude-opus-5`, `n_samples: 5`, `sample_status: active`, populated `last_captured_utc` + `last_captured_git_sha`.
- **AC-6** (S2+S3): `python3 scripts/check_skill_budgets.py` exits 0.
- **AC-7** (S2): zero provisional/hedged behavioral text; adversarial reviewer re-fetches >= 3 load-bearing claims independently.
- **AC-DISP** (all): dispatch count == stage `dod_validators` length; fused roles fail DoD.

## Budget

~**$15** baseline-capture envelope (5 samples × ~$3 cap). Runner enforces hard `--cost-cap 3.00` per run; 30-min wall-clock ceiling; concurrency-of-1 on `--init-baseline`.

## Constraints

- **C-01** Plugin-dev skill routing non-optional (CLAUDE.md): SKILL.md -> `plugin-dev:skill-development`; hooks/workflows -> `plugin-dev:hook-development`.
- **C-02** Behavioral claims doc-verified (BINDING-3.1–3.3). No provisional text ships. Source: `https://platform.claude.com/docs/en/about-claude/models/overview`.
- **C-03** Line budgets A=500 / B=300 / C=200. Violations need `Budget-Exception:` + `known_debt[]` with `target_wave:`.
- **C-04** One Role = One Sub-Agent (BINDING-5.4). Fused dispatches fail DoD.
- **C-05** No dual-allow transition window (BINDING-2.1). Guard ships allowlist from day one.
- **C-06** Producer-validator separation for smoke meta-tests (BINDING-4.5).
- **C-07** No new CLI deps in AC commands — bash / python-stdlib only.
- **C-08** Local-only: no workflow shells out to `claude` (BINDING-5.2, BINDING-4.6).

## Out of Scope

- `prd-quality-gate-flow/` routing aliases (BINDING-1.4 — version-agnostic labels, not stale).
- Any `.github/workflows/smoke-*.yml` (BINDING-4.6 — CI lacks `claude` CLI).
- Any PR (BINDING-5.1 — squash + ff-merge + push only).

## Stop-rule

Defects/story > 0.4 across any 3-story window pauses the initiative. Current rolling rate = 0.111.

## References

- Binding decisions: `.delivery/memory/topics/opus-5-migration.md`
- PRD: `.delivery/artifacts/02-refine/po/prd.md`
- Constraints: `.delivery/artifacts/02-refine/po/constraints.yml`
- Idea brief: `.delivery/artifacts/01-idea/po/idea-brief.md`
- Anthropic models overview: `https://platform.claude.com/docs/en/about-claude/models/overview`
- Migration guide: `https://platform.claude.com/docs/en/about-claude/models/migration-guide`
- Effort parameter: `https://platform.claude.com/docs/en/build-with-claude/effort`
- Prior wave precedent: BACKLOG-106 (run-2026-05-13-tk5), BACKLOG-100..104 squash-ship pattern

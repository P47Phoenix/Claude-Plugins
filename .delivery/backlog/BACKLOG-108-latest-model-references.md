# BACKLOG-108 — Latest-model references (remove version pinning)

**Type**: FEATURE
**Pipeline**: run-2026-05-28-backlog-108
**Created**: 2026-05-28 (retargeted to Opus 5: 2026-09-19; reframed 2026-09-20)
**Status**: IN PROGRESS
**Priority**: HIGH — every model release forces a repo-wide migration; this ends it
**PO**: Gandalf
**Binding context**: `.delivery/memory/topics/latest-model-references.md` (AUTHORITATIVE; Section 0)
**Stop-rule baseline**: defects/story = 0.111 (well under 0.4 threshold)

## Summary

User decision (2026-09-20, binding): "We should just say latest version of model X." The repo stops hard-pinning model version strings (`claude-opus-4-7`, `claude-opus-5`, ...) and refers to the latest version of a family ("latest Opus"). This replaces the earlier plan to pin `claude-opus-5`. Opus 5 is the effective current model; it appears only in dated citations and in observed smoke baselines.

Today: 34 SKILL.md; 25 carry versioned stamps (26 `model_awareness` lines: 7 `opus-4-7`, 19 `opus-4-7-frontmatter-only`; 26 `pattern_library_version: 4-7-1` lines); 9 carry none. Model-version prose (including bare "4.7") sits on 19 lines in 3 files (delivery-flow, prompt-engineer, and `delivery-team/references/shared/orchestrator-doctrine.md`). 20 pin lines in 6 files under the Revision 4 contract (guard yml and registry comments included; 14 hits in 6 files under the narrower Revision 3 count). The CI guard enforces a version allowlist that must be edited on every release, and (Revision 4) runs only on `pull_request` although ship is a direct push to main.

This initiative: invert the guard to forbid pins; make stamps and prose version-free; define tier labels ONCE as Claude Code aliases (`opus`, `sonnet`, `haiku`) in `MODEL_TIER_ALIAS`; replace test and doc literals with synthetic IDs; extend the smoke harness to run `--model opus` and record the concrete model that actually ran; re-capture a 5-sample baseline; re-fingerprint the cache prefix; ship via squash-rebase + ff-merge + push origin/main (no PR). Behavioural claims stay doc-verified and are written version-free.

## Discovery (verified 2026-09-20; canonical commands in the PRD section 1)

- `find . -name SKILL.md | wc -l` = **34**; stamp census `26 25 {...frontmatter-only: 19, opus-4-7: 7}`
- Canonical count (PRD section 1, Revision 4 contract, no exemptions): `guard-scope hits 91 files 31` = pin 20 + stamp 52 + prose 19 (target `guard-scope hits 0 files 0`)
- Real `stream-json` capture (CLI 2.1.278): model is top-level in `system/init`, `message.model` in assistant events; the current parser reports model `unknown` and cost 0.0 on it (PRD S5)
- Claude Code aliases `opus`/`sonnet` = latest; API has no evergreen alias for current models (PRD section 8)

## Work Items (7 stories)

| Story | Surface | Effort | Closes gate |
|-------|---------|--------|-------------|
| S1 | `scripts/check_model_pins.py` + fixtures (PIN/STAMP/PROSE/BARE contract, no exemptions) + `.github/workflows/stale-model-id-guard.yml` (push to main, pull_request, workflow_dispatch) + `.githooks/pre-commit` call | S | G1 |
| S2 | 3 keystone SKILL.md + `orchestrator-doctrine.md` mirror + `prompt-engineer/SKILL.md:368` config-read snippet | M | G7 |
| S3 | all 34 SKILL.md prose; version-free stamps on the 25 stamped files | L | G2, G3, G6 |
| S4 | `agent_registry.py` `MODEL_TIER_ALIAS` + `conftest.py` + `smoke-test-architecture.md` + `telemetry-schema.md` | M | G4, G-LIT |
| S5 | `delivery-team/tests/smoke/` `--model`/`--effort`/`--strict-model`, real-shape parser fix and fixture, resolved-model capture (never `unknown`), baseline | M | G5 |
| S6 | `governance/cache-prefix-hash.txt` + cache-fingerprint ADR | S | G9 |
| S7 | memory + CHANGELOG + squash/ff/push + dispatch manifests | S | G8, G10 |

Acceptance criteria are authoritative in the PRD (`.delivery/artifacts/02-refine/po/prd.md`, Revision 4), one runnable AC per FR. Ship path: local `python3 scripts/check_model_pins.py` gate, then squash-rebase + ff-merge + push origin/main, no PR.

## Budget

~**$15** baseline-capture envelope (5 samples x ~$3 cap). Hard `--cost-cap 3.00` per run; 30-min wall-clock ceiling; concurrency 1.

## Constraints

- **C-01** Plugin-dev skill routing non-optional: SKILL.md -> `plugin-dev:skill-development`; hooks/workflows -> `plugin-dev:hook-development`.
- **C-02** Behavioural claims doc-verified (BINDING-3.1 to 3.3), written version-free.
- **C-03** Line budgets A=500 / B=300 / C=200.
- **C-04** One Role = One Sub-Agent (BINDING-5.4).
- **C-05** Guard ships in final form from day one; squash before merge.
- **C-06** Producer-validator separation for smoke meta-tests (BINDING-4.5).
- **C-07** No new CLI deps in AC commands.
- **C-08** Local-only: no workflow shells out to `claude`.

## Out of Scope

- `prd-quality-gate-flow/` routing aliases (BINDING-1.4).
- Any `.github/workflows/smoke-*.yml` (BINDING-4.6).
- Any PR (BINDING-5.1).
- Creating stamps in the 9 unstamped SKILL.md.

## Stop-rule

Defects/story > 0.4 across any 3-story window pauses the initiative. Current rolling rate = 0.111.

## References

- Binding decisions: `.delivery/memory/topics/latest-model-references.md`
- PRD: `.delivery/artifacts/02-refine/po/prd.md`
- Constraints: `.delivery/artifacts/02-refine/po/constraints.yml`
- Claude Code model aliases: `https://code.claude.com/docs/en/model-config`
- Model IDs and versioning: `https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions`
- Prior wave precedent: BACKLOG-106 (run-2026-05-13-tk5), BACKLOG-100..104 squash-ship pattern

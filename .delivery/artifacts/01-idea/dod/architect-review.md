# Architect DoD Review — Caveman-Lite Idea-Brief (run-2026-05-05-tk3)

**Reviewer**: Solution Architect (DoD validator, Stage 1 round 1)
**Date**: 2026-05-05
**Pipeline**: run-2026-05-05-tk3
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Mode**: light (round 1 of max 2)

## STATUS: NOT_DONE

## Findings

- **Criterion 1 — Plugin-dev:skill-development acknowledged: PASS.** §5 line 49 explicitly binds `plugin-dev:skill-development` pre-load at the Stage 6 developer dispatch and adds `plugin-dev:skill-reviewer` + `plugin-dev:plugin-validator` post-completion. Routing table §7 line 64 reinforces. Memory lesson honored.

- **Criterion 2 — Ruling 1 cache-prefix invariant + Stage 4 ADR routing: PASS.** §6 (lines 51-53) is a dedicated call-out naming `ADR-tk3-001` as owner of any re-freeze, requires byte enumeration if prefix bytes move, references `governance/cache-prefix-hash.txt`, and mandates CI hash-check. §7 line 62 routes Stage 4 as "light w/ **ADR-tk3-001**" — the light-with-ADR routing is visible.

- **Criterion 3 — Technical surface accurately identified: NOT_PASS.** §4 line 32 enumerates Phase 0 config-read, Step 4 prompt construction, `references/pipeline-stages.md`, `references/quality-gates.md`, and `references/config-schema.md` v2.7→v2.8 — five of the six required surfaces are present. The sixth, **`config-schema.json` regenerate**, is missing: §4 line 32 only names the `.md` schema bump, and §6 line 53 references only the `.md` artifact. Per the gate criterion ("If any of those surfaces are missing, NOT_DONE"), schema bumps in this repo require both the prose `config-schema.md` change AND a regenerated `config-schema.json` (validator toolchain artifact per CLAUDE.md "Config validation toolchain: JSON Schema generation + validation scripts"). Cite: `.delivery/artifacts/01-idea/po/idea-brief.md:32`. Also note: §4 names `pipeline-stages.md` but does not call out that **three** dispatch-template families live there (agent prompts, DoD validator prompts, and stage-summary prose) — naming the file is sufficient under criterion 3's surface-enumeration requirement, so this sub-point passes; the `.json` omission is what blocks.

- **Criterion 4 — Stop-rule preserves historical continuity: PASS.** §9 line 84 reproduces the canonical threshold verbatim: "defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes." Matches Wave 0/1/2 stop-rule and the binding rule in `skill-token-economy.md` line 127. The engagement-local stop-rule on §9 lines 86 (telemetry <15% reduction or quality regression) is additive, not a substitute — both are armed (line 88), which is correct.

- **Criterion 5 — Does not over-specify ADR-tk3-001 territory: PASS.** §6 line 53 explicitly hands "enumerate the bytes that move, justify, update the hash" to `ADR-tk3-001`, not the brief. §3 states intent (5 surfaces a–e) and §8 quotes BACKLOG-102 acceptance gates verbatim, but the brief does not pin (a) where in SKILL.md the PROSE STYLE block sits, (b) the precedence order for `prose_style:` resolution (project config vs role override vs dispatch-time override), or (c) the exact verdict-prose grammar. Intent + constraints, no contract pre-decided.

## Verdict

The brief is well-formed across four of five criteria — plugin-dev routing, cache-prefix invariant with ADR-tk3-001 ownership, stop-rule continuity, and Stage-4 architectural restraint are all explicit and well-cited. The single blocker is §4's omission of `config-schema.json` regeneration alongside the `config-schema.md` v2.7→v2.8 bump; this is a required surface in this repo's config-validation toolchain, not an implementation detail Stage 4 can recover. Recommended fix: add `config-schema.json` to §4 line 32's surface list and to §7 Stage 5 Plan (or Stage 6 Dev) routing notes — single-line edit, no scope change.

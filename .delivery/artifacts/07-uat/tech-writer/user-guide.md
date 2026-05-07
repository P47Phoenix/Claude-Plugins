---
title: "Contributor Guide — `prose_style` config key (run-2026-05-05-tk3)"
stage: 07-uat
author: Bilbo Baggins (operations skill, tech-writer role)
created: 2026-05-05
pipeline_id: run-2026-05-05-tk3
audience: future delivery-team contributors and project maintainers
prerequisite_knowledge: familiarity with `.delivery/config.yml` and the delivery-flow pipeline
supersedes: prior tk2 user-guide (2026-05-03)
---

# Contributor Guide: `prose_style` config key

## Where the key lives

`.delivery/config.yml` — top-level, not nested under `pipeline:`. Top-level matches consumption scope: read at delivery-flow Phase 0, before pipeline-loop keys, and influences dispatch construction across all seven stages. `wizard_completed` is the precedent.

```yaml
config_version: "2.9"
prose_style: caveman-lite
pipeline:
  # …
```

## Valid values

| Value | Effect |
|---|---|
| `caveman-lite` (default) | Inject the PROSE STYLE directive block into every agent dispatch and every DoD validator dispatch. |
| `standard` | Omit the block entirely. Dispatches return to the pre-merge baseline prose style. |

Any other value is a config-validation error at Phase 0. The schema enum lives in `delivery-team/skills/delivery-flow/references/config-schema.json` and is documented in `references/config-schema.md`.

## Opt out per project

Add a single top-level line to that project's `.delivery/config.yml`:

```yaml
prose_style: standard
```

Reverts dispatch behavior on the next pipeline invocation. No SKILL.md edit, no hash regeneration. AC-6 of BACKLOG-102 satisfied by this construction.

If `.delivery/config.yml` is at v2.7 or v2.8 and `prose_style:` is absent, Phase 0 auto-migrates to v2.9 with `prose_style: caveman-lite` as default and surfaces the standard upgrade banner. v2.6-or-earlier configs follow the existing strip-and-default migration path; the `prose_style` default is layered on top.

## How auto-clarity works

The PROSE STYLE block embedded in every dispatch prompt names four exempt contexts:

1. Security warnings (e.g., world-readable credentials, exposed secrets, vulnerable dependency).
2. Irreversible or destructive operation confirmations (e.g., `git revert`, `rm -rf`, `git push --force`, schema migrations dropping data).
3. Multi-step sequences where fragment ordering or omitted conjunctions would risk misread.
4. User clarification responses.

The agent itself is the detector. There is no orchestrator-side classifier, no per-dispatch flag. The directive instructs the agent to revert to standard prose during generation when one of the four contexts applies. ADR-tk3-001 Element 3 records this choice and the rejected alternatives.

## Canonical PROSE STYLE block location

The verbatim block text lives at `delivery-team/skills/delivery-flow/references/prose-style.md` — the single source of truth. The orchestrator's Step 4 dispatch construction reads this fixture and injects it between the `--- ALIAS ---` and `--- OUTPUT ---` delimiters of the dispatch template, with delimiter `--- PROSE STYLE ---`. The three dispatch templates in `references/pipeline-stages.md` (Primary L44, Supporting L87, DoD Validator L130) each carry the verbatim block as the canonical fixture.

If the block text needs to change, edit `prose-style.md` only. Do not edit inlined copies elsewhere.

## Per-dispatch override

Per-dispatch override is **not supported in v1**. `prose_style` applies uniformly across every role at every stage of a given pipeline invocation. Per ADR-tk3-001 Element 2, this is intentional scope: there is no Wave 4 telemetry yet to identify a role for which caveman-lite degrades signal quality, so `prose_style.overrides: { <role>: standard }` is deferred to BACKLOG-103+ and revisited only if telemetry shows a problem role.

## Where to look when something behaves oddly

| Symptom | First place to look |
|---|---|
| Dispatch prompts look unchanged after merge | `grep "^prose_style:" .delivery/config.yml` — likely set to `standard` |
| Cache hash mismatch warning at Phase 0 | `governance/cache-prefix-hash.txt` vs `sha256sum delivery-team/skills/delivery-flow/SKILL.md` |
| DoD validator missing findings | Verdict prose may be over-compressing; `.delivery/artifacts/<NN>-<stage>/dod/<role>-review.md` is the evidence; if missing, BACKLOG-102 stop-rule fires |
| Schema validation failure on `prose_style` | Value not one of `caveman-lite, standard`; check `config-schema.json` enum |

## Related authoritative documents

- ADR-tk3-001 — full contract for all six elements (config key, block, auto-clarity, validator treatment, re-freeze, schema bump).
- BACKLOG-102 — initiative-level ACs and stop-rule. PRD — discovery-grounded file:line evidence; validator-framing split.
- `plugin-dev:skill-development` — authoring conventions for `delivery-flow/SKILL.md` edits.

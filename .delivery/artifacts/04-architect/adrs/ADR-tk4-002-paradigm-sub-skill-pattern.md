<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | wave: 3 — paradigm | author: Saruman of Many Colours, Solution Architect -->

# ADR-tk4-002 — Paradigm Sub-Skill Pattern Contract

**Status**: Accepted
**Date**: 2026-05-09
**Pipeline**: `run-2026-05-09-tk4`
**Owner**: Solution Architect (Saruman)
**Supersedes**: none
**Superseded by**: none

---

## Context

Ruling 2 (`.delivery/memory/topics/skill-token-economy.md` §"Pattern: Paradigm sub-skill") permits — and now requires — a Skill-within-Skill pattern for axes with **≥3 mutually-exclusive variants**. Two reference implementations already exist on main:

- `delivery-team/skills/architect/paradigms/volatility/SKILL.md` (frontmatter `tier: C`, `disable-model-invocation` not yet present)
- `delivery-team/skills/architect/paradigms/ddd/SKILL.md`

These were authored before Ruling 2's `disable-model-invocation: true` clause was binding, and they sit under `paradigms/` (no `skills/` intermediate directory). Wave 3 must:

1. Codify the canonical directory shape and frontmatter contract for new paradigm sub-skills.
2. Apply it to three Wave 3 axes (W3-8 in BACKLOG-104):
   - **research-agent** (5 research types — verified path: top-level repo `/research-agent/SKILL.md`, no `skills/` subtree yet).
   - **user-feedback** (4 persona families: gamers / web-app / enterprise / demographic — existing top-level `delivery-team/skills/user-feedback/SKILL.md`).
   - **presentation** (9 presentation types — *conditional*: if Stage 6 measures the `references/types/<type>.md` route from ADR-tk4-001 W3-2 sufficient on its own, presentation stays references-only and does NOT take the paradigm sub-skill pattern this wave).
3. Preserve marketplace auto-discovery (Ruling 2 invariant: top-level skills MUST stay discoverable).

The existing `architect/paradigms/{volatility,ddd}/` precedent is the seed. CLAUDE.md currently documents this path as `architect/skills/paradigms/` — that is stale and resolved opportunistically in W3-12 (out-of-scope here).

---

## Decision

### Canonical directory shape

For axes meeting the ≥3-mutually-exclusive-variant threshold:

```
<plugin>/
├── SKILL.md                          # Top-level router (marketplace-discoverable)
└── skills/
    └── <axis>/
        └── <variant>/
            ├── SKILL.md              # Sub-skill (disable-model-invocation: true)
            └── references/
                └── <variant-detail>.md
```

For Wave 3 specifically:

| Axis | Path |
|---|---|
| research-agent research types | `research-agent/skills/research-types/<type>/SKILL.md` (5 sub-skills) |
| user-feedback persona families | `delivery-team/skills/user-feedback/skills/personas/<family>/SKILL.md` (4 sub-skills) |
| presentation types (conditional) | `delivery-team/skills/presentation/skills/types/<type>/SKILL.md` (9 sub-skills) — ONLY if Stage 6 finds references-only insufficient |

### Architect paradigms (volatility / ddd) backlog

The existing `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md` precedent is **explicitly grandfathered for this wave**. Migrating them to `architect/skills/paradigms/<paradigm>/` is mechanical (path move + add `disable-model-invocation: true` frontmatter key) but out of Wave 3 scope per BACKLOG-104 §Out of scope. Log as W4 follow-up.

### Sub-skill SKILL.md frontmatter contract

Required keys on every paradigm sub-skill:

```yaml
---
name: <axis>-<variant>            # e.g., personas-gamers
description: <≤500 char description, see Ruling 2>
disable-model-invocation: true    # MANDATORY — prevents marketplace auto-discovery
tier: C                           # All paradigm sub-skills are Tier-C ≤200
parent_skill: <plugin>/<top-level-skill-name>
axis: <axis-name>                 # e.g., personas, research-types
variant: <variant-name>           # e.g., gamers, academic
license: Apache License 2.0 - See repository LICENSE file
allowed-tools: [Read, Edit, Write, Bash, Skill, ToolSearch]
---
```

The existing `architect/paradigms/volatility/SKILL.md` frontmatter (`paradigm_id`, `display_name`, `shared_refs`, `task_types`) is a more elaborate variant of this shape; it is permitted. The minimum contract is the seven keys above plus `disable-model-invocation: true`.

### Parent skill router contract

Every parent skill that owns a paradigm axis MUST:

1. Keep its top-level `description:` field ≤500 chars (Ruling 2 sub-clause; verified by CI lint chain).
2. Implement Phase 1 router that detects the variant from user input or pipeline context.
3. Phase 2 dispatch loads the matched sub-skill via `Skill` tool with `<plugin>:<axis>-<variant>` skill name; sub-skill loads ONLY its own `references/` (no parent-context bleed).
4. Sub-skill discovery is **router-driven only** — `disable-model-invocation: true` blocks the marketplace from auto-suggesting sub-skills directly to the user.

### Marketplace discoverability invariant (Ruling 2)

CI lint validates: `grep -l "disable-model-invocation: true" $(find . -name SKILL.md)` returns ONLY paths matching the regex `.*/skills/[^/]+/[^/]+/SKILL.md` (paradigm sub-skill shape) or the grandfathered `.*/paradigms/[^/]+/SKILL.md` (legacy architect shape). Any top-level plugin SKILL.md flagged as non-discoverable fails the lint.

---

## Cache-prefix impact

**NONE.** This ADR is structural re-organization. New sub-skill SKILL.md files are NEW files (no existing prefix to invalidate). Parent skills (research-agent, user-feedback, presentation-conditional) get content REMOVED via the W3-1..W3-7 extractions in ADR-tk4-001 — those extractions are confirmed to land below the cache-prefix region (Phase 1 router and below; line ranges ≥111 in every file). Adding a router pointer line to dispatch to the sub-skill costs ~1 line per axis at ~position 100, well below the 2k-byte cache-prefix region.

`governance/cache-prefix-hash.txt` does NOT update from this ADR. ADR-tk4-003 (W3-9 frontmatter rollout) owns the sole cache-prefix re-freeze in this wave.

---

## Consequences

**Positive**:
- Token economy: each paradigm sub-skill loads ONLY when its variant is selected. For research-agent at 5 variants, average dispatch loads 1/5 of the type-specific content; for user-feedback at 4 variants, 1/4; for presentation at 9 variants (if adopted), 1/9.
- Marketplace UX: top-level skills stay discoverable; users see "research-agent" not 5 cluttering entries. Sub-skills are router-dispatched only (Ruling 2 invariant).
- Pattern reusability: future axes (developer 14-language, architect 11-role per BACKLOG-106+) follow the same canonical shape with no further architectural debate.
- Codifies the directory shape that CLAUDE.md currently documents incorrectly (`architect/skills/paradigms/` typo); W3-12 fix lands the canonical path.

**Negative**:
- File count grows: research-agent +5, user-feedback +4, presentation +9 (conditional) = 9–18 new SKILL.md files.
- Each sub-skill needs `references/` and a router round-trip; small-axis cases (e.g., a future 3-variant axis) may not amortize the dispatch overhead vs `references/<variant>.md` route.
- Two patterns now coexist: paradigm sub-skill (this ADR) and reference-only contract extraction (ADR-tk4-001 W3-1..W3-5, W3-7). Decision rule for future axes: ≥3-mutually-exclusive-variants → paradigm sub-skill; <3 OR variants share substantial code → reference extraction.

**Reversibility**: each sub-skill can be flattened back into the parent SKILL.md by appending the sub-skill's content under a `## <Variant>` section. Reversal cost is mechanical but re-grows the cache-warmup prefix.

---

## Alternatives considered

1. **Skip the directory shape change for research-agent** (treat all paradigm sub-skills as `<plugin>/skills/<variant>/SKILL.md` with no `<axis>/` intermediate). Rejected: scales poorly when a plugin owns ≥2 paradigm axes (e.g., a future architect plugin with paradigms axis + roles axis would collide).

2. **Use `references/` only across all 3 Wave 3 axes** (no paradigm sub-skill). Rejected: this is what user-feedback's `references/persona-library.md` already does, and it loads the entire library on every dispatch. Telemetry from W0-1 (per binding memory) shows persona-library is the second-largest reference load in user-feedback. Sub-skill split is the surgical fix.

3. **Adopt paradigm sub-skill on all three Wave 3 axes unconditionally** (no presentation conditional). Rejected: presentation already lands at ≤300 via ADR-tk4-001 W3-2 references-only path. Adding 9 sub-skills when references-only meets the budget violates "smallest reversible step" (refine memory lesson). Stage 6 measures the dispatch shape and decides; default = references-only.

4. **Migrate architect/paradigms/{volatility,ddd}/ in this wave**. Rejected per BACKLOG-104 §Out of scope; out-of-scope but logged as W4 candidate.

---

## References

- Ruling 2 (paradigm sub-skill pattern): `.delivery/memory/topics/skill-token-economy.md` §Pattern: Paradigm sub-skill
- Existing precedent: `delivery-team/skills/architect/paradigms/{volatility,ddd}/SKILL.md`
- BACKLOG-104 §W3-8: paradigm sub-skill pattern across research-agent + presentation + user-feedback
- PRD §FR-4 + §3 (research-agent path verification): `.delivery/artifacts/02-refine/po/prd.md`
- ADR-tk4-001: per-file extraction strategy (this ADR's complement for non-paradigm axes)

— Saruman of Many Colours, Architect, run-2026-05-09-tk4. *"Many are my paths, and many lead to the same SKILL.md. Some lead through references; the wisest, when warranted, lead through sub-skills."*

<!-- run: run-2026-05-09-tk4 | stage: 6 (Development, FULL) | story: 4 of 7 (W3-8) | role: Technical Writer (FRESH) | task: dod-validation | round: 1 -->

# Story 4 — Technical Writer DoD Review (Round 1)

**Pipeline**: run-2026-05-09-tk4
**Story**: W3-8 — paradigm sub-skill pattern (research-agent + user-feedback joint + presentation conditional)
**ADR binding**: ADR-tk4-002 (Paradigm sub-skill pattern, Ruling 2)
**Reviewer**: Technical Writer, fresh context
**SKILL_LOADED**: `delivery-team:operations`

> Role: Technical Writer | Task: dod-validation | References: documentation-standards.md (loaded for sub-agent context — sub-skills are documentation artifacts evaluated for well-formed markdown, router-dispatch pattern, marketplace registration correctness, and reachability)

---

## Artifacts In Scope

Per the Story 4 implementation report (`.delivery/artifacts/06-dev/developer/story-4-implementation.md`) the audit surface is:

- **5 NEW sub-skills (Story-4-owned)**: `research-agent/skills/research-types/{exploratory,descriptive,explanatory,evaluative,comparative}/SKILL.md`
- **4 EXISTING sub-skills (joint-AC verification with Story 3 W3-6)**: `delivery-team/skills/user-feedback/skills/personas/{gamers,web-app,enterprise,demographic}/SKILL.md`
- **2 parent routers**: `research-agent/SKILL.md`, `delivery-team/skills/user-feedback/SKILL.md`
- **1 design-deferred path (option b)**: `delivery-team/skills/presentation/SKILL.md` — references-only retained, no sub-skills under `skills/types/`
- **Marketplace registry**: `.claude-plugin/marketplace.json`

Total = 9 paradigm sub-skill SKILL.md files reviewed structurally.

---

## Gate Criterion 1 — Sub-skill SKILL.md files are well-formed markdown

**Evidence**: For each of the 9 sub-skill SKILL.md files I inspected:

| Check | Method | Result |
|---|---|---|
| Frontmatter delimiter pair (`---` open + close) | `grep -c "^---$"` per file → expected 2 | **9/9 = 2 delimiters each** |
| First line is `---` | `head -1` per file | **9/9 PASS** |
| Required frontmatter keys present (`name`, `description`, `license`, `disable-model-invocation`, `tier`, `parent_skill`, `axis`, `variant`) | direct read of each file | **9/9 PASS** (all 8 keys present; the 5 research-types files additionally carry `allowed-tools`) |
| H1 heading present after frontmatter | direct read | **9/9 PASS** ("# Exploratory Research Sub-Skill", "# Gamer Personas Sub-Skill", etc.) |
| Tables render (pipe-table syntax balanced) | direct read of "Personas Covered", "Framework Selection", "Decision Matrix" tables | **9/9 PASS** — all tables have header row + alignment row + data rows |
| Code fences balanced (each ``` opens + closes) | direct read of Output Pattern blocks (research-types) | **5/5 research-types files PASS** (no unclosed fences); persona files do not use fenced blocks |
| Internal markdown anchors reference real headings | direct read | **9/9 PASS** — references-section bullets either point to relative file paths or to ADR sections, not phantom anchors |

**Edge note**: Persona files use `../../references/persona-invocation.md` and `references/persona-library.md`-relative paths inside body prose; these are documented in the parent skill's `references/` directory, so they are valid relative links from the sub-skill location.

**Verdict**: PASS

---

## Gate Criterion 2 — Sub-skills follow router-dispatch pattern (parent → sub-skill links visible)

**Evidence**:

### research-agent axis

Parent `research-agent/SKILL.md` Phase 1 contains an explicit "Sub-Skill Dispatch (per ADR-tk4-002 paradigm pattern)" section (lines 57–69) with a markdown table mapping each detected research type to its sub-skill name + path:

```
| Detected Type | Sub-Skill | Pattern Loaded |
| EXPLORATORY  | research-types-exploratory  | skills/research-types/exploratory/SKILL.md  | Pattern A: Discovery Report |
| DESCRIPTIVE  | research-types-descriptive  | skills/research-types/descriptive/SKILL.md  | Pattern B: Landscape Map |
| EXPLANATORY  | research-types-explanatory  | skills/research-types/explanatory/SKILL.md  | Pattern C: Causal Analysis |
| EVALUATIVE   | research-types-evaluative   | skills/research-types/evaluative/SKILL.md   | Pattern D: Impact Assessment |
| COMPARATIVE  | research-types-comparative  | skills/research-types/comparative/SKILL.md  | Pattern E: Decision Matrix |
```

Each sub-skill file declares the inverse contract via frontmatter `parent_skill: research-agent/SKILL.md`, `axis: research-types`, `variant: <type>`, and a body opening ("Router-dispatched paradigm sub-skill for **<Type>** research. Not directly model-invocable; the `research-agent` parent loads this sub-skill only when Phase 1 detection classifies the question as <Type>.") that names the parent. Bidirectional link verified.

### user-feedback axis

Parent `delivery-team/skills/user-feedback/SKILL.md` Phase 3 (lines 95–104) contains a dispatch table mapping project type triggers to family sub-skills:

```
| GAME_DEV                       | skills/personas/gamers/SKILL.md       | <persona list> |
| GREENFIELD / FEATURE / WEB_APP | skills/personas/web-app/SKILL.md      | <persona list> |
| ENTERPRISE / B2B               | skills/personas/enterprise/SKILL.md   | <persona list> |
| Any (overlay)                  | skills/personas/demographic/SKILL.md  | <persona list> |
```

Each persona sub-skill declares `parent_skill: delivery-team/skills/user-feedback/SKILL.md`, `axis: personas`, `variant: <family>`, and the body opens with a "Router-dispatched paradigm sub-skill … the user-feedback parent skill loads this sub-skill only when …" sentence naming the parent. Bidirectional link verified.

### Per-sub-skill router-contract evidence

| Sub-skill | parent_skill in frontmatter | Body names parent | Parent table cites sub-skill path |
|---|---|---|---|
| research-types/exploratory | research-agent/SKILL.md | "the `research-agent` parent loads this sub-skill" | line 63 of parent |
| research-types/descriptive | research-agent/SKILL.md | same | line 64 of parent |
| research-types/explanatory | research-agent/SKILL.md | same | line 65 of parent |
| research-types/evaluative | research-agent/SKILL.md | same | line 66 of parent |
| research-types/comparative | research-agent/SKILL.md | same | line 67 of parent |
| personas/gamers | delivery-team/skills/user-feedback/SKILL.md | "the user-feedback parent skill loads this sub-skill" | line 99 of parent |
| personas/web-app | delivery-team/skills/user-feedback/SKILL.md | same | line 100 of parent |
| personas/enterprise | delivery-team/skills/user-feedback/SKILL.md | same | line 101 of parent |
| personas/demographic | delivery-team/skills/user-feedback/SKILL.md | same | line 102 of parent |

**Verdict**: PASS — the router-dispatch contract is visible from both directions for every sub-skill.

---

## Gate Criterion 3 — Each sub-skill description ≤ 500 chars (Ruling 2 ceiling)

**Method**: Extracted the `description:` value from each sub-skill's frontmatter (single-line YAML scalar) and measured byte length.

| Sub-skill | Description length (chars) | Ceiling | Result |
|---|---|---|---|
| research-types/exploratory | 279 | 500 | PASS (44% headroom) |
| research-types/descriptive | 247 | 500 | PASS (50% headroom) |
| research-types/explanatory | 280 | 500 | PASS (44% headroom) |
| research-types/evaluative | 296 | 500 | PASS (40% headroom) |
| research-types/comparative | 337 | 500 | PASS (33% headroom) |
| personas/gamers | 352 | 500 | PASS (30% headroom) |
| personas/web-app | 322 | 500 | PASS (36% headroom) |
| personas/enterprise | 282 | 500 | PASS (44% headroom) |
| personas/demographic | 340 | 500 | PASS (32% headroom) |

**Max observed**: 352 chars (personas/gamers) — 148 chars below ceiling. **Min**: 247 chars.

**Verdict**: PASS — all 9 sub-skills are well under the 500-char Ruling-2 ceiling. No descriptions are at risk of overflow if marginal trigger phrases are appended in future.

---

## Gate Criterion 4 — Marketplace.json registration check (sub-skills correctly NOT registered)

**Method**: Searched `.claude-plugin/marketplace.json` for any reference to the 9 sub-skill paths or names.

**Command**:
```
grep -E "research-types|user-feedback-personas|personas-(gamers|web-app|enterprise|demographic)" .claude-plugin/marketplace.json
```
**Result**: NO MATCHES.

**Cross-check (positive)**: Parent skill paths ARE registered:
- `research-agent` registered at line 38, source `./research-agent` (line 43)
- `user-feedback` registered as part of delivery-team plugin, source `./delivery-team/skills/user-feedback` (line 60)

**Discoverability invariant evidence**: Each of the 9 sub-skills carries `disable-model-invocation: true` in frontmatter. Per ADR-tk4-002 §Marketplace discoverability invariant (Ruling 2), this flag is what excludes the file from auto-discovery / direct model-invocation; absence from `marketplace.json` is the **correct and required** state, NOT an oversight. Discovery happens via the parent router's `Skill` tool dispatch, which reads the path strings out of the parent's dispatch table.

**Verdict**: PASS — sub-skills are correctly NOT registered in marketplace.json. The omission is intentional, contractual (ADR-tk4-002 Ruling 2), and matches the `disable-model-invocation: true` flag on every sub-skill file.

---

## Gate Criterion 5 — No orphan sub-skills (each is reachable from parent SKILL.md)

**Method**: For each of the 9 sub-skill files, searched the parent SKILL.md for a literal path reference to confirm the sub-skill is reachable through the parent's documented dispatch surface.

| Sub-skill path | Parent | Parent line(s) referencing it | Reachable? |
|---|---|---|---|
| `research-agent/skills/research-types/exploratory/SKILL.md` | research-agent/SKILL.md | line 63 (Phase 1 dispatch table row) | YES |
| `research-agent/skills/research-types/descriptive/SKILL.md` | research-agent/SKILL.md | line 64 | YES |
| `research-agent/skills/research-types/explanatory/SKILL.md` | research-agent/SKILL.md | line 65 | YES |
| `research-agent/skills/research-types/evaluative/SKILL.md` | research-agent/SKILL.md | line 66 | YES |
| `research-agent/skills/research-types/comparative/SKILL.md` | research-agent/SKILL.md | line 67 | YES |
| `delivery-team/skills/user-feedback/skills/personas/gamers/SKILL.md` | user-feedback/SKILL.md | line 99 (Phase 3 dispatch table row) | YES |
| `delivery-team/skills/user-feedback/skills/personas/web-app/SKILL.md` | user-feedback/SKILL.md | line 100 | YES |
| `delivery-team/skills/user-feedback/skills/personas/enterprise/SKILL.md` | user-feedback/SKILL.md | line 101 | YES |
| `delivery-team/skills/user-feedback/skills/personas/demographic/SKILL.md` | user-feedback/SKILL.md | line 102 | YES |

**Cross-check** (find vs. registered): Listing all directories under `research-agent/skills/research-types/` returns exactly the 5 expected variants `{comparative, descriptive, evaluative, explanatory, exploratory}` — no orphan directories with a SKILL.md not represented in the parent table. Same check on `delivery-team/skills/user-feedback/skills/personas/` returns exactly `{demographic, enterprise, gamers, web-app}` — 4 expected, 0 orphans.

**Disable-model-invocation cross-cohort sanity**: `grep -lr "disable-model-invocation: true"` over the entire repo returns exactly the 9 expected sub-skill files. There are no other SKILL.md files claiming router-only status that might be orphaned. (This matches the developer's AC-3 finding and the prose-fix follow-up noted in the implementation report.)

**Verdict**: PASS — zero orphan sub-skills on the W3-8 audit surface.

---

## Cross-Cutting Documentation Quality Notes (advisory, non-blocking)

| # | Observation | Severity | Recommended owner |
|---|---|---|---|
| D1 | All 9 sub-skill files state their audience implicitly via the "Router-dispatched paradigm sub-skill … not directly model-invocable" opening. This satisfies the Technical Writer guardrail "Audience is stated" because the audience is `research-agent` / `user-feedback` parent dispatch, not a human reader. Worth memorializing in the future ADR-tk4-002 docs spec as a general rule. | Info | Story 5 W3-9 governance frontmatter rollout |
| D2 | The user-feedback persona sub-skills use `../../references/...` relative paths inside body prose (e.g. gamers line 32). These resolve correctly from the sub-skill's location to the parent's `references/` directory. No broken links found. The same convention is **not** used in research-types sub-skills — they use repo-relative paths like `research-agent/references/research-type-patterns.md`. Both are valid; harmonizing in a follow-up doc-style PR would improve consistency but is not in W3-8 scope. | Info | Backlog (doc-style harmonization, low priority) |
| D3 | Developer's CI Lint Note (Story 4 implementation report §"CI Lint Note") flags that the raw `grep -lr "disable-model-invocation: true"` discoverability invariant is fragile against prose mentions of the literal token. This was caught and resolved during AC-3 verification; a frontmatter-aware check is recommended for `.github/workflows/marketplace-discoverability-lint.yml`. Story 4 ACs all pass under either lint shape, so this is a non-blocking refinement. | Info — already logged | DevOps / Stage 7 W3-9 |
| D4 | Presentation parent is unchanged per AC-5 option (b). No `delivery-team/skills/presentation/skills/types/<type>/SKILL.md` files exist. There are therefore zero orphans on the presentation axis (vacuously satisfied). The `references/types/<type>.md` ×9 path from Story 2 W3-2 remains the loaded surface for presentation type dispatch. | Info | Already documented in Story 4 implementation report |

None of D1–D4 block the gate. Story 4 implementation accurately self-reported these.

---

## Self-DoD Compliance Cross-Check

The Story 4 implementation report's Self-DoD table claims all 5 ACs PASS. Mapping to my 5 gate criteria:

| My Gate | Implementation Report AC | Cross-check |
|---|---|---|
| 1 (well-formed markdown) | AC-1 (5 NEW research-types files; frontmatter contract OK) | Confirmed PASS — frontmatter delimiters, required keys, body structure all valid on 5 NEW + 4 EXISTING files |
| 2 (router-dispatch visible) | AC-1 + AC-2 (frontmatter contract + parent router shape) | Confirmed PASS — bidirectional router contract visible on all 9 |
| 3 (description ≤500 chars) | (implicit per Ruling 2 in ADR-tk4-002) | Confirmed PASS — max 352 / ceiling 500 |
| 4 (marketplace registration correct) | AC-3 (disable-model-invocation invariant) | Confirmed PASS — zero matches in marketplace.json; flag set on all 9 |
| 5 (no orphans) | (implicit; covered by Story 5 W3-9 sequencing gate) | Confirmed PASS — every sub-skill cited in parent dispatch table |

No discrepancy between implementation self-report and fresh-context Technical-Writer review.

---

## Decision

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/dod/story-4-tech-writer-review.md
SUMMARY: All 5 gate criteria PASS. 9 sub-skills well-formed; router-dispatch bidirectional; descriptions 247-352 chars (≤500); correctly absent from marketplace.json (disable-model-invocation flag); zero orphans. Presentation axis vacuously OK (option b).
```

— Technical Writer (FRESH), Stage 6 Story 4 DoD round 1, run-2026-05-09-tk4

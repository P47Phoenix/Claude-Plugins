---
title: "Caveman-Lite Prose Discipline — PRD"
pipeline_id: run-2026-05-05-tk3
wave: caveman-lite (Step 1 of 4)
work_items: [W2-1, W2-2, W2-3]
stage: 02-refine
depth: light
author: Product Owner (product-delivery skill)
predecessor: run-2026-05-05-tk2 (commit c2e7d5a)
source_brief: .delivery/artifacts/01-idea/po/idea-brief.md
source_backlog: .delivery/backlog/BACKLOG-102-caveman-prose-discipline.md
binding_memory: .delivery/memory/topics/skill-token-economy.md
created: 2026-05-05
---

> "A wizard is never late, nor is he early; he arrives precisely when he means to."
> — Gandalf the Grey, speaking as PO at Refine

# Caveman-Lite Prose Discipline — Product Requirements

## 1. Engagement

This PRD scopes the caveman-lite prose discipline wave for delivery-team agent dispatches and DoD validator outputs. The engagement is `run-2026-05-05-tk3`, a FEATURE-execution-of-pre-planned-waves run binding to BACKLOG-102. The full engagement framing — predecessor commit, theme, and stop-rule arming — is captured in the idea brief at `.delivery/artifacts/01-idea/po/idea-brief.md`; this PRD does not restate that framing. Three work items (W2-1, W2-2, W2-3) ship together as ONE consolidated story per the file-scope rule (idea-brief §4). Refine is light; ACs already exist in BACKLOG-102 §Acceptance Criteria, so this PRD's job is to ground each AC in measured TARGET-state file evidence and split each AC's framing between "well-formed?" (Refine concern) and "applies?" (Stage 6 concern).

## 2. Source

- **Authoritative backlog**: `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md` (work items, tier scoping, exemptions, AC list, stop-rule).
- **Binding decisions** (do not re-debate): `.delivery/memory/topics/skill-token-economy.md` (Rulings 1–5; the cache-prefix freeze in Ruling 1 governs every edit in W2-1 and W2-3).
- **Idea brief** (engagement framing, routing, story consolidation): `.delivery/artifacts/01-idea/po/idea-brief.md`.

This PRD does not duplicate those documents. Where this PRD adds value is the discovery-grounded mapping of each work item to a precise TARGET file:line surface and the explicit Validator-Framing split.

## 3. Discovery (TARGET-state file evidence)

All values below were measured during this Refine pass. Stage 6 developer DoD validators will re-run identical commands; if the values drift between Refine and Dev, that is a defect signal.

| Surface | Path | Lines | Measured |
|---|---|---|---|
| Tier-A orchestrator | `delivery-team/skills/delivery-flow/SKILL.md` | 497 | `wc -l` |
| Stage + dispatch templates | `delivery-team/skills/delivery-flow/references/pipeline-stages.md` | 682 | `wc -l` |
| DoD validator template | `delivery-team/skills/delivery-flow/references/quality-gates.md` | 288 | `wc -l` |
| Config schema | `delivery-team/skills/delivery-flow/references/config-schema.md` | 369 | `wc -l` |
| Generated JSON schema | `delivery-team/skills/delivery-flow/references/config-schema.json` | exists | `head -3` |

Additional discovery facts:

- `pipeline-stages.md` contains **3 dispatch templates** at lines 44 (Primary), 87 (Supporting), 130 (DoD Validator) — all three must receive the PROSE STYLE block.
- `pipeline-stages.md` has **10 top-level (`^## `) sections** (`grep -nc`).
- `config-schema.md` `Current Version: 2.8` (line 5); the row at line 15 already declares `config_version: "2.8"`.
- The Version History (lines 347–369) shows the v2.8 slot is **already taken** by the DESIGN routing addition (entry dated 2026-04-05). Therefore W2-3 MUST bump to **v2.9**, not v2.8 as the BACKLOG-102 work item draft suggests. This is the only material deviation from BACKLOG-102 wording, and is forced by surface evidence — the BACKLOG was authored before v2.8 landed. FR-3 below records the corrected target.
- SKILL.md Phase 0 config-read lives at lines 56–89; the Volatile marker sits at line 475, so Phase 0 IS inside the cache-prefix region (bytes 0..2048; boundary documented at line 478). Edits that change Phase 0 byte content are cache-prefix-affecting and require ADR-tk3-001 (already scoped to Stage 4 per idea-brief §6).
- SKILL.md Step 4 dispatch construction lives at lines 329–345; this is past the cache-prefix boundary, so the W2-1 PROSE STYLE block addition there does NOT require an ADR.
- Step 7 DoD validation orchestration lives at lines 377–402; also past the prefix boundary.

## 4. Functional Requirements

Each FR cites a single Work Item; each FR has a target file:line locus.

### FR-1 (W2-1): PROSE STYLE block in agent dispatch templates

**MUST** add a PROSE STYLE directive block to all three dispatch templates in `delivery-team/skills/delivery-flow/references/pipeline-stages.md`:

- Primary Agent Dispatch Template (line 44+)
- Supporting Agent Dispatch Template (line 87+)
- DoD Validator Dispatch Template (line 130+) — NOTE: FR-2 governs the *output* style of validator review files; FR-1 governs the *dispatch prompt* itself, which is the same PROSE STYLE block.

Block content (verbatim from BACKLOG-102 §W2-1):

```
PROSE STYLE: caveman-lite for narrative-framing prose ONLY (the prose between
signal block and response end, plus signal block SUMMARY field). Drop articles/
filler/pleasantries/hedging; fragments OK; short synonyms; preserve technical
terms exact and code/error-string verbatim. Artifact body uses standard prose.
Auto-clarity exemptions apply: standard prose for security warnings,
irreversible-op confirmations, multi-step sequences, user clarifications.
```

The block is conditionally injected by SKILL.md Phase 0 based on the `prose_style` config key (FR-3); see FR-3 for the wiring.

**Locus**: `pipeline-stages.md` lines 44–176 (the three template blocks); `SKILL.md` Step 4 (lines 329–345) for the injection-point reference.

### FR-2 (W2-2): caveman-lite verdict prose in DoD validator review files

**MUST** update the DoD Validator Prompt Template at `delivery-team/skills/delivery-flow/references/quality-gates.md` lines 21–38 to emit caveman-lite verdict prose in produced review files. Specifically:

- The freeform verdict prose surrounding gate-result tables and findings bullets uses caveman-lite.
- The `STATUS:` line (DONE / NOT_DONE / CODE_COMPLETE) remains verbatim — value semantics MUST NOT change.
- Each FINDING still names file/line/criterion (BACKLOG-102 §W2-2 AC).
- Tabular gate-result blocks remain in current Markdown table format (already terse; no further compression).

**Locus**: `quality-gates.md` lines 21–53 (template block + parallel-validator clarification); also referenced from `SKILL.md` Step 7 (lines 377–402).

### FR-3 (W2-3): `prose_style:` config key + schema bump v2.8 → v2.9

**MUST** add a top-level `prose_style` key to the config schema:

- Key: `prose_style`
- Type: string
- Required: no
- Default: `caveman-lite`
- Valid values: `caveman-lite`, `standard`
- Consumed by: `delivery-flow` Phase 0 (conditional injection of FR-1 block); `delivery-flow` Step 7 (conditional caveman-lite framing of FR-2 validator output).

**Schema version**: Bump `Current Version` (config-schema.md line 5) and `config_version` row default (line 15) from `2.8` to **`2.9`**. The v2.8 slot is already occupied by the DESIGN-routing entry (2026-04-05). The Version History table (line 347+) gains a v2.9 row with date and change description. The Config File Template at line 207+ gains the `prose_style:` line.

**Migration**: Existing v2.8-or-earlier configs auto-migrate. If `prose_style` is absent on load, default to `caveman-lite` and surface the standard "Config upgraded from v[old] to v2.9" banner per SKILL.md Phase 0 lines 60–64. Existing v2.7→v2.8 migration paths are preserved (lines 65–71).

**JSON schema regeneration**: After editing `config-schema.md`, run `delivery-team/scripts/generate-schema.py` to regenerate `references/config-schema.json` (per Step 6.5 of the schema extension protocol; idea-brief §7 Stage 5 also makes this an explicit Plan-stage Story DoD task).

**SKILL.md Phase 0 wiring**: Add a single conditional line in Phase 0 (lines 56–89) that reads `config.prose_style` and stores it in the loaded-config struct. Step 4 dispatch construction reads the value and either includes the FR-1 PROSE STYLE block (when `caveman-lite`) or omits it (when `standard`). The Step 4 edit sits OUTSIDE the cache-prefix region (line 329+); the Phase 0 edit sits INSIDE (lines 56–89). ADR-tk3-001 (Stage 4 deliverable per idea-brief §6) governs the prefix re-freeze — Refine does not pre-judge whether the Phase 0 edit will move prefix bytes; Architect does.

**Locus**: `config-schema.md` lines 5, 15, 207+, 347+; `SKILL.md` lines 56–89 (Phase 0) and 329–345 (Step 4); `references/config-schema.json` (regenerated artifact).

## 5. Non-Functional Requirements

| ID | NFR | Source | Verification |
|---|---|---|---|
| NFR-1 | Cache-prefix freeze preserved (Ruling 1). Any Phase 0 byte change is covered by ADR-tk3-001 + `governance/cache-prefix-hash.txt` update + CI hash-check pass. | skill-token-economy.md Ruling 1; idea-brief §6 | Architect Stage 4 (ADR + hash diff); CI hash-check |
| NFR-2 | Telemetry-measurable. Pre/post token counts come from the existing W0-1 hook at `.delivery/telemetry/skill-loads.jsonl`. No new telemetry surface. | BACKLOG-102 §Source bullet 3; idea-brief §3 | Stage 6/7 dogfood (§7 below) |
| NFR-3 | Opt-out path. `prose_style: standard` reverts behavior to current; verified by 3-dispatch dogfood. | BACKLOG-102 §W2-3 AC; AC-6 | Stage 6 dogfood |
| NFR-4 | Auto-clarity exemptions enforced. Security / irreversible-op / multi-step / user-clarification dispatches use standard prose even when `prose_style: caveman-lite`. The PROSE STYLE block text in FR-1 declares the exemptions; the developer at Stage 6 MUST add at least one negative test (synthetic security-warning dispatch) to demonstrate exemption. | BACKLOG-102 §Auto-clarity boundaries; idea-brief §8 AC-5 | Stage 6 dogfood (§7 below) |
| NFR-5 | No new CLI dependencies in Developer-DoD commands. Every AC check below uses bash + python (stdlib + PyYAML). NO `yq`, `xq`, `jq` etc. Verified by reading `.claude/settings.local.json` allowlist, which currently permits only `WebSearch`, `Bash(flatpak list:*)`, `Read(//usr/bin/**)`, `Read(//var/usrlocal/bin/**)`, `Bash(git add:*)` — no general bash CLI tools beyond `git add`. The repo's standing dogfood prereq is bash + python3 + PyYAML; ACs below conform. | Memory lesson 3 (PRD instructions); `.claude/settings.local.json` content | Stage 6 grep audit on AC commands |
| NFR-6 | Validator-prompt path canonicality. Every validator dispatch in Stage 6/7 cites `.delivery/artifacts/<NN>-<stage>/` paths so the validator reads the canonical file. | Wave 2 retro carry-forward; idea-brief §8 footer | UAT spot-check on dogfood dispatch |
| NFR-7 | DoD pass-rate baseline preserved (4/7 first-try per memory/index.md). Caveman-lite verdict prose MUST NOT cause validators to miss findings (stop-rule trigger). | BACKLOG-102 AC-3, §Stop-rule; idea-brief §9 | UAT measurement vs baseline |
| NFR-8 | Light = reduced depth, NOT skipped. Refine ran every discovery command cited in §3 above. The Developer DoD validator MUST also run them — no copy-paste of cited values without re-measurement. | Memory lesson 5 | Stage 6 DoD validator |

## 6. Acceptance Criteria

### 6.1 Initiative-level AC (verbatim from BACKLOG-102 §Acceptance Criteria)

These six are the binding initiative gates. Each is tagged with the closing WI.

| AC | Verbatim text | Closes WI |
|---|---|---|
| AC-1 | Agent narrative-framing prose MEASURABLY shorter (≥20% reduction in response-prose tokens, telemetry-verified). | W2-1 |
| AC-2 | DoD review files MEASURABLY smaller (≥25% reduction). | W2-2 |
| AC-3 | NO regression in DoD pass rate (currently 4/7 first-try per memory/index.md). | W2-1 + W2-2 (joint) |
| AC-4 | NO regression in artifact quality (PRDs/ADRs/release-notes still pass downstream agents' reads — verified by next pipeline run). | W2-1 + W2-2 (joint) |
| AC-5 | Auto-clarity boundaries respected (security/destructive/multi-step prose remains standard). | W2-1 |
| AC-6 | Opt-out via `prose_style: standard` works (one-line config change reverts behavior). | W2-3 |

### 6.2 Per-WI structural ACs (Refine-grounded, "well-formed?" framing)

#### W2-1 PROSE STYLE block (closes AC-1, AC-5)

| AC ID | Target file:line | Runnable check (bash + python3) | Expected at TARGET state | Frame |
|---|---|---|---|---|
| W2-1-S1 | `references/pipeline-stages.md` lines 44, 87, 130 | `grep -c "^PROSE STYLE: caveman-lite for narrative-framing prose ONLY" delivery-team/skills/delivery-flow/references/pipeline-stages.md` | `3` | well-formed? |
| W2-1-S2 | `references/pipeline-stages.md` (each block) | `grep -c "Auto-clarity exemptions apply" delivery-team/skills/delivery-flow/references/pipeline-stages.md` | `3` | well-formed? |
| W2-1-S3 | `SKILL.md` Step 4 (lines 329–345) | `grep -n "PROSE STYLE\|prose_style" delivery-team/skills/delivery-flow/SKILL.md \| head -5` returns non-empty match within Step 4 region | match present | well-formed? |
| W2-1-A1 | telemetry log | python3 reads `.delivery/telemetry/skill-loads.jsonl`, computes mean response-prose tokens for last 5 pre-merge dispatches vs first 5 post-merge dispatches; reduction ≥ 20% | reduction ≥ 20% (AC-1) | applies? |
| W2-1-A2 | synthetic dispatches | 3 dogfood dispatches (security warning / `git revert` confirmation / 4-step migration) inspected; each shows standard prose, no PROSE STYLE compression | 3/3 standard prose (AC-5) | applies? |

#### W2-2 caveman-lite verdict prose in DoD validator template (closes AC-2)

| AC ID | Target file:line | Runnable check (bash + python3) | Expected at TARGET state | Frame |
|---|---|---|---|---|
| W2-2-S1 | `references/quality-gates.md` lines 21–38 (validator template block) | `grep -n "STATUS: DONE \| NOT_DONE \| CODE_COMPLETE" delivery-team/skills/delivery-flow/references/quality-gates.md` returns line within template block; STATUS values UNCHANGED | unchanged | well-formed? |
| W2-2-S2 | `references/quality-gates.md` template body | `grep -c "caveman-lite" delivery-team/skills/delivery-flow/references/quality-gates.md` ≥ 1 (template instructs validator to use caveman-lite for verdict prose) | `≥ 1` | well-formed? |
| W2-2-S3 | structural — findings format | `grep -nE "file/line/criterion\|name file" delivery-team/skills/delivery-flow/references/quality-gates.md` matches the existing finding-format directive (preserved verbatim) | preserved | well-formed? |
| W2-2-A1 | DoD review file size delta | python3 averages byte-length of `.delivery/artifacts/*/dod/*-review.md` for last 5 pre-merge stage runs vs first 5 post-merge stage runs; reduction ≥ 25% | reduction ≥ 25% (AC-2) | applies? |
| W2-2-A2 | DoD pass-rate | python3 counts first-try DONE rate over 5-run window post-merge vs the 4/7 baseline in `memory/index.md`; no regression | ≥ 4/7 first-try (AC-3) | applies? |

#### W2-3 `prose_style:` config key + schema bump (closes AC-6)

| AC ID | Target file:line | Runnable check (bash + python3) | Expected at TARGET state | Frame |
|---|---|---|---|---|
| W2-3-S1 | `references/config-schema.md` line 5 | `grep -n "^## Current Version: 2.9" delivery-team/skills/delivery-flow/references/config-schema.md` | match on line 5 | well-formed? |
| W2-3-S2 | `references/config-schema.md` line 15 | `grep -n '^| \`config_version\` .*"2.9"' delivery-team/skills/delivery-flow/references/config-schema.md` | match | well-formed? |
| W2-3-S3 | `references/config-schema.md` schema table | `grep -n '^| \`prose_style\`' delivery-team/skills/delivery-flow/references/config-schema.md` | match (key present, type string, default `caveman-lite`, valid values `caveman-lite, standard`) | well-formed? |
| W2-3-S4 | `references/config-schema.md` Version History (lines 347+) | `grep -n '^| 2.9 ' delivery-team/skills/delivery-flow/references/config-schema.md` | match (one v2.9 row) | well-formed? |
| W2-3-S5 | `references/config-schema.md` Config File Template (lines 207+) | `grep -nA1 "^prose_style:" delivery-team/skills/delivery-flow/references/config-schema.md` | match within template block | well-formed? |
| W2-3-S6 | `references/config-schema.json` | `python3 -c "import json; d=json.load(open('delivery-team/skills/delivery-flow/references/config-schema.json')); assert 'prose_style' in d.get('properties', {}); assert d['properties']['config_version'].get('default')=='2.9'"` | exit 0 | well-formed? |
| W2-3-S7 | `SKILL.md` Phase 0 (lines 56–89) | `grep -nE "prose_style" delivery-team/skills/delivery-flow/SKILL.md \| head -3` returns ≥ 1 match within line range 56..89 | match | well-formed? |
| W2-3-A1 | runtime opt-out | 3 synthetic dispatches with `.delivery/config.yml` set to `prose_style: standard`; PROSE STYLE block absent from each dispatch prompt; baseline-style prose returns | 3/3 absent (AC-6) | applies? |

## 7. Validator Framing (Wave 1 retro lesson, made surface)

Each AC above carries a Frame column tagged either **well-formed?** or **applies?**. This split is binding for validator dispatch:

- **Refine DoD validators (Stage 2)** evaluate ONLY the **well-formed?** ACs. They check the directive itself: is the PRD self-consistent, is the schema bump well-targeted, do the cited file:line loci exist, does the AC list cover all six initiative ACs? They do NOT measure runtime telemetry — the change has not landed yet.
- **Stage 6 Developer DoD validators** evaluate BOTH **well-formed?** (re-running the Refine commands to detect drift) AND **applies?** (running the post-merge measurement protocol of §7 below).
- **Stage 7 UAT validators** focus on **applies?** ACs against the dogfood evidence pack and validate NFR-6 path-canonicality on the produced artifact set.

This split eliminates the Wave 1 retro defect where Refine validators tried to measure runtime telemetry on un-merged code.

## 8. Stage 6 Dogfood Plan (the empirical measurement protocol)

Stage 6 owns AC-1, AC-2, AC-5, AC-6. Stage 7 confirms AC-3 and AC-4 (no-regression rolling).

### 8.1 Pre-merge baseline (already collected)

Pre-merge baseline = the last 5 dispatches in `.delivery/telemetry/skill-loads.jsonl` from runs predecessor-tk2 and earlier. Wave 2 telemetry per BACKLOG-102 §W2-1 AC bullet 2 already covers this. The developer reads the file with `python3 -c "import json; ..."` and computes mean response-prose tokens. The exact dispatch IDs entering the baseline are recorded in the `w2-1-implementation.md` report.

### 8.2 Post-merge sample (Stage 6, full depth)

After the consolidated Story 1 lands (W2-1 + W2-2 + W2-3 in one developer dispatch per idea-brief §4), the developer triggers 5 dispatches against routine pipeline work to populate fresh telemetry rows. For each row: response-prose token count is logged by the W0-1 hook. Compute mean. Required: **≥ 20% reduction vs pre-merge baseline** (AC-1 / W2-1-A1). If <15%, the BACKLOG-102 stop-rule fires (idea-brief §9): pause, retro, do not proceed to Tier 2 deferral targets.

### 8.3 DoD review file size delta (AC-2 / W2-2-A1)

Compute mean byte-length of all `.delivery/artifacts/*/dod/*-review.md` files produced in the 5 post-merge dispatches; compare to the same metric across the 5 pre-merge baseline dispatches. Required: **≥ 25% reduction**. If under, same stop-rule fires.

### 8.4 Auto-clarity exemption check (AC-5 / W2-1-A2)

3 synthetic dogfood dispatches:

1. **Security warning**: a dispatched prompt where the agent's narrative MUST include a security warning (e.g., "the credentials file is world-readable"). Inspect dispatch transcript: PROSE STYLE block is sent, but the agent's emitted security-warning prose remains in standard form per the auto-clarity exemption embedded in FR-1.
2. **Irreversible op**: a dispatch involving `git revert` or `rm -rf` confirmation prose. Same expectation.
3. **Multi-step sequence**: a 4-step migration / rollback sequence in the agent's narrative. Same expectation.

Each transcript is captured to `.delivery/artifacts/06-development/dogfood/auto-clarity-<n>.md` and inspected by the Stage 6 QA validator.

### 8.5 Opt-out check (AC-6 / W2-3-A1)

1 dogfood dispatch with `.delivery/config.yml` patched to `prose_style: standard`. Verify the PROSE STYLE block is NOT injected into the dispatch prompt (transcript inspection) and the agent's emitted prose matches the pre-merge baseline style (no caveman-lite compression artifacts). Restore `prose_style: caveman-lite` after the test.

### 8.6 Path-canonicality spot-check (NFR-6)

The Stage 6 validator dispatches MUST cite `.delivery/artifacts/06-development/` paths (not in-prompt content). UAT spot-checks one dispatch transcript to confirm.

## 9. Out of Scope

Per BACKLOG-102 §Out of scope and §Tiered scope, the following are explicitly NOT in this engagement:

- **Tier 2 surfaces** — retrospective body prose; sprint plan body prose. Both deferred to BACKLOG-103 A/B.
- **Tier 3 surfaces** — PRD body, ADR body, release notes / user-guide, memory topic chunks, run archive files. Standard prose required.
- **CLAUDE.md** — handled by Wave 3 refactor.
- **Code, commit messages, PR bodies** — already excluded by caveman's own boundary rule.
- **caveman `full` / `ultra` modes** — out of scope; revisit only if Tier 1 + Tier 2 measure clean.
- **Wenyan modes** — no business case.
- **Marketplace caveman plugin install** — this engagement implements caveman-lite *patterns* directly; no external dependency added.

## 10. Stop-rule (verbatim from idea-brief §9)

**From skill-token-economy.md**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes.

**From BACKLOG-102 §Stop-rule** (engagement-local): if Tier-1 measurement shows <15% prose-token reduction (low ROI) OR if any DoD validator misses a finding due to over-compression (quality regression), pause Tier-2 A/B (deferred to BACKLOG-103+) and run a root-cause retro before proceeding.

Both stop-rules are armed for this run.

## 11. References

- Idea brief: `.delivery/artifacts/01-idea/po/idea-brief.md`
- Source backlog: `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`
- Binding decisions: `.delivery/memory/topics/skill-token-economy.md`
- Cache-prefix hash: `governance/cache-prefix-hash.txt`
- Telemetry: `.delivery/telemetry/skill-loads.jsonl`
- Predecessor archive: `.delivery/memory/archive/run-2026-05-05-tk2.md`
- Schema generator: `delivery-team/scripts/generate-schema.py`

<!-- run: run-2026-05-05-tk3 | wave: caveman-lite (Step 1 of 4-step Skill Token-Economy completion plan) | predecessor: run-2026-05-05-tk2 c2e7d5a -->

# Idea Brief — Caveman-Lite Prose Discipline (Wave caveman-lite)

*Spoken by Aragorn, son of Arathorn, Ranger of the North.*

> The road is set. The Fellowship rides at dawn — light packs, plain speech, blades sharp where it counts.

## 1. Engagement

- **Pipeline**: `run-2026-05-05-tk3`
- **Project type**: FEATURE (execution of pre-planned waves; binding-decisions-in-memory pattern)
- **Wave**: caveman-lite — Step 1 of the 4-step Skill Token-Economy completion plan
- **Theme**: lotr (continued; PO maps to Aragorn)
- **Predecessor**: run-2026-05-05-tk2 (commit c2e7d5a, Wave 2 structural extractions, GO)

## 2. Source

The authoritative source brief is `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`. This idea brief CONSOLIDATES — it does not re-author. All tier scoping, work-item ACs, and exemption rules live in BACKLOG-102 verbatim; the team executes against BACKLOG-102, not against this brief.

Origin trail:
- External pattern: [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — Claude Code skill targeting ~65–75% output-token reduction with explicit auto-clarity boundaries.
- User direction (2026-05-04): apply caveman discipline to agent outputs and ephemeral artifacts to reduce orchestrator-flow context.
- Telemetry substrate: BACKLOG-100 W0-1 hook (`.delivery/telemetry/skill-loads.jsonl`) — already in place; provides the empirical baseline and post-change deltas.

## 3. Goal

Apply caveman-lite prose discipline selectively to (a) agent narrative-framing prose between signal block and end, (b) signal-block SUMMARY fields, (c) DoD review verdict prose, (d) `stage-summary.md` orchestrator metadata, and (e) implementation report bodies — without compromising durable-artifact readability or technical accuracy. Success is measured empirically: ≥20% reduction in response-prose tokens and ≥25% reduction in DoD review file size, with no DoD pass-rate regression and auto-clarity exemptions honored.

## 4. Story Consolidation Decision (binding)

Per memory `topics/project-types.md` ("Story consolidation by file scope"): BACKLOG-102 has 3 WIs (W2-1 dispatch templates, W2-2 validator templates, W2-3 `prose_style:` config key) — and **all 3 touch overlapping prompt-template surfaces in `delivery-team/skills/delivery-flow/`** (SKILL.md Step 4 + Step 7 + Phase 0 config-read; plus `references/pipeline-stages.md`, `references/quality-gates.md`, `references/config-schema.md` v2.7→v2.8, and the regenerated `config-schema.json` produced by `delivery-team/scripts/generate-schema.py` — the validator-toolchain artifact required whenever the prose schema bumps). Decision: collapse to **ONE Story 1 (Effort S)** at Plan stage. Same DoD coverage; one developer dispatch instead of three.

## 5. Binding Constraints (from memory — do NOT re-debate)

From `.delivery/memory/topics/skill-token-economy.md` (5 rulings still in force):

1. **Cache-prefix freeze** — first ~2k tokens of every Tier-A SKILL.md MUST be byte-stable across runs; any prefix change requires an ADR citing cache-cost impact.
2. **`disable-model-invocation` boundary** — paradigm sub-skills only; top-level skills stay discoverable.
3. **SKILL.md line budgets** — Tier-A ≤500, Tier-B ≤300, Tier-C ≤200 (delivery-flow Tier-A 500 is the live budget).
4. **Agent prompts as markdown references** — no Python prompt-builders.
5. **`allowed-tools` whitelist scope** — required on Tier-A orchestrators.

From `.delivery/memory/topics/project-types.md`:
- **FEATURE-execution-of-pre-planned-waves with binding-decisions-in-memory** — execute, do not re-debate. Cite BACKLOG-102 + skill-token-economy.md; if a stage agent finds itself re-litigating a ruling, that is a defect.
- **Story consolidation by file scope** — applied above (§4).

From `CLAUDE.md` Key Conventions:
- **Plugin-dev skill routing for Dev** (binding, not deferrable to Architect): this BACKLOG modifies a skill (`delivery-flow/SKILL.md` + references) → `plugin-dev:skill-development` MUST be pre-loaded at the developer dispatch in Stage 6. Post-completion: `plugin-dev:skill-reviewer` on the modified SKILL.md, then `plugin-dev:plugin-validator` before PR.

## 6. Cache-Prefix Invariant (Ruling 1) — explicit call-out

The PROSE STYLE block (W2-1) and the Phase 0 config-read change (W2-3) both touch `delivery-flow/SKILL.md`. **The change MUST NOT invalidate the byte-stable cache prefix established Wave 1 + Wave 2** (`governance/cache-prefix-hash.txt`). If prefix-region edits are unavoidable, **ADR-tk3-001 owns the re-freeze**: enumerate the bytes that move, justify, update the hash, pass the CI hash-check. Architect at Stage 4 is responsible for confirming this before approving the structural change.

## 7. Routing (per BACKLOG-102 §Pipeline-run preferences)

| Stage | Depth | Notes |
|---|---|---|
| 1 Idea | light | This brief |
| 2 Refine | light | ACs already in BACKLOG-102; refine = consolidate to ONE story + sharpen exit gates |
| 3 Design | **SKIP** | DX-only — no UI surface. Per `topics/project-types.md`: record skip at state-entry as "DX-only routing deviation"; do NOT conflate with silent stage fusion (R-09) |
| 4 Architect | light w/ **ADR-tk3-001** | Cache-prefix re-freeze ADR is mandatory; config schema v2.7→v2.8 = small ADR; no full board needed |
| 5 Plan | light | One Story 1 (Effort S); single developer dispatch; Story DoD MUST list `config-schema.json` regeneration as an explicit task alongside the `.md` schema bump |
| 6 Development | full | `plugin-dev:skill-development` pre-loaded; run `delivery-team/scripts/generate-schema.py` after the v2.8 schema edit and commit the regenerated `config-schema.json`; dogfood per W2-3 (3-dispatch opt-out verification) |
| 7 UAT | full | Empirical telemetry deltas validated; auto-clarity exemptions spot-checked; DoD pass-rate compared |

**SKIP rationale (Stage 3)**: BACKLOG-102 changes prompt-template strings and a config key. There is no user-facing UI surface, no wireframe, no component spec. Per memory pattern (validated run-2026-04-22-4x7e), DX-only migrations route around Design with the skip recorded — not silently fused.

## 8. Acceptance Gates (verbatim from BACKLOG-102 §Acceptance Criteria)

1. Agent narrative-framing prose MEASURABLY shorter (≥20% reduction in response-prose tokens, telemetry-verified).
2. DoD review files MEASURABLY smaller (≥25% reduction).
3. NO regression in DoD pass rate (currently 4/7 first-try per memory/index.md).
4. NO regression in artifact quality (PRDs/ADRs/release-notes still pass downstream agents' reads — verified by next pipeline run).
5. Auto-clarity boundaries respected (security/destructive/multi-step prose remains standard).
6. Opt-out via `prose_style: standard` works (one-line config change reverts behavior).

**Stage-7 acceptance carry-forward (Wave 2 retro lesson)**: every dispatched validator prompt MUST cite `.delivery/artifacts/<NN>-<stage>/` paths so the validator reads the canonical file. UAT MUST spot-check this on the dogfood dispatch.

**Stage-4 acceptance**: ADR-tk3-001 produced; `governance/cache-prefix-hash.txt` updated only if a prefix byte actually changed; CI hash-check passes.

## 9. Stop-rule

**From skill-token-economy.md**: defects/story rate >0.4 across any 3-PR window pauses subsequent waves until a root-cause retro completes.

**From BACKLOG-102 §Stop-rule** (engagement-local): if Tier-1 measurement shows <15% prose-token reduction (low ROI) OR if any DoD validator misses a finding due to over-compression (quality regression), pause Tier-2 A/B (deferred to BACKLOG-103+) and run a root-cause retro before proceeding.

Both stop-rules are armed for this run.

## 10. Open Questions

None. All ambiguities are resolved by BACKLOG-102 + the two memory topic files. The team is empowered to execute.

## 11. References

- Source brief: `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`
- Binding decisions: `.delivery/memory/topics/skill-token-economy.md`
- Project-type pattern: `.delivery/memory/topics/project-types.md` (FEATURE-execution-of-pre-planned-waves, story-consolidation-by-file-scope, DX-only Design skip)
- Cache-prefix hash: `governance/cache-prefix-hash.txt`
- Telemetry: `.delivery/telemetry/skill-loads.jsonl`
- Predecessor archives: `.delivery/memory/archive/run-2026-05-04-tk1.md`, `.delivery/memory/archive/run-2026-05-05-tk2.md`

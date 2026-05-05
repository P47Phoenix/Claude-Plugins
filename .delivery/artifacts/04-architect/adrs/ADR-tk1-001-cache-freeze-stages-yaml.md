# ADR-tk1-001: Cache-Prefix Freeze + stages.yml Schema

**Status**: Accepted
**Deciders**: Architect (solution_architect), Product Owner
**PRD refs**: FR-01, FR-02, FR-03, FR-04
**Wave**: Wave 1 (W1-1, W1-2)
**Date**: 2026-05-04
**Binds**: `delivery-team/skills/delivery-flow/SKILL.md`; new `references/stages.yml`; new `references/stages-schema.json`; new `governance/cache-prefix-hash.txt`

---

## Context

`delivery-flow/SKILL.md` is 1,090 lines / ~16,240 tokens. It is the highest-frequency load in the
delivery-team plugin. Without a stable prefix, Anthropic's prompt-cache TTL (5-minute sliding
window) resets on every invocation containing dynamic content near the head of the file — volatile
items such as run-IDs, config echoes, and date stamps force a cache miss on every second call.

Stage definitions (lines 613–746, ~133 lines) are static reference data embedded inline; they
inflate cold-load tokens and duplicate knowledge already expressed in memory topics.

Binding decision: Ruling 1 (skill-token-economy.md) mandates prefix freeze after doctrine
externalization lands; Ruling Corollary mandates YAML manifest for stage definitions (Pattern:
Stage definitions as YAML manifest).

Pre-rollout baseline (mandatory-rollout side-effect lesson): delivery-flow 1090 L; no files at
the Tier-A 500-line edge.

---

## Decision

### W1-1 — Cache-prefix freeze

1. **Content boundary**: Lines 1 through (and including) the last line of `## Phase 3: Stage
   Routing` (currently L332) constitute the **frozen prefix**. This covers: frontmatter, design
   principle, core principles, Phase 0 setup wizard, Phase 1 project-type detection, Phase 2
   memory retrieval, and Phase 3 routing matrix. Combined character count of this region is
   approximately 2,000 tokens (safe Anthropic cache-segment boundary).

2. **Volatile marker**: All content that changes between runs — config echoes, run-IDs,
   date-stamps — MUST appear after a `## Volatile` H2 marker placed near EOF (after `## References`
   if present; otherwise as the final H2 section).

3. **Verification mechanism**: A SHA-256 of the first 2,048 bytes of the file (post-commit,
   byte-for-byte) MUST be stored in `governance/cache-prefix-hash.txt`. A CI step
   (`scripts/check_cache_prefix_hash.sh`) recomputes the hash on every PR and fails if the hash
   changes without a corresponding commit that also updates `cache-prefix-hash.txt` and cites an
   ADR in its message.

4. **Future-change protocol**: Any PR that moves content into or rearranges the frozen prefix
   region MUST include: (a) updated `cache-prefix-hash.txt`, (b) a new or amended ADR citing
   cache-cost impact, (c) PR body line `Cache-Prefix-Change: <ADR-link>`.

### W1-2 — stages.yml schema

1. **File location**: `delivery-team/skills/delivery-flow/references/stages.yml`

2. **Required fields per stage row**:

   ```yaml
   stages:
     - id: stage_1_idea          # snake_case, unique
       name: "Idea"              # human display
       runs_for: [GREENFIELD, FEATURE, BUG_FIX, DESIGN, GAME_DEV, SPIKE, DOCS_ONLY]
       primary_agent: product-delivery
       dod_validators: [architect, quality, operations]
       output_path: .delivery/artifacts/01-idea/
       max_self_correction: 2
       human_checkpoint: false
       collaboration_patterns: [evaluator-optimizer]
       light_mode_rules:         # optional; omit for full-depth
         depth: light
         skip_patterns: []
   ```

3. **JSON Schema**: `delivery-team/skills/delivery-flow/references/stages-schema.json` validates
   the YAML. Required properties: `stages` (array, minItems 7, maxItems 7). Each item requires
   all fields except `light_mode_rules` (optional object).

4. **SKILL.md backward compatibility**: The inline Stage Definitions block (lines 613–746) MUST
   be replaced with a single-line directive:
   ```
   <!-- stages: see references/stages.yml — loaded on demand by orchestrator -->
   ```
   Orchestrator loads `stages.yml` via `Read` tool at Phase 4 pipeline execution start (Step 3).

5. **Schema validation gate**: CI runs
   `python3 -c "import json,yaml,jsonschema; ..."` (as specified in PRD AC W1-2).
   PR fails if schema validation or 7-stage count assertion fails.

---

## Consequences

**Positive**:
- Cache read/input ratio ≥ 0.85 on second invocation (measurable via W0-1 telemetry).
- ~2,000+ token cold-load reduction from stage externalization alone.
- Future stage changes are isolated to `stages.yml`; SKILL.md prefix remains frozen.
- Schema validation in CI prevents malformed stage rows from silently breaking routing.

**Negative / Trade-offs**:
- Adds a `Read` tool call per pipeline run to load `stages.yml` (negligible overhead vs cache gain).
- Two-file consistency risk: `stages.yml` and SKILL.md orchestrator references must stay aligned.
  Mitigated by schema CI gate and mandatory SKILL.md inline comment pointer.
- `governance/cache-prefix-hash.txt` becomes a CI-critical file; accidental edits to the frozen
  prefix will block PRs even when intentional. Mitigation: clear PR protocol in W1-1 decision §4.

---

## Alternatives Considered

| Option | Decision | Reason rejected |
|--------|----------|-----------------|
| Store cache boundary as line number (not byte hash) | Rejected | Line numbers shift on any edit above the boundary; byte hash of first 2,048 bytes is content-addressable and editor-invariant |
| Move ALL stage content to SKILL.md frontmatter YAML block | Rejected | Frontmatter is parsed at load time — defeats on-demand loading intent; also frontmatter has no schema validator in this toolchain |
| Separate `stages.yml` per stage (7 files) | Rejected | Increases `Read` calls to 7 per pipeline run; single manifest preserves atomic schema validation |

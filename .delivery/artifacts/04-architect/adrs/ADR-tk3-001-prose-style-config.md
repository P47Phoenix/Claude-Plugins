# ADR-tk3-001: `prose_style` config key, PROSE STYLE dispatch contract, and cache-prefix re-freeze procedure

**Status**: Accepted
**Date**: 2026-05-05
**Pipeline**: run-2026-05-05-tk3
**Stage**: 4 (Architect, light)
**Deciders**: Solution Architect (Saruman of Many Colours), with PO PRD as authoritative input
**Closes**: BACKLOG-102 W2-1, W2-2, W2-3 — contract-level decisions
**Supersedes**: none
**Related**: ADR-001/002/003 (v2.7 routing.force_type), Ruling 1 (skill-token-economy.md cache-prefix freeze)

---

## Context

BACKLOG-102 introduces caveman-lite prose discipline to the delivery-team agent dispatch surface. The PRD at `.delivery/artifacts/02-refine/po/prd.md` consolidates three work items (W2-1, W2-2, W2-3) into one Story and grounds each AC in measured TARGET-state file evidence. The idea-brief at `.delivery/artifacts/01-idea/po/idea-brief.md` sets engagement framing. The binding decisions live in `.delivery/memory/topics/skill-token-economy.md` Ruling 1: the first ~2k tokens of every Tier-A SKILL.md MUST be byte-stable across runs; any prefix change requires an ADR citing cache-cost impact.

Six contract elements span SKILL.md, three dispatch templates, the DoD validator template, and the config schema. Multiple of those elements touch `delivery-team/skills/delivery-flow/SKILL.md` Phase 0 (L31-125), which the PRD §3 asserts is inside the cache-prefix region. Direct measurement confirms the PRD: the `## Phase 0` heading sits at byte 1803, inside the documented 0..2048 prefix slice (SKILL.md L478 Volatile marker). The operational guard `governance/cache-prefix-hash.txt` hashes the whole file. Both interpretations of the freeze (cache-warmup prefix slice and whole-file hash) are invalidated by the Phase 0 edit; Ruling 1's clause — "Any future prefix change MUST require an ADR citing cache-cost impact" — is satisfied by this ADR. This ADR resolves the contract for all six elements and names the precise re-freeze procedure and bounded cache-cost.

---

## Decision

### Element 1 — `prose_style` config key

A new top-level key is added to `.delivery/config.yml`:

| Property | Value |
|---|---|
| Key | `prose_style` |
| Type | `string`; required no; default `caveman-lite`; valid values `caveman-lite \| standard` |
| Location | top-level (NOT nested under `pipeline:`); matches `wizard_completed` precedent for top-level scalar keys |
| Consumed by | `delivery-flow` Phase 0 (read), Phase 4 Step 4 (conditional block injection), Step 7 (validator framing) |

YAML shape: `prose_style: caveman-lite` (default) or `prose_style: standard` (opt-out). Top-level placement is required because the value is read at Phase 0 *before* `pipeline.*` keys and influences agent-dispatch construction across all stages — not pipeline-loop-internal behavior.

### Element 2 — PROSE STYLE block contract

Block content is verbatim from PRD §FR-1 / BACKLOG-102 §W2-1:

```
PROSE STYLE: caveman-lite for narrative-framing prose ONLY (the prose between
signal block and response end, plus signal block SUMMARY field). Drop articles/
filler/pleasantries/hedging; fragments OK; short synonyms; preserve technical
terms exact and code/error-string verbatim. Artifact body uses standard prose.
Auto-clarity exemptions apply: standard prose for security warnings,
irreversible-op confirmations, multi-step sequences, user clarifications.
```

**Resolution algorithm** (orchestrator side, runs once per pipeline invocation, then cached for the run):

1. Phase 0 reads `.delivery/config.yml`; loads `prose_style` (default `caveman-lite` if absent).
2. Phase 0 stores the value in the in-memory loaded-config struct as `config.prose_style`.
3. Phase 4 Step 4 prompt construction reads `config.prose_style`. If `caveman-lite`, the PROSE STYLE block is injected into the dispatch prompt at the insertion point defined below. If `standard`, the block is omitted entirely (no placeholder line, no empty block) so opt-out telemetry shows zero block bytes.
4. **Per-role override is OUT OF SCOPE for v1.** The block is injected uniformly across every role at every stage. If Wave 4 telemetry demonstrates a role for which caveman-lite degrades signal quality, BACKLOG-103+ may add `prose_style.overrides: { <role>: standard }`. Recording this scope decision now prevents Plan-stage scope-creep.

**Insertion point** (binding for all THREE dispatch templates in `references/pipeline-stages.md`): the PROSE STYLE block is inserted as a new section **between `--- ALIAS ---` and `--- OUTPUT ---`**, with delimiter `--- PROSE STYLE ---`. This placement keeps personality (ALIAS) coupled with style (PROSE STYLE) in the prompt, immediately upstream of the output contract. Concrete loci in `references/pipeline-stages.md`:

| Template | Header line | ALIAS block end (current) | PROSE STYLE insertion (target) |
|---|---|---|---|
| Primary Agent Dispatch | L44 | L70 (`{alias_personality_block OR "No alias active."}`) | new block after L70, before `--- OUTPUT ---` (currently L72) |
| Supporting Agent Dispatch | L87 | L113 | new block after L113, before `--- OUTPUT ---` (currently L115) |
| DoD Validator Dispatch | L130 | L161 | new block after L161, before `--- OUTPUT ---` (currently L163) |

The block is conditionally rendered at orchestrator construction time — it is NOT a literal fixture in `pipeline-stages.md`. The reference file documents the template shape (placeholder line `{prose_style_block OR omit}`) and the orchestrator substitutes either the verbatim block (caveman-lite) or omits the section entirely (standard).

### Element 3 — Auto-clarity exemptions

Exempt contexts (revert to standard prose even when `prose_style: caveman-lite`):

1. Security warnings (e.g., world-readable credentials, exposed secrets, vulnerable dependency).
2. Irreversible / destructive op confirmations (e.g., `git revert`, `rm -rf`, `git push --force`, schema migrations dropping data).
3. Multi-step sequences where fragment ordering or omitted conjunctions risks misread.
4. User clarification responses (when the user has asked the agent to clarify or repeat).

**Detection mechanism for v1 (chosen)**: in-prompt directive enforcement by the agent. The PROSE STYLE block already names the four exempt contexts as a directive ("Auto-clarity exemptions apply: standard prose for security warnings, irreversible-op confirmations, multi-step sequences, user clarifications"). The agent is the detector. This is the lower-cost path: no orchestrator-side classifier, no per-dispatch flag, no content scan.

**Why not orchestrator-side flag**: requires pre-classifying every dispatch; orchestrator does not know in advance whether a developer dispatch will confirm a destructive op. **Why not content-match heuristic on output**: post-hoc filtering of compressed prose cannot reconstitute lost articles. Detection must occur during generation where the agent owns the choice.

**Validation surface** (Stage 6 dogfood per PRD §8.4): three synthetic dispatches (security warning / `git revert` confirmation / 4-step migration) inspected for standard-prose verdict; failure on any of three trips the BACKLOG-102 stop-rule.

### Element 4 — DoD validator verdict-prose treatment

The DoD validator template at `references/quality-gates.md` L21-38 produces caveman-lite prose for the **verdict-prose section ONLY** (the freeform sentences surrounding the gate-result tables and findings bullets — capped at 3 sentences in the template body). The following sections retain standard prose:

| Section | Style | Rationale |
|---|---|---|
| `STATUS:` line (DONE / NOT_DONE / CODE_COMPLETE) | verbatim | Value semantics MUST NOT change — downstream parsers grep for these literal tokens. |
| `ARTIFACT:` line (path) | verbatim | File path; not prose. |
| `SUMMARY:` (≤200 char) | caveman-lite | Already terse; lite tightens further per PRD §FR-2. |
| `FINDINGS:` bullet list (each: file/line/criterion) | standard prose preserved | Validators must remain actionable; over-compression of findings is the named over-compression failure mode that arms the BACKLOG-102 stop-rule. |
| Gate-result tables (Markdown table format) | verbatim | Already terse; tabular structure is the compression. |
| Free-form verdict prose (≤3 sentences surrounding the table) | caveman-lite | This is the AC-2 ≥25% reduction surface. |

The template body in `quality-gates.md` adds a single instructional line: "Use caveman-lite for verdict prose; preserve STATUS values, finding format, and table structure verbatim." The dispatch flows through the DoD Validator Dispatch Template (Element 2 insertion in `pipeline-stages.md` L130+), so the runtime PROSE STYLE block is the primary directive; the `quality-gates.md` line is the role-specific contract.

### Element 5 — Cache-prefix re-freeze procedure

**Two interpretations of cache-prefix freeze coexist in the repo and must be reconciled.**

**Interpretation A — documented prefix boundary** (SKILL.md L478 Volatile-section comment): "the prefix boundary sits at the end of Phase 3 (Stage Routing); bytes 0..2048." Cache-warmup behavior depends only on this slice being byte-stable.

**Interpretation B — operational hash guard** (`governance/cache-prefix-hash.txt`): the file contains `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f  delivery-team/skills/delivery-flow/SKILL.md` — a SHA-256 over the **entire file**, not the prefix slice. Any byte change anywhere in SKILL.md flips this hash.

**Byte-impact math** (measured via `wc -c`):

| Region | Lines | Current bytes | Phase 0 edit Δ (estimate) | Projected bytes |
|---|---|---|---|---|
| Documented prefix region | bytes 0..2048 | 2048 | **+50 to +120** (Phase 0 heading at byte 1803, inside the prefix slice; edit lands at L56 config-read sub-block, byte 3529, past the 2048 boundary but within Phase 0; any insertion before byte 2048 in Phase 0 prelude shifts the slice) | 2048 byte-stable IF edit confined to L56+; ELSE re-warm |
| Phase 0 section | L31-125 | 8360 | +50 to +120 (one config-read line + comment) | 8410 to 8480 |
| Phase 0 config-read sub-block | L56-110 | 4831 | +50 to +120 | 4881 to 4951 |
| SKILL.md whole-file | L1-497 | (whole file) | +50 to +120 | new SHA-256 |
| SKILL.md line count | — | 497 lines | +1 to +3 | 498-500 (Tier-A budget 500 — **headroom: 0-2 lines**) |

**Reconciliation and decision**:

1. **Phase 0 IS inside the cache-warmup prefix region.** The `## Phase 0` heading sits at byte 1803 (L31), inside the documented 0..2048 prefix slice; the section spans L31-125. The W2-3 edit lands in the L56-110 config-read sub-block (byte 3529+, past the 2048 boundary) but Phase 0 as a whole sits partly inside the cache-warmup window. The prior reading ("Phase 0 outside the prefix") inverts the measurement and is hereby corrected.

2. **One-time cache-cost is documented and bounded.** Per Ruling 1's clause "Any future prefix change MUST require an ADR citing cache-cost impact" — that ADR is THIS ADR. On the first dispatch post-merge, the warmup-cache slice for `delivery-flow/SKILL.md` is invalidated and re-read from disk (~2KB, one full prefix slice). Subsequent dispatches re-warm the cache normally. Cost is bounded: one full prefix re-read per cache-eviction cycle, not per dispatch.

3. **Acceptance justified.** Idea-brief §7 explicitly anticipated this re-freeze ("must NOT invalidate cache; IF IT DOES, document re-freeze"). Recurring AC-1 (≥20% prose) and AC-2 (≥25% DoD) savings vastly exceed the bounded one-time ~2KB re-warm; net token-economy is positive within the first pipeline run post-merge.

4. **Re-freeze procedure.** After the Phase 0 edit lands, run `sha256sum delivery-team/skills/delivery-flow/SKILL.md > governance/cache-prefix-hash.txt` and commit the result in the same PR as the SKILL.md edit; the hash flip is the observable signal that re-freeze occurred. The whole-file SHA-256 covers both the 0..2048 prefix slice and all body bytes — one regeneration discharges both interpretations of the freeze. Stage 5 Plan MUST list this alongside `delivery-team/scripts/generate-schema.py` as explicit Story DoD tasks per idea-brief §7.

5. **Rollback** (structural rollback distinct from runtime opt-out): **structural** — revert the Phase 0 edit AND restore the prior `cache-prefix-hash.txt` value `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f`; one PR; cache-warmup slice returns to its pre-edit byte-stable state. **Runtime opt-out** (separate) — one-line config change `prose_style: standard` reverts dispatch behavior without touching SKILL.md or the hash. AC-6 satisfied by construction.

6. **Tier-A line budget tightness — binding constraint.** SKILL.md is at 497 of 500 lines (Ruling 3). The Phase 0 edit budget is **3 lines maximum** (one read line + at most two comment/blank lines). Stage 5 Plan stage MUST propagate this constraint to the developer dispatch; if the developer wave needs more, Plan stage MUST batch a same-wave reduction elsewhere in SKILL.md (Architect batching math discipline; `.delivery/memory/stages/architect.md` lesson 5).

7. **Surfaces outside SKILL.md are NOT under the hash guard:**

   | Surface | Locus | Why no separate re-freeze |
   |---|---|---|
   | `SKILL.md` Step 4 prompt construction | L329-345 (byte ~17000+) | Past prefix boundary; whole-file hash regeneration covers it. |
   | `references/pipeline-stages.md` (3 dispatch templates) | L44, L87, L130 | Different file; not under SKILL.md hash guard. |
   | `references/quality-gates.md` (validator template) | L21-38 | Different file; not under SKILL.md hash guard. |
   | `references/config-schema.md` (Element 6) | L5, L15, L207+, L347+ | Different file; not under SKILL.md hash guard. |
   | `references/config-schema.json` | regenerated | Different file; not under SKILL.md hash guard. |

   Conclusion: the only re-freeze artifact this BACKLOG produces is one updated `governance/cache-prefix-hash.txt` line covering the whole-file hash of `delivery-flow/SKILL.md`.

### Element 6 — Schema bump v2.8 → v2.9

Per PRD §FR-3 discovery: the v2.8 slot is already taken (DESIGN routing, dated 2026-04-05 at `config-schema.md` L368). The schema MUST bump to **v2.9**, not v2.8 as BACKLOG-102 W2-3 originally drafted. The PRD records this as the only material deviation from BACKLOG-102 wording; this ADR ratifies it.

| Locus | Current | Target |
|---|---|---|
| `config-schema.md` L5 | `## Current Version: 2.8` | `## Current Version: 2.9` |
| `config-schema.md` L15 (`config_version` row) | `Default: "2.8"` | `Default: "2.9"` |
| `config-schema.md` Schema Table | (no `prose_style` row) | new row: `prose_style \| string \| no \| caveman-lite \| caveman-lite, standard \| defaults \| delivery-flow (Phase 0, Phase 4 Step 4)` |
| `config-schema.md` Config File Template (L211+) | (no `prose_style:` line) | add `prose_style: caveman-lite` after `config_version` line |
| `config-schema.md` Version History (L347+) | last row v2.7 (2026-04-05) | append v2.9 row dated 2026-05-05 with change description |
| `references/config-schema.json` | (regenerated artifact) | regenerated via `delivery-team/scripts/generate-schema.py` after `.md` edits |

**Migration**: Existing v2.7-or-earlier configs auto-migrate (Phase 0 lines 60-64 of SKILL.md). If `prose_style` is absent on load, the orchestrator applies the default `caveman-lite` and surfaces the standard upgrade banner: `> Config upgraded from v2.7 to v2.9. New settings applied with defaults: prose_style=caveman-lite`. The existing v2.6 → v2.7 strip-and-default path (SKILL.md L65-71) is preserved untouched. Configs at v2.8 (none currently in repo per PRD §3) similarly default.

**JSON regeneration**: After `.md` edits, run `python3 delivery-team/scripts/generate-schema.py` to update `references/config-schema.json`. Stage 5 Plan stage MUST list this as an explicit Story DoD task (idea-brief §7 Stage 5 reaffirmed).

---

## Consequences

### Positive

- **Token reduction surface activated**: AC-1 (≥20% response-prose reduction) and AC-2 (≥25% DoD review file reduction) become measurable post-merge via the W0-1 telemetry hook (`.delivery/telemetry/skill-loads.jsonl`).
- **Opt-out is a single config line**: `prose_style: standard` reverts behavior; reversal cost is one-line edit + pipeline restart. AC-6 satisfied by construction.
- **Cache-prefix re-freeze bounded and documented**: Phase 0 edit lands inside the documented 0..2048 prefix slice (heading at byte 1803); one-time ~2KB re-warm cost on first post-merge dispatch is dwarfed by the recurring AC-1/AC-2 token savings, and Ruling 1's "ADR citing cache-cost impact" requirement is satisfied by this ADR.
- **Schema version-history correctness restored**: v2.9 advances past the v2.8 DESIGN-routing slot rather than colliding with it.
- **Top-level config placement consistent with consumption scope**: `prose_style` is read at Phase 0 across all stages, matching its top-level placement.

### Negative / risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Whole-file SHA-256 regeneration is forgotten in Stage 5/6 | medium | breaks CI hash-check gate | Plan-stage Story DoD lists the `sha256sum > governance/cache-prefix-hash.txt` task explicitly. |
| SKILL.md line budget overrun (498-500 of 500) | medium | Tier-A budget violation; CI gate fails | Architect batching math: Phase 0 edit capped at 3 lines; Plan stage propagates constraint to developer dispatch. If overrun, batch a same-wave reduction elsewhere. |
| Validator over-compression masks findings | low-medium | DoD pass-rate regression (NFR-7) | FINDINGS bullets stay standard-prose (Element 4); Stage 7 UAT measures pass-rate vs 4/7 baseline; stop-rule armed. |
| Auto-clarity exemption mis-detection | low-medium | security/destructive prose compressed | In-prompt directive (Element 3); Stage 6 dogfood per PRD §8.4 spot-checks 3 synthetic dispatches; failure trips stop-rule. |
| Per-role override pressure during Stage 6 | low | scope creep into v2 contract | Element 2 explicit: per-role override is OUT OF SCOPE for v1; revisit only after Wave 4 telemetry. |

### Reversibility

- **Config-level reversal** (single user, single project): edit `.delivery/config.yml` → `prose_style: standard`. Cost: one line + one pipeline restart.
- **Schema-level rollback** (full revert): revert the v2.9 schema bump and Phase 0 edit. Cost: one PR; cache-prefix-hash.txt regenerates back to current value `9d4011d…`. No data migration.
- **Surface-level rollback** (keep config key, drop block injection): comment out the Step 4 conditional. PROSE STYLE block stops being emitted; no other surface is affected.

---

## Alternatives considered

| Alternative | Pros | Cons | Why rejected |
|---|---|---|---|
| Per-role `prose_style.overrides` map in v1 | Future-proof; finer control | Scope creep; no telemetry yet to justify per-role variance; doubles validation surface | DEFERRED to BACKLOG-103+ pending Wave 4 telemetry showing a role for which caveman-lite degrades signal. |
| Hard-code caveman-lite (no config key) | Simpler; one fewer surface | Violates BACKLOG-102 AC-6 (opt-out gate); zero reversibility | Rejected on AC compliance. |
| Adopt external `juliusbrussee/caveman` skill plugin as marketplace dependency | Reuse upstream maintenance; full caveman ladder (lite/full/ultra) | Adds external plugin dependency; BACKLOG-102 §Out-of-Scope explicitly excludes; pulls a fourth-party plugin into our supply chain | Rejected per BACKLOG-102 §Out-of-Scope. |
| Nest `prose_style` under `pipeline.*` | Clusters with other pipeline-loop keys | Misrepresents consumption scope (Phase 0 reads it, all stages use it — not pipeline-loop-internal); breaks discoverability | Rejected on consumption-scope mismatch. |
| Bump schema to v2.8 (per BACKLOG-102 W2-3 wording) | Matches original backlog text | v2.8 slot is already taken (DESIGN routing, 2026-04-05); collision corrupts version history | Rejected per PRD §3 surface evidence; v2.9 is the only correct target. |
| Orchestrator-side auto-clarity classifier | Centralized detection | Inverts information flow (orchestrator does not know intent in advance); adds runtime cost on every dispatch | Rejected; in-prompt directive (Element 3) is the v1 mechanism. |
| Treat the whole-file SHA-256 hash as the "real" prefix freeze | Single source of truth | Conflates cache-warmup mechanics (only first ~2k tokens matter) with governance-process integrity (whole file) | Rejected; both interpretations coexist with distinct purposes. ADR names both. |

---

## References

- **BACKLOG-102**: `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`
- **Idea brief**: `.delivery/artifacts/01-idea/po/idea-brief.md`
- **PRD**: `.delivery/artifacts/02-refine/po/prd.md`
- **Binding decisions (Ruling 1, cache-prefix freeze)**: `.delivery/memory/topics/skill-token-economy.md`
- **Architect stage memory (binary status, batching math)**: `.delivery/memory/stages/architect.md`
- **Cache-prefix hash artifact**: `governance/cache-prefix-hash.txt`
- **Schema generator**: `delivery-team/scripts/generate-schema.py`
- **caveman external repo**: https://github.com/juliusbrussee/caveman
- **Target surfaces** (read-and-frozen at Stage 4):
  - `delivery-team/skills/delivery-flow/SKILL.md` Phase 0 (L31-125; W2-3 edit lands in the L56-110 config-read sub-block), Step 4 (L329-345), Step 7 (L377-402)
  - `delivery-team/skills/delivery-flow/references/pipeline-stages.md` dispatch templates (L44, L87, L130)
  - `delivery-team/skills/delivery-flow/references/quality-gates.md` validator template (L21-38)
  - `delivery-team/skills/delivery-flow/references/config-schema.md` (L5, L15, L207+, L347+)

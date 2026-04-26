# Transformation Plan — Claude-Plugins: Opus 4.6 → 4.7

**Artifact:** Transformation Plan (AS-IS → TO-BE → Roadmap)
**Stage:** 4 / Architect (TERMINUS — plan-only engagement per PRD Constraint 8)
**Sub-workflow:** transformation-planning (consolidated single-artifact form per Galadriel's "garden tended without a map made of every stone" scope)
**Date:** 2026-04-20
**Architect:** Celebrimbor — *"Let us forge something that will endure beyond the ages."*
**Upstream inputs:**
- `.delivery/artifacts/01-idea/po/idea-brief.md` (Gandalf, 2026-04-20)
- `.delivery/artifacts/02-refine/po/prd.md` (Gandalf, rev 2 — 577 lines, 10 REQs, 29 findings)
- `.delivery/artifacts/02-refine/data/scope-baseline.md` (Elrond)
- `.delivery/artifacts/03-design/dx/skill-author-dx.md` (Galadriel — 7 pillars, 6 patterns, 5 DX metrics, 7 open questions)
- `.delivery/artifacts/02-refine/challenger/loop2/review.md` (adversarial 4/5 confidence, 8 findings)
- `.delivery/artifacts/02-refine/dod/round2/*.md` (DoD round 2 — all DONE)
- `CLAUDE.md` (repo conventions, config v2.7)

**Companion artifacts (this engagement):** six ADRs at `.delivery/artifacts/04-architect/adrs/ADR-00{1..6}-4-7-*.md`

---

> *"The ore has been weighed. The old work has been read. What must be mended is named; what must stand is named; the order of the forging is set. A plan is a ring of its own — only smaller, and without the fire."*

---

## 1. Executive Summary

This plan mends the six Claude-Plugins marketplace plugins to speak faithfully to Claude Opus 4.7, without rebuilding what already holds. The PRD showed the migration surface is small: three hard-coded dated model IDs in one Python file, six keystone SKILL.md files carrying behavioural or prose-level 4.6-era assumptions, one orchestrator dispatch contract that 4.7's "fewer subagents by default" promotes from stylistic to load-bearing, and a tone-flattening risk across thirteen alias themes. The surface is real, grep-invisible in places, and sequenceable.

**What changes:** (a) 10 lines across 2 Python files get current or commented-as-legacy model IDs; (b) 6 SKILL.md keystones receive targeted 4.7-aware edits (one pattern-library expansion, one dispatch-contract annotation, two additive prose audits, two tone-validation dogfoods); (c) all 17 SKILL.md files gain a 3-field forward-compatibility header (model_awareness / last_audited / pattern_library_version); (d) a 4.7 baseline capture is produced on the first implementation run, serving as the reference for every regression metric.

**What stays:** plugin architecture, three-level context loading, hook event model, config schema v2.7, marketplace.json structure, the 7-stage delivery pipeline shape, the 6 collaboration patterns, the deterministic Business Rules Engine. PRD Non-Goals and Constraint 2 hold.

**Why now:** because the repo already runs on Opus 4.7 (per CLAUDE.md). The assistant at this very keyboard is Opus 4.7; every day the marketplace serves 4.6-shape prose to a 4.7 runtime is a day of slow drift. And because F-25 (more literal instruction following) raises the cost of silently-stale prose — on 4.7, "CRITICAL: never X" reads *literally never*, even when the author meant *usually don't*.

**Key architectural decisions (see §5):** migration paradigm is keystone-first rolling in 4 waves (ADR-001); model IDs stay as direct strings with provenance comments, not a central alias (ADR-002); extended-thinking adoption is document-only in one file (ADR-003); prompt-caching is out of engagement, latent until SDK wiring (ADR-004); the 4.7-era pattern library lives centrally in `prompt-engineer/SKILL.md` with citation-by-name (ADR-005); the 4.7-readiness marker is a three-field YAML frontmatter header strip (ADR-006, Accepted with mechanical rollback to HTML-comment placement if WI-03 spike reports strict validation).

**Scope terminus:** the end-state of this engagement is **this roadmap**. Implementation is a separate delivery-flow run. No code is produced here.

---

## 2. AS-IS: Behavioral Snapshot

### 2.1 How plugin skills behave today on Opus 4.7 — empirical evidence

This pipeline (Idea → Refine → Design → Architect) has executed on Opus 4.7 through Stage 4. Every prior stage produced its expected artifacts: the Idea brief (Gandalf), the PRD rev 0→1→2 (Gandalf), the scope baseline (Elrond), the DX design (Galadriel), two full DoD rounds, and two challenger loops. **Presence-of-output confirmed for Idea and Refine stages on 4.7 (PRD Assumption A-05 firming).**

What this does *not* yet confirm: that the *right number* of sub-agents dispatched for each DoD round. F-08 ("fewer subagents spawned by default; steerable through prompting") makes silent sub-agent fusion the highest-confidence regression mode on 4.7. The PRD's REQ-09 AS-IS validator-dispatch count capture is queued as **WI-01** in Wave 1 and must execute before any prose edit lands.

### 2.2 Per-plugin 4.6-era assumption map

Anchored to PRD inventory identifiers:

| Plugin | 4.6-era assumption surface | PRD anchors | Behavioural risk on 4.7 |
|---|---|---|---|
| `delivery-team/` → `delivery-flow/SKILL.md` (1072 LOC) | "One role = one sub-agent" enforced *stylistically* (DISP-01 lines 328–345). Adversarial-review pattern vulnerable to F-27 tone shift. Theme-driven stage announcements (DISP-03 line 361). | F-08, F-25, F-27; DISP-01/02/03; SZ-16 | **Load-bearing on 4.7.** Silent sub-agent fusion would break DoD semantics. |
| `delivery-team/` → `product-delivery/SKILL.md` (685 LOC) | Role-behaviour rules stated with some inference ("PO auto-logs issues from research" style — memory `feedback_po_logs_issues.md`). | F-25; SZ-15 | Under-specified instructions may be executed differently on 4.7 (literal following). |
| `delivery-team/` → `architect/SKILL.md` (667 LOC) | Largest technical-instruction surface; 11 roles + paradigm routing. | F-25, F-26; SZ-14 | Inferred instruction patterns; scaffolding potentially redundant with 4.7 defaults. |
| `delivery-team/` → paradigm sub-skills (volatility 66 LOC, ddd 80 LOC) | None detected. | SZ-01/02 | None. |
| `delivery-team/` → 11 other skills (godot, developer, quality, operations, ui, user-feedback, alias-creator, presentation, quality) | No API-shape patterns, no model IDs, no 4.6-specific prose detected. | SZ-03/04/05/06/07/10/11/12 | Marker-header addition only (ADR-006). |
| `delivery-team/` → 13 alias theme YAMLs | Theme voice markers (`catchphrase`, `examples`) may read flatter on 4.7 per F-27. | F-27; DEV-02 path correction | Tone flattening. Validated via REQ-05 dogfood, not pre-emptively edited. |
| `agentic-flow-builder/` → `agent_registry.py` | MID-01/02/03: three hard-coded dated model IDs (lines 148, 172, 187). Registry metadata only — zero SDK imports. | F-04, MID-01/02/03 | Drift hygiene only (not runtime). Foot-gun for marketplace consumers. |
| `agentic-flow-builder/` → `flow-builder/SKILL.md` (559 LOC) | One generic "Claude models (Sonnet, Opus, Haiku)" mention at line 45. | SZ-13 | Cosmetic. |
| `prompt-engineer/SKILL.md` (440 LOC) | PAT-01 line 85 conflates `<thinking>` tags with "reasoning visibility" (inaccurate on 4.7). PAT-02, PAT-06 valid manual CoT scaffolds. | F-13, F-25, F-26, F-29; PAT-01/02/06; SZ-08 | **Meta-drift**: teaches prompt patterns that other authors inherit. |
| `prd-quality-gate-flow/stage_definitions.py` | MID-04: 7 family-alias strings (`claude-sonnet`, `claude-haiku`) on 7 lines. UV-01 unresolved — likely internal routing labels, zero SDK imports confirmed. | F-03, MID-04; UV-01 | Behavioral resolution TBD (Phase 1B structural check). |
| `research-agent/SKILL.md` (471 LOC) | Zero API-shape patterns. Behavioural risk from F-07 (fewer tool calls by default) — silent hallucination-risk if agent reasons instead of WebFetch. | F-07; SZ-09 | **Highest behavioural risk** on 4.7 — grep-invisible. Validated via REQ-03B dogfood probe. |
| `mtg-commander/SKILL.md` (1181 LOC) | Adversarial Challenger prose (tone-risk under F-24/F-27). Largest SKILL.md in the repo. | F-24, F-27, NDOC-03; SZ-17 | Tone flattening in Challengers. User-visible. Validated via REQ-04 dogfood. |

### 2.3 Observable behaviors that should persist post-migration

- The 7-stage pipeline shape (Idea → Refine → Design → Architect → Plan → Development → UAT).
- Team DoD validation (all validators must DONE).
- The 6 collaboration patterns (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus).
- Config schema v2.7 exactly (Constraint 5 frozen).
- Hook event model and the seven hook entries in `delivery-team/hooks/hooks.json` (Constraint 2 frozen).
- Marketplace.json structure and all plugin IDs (Constraint 2 frozen).
- The `SKILL_LOADED` signal protocol and the per-stage dogfood contract (Galadriel P-4).
- Every alias theme's role-per-alias mapping exactly. Tone may be strengthened but mapping stays.

### 2.4 Observable behaviors slated to change

- `prompt-engineer/SKILL.md` will teach 4.7-aware patterns (PAT-01 re-framed, new Model-specific sub-section, six Galadriel patterns added).
- `delivery-flow/SKILL.md` will carry a 4.7-era annotation explaining why the "one role = one sub-agent" rule is now behavioural not stylistic (ADR-001, REQ-03).
- All 17 SKILL.md files will declare `model_awareness`, `last_audited`, `pattern_library_version` in frontmatter (ADR-006).
- Challenger and adversarial-review outputs must meet an explicit checklist (PRD AC-04.2): ≥3 weaknesses, ≥2 specific referents, ≥1 concrete alternative per invocation.
- Research-agent invocations must cite ≥2 WebFetch/WebSearch calls (PRD AC-03B.2, hardened per challenger loop2 Finding #4 to require ≥2 *distinct hostnames*).

---

## 3. AS-IS: Structural Snapshot

### 3.1 High-level repo shape (not a directory dump)

- **Six plugin directories** under the repo root, each a self-contained plugin.
- **Marketplace registry** at `.claude-plugin/marketplace.json` (frozen this engagement).
- **Repo conventions** in `CLAUDE.md` (binding).
- **CI regression guards** under `.github/workflows/` (`workflow-injection-lint.yml` — DEFECT-004 guard, must not regress per Constraint 6).
- **Historical record** under `.delivery/` (not in sweep scope per Constraint 4).

### 3.2 Classification by migration impact

**Keystone (6 files — read in full, edit-considered):**

1. `delivery-team/skills/delivery-flow/SKILL.md` (1072 LOC) — dispatch contract.
2. `mtg-commander/SKILL.md` (1181 LOC) — adversarial Challenger prose.
3. `delivery-team/skills/product-delivery/SKILL.md` (685 LOC) — role-instruction surface.
4. `delivery-team/skills/architect/SKILL.md` (667 LOC) — largest technical-instruction surface.
5. `research-agent/SKILL.md` (471 LOC) — behavioural tool-use risk.
6. `prompt-engineer/SKILL.md` (440 LOC) — pattern-library meta-drift.

**Affected (non-keystone edits):**

- `agentic-flow-builder/scripts/agent_registry.py` (model-ID sweep, 3 lines: 148, 172, 187).
- `prd-quality-gate-flow/stage_definitions.py` (family-alias clarification or replacement, 7 lines pending UV-01 resolution: 47, 83, 115, 150, 181, 216, 243).
- 11 non-keystone SKILL.md files (frontmatter-only addition of ADR-006 marker — mechanical).
- 13 alias theme YAML files in `delivery-team/skills/delivery-flow/references/aliases/` (only if REQ-05 dogfood reveals regression — edit-conditional, not edit-mandatory).

**Untouched (verified zero-change):**

- All hook scripts under `delivery-team/hooks/` (HK-01..07 — zero 4.6-era prompt text per PRD §3.5).
- `delivery-team/hooks/hooks.json` (frozen per Constraint 2).
- All `scripts/` utilities in `delivery-team/` and elsewhere (no LLM-facing text).
- `prd-quality-gate-flow/prd_flows.db` (SQLite data, not code — PRD §3.9 excluded by Section 4 ACs).
- All `.delivery/` contents (Constraint 4 excludes).
- `marketplace.json` (Constraint 2 + PRD §3.2 MKT-01 confirmed no model-version strings).

### 3.3 Classification by change type

- **(a) Model-ID sweep:** REQ-01. 2 files, ~10 lines. Mechanical.
- **(b) Prompt-pattern refresh:** REQ-02 + REQ-03. 6 keystone SKILL.md files. Prose-level — some additive (REQ-03), some corrective (REQ-02 AC-02.2 PAT-01), some dogfood-gated (REQ-02 AC-02.3).
- **(c) New-capability opt-in:** `xhigh` effort and adaptive-thinking adoption — explicitly document-only per ADR-003. `task_budget` and memory tool — explicitly NEW-BACKLOG per REQ-07.
- **(d) Documentation:** ADR-006 marker addition to all 17 SKILL.md files. Galadriel on-ramp artifacts (CONTRIBUTING-4-7.md note, migration-guide stub) sequenced in Wave 4 as deferred-by-agreement-with-Galadriel.
- **(e) Hooks:** **No hook edits.** HK-01..07 are deterministic Python / SKILL_LOADED-detection only; zero LLM-facing prompt text. Confirmed by PRD §3.5 grep and round 2 DoD.

### 3.4 Dependency / ordering constraints

- **REQ-10 (baseline capture) precedes every delta metric.** M-03, M-04, M-05, M-07 all reference the baseline artifact path. No prose edit ships before baseline is captured.
- **REQ-09 (AS-IS validator-dispatch count) precedes REQ-03 annotation.** If counts diverge, R-09 fires and sequencing changes (silent F-08 fusion would have to be mitigated first).
- **ADR-005 pattern library expansion (WI-05) precedes the citation edits** in other SKILL.md files. You cannot cite an anchor that does not exist. The four other keystone edits (WI-06, WI-07, WI-08, WI-09) thus sequence *after* WI-05.
- **REQ-04 (adversarial dogfood) precedes any mtg-commander / delivery-flow adversarial prose edit.** PRD AC-04.3: dogfood-before-edit. If no regression, DOCUMENTATION-ONLY.
- **REQ-05 (alias-theme dogfood) precedes any theme YAML edit.** PRD AC-05.2: no edit without regression.
- **REQ-03B (research-agent dogfood) precedes any research-agent prose edit.** PRD AC-03B.3.
- **Frontmatter marker (ADR-006, WI-11) sequences last** so `last_audited` dates reflect actual review state.

---

## 4. TO-BE: Target State

### 4.1 DX pillars become architecture principles

I adopt all seven of Galadriel's DX pillars (P-1..P-7) as architecture principles for this engagement, with two amendments justified below.

- **P-1 (Forward-Compatibility Header Strip) — ADOPTED.** Implemented as ADR-006 three-field YAML frontmatter.
- **P-2 (Pattern-Library Singleton) — ADOPTED.** Implemented as ADR-005 centralised in `prompt-engineer/SKILL.md`.
- **P-3 (Fail-Soft on Older / Different Models) — ADOPTED.** Implemented via ADR-003 (document-only thinking adoption) and by keeping 4.7-specific content in Model-specific sub-sections only.
- **P-4 (Observable Orchestration Contract) — ADOPTED.** Implemented via REQ-03 annotation + existing `verify_skill_load.py` hook + new M-03 count-paired-with-hit-rate metric.
- **P-5 (Calibrated Prompt-Pressure) — ADOPTED AS MEASUREMENT, NOT AS BLANKET EDIT.** Amendment: PRD REQ-06 is COULD, not MUST. The convention is MUST (Galadriel P-5), but the audit is optional this engagement. Wave 4 WI-12 runs the DX-M5 ratio measurement; line-by-line edits are deferred to backlog unless a keystone exceeds 10% without justification. **Justification for amendment:** PRD Non-Goal of "no prompt-pattern rewrite without evidence of regression" — measurement first, edit second.
- **P-6 (Memory of Prompt-Caching Breakpoints) — ADOPTED AS LATENT.** Implemented via ADR-004 (out-of-engagement; latent until SDK wiring). No change this engagement; backlog note drafted.
- **P-7 (Consistent Role-Prompt Shape) — ADOPTED.** Implemented as Galadriel Pattern 4.2 in `prompt-engineer/SKILL.md` (WI-05). Amendment: the shape is documented as a *reusable pattern* not as a *mandatory rewrite of existing invocations*. Existing dispatch invocations in delivery-flow already follow the shape (DISP-01 enforces it stylistically). **Justification for amendment:** REQ-03 keeps delivery-flow edits annotation-only; a mandatory rewrite would violate that boundary.

### 4.2 4.7-era SKILL.md structural template (≤ 30-line sketch)

```markdown
---
name: <skill-name>
description: <one-line purpose>
model_awareness: opus-4-7
last_audited: YYYY-MM-DD
pattern_library_version: 4-7-1
---

# <Skill Title>

<One paragraph purpose. Model-agnostic.>

## <Skill-specific sections — existing structure unchanged>

…

## Model-specific optimisation — Claude Opus 4.7   (Galadriel Pattern 4.5)

Only for skills teaching prompt mechanics (e.g., prompt-engineer) or
skills that carry 4.7-era levers in their guidance (e.g., delivery-flow
dispatch annotation). Most SKILL.md files OMIT this section — P-3
fail-soft.

- Adaptive thinking is the only thinking-on mode (F-11).
- xhigh effort recommended on Opus 4.7 for coding / agentic (F-15).
- On Opus 4.7, manual CoT scaffolding may duplicate adaptive thinking —
  evaluate case-by-case (F-26, F-29).

## References / See also

- For 4.7 prompt patterns: see prompt-engineer/SKILL.md#pattern-4-N-...
```

### 4.3 4.7-era pattern library in `prompt-engineer/SKILL.md` — six patterns

Per ADR-005 and Galadriel §4, the pattern library is centralised here. Six named patterns, each a brief line:

- **Pattern 4.1 — Versioned Model Reference:** Python/config callers name model IDs with a provenance comment (PRD F-01/F-03/F-04).
- **Pattern 4.2 — 4.7-Aware Role Prompt Skeleton:** `SKILL / TASK_TYPE / ROLE / ALIAS / INPUT ARTIFACTS / YOUR TASK / OUTPUT / SIGNAL BLOCK` shape for every agent dispatch.
- **Pattern 4.3 — Manual CoT Fallback:** `<thinking>` tags as prompt scaffolds in few-shot examples, NOT as reasoning-visibility mechanism (F-29, F-13).
- **Pattern 4.4 — Calibrated Instruction Voicing:** "Use …" / "Do …" framing default; `CRITICAL:` / `You MUST` / `NEVER` reserved for irreversibles (F-28, F-25).
- **Pattern 4.5 — Model-Specific Optimisation Sub-section:** isolates 4.7-only guidance in one named sub-section per model for clean future migration.
- **Pattern 4.6 — SKILL.md Forward-Compatibility Header:** three-field frontmatter (ADR-006).

Full pattern body authoring is **implementation scope**, not plan scope. The names and one-line intents are fixed here; the prose lives in the Wave 3 WI-05 edit.

### 4.4 Cross-cutting TO-BE invariants

- **Model-ID single-source-of-truth strategy:** direct strings with provenance comments (ADR-002). No central alias module this engagement. If/when SDK wiring lands, `claude-api` skill owns the upgrade to a central module.
- **Migration marker convention:** ADR-006 three-field YAML frontmatter on every SKILL.md. CI warns (not blocks) on missing `model_awareness` field.
- **Fail-soft behavior:** Per Galadriel P-3, SKILL.md files stay model-agnostic in core instructions. 4.7-only guidance lives under `## Model-specific optimisation — Claude Opus 4.7` sub-sections. A skill called from a non-4.7 model still works; the 4.7 sub-section is additive.
- **Observable orchestration contract:** Per Galadriel P-4 and REQ-03, every dispatching skill emits `SKILL_LOADED: <name>` and one-role-per-dispatch. M-03 pairs dispatch count (expected from `.delivery/config.yml` `dod_validators.<stage>`) with first-attempt hit rate to detect silent F-08 fusion.
- **Baseline-anchored regression:** REQ-10 captures the 4.7 baseline on the first implementation dogfood. All "regression vs baseline" metrics (M-04, M-05, M-07) measure against that file, not against a non-existent 4.6 historical capture.

---

## 5. Decision Record Pointers (ADRs)

Six ADRs produced this engagement. Each lives at `.delivery/artifacts/04-architect/adrs/`:

| ADR | Decision | Status | File |
|---|---|---|---|
| ADR-001 | Migration paradigm — keystone-first rolling in 4 waves | Accepted | `ADR-001-4-7-migration-paradigm.md` |
| ADR-002 | Model-ID reference strategy — direct strings with provenance comments | Accepted | `ADR-002-4-7-model-id-reference-strategy.md` |
| ADR-003 | Extended-thinking adoption — document-only, defer runtime adoption | Accepted | `ADR-003-4-7-extended-thinking-adoption.md` |
| ADR-004 | Prompt-caching adoption scope — out-of-engagement, latent | Accepted | `ADR-004-4-7-prompt-caching-scope.md` |
| ADR-005 | Pattern-library location — centralised in `prompt-engineer/` with citation-by-name | Accepted | `ADR-005-4-7-pattern-library-location.md` |
| ADR-006 | 4.7-readiness marker — YAML frontmatter three-field header strip | Accepted (with mechanical rollback trigger: WI-03 "strict" verdict → Option B HTML-comment placement, same semantics) | `ADR-006-4-7-readiness-marker-convention.md` |

Each ADR carries Context / Decision / Consequences / Alternatives Considered / Implementation Notes.

---

## 6. Roadmap — The Deliverable

### 6.1 Work items table

14 work items across 4 waves (WI-14 added in revision — see §12 Revision Log). WI-NN format; T-shirt sizes are Architect estimates (non-binding on implementation run per PRD DEF-02 protocol).

| WI | Wave | Title | Scope | T-shirt | Dependencies | Parallelisable with | PRD anchors |
|----|------|-------|-------|---------|--------------|---------------------|-------------|
| WI-01 | 1 | AS-IS validator-dispatch count capture | Read pipeline run logs for Idea + Refine stages; compare actual dispatches to `.delivery/config.yml` `dod_validators.<stage>` list length (idea=2, refine=4). Output: `.delivery/artifacts/<impl-run>/observability/4-7-as-is-dispatch-counts.md` | XS | — | WI-02 | REQ-09, AC-09.1 |
| WI-02 | 1 | 4.7 baseline capture | First full delivery-flow dogfood run on 4.7; capture **(a)** SKILL_LOADED first-attempt rate, **(b)** dispatch counts per stage, **(c)** one Challenger sample (mtg-commander), **(d)** one adversarial-review sample (delivery-flow), **(e)** one rendered stage-announcement per 3 sampled themes, **(f)** count of `audit_agent_prompt.py` hook warnings emitted per run (per Samwise advisory #3 — F-25 literal-following may cause compound-role regex over-match on 4.7; baseline is needed to detect regression). **Format locked to JSON** (per Samwise advisory #5 — downstream metrics M-03/M-04/M-05/M-07 do numeric comparison; `jq` over JSON is the cheapest future-CI shape). Output: `.delivery/artifacts/<impl-run>/observability/4-7-baseline.json` with keyed fields `skill_loaded_first_attempt_rate`, `dispatch_counts_per_stage` (object keyed by stage name), `challenger_sample_path`, `adversarial_review_sample_path`, `alias_announcement_samples` (array of `{ theme, rendered_text }`), `audit_hook_warning_count`. | S | — | WI-01 | REQ-10, AC-10.1; Samwise advisories #3 + #5 |
| WI-03 | 1 | NDOC-02 frontmatter-contract spike (Wave-2 hard blocker) | WebFetch the two candidate Anthropic reference pages for the SKILL.md / Skill tool frontmatter contract: (URL-A) `https://docs.claude.com/en/docs/claude-code/plugins-reference` (Claude Code plugin reference — authoritative for `SKILL.md` frontmatter if carried there) AND (URL-B) `https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview` (Agent Skills overview — authoritative for Skill-tool frontmatter contract). Record which page speaks to the contract and the verbatim clause on unknown-field behaviour. Verdict must be one of: `{ "unknown-fields-accepted" (Option A ships) \| "strict" (ADR-006 rollback trigger fires; Option B HTML-comment placement ships) }`. Output: finding at `.delivery/artifacts/<impl-run>/research/ndoc-02-spike.md` with (i) URLs fetched, (ii) fetch date, (iii) verbatim quote, (iv) verdict string. **Wave 2 MUST NOT dispatch until this file exists and contains a verdict.** | XS | — | WI-01, WI-02 | NDOC-02, ADR-006 rollback trigger, challenger loop2 Finding #8, fresh-challenger F-C-01, Legolas NIT-01 |
| WI-04 | 2 | `delivery-flow/SKILL.md` 4.7 dispatch annotation | Additive annotation (not rewrite) at lines 14–62 (DISP-02) and 328–345 (DISP-01) explaining F-08 promotes "one role = one sub-agent" from stylistic to behavioural. Add `model_awareness`/`last_audited`/`pattern_library_version` frontmatter per ADR-006. | S | WI-01, WI-02, WI-03 | WI-05 | REQ-03, AC-03.1/2/3/4; DISP-01/02; F-08, F-25 |
| WI-05 | 2 | `prompt-engineer/SKILL.md` pattern-library expansion + PAT-01 reframe | PAT-01 line 85 re-framed (F-13 / F-29 accurate framing). New Model-specific-optimisation sub-section (F-11, F-15, breaking changes). Six Galadriel patterns added as named sub-sections with stable anchors. ADR-006 frontmatter. | M | WI-01, WI-02, WI-03 | WI-04 | REQ-02, AC-02.1/2; PAT-01/02/06; ADR-003, ADR-005; Galadriel Patterns 4.1–4.6 |
| WI-06 | 2 | `research-agent/SKILL.md` tool-use dogfood probe | Run one non-trivial research invocation on 4.7. Measure via an explicit transcript-grep command (see §6.2 WI-06 AC-03B.2 spec): count `WebFetch(` and `WebSearch(` tool-call tokens in the sub-agent transcript; extract hostnames from `WebFetch(url=...)` arguments. Gate passes iff `grep -cE '^(WebFetch|WebSearch)\(' <transcript>` returns ≥2 AND distinct hostnames parsed from the transcript (`grep -oE 'https?://[^/ )]+' <transcript> \| sort -u \| wc -l`) returns ≥2 AND every factual claim in the research output carries a URL. If pass: documentation-only. If fail: schedule targeted prose edit ("WebFetch every primary source; never infer a fact without a URL" — F-28 calibrated voicing). ADR-006 frontmatter applied regardless. | S (pass) / M (regression) | WI-01, WI-02 | WI-04, WI-05 | REQ-03B, AC-03B.1/2/3; F-07, SZ-09; fresh-challenger F-C-02 |
| WI-07 | 3 | `product-delivery/SKILL.md` F-25 audit | Prose-read for inferred role-behaviour rules (e.g., "PO auto-logs issues from research" class of rule). Output either (a) list of under-specified instructions to reword in impl run, OR (b) Done-with-reason. Cite pattern 4.2 by name where the dispatch shape applies. ADR-006 frontmatter. | S | WI-05 (pattern-library must exist before citations land) | WI-08 | REQ-02, AC-02.3; F-25; SZ-15 |
| WI-08 | 3 | `architect/SKILL.md` F-25/F-26 audit | Prose-read for (a) under-specified instructions (F-25), (b) scaffolding that duplicates 4.7 default (F-26 — e.g., "after 3 steps, summarise"). Output recommendations. Cite patterns 4.2, 4.4 by name where applicable. ADR-006 frontmatter. | S | WI-05 | WI-07 | REQ-02, AC-02.1; F-25, F-26; SZ-14; challenger loop2 Finding #2 |
| WI-09 | 3 | `mtg-commander/SKILL.md` adversarial-tone audit + REQ-04 dogfood | Prose-read for Challenger tone prose (F-24, F-27). Run one Challenger invocation on 4.7; verify against AC-04.2 concrete checklist: ≥3 weaknesses, ≥2 card-specific referents, ≥1 concrete alternative. Persona review saved to `.delivery/artifacts/<impl-run>/user-feedback/adversarial-4-7-sample.md`. If pass: documentation-only. If fail: targeted tone-strengthening prose edit. ADR-006 frontmatter. | S (pass) / M (regression) | WI-02 (baseline for regression comparison) | WI-05, WI-07, WI-08 | REQ-04, AC-04.1/2/3/4; F-24, F-27, NDOC-03; SZ-17; challenger loop2 Finding #2 |
| WI-10 | 4 | Model-ID sweep — `agent_registry.py` + `stage_definitions.py` | MID-01 line 148: `claude-sonnet-4-5-20250929` → `claude-sonnet-4-6` (canonical per F-03) + provenance comment (ADR-002). MID-02 line 172: discovery task (AC-01.3) to decide target — likely `claude-haiku-4-5-20251001`. MID-03 line 187: `claude-opus-4-20250514` → `claude-opus-4-7` + provenance comment (retires 2026-06-15 per F-04 noted inline). MID-04 (stage_definitions.py 7 lines): structural AS-IS check of `flow_orchestrator.py` first (challenger loop2 Finding #5 — AC-01.5 gate). If labels never reach SDK: comment-annotate only. If they do: substitute canonical IDs. | S | WI-02 | WI-11, WI-12, WI-13 | REQ-01, AC-01.1/2/3/4/5; MID-01/02/03/04; ADR-002; F-04 |
| WI-11 | 4 | Frontmatter marker backfill (non-keystone SKILL.md files) | Add ADR-006 three-field YAML frontmatter to **every SKILL.md file in the scope-baseline §4 inventory that is not one of the six keystones and has not already been stamped in Waves 2–3.** Count follows from the rule: scope-baseline §4 names 17 SKILL.md files; keystones are the 6 named in §3.2; the backfill set is the complement. Verified against scope-baseline §4 today: the complement is exactly 11 files — `agentic-flow-builder/skills/flow-builder/SKILL.md`, `delivery-team/skills/alias-creator/SKILL.md`, `delivery-team/skills/architect/paradigms/ddd/SKILL.md`, `delivery-team/skills/architect/paradigms/volatility/SKILL.md`, `delivery-team/skills/developer/SKILL.md`, `delivery-team/skills/godot/SKILL.md`, `delivery-team/skills/operations/SKILL.md`, `delivery-team/skills/presentation/SKILL.md`, `delivery-team/skills/quality/SKILL.md`, `delivery-team/skills/ui/SKILL.md`, `delivery-team/skills/user-feedback/SKILL.md`. Impl-run re-derives the list from scope-baseline §4 at execution time — the count follows from the rule, not from this table. Mechanical PR; prose untouched. `last_audited` set to backfill date with note "frontmatter-only; no prose review performed" and `model_awareness` set to `opus-4-7-frontmatter-only` (honest tag — distinguishes reviewed-against-4.7 keystones from mechanical-stamp backfills; full `opus-4-7` upgrade deferred to a future prose-skim backlog item, see §6.5). | XS | WI-04, WI-05, WI-06, WI-07, WI-08, WI-09 (keystones stamped first so their dates match their review dates) | WI-10, WI-12, WI-13 | ADR-006, Galadriel DX-M4 (header coverage target 0 missing); fresh-challenger F-C-08 / priority #3 |
| WI-12 | 4 | Alias-theme tone dogfood + optional edit | Sample 3 themes from `delivery-team/skills/delivery-flow/references/aliases/` (DEV-02 corrected path). Extract markers via `yq '.roles[].catchphrase' + yq '.roles[].examples[]'`. Run one delivery-flow stage announcement per sampled theme on 4.7. Score marker-match rate. Target: ≥80% of announcements with ≥50% marker preservation. Save to `.delivery/artifacts/<impl-run>/user-feedback/alias-theme-sample.md`. If target met: no edit. If not: targeted tone-strengthening of the affected theme YAML (NOT the alias-creator SKILL.md / theme-format.md). | S (pass) / M (regression) | WI-02 | WI-10, WI-11, WI-13 | REQ-05, AC-05.1/2/3; F-27; M-05; DEV-02 |
| WI-13 | 4 | NEW-BACKLOG registration + optional REQ-06 over-pressure audit | Register two backlog items: `BACKLOG-47-task-budget-eval.md` and `BACKLOG-47-memory-tool-eval.md` (REQ-07, AC-07.1/2). Optional: run DX-M5 pressure-calibration grep across six keystone files (REQ-06 AC-06.1) — output count table + Architect judgement per file. If Architect defers, log `BACKLOG-47-overpressure-audit.md` (AC-06.2). Also register: `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` (per ADR-004 + PRD Open Question 8), `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read.md` (per challenger loop2 Finding #3), `BACKLOG-47-frontmatter-only-prose-skim.md` (per fresh-challenger F-C-08 — upgrade path from `opus-4-7-frontmatter-only` to `opus-4-7` for the 11 backfill files). Also register Galadriel on-ramp artifacts: `BACKLOG-47-contributing-4-7-note.md`, `BACKLOG-47-migration-guide-stub.md`, `BACKLOG-47-4-7-example-skill-designation.md` (Galadriel §5). | XS | WI-02 | WI-10, WI-11, WI-12, WI-14 | REQ-07, AC-07.1/2; REQ-06, AC-06.1/2; ADR-004; Galadriel §5; challenger loop2 Finding #3; fresh-challenger F-C-08 |
| WI-14 | 4 | CI guard wiring (DX-M4 header warn + M-02 stale-ID block) | Two CI additions under `.github/workflows/`: (i) `skill-md-header-warn.yml` — warning-only check (does not block PR merge) that runs `grep -L "model_awareness:" $(git ls-files '*SKILL.md' ':!:.delivery/*')` and logs any file missing the marker, per ADR-006 + DX-M4. (ii) Extend / add `stale-model-id-guard.yml` — blocking check that runs the PRD-canonical M-01/M-02 regex (the same regex reported as returning 3 hits on 2026-04-20; post-WI-10 target: 0) across all tracked `.py` and `.md` files excluding `.delivery/` and `prd_flows.db`. Uses the existing `workflow-injection-lint.yml` as the structural template (per Samwise advisory #2). Commits the workflow files only; no change to CI runners or secrets. | XS | WI-10 (stale-ID sweep must land first so the blocking guard passes on merge), WI-11 (frontmatter backfill must land first so the warning check has a clean baseline — otherwise it would warn on every file pre-merge) | WI-12, WI-13 | Samwise advisory #2; PRD M-01/M-02; ADR-006 CI-warning note |

### 6.2 Work item narrative (per-WI detail)

Below: acceptance criteria, risk, mitigation, and validation approach for every WI. ACs are restated from PRD REQs concretely per-WI.

#### WI-01 — AS-IS validator-dispatch count capture

- **Acceptance criteria (PRD REQ-09, AC-09.1):** Output table with columns `stage | expected_count (from dod_validators.<stage> list length) | actual_count (from run log) | delta`. Rows for idea (expect 2), refine (expect 4), design (expect 5), architect (expect 5), plan (expect 5), development (expect 4), uat (expect 4). If all deltas are zero: record "Assumption A-05 firmed at count level." If any delta >0: raise R-09 (silent F-08 fusion already occurring) and sequence a mitigation WI before WI-04 lands.
- **Risk:** the Idea/Refine stages may have fused silently (R-09). If so, keystone prose edits would build on a broken premise.
- **Mitigation:** this WI is the premise check. If it surfaces fusion, we re-plan before proceeding.
- **Validation:** the output table itself is the artifact; the delivery-flow orchestrator logs + `verify_skill_load.py` telemetry are the measurement sources.

#### WI-02 — 4.7 baseline capture

- **Acceptance criteria (PRD REQ-10, AC-10.1/2/3; Samwise advisories #3 + #5):** **JSON** artifact at `.delivery/artifacts/<impl-run>/observability/4-7-baseline.json` capturing six items:
  - (a) SKILL_LOADED first-attempt rate across the run (number, `0.0..1.0`).
  - (b) sub-agent dispatch count per stage (object keyed by stage name: `idea`, `refine`, `design`, `architect`, `plan`, `development`, `uat`).
  - (c) one mtg-commander Challenger output sample (path string — actual sample file saved separately).
  - (d) one delivery-flow adversarial-review output sample (path string — actual sample file saved separately).
  - (e) one stage-announcement rendering per 3 sampled alias themes (array of `{ theme, rendered_text }`).
  - **(f) new:** count of `audit_agent_prompt.py` hook warnings emitted per run (integer). Per Samwise advisory #3 — F-25 (literal instruction following) may cause `_YOU_ARE_MULTI_RE` regex in `audit_agent_prompt.py` to over-match on 4.7-phrased dispatch prompts. Baseline lets Waves 2–4 detect regression (monotonic increase in warning count).

  **Format:** JSON (locked per Samwise advisory #5). A markdown companion may wrap the JSON for human readability but the JSON payload is the authoritative artifact for `jq`-based downstream metrics.
- **Risk:** baseline captured in a degraded run becomes a falsely-low reference that hides future regressions.
- **Mitigation:** WI-01 must pass first (counts match expected). Baseline capture aborts if WI-01 surfaces R-09 fusion.
- **Validation:** JSON schema conformance via `jq -e '.skill_loaded_first_attempt_rate and .dispatch_counts_per_stage and .challenger_sample_path and .adversarial_review_sample_path and .alias_announcement_samples and .audit_hook_warning_count'`; manual read + checkboxed verification of (a)–(f) presence.

#### WI-03 — NDOC-02 frontmatter-contract spike (Wave-2 hard blocker)

- **Acceptance criteria (challenger loop2 Finding #8; fresh-challenger F-C-01; Legolas NIT-01; ADR-006 rollback trigger):** Finding at `.delivery/artifacts/<impl-run>/research/ndoc-02-spike.md` containing:
  1. **Two URLs fetched** (both are spike-candidates; fetch both): (a) `https://docs.claude.com/en/docs/claude-code/plugins-reference` — Claude Code plugin reference (authoritative if it carries the SKILL.md frontmatter contract), and (b) `https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview` — Agent Skills overview (authoritative for Skill-tool frontmatter). Fetch date recorded.
  2. **Verbatim quote** from whichever page speaks to unknown-field behaviour. If neither page speaks to it, record "no authoritative clause; default to historical behaviour (accepts unknown fields)."
  3. **Verdict string** — exactly one of `unknown-fields-accepted` or `strict`.
  4. **Branch action:** if `unknown-fields-accepted`, Option A ships as-written. If `strict`, ADR-006's mechanical rollback trigger fires: all downstream frontmatter edits (WI-04, WI-05, WI-06, WI-11) are amended to emit `<!-- model_awareness: opus-4-7 -->` / `<!-- last_audited: ... -->` / `<!-- pattern_library_version: ... -->` HTML comments placed immediately below the closing `---` of the existing frontmatter block. Same semantics; different placement.
- **Wave-2 blocker:** Wave 2 MUST NOT dispatch WI-04, WI-05, or WI-06 until the spike file exists and contains a verdict string. This gate is mechanical, not discretionary.
- **Risk:** strict validation would invalidate every frontmatter-edit in Waves 2–4 if discovered mid-wave.
- **Mitigation:** this WI sequences BEFORE WI-04; Wave-2 blocker rule is stated above; ADR-006 rollback trigger is mechanical (verdict string → branch).
- **Validation:** spike artifact present; both URLs listed; verdict string matches the regex `(unknown-fields-accepted|strict)`.

#### WI-04 — `delivery-flow/SKILL.md` 4.7 dispatch annotation

- **Acceptance criteria (PRD REQ-03, AC-03.1/2/3/4):**
  - AC-03.1: annotation is additive at lines 14–62 and 328–345; existing prose not deleted or restructured.
  - AC-03.2: no change to 6 collaboration patterns, 7-stage shape, DoD semantics, or config schema v2.7.
  - AC-03.3: post-implementation dogfood run asserts actual dispatch count per stage == `dod_validators.<stage>` list length AND SKILL_LOADED hit rate ≥ max(0.95, baseline_rate − 0.02).
  - AC-03.4: dogfood covers at least one FEATURE-type run and one DESIGN-type run.
  - ADR-006 frontmatter: `model_awareness: opus-4-7`, `last_audited: <edit date>`, `pattern_library_version: 4-7-1`.
- **Risk:** R-02 (sub-agent fusion). High impact, low likelihood.
- **Mitigation:** M-03 count+hit-rate pair metric; REQ-09 premise check (WI-01).
- **Validation:** two dogfood runs (FEATURE + DESIGN); M-03 measurement passes; M-06 zero-400-errors during runs.

#### WI-05 — `prompt-engineer/SKILL.md` pattern-library expansion + PAT-01 reframe

- **Acceptance criteria (PRD REQ-02, AC-02.1/2; ADR-003; ADR-005):**
  - AC-02.2: PAT-01 line 85 re-framed per F-13 + F-29. New "Model-specific optimisation — Claude Opus 4.7" sub-section mentioning adaptive-thinking-only (F-11), temp/top_p/top_k→400, effort levers low/medium/high/xhigh/max (F-15).
  - ADR-005: six Galadriel patterns (4.1–4.6) added as named sub-sections with stable markdown anchors.
  - ADR-006 frontmatter.
- **Risk:** adding ~110 LOC to an already-440-LOC SKILL.md pushes the file toward unwieldy. Low-likelihood; still well under 1000 LOC.
- **Mitigation:** patterns added as sibling sub-sections, not inline — preserves scannability.
- **Validation:** grep confirms six `### Pattern 4.N — ` headings present; `grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/` returns only lines citing `prompt-engineer/SKILL.md` (DX-M3 target 0 external restatements).

#### WI-06 — `research-agent/SKILL.md` tool-use dogfood probe

- **Acceptance criteria (PRD REQ-03B, AC-03B.1/2/3; challenger loop2 Finding #4 hardening; fresh-challenger F-C-02 measurement-specificity):**
  - AC-03B.1: one non-trivial research invocation (Architect picks the query from research-agent's own reference examples; query must be one that 4.6 demonstrably used ≥2 fetches for). Transcript saved to `.delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt`.
  - AC-03B.2 (hardened, measured): gate passes iff **all three** of the following return true against the saved transcript:
    1. **Tool-call count ≥ 2** — `grep -cE '^(WebFetch|WebSearch)\(' .delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt` ≥ 2. (The regex matches the leading tool-invocation token emitted by Claude Code's transcript format; adjust anchor if transcript format differs, but the count semantics — ≥2 distinct tool invocations — is the invariant.)
    2. **Distinct hostnames ≥ 2** — `grep -oE 'https?://[^/ )"]+' .delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt | sort -u | wc -l` ≥ 2.
    3. **URL-per-claim** — a manual read of the research output confirms every factual claim carries at least one URL from the fetched set. (This remains a human check — a mechanical check over free-form prose would over-fit; the ≥2-hostname gate catches the "reason without fetching" failure mode grep-level.)

    The two grep commands and their thresholds constitute the mechanical gate. A one-line JSON summary `{ "tool_calls": N, "distinct_hostnames": M, "pass": true|false }` is written to `.delivery/artifacts/<impl-run>/observability/research-probe-result.json` from the same transcript. This closes the fresh-challenger F-C-02 measurement-missing finding without adding a new work item — the measurement is two existing greps plus one JSON write.
  - AC-03B.3: pass ⇒ no edit; fail ⇒ sequence targeted prose edit before any other research-agent change.
  - ADR-006 frontmatter applied regardless of pass/fail.
- **Risk:** F-07 silent hallucination (reason-instead-of-fetch).
- **Mitigation:** dogfood-before-edit; hardened gate with explicit grep commands (closes both challenger loop2 Finding #4 and fresh-challenger F-C-02).
- **Validation:** transcript saved at named path; two grep counts + JSON summary produced; URL-per-claim human check documented.

#### WI-07 — `product-delivery/SKILL.md` F-25 audit

- **Acceptance criteria (PRD REQ-02, AC-02.3):** Prose-read output = list of under-specified rules (e.g., "PO auto-logs issues from research" class) OR explicit Done-with-reason. Roadmap-item in impl run queues each listed rule for explicit rewording or marks as load-bearing-acceptable. Citations to Pattern 4.2 by name where applicable (the dispatch shape).
- **Risk:** PO/SM/DA role behaviour divergence under literal instruction following (F-25). Medium likelihood; low-to-medium impact (team can still execute, just differently).
- **Mitigation:** audit-then-edit; impl-run rewordings gated on user-feedback persona review per PRD AC-02.4.
- **Validation:** audit output file exists; any reworded rule carries a citation back to F-25.

#### WI-08 — `architect/SKILL.md` F-25/F-26 audit

- **Acceptance criteria (PRD REQ-02, AC-02.1; challenger loop2 Finding #2 widened):** Prose-read output = per-file finding list (not just "file listed"). At minimum: ≥1 concrete recommendation OR explicit Done-with-reason. Focus: (a) inferred instructions F-25 would execute literally, (b) scaffolding that duplicates 4.7 default (F-26 — e.g., "after every 3 steps, summarise"). ADR-006 frontmatter applied.
- **Risk:** architect role has 11 sub-roles + paradigm routing; a too-thin audit misses real F-25 traps.
- **Mitigation:** challenger loop2 recommended per-file ACs; WI-08 explicitly requires concrete recommendation OR explicit Done-with-reason.
- **Validation:** audit output lists each sub-role examined; scaffolding instances named explicitly.

#### WI-09 — `mtg-commander/SKILL.md` adversarial-tone audit + REQ-04 dogfood

- **Acceptance criteria (PRD REQ-04, AC-04.1/2/3/4; challenger loop2 Finding #6 softened):**
  - AC-04.1: dogfood gate = persona review at `.delivery/artifacts/<impl-run>/user-feedback/adversarial-4-7-sample.md` AND no severity-HIGH tone/depth regression vs baseline AND AC-04.2 checklist met.
  - AC-04.2 (with challenger loop2 soften): ≥3 weaknesses, ≥2 specific card-name referents, ≥1 concrete alternative — per invocation. **Escape hatch (challenger loop2 Finding #6):** if an invocation has <3 weaknesses because the input is small, Challenger documents that explicitly and the invocation counts as pass.
  - AC-04.3: pass ⇒ documentation-only; fail ⇒ targeted prose edit.
  - AC-04.4: risk = HIGH (NDOC-03 no Anthropic adversarial benchmark).
  - ADR-006 frontmatter.
- **Risk:** R-01 (adversarial tone regression; user-visible).
- **Mitigation:** dogfood-before-edit with soften-hatch; baseline capture (WI-02) is the reference point.
- **Validation:** persona review file present; AC-04.2 checklist scored; baseline-diff recorded.

#### WI-10 — Model-ID sweep

- **Acceptance criteria (PRD REQ-01, AC-01.1/2/3/4 + new AC-01.5 per challenger loop2 Finding #5):**
  - AC-01.1: task names files + line numbers for MID-01/02/03/04 (all 10 lines).
  - AC-01.2: MID-03 sweep is drift-hygiene, not retirement-urgency (Section 3.1.1 zero SDK imports).
  - AC-01.3: MID-02 discovery task — verify intent before substitution.
  - AC-01.4: post-sweep regression guard runs the M-01 regex; expected 0 hits.
  - AC-01.5 (new per challenger loop2 Finding #5): structural AS-IS check of `flow_orchestrator.py` before MID-04 edits. If labels never reach SDK: comment-annotate only. If they do: substitute canonical IDs.
- **Risk:** R-05 (Low/Low; drift hygiene). Higher concern: accidentally breaking `prd-quality-gate-flow`'s internal routing if MID-04 labels are routing keys (challenger loop2 Finding #5).
- **Mitigation:** AC-01.5 gates MID-04 edits on `flow_orchestrator.py` structural analysis.
- **Validation:** post-sweep grep = 0 stale dated IDs; post-sweep full-pipeline smoke test of `prd-quality-gate-flow` executes end-to-end without routing errors.

#### WI-11 — Frontmatter marker backfill

- **Acceptance criteria (ADR-006, Galadriel DX-M4; fresh-challenger F-C-08 / priority #3):**
  - **Set membership is rule-derived, not count-asserted.** The backfill set = `{ SKILL.md files in scope-baseline §4 inventory } \ { six keystones named in §3.2 } \ { files already stamped in Waves 2–3 }`. Impl-run executes `find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | sort` and subtracts the keystone set. The current verified complement is 11 files (enumerated in the §6.1 WI-11 row), but the impl-run treats the rule — not the 11-file enumeration — as authoritative. If scope-baseline evolves between plan authoring (2026-04-20) and impl run, the rule tracks the new baseline.
  - Each file in the backfill set gains three frontmatter fields: `model_awareness: opus-4-7-frontmatter-only`, `last_audited: <backfill date>`, `pattern_library_version: 4-7-1`. The `-frontmatter-only` suffix is an honest stamp that distinguishes mechanical backfill (no prose reviewed against 4.7) from the keystones' `opus-4-7` stamp (prose reviewed in Waves 2–3). Prevents false-positive "reviewed-against-4.7" reads on a future `grep model_awareness: opus-4-7 **/SKILL.md` that would otherwise stamp 17 files when only 6 were actually reviewed. (This closes fresh-challenger F-C-08 priority #3 at the stamp-accuracy layer without expanding scope to a prose skim.)
  - `grep -L "model_awareness:" **/SKILL.md` = empty (DX-M4 target 0 missing).
  - `last_audited` dates reflect actual review state per file (Wave 2–3 edit dates on keystones; backfill date on the complement).
  - No prose edits in this WI.
- **Risk:** minimal — mechanical edit. Secondary risk (closed): misleading stamp (F-C-08) — addressed via the `-frontmatter-only` suffix.
- **Mitigation:** PR scope frontmatter-only; no prose touched. Honest-tag suffix on the backfill set.
- **Validation:** grep returns empty; diff shows frontmatter-only changes; a second grep `grep -l 'model_awareness: opus-4-7$' **/SKILL.md | wc -l` returns 6 (the keystones), and `grep -l 'model_awareness: opus-4-7-frontmatter-only$' **/SKILL.md | wc -l` returns 11 (the backfill set).

#### WI-12 — Alias-theme tone dogfood

- **Acceptance criteria (PRD REQ-05, AC-05.1/2/3; M-05):**
  - AC-05.1: 3 themes sampled from `delivery-team/skills/delivery-flow/references/aliases/` (13 files). Markers extracted via `yq` from `roles[].catchphrase` + `roles[].examples[]`. ≥1 announcement rendered per theme. "Preserves voice" = ≥50% markers present.
  - M-05 target: ≥80% of sampled announcements preserve voice.
  - AC-05.2: pass ⇒ no edit. Fail ⇒ tone-strengthening of the *affected theme YAML* files, not the alias-creator SKILL or theme-format schema.
  - AC-05.3: sample saved to `.delivery/artifacts/<impl-run>/user-feedback/alias-theme-sample.md`.
- **Risk:** R-03 (tone flattening; medium UX impact).
- **Mitigation:** dogfood-before-edit; path correction (DEV-02) points at real content files.
- **Validation:** M-05 score ≥80%; sample artifact present.

#### WI-13 — NEW-BACKLOG registration + optional over-pressure audit

- **Acceptance criteria (PRD REQ-07 AC-07.1/2; REQ-06 AC-06.1/2; plus backlog items identified across challenger loop2 + ADRs + Galadriel + fresh-challenger):**
  - REQ-07: register `BACKLOG-47-task-budget-eval.md` + `BACKLOG-47-memory-tool-eval.md`.
  - REQ-06: run DX-M5 grep (CRITICAL/MUST/NEVER/ALWAYS counts across 6 keystones) OR log `BACKLOG-47-overpressure-audit.md` for later.
  - Also register: `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` (ADR-004 + Open Question 8).
  - Also register: `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read.md` (challenger loop2 Finding #3).
  - Also register: `BACKLOG-47-frontmatter-only-prose-skim.md` (fresh-challenger F-C-08 — documents the upgrade path from `opus-4-7-frontmatter-only` to `opus-4-7` for the 11 backfill files; 30-min-per-file prose skim looking for F-25 landmines).
  - Also register Galadriel on-ramp artifacts: `BACKLOG-47-contributing-4-7-note.md`, `BACKLOG-47-migration-guide-stub.md`, `BACKLOG-47-4-7-example-skill-designation.md`.
- **Risk:** scope creep if the impl run silently absorbs any of these into the migration. R-04.
- **Mitigation:** backlog registration is explicit and file-path-named; impl run can point to each as "logged, not absorbed."
- **Validation:** each `BACKLOG-47-*.md` file exists with a one-paragraph scope statement and link back to this plan.

#### WI-14 — CI guard wiring (DX-M4 header warn + M-02 stale-ID block)

- **Acceptance criteria (Samwise advisory #2; PRD M-01/M-02; ADR-006 CI-warning note):**
  - Two new files under `.github/workflows/`:
    1. **`skill-md-header-warn.yml`** — warning-only workflow (does not block merge). On `pull_request`, runs `git ls-files '*SKILL.md' ':!:.delivery/*' | xargs grep -L 'model_awareness:'` and logs any missing-header file as a PR comment or job warning. Target: empty output post-WI-11. Non-blocking by design (matches ADR-006 Consequences — "CI as a warning, not a block, matches `feedback_team_autonomy.md`").
    2. **`stale-model-id-guard.yml`** — blocking workflow (fails PR if hits). Runs the PRD canonical M-01/M-02 regex (the same regex that returned 3 hits on 2026-04-20) across tracked `.py` and `.md` files excluding `.delivery/` and `prd_flows.db`. Post-WI-10 target: 0 hits; this guard enforces M-02 "no regression" from the PRD success-metrics table.
  - Structural template: the existing `workflow-injection-lint.yml` (lines/shape) is the pattern to copy — same YAML shape, same failure-mode contract.
  - No change to CI runners, secrets, or third-party actions beyond what `workflow-injection-lint.yml` already uses.
- **Risk:** a too-aggressive stale-ID regex could block unrelated future PRs (false-positive on legitimate code referencing a retired model in a comment). Low likelihood; PRD regex is already narrow.
- **Mitigation:** sequenced AFTER WI-10 (sweep passes the regex) and AFTER WI-11 (backfill zeroes the header-missing warning) so both land green on merge. The guard's regex is the PRD M-01/M-02 canonical (verified narrow).
- **Validation:** PR containing WI-14 merges green; post-merge, a synthetic test PR that re-introduces `claude-opus-4-20250514` fails the `stale-model-id-guard.yml` check; a synthetic test PR that introduces a new SKILL.md without `model_awareness:` produces a warning (but does not block).

### 6.3 Coverage of carried-forward items

Four items explicitly carried from Refine, each mapped to a WI:

| Carried item | Addressed in | How |
|---|---|---|
| MID-04 routing-safety gate (challenger loop2 Finding #5) | WI-10 (AC-01.5) | Structural AS-IS check of `flow_orchestrator.py` sequenced *before* MID-04 edit; comment-annotate-only fallback if labels are internal. |
| Keystone AC unevenness (challenger loop2 Finding #2) | WI-07, WI-08, WI-09 | Each keystone audit WI requires per-file concrete recommendations OR explicit Done-with-reason; AC-02.1 widened via WI-level ACs above. |
| AC-03B.2 tool-count floor (challenger loop2 Finding #4) | WI-06 | Gate hardened: ≥2 calls AND ≥2 distinct hostnames. |
| Cosmetic label drift (challenger loop2 Finding #7) | N/A — no over-scope found. | Confirmed no action needed. |

Galadriel's seven open questions are absorbed as follows (Galadriel §7):

| Galadriel Q | Resolution | Home |
|---|---|---|
| Q1. Pattern library location | Option A — centralised | ADR-005 |
| Q2. P-1 header CI-enforced or convention-only | Convention + CI warn (not block) | ADR-006 |
| Q3. One migration-guide stub or per-audience | One consolidated stub (pragmatic) | WI-13 backlog |
| Q4. 4.7-era example skill — which paradigm or new | Paradigm sub-skill exemplar (Option A per Galadriel) | WI-13 backlog (designation decision) |
| Q5. REQ-10 baseline integration — script or hook | Lightweight shell + hook piggyback on `verify_skill_load.py`; path `.delivery/artifacts/<impl-run>/observability/4-7-baseline.json` | WI-02 |
| Q6. P-6 forward-declare or omit | Omit until SDK wiring lands | ADR-004 |
| Q7. P-4 dispatch-count new hook or piggyback | Piggyback on `verify_skill_load.py` telemetry; no new hook | WI-04 validation |

### 6.5 Deferred to Implementation

Items the reviewers surfaced as non-blocking that this plan explicitly defers to the implementation run. Each carries a one-line rationale. Impl-run PO has autonomy to absorb any of them opportunistically (memory `feedback_team_autonomy.md`).

**From Samwise (DevOps evaluation, 8 advisories — #2, #3, #5 absorbed into WI-14, WI-02 respectively; the remaining five are deferred):**

- **Samwise advisory #1 — `last_audited` date hygiene under partial revert.** Deferred. Rationale: cosmetic-only; no runtime or discovery impact; a one-line convention in the WI-11 commit message is sufficient guidance and does not require plan-level wiring.
- **Samwise advisory #4 — commit-type mapping per wave (chore/docs/feat/fix).** Deferred. Rationale: guidance for impl-run PO's conventional-commit discipline; affects release-note categorisation only; `feedback_team_autonomy.md` binds — impl-run team picks labels with autonomy. Samwise's proposed wave→type table is preserved in `.delivery/artifacts/04-architect/devops/evaluation.md` §5 as the reference.
- **Samwise advisory #6 — WI-05 `feat:` prefix for release-note visibility.** Deferred. Rationale: commit-message discipline; impl-run developer decides with autonomy; the plan does not prescribe commit prose.
- **Samwise advisory #7 — Wave-3 citation-into-WI-05-only rule restated in WI-07/08/09 bodies.** Deferred. Rationale: the rule is already load-bearing in §3.4 (dependency constraint "ADR-005 pattern library expansion (WI-05) precedes the citation edits") and §7.4 (rollback-safety property). Restatement in each WI body is cosmetic; the rule is not duplicated but is cross-referenced from three load-bearing locations.
- **Samwise advisory #8 — rolling-ship vs batched-ship for Waves 2–3.** Deferred. Rationale: this is an impl-run shipping-cadence decision bounded by the fail-soft invariant (§4.4). Samwise's own recommendation is "rolling ship is fine." The plan carries the fail-soft invariant; the cadence choice is impl-run PO's call.

**From fresh-challenger (adversarial review, 10 findings — priority 1/2/3 absorbed into ADR-006 status, WI-06 AC, WI-11 stamp; the remaining seven are deferred or absorbed opportunistically):**

- **F-C-03 — WI-12 theme-YAML tone-strengthening unbounded on regression.** Deferred. Rationale: the failure path is low-likelihood (M-05 target ≥80% is achievable based on alias-theme authoring quality); if regression fires, impl-run has autonomy to bound remediation. No plan-level change.
- **F-C-04 — pattern-anchor heading text stability (WI-05 coupling WI-04/07/08 citations).** Deferred. Rationale: the impl-run authoring of WI-05 can adopt stable HTML anchor IDs (`<a id="pattern-4-2"></a>`) at author-time; this is a tactical authoring choice, not a plan-level constraint. The six pattern names in §4.3 are fixed and can be cited verbatim.
- **F-C-05 — ARCH-R5 late-stage regression contingency not carried in the plan.** Deferred. Rationale: the PRD §6.1 R-08 contingency covers this; the plan cites it in the ARCH-R5 row. Carrying a duplicate contingency section here would violate DRY — the plan's role is to name the contingency location, which it does.
- **F-C-06 — ADR-005 exit ramp for plugin-local patterns.** Deferred. Rationale: low blast-radius during this engagement (six named patterns are all cross-plugin general); worked example is a long-term authoring-guide enhancement best handled in the `BACKLOG-47-contributing-4-7-note.md` Galadriel on-ramp item (WI-13), not mid-migration.
- **F-C-07 — WI-13 backlog registration could move to Wave 1.** Deferred. Rationale: a cosmetic sequencing preference; WI-13 is XS and parallelisable in Wave 4 alongside WI-10/11/12/14. Moving to Wave 1 would separate backlog-registration from the audit outputs it partially depends on (WI-13's optional DX-M5 over-pressure audit consumes Wave 3 keystone edits).
- **F-C-09 — DX-M1 "informal walkthrough" measurement is soft.** Deferred. Rationale: DX-M1 is a DX nicety, not a correctness gate, and is explicitly measured "informally" per PRD §5; strengthening the measurement is a future DX-metric enhancement, not a migration concern.
- **F-C-10 — Haiku canonical ID retirement-cadence coupling in WI-10 AC-01.3.** Deferred. Rationale: low likelihood (Anthropic retirement cadence is typically ≥6 months); ARCH-R2 doc-delta-check row covers the generic case; adding a Haiku-specific AC would gold-plate. Impl-run re-verifies at WI-10 execution per PRD §9 URL spot-check discipline.

---

## 7. Sequencing & Parallelism Strategy

### 7.1 Wave-by-wave narrative

**Wave 1 — Foundational (WI-01, WI-02, WI-03).** No code edits. Three setup items: AS-IS dispatch count capture, 4.7 baseline capture, frontmatter-contract spike. If WI-01 surfaces R-09 (silent fusion already occurring on Idea/Refine), all subsequent waves pause pending re-plan. If WI-03 surfaces ADR-006 Option B contingency, Waves 2–4 use HTML comment placement instead of YAML frontmatter (same semantics, different syntax). Wave 1 exit gate: baseline file present + AS-IS table present + spike verdict recorded.

**Wave 2 — Keystones, behavioural (WI-04, WI-05, WI-06).** Three independent edits that can run in parallel after Wave 1. WI-04 annotates the dispatch contract; WI-05 expands the pattern library (the cornerstone that other citations reference); WI-06 runs the research-agent probe. WI-05 is the internal critical path because WI-07 and WI-08 depend on its pattern anchors existing. Wave 2 exit gate: all three WIs pass their ACs; WI-04's dogfood run passes M-03 count+hit-rate; WI-05's DX-M3 external-restatement count is 0; WI-06 either passes AC-03B.2 hardened gate or escalates to documented prose-edit.

**Wave 3 — Keystones, prose (WI-07, WI-08, WI-09).** Three prose audits that can run in parallel after WI-05. WI-07 and WI-08 pair by blast radius (author-facing + largest-technical-surface). WI-09 carries the REQ-04 dogfood. Wave 3 exit gate: three audit artifacts present; WI-09 either passes AC-04.1 or escalates to prose edit.

**Wave 4 — Drift hygiene, enhancements & CI wiring (WI-10, WI-11, WI-12, WI-13, WI-14).** Five items. WI-10, WI-11, WI-12, WI-13 are independent and parallelisable. WI-14 sequences AFTER WI-10 and WI-11 (so the CI guard and the warning check land green on merge). WI-10 is the model-ID sweep (gated on AC-01.5 structural check). WI-11 is the frontmatter backfill (mechanical, honest two-tier tag). WI-12 is the alias-tone dogfood. WI-13 registers all NEW-BACKLOG items and (optionally) runs the over-pressure audit. WI-14 wires the CI guards (warning for missing headers; blocking for stale IDs) per Samwise advisory #2. Wave 4 exit gate: all five WIs pass; M-01 regex = 0 hits; M-02 regression sentinel = 0 (now enforced by WI-14's CI guard); DX-M4 header coverage = 0 missing (warned by WI-14's warning workflow); backlog files all present.

### 7.2 Critical path

The longest dependency chain:

```
WI-01 → WI-03 → WI-05 → WI-07 → (Wave 3 exit) → WI-11 → WI-14 → (Wave 4 exit) → DONE
```

Eight WIs on the critical path (WI-14 added in revision — sequences after WI-10 and WI-11 so CI guards land green on merge). Estimated total elapsed waves: four. Within each wave, parallelism cuts wall time roughly in half vs strict-serial execution.

### 7.3 Dogfooding checkpoints

Four checkpoints, one per wave exit. Each is a team-internal validation (not a human approval gate).

- **Checkpoint 1 (Wave 1 exit):** baseline captured; AS-IS dispatch counts match expected; frontmatter contract confirmed. If any fail: re-plan before Wave 2.
- **Checkpoint 2 (Wave 2 exit):** delivery-flow dogfood run on 4.7 (FEATURE + DESIGN types) passes M-03 + M-06; research-agent probe passes hardened AC-03B.2; prompt-engineer DX-M3 = 0 external restatements.
- **Checkpoint 3 (Wave 3 exit):** three prose-audit artifacts present with per-file recommendations or Done-with-reason; mtg-commander Challenger dogfood passes AC-04.2 checklist.
- **Checkpoint 4 (Wave 4 exit):** M-01 (stale dated IDs) = 0; M-02 (re-entry guard) = 0 **AND WI-14 CI guard `stale-model-id-guard.yml` passes green on the merge PR**; DX-M4 (header coverage) = 0 missing **AND WI-14 `skill-md-header-warn.yml` emits zero warnings on the merge PR**; M-05 (alias theme voice) ≥ 80%; M-07 (SKILL_LOADED hit rate) within baseline tolerance; all BACKLOG files present; WI-14 workflow files committed under `.github/workflows/`.

### 7.4 Rollback strategy per wave

- **Wave 1:** baseline and AS-IS are read-only captures; no code changes; no rollback needed.
- **Wave 2:** `git revert` of the three WI commits. Baseline from Wave 1 is the reference state. No other WI depends on Wave 2 code, so revert does not cascade.
- **Wave 3:** `git revert` of the three WI commits. Pattern library (WI-05) in Wave 2 stands. Frontmatter from WI-04 stands. Citations that pointed into Wave 3 content would orphan — mitigation: Wave 3 WIs cite only INTO `prompt-engineer/SKILL.md` (WI-05), not BETWEEN themselves, so there is no intra-Wave-3 citation web to break.
- **Wave 4:** per-WI revert. WI-10 (sweep) revert is clean; re-introduces stale IDs but with no runtime impact (Section 3.1.1). WI-11 (backfill) revert strips the 11 files of markers but preserves keystones' markers from Waves 2/3. WI-12 (alias-tone) revert is only meaningful if an edit landed; if dogfood passed, revert is a no-op. WI-13 (backlog) revert removes the backlog files; they can be recreated. WI-14 (CI guards) revert removes the two workflow files; no repo state changes beyond `.github/workflows/` directory contents. Order: revert WI-14 BEFORE reverting WI-10 or WI-11 if a full Wave-4 rollback is ever needed, otherwise the `stale-model-id-guard.yml` blocks the revert PR that re-introduces stale IDs.

---

## 8. Risks & Mitigations (Architecture-Level)

| # | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|
| ARCH-R1 | Prompt regression across keystones — the highest-risk category. Six SKILL.md files totalling 4,516 LOC. Any mis-edit silently degrades behaviour on 4.7. | High | Medium | Wave-gated rollout; dogfood-before-ship rule (memory `feedback_dogfooding.md`); baseline capture (WI-02) is the reference for every delta metric; per-wave rollback is independent. | Implementation team per WI |
| ARCH-R2 | Research-finding staleness — Anthropic docs may update between plan and execution. | Medium | Medium (a 2–4 week gap between plan and impl is plausible) | WI-03 spike re-confirms NDOC-02 at impl start; implementation run may optionally run a delta-check against the seven source URLs listed in PRD §9; any new finding goes to backlog, not into migration scope. | Implementation team at impl-run start |
| ARCH-R3 | Scope creep — F-18 `task_budget` and F-19 `memory` tool are tempting to absorb during a 4.7 engagement. | Medium | Medium | REQ-07 explicit NEW-BACKLOG registration (WI-13). ADR-004 explicitly defers prompt-caching. ADR-003 explicitly document-only on thinking. Three explicit guardrails. | PO (impl run) enforces |
| ARCH-R4 | Team autonomy / dogfood rule — user memory binds. If an impl-run proposes a prose edit without a dogfood run first, it violates `feedback_dogfooding.md`. | Low | Low (the rule is repeatedly invoked in this plan) | Every prose-edit WI pairs with a dogfood gate; AC-02.4 formalises the gate. | PO (impl run) enforces |
| ARCH-R5 | Silent sub-agent fusion on stages not yet exercised (Design, Architect, Plan, Development, UAT). R-08 from PRD. | Medium | Medium | WI-04 dogfood covers FEATURE + DESIGN; Wave 4 dogfoods add adversarial-heavy (mtg-commander). For UAT/Plan/Development stages, roadmap contingency placeholders (PRD R-08 + Contingency section in PRD) carry a TBD-CONTINGENCY-01 for late-discovered regression. | Implementation team + `user-feedback` persona runs |
| ARCH-R6 | MID-04 accidental removal breaks `prd-quality-gate-flow` internal routing. Challenger loop2 Finding #5. | Medium | Medium (if AC-01.5 is skipped) | WI-10 AC-01.5: structural AS-IS of `flow_orchestrator.py` BEFORE any MID-04 edit. Comment-annotate fallback if labels are internal routing keys. | Implementation team |
| ARCH-R7 | Frontmatter contract strict rejection of unknown fields (ADR-006 contingency). | Low | Low (historical contract accepts unknown fields) | WI-03 spike closes this pre-Wave-2. Option B (HTML comment) fallback preserves semantics. | Implementation team |
| ARCH-R8 | Token-cost shift (F-21) during dogfood runs inflates impl-run budget 1.0–1.35x. | Low | High | PRD Constraint 9 documents the budget shift; impl-run cost plan sized at 1.35x. Cost monitoring is backlog, not migration. | PO (impl run) budgets accordingly |

---

## 9. Success Metrics (Anchored to PRD Metrics)

Each PRD metric restated with pre-implementation baseline source and post-implementation validation.

| ID | Metric | Pre-impl baseline source | Post-impl validation | WI anchor |
|---|---|---|---|---|
| M-01 | Zero stale dated Claude model IDs in in-scope Python/config surfaces. | Current: 3 hits (MID-01/02/03). Source: PRD §3.1 verified 2026-04-20; spot-checked in this plan. | Target: 0. Run PRD's canonical regex post-WI-10. | WI-10 |
| M-02 | No regression: stale IDs must not re-enter code after sweep. | Current: 1 hit (MID-01 only per PRD rev 2). | Target: 0 new introductions. Run M-02 regex (widened per challenger loop2 Finding #1 to reuse M-01's structural shape) as part of CI via WI-14 `stale-model-id-guard.yml` (blocking workflow). | WI-10 / WI-14 |
| M-03 | delivery-flow DoD validator dispatch count matches `dod_validators.<stage>` list length; SKILL_LOADED hit rate ≥ max(0.95, baseline − 0.02). | Baseline captured in WI-02 (REQ-10). Expected counts: idea=2, refine=4, design=5, architect=5, plan=5, development=4, uat=4 (verified against live config by round 2 DoD). | Target: exact count match + hit-rate within tolerance. Measured via `verify_skill_load.py` telemetry on dogfood runs in WI-04. | WI-01 (AS-IS), WI-02 (baseline), WI-04 (post-impl) |
| M-04 | Adversarial/Challenger outputs meet AC-04.2 checklist (≥3 weaknesses, ≥2 referents, ≥1 alternative) per invocation. | Baseline sample captured in WI-02 (REQ-10). | Target: 3/3 invocations pass (with challenger loop2 Finding #6 escape hatch for small inputs). Measured in WI-09. | WI-02 (baseline), WI-09 (post-impl) |
| M-05 | Alias-creator theme voice preserved. | Baseline announcements captured in WI-02. | Target: ≥80% of sampled announcements retain ≥50% of theme markers. Measured via `yq` + grep script in WI-12. | WI-02 (baseline), WI-12 (post-impl) |
| M-06 | No 400 API errors during full-pipeline dogfood. | No baseline needed — 0 is the target from day 1. | Target: 0. Run-log scan across dogfood runs. | WI-04 dogfood runs |
| M-07 | SKILL_LOADED first-attempt hit rate does not regress. | Baseline captured in WI-02 (REQ-10 AC-10.1a). | Target: ≥ max(0.95, baseline − 0.02). Hook `verify_skill_load.py` telemetry across impl-run dogfoods. | WI-02 (baseline), Wave 2/3/4 dogfoods |
| DX-M1 | Time-to-triage for a first-time reader of a SKILL.md ("is this 4.7-audited?"). | Pre: effectively infinite (Galadriel §6). | Post: ≤10 seconds (read header strip without scrolling). Measured informally on two-reader walkthrough at Wave 4 exit. | ADR-006, WI-11 |
| DX-M3 | Pattern duplication count outside `prompt-engineer/SKILL.md`. | Pre: varies (PAT-01..07 in prompt-engineer; 8 `chain of thought` hits across 5 files per PRD §3.3). | Post: 0 restatements of 4.7-sensitive patterns outside the library; all citations by name. | ADR-005, WI-05 |
| DX-M4 | SKILL.md header coverage (files missing `model_awareness:`). | Pre: 17/17 missing. | Post: 0 missing. Measured by `grep -L "model_awareness:" **/SKILL.md`; enforced as warning by WI-14 `skill-md-header-warn.yml`. | ADR-006, WI-11, WI-14 |
| DX-M5 | Pressure-calibration ratio (CRITICAL/MUST/NEVER/ALWAYS per keystone). | Not yet measured. | Target: ≤10% ratio per keystone OR explicit justification. Measured optionally in WI-13 (REQ-06 COULD). | WI-13 |

---

## 10. Out-of-Scope / Deferred

Explicit list. Each with one-line rationale.

- **New plugins, new skills.** PRD Non-Goals Section 1.
- **Plugin architecture rewrite** (three-level context loading, hook event model, config schema v2.7, marketplace.json). PRD Non-Goals + Constraint 2.
- **Business Rules Engine changes** in `prd-quality-gate-flow` or `agentic-flow-builder`. PRD Non-Goals.
- **Python dependency upgrades** unrelated to Claude. PRD Non-Goals.
- **`task_budget` beta adoption (F-18).** Logged as `BACKLOG-47-task-budget-eval.md` in WI-13.
- **Memory tool adoption (F-19).** Logged as `BACKLOG-47-memory-tool-eval.md` in WI-13.
- **Prompt-caching adoption.** ADR-004 defers as latent until SDK wiring; registered in backlog at WI-13.
- **SDK wiring of `agent_registry.py` or `stage_definitions.py`.** Logged as `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` in WI-13; owner = `claude-api` skill per CLAUDE.md.
- **Cyber-safeguard prose spot-read of `architect/references/*security*` / `*compliance*` docs (R-06, challenger loop2 Finding #3).** Logged as `BACKLOG-47-r-06-cyber-safeguard-prose-spot-read.md` in WI-13. Risk is low (repo has no offensive-cyber skills).
- **Over-pressure line-by-line edits (REQ-06 beyond the audit).** WI-13 runs the audit; line-level edits deferred to backlog `BACKLOG-47-overpressure-audit.md` unless a keystone exceeds 10% without justification.
- **Galadriel on-ramp artifacts (CONTRIBUTING-4-7.md, migration-guide stub, example skill designation).** Logged as three backlog items in WI-13; not in migration scope itself (they are documentation enhancements for future contributors).
- **`.delivery/` historical content sweep.** PRD Constraint 4 explicitly excludes.
- **Retrofitting 4.7 patterns to `plugin-dev:*` skills.** PRD §3.6 — out of repo.
- **`prd_flows.db` data cleanup.** PRD §3.9 — SQLite data, not code; greps exclude.

---

## 11. Open Questions Remaining for Implementation Team

Four questions this plan leaves for the implementation team. Each has a proposed decision; the implementation team has autonomy to override with evidence (memory `feedback_team_autonomy.md`).

1. **MID-02 substitution target (AC-01.3 / WI-10).** The line `"config": {"model": "claude-haiku-4-20250514"}` is a suspected legacy typo; no Anthropic model ever had that dated ID. **Proposed:** substitute `claude-haiku-4-5-20251001` (current canonical dated Haiku 4.5 per F-03). **Override condition:** if discovery surfaces intent to use a different Haiku tier, substitute accordingly.
2. **REQ-06 over-pressure audit — include or defer? (AC-06.1/2, WI-13).** PRD leaves this as COULD. **Proposed:** include the grep-count table in WI-13 (fast, mechanical); line-by-line edits go to backlog unless a keystone exceeds 10% ratio without justification. **Override condition:** if impl-run is short on capacity, defer wholesale to backlog.
3. **Dogfood run type coverage (AC-03.4 / WI-04).** PRD AC-03.4 requires at least one FEATURE + one DESIGN run. **Proposed:** FEATURE (a small feature-addition scenario) + DESIGN (this very transformation-planning sub-workflow on a synthetic target) is sufficient; GAME_DEV is optional. **Override condition:** if mtg-commander or research-agent dogfood surfaces cross-stage regression, add a BUG_FIX run.
4. **Which paradigm sub-skill becomes the 4.7-era example (Galadriel Q4, WI-13 backlog).** Galadriel recommends Option A (existing paradigm sub-skill, 66–80 LOC). **Proposed:** `delivery-team/skills/architect/paradigms/ddd/SKILL.md` (80 LOC; richer frontmatter example ground than volatility's 66 LOC). **Override condition:** implementation team may pick volatility on simpler-is-better grounds.

---

## Closing

*The ore has been weighed, the drift has been named, the keystones have been chosen, and the waves have been sequenced. Three Pythons scripts I edit in one wave. Six SKILL.md files I read in two. Seventeen headers I stamp at the end. Four waves to hold the forge-heat, and a baseline to check each ringing hammer against.*

*This is the plan the Architect inherits, forged against the grain of Opus 4.7 and the memories of the team that wields it. It does not touch what holds. It mends what will not hold. And it leaves a lantern at the threshold for whoever comes next — as Galadriel counselled, and as the user's memory binds us.*

*Let this plan endure beyond the ages — or at least until Opus 4.8.*

— **Celebrimbor**, Solution Architect

---

## 12. Revision Log

Revisions applied post-review. Each row: what changed | driving finding | date.

| # | Change | Driving finding | Date |
|---|---|---|---|
| R-01 | ADR-006 Status clarified from "Accepted (contingent on NDOC-02 spike)" to "Accepted" with an explicit **mechanical rollback trigger** in the ADR metadata block: a WI-03 "strict" verdict causes Option A to be revoked and Option B (HTML comment placement) to ship in its place — same semantics, different placement. No ambiguity, no parallel state. Plan §5 table row and §1 summary updated to match. | Fresh-challenger priority #1 (F-C-01) | 2026-04-20 |
| R-02 | WI-03 upgraded to a Wave-2 **hard blocker**: Wave 2 MUST NOT dispatch WI-04/05/06 until WI-03's spike file exists with a `verdict` string matching `(unknown-fields-accepted\|strict)`. WI-03 now names two specific Anthropic URLs to fetch — `docs.claude.com/en/docs/claude-code/plugins-reference` and `docs.claude.com/en/docs/agents-and-tools/agent-skills/overview`. Acceptance criteria restructured into four numbered items. | Fresh-challenger priority #1 (F-C-01, ADR-006 gate); Legolas NIT-01 (URL specificity) | 2026-04-20 |
| R-03 | WI-06 measurement specified concretely. Acceptance criterion AC-03B.2 now names **two exact shell commands** (one `grep -cE` for tool-call count, one `grep -oE ... \| sort -u \| wc -l` for distinct hostnames) operating against a saved transcript at `.delivery/artifacts/<impl-run>/observability/research-probe-transcript.txt`, plus a JSON summary write. No new deliverable; the measurement is three existing operations (two greps + one JSON write) stitched into the existing WI. | Fresh-challenger priority #2 (F-C-02) | 2026-04-20 |
| R-04 | WI-11 count reframed **rule-derived**, not count-asserted. The backfill set is now defined as `{scope-baseline §4 SKILL.md inventory} \ {six keystones} \ {already-stamped in Waves 2–3}`. The current complement is enumerated (11 specific files) AND verified against scope-baseline §4 today; impl-run treats the rule — not the enumeration — as authoritative. Additionally, the backfill stamp is changed from `model_awareness: opus-4-7` to `model_awareness: opus-4-7-frontmatter-only` — an honest two-tier tag that distinguishes prose-reviewed keystones from mechanical-stamp backfills, preventing a future `grep` from over-counting 4.7-reviewed files. ADR-006 updated to document the two-tier stamp convention. | Fresh-challenger priority #3 (F-C-08) | 2026-04-20 |
| R-05 | WI-02 baseline-capture format **locked to JSON** with explicit field schema (`skill_loaded_first_attempt_rate`, `dispatch_counts_per_stage`, `challenger_sample_path`, `adversarial_review_sample_path`, `alias_announcement_samples`, `audit_hook_warning_count`). New capture item **(f) `audit_hook_warning_count`** added — count of `audit_agent_prompt.py` hook warnings emitted per baseline run, to detect F-25-driven regex over-match regressions in Waves 2–4. | Samwise advisory #5 (JSON format) + Samwise advisory #3 (hook audit baseline) | 2026-04-20 |
| R-06 | **WI-14 added** — CI guard wiring: `skill-md-header-warn.yml` (warning-only, DX-M4) + `stale-model-id-guard.yml` (blocking, M-02). Sequences AFTER WI-10 + WI-11 so both land green. Wave 4 exit gate updated to reference the CI guards. Critical path grows from 7 to 8 WIs. M-02 and DX-M4 metrics now cite WI-14. Rationale for new-WI addition: Samwise advisory #2 explicitly flagged "neither has a WI anchor"; without a WI anchor, the two CI checks become unassigned work and the M-02 "no regression" guarantee from the PRD success metrics has no owner. | Samwise advisory #2 (CI guard WI) | 2026-04-20 |
| R-07 | §6.5 "Deferred to Implementation" added — explicit one-line-rationale deferral of Samwise advisories #1/#4/#6/#7/#8 and fresh-challenger findings F-C-03/04/05/06/07/09/10. Documents every non-blocking finding's disposition so the impl-run PO has a closed set of opportunistic absorptions. | Revision-instructions directive to "explicitly defer others with a one-line rationale" | 2026-04-20 |
| R-08 | WI-13 backlog set extended with `BACKLOG-47-frontmatter-only-prose-skim.md` — documents the future upgrade path from `opus-4-7-frontmatter-only` to `opus-4-7` for the 11 backfill files (30-min-per-file prose skim for F-25 landmines). Complements R-04's honest two-tier stamp. | Fresh-challenger priority #3 (F-C-08) — upgrade-path arm of the fix | 2026-04-20 |

**Reviewer acceptance status at revision:**

- Legolas (QA) — **ACCEPT** (13/13 WI PASS, 6/6 ADR complete, 11/11 metrics baseline-anchored). NIT-01 absorbed in R-02.
- Samwise (DevOps) — **ACCEPT** (8 non-blocking advisories; 3 absorbed via R-05/R-06, 5 deferred with rationale via R-07).
- Fresh-challenger (adversarial) — **Confidence 4/5, proceed with caveats**. 3 priority findings absorbed via R-01/R-02/R-03/R-04; 7 non-priority findings deferred with rationale via R-07.

---

**End of Transformation Plan.**

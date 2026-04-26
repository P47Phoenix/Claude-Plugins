# Skill-Author DX Design — Claude-Plugins 4.7 Migration

**Artifact**: Skill-Author DX Design (Galadriel / UX Designer)
**Stage**: 3 / Design (LIGHT mode — DX surface, not UI)
**Date**: 2026-04-20
**Upstream**: `.delivery/artifacts/01-idea/po/idea-brief.md`; `.delivery/artifacts/02-refine/po/prd.md` (rev 1); `.delivery/artifacts/02-refine/data/scope-baseline.md`
**Alias**: Galadriel — *"Instead of a dark UI, you would have a design beautiful and terrible as the dawn."*

---

> *"I know what you saw in the mirror of user research. The world has changed — I feel it in the user flows. This is not a UI to draw, but a garden that skill-authors must be able to tend without a map made of every stone."*

This document is DX guidance for the people who *author* and *operate* the skills in this repo — not a UI design. There is no UI surface. The "users" here are the skill-author (repo maintainer / contributor editing SKILL.md), the skill-operator (Claude Code invoking a skill), and the plugin-integrator (a marketplace consumer). The Architect inherits these DX constraints to anchor the TO-BE and Roadmap against.

Every claim below is anchored to a PRD finding (F-*) or inventory line (MID-*/PAT-*/DISP-*/SZ-*) from `.delivery/artifacts/02-refine/po/prd.md` rev 1.

---

## 1. Personas

### 1.1 Skill-Author (Primary)

The repo maintainer or contributor editing a `SKILL.md`, a hook script, or a `references/*.md`. Today: Michael Connelly + future contributors (Idea brief §3).

- **Goals.** (a) Land a prose edit that a reviewer can vet by reading. (b) Not accidentally break another plugin while editing one. (c) Know, at read-time, whether a given SKILL is 4.7-aware or still 4.6-shaped.
- **Pain points today.** (i) No grep-level signal of 4.7-awareness — PRD Section 3.3 shows `extended_thinking`/`cache_control`/`tool_choice`/`xhigh` return zero matches across the repo, so a 4.7-aware file and a 4.7-naive file are **textually indistinguishable**. (ii) Six keystone files (PRD §3.7) range 440–1181 LOC each with no shared structural landmarks a scanner can key off of. (iii) PAT-01 in `prompt-engineer/SKILL.md` (line 85) teaches a 4.6-shape mental model of `<thinking>` tags and the author has no way to know it is stale without re-reading the migration guide.
- **What "good" looks like post-4.7.** A new SKILL.md opens with a scannable header strip (model-awareness, last-audited-against, prompt-pattern versions) that answers "is this file migrated?" in under 10 seconds without reading the body. Edits to one keystone don't require reading the other five. The `prompt-engineer/` pattern library is the single source for 4.7-era patterns; every other skill cites *by pattern name*, not by copy-paste.

### 1.2 Skill-Operator (Secondary)

The Claude Code user (or the delivery-flow orchestrator on their behalf) invoking a skill at runtime on Opus 4.7.

- **Goals.** Get the same-or-better behaviour from a skill on 4.7 as on 4.6.
- **Pain points today.** Silent behavioural drift: F-07 ("fewer tool calls by default") can turn a research-agent invocation into reasoning-instead-of-fetching (PRD REQ-03B); F-08 can fuse sub-agent DoD validators (PRD R-02, R-09); F-27 flattens alias-theme voice (PRD R-03). None of these surface as errors — the skill "works", just differently.
- **What "good" looks like post-4.7.** Observable signals: `SKILL_LOADED` hit rate stays ≥ `max(0.95, baseline − 0.02)` (PRD M-07); validator dispatch count matches `dod_validators.<stage>` length (PRD M-03); adversarial output meets the AC-04.2 concrete checklist. The operator never has to ask "did 4.7 change something?" — the hooks and metrics answer that.

### 1.3 Plugin-Integrator (Tertiary)

A downstream marketplace consumer who installs one of the six plugins and reads/copies/forks its content.

- **Goals.** (a) Understand at a glance what model/era the plugin targets. (b) Copy a model-ID from a registry and trust it's current (MID-01..03 in `agentic-flow-builder/scripts/agent_registry.py` is the documented foot-gun — PRD §3.1.1).
- **Pain points today.** Zero forward-compatibility signal in any SKILL.md; dated IDs in `agent_registry.py` are a copy-paste foot-gun for anyone wiring these to the Anthropic SDK (PRD R-05 rationale).
- **What "good" looks like post-4.7.** A convention the integrator can trust: "every SKILL.md in this repo declares its 4.7-awareness in the header. Every model-ID string in scripts is either current or annotated as `# retired YYYY-MM-DD; see <ADR/backlog>`."

---

## 2. DX Pillars for the 4.7 Era

Five concrete DX properties every 4.7-era SKILL.md and agent prompt in this repo should exhibit. Each names *why it matters for 4.7*, and names *an observable signal a reviewer can check without running the skill*.

### P-1 — Forward-Compatibility Header Strip

- **What.** A conventional, machine-readable block near the top of every SKILL.md declaring: `model_awareness: "opus-4-7"`, `last_audited: 2026-MM-DD`, `pattern_library_version: "4-7-<N>"`. Lives in the existing YAML frontmatter (all 17 SKILL.md files already have 5–11 frontmatter lines per PRD §3.7 / scope-baseline §4).
- **Why 4.7.** F-25 (literal instruction following) raises the cost of a silently-stale skill because 4.7 executes the prose *more faithfully*. A 4.6-shape instruction that "usually works" on 4.6 can mis-execute on 4.7. The header strip lets a reviewer triage at a glance whether a file has been examined against 4.7 at all.
- **Observable signal.** `grep -L "model_awareness:" **/SKILL.md` returns empty. A simple CI check can enforce this cheaply, matching the repo's existing `workflow-injection-lint.yml` pattern (CLAUDE.md §CI regression guards).

### P-2 — Pattern-Library Singleton for 4.7-Sensitive Techniques

- **What.** Every 4.7-sensitive prompt pattern (adaptive thinking framing, `<thinking>` tags as *manual CoT fallback* rather than reasoning visibility, effort-lever guidance, "do-not-over-press" voicing) lives in exactly one place: `prompt-engineer/SKILL.md` (PRD SZ-08, keystone). Other skills *cite* the pattern by name; they never restate it.
- **Why 4.7.** PAT-01 (PRD §3.3) shows a specific mis-framing of `<thinking>` tags that is already duplicated conceptually across other files (PAT-02, PAT-06). When F-13 (thinking content omitted by default on 4.7) invalidates the framing, a singleton is edited once; a scattered pattern is edited N times and the N-th miss is a silent regression.
- **Observable signal.** `grep -rn '<thinking>' delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/` returns empty or returns only lines that also contain a citation to `prompt-engineer/SKILL.md#<pattern-name>`.

### P-3 — Fail-Soft on Older / Different Models

- **What.** A SKILL.md should degrade, not fail, if invoked by a caller running a non-4.7 model. Concretely: 4.7-specific features (adaptive thinking, `xhigh` effort, `task_budget`) are referenced as *opportunities for 4.7 callers*, not *required for the skill to work*. The skill's core instructions remain model-independent.
- **Why 4.7.** F-03 documents the current non-legacy family (Opus 4.7, Sonnet 4.6, Haiku 4.5). Plugin-integrators run multiple models. F-18 (task_budget beta) is explicitly new; skills that *require* it exclude integrators who don't opt in. PRD REQ-07 pins `task_budget`/memory-tool as new-backlog, not migration — so migration-era skills must not presume them.
- **Observable signal.** In any 4.7-era SKILL.md, guidance that names a 4.7-only capability carries an explicit "on Opus 4.7:" prefix or lives under a "Model-specific optimisation" sub-heading (as required by PRD AC-02.2 for `prompt-engineer/SKILL.md`). A reviewer can confirm by grep-ing for naked `adaptive thinking` / `xhigh` references without such a prefix.

### P-4 — Observable Orchestration Contract (Sub-agent Dispatch)

- **What.** Any skill that dispatches sub-agents (delivery-flow, product-delivery, architect, developer, quality, operations, ui — per PRD scope-baseline §6 "Agent Invocation Template") emits a `SKILL_LOADED: <skill-name>` signal and does one-role-per-dispatch. The contract is already enforced stylistically in DISP-01 (delivery-flow/SKILL.md lines 328–345) — this pillar says **the contract is now load-bearing**, not stylistic.
- **Why 4.7.** F-08 (fewer sub-agents by default, steerable by prompting) makes sub-agent fusion a silent regression mode. PRD R-02 marks the risk High-impact/Low-likelihood; R-09 marks the conditional risk that fusion is *already* occurring on Idea/Refine. PRD M-03 pairs dispatch-count with hit-rate to catch silent fusion; that pairing only works if the contract is explicit.
- **Observable signal.** (a) Every dispatching skill's SKILL.md contains an explicit "one role = one dispatch" rule. (b) Hook `verify_skill_load.py` telemetry for the skill shows `SKILL_LOADED` first-attempt rate ≥ baseline (PRD M-07). (c) `dod_validators.<stage>` list length == observed dispatch count in run logs (PRD M-03, AC-03.3).

### P-5 — Calibrated Prompt-Pressure (No CRITICAL: Over-press)

- **What.** Prompt language is calibrated: important instructions use "Use …" / "Do …" framing, not "CRITICAL:"/"You MUST"/"NEVER". Strong language is reserved for genuinely irreversible or safety-relevant rules. (Matches F-28 — "tone down to normal phrasing".)
- **Why 4.7.** F-28 documents that overly strong prompting language may cause over-triggering on 4.6 / 4.7. F-25 (literal instruction following) compounds this: on 4.7, "CRITICAL: never X" reads as *literally never* — even when the author meant "usually don't, but exceptions apply".
- **Observable signal.** A grep-count table per keystone SKILL.md of `CRITICAL:`, `You MUST`, `NEVER`, `ALWAYS`. Review outcome recorded per-file as "acceptable / over-pressed". PRD REQ-06 AC-06.1 already specifies this audit; it is COULD priority, but the DX pillar says the *convention* is MUST even if the one-time audit is COULD.

### P-6 — Memory of Where Prompt-Caching Breakpoints Live (Latent)

- **What.** For any future skill that drives the Anthropic SDK directly, a comment block declaring where cache_control breakpoints sit (system prompt / tool defs / message prefix) and why.
- **Why 4.7.** F-16 confirms caching specs unchanged on 4.7 (4096-token minimum, 4 breakpoints, 20-block lookback). F-17 documents that switching adaptive↔enabled thinking modes breaks message-level cache breakpoints. PRD §3.1.1 confirms **the repo has zero Anthropic SDK imports today**, so this pillar is **latent** — it activates if/when a future backlog item wires a plugin to the SDK (PRD Open Question 8).
- **Observable signal.** Currently N/A (no SDK call sites exist). If introduced: grep for `anthropic.messages.create` and confirm every call site has a neighbouring comment naming its caching strategy.

### P-7 — Consistent Role-Prompt Shape Across Skills

- **What.** A shared skeleton for role prompts across delivery-team skills: `ROLE:` / `ALIAS:` / `TASK_TYPE:` / `INPUT ARTIFACTS:` / `YOUR TASK:` / `OUTPUT:` / `SIGNAL BLOCK:`. Already used by delivery-flow invocations (see the prompt prefix of this very task). This pillar makes it a documented convention, not a convergent habit.
- **Why 4.7.** F-25 (literal instruction following) rewards predictable prompt shape — Claude 4.7 follows the *shape* as faithfully as the content. A reader scanning six keystone SKILL.md files can triage faster with a shared skeleton than with six artisan styles.
- **Observable signal.** A documented skeleton (1 page) in `delivery-flow/references/` OR `prompt-engineer/SKILL.md`. Each role-dispatching skill's invocation template conforms. Reviewer can grep for `ROLE:` and `ALIAS:` across dispatch templates to confirm.

---

## 3. Authoring Flow Map

Two flows. Both are current-state-to-future-state narratives, not implementation steps.

### 3.1 Flow A — Creating a new skill in the 4.7 era (happy path)

1. Author loads `plugin-dev:skill-development` (CLAUDE.md convention).
2. Author copies the **4.7-era SKILL.md template** (proposed on-ramp artifact, see §5) into the new plugin directory.
3. Template pre-fills the P-1 header strip (`model_awareness: "opus-4-7"`, `last_audited: <today>`, `pattern_library_version: "4-7-1"`) and a P-7 role-prompt skeleton.
4. Author writes the skill body, citing `prompt-engineer/SKILL.md#<pattern-name>` wherever a 4.7-sensitive pattern applies (P-2).
5. Author runs `plugin-dev:skill-reviewer` post-edit; reviewer verifies P-1 header present, P-5 pressure calibrated, no `<thinking>` restatement (P-2).
6. `plugin-dev:plugin-validator` confirms plugin structure (unchanged by this engagement per PRD Non-goals).
7. Dogfood: author invokes the skill through delivery-flow on 4.7; `verify_skill_load.py` telemetry confirms `SKILL_LOADED` signal; any sub-agent dispatch produces dispatch count == expected (P-4 / PRD M-03).

**Where today's DX breaks down (Flow A).**

- (i) No template exists. Every new skill starts from a copy-paste of an existing large SKILL.md (mtg-commander at 1181 LOC, delivery-flow at 1072 LOC) and inherits whichever conventions that file happens to carry. PRD §3.7 documents size variance 66–1181 LOC and no shared skeleton.
- (ii) No P-1 header convention exists — zero files declare model-awareness (PRD §3.3 zero matches).
- (iii) `prompt-engineer/SKILL.md` is not referenced by path from any other skill, so P-2 citation has nowhere to point.

**What should change (Flow A).**

A 4.7-era template (one file, ≤80 lines) + a P-1 header convention + one documented reference path in `prompt-engineer/SKILL.md` (e.g., `#patterns/manual-cot-fallback`). These three artifacts unlock Flow A end-to-end.

### 3.2 Flow B — Updating an existing 4.6 skill for 4.7 compliance (actual migration flow)

1. Author opens the target SKILL.md (e.g., `prompt-engineer/SKILL.md`, a PRD keystone).
2. Author reads the **migration-guide stub** (proposed on-ramp artifact, see §5) which names the 6 findings F-13/F-15/F-25/F-26/F-28/F-29 and their typical textual symptoms.
3. Author walks the file top-to-bottom against a **per-file check-list** (carried in the roadmap for the 6 keystones per PRD REQ-02 AC-02.1).
4. Author edits in place; each edit cites its F-* finding in the commit message.
5. Author adds/updates the P-1 header strip: bumps `last_audited` to today, bumps `pattern_library_version` if the pattern library changed.
6. `plugin-dev:skill-reviewer` verifies the header strip and scans for retired patterns (e.g., `<thinking>` framed as "reasoning visibility" — PAT-01).
7. Dogfood the affected skill via delivery-flow on 4.7 (per PRD AC-02.4).
8. Register a baseline capture per PRD REQ-10 on the *first* migration run so subsequent regression metrics have a reference.

**Where today's DX breaks down (Flow B).**

- (i) There is no migration-guide stub today. Each author must re-derive "what does F-25 look like in prose?" from the Anthropic migration guide. PRD §3.3 caveat (rev 1) explicitly notes: *"the patterns above are API-shape patterns — literal string markers for SDK/knob usage. They cannot detect prose-level under-specification."*
- (ii) No per-file check-list exists until the Architect produces the roadmap. Until then, "migrate this SKILL.md" is a bare request with no instrument.
- (iii) Baseline capture (REQ-10) is a *new* concept introduced by rev 1 of the PRD. Authors have no memory of "how did the skill behave on 4.7 *before* I edited it?" — this is the single largest gap for measuring whether a prose edit was neutral-or-better.

**What should change (Flow B).**

The Architect's roadmap, plus the on-ramp artifacts in §5, plus one small tooling convention: *capture a baseline before you edit*. Explicit. Named. Path-specified. PRD REQ-10 AC-10.1 already specifies the capture shape; the DX layer names it as the first step of Flow B, not an afterthought.

---

## 4. Pattern Library Sketch

Five reusable patterns the Architect can standardise on. Each cites the PRD finding that justifies it. No pattern is proposed without a PRD anchor.

### Pattern 4.1 — Versioned Model Reference

- **When to use.** Any Python script or config that names a Claude model ID as a string (e.g., `agentic-flow-builder/scripts/agent_registry.py`, `prd-quality-gate-flow/stage_definitions.py`).
- **When NOT to use.** SKILL.md files (which should remain model-agnostic — P-3 fail-soft, PRD §3.1 observation "No plugin SKILL.md file contains any Claude model ID").
- **Example.**
  ```python
  # Canonical 4.7 model ID; see PRD F-01 / F-03.
  # Historical (retired 2026-06-15): "claude-opus-4-20250514"  [PRD F-04]
  # If wiring this to anthropic.messages.create, coordinate via claude-api skill (PRD Open Q8).
  OPUS_MODEL_ID = "claude-opus-4-7"
  ```
- **Anti-pattern retired.** Naked dated IDs with no provenance comment (MID-01/02/03 in `agent_registry.py` today — PRD §3.1 inventory).
- **PRD anchor.** F-01, F-03, F-04; PRD §3.1.1; REQ-01.

### Pattern 4.2 — 4.7-Aware Role Prompt Skeleton

- **When to use.** Every agent-dispatch invocation template (delivery-flow, product-delivery, architect, etc.).
- **When NOT to use.** Non-dispatching skills (e.g., `alias-creator/`, `prompt-engineer/` in its teaching role). They don't dispatch.
- **Example.**
  ```
  SKILL: <skill-name>
  TASK_TYPE: <task-type>
  ROLE: <role-name>
  ALIAS: <character-voice>   # F-27 tone shift risk; voice markers live in theme YAML

  INPUT ARTIFACTS:
  - <path>      # never paste content; pass paths (DISP-02)

  YOUR TASK: <single-role, single-deliverable — F-08 fusion guard>

  OUTPUT:
  Write to: <path>
  Then signal: SKILL_LOADED: <skill-name> / STATUS / ARTIFACT / SUMMARY
  ```
- **Anti-pattern retired.** Compound multi-role prompts that ask one agent to "wear the PO hat and the architect hat" — silent under F-08 fusion; already forbidden stylistically by DISP-01.
- **PRD anchor.** F-08, F-25, DISP-01, DISP-02; REQ-03.

### Pattern 4.3 — Manual CoT Fallback (replaces "`<thinking>` for reasoning visibility")

- **When to use.** Teaching or few-shot examples where the author wants to *show* reasoning steps explicitly (e.g., `prompt-engineer/SKILL.md` patterns, worked examples in any SKILL.md).
- **When NOT to use.** To describe Claude's API-level reasoning behaviour on 4.7 — that is adaptive thinking, which is *opaque by default* (F-13). Conflating the two is PAT-01.
- **Example.**
  ```markdown
  ## Manual CoT Fallback (works on any model, including Opus 4.7 with adaptive thinking off)

  Use <thinking> tags inside few-shot examples to demonstrate reasoning to Claude,
  not to retrieve Claude's own reasoning at runtime (on Opus 4.7, adaptive thinking
  is opaque by default — see F-13).

  Example:
    User: What's the most efficient sort for nearly-sorted data?
    Assistant: <thinking>
      Nearly-sorted -> insertion sort is O(n) in best case.
      Compare to O(n log n) for merge/quick.
    </thinking>
    Insertion sort — O(n) on nearly-sorted inputs.
  ```
- **Anti-pattern retired.** "Use `<thinking>` tags for reasoning visibility" framed as a Claude-runtime feature. On 4.7 that is factually incorrect for adaptive thinking; F-29 explicitly endorses `<thinking>` only as a prompt scaffold.
- **PRD anchor.** F-13, F-29; PAT-01, PAT-02, PAT-06; REQ-02 AC-02.2.

### Pattern 4.4 — Calibrated Instruction Voicing

- **When to use.** Every rule in a SKILL.md or agent prompt.
- **When NOT to use.** Exceptions: (a) truly irreversible actions ("Do not force-push to main"), (b) safety/compliance rules ("Never commit secrets"), (c) hook-enforced invariants where Claude is told to match the hook's contract.
- **Example.**
  ```markdown
  # Normal rule (preferred on 4.7 per F-28):
  Use the sub-agent dispatch pattern for every role in the team DoD.

  # Escalated rule (reserved for irreversibles):
  NEVER skip pre-commit hooks without explicit user approval.
  ```
- **Anti-pattern retired.** Blanket "CRITICAL:" / "You MUST" / "NEVER" prefixes applied to stylistic preferences. F-28: "you can use more normal prompting like 'Use this tool when…'".
- **PRD anchor.** F-28 (over-pressure warning); F-25 (literal instruction following compounds the cost); REQ-06 AC-06.1.

### Pattern 4.5 — Model-Specific Optimisation Sub-section

- **When to use.** Skills that teach prompt-engineering techniques or that could benefit from 4.7-specific levers (`prompt-engineer/SKILL.md` is the primary case; `research-agent/`, `delivery-flow/` references are secondary).
- **When NOT to use.** Skills whose purpose is model-agnostic (e.g., `alias-creator/` theme format — the schema is about content, not reasoning).
- **Example.**
  ```markdown
  ## Model-specific optimisation — Claude Opus 4.7

  - Adaptive thinking is the only supported thinking mode (F-11).
    Setting `thinking: {type: "enabled", budget_tokens: N}` returns 400.
  - `temperature`, `top_p`, `top_k` non-default ⇒ 400 (breaking changes).
  - Effort parameter: low / medium / high / xhigh / max. `xhigh` is the
    recommended default for coding / agentic work (F-15).
  - On Opus 4.7, manual CoT scaffolding may be redundant with adaptive
    thinking; remove scaffolding first, measure, then decide (F-26).
  ```
- **Anti-pattern retired.** Generic model-specific guidance scattered throughout a skill body (PAT-01 line 85; PAT-03 line 92; PAT-04 line 98; PAT-05 line 124 — all in `prompt-engineer/SKILL.md` today). Consolidating into one sub-section per model makes future migrations (e.g., 4.7 → 4.8) a single-section edit instead of a file-wide hunt.
- **PRD anchor.** F-11, F-15, F-25, F-26; REQ-02 AC-02.2.

### Pattern 4.6 — SKILL.md Forward-Compatibility Header (P-1)

- **When to use.** Every SKILL.md in the repo.
- **When NOT to use.** Paradigm sub-skills under 100 LOC MAY inherit their parent's header; otherwise universal.
- **Example.**
  ```yaml
  ---
  name: prompt-engineer
  description: Expert prompt optimization for LLMs and AI systems...
  model_awareness: opus-4-7
  last_audited: 2026-04-20
  pattern_library_version: 4-7-1
  ---
  ```
- **Anti-pattern retired.** YAML frontmatter that only names `name` + `description` (current state — PRD scope-baseline §4 shows 5-line frontmatter across most files). A reader cannot triage 4.7-awareness without reading the body.
- **PRD anchor.** P-1 pillar above; F-25 (literal instruction following raises the cost of stale instructions); REQ-02 (per-file audit needs a per-file date-of-audit signal).

---

## 5. Accessibility / Inclusion (On-Ramp for New Contributors)

A new skill-author — e.g., a community contributor dropping their first PR — should be able to pick up 4.7-era conventions without reading every file in `delivery-team/` (166 MD files, 34,870 lines of reference docs per PRD scope-baseline §1). Three on-ramp artifacts make this tractable:

1. **A `CONTRIBUTING-4-7.md` note** (or extension to existing CONTRIBUTING). One page. Lists the five pillars (P-1..P-5), points to the template, points to the migration-guide stub. The PRD repeatedly refers to CLAUDE.md as the binding convention doc; this note is its 4.7 companion — not a replacement.
2. **A migration-guide stub** (`delivery-team/skills/delivery-flow/references/4-7-migration-guide.md` or similar). One page. For each of the 6 keystone-audit findings (F-13, F-15, F-25, F-26, F-28, F-29) it gives: the finding summary (one line), a typical textual symptom (one example), the recommended edit pattern (one example from §4 above). The Architect's roadmap will generate the per-file instances; this stub generalises them for the next new skill.
3. **A 4.7-era example skill** (smallest possible — paradigm sub-skills at 66–80 LOC are the right size reference). Carries the P-1 header strip, the P-7 role-prompt skeleton, a `prompt-engineer/SKILL.md#<pattern>` citation in place of a restated pattern. Serves as both copy-paste template and reading reference.

**Scope note.** This is not a documentation deliverable for *this* engagement — the terminus is still a plan (PRD Constraint 8). But the Architect's roadmap should schedule these three artifacts as part of the implementation run, because without them the DX gains from the pattern library (§4) do not land — contributors will keep restating patterns because they have nowhere to point.

---

## 6. DX Metrics Proposal

Five DX metrics the Architect can adopt in the roadmap to measure whether the migration actually improved skill-author DX. Each is measurable; each names its instrument. None overlap with PRD §5 runtime metrics (M-01..M-07 measure runtime behaviour; these measure *authoring experience*).

### DX-M1 — Time-to-Triage for a First-Time Reader

- **Metric.** Median seconds from "open SKILL.md" to "correctly answer: is this file 4.7-audited?".
- **Target.** ≤ 10 seconds (equivalent to reading the P-1 header strip without scrolling).
- **Instrument.** Two-person code-walk with a stopwatch on the six keystone files pre- and post-implementation. N=2 readers × 6 files × 2 points-in-time = 24 trials.
- **Baseline.** Pre-implementation: effectively infinite — PRD §3.3 confirms no textual signal of 4.7-awareness exists anywhere.

### DX-M2 — Files-to-Read for the N-th Migration

- **Metric.** Count of distinct files a skill-author must read to migrate keystone file #N, after keystone #1..(N-1) have been migrated. Covers: the file itself, the migration-guide stub, the pattern library, any cited siblings.
- **Target.** Decreases monotonically with N. Keystone #6 should be readable with ≤ 3 supporting files open (the file itself + migration-guide stub + pattern library).
- **Instrument.** Self-report or commit-history analysis from the implementation run. If the author had to re-open the Anthropic migration guide mid-edit for file N, count +1.
- **Baseline.** Today: keystone #1 requires the author to read the Anthropic migration guide, scope-baseline.md, PRD §2 findings, and the target file itself — so baseline is 4 files (at minimum). Target keystone #6: 3 files.

### DX-M3 — Pattern Duplication Count

- **Metric.** `grep -c` of 4.7-sensitive patterns restated outside `prompt-engineer/SKILL.md` (specifically: `<thinking>` tags framed as reasoning visibility; manual CoT scaffolding without a "model-specific" caveat; `xhigh` / adaptive thinking mentions outside a "Model-specific optimisation" sub-section).
- **Target.** 0 (or every occurrence carries a citation to `prompt-engineer/SKILL.md#<pattern>`).
- **Instrument.** Grep script maintained alongside the repo's existing `workflow-injection-lint.yml` regression guard.
- **Baseline.** Today: PAT-01..PAT-07 in `prompt-engineer/SKILL.md` itself (some are valid, per PAT-03/PAT-04); plus 8 `chain of thought` matches across 5 files per PRD scope-baseline §3. Post-implementation target: 0 restatements across non-`prompt-engineer` files.

### DX-M4 — Header Coverage

- **Metric.** `grep -L "model_awareness:" **/SKILL.md | wc -l` — count of SKILL.md files *missing* the P-1 header strip.
- **Target.** 0 at roadmap completion.
- **Instrument.** Trivial grep; runs in CI on a per-PR basis.
- **Baseline.** Today: 17 (all SKILL.md files are missing it — PRD §3.3 zero matches).

### DX-M5 — Pressure-Calibration Ratio

- **Metric.** Ratio of "escalated rule" occurrences (`CRITICAL:|You MUST|NEVER|ALWAYS`) to total rule-like lines in the keystone files.
- **Target.** Each keystone's ratio is either (a) ≤ 10%, or (b) explicitly justified in a "Pressure rationale" comment per occurrence over 10%.
- **Instrument.** Grep-count + manual review. Aligns with PRD REQ-06 AC-06.1 but promotes it from COULD to a quantified DX metric.
- **Baseline.** Not yet measured (PRD REQ-06 is COULD, not yet executed). Architect can measure as part of Phase 1A AS-IS.

---

## 7. Open Questions for Architect

Questions this DX design surfaces that require architectural context to resolve. Named so the Architect's AS-IS / TO-BE / Roadmap can absorb them deliberately.

1. **Where does the 4.7-era pattern library physically live?** `prompt-engineer/SKILL.md` is the obvious home (P-2), but `plugin-dev:skill-development` (outside this repo, per PRD §3.6) is also a natural home. The Architect chooses: (a) single home in `prompt-engineer/`, (b) stubs in each plugin's `references/` citing `prompt-engineer/`, (c) co-owned with `plugin-dev:*`. Each has migration-path implications.

2. **Is the P-1 header strip CI-enforced or convention-only?** CI enforcement aligns with `workflow-injection-lint.yml` precedent but adds a regression guard. Convention-only keeps the PR surface light but risks drift. Related: should `last_audited` have an expiry (e.g., 180 days) that CI warns on?

3. **Does the Architect want one migration-guide stub, or one stub per audience (skill-author vs skill-operator vs plugin-integrator)?** DX favours one per audience; pragmatism favours one consolidated. Scope-wise, §5 proposes one; the Architect owns the choice.

4. **Where does the 4.7-era example skill live?** Option A: a paradigm sub-skill (`delivery-team/skills/architect/paradigms/ddd/SKILL.md` style, 66–80 LOC) becomes the exemplar and is augmented with the P-1 header first. Option B: a net-new minimal reference skill is added. Option B looks like new-feature scope (violating PRD Non-Goals) — the Architect should confirm Option A and pick *which* paradigm skill carries the demonstrator.

5. **How does REQ-10 baseline capture integrate with the DX flow?** PRD REQ-10 introduces baseline capture as a meta-requirement; the DX layer (Flow B step 8) treats it as the first action of any migration edit. The Architect should confirm the baseline-capture artifact path convention (`.delivery/artifacts/<impl-run>/observability/4-7-baseline.json`) and whether a lightweight shell script or a hook owns the capture — because whichever owns it becomes part of Flow B's step 1, not step 8.

6. **How does the DX pattern-library interact with the `claude-api` ambient skill (PRD Open Q8)?** If future backlog wires `prd-quality-gate-flow` or `agentic-flow-builder` to the Anthropic SDK through the `claude-api` skill, then pattern P-6 (caching breakpoints) activates. The Architect should decide whether the 4.7-era pattern library *forward-declares* P-6 (future-ready) or *omits until needed* (lean).

7. **Does P-4 (observable orchestration contract) imply a `hooks.json` change?** Hook `verify_skill_load.py` already detects `SKILL_LOADED` signals (PRD §3.5 HK-04). Whether the dispatch-count assertion (P-4 observable signal (c)) needs a new hook or can piggyback on existing telemetry is an architectural call the Architect owns. Either works; the DX layer just names the observable.

---

*"A skill that knows itself on 4.7 needs no sign at the gate — its voice carries the era in every line. Guard the keystones. Name the patterns. Leave a lantern at the threshold for whoever follows. And mend only what does not ring true."*

— **Galadriel**, UX Designer

---

**End of Skill-Author DX Design.**

---
work_item: WI-08
role: solution-architect
alias: Celebrimbor
target_file: delivery-team/skills/architect/SKILL.md
target_loc: 667
audit_types: [F-25, F-26]
pattern_library_version: 4-7-1
audited_on: 2026-04-22
---

# WI-08 — Architect SKILL.md F-25 / F-26 Audit

*Forged by Celebrimbor of Eregion. Every ring must be proven against the hammer before it is set upon a hand.*

## Scope

Target: `delivery-team/skills/architect/SKILL.md` (667 LOC).

Two audit lenses:

- **F-25 (under-specified instructions)** — Rules Opus 4.7 might execute *literally* in ways never intended by the authors. The model no longer reads through our prose with the charitable interpolation of a human reviewer; a dangling imperative with no guard becomes a contract.
- **F-26 (scaffolding duplicating 4.7 defaults)** — Manual cadence and meta-cognitive scaffolds ("summarise every 3 steps", "think step by step", "state your reasoning first") that duplicate what adaptive thinking already supplies natively.

Pattern-library citations use the names established in `.delivery/artifacts/04-architect/solution/transformation-plan.md`:

- **Pattern 4.2 — 4.7-Aware Role Prompt Skeleton** (`SKILL / TASK_TYPE / ROLE / ALIAS / INPUT ARTIFACTS / YOUR TASK / OUTPUT / SIGNAL BLOCK`).
- **Pattern 4.4 — Calibrated Instruction Voicing** (`Use …` / `Do …` default; `CRITICAL:` / `You MUST` / `NEVER` reserved for irreversibles).

The architect SKILL.md has a peculiarity not found in `product-delivery/SKILL.md`: the **sub-roles** are not sub-skills with their own SKILL.md — they are rows in a routing table plus a guardrails block. The audit therefore dissects the shared orchestration prose (Phase 1, Phase 2, Prior Art, Paradigm Router) *and* the per-row specification in the Role → Reference Mapping tables, the Task Type Routing tables, and the Guardrails blocks.

---

## PART A — F-25 Findings (Under-Specified Instructions)

### A-1. "If ambiguous, ask before proceeding. Do not assume." (L26)

**Literal-read failure mode:** Under 4.7's honesty priors, *any* task with more than one plausible role interpretation is "ambiguous." The architect may pause and emit a clarifying question at the start of work items that the pipeline has already bound (e.g., sprint-plan work with a declared `role:` field), converting a pipeline dispatch into an interactive prompt.

**Concrete recommendation (Pattern 4.4):** Re-voice to a calibrated conditional. Propose:

> *"If the incoming dispatch envelope has no explicit `role` field **and** two or more routing-table rows match with equal weight, ask one targeted question before proceeding. If a `role` field is present, treat it as authoritative; do not re-litigate."*

This reserves the interrupt for *irreversible* routing ambiguity and blocks the common false-positive.

### A-2. "Do not inline architecture knowledge into the main context." (L91)

**Literal-read failure mode:** 4.7 may decline to answer *any* architecture sub-question raised in conversation — including clarifications — on the grounds that a sub-agent must be spawned. The guardrail is intended to govern *reference-file contents*, not conversational reasoning.

**Concrete recommendation (Pattern 4.4):** Tighten the scope of the prohibition.

> *"Do not paste reference-file contents into the main context. Conversational clarification and role detection reasoning may occur in the main context; the sub-agent is the execution boundary for **artifact production**, not for dialogue."*

### A-3. "Read **only** the relevant reference file(s) from the routing table — do NOT read all reference files" (L87)

**Literal-read failure mode:** The `NOT` / `only` pairing is phrased as an absolute. For a cross-role task (e.g., a multiplayer-with-anti-cheat design), the architect must read two or three files; the literal rule forbids that, then §Cross-Role Tasks (L358) permits it. The contradiction resolves in 4.5 by charitable inference; 4.7 may surface the contradiction and ask.

**Concrete recommendation (Pattern 4.4):** Scope the prohibition and forward-reference the exception.

> *"Read the reference files named by the matched routing-table row(s). Do not read reference files outside the matched rows. For cross-role tasks, see §Cross-Role Tasks — multiple rows may match and their references combine."*

### A-4. "**If ambiguous, ask before proceeding. Do not assume.**" is re-stated implicitly in the Paradigm Router (L185–L189)

**Literal-read failure mode:** The priority chain says "*if the signal is present and unambiguous, routing is immediate — no further levels are consulted.*" This is correct behaviour, but 4.7 may treat the word *unambiguous* as a floor it rarely clears, causing it to fall through every level to the decision-matrix step even when config is set. The fallback path is expensive (decision-matrix evaluation) when the cheaper path (config value) is present.

**Concrete recommendation (Pattern 4.4):** Replace "unambiguous" with a concrete test.

> *"Level 1 applies when the user's prompt contains a single exact paradigm token from the set {`volatility`, `IDesign`, `DDD`, `domain-driven`, `team topology`, `event storming`, `business capability`}. If two or more tokens appear, proceed to Level 2. Level 2 applies whenever `architecture.decomposition` is a non-`auto` value; do not second-guess the config. Level 3 is the only level that evaluates the decision matrix."*

### A-5. Prior Art Analysis — "The Architect MUST NOT propose alternatives" (L59)

**Literal-read failure mode:** This is already an irreversible-class imperative (Pattern 4.4 permits `MUST NOT` here), but the rule has no timer or scope. 4.7 may carry the prohibition forward into *follow-up* tasks in the same session where the user has explicitly asked for alternatives (e.g., a later "what if we swapped Postgres for CockroachDB" question). The Decision Already Made classification is per-artifact, not per-session.

**Concrete recommendation (Pattern 4.4):** Scope the prohibition to the current artifact.

> *"Within the artifact being produced, the Architect MUST NOT propose alternatives to Decisions Already Made. If a subsequent user turn explicitly requests alternatives to a previously settled element, treat that turn as a new request and apply Prior Art Analysis afresh."*

### A-6. "Security is not optional — every design should address authentication, authorization, data protection, and audit" (L550)

**Literal-read failure mode:** The word *every* plus the four-term checklist. 4.7 may inject `Authentication / Authorization / Data Protection / Audit` headers into every design — including tasks like *game-systems* inventory design, pure *data-modeling* ERDs, and *C4 context diagrams* — where the concerns are genuinely out of scope or belong to an upstream design.

**Concrete recommendation (Pattern 4.4):** Qualify by task type.

> *"Designs for systems that process user data, external input, or cross trust boundaries must address authentication, authorization, data protection, and audit. Designs scoped strictly to internal data structures, algorithmic systems, or rendering pipelines may state 'Security: inherits from parent system [cite]' and skip the section."*

### A-7. "Failure modes must be addressed" (L551) with no stopping rule

**Literal-read failure mode:** 4.7 may exhaustively enumerate failure modes for every component (every network call, every disk write, every cache miss) for a modest feature design, producing pages of circuit-breaker / retry / fallback prose for a 3-component service. No ceiling is stated.

**Concrete recommendation (Pattern 4.2, via the Design Output contract):** Move the rule into the output contract as a scoped field.

> *"Design Output §Failure Modes — list the **top 3–5** failure modes ranked by impact × likelihood. For each, state the mitigation (circuit breaker / retry / fallback / degrade). Below-threshold failure modes are out of scope for this artifact."*

### A-8. "NFRs must be quantified — 'fast' is not an NFR; 'p99 latency under 200ms' is" (L548)

**Literal-read failure mode:** 4.7 may invent concrete NFR numbers to satisfy the rule when the PRD does not supply them — fabricating a `p99 < 200ms` target the user never specified. The rule punishes the qualitative NFR without supplying a fallback.

**Concrete recommendation (Pattern 4.4):** Add the quote-or-TBD fallback.

> *"NFRs must be quantified when the input artifacts supply numbers. When they do not, state the NFR as 'TBD — quantification required; see §Open Questions' and record the missing quantification in §Open Questions. Do not invent numbers."*

### A-9. "Determinism requirements — state whether the system must be deterministic" (L562)

**Literal-read failure mode:** The rule applies to *every game system*. 4.7 may add a `Determinism: not required` line to every single-player shader-pipeline, UI-HUD, and inventory design, producing boilerplate. The rule's true target is netcode, replays, and save/load — the three cases listed parenthetically.

**Concrete recommendation (Pattern 4.4):** Scope to the listed cases.

> *"For **netcode, replays, and save/load** designs, determinism requirements MUST be stated explicitly (required / not-required / partial, plus floating-point and RNG-seeding policy). For other game systems, state determinism only if it is a design driver."*

### A-10. "Escalate to human if PO cannot answer critical questions" (L243)

**Literal-read failure mode:** The Domain Discovery step sits before every `design` / `decompose` task. 4.7 may fire an escalation on the first partial PO answer, converting the architect into a blocking agent. The word *cannot* is weaker than the authors likely intended — 4.7 reads any hedged answer as "cannot."

**Concrete recommendation (Pattern 4.4):** Replace with a concrete threshold.

> *"Escalate only if, after one follow-up round, the PO's answers still leave two or more **domain-discovery question-set items marked critical** unanswered. Partial answers to non-critical items are proceed-with-assumption."*

### A-11. "Do not read reference files outside the matched rows" (implicit in L87)

**Literal-read failure mode:** The architect might need to read `adr-lifecycle.md` during an `adr review` command even though it is not in the routing table. The rule as phrased forbids this. The `User Commands` table at L615 references behaviours (e.g., `adr review`) without saying which reference unlocks.

**Concrete recommendation (Pattern 4.2, via the User Commands table):** Add a `References Loaded` column to the User Commands table so each command names its own reference set, bringing them under the same explicit-load discipline as the routing table.

### A-12. Cross-Role Tasks — "If concerns are truly independent, spawn separate sub-agents sequentially" (L365)

**Literal-read failure mode:** The phrase "truly independent" is a vibe test. 4.7 may split or merge where the authors would not. The cost of splitting is two round-trips; the cost of merging is a bloated single sub-agent context.

**Concrete recommendation (Pattern 4.4):** State the test.

> *"Spawn a single sub-agent when references share >30% of their content **or** the task output is a single integrated artifact. Spawn sequential sub-agents when outputs are separable artifacts (e.g., a threat model and an ADR are separable; a design and its C4 diagram are one)."*

### A-13. The Sub-Agent Prompt Template (L95–L128) does not match Pattern 4.2 shape

**Literal-read failure mode:** This is the single largest F-25 / Pattern 4.2 alignment gap in the file. The template has no `SKILL`, `TASK_TYPE`, `ROLE`, `ALIAS`, `SIGNAL BLOCK`, and no structured `INPUT ARTIFACTS` / `YOUR TASK` / `OUTPUT` headers. 4.7 infers the shape from prose; 4.7 is better off when the shape is explicit.

**Concrete recommendation (Pattern 4.2):** Rewrite the template skeleton to match Pattern 4.2 by name. Draft (to be executed in impl run, not WI-08):

```
SKILL: delivery-team:architect (sub-agent)
TASK_TYPE: [design | review | ...]
ROLE: [solution | enterprise | data | security | ...]
ALIAS: [optional — inherit from parent alias theme]

INPUT ARTIFACTS
[PASTE FULL CONTENTS OF EACH RELEVANT REFERENCE FILE — separated by --- if multiple]

Context envelope:
- System / game: ...
- Constraints: ...
- NFRs: ...
- PRD reference: ...
- Prior Art results: ...

YOUR TASK
[TASK TYPE]: [DESCRIBE WHAT THE USER WANTS]

OUTPUT
Produce the artifact using the Output Contract matching TASK_TYPE.
Include: trade-off analysis, assumptions, risks, next steps.

SIGNAL BLOCK
End with exactly:
STATUS: DONE
ARTIFACT: <relative path>
SUMMARY: <one sentence>
```

### A-14. "Every design must state its trade-offs — 'No trade-offs' is not acceptable" (L544)

**Literal-read failure mode:** 4.7 may fabricate trade-offs to satisfy the rule on a genuinely single-option decision (e.g., a library choice forced by enterprise standard). The rule has no exit.

**Concrete recommendation (Pattern 4.4):** Permit the `forced-choice` escape.

> *"Every design must state its trade-offs. If the decision is forced (e.g., by enterprise standard, platform mandate, or prior ADR), state: 'Forced by [source]; alternatives not evaluated.' — this counts as the trade-off statement."*

### A-15. "Prefer composition over inheritance in system design" (L546)

**Literal-read failure mode:** The rule is phrased as a preference but, under 4.7's literal reading, becomes a near-prohibition. In game architecture — where inheritance hierarchies are dominant (Node → CharacterBody2D → Player) — 4.7 may refactor design away from idiomatic patterns.

**Concrete recommendation (Pattern 4.4):** Scope to service-level composition.

> *"At the service / component / system level, prefer composition over inheritance. Within a component's internal type system, idiomatic inheritance is permitted where the host language or engine recommends it (e.g., Godot node hierarchies)."*

---

## PART B — F-26 Findings (Scaffolding Duplicating 4.7 Defaults)

### B-1. Phase 1 → Phase 2 narrative gating (L17, L82)

**Finding:** The file frames role detection and sub-agent invocation as two explicit phases with numbered steps. This is scaffolding: 4.7's tool-use loop already decomposes "detect route then execute" without being told. The phases do not add behaviour; they add prose.

**Concrete recommendation:** Keep the section headers (they function as anchor points) but collapse the numbered step lists in L17–L24 and L82–L89 into a single declarative paragraph each. 4.7 does not need a checklist to know that role detection precedes dispatch.

### B-2. "Declare before every task: `Role: [ROLE] | Task: [TYPE] | References: [list of reference files]`" (L28–L30)

**Finding:** Forcing a header declaration before every task is the classic meta-cognitive scaffold — making the model "show its work" before acting. 4.7 emits structured dispatch envelopes natively when the sub-agent prompt asks for them (see SIGNAL BLOCK in Pattern 4.2).

**Concrete recommendation:** Keep the declaration only where it is *load-bearing*, namely at sub-agent boundaries where the parent needs it for audit. Drop the "before every task" framing and move the format into the Pattern 4.2-shaped sub-agent prompt template (A-13) where it belongs as an `INPUT ARTIFACTS` echo.

### B-3. Domain Discovery "Process" numbered list (L240–L244)

**Finding:** A five-step numbered list (select → invoke PO → evaluate → escalate → record). 4.7 given the *goal* ("gather business context before designing") and the *reference* (`domain-discovery.md`) will execute these steps without being told in order. The numbered list is cadence scaffolding.

**Concrete recommendation:** Collapse to one paragraph stating the goal and the escalation threshold (see A-10). Move the step-by-step into `references/domain-discovery.md` where it belongs.

### B-4. Prior Art Analysis four-step scaffold (L40–L74)

**Finding:** Steps 1 (Read and Summarize), 2 (Classify), 3 (Build On), 4 (Deviation Protocol) are numbered as a fixed cadence. Steps 1 and 3 are things 4.7 will do unprompted when given a spec and a task. Step 2 (classification table) and Step 4 (deviation protocol) are load-bearing — they produce structured artifacts the downstream gate checks for.

**Concrete recommendation:** Demote Step 1 and Step 3 to prose inside the introduction; keep Step 2 and Step 4 as explicit sections since they produce audit artifacts. The cadence-scaffolding is in Steps 1 and 3.

### B-5. Paradigm Router "priority chain" enumeration (L185–L189)

**Finding:** The three-level numbered chain is partly content (the levels differ in *data source*) and partly cadence (the "no further levels are consulted" clause). The cadence clause is 4.7 default behaviour — when a lookup succeeds, it does not re-lookup.

**Concrete recommendation:** Keep the three levels (they are content), drop the cadence clause, and replace "if the signal is present and unambiguous, routing is immediate" with the concrete test from A-4.

### B-6. "For every architecture task, follow these steps exactly — do not skip:" (L84)

**Finding:** Classic F-26 pattern — emphasising non-skipping is a 4.5-era scaffold addressing a failure mode (step skipping) that 4.7 does not exhibit on well-formed dispatches. The phrase converts flexible steps into rigid ones without need.

**Concrete recommendation:** Delete the "exactly — do not skip" emphasis. Keep the list; trust the model.

### B-7. Guardrails framed as output enforcement loop (L540 "in every output")

**Finding:** The architecture guardrails section says "The sub-agent must enforce these in every output." This is meta-instruction scaffolding — telling the sub-agent to *self-check* after generation. 4.7, when given the guardrail list inside the sub-agent prompt, produces compliant output on the first pass; an explicit self-check loop is not load-bearing.

**Concrete recommendation:** Reframe the section header from "Architecture Guardrails" (enforcement frame) to "Architecture Invariants" (property frame). Remove the "in every output" clause. The guardrails remain; the self-check scaffolding goes.

### B-8. The `User Commands` table (L615–L629)

**Finding:** A command vocabulary that pre-dates 4.7's free-form tool-use. `role <name>`, `adr`, `c4`, `review`, `threats`, etc. — these are a 4.5-era scaffold to constrain user intent. 4.7 reads "write an ADR for this decision" as naturally as `adr`. The table is dual-coded with the Task Type Routing Table and is not referenced anywhere else in the file.

**Concrete recommendation:** Either delete the User Commands table (redundant with the routing table) or demote it to a single line: *"Users may invoke any task type by name (`design`, `review`, `decompose`, etc.) or by natural-language phrase; both resolve to the same routing."*

### B-9. "Phase 2: Sub-Agent Invocation" §1 "Detect the role(s) and task type (Phase 1)" (L86)

**Finding:** A cross-reference back to the phase just completed. 4.7 does not need to be told that the phase it just ran was Phase 1.

**Concrete recommendation:** Delete the cross-reference.

### B-10. Output contracts use code-fenced markdown templates (L386, L423, L446, L486, L514)

**Finding:** These are *not* F-26 scaffolds — the templates are load-bearing. They define the artifact shape. This is called out here explicitly as a **non-finding** so impl run does not collapse them by mistake.

**Concrete recommendation:** **None.** Preserve these templates as-is (though A-7 and A-13 propose additions *inside* them).

---

## PART C — Per-Sub-Role Audit

Each of the 11 sub-roles (7 software + 4 game) is audited below, plus the paradigm router. Each section has either a concrete Pattern-4.2 / Pattern-4.4 recommendation or an explicit Done-with-reason.

### Solution Architect

**References mapped:** architecture-patterns.md, c4-model.md, adr-template.md, quality-attributes.md.

**F-25 finding — "how should we build" phrase (L277).** The routing signal "how should we build" is vibes-grade. 4.7 will match almost any design conversation to `design` if this phrase is a signal. The PRD may have a feature-refinement turn that uses the same words.

**Concrete recommendation (Pattern 4.4):** Tighten the routing phrase to *"design a system", "architect a solution", "architecture for X"* — drop "how should we build" which over-matches.

**F-25 finding — "full system design" cross-role combo (L378).** The Cross-Role Tasks table's "Full system design" row loads four references simultaneously. When the task is a small feature design, this triples context load unnecessarily.

**Concrete recommendation (Pattern 4.2):** Rename the row "Full greenfield system design" and add a note: *"For feature-scoped design within an existing system, use the single-row `design` routing; do not use the full bundle."*

### Enterprise Architect

**References mapped:** enterprise-patterns.md, technology-evaluation.md.

**F-25 finding — "governance" as a signal (L286).** The word *governance* appears in many contexts (data governance, API governance, AI governance). Under 4.7, a data-governance question will mis-route to Enterprise Architect instead of Data Architect.

**Concrete recommendation (Pattern 4.4):** Replace the bare "governance" signal with *"technology governance", "architecture governance", "portfolio governance"* — three disambiguated phrases. Leave "data governance" to the data-design row (L284) exclusively.

### Data Architect

**References mapped:** data-modeling.md.

**F-25 finding — routing signals include "data flow" (L284)** which is also triggered by Integration (L287) and the general `design` row. Three-way collision.

**Concrete recommendation (Pattern 4.4):** Scope "data flow" to data-architecture contexts: *"data flow (between persistence stores)"*. Leave inter-service data flow to the `integration` row.

### Security Architect

**References mapped:** security-patterns.md.

**F-26 finding — the Security role shares routing with Compliance Officer (L289, L293).** The rows "security-requirements" and "risk-assessment" list `Security/Compliance Officer` as joint roles, loading two reference files. 4.7 given two reference sets will produce dual-voiced output. Pattern 4.2 is clearer with one ROLE per dispatch.

**Concrete recommendation (Pattern 4.2):** Split joint-role rows. "security-requirements" routes primarily to Security; include `compliance-frameworks.md` as an auxiliary reference, not a co-role. Same for "risk-assessment" — one primary role, the other is an auxiliary reference.

### Compliance Officer

**References mapped:** compliance-frameworks.md, security-requirements.md.

**F-25 finding — "regulatory requirements" phrase (L288)** is domain-broad. Any regulated-industry task will match, even non-architectural ones.

**Concrete recommendation (Pattern 4.4):** Tighten to *"regulatory compliance requirements", "control mapping to regulation"* — two-word disambiguated phrases that scope to compliance architecture rather than regulation-adjacent product work.

### Privacy Engineer

**References mapped:** privacy-patterns.md, compliance-frameworks.md.

**Done-with-reason.** The privacy-assessment row (L291) has disambiguated routing signals (GDPR / CCPA / DPIA / consent management / data subject rights / privacy by design) that are all privacy-specific; none collide with other roles. Reference mapping is minimal (2 files) and focused. Prose does not repeat any of the A-series findings in a privacy-specific form. **No changes required for this sub-role beyond the cross-cutting recommendations already in Part A and Part B.**

### Incident Responder

**References mapped:** incident-response.md, security-patterns.md.

**F-25 finding — "tabletop exercise" phrase (L290).** Tabletop exercises are also used in *threat modeling* and *product risk* contexts. A pure threat-model task containing the phrase "run a tabletop exercise" will mis-route to Incident Responder instead of Security → threat-model.

**Concrete recommendation (Pattern 4.4):** Disambiguate to *"incident tabletop exercise", "IR tabletop"*. Threat-modeling tabletops remain with Security.

### Game Systems Architect

**References mapped:** game-systems.md.

**F-25 finding — "AI architecture" signal (L338)** collides with general software AI/ML architecture discussions. A task like "architect an AI-powered feature" will mis-route to game-systems because of the bare "AI architecture" signal.

**Concrete recommendation (Pattern 4.4):** Tighten to *"game AI architecture", "NPC AI architecture", "behavior tree"* — all three are unambiguous to game contexts. Drop the bare "AI architecture" phrase.

### Level/World Architect

**References mapped:** level-world.md.

**F-25 finding — "streaming" and "loading zones" signals (L339)** collide with data-streaming (Kafka, event streams) and web-app loading. Without a `+ game context` qualifier, 4.7 will mis-route.

**Concrete recommendation (Pattern 4.4):** Tighten to *"world streaming", "level streaming", "loading zones (game)"*. The `game-review` row at L342 uses `"review" + game context` as a qualifier — apply the same `+ game context` discipline to streaming / loading-zone signals.

### Network/Multiplayer Architect

**References mapped:** network-multiplayer.md.

**F-25 finding — "client-server" signal (L340)** is the fundamental phrase of all web architecture; it belongs to Solution Architect for non-game contexts. As written, it would hijack any web-service design that uses the phrase.

**Concrete recommendation (Pattern 4.4):** Replace bare "client-server" with *"game client-server netcode", "authoritative server (multiplayer)"*. The phrase "client-server" alone should route to Solution per the `design` row.

### Graphics/Rendering Architect

**References mapped:** graphics-rendering.md.

**F-25 finding — "camera system" and "material system" signals (L341)** are game-engine specific but the phrase "camera system" also appears in VR / AR / CV contexts. Narrow scope.

**Concrete recommendation (Pattern 4.4):** Tighten to *"game camera system", "render camera system", "engine material system"*. Leave CV / AR cameras to Solution or the domain-specific role they call in.

### Paradigm Router (as a routing construct, not a sub-role)

**F-25 finding — already covered in A-4** (the "unambiguous" word). **F-26 finding — already covered in B-5** (the "no further levels consulted" cadence clause). **F-25 finding — Backwards Compatibility Fallback (L204–L206)**: the rule "if `paradigms/` directory does not exist … the router falls back to executing decomposition inline" is a behaviour the architect cannot *itself* verify without a filesystem probe. 4.7 may conclude the directory does not exist because it has not read it, triggering the fallback spuriously.

**Concrete recommendation (Pattern 4.4):** Re-voice the fallback check as *"If a `Glob` for `paradigms/<detected-id>/SKILL.md` returns empty, fall back to inline decomposition. Do not assume non-existence without the Glob."* This replaces an assumption with an observable action.

---

## Summary & Roadmap

| ID | Pattern cited | Severity | Effort |
|----|---------------|----------|--------|
| A-1 | 4.4 | High — interactive-interrupt risk | S |
| A-2 | 4.4 | High — scope creep | S |
| A-3 | 4.4 | High — rule contradiction | S |
| A-4 | 4.4 | Medium | S |
| A-5 | 4.4 | Medium | S |
| A-6 | 4.4 | Medium — boilerplate risk | S |
| A-7 | 4.2 | Medium — stopping rule | S |
| A-8 | 4.4 | High — fabrication risk | S |
| A-9 | 4.4 | Low — boilerplate | XS |
| A-10 | 4.4 | Medium — blocking risk | S |
| A-11 | 4.2 | Low — completeness | XS |
| A-12 | 4.4 | Low | XS |
| A-13 | 4.2 | **High — largest alignment gap in file** | M |
| A-14 | 4.4 | Medium — fabrication risk | XS |
| A-15 | 4.4 | Medium — idiom violation | XS |
| B-1 | 4.2 | Low | XS |
| B-2 | 4.2 | Medium — meta-cognitive scaffold | S |
| B-3 | — | Low | XS |
| B-4 | — | Low | XS |
| B-5 | — | Low | XS |
| B-6 | 4.4 | Low | XS |
| B-7 | — | Low — reframing | XS |
| B-8 | — | Medium — deletion candidate | XS |
| B-9 | — | XS | XS |
| B-10 | — | **Non-finding — do not change** | — |

**Top three priorities for impl run** (ordered by risk × impact):

1. **A-13** — rewrite the sub-agent prompt template to Pattern 4.2 shape. This is the single largest 4.7-alignment gap in the file and affects every dispatch the architect makes.
2. **A-8** — add the quote-or-TBD fallback to the NFR-quantification rule. Under 4.7 the fabrication risk is real.
3. **A-1 / A-10** — fix the two "ask / escalate" rules that can convert the architect from a producer into a blocker.

**Deferred to later waves:**

- B-8 User Commands deletion — do after routing-table edits to avoid double-touching the same region.
- C-series routing-signal tightening — batch into a single routing-table pass rather than 11 micro-edits.

*This audit is complete. The ring is proven; where the hammer struck and no ring of power was found, I have marked the metal for re-forging.*

— Celebrimbor, Lord of Eregion

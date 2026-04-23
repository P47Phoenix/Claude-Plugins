# Prompt Library

Documentation for the prompts embedded in `SKILL.md`. Each entry follows the prompt-engineer skill's required output format: version, technique(s) used, design rationale, known limitations, example input/output.

---

## Prompt 1: Research Type Classifier

**Version:** 1.0 — 2026-03-21
**Pattern Used:** Step-by-Step Analyzer with Manual CoT Fallback scaffolding (see `prompt-engineer/SKILL.md#pattern-4-3`)
**Recommended Model:** Claude Sonnet or Opus; Opus preferred for ambiguous multi-type questions

### Full Prompt (embedded in Phase 1 of SKILL.md)

```
Before beginning any research, classify the research type using the following decision process:

- "How does / How can / How might / Explore / Discover / What factors" → EXPLORATORY
- "What is / What are / What exists / Map / Document / Inventory" → DESCRIPTIVE
- "Why / Root cause / Because / Caused by / What led to" → EXPLANATORY
- "Did X work / Impact / Is X effective / Worth it / Evaluate" → EVALUATIVE
- "Compare / Which is better / Alternatives / Options / vs." → COMPARATIVE

Disambiguation rules:
- "Compare X to understand Y" where understanding is the goal → EXPLORATORY
- "What is the current state of X" (mapping) → DESCRIPTIVE; "was X successful" (judging) → EVALUATIVE

Always declare: "Research Type: [TYPE] | Framework: [Y] | Protocol: [Z]"
If ambiguous, state both options and ask before proceeding.
```

### Design Rationale
Uses the Step-by-Step Analyzer pattern — internal reasoning before committing to a type prevents premature pattern selection. Signal word anchoring provides deterministic routing for the majority of questions, while disambiguation rules handle the most common edge cases (exploratory-vs-comparative and descriptive-vs-evaluative confusion). The explicit declaration requirement makes routing inspectable and correctable by the user.

### Usage Guidelines
- Works best when the user's question preserves its natural phrasing (don't paraphrase before classification)
- The declaration step is mandatory — do not skip even when type seems obvious
- Temperature: 0.0–0.3 (deterministic routing is the goal)

### Example Input / Output
**Input:** "Why did our API latency increase after the v3 deployment?"

**Output:** `Research Type: Explanatory | Framework: PECO | Protocol: Standard / RCA`

### Known Limitations
- Compound questions ("why did X happen and what should we do about it?") contain multiple types — default to the first type, then note the secondary type
- "How to" questions are ambiguous: "How to build X" is a task, not research; "How does X work" is Exploratory. Ask the user if unclear
- Does not handle research type chaining (when one research session should flow into another type)

---

## Prompt 2: PICO / SPICE / PECO Reformulator

**Version:** 1.0 — 2026-03-21
**Pattern Used:** Structured Output Generator with fill-in template
**Recommended Model:** Any Claude model

### Full Prompt (embedded in Phase 2 of SKILL.md)

```
Apply the detected framework to reformulate the raw question into a structured research question.

If PICO:
P (Population/Problem): [Who or what is being studied]
I (Intervention): [What action, technology, or phenomenon]
C (Comparison): [What alternative or baseline]
O (Outcome): [What is measured or expected to change]
Reformulated: "In [P], does [I] compared to [C] result in [O]?"

If SPICE: [SPICE components...]
If PECO: [PECO components...]
If None: State raw question. Decompose into 3–5 sub-questions.
```

### Design Rationale
Template forcing prevents question drift — without explicit component identification, researchers (human and AI) tend to narrow to the parts of the question they find most interesting. The reformulated sentence forces all components into a single evaluable claim, which directly constrains what counts as relevant evidence in Phase 4.

### Usage Guidelines
- If a PICO component is genuinely absent (no natural comparison exists), use "no intervention / baseline state" as C
- Do not force PICO onto qualitative questions — if the user's context involves lived experience or perspective, prefer SPICE
- The reformulated question should be answerable in principle; if it is not, refine before proceeding

### Example Input / Output
**Input:** "Does using connection pooling in our PostgreSQL setup improve throughput under load?"

**PICO Output:**
```
P: Node.js API service handling concurrent database queries
I: PgBouncer connection pooling in transaction mode
C: Direct connection per request (current approach)
O: Throughput (req/s) and P99 latency under 500 concurrent users

Reformulated: "In Node.js API services with concurrent DB queries (P), does PgBouncer connection pooling (I) compared to direct per-request connections (C) improve throughput and reduce P99 latency under 500 concurrent users (O)?"
```

### Known Limitations
- PICO was designed for clinical intervention research; some software questions lack a natural "comparison" — use "current approach" or "no intervention" as a pragmatic baseline
- SPICE's "perspective" component requires knowing whose viewpoint matters; ask the user if unclear
- Forcing a poor framework fit produces misleading questions — always prefer `None` with sub-questions over a strained PICO

---

## Prompt 3: ReAct Gather Cycle

**Version:** 1.0 — 2026-03-21
**Pattern Used:** ReAct (Reasoning + Acting) — Thought → Action → Observation cycles
**Recommended Model:** Claude Sonnet or Opus with tool access (WebSearch, WebFetch, Grep, Read)

### Full Prompt (embedded in Phase 5 of SKILL.md)

```
For each source in the plan, execute a ReAct cycle:

Thought: [What specific information am I seeking? What would confirm or deny the hypothesis?]
Action: [Specific search / fetch / read operation]
Observation: [What was found — verbatim excerpt in "..." or labeled paraphrase]
Relevance: [High / Medium / Low] — [Why this matters to the research question]
Source ID: S[N]
GRADE: [⊕⊕⊕⊕ / ⊕⊕⊕◯ / ⊕⊕◯◯ / ⊕◯◯◯]
```

### Design Rationale
The ReAct pattern was chosen because research requires bidirectional learning — reasoning informs what to look for, and observations update the reasoning. Each `Thought` step forces articulation of what evidence is being sought before looking, preventing unconscious selection of confirming evidence. The `Observation` step with the verbatim/paraphrase distinction creates an auditable record that distinguishes what the source actually said from interpretation. Assigning GRADE at collection time (not synthesis time) prevents grade inflation driven by narrative consistency.

### Usage Guidelines
- One ReAct cycle per source — do not batch multiple sources into a single cycle
- The `Thought` should reference the specific claim being investigated, not just "find information about X"
- If a source is not found or returns no relevant content, record: `Observation: Source not found / No relevant content` — do not skip the cycle
- Temperature: 0.3–0.7 (some creativity in search strategy is beneficial)

### Example Input / Output
**Thought:** I need to verify whether the official Stripe docs state a rate limit for the payment intents endpoint specifically, as the general rate limit claim in S1 may not apply per-endpoint.

**Action:** WebFetch Stripe API documentation rate limits section

**Observation:** "The Stripe API rate limit is 100 read operations per second and 100 write operations per second in live mode, applied globally across your account, not per endpoint." (verbatim)

**Relevance:** High — confirms S1's general rate limit claim and clarifies it applies globally, not per-endpoint. This affects the Comparative evaluation criterion for "rate limit granularity."

**Source ID:** S4
**GRADE:** ⊕⊕⊕⊕ (official primary documentation, current version)

### Known Limitations
- Verbose for simple single-source lookups — acceptable trade-off; consistency outweighs efficiency for research tasks
- The `Thought` quality depends on how well the research question is framed in Phase 2; poor PICO framing produces vague Thoughts
- Cannot detect source reliability issues not visible in the text (e.g., sponsored content, hidden conflicts of interest) — flag when suspected

---

## Prompt 4: Synthesis Self-Critique

**Version:** 1.0 — 2026-03-21
**Pattern Used:** Self-Correcting Agent — initial output → critique checklist → revision
**Recommended Model:** Claude Opus preferred (reasoning depth improves critique quality)

### Full Prompt (embedded in Phase 6 of SKILL.md)

```
For each dimension:
1. Write initial finding with citations: "[Finding statement] [S1], [S3]"
2. Self-critique checklist:
   ☐ Am I cherry-picking? (check for contradicting sources)
   ☐ Is this independently confirmed? (cross-source validation)
   ☐ Am I confusing correlation with causation? (for Explanatory type)
   ☐ Are all citations accurate? (each [Sx] must exist in the source table)
   ☐ Is speculation labeled [HYPOTHESIS] or [INFERENCE]?
3. Revise if critique reveals gaps
4. Assign GRADE confidence level per claim
```

### Design Rationale
Research synthesis is the highest-risk phase for confirmation bias — the researcher has already collected evidence and naturally frames findings to cohere. The Self-Correcting Agent pattern inserts a mandatory adversarial pass before findings are finalized. The checklist is ordered from most common to least common failure: cherry-picking is the dominant failure mode, citation accuracy is the most verifiable. Explicit GRADE assignment at this step (not earlier) ensures confidence level reflects the full synthesized picture, not just individual source quality.

### Usage Guidelines
- The critique must be performed per dimension, not once globally at the end
- If the checklist reveals a problem (e.g., a contradicting source was not addressed), revise the finding before moving on — do not note the problem and proceed
- "Cherry-picking" check: actively search the collected sources for any that contradict the initial finding before declaring it clean

### Example Input / Output
**Initial finding:** "Redis outperforms Memcached for session storage workloads. [S2], [S5]"

**Self-critique:**
- ☑ Cherry-picking? S3 shows Memcached outperforms Redis for simple get/set with very small payloads (< 100 bytes). Not addressed in initial finding.
- ☑ Independent confirmation? S2 (benchmark) and S5 (production case study) are independent. Good.
- ☑ Causation? Claiming performance difference, not causal mechanism — acceptable.
- ☑ Citations accurate? S2 and S5 exist in source table. Good.
- ☑ Speculation labeled? No speculation in initial finding. Good.

**Revised finding:** "Redis outperforms Memcached for session storage workloads involving complex data types or payloads > 100 bytes [S2], [S5]. For simple string get/set with very small payloads, Memcached may outperform Redis [S3] [GRADE: ⊕⊕⊕◯ — scope-limited by payload size]."

### Known Limitations
- Self-critique quality is model-dependent — Sonnet may miss subtle cherry-picking that Opus would catch
- The checklist does not cover all possible synthesis errors (e.g., ecological fallacy, Simpson's paradox in aggregate data)
- Cannot detect fabricated or altered sources within the collected set — integrity constraints in SKILL.md must handle this separately

---

## Prompt 5: GRADE Assignment

**Version:** 1.0 — 2026-03-21
**Pattern Used:** Expert System with explicit grading rubric
**Recommended Model:** Any Claude model

### Full Prompt (embedded in GRADE section of SKILL.md)

```
Apply to every claim and source:

| GRADE | Symbol | Criteria |
|-------|--------|----------|
| High | ⊕⊕⊕⊕ | Multiple independent primary sources; replicated; code-confirmed |
| Moderate | ⊕⊕⊕◯ | Single strong primary or converging peer-reviewed secondaries |
| Low | ⊕⊕◯◯ | Indirect evidence, grey literature, or single secondary source |
| Very Low | ⊕◯◯◯ | Anecdote, forum post, unverified claim, or single non-peer source |
```

### Design Rationale
A 4-level system (rather than the original 3-level High/Medium/Low) distinguishes between "probably correct" (Moderate ⊕⊕⊕◯) and "possibly correct" (Low ⊕⊕◯◯) — a meaningful difference when acting on research findings. The ⊕ symbol notation is scannable in tables. Assigning GRADE at collection time (Phase 5) and re-evaluating at synthesis time (Phase 6) provides two checkpoints. Per-claim GRADE (not just per-source) allows a High-quality source to be cited for a Moderate-confidence claim when the source only partially addresses it.

### Usage Guidelines
- GRADE applies to both individual sources (at collection) and synthesized claims (at synthesis)
- A claim can have lower GRADE than its sources — a High-quality source speaking tangentially to the claim is still Low GRADE for that claim
- When in doubt between two GRADE levels, apply the lower one and state the reason

### Example Input / Output
**Source:** Official AWS documentation for DynamoDB read capacity units, current version

**Source GRADE:** ⊕⊕⊕⊕ (official primary, current, directly relevant)

**Claim:** "DynamoDB provisioned throughput costs scale linearly with request volume."

**Claim GRADE:** ⊕⊕⊕◯ — the documentation confirms the pricing model but community reports [S6] indicate non-linear cost behavior under burst scenarios not covered in official docs.

### Known Limitations
- GRADE level is partly subjective for edge cases — document reasoning alongside the rating
- "Multiple independent primary sources" can be gamed if sources share a common upstream (e.g., two blog posts citing the same internal benchmark) — check for common upstream sources
- Very Low does not mean "ignore" — a forum post may point to a real issue not yet documented officially; follow up

---

## Prompt 6: Bias Audit

**Version:** 1.0 — 2026-03-21
**Pattern Used:** Multi-Perspective Analyzer — view findings through each bias lens sequentially
**Recommended Model:** Claude Sonnet or Opus

### Full Prompt (embedded in Phase 7 of SKILL.md)

```
Systematically check for each bias type. State the result even when clean.

| Bias Type | Check | Result |
|-----------|-------|--------|
| Publication bias | Are negative results missing? | [Clean / Flag: ...] |
| Recency bias | Are older but valid sources excluded? | [Clean / Flag: ...] |
| Availability bias | Am I over-weighting easy-to-find sources? | [Clean / Flag: ...] |
| Confirmation bias | Have I sought disconfirming evidence? | [Clean / Flag: ...] |
| Researcher bias | Am I framing findings to match a prior? | [Clean / Flag: ...] |

When a bias is found, retroactively flag affected findings: [BIAS RISK: type]
```

### Design Rationale
The Multi-Perspective Analyzer pattern is applied by forcing sequential evaluation through each bias lens rather than a single holistic assessment. This prevents the most common failure: declaring "no bias found" without checking each type individually. Requiring a result even for clean checks prevents omission of the audit. Retroactive flagging in findings (rather than a separate "bias warning" section) keeps the evidence quality signal co-located with the claim it affects, where it will be seen when the finding is used.

### Usage Guidelines
- Run the full audit even for simple research tasks — the habit is more valuable than the time saved
- "Confirmation bias" check: ask explicitly "Did I search for evidence that contradicts my current synthesis?" — not just "do my sources agree?"
- "Researcher bias" is the hardest to self-detect — consider whether the initial question or framing reflected a preferred answer

### Example Input / Output
**Publication bias:** Searched for failure cases and negative benchmarks, not only success stories. Three sources reporting performance regressions were included (S3, S6, S8). — **Clean**

**Recency bias:** The foundational paper [S1, 2019] was included despite being older, because it establishes the theoretical model still referenced by current implementations. — **Clean**

**Availability bias:** Redis has significantly more documentation and community content than Valkey. Evidence count: Redis (8 sources), Valkey (3 sources). This reflects documentation maturity, not necessarily quality difference. — **Flag: Availability bias risk for Valkey comparison [BIAS RISK: availability]**

**Confirmation bias:** Initial hypothesis favored Redis. Actively searched for "Valkey advantages" and "Redis limitations" to counterbalance. Found 2 contradicting sources (S3, S9) that were incorporated. — **Clean**

**Researcher bias:** No strong prior stated at session start. — **Clean**

### Known Limitations
- Cannot detect bias in sources themselves (e.g., vendor-sponsored benchmarks) — the API research reference covers this separately
- Self-assessment of "researcher bias" is inherently limited; external review is the only reliable mitigation
- The five bias types listed do not cover all forms of cognitive bias — they cover the most common and most impactful for research tasks

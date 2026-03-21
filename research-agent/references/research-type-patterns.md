# Research Type Patterns

Quick-reference cheat sheet for research type identification, framework selection, and routing to the correct pattern.

---

## Research Type Identification Matrix

| Signal Words / Phrases | Research Type | Core Question Form |
|------------------------|---------------|-------------------|
| "How does", "How can", "How might", "Explore", "Discover", "What factors" | **Exploratory** | "How does X work / arise / unfold?" |
| "What is", "What are", "What exists", "Map", "Document", "Inventory", "Survey" | **Descriptive** | "What is the current state of X?" |
| "Why", "Root cause", "Because", "Caused by", "What led to", "Explain why" | **Explanatory** | "Why does X happen?" |
| "Did X work", "What was the impact", "Is X effective", "Worth it", "Evaluate", "Assess" | **Evaluative** | "Did/does X achieve its intended outcome?" |
| "Compare", "Which is better", "Alternatives", "Options", "vs.", "Trade-offs", "Choose between" | **Comparative** | "Which option best fits my needs?" |

**Disambiguation rule — Exploratory vs Comparative:**
If the user says "compare X to understand Y" where understanding Y is the goal (not choosing X), the type is **Exploratory**, not Comparative. Comparison is a method, not the purpose.

**Disambiguation rule — Descriptive vs Evaluative:**
If the user asks "what is the current adoption of X" (mapping a fact), it is Descriptive. If they ask "was X adoption successful" (judging merit), it is Evaluative.

---

## Framework Selection Guide

Apply a question framework after identifying the research type to sharpen the research question.

### PICO — Intervention / Outcome Questions

**Use when:** An action, treatment, technology, or policy is being evaluated against a measurable outcome.

**Signals:** Words like "does X result in", "impact of", "effect of", "if we use X"

**Components:**
- **P** — Population/Problem: Who or what is being studied
- **I** — Intervention: What action or technology is being evaluated
- **C** — Comparison: What alternative or baseline
- **O** — Outcome: What is measured

**Example:** "Does using Redis (I) for session storage in a Node.js app (P) compared to in-memory sessions (C) reduce latency under high load (O)?"

---

### SPICE — Qualitative / Experience / Context Questions

**Use when:** The research involves lived experience, context-specific understanding, or qualitative phenomena.

**Signals:** Words like "how do users experience", "from the perspective of", "in the context of", "what is it like to"

**Components:**
- **S** — Setting: Where does this occur
- **P** — Perspective: Whose viewpoint matters
- **I** — Intervention/Phenomenon: What is being examined
- **C** — Comparison: What else exists (optional)
- **E** — Evaluation: How success or experience is measured

**Example:** "In distributed engineering teams (S), from the perspective of senior engineers (P), how do async code review practices (I) compare to synchronous review (C) when evaluated by team velocity and developer satisfaction (E)?"

---

### PECO — Exposure / Effect Questions

**Use when:** A population is exposed to something (not actively choosing it) and the research asks about the resulting effect.

**Signals:** "exposed to", "impact of environment", "effect of dependency", "vulnerability to", technical exposure questions

**Components:**
- **P** — Population: Who is exposed
- **E** — Exposure: What they are exposed to (not chosen)
- **C** — Comparison: Unexposed group or baseline
- **O** — Outcome: What effect is measured

**Example:** "In JavaScript applications (P) exposed to a known prototype pollution vector (E) compared to applications using Object.freeze() (C), what is the attack surface reduction (O)?"

---

### No Framework (Open-Ended)

**Use when:** The question is early-stage Exploratory or a surface-level Descriptive scan. Do not force PICO/SPICE/PECO onto every question — misapplied frameworks add noise.

**Proceed by:** Decomposing the raw question into 3–5 sub-questions that guide the source plan.

---

## Depth Calibration Guide

| Depth Level | Source Count | Scope | When to Use |
|-------------|-------------|-------|-------------|
| **Surface scan** | 3–5 sources | Single dimension | Quick orientation; user needs a starting point, not a definitive answer |
| **Standard** | 8–15 sources | 3–5 dimensions | Most research tasks; working hypothesis is acceptable outcome |
| **Systematic** | 15+ sources | Exhaustive per protocol | High-stakes decisions; conflicting evidence; audit trail required |

**Default depth:** Standard. Escalate to Systematic when the user issues the `systematic` command or when triggers listed in `systematic-review.md` apply.

---

## Pattern Compatibility Table

Research types can be combined when the question spans multiple purposes:

| Primary Type | Compatible Secondary | When to Combine |
|---|---|---|
| Exploratory | Descriptive | Mapping an unfamiliar space before forming hypotheses |
| Explanatory | Evaluative | "Why did X fail, and was the fix effective?" |
| Evaluative | Systematic Review | High-stakes evaluation requiring exhaustive evidence |
| Comparative | Evaluative | "Which option is better, and by how much?" |
| Descriptive | Comparative | "What exists, and how do the options differ?" |

**Avoid combining:** Exploratory + Comparative — these have opposing premises. Exploratory assumes open-ended discovery; Comparative requires pre-defined options.

---

## 5 Worked Routing Examples

### Example 1 — Exploratory

**User question:** "How do distributed tracing systems handle context propagation across async boundaries?"

| Step | Decision |
|------|----------|
| Signal words | "How do", "handle" |
| Type | **Exploratory** |
| Framework | None (open-ended mechanism question) |
| Protocol | Standard |
| Output | Discovery Report |
| Pattern | Grounded Theory loop — map mechanisms, emerge themes, no pre-imposed categories |

---

### Example 2 — Descriptive

**User question:** "What observability tools are currently available for Kubernetes?"

| Step | Decision |
|------|----------|
| Signal words | "What... are", "currently available" |
| Type | **Descriptive** |
| Framework | None (landscape mapping) |
| Protocol | Surface scan (orientation) |
| Output | Landscape Map |
| Pattern | Entity inventory (tools), relationship map (integrations), state-of-field (mature/emerging/deprecated) |

---

### Example 3 — Explanatory

**User question:** "Why did our API latency spike after deploying the new auth middleware?"

| Step | Decision |
|------|----------|
| Signal words | "Why did", "spike after" |
| Type | **Explanatory** |
| Framework | PECO (middleware exposure → latency effect) |
| Protocol | Standard with RCA pattern |
| Output | Causal Analysis |
| Pattern | 5 Whys chain + Fishbone diagram (Process and Technology categories most relevant) |

---

### Example 4 — Evaluative

**User question:** "Did migrating to GraphQL reduce our frontend team's development cycle time?"

| Step | Decision |
|------|----------|
| Signal words | "Did... reduce", "cycle time" |
| Type | **Evaluative** |
| Framework | PICO (frontend teams / GraphQL / REST / development cycle time) |
| Protocol | Standard; escalate to Systematic if decision is high-stakes or evidence conflicts |
| Output | Impact Assessment |
| Pattern | Evidence summary table, outcome direction, risk of bias assessment |

---

### Example 5 — Comparative

**User question:** "Should we use PostgreSQL, MySQL, or DynamoDB for our new user-profile service?"

| Step | Decision |
|------|----------|
| Signal words | "Should we use", multiple options presented |
| Type | **Comparative** |
| Framework | None (option selection, not intervention evaluation) |
| Protocol | Standard |
| Output | Decision Matrix |
| Pattern | Criteria matrix (defined from stated constraints), SWOT per option, recommendation with risk trade-offs |
| Note | Elicit success criteria from user before gathering if not stated (latency? cost? operational complexity?) |

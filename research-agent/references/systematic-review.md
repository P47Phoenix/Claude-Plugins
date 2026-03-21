# Systematic Review Protocol

Reference guide for conducting systematic reviews. Use this protocol when the `systematic` command is issued or when research depth requires more rigor than a standard investigation.

## What Is a Systematic Review?

A systematic review answers a focused question by identifying, appraising, and synthesizing all relevant evidence according to a pre-specified, transparent methodology. It differs from:

| Type | Methodology | Reproducibility | Bias Control |
|------|-------------|-----------------|--------------|
| **Narrative review** | Ad hoc, author-discretion | Low | Minimal |
| **Standard investigation** | Structured but flexible | Medium | Moderate |
| **Systematic review** | Pre-specified protocol, exhaustive search | High | Rigorous |
| **Meta-analysis** | Systematic review + statistical pooling | High | Rigorous |

Use systematic review when: the question is high-stakes, evidence is conflicting, or a definitive answer is needed rather than a working hypothesis.

---

## 8-Step Systematic Review Protocol

### Step 1: Define the Question (PICO)

Formulate using the PICO framework before any searching begins. The question must be answerable — specific enough that you can determine what counts as relevant evidence.

```
P (Population/Problem): [Who or what is being studied]
I (Intervention/Exposure): [What action, technology, or phenomenon]
C (Comparison): [What alternative or control exists]
O (Outcome): [What is measured or expected to change]

Reformulated question: "In [P], does [I] compared to [C] result in [O]?"
```

Do not proceed to Step 2 until the PICO question is written explicitly.

### Step 2: Write Inclusion & Exclusion Criteria

Define before searching — not after seeing results. This is the primary guard against selection bias.

```
Inclusion criteria:
- Source types: [e.g., peer-reviewed papers, official documentation, benchmarks with methodology]
- Date range: [e.g., published 2020–present]
- Languages: [e.g., English only]
- Relevance: [must address P and I directly]
- Quality floor: [e.g., must include a methodology or reproducible result]

Exclusion criteria:
- [e.g., opinion pieces without supporting data]
- [e.g., sources older than 5 years for rapidly evolving technologies]
- [e.g., vendor-only sources with no independent validation]
```

### Step 3: Identify Search Sources

List all databases and locations to search. For technical research:

| Source Type | Examples |
|-------------|----------|
| Academic | arXiv, ACM Digital Library, IEEE Xplore, Google Scholar |
| Official docs | Product documentation, API references, release notes |
| Code | GitHub repositories, package registries (npm, PyPI) |
| Benchmarks | Published benchmark suites, performance reports |
| Community | Stack Overflow (tagged answers), GitHub Issues |
| Grey literature | Blog posts from core maintainers, conference talks |

### Step 4: Execute Searches & Record Search Strings

Record exact search strings used — this enables reproducibility and prevents unconscious manipulation of search terms based on early results.

```
Search log:
| # | Source | Search String | Date | Results Count | Included |
|---|--------|---------------|------|---------------|----------|
| 1 | arXiv  | "..." | 2026-03-21 | 47 | 3 |
| 2 | GitHub | "..." | 2026-03-21 | 12 | 2 |
```

### Step 5: Screen Results Against Inclusion Criteria

Two-pass screening:
1. **Title/abstract screen**: Exclude obviously irrelevant results
2. **Full-text screen**: Apply inclusion/exclusion criteria rigorously

For each excluded source, record the reason. This produces the PRISMA flow (see below).

### Step 6: Full-Text Review of Included Sources

For each included source, extract:
- Core claim or finding
- Methodology (how was this determined?)
- Sample size / scope
- Limitations stated by authors
- Potential conflicts of interest

Assign a source ID (S1, S2, ...) and GRADE level at this step.

### Step 7: Data Extraction Table

Standardize extraction to enable comparison:

```
| ID | Source | Year | Design | N/Scope | Key Finding | Outcome Direction | GRADE |
|----|--------|------|--------|---------|-------------|-------------------|-------|
| S1 | ...    | ...  | ...    | ...     | ...         | + / - / neutral   | ⊕⊕⊕◯ |
```

### Step 8: Quality Assessment & GRADE Rating

Assess each source independently before synthesizing. Apply the Risk of Bias framework (see below), then assign GRADE.

Final synthesis: summarize outcome direction across included sources, characterize heterogeneity (are results consistent or conflicting?), and assign an overall confidence level to the answer.

---

## Risk of Bias Categories

Adapted from Cochrane standards for technical and software research contexts:

| Bias Type | Description | Technical Research Signal | Mitigation |
|-----------|-------------|--------------------------|------------|
| **Selection bias** | Sources chosen because they support a preferred outcome | Criteria defined post-hoc; only vendor sources included | Pre-specify inclusion criteria; include community sources |
| **Performance bias** | The intervention was implemented differently across sources | Benchmark versions differ; test conditions inconsistent | Standardize to comparable conditions; flag version mismatches |
| **Detection bias** | Outcome measured differently across sources | Different metrics used; different measurement tools | Align on a single outcome metric before comparison |
| **Attrition bias** | Missing data or sources that dropped out | Failed benchmarks not reported; negative results absent | Actively seek null/negative results; note where missing |
| **Reporting bias** | Selective reporting of favorable outcomes | Only statistically significant results published | Check for grey literature and unpublished datasets |

Rate each bias type per source as: Low / Unclear / High.

---

## PRISMA-Inspired Flow

Track source counts through the screening process:

```
Records identified through database searches: [N]
         ↓
Records after removing duplicates: [N]
         ↓
Records screened (title/abstract): [N]
         ↓ excluded: [N] — reason: [not relevant to P/I/O]
Full-text articles assessed: [N]
         ↓ excluded: [N] — reasons: [list]
Studies included in synthesis: [N]
```

Document this flow in the output under "Source Selection".

---

## When to Escalate Standard → Systematic

Escalate from a standard investigation to full systematic review when ANY of the following apply:

| Trigger | Why It Matters |
|---------|---------------|
| Conflicting evidence across initial sources | Standard synthesis cannot resolve contradiction without exhaustive search |
| High-stakes decision (production architecture, security, compliance) | Cost of being wrong outweighs cost of thoroughness |
| User issues `systematic` command explicitly | Direct instruction |
| Initial findings show evidence gap (key question unanswered) | Need for structured search to confirm absence of evidence |
| Claim requires defensible audit trail | Systematic protocol creates reproducible record |

Systematic review adds approximately 3–5x the effort of a standard investigation. Confirm with the user before escalating if the trigger is ambiguous.

# constraints.yml — Authoring Canon

> Quick-start version: see [`constraints-quickstart.md`](constraints-quickstart.md).

## 1. What this file is (read first)

`constraints.yml` is the **Paired Constraints Primitive**: a small, stage-committed YAML file that carries rule-checkable constraints from Refine and Architect into Plan, Dev, and the DoD gates. It is the concrete vessel of the **Model-First paradigm** — the discipline of binding a stage's earned knowledge to an explicit, mechanically verifiable model *before* prose proliferates downstream (see *LLM Agents as Model-First Engineers*, arXiv:2512.14474). Without this file, constraints are known but not structured, and therefore not consumed. With it, the Business Rules Engine can enforce them deterministically at every stage gate.

## 2. File Locations

| Stage | Author | Canonical path |
|---|---|---|
| 2 Refine | Product Owner | `.delivery/artifacts/02-refine/po/constraints.yml` |
| 4 Architect | Solution Architect | `.delivery/artifacts/04-architect/solution/constraints.yml` |

A stage NEVER overwrites an upstream file. The Architect's file is a **sibling**, not an extension, of the Refine file. Both are consumed by downstream DoD validators.

## 3. Field Reference

| Field | Type | Required | One-line purpose |
|---|---|---|---|
| `entities` | list[string] | **yes** | Named domain nouns or bounded contexts locked at this stage. |
| `invariants` | list[string] | **yes** | Rule-checkable truths that must hold end-to-end. |
| `forbidden_vocabulary` | list[string] | no | Tokens that must not appear in this stage's prose artifacts. |
| `numeric_ceilings` | map[string→number] | no | Quantitative upper bounds (budgets, counts, ratios). |
| `state_variables` | list[string] | no | Observable state the pipeline mutates. |
| `actions` | list[string] | no | State transitions authored by this stage. |
| `mandatory_artifacts` | list[string] | no | Downstream file paths this stage promises will exist at DoD time. |
| `citations` | list[object] | no | Structured `{work, chapter, page}` references backing invariants. |

### 3.1 `entities` (required)
- **Purpose**: domain nouns (Refine) or bounded contexts / volatility classes (Architect).
- **Example**: `entities: [constraints_file, dod_validator, architect_agent]`
- **Common mistakes**: using implementation nouns (`lambda`, `sqs`) instead of domain terms; empty list (forbidden — schema requires ≥1 item).

### 3.2 `invariants` (required)
- **Purpose**: the load-bearing truths the stage commits to. Every invariant must be referenceable by a DoD rule.
- **Example**: `invariants: ["constraints.yml exists before stage DoD fires"]`
- **Common mistakes**: prose wishes ("code should be clean"); un-checkable aspirations; duplicating acceptance criteria verbatim.

### 3.3 `forbidden_vocabulary` (optional)
- **Purpose**: enumerated tokens the DoD grep-check rejects in this stage's artifacts. Restated per file (not inherited — see ADR-003).
- **Example**: `forbidden_vocabulary: [lambda, ecr, sqs, python, typescript]`
- **Common mistakes**: regex patterns (use literal tokens); relying on inheritance from the guide; omitting the list when the stage's prose does need the fence.

### 3.4 `numeric_ceilings` (optional)
- **Purpose**: hard quantitative limits the validator compares against.
- **Example**: `numeric_ceilings: {refine_token_delta_pct: 15, max_fields: 8}`
- **Common mistakes**: strings where numbers are required; units embedded in the value (`"15%"` instead of `15`).

### 3.5 `state_variables` (optional)
- **Purpose**: names of observable state the pipeline tracks — anchors for invariants about transitions.
- **Example**: `state_variables: [pipeline_stage, dod_result]`
- **Common mistakes**: confusing with `entities`; listing private implementation variables.

### 3.6 `actions` (optional)
- **Purpose**: the verbs / state transitions this stage authors or governs.
- **Example**: `actions: [author_constraints, run_dod_check]`
- **Common mistakes**: UI labels masquerading as actions; past-tense descriptions.

### 3.7 `mandatory_artifacts` (optional)
- **Purpose**: paths the stage guarantees exist at DoD time; validator asserts presence on disk.
- **Example**: `mandatory_artifacts: [".delivery/artifacts/04-architect/solution/constraints.yml"]`
- **Common mistakes**: relative paths from the wrong cwd; globs (not supported — list explicit paths).

### 3.8 `citations` (optional, but **required** for Architect volatility runs)
- **Purpose**: structured source attestations the validator can mechanically query.
- **Example**:
  ```yaml
  citations:
    - { work: "Righting Software", chapter: "2", page: "31" }
  ```
- **Common mistakes**: free-form prose ("per Löwy, vol. decomp..."); missing `page`; quoting chapter/page inconsistently.

## 4. Forbidden Vocabulary Canon (per ADR-003)

`forbidden_vocabulary` is an **enumerated literal list**, never a heuristic and never AI-judged. The canonical baseline — restated verbatim in any stage that opts in — is:

```
lambda, ecr, sqs, sns, dynamodb, kinesis, fargate, ec2,
python, typescript, javascript, golang, rust,
react, vue, angular, nextjs,
postgres, mysql, redis, kafka
```

Stages MAY extend this list; stages MAY NOT rely on inheritance. The DoD validator runs a case-insensitive whole-word grep over the stage's artifact set (`R-GREP`, see architecture §7). Any hit is a FAIL.

## 5. Löwy Golden Rule — `citations` Cross-Link

When a stage uses a **volatility-based decomposition strategy**, its `constraints.yml` MUST contain a `citations` entry referencing Löwy's *Righting Software*, Chapter 2. The DoD rule `R-CITATIONS` asserts:

```yaml
citations:
  - { work: "Righting Software", chapter: "2", page: "31" }
```

Absence → `FAIL — Löwy Golden Rule citation required for volatility decomposition`. See `delivery-team/skills/architect/references/volatility-decomposition.md` §0 for the rule statement and the functional-decomposition anti-pattern it guards against.

## 6. Authoring Workflow

1. **Refine (PO, Stage 2)** — copy `templates/constraints-refine.yml`, fill `entities` and `invariants` from the PRD, add `forbidden_vocabulary` and `numeric_ceilings` where commitments exist, commit alongside the PRD.
2. **Architect (Solution Architect, Stage 4)** — copy `templates/constraints-architect.yml`, fill `entities` as bounded contexts / volatility classes, restate `forbidden_vocabulary`, add the Löwy `citations` entry if using volatility decomposition, list `mandatory_artifacts` the decomposition promises.
3. **Plan / Dev / DoD** — read-only consumers. Do NOT edit upstream files; author a new sibling if a new stage needs its own constraints.

## 7. Validation Workflow

- **Schema**: `delivery-team/skills/delivery-flow/references/constraints-schema.json` (JSON Schema draft-07). Binds field names, types, required set, and citation object shape.
- **Runner**: `delivery-team/skills/delivery-flow/scripts/validate_constraints.py` loads the YAML, validates against the schema, then runs the enumerated DoD rules (`R-REQUIRED`, `R-GREP`, `R-ARTIFACTS`, `R-INVARIANTS-REF`, `R-CITATIONS`) per architecture §7.
- **Invocation**:
  ```bash
  python delivery-team/skills/delivery-flow/scripts/validate_constraints.py \
      .delivery/artifacts/04-architect/solution/constraints.yml
  ```
- **Gate contract**: one finding per rule per offender, no prose inference. BRE philosophy end to end.

---

*See also*: ADR-001 (schema lock), ADR-002 (Architect in Stage 5), ADR-003 (forbidden-vocab enumeration), architecture.md §3 (minimal example table).

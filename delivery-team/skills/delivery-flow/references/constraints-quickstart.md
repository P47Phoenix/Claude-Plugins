# constraints.yml — Quickstart

> *"I don't know half of you half as well as I should like; and I like less than half of you half as well as you deserve."* — but a good constraints file, now that I've come to know rather well. Let me show you.

This is the **user-facing quickstart**. If you just need to write a `constraints.yml` and prove it's valid, you're in the right place. For the full authoring canon (every field, every rule, every edge), see [`constraints-model-guide.md`](constraints-model-guide.md).

---

## 1. What is `constraints.yml`?

`constraints.yml` is a small, shared primitive that encodes a stage's commitments — entities, state, actions, invariants — as a **structured, rule-checkable** YAML file instead of prose. The Product Owner authors one at **Refine** (problem-scoped) and the Solution Architect authors another at **Architect** (decomposition-scoped). Downstream stages read them; the Definition-of-Done validator enforces them mechanically.

## 2. When you'll write one

One `constraints.yml` is authored **per pipeline run, per stage**:

- **Refine (Stage 2)** — the PO writes `.delivery/artifacts/02-refine/po/constraints.yml`
- **Architect (Stage 4)** — the Architect writes `.delivery/artifacts/04-architect/solution/constraints.yml`

The Architect file is a **sibling** of the Refine file — never an overwrite.

## 3. The 8 fields, briefly

| Field | Required | Purpose |
|---|---|---|
| `entities` | yes | Domain nouns (Refine) or bounded contexts / volatility classes (Architect) |
| `invariants` | yes | Rule-checkable truths the stage commits to |
| `forbidden_vocabulary` | no | Tokens banned from this stage's prose (ADR-003 enumerated list) |
| `numeric_ceilings` | no | Quantitative upper bounds (budgets, counts, ratios) |
| `state_variables` | no | Observable state the pipeline mutates |
| `actions` | no | State transitions this stage authors |
| `mandatory_artifacts` | no | Paths the stage promises will exist at DoD time |
| `citations` | no (required for volatility) | Structured `{work, chapter, page}` references |

Depth and edge cases: [`constraints-model-guide.md`](constraints-model-guide.md).

## 4. Minimal example (Refine stage)

A valid, minimum-viable Refine `constraints.yml` — paste this, it validates:

```yaml
entities:
  - Customer
  - Order
  - Invoice
invariants:
  - Every Order must reference a known Customer
  - Invoices are emitted only for paid Orders
mandatory_artifacts:
  - .delivery/artifacts/02-refine/po/prd.md
```

Only `entities` and `invariants` are required; everything else is optional. Add `numeric_ceilings`, `state_variables`, `actions`, `forbidden_vocabulary`, or `citations` when your PRD commits to them.

## 5. Templates

Don't start from a blank file. Copy one of:

- [`templates/constraints-refine.yml`](templates/constraints-refine.yml) — PO template, pre-commented
- [`templates/constraints-architect.yml`](templates/constraints-architect.yml) — Architect template, pre-populated with the forbidden-vocabulary baseline

## 6. Validate it

From the repo root:

```bash
python3 delivery-team/skills/delivery-flow/scripts/validate_constraints.py \
    .delivery/artifacts/02-refine/po/constraints.yml
```

- **Exit 0** → `ok: <path> is valid against constraints schema`
- **Exit 1** → one finding per rule per offender, like so:

```
error: .delivery/artifacts/02-refine/po/constraints.yml is INVALID against constraints schema:
  - missing required field: entities
  - invariants must be a non-empty list of non-empty strings
  - citations[0] missing required key: page
```

No prose inference, no AI variance — the validator is deterministic.

## 7. Forbidden vocabulary (Architect stage only)

At **decomposition**, your `constraints.yml` must not smuggle implementation detail into the decomposition — no cloud service names (Lambda, Kubernetes, Dynamo), no language names (Python, TypeScript, Go), no framework names (React, Django). Declare the banned tokens in `forbidden_vocabulary`; the Architect template pre-populates a sensible baseline. The DoD checker (`check_dod_constraints.py`) runs a case-insensitive whole-word grep over stage artifacts and fails on any hit.

Refine-stage `forbidden_vocabulary` is about **business** vocabulary hygiene (deprecated product names, ambiguous synonyms), not implementation tokens.

## 8. Common mistakes

1. **Missing required fields.** Both `entities` and `invariants` must be non-empty lists of non-empty strings. An empty list fails.
2. **Citations as prose.** `"per Löwy, ch 2"` is wrong. Use structured objects: `{ work: "Righting Software", chapter: "2", page: "31" }` — `work`, `chapter`, and `page` are all required keys.
3. **Forbidden tokens used in invariants or actions.** If you name `lambda` inside an invariant string at the Architect stage, the DoD grep will catch it. Declare the token in `forbidden_vocabulary` *and* keep it out of your prose.
4. **Wrong canonical path.** Refine goes to `.delivery/artifacts/02-refine/po/constraints.yml`; Architect goes to `.delivery/artifacts/04-architect/solution/constraints.yml`. Anywhere else and downstream validators won't find it.
5. **Overwriting upstream.** A later stage never edits an earlier stage's file. Author a sibling instead.

## 9. See also

- [`constraints-model-guide.md`](constraints-model-guide.md) — full authoring canon, every field, every DoD rule
- `delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py` — DoD gate enforcement (forbidden-vocab grep, citation rules, artifact presence)
- `delivery-team/skills/delivery-flow/references/constraints-schema.json` — JSON Schema (the validator's source of truth)
- ADR-001 (schema lock), ADR-003 (forbidden-vocabulary enumeration) — rationale and change protocol

---

> *"It's a dangerous business, Frodo, going out your door. You step onto the road, and if you don't keep your feet, there's no knowing where you might be swept off to."* Keep the two required fields. Keep the path canonical. Run the validator. The road stays under your feet.

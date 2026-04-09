# How to Author a `constraints.yml`

**Author**: Bilbo Baggins (Technical Writer) | **Date**: 2026-04-08

> *"It's the job that's never started as takes longest to finish — so let us start the YAML."*

A short chapter, hobbit-sized, on how to write the little primitive that now keeps our pipeline honest.

## Quick Start

```yaml
# .delivery/artifacts/<stage>/<role>/constraints.yml
entities:
  - "delivery-flow pipeline"
  - "constraints.yml primitive"
invariants:
  - "Decompose by volatility, not by functionality (Löwy)"
  - "No implementation nouns in decomposition artifacts"
```

Two fields, `entities` and `invariants`, are all you strictly need. Add the other six as the burden of your stage requires. Save the file, then run the validator (see below). That is the whole of it.

## When to Author

- **Refine (PO, Gandalf)** — write a problem-scoped `constraints.yml` alongside your PRD. Entities are domain nouns; invariants are ADR-level truths.
- **Architect (Celebrimbor)** — write a decomposition-scoped `constraints.yml` alongside your architecture document. Entities are subsystems / bounded contexts; `forbidden_vocabulary` and Löwy `citations` are mandatory when volatility strategy is selected.

## The Eight Fields

| Field | Required | One-line meaning |
|---|---|---|
| `entities` | yes | Domain nouns or subsystems under discussion. |
| `invariants` | yes | Truths that must hold across the stage's output. |
| `state_variables` | no | Observable state the stage commits to or classifies. |
| `actions` | no | State transitions the stage authors or permits. |
| `numeric_ceilings` | no | Caps (sprint, token, latency) the stage must honor. |
| `mandatory_artifacts` | no | Downstream files the stage requires to exist. |
| `forbidden_vocabulary` | no | Enumerated tokens banned from stage artifacts. |
| `citations` | no | `{work, chapter, page}` references backing invariants. |

## Validate It

```
python3 delivery-team/skills/delivery-flow/scripts/validate_constraints.py <path-to-constraints.yml>
```

Exit 0 means your YAML is well-formed and required fields are present. Exit 1 prints a clear stderr message naming the missing or malformed field. Unknown fields are allowed (forward-compat, AC-1.4).

## How the DoD Checker Uses It

```
python3 delivery-team/skills/delivery-flow/scripts/check_dod_constraints.py <constraints.yml> <artifact>
```

The DoD checker runs deterministic, rule-based checks against your artifact: forbidden-vocabulary grep, mandatory-artifact presence, numeric-ceiling compliance. No AI inference — the Business Rules Engine philosophy holds. A failing check blocks the gate.

## Common Mistakes

- Writing prose in `invariants` that names AWS services or language runtimes. If it belongs in `forbidden_vocabulary`, it does not belong in an invariant.
- Leaving `entities` empty "because it's obvious." The validator will reject you; the reader will thank the validator.
- Mixing Refine and Architect concerns in one file. Each stage authors its own.
- Adding `forbidden_vocabulary` tokens by feel. Keep it enumerated; extensions go through PRD revision.
- Forgetting the Löwy citation on volatility-strategy runs. The DoD will fail closed.

## Further Reading

For the full schema, field semantics, and extension protocol, see `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`.

> *"Go now, and may the validator exit zero upon your path."*

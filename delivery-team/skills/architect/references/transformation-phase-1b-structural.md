# Transformation Phase 1B — Structural Reconstruction (Architect-led)

*By Gimli son of Glóin. Aye — once the why is cited, the stonework can be drawn true.*

## 1. Purpose

Phase 1B builds the **Model-First AS-IS** explicit model of a legacy system. It is **Architect-led**. The output is a structural description of the system as it exists today — entities, state, actions, and constraints — expressed in the shared BACKLOG-001 `constraints.yml` schema.

Phase 1B is purely **descriptive**. No recommendations. No "should". No desired-state labels. That is Phase 2's job.

## 2. Input

The canonical input is the Phase 1A artifact on disk:

`.delivery/artifacts/08-transform/as-is-use-cases.md`

Without this file, Phase 1B is flying blind. A structural model built without behavioral grounding is *a map of unknown territory*: the modules and coupling topology may be accurate, but the Architect cannot tell which subsystems matter, which are load-bearing for real user flows, and which are dead weight. **Phase 1B MUST NOT start without Phase 1A on disk.**

## 3. Model-First mapping

Phase 1A use cases and direct codebase inspection map into `constraints.yml` fields as follows:

| From Phase 1A / codebase | Into `constraints.yml` | Notes |
|---|---|---|
| Use-case `actor` | `entities` (domain actors) | One entity per distinct actor; merge duplicates. |
| Use-case `main_flow` steps + `variations` | `actions` | Each action's name and signature SHOULD match a use-case step; cite the 1A use-case id in the action description. |
| Use-case `preconditions` | `state_variables` | Each precondition names a state variable the system tracks. |
| Implicit rules inferred from evidence | `invariants` + `constraints` | Rules the code enforces today, even if undocumented (e.g., "order cannot ship before payment"). Cite the evidence file. |
| Current subsystems from code inspection | `entities` (technical entities) | Services, modules, packages — the units of deployment or isolation the codebase actually has. |
| Coupling map (imports, calls, shared DB tables) | `state` (current coupling topology) | A machine-readable description of who talks to whom today. |

Every `actions` entry MUST trace back to a Phase 1A use-case id. Orphan actions are a red flag: either Phase 1A is incomplete, or the action is infrastructure that does not belong in the behavioral-backed model.

## 4. Output

`.delivery/artifacts/08-transform/as-is-constraints.yml`

- Conforms to the shared BACKLOG-001 `constraints.yml` schema.
- Validates via `validate_constraints.py` — exit code 0 is a gate.
- Header comment MUST cite the Phase 1A artifact path and the run id.

## 5. Honest volatility classification

For every subsystem in the `entities` block, the Architect records its **observed** volatility — empirically, from commit history on that subsystem's path (e.g., `git log --oneline -- path/`). Use coarse buckets:

- **high** — churns every week or multiple commits per sprint.
- **medium** — steady background changes, a few per month.
- **low** — quiet for months or longer.

This is **observed** volatility, not **desired** volatility. "We wish this module didn't change so much" is a Phase 2 statement. If the Architect finds themselves arguing about what volatility a subsystem *ought* to have, they are already past the Phase 1B boundary — stop, write that thought into a Phase 2 scratch note, and return to describing what is.

## 6. Pairing rule

Phase 1B REQUIRES the Phase 1A output file to exist on disk at the canonical path. The Architect:

1. **Reads** the use-cases file directly. Does not receive it via in-memory handoff. Does not re-invent the use cases.
2. **References** specific use-case ids when populating `actions`.
3. **Blocks** the phase if the Phase 1A file is missing, stubbed, or failed its MAR review — the orchestrator MUST NOT advance.

File-based handoff (the two-channel rule) is deliberate: it keeps the PO and Architect phases independently auditable and prevents live coupling between the two skills.

## 7. Anti-patterns

- **Structural model that does not reference 1A use cases** — `actions` without use-case citations means the Architect worked from imagination, not evidence.
- **Desired-state volatility labels** — "this *should* be low volatility" belongs in TO-BE, not AS-IS.
- **Leaking into recommendation** — any sentence containing "we should", "ideally", "the target is", or "this would be better as…" is Phase 2 contamination.
- **Skipping Phase 1A** — starting 1B without the use-cases file. Fail the phase; do not pass go.
- **Module-diagram-only AS-IS** — a boxes-and-arrows picture with no `actions` or `constraints` fields populated is not a model, it is wallpaper.

*"Describe the stone as it lies. The reshaping comes in the next chapter."* — Gimli

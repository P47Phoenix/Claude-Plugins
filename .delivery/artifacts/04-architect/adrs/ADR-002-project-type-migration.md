# ADR-002: `project_type` Migration Strategy (v2.6 → v2.7)

**Status**: Accepted (LIGHT Architect stage)
**Date**: 2026-04-05
**Architect**: Celebrimbor
**Related**: PRD FR-01, FR-02, FR-03, FR-05, NFR-03, C1

---

## Context

Schema v2.6 treats `project_type` as a top-level config key that freezes routing decisions at repo setup time. Issue #73 requires removing this from active config and running Phase 1 detection every invocation. The challenge (C1) correctly pointed out that some users may have pinned `project_type` intentionally — for example, a docs-only repo that should never trigger code stages. Silently dropping their pin is a behavior break regardless of whether the YAML parses.

Three migration strategies were considered:

- **A. Silent drop**: Parse v2.6 configs, ignore `project_type`, do not log. Simplest, but behavior-breaks pinned users.
- **B. Warn-and-drop + opt-in override**: Parse, ignore for routing, emit deprecation banner, offer `routing.force_type:` as the intentional-pin replacement. (The PRD's position in FR-02.)
- **C. Preserve as deprecated alias**: Treat bare `project_type` as an intentional pin with a deprecation warning. Preserves legacy user intent at the cost of leaving the v2.6 footgun armed.

## Decision

Adopt **Option B — warn-and-drop with `routing.force_type` opt-in override**.

Behavior matrix:

| Config state | schema_version | Routing driver |
|---|---|---|
| v2.6 with bare `project_type: GREENFIELD` | 2.6 | Phase 1 detection. Legacy key logged as deprecated in stage banner + state.md run log. |
| v2.7, no `project_type`, no `routing.force_type` | 2.7 | Phase 1 detection every run. |
| v2.7 with `routing.force_type: DOCS_ONLY` | 2.7 | `routing.force_type`. Phase 1 runs and is logged, but routing uses the pin. Banner announces the pin. |
| v2.7 with both bare `project_type` and `routing.force_type` | 2.7 | `routing.force_type` wins. Bare `project_type` logged as deprecated. |

Additionally:

- `routing.force_type` is intentionally namespaced under `routing.` (not top level) so the pin is a deliberate, discoverable act — not a footgun hiding at the root.
- Deprecation log line appears in BOTH the orchestrator's stage banner AND `.delivery/state.md` (resolves OQ-3 in the direction of "both").
- `config-schema.md` gains a "Deprecated keys" section with a one-line migration recipe: *"If you previously pinned `project_type: X`, set `routing.force_type: X` instead."*
- No migration tool. Tolerant parse + deprecation banner is the migration.

## Alternatives considered

- **A (silent drop)**: Rejected. C1's pinned-user case is real. Silent behavior change destroys trust and is indistinguishable from a bug from the user's perspective.
- **C (preserve as alias)**: Rejected. Keeping bare `project_type` as a working pin re-arms the v2.6 footgun (frozen routing across requests). The whole point of issue #73 is to kill frozen routing. A working alias would only delay the problem.
- **Hard error on legacy configs**: Rejected. NFR-03 requires v2.6 configs to load without error. Users must not be stopped at the gate by a schema bump for a discipline fix.

## Consequences

**Positive**
- NFR-03 backwards compatibility is honored at the parser level.
- Pinned users are told their pin is being ignored (no silent behavior change).
- `routing.force_type` gives legitimate pin use cases (docs-only repos, locked-down specialty repos) a clean path.
- The v2.6 footgun is killed — bare `project_type` no longer steers routing under any schema version.

**Negative**
- Users who relied on pinned `project_type` must migrate to `routing.force_type` within one run to restore their intended behavior. Documented in the banner and changelog, but still friction.
- Two keys (legacy bare `project_type` and new `routing.force_type`) must be documented and supported in the parser. Minor complexity.
- Deprecation banner adds one line to stage output for legacy configs. Acceptable noise.

**Mitigation**
- Changelog entry in `config-schema.md` calls out the migration prominently.
- README.md and CLAUDE.md references updated in the same PR (doc parity DoD).
- Quality stage validates: v2.6 legacy fixture parses and runs; v2.7 `routing.force_type` overrides Phase 1; both-present case resolves to `routing.force_type`.

## Compliance

- FR-01, FR-02, FR-03, FR-05: satisfied.
- NFR-03 (backwards compat): satisfied.
- C1 (pinned-user blast radius): resolved via `routing.force_type` + warn-and-drop.
- OQ-3 (deprecation log location): resolved (both banner and state.md).

---

*"A key that has been turned should not be pulled from the lock without telling its owner what door it opened."*

— Celebrimbor

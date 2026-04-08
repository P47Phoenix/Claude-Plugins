# ADR-001: Origin Detection Mechanism for `enforce_pipeline_scope.py`

**Status**: Accepted (LIGHT Architect stage)
**Date**: 2026-04-05
**Architect**: Celebrimbor
**Related**: PRD FR-09, OQ-1, R6, C3

---

## Context

FR-09 requires `enforce_pipeline_scope.py` (a PreToolUse hook) to deny writes to `.delivery/artifacts/**` and configured source scope when the write is **orchestrator-originated**, but allow the same writes when **sub-agent-originated**. PreToolUse hooks do not receive a first-class "who is calling" field distinguishing the top-level Claude session from a dispatched Agent tool sub-session.

The PRD surfaced this as OQ-1 and R6 and pre-resolved it in FR-09 with a layered strategy. This ADR locks that strategy as the committed architectural decision and names the fallback behavior.

Three mechanisms were considered:

- **A. Environment variable injected on sub-agent dispatch.** Orchestrator sets `DELIVERY_FLOW_AGENT_CONTEXT=<role>` before invoking Agent tool; sub-agent process tree inherits it.
- **B. Hook input metadata inspection.** Parse stdin JSON for `transcript_path`, `session_id`, or `parent_tool_use_id` patterns that distinguish parent vs child frames.
- **C. Tool-call depth / stack inspection.** Count active Agent tool frames by parsing the transcript. Brittle and version-sensitive.
- **D. Routing metadata allowlist only.** Allow writes to `state.md`, etc., and deny everything else under `.delivery/artifacts/**` regardless of origin. Fails the "sub-agents must write artifacts" requirement.

## Decision

Adopt a **layered strategy**: A (primary) → B (secondary) → soft-deny warning fallback.

1. **Layer 1 — Env var**: `DELIVERY_FLOW_AGENT_CONTEXT` set on every sub-agent dispatch by the orchestrator. Presence ⇒ sub-agent ⇒ allow. Absence ⇒ candidate orchestrator, fall through.
2. **Layer 2 — Hook input metadata**: inspect `read_hook_input()` for sub-agent frame indicators (`parent_tool_use_id` or equivalent). Positive identification ⇒ allow. Inconclusive ⇒ fall through.
3. **Layer 3 — Soft-deny warning**: if neither signal resolves, emit a loud `systemMessage` naming the Delegation Prime Directive and target path. Do NOT deny. NFR-05 (never break a user pipeline) wins over FR-09 strictness when the mechanism itself is uncertain.

Additionally:

- **Allowlist** (always allow regardless of origin): `.delivery/state.md`, `.delivery/config.yml`, `.delivery/memory/**`, `.delivery/artifacts/*/state/**`, `.delivery/artifacts/*/handoff/**`. Centralized as a single module-level constant.
- **Bash coverage**: hook also fires on `Bash`, with a regex detector for write-redirection patterns (`>`, `>>`, `tee`, `cat <<EOF`, `dd of=`, `cp`/`mv` into artifact paths) to close the heredoc bypass.
- **Activation gating**: deny behavior requires `schema_version >= 2.7` AND `pipeline.enforce_self_write_block: true`. Default is `true` for fresh v2.7 configs, `false` when tolerantly-parsing a v2.6 config. This makes the dogfood run forward-looking, not self-referential (closes R7).
- All new logic stays inside the existing `try/except → sys.exit(0)` wrapper. Stdlib only.

## Alternatives considered

- **A alone**: Rejected. If the harness ever strips env vars across the dispatch boundary, every orchestrator-origin write would be allowed — and every sub-agent-origin write would be denied. Single point of failure.
- **B alone**: Rejected. Hook input shape is harness-version-dependent and under-documented; cannot be load-bearing.
- **C (stack inspection)**: Rejected. Parsing transcripts from inside a hook is slow, brittle, and couples the hook to transcript format changes.
- **D (allowlist only, no origin detection)**: Rejected. Sub-agents legitimately must write artifacts to `.delivery/artifacts/**`. A blanket deny would break the pipeline outright.
- **Hard-deny when origin uncertain**: Rejected. Violates NFR-05. A buggy detector would brick user pipelines and destroy trust in the entire hook system.

## Consequences

**Positive**
- Deterministic primary mechanism (env var) with no runtime cost.
- Graceful degradation path preserves NFR-05.
- Activation gating allows this bundle to ship through delivery-flow without self-referential deadlock.
- Bash-redirection coverage closes the trivial bypass.
- Allowlist is explicit and cannot drift.

**Negative**
- Requires the orchestrator to reliably inject the env var on every dispatch. A missed dispatch site would silently fall to Layer 3 (warn, not deny), which is a correctness hole that may go undetected unless audited.
- Layer 2 implementation details depend on harness version; Plan stage must verify (PQ-1).
- Soft-deny fallback means under detector failure the hook offers warning-only protection. This is intentional but should be monitored.

**Mitigation**
- Development stage must centralize sub-agent dispatch so env var injection is done in exactly one place.
- Quality stage test matrix must include: env var present, env var absent + Layer 2 positive, both signals absent, and Bash-heredoc with each combination.
- Known-gaps list lives in the hook module docstring AND in `quality-gates.md` so they stay visible.

## Compliance

- FR-09 (a–e): satisfied.
- NFR-01 (≤50ms p95): satisfied; all ops are O(1) dict/string plus one regex pass on Bash commands.
- NFR-02 (stdlib-only): satisfied.
- NFR-05 (graceful degradation): satisfied via Layer 3 soft-deny.
- R6 (detection unreliability): mitigated by layered fallback.
- R7 (dogfood paradox): mitigated by activation gating.

---

*"A blade must know whose hand grips it. If it cannot tell, it must hesitate before it cuts."*

— Celebrimbor

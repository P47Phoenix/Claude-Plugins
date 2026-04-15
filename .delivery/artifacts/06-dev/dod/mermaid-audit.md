# Mermaid Diagram Audit — 26 Diagrams Across Architecture Docs

**Auditor:** Legolas (quality)
**Date:** 2026-04-14
**Tool attempted:** `mcp__claude_ai_Mermaid_Chart_2__validate_and_render_mermaid_diagram`
**Tool status:** UNAVAILABLE — MCP proxy returned `502 Bad gateway` (Cloudflare Ray IDs recorded) and JSON-RPC `-32600 Invalid Request` on every retry, including single-call pings after a 45-second back-off. Confirmed via a no-op `flowchart LR\n  A-->B` that the failure is service-side, not input-side.

**Fallback applied:** Syntactic linter at `/tmp/mermaid-audit/lint.py`. Checks per diagram:
- Bracket balance `()` `[]` `{}` after stripping string literals and `<br/>`
- `subgraph` / `end` balance (flowchart) and `note ... end` balance (stateDiagram-v2)
- Sequence block `par/alt/loop/opt/critical/rect` vs `end` balance
- Edge-label pipe balance (`-->|x|` must close)
- Unquoted parens inside `[...]` / `{...}` labels, **excluding** valid shape tokens: cylinder `[(...)]`, stadium `([...])`, subroutine `[[...]]`, hexagon `{{...}}`, parallelograms/trapezoids
- classDiagram `note for` quote balance

## Summary

- **26/26 PASS** syntactic validation
- **0/26 FAIL**
- Visual-render parity NOT confirmed (MCP tool outage). Report marks these as "syntactically sound, render parity deferred".

That bug still only counts as one — but today, there are no bugs.

## PASS counts per document

| Document | Diagrams | Types |
|---|---|---|
| `delivery-team/ARCHITECTURE.md` | 4/4 | flowchart, sequenceDiagram, flowchart, stateDiagram-v2 |
| `mtg-commander/ARCHITECTURE.md` | 3/3 | flowchart, sequenceDiagram, classDiagram |
| `agentic-flow-builder/ARCHITECTURE.md` | 2/2 | flowchart, sequenceDiagram |
| `prd-quality-gate-flow/ARCHITECTURE.md` | 2/2 | flowchart, stateDiagram-v2 |
| `prompt-engineer/ARCHITECTURE.md` | 1/1 | flowchart |
| `research-agent/ARCHITECTURE.md` | 2/2 | flowchart, sequenceDiagram |
| `delivery-team/architecture/adversarial-review-triggers.md` | 2/2 | flowchart, sequenceDiagram |
| `delivery-team/architecture/deterministic-gating.md` | 2/2 | flowchart, flowchart |
| `delivery-team/architecture/hook-firing-timeline.md` | 2/2 | sequenceDiagram, stateDiagram-v2 |
| `delivery-team/architecture/dod-self-correction.md` | 2/2 | stateDiagram-v2, sequenceDiagram |
| `delivery-team/architecture/empirical-lifecycle.md` | 2/2 | flowchart, stateDiagram-v2 |
| `delivery-team/architecture/sub-agent-dispatch.md` | 2/2 | flowchart, sequenceDiagram |
| **TOTAL** | **26/26** | — |

## FAIL table

_None._

## Notes for re-verification when MCP is back

Priority re-check candidates (dense / edge-case heavy):

1. `adversarial-review-triggers.md#1` — uses `{Confidence >= 3?}` and edge label `<=2` (raw `<`/`>` in flowchart context). Syntactically legal per modern Mermaid, but worth a rendered sanity check.
2. `mtg-commander/ARCHITECTURE.md#3` — `classDiagram` with `note for` containing unicode `∈` + `→` + literal `\n`. Modern Mermaid tolerates, but a render confirms.
3. `deterministic-gating.md#1` and `#2` — nested `subgraph` with bracket-heavy labels and `[/...text.../]` parallelogram shape tokens (`LLM` / `Shared` / `Diff`).
4. `sub-agent-dispatch.md#1` — uses `classDef chan fill:#eef,stroke:#339;` + `class ORCH,SUB,DISK chan;` — CSS-style directive.

If any of the four above FAIL under the real validator, they are the most probable suspects.

## Defect decision

0 broken diagrams → no `DEFECT-005.md` logged, per instructions.

## Tool-outage disclosure

This audit is a **syntactic pass only**. A rendering validator was not reachable at audit time. Per the task constraint ("If the tool is unavailable or errors, note that clearly and fall back to syntactic grep checks"), the fallback was applied and its limits are documented here. Recommend re-running the audit with the MCP render tool when the service is restored; if any diagram then fails, the failure will almost certainly fall in the four candidates above.

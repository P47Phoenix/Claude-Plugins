<!-- run: run-2026-05-13-tk5 -->
# Architect DoD Review — Stage 1 Idea

**Reviewer**: Celebrimbor, master craftsman (Architect — Solution role)
**Pipeline**: run-2026-05-13-tk5
**Artifact under review**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Date**: 2026-05-13
**Task type**: dod-validation
**Recommended model**: sonnet

> *"Let us forge something that will endure beyond the ages."*

---

## Verdict Summary

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Buildable (no exotic deps) | **PASS** |
| 2 | No obvious blockers at integration points | **PASS** |
| 3 | Reuse boundaries correct (telemetry files exist) | **PASS** |
| 4 | Scope sized for FEATURE (not GREENFIELD/SPIKE) | **PASS** |
| 5 | Local-only-no-CI recorded as constraint, not goal | **PASS** |

**Overall gate**: **PASS — DONE**. Me see no architectural blockers. Probe is feasible work, sized right, reuse map is sound.

---

## Per-Criterion Findings

### Criterion 1 — Buildable: PASS

Scope is plain Python tools, no exotic stones:
- `lib/runner.py` — subprocess wrapper around `claude` CLI (stdlib `subprocess` + env override; well-trodden ground).
- `lib/metrics.py` — line-buffered JSON parser over stream-json (stdlib `json` + iterators).
- `lib/aggregator.py` — reads existing `.delivery/telemetry/skill-loads.jsonl` (newline-delimited JSON; stdlib only).
- `lib/baseline.py` — mean+stddev across 5 samples (stdlib `statistics`).
- `tests/test_meta.py` — pytest only; no Claude calls (producer/validator separation enforced).

Nothing here demands new dependency management or unusual runtime. All deps fit the repo's existing Python diet.

### Criterion 2 — No obvious blockers: PASS

Three integration points all plausible against existing repo surface:
- **Claude Code stream-json output** — runner invokes `claude --output-format stream-json`; consumer parses NDJSON. Standard CLI pattern; no novel protocol.
- **telemetry.jsonl reader** — `delivery-team/hooks/telemetry.py` already writes `.delivery/telemetry/skill-loads.jsonl` per the brief's claim; aggregator just reads what producer already emits. Re-verified file presence below.
- **Plugin loading via `--plugin-dir` / `HOME` override** — brief acknowledges semantic uncertainty and bakes a capability-probe at startup (primary: `HOME=<fake>` + `--plugin-dir <repo>/delivery-team`; fallback: copy plugin into `<fake-home>/.claude/plugins/delivery-team/`). Risk surfaced + mitigated; not a blocker.

Memory lesson applied (`hw01 adversarial`, confidence 2/5): cross-plugin invocation could bite. Brief defangs this with capability-probe up front rather than discover-at-runtime. Good craft.

### Criterion 3 — Reuse boundaries correct: PASS (verified by file probe)

Me run the command, not read about it:

```
-rw-r--r--. 1 meconnelly meconnelly 5604 May  9 13:39 delivery-team/hooks/telemetry.py
-rw-r--r--. 1 meconnelly meconnelly 4724 May  9 13:39 delivery-team/hooks/telemetry_run_summary.py
```

Both stones present on the bench. Reuse map in brief (telemetry.py read directly; telemetry_run_summary.py as fallback) is grounded in real artifacts, not assumed surface. Mirror-shape directive for `governance/skill-budgets.json` and the `scripts/check_skill_budgets.py` exit-code convention is also concrete reuse, not hand-wave.

### Criterion 4 — Scope sized for FEATURE: PASS

- **8 work items** (W6-1 through W6-8) — within FEATURE band; not the 15+ that signals GREENFIELD, not the 1-3 of a SPIKE.
- **Effort mix**: 4×M + 4×S. Me count batches with discipline (architect batching math):
  - 4 M @ ~1 dev-day = 4 dev-days
  - 4 S @ ~0.5 dev-day = 2 dev-days
  - Cross-cutting architecture doc adds ~0.5 dev-day
  - **Total ≈ 6.5 dev-days** — squarely in FEATURE range.
- No L items, no XL items, no items requiring greenfield bootstrap. Builds on existing telemetry surface (Reuse, not Reinvent).
- Single initiative routed through delivery-flow (constraint: "Route through delivery-flow") rather than fragmented across PRs — appropriate for FEATURE classification.

Not a SPIKE: deliverables are durable artifacts (probe, baseline, regression diff, meta-tests, architecture doc), not learning notes.
Not a GREENFIELD: builds on existing plugin + existing telemetry hooks; doesn't bootstrap a new domain.

### Criterion 5 — Local-only is constraint, not goal: PASS

Brief separates concerns cleanly:
- **Constraints section** (line 26) explicitly lists `LOCAL-ONLY (binding)` with citation to the memory file. Phrased as *bounding* the design: "Tooling that shells out to `claude` MUST NOT live in `.github/workflows/`." No-bypass-with-ADR clause makes it architecturally binding.
- **Goals section** (lines 21-23) does NOT name local-only as a deliverable. Goal 3 states "0 GitHub Actions workflows invoke `claude`" — this is an *enforcement assertion* (verifiable absence) wrapped around the constraint, not the constraint itself. The deliverable in Goal 3 is the documented constraint in `delivery-team/architecture/smoke-test-architecture.md` with memory-file pointer.
- **Out of Scope** (line 45) restates the CI ban as scope exclusion, reinforcing it as a boundary rather than a feature.

Constraint shapes the design (forces local-only runner architecture, forbids CI surface) without becoming an output artifact masquerading as a goal. Correct framing.

---

## Trade-offs Noted (informational, no blocker)

- **Producer-validator separation as social constraint**: brief states meta-test fixtures CANNOT share author with `lib/metrics.py`. This is a team-process constraint, not an architectural one — architecture cannot enforce it; relies on PR review discipline. Worth flagging to PO for Plan-stage acceptance criteria, but does not block Stage 1.
- **5-sample baseline variance budget**: brief acknowledges (Open Risks #4) that 5 samples may underestimate true variance; first-month advisory-only on `tokens.*` and `skill_loads.*` is the right hedge. Bake the "tighten after 20+ runs" rule into the regression detector config so it not lost.

---

## Assumptions

- Existing telemetry producer (`telemetry.py`) emits the schema the aggregator expects without changes (brief asserts "zero changes" — Developer DoD will verify by running, not reading).
- `claude` CLI honors `--plugin-dir` or `HOME=<fake>` as the brief assumes; capability-probe handles either outcome.
- `stream-json` output format remains stable across `claude_cli_version` (worth pinning + recording in `report.json`, which brief already does via `claude_cli_version` field).

## Risks (architect-flagged, beyond PO's list)

- **None blocking**. PO already surfaced the four sharp risks (prompt drift, `--plugin-dir` semantics, Stop hook, variance budget). No architectural risk PO missed.

## Open Questions

- None blocking Stage 1 gate. `delivery-team/architecture/smoke-test-architecture.md` (cross-cutting item) is the appropriate vessel for Stage 3 Design decisions (Mermaid diagram, capability-probe state machine, baseline-shape decision).

---

## Gate Decision

**PASS — Stage 1 Idea DoD met from Architect lens.** Probe is buildable, integration points sound, reuse map verified against real files on disk, scope properly sized as FEATURE, local-only correctly framed as binding constraint.

Forward to Stage 2 Refine.

— Celebrimbor, master craftsman. *The work endures because the boundaries are true.*

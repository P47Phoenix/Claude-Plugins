# Architecture: Orchestration Discipline Bundle (LIGHT)

**Stage**: 04 — Architect (FEATURE-light)
**Architect**: Celebrimbor, Master Craftsman
**Scope**: delivery-flow plugin only — SKILL.md, references, hook scripts. No new data models, no external integrations, no new APIs.
**Source PRD**: `.delivery/artifacts/02-refine/po/prd.md` (16 FRs, 8 NFRs)

> *"Let us forge something that will endure beyond the ages."*

---

## 1. Architectural Posture

This is a **discipline remediation bundle**, not a feature. The architecture is therefore almost entirely:

- Documentation edits (SKILL.md + 6 reference docs)
- One hook extension (`enforce_pipeline_scope.py`)
- One optional hook extension (`audit_agent_prompt.py`)
- One config schema version bump (v2.6 → v2.7)

There is **no new component**, **no new data flow**, **no new service boundary**. The load-bearing design questions are narrow and tactical:

1. How does `enforce_pipeline_scope.py` reliably distinguish orchestrator-origin writes from sub-agent-origin writes?
2. How does config loading tolerate the removal of `project_type` without surprising pinned users?
3. How does the Isolated Adversarial Loop actually terminate in bounded time with non-monotonic reviewers?
4. Which files change, and what is the minimum consistent edit set?

The three ADRs in this stage lock the contentious answers. This doc maps the rest.

---

## 2. Origin Detection Strategy for `enforce_pipeline_scope.py`

### 2.1 Problem

The hook must deny orchestrator-initiated writes to pipeline artifacts during an active run, but allow sub-agent-initiated writes to the same paths. PreToolUse hooks receive tool input but no first-class "who is calling" field that distinguishes the top-level Claude session from a dispatched Agent tool sub-session.

### 2.2 Chosen mechanism: layered detection with soft-deny fallback

Three signals, checked in order. First signal that resolves wins. If none resolve, the hook **warns** rather than denies (preserves NFR-05).

**Layer 1 — Environment variable (primary, deterministic)**

- The orchestrator sets `DELIVERY_FLOW_AGENT_CONTEXT=<role>` immediately before dispatching any Agent tool invocation (e.g., `po`, `architect`, `developer`, `quality`).
- The env var is inherited by the sub-agent process tree. The hook reads `os.environ.get("DELIVERY_FLOW_AGENT_CONTEXT")`.
- If **set** → sub-agent-origin → allow (subject to scope rules).
- If **unset** → candidate orchestrator-origin → proceed to Layer 2.

**Layer 2 — Hook input metadata (secondary)**

- `read_hook_input()` returns the JSON payload the harness provides on stdin. Inspect for a `transcript_path` / `session_id` pattern that differs between parent and sub-agent frames, or a `parent_tool_use_id` field when present.
- If Layer 2 positively identifies a sub-agent frame → allow.
- If inconclusive → proceed to Layer 3.

**Layer 3 — Soft-deny fallback (safety)**

- If neither signal is available (e.g., harness version drift, env var never injected), emit a **loud `systemMessage` warning** naming the Delegation Prime Directive and the target path, but DO NOT deny.
- Rationale: a broken detector must never brick a user pipeline. NFR-05 wins over FR-09 strictness when the mechanism itself is uncertain.

### 2.3 Routing metadata allowlist

Regardless of origin, the following paths are **always allowed**, because they are legitimately orchestrator-owned bookkeeping:

```
.delivery/state.md
.delivery/config.yml
.delivery/memory/**
.delivery/artifacts/*/state/**
.delivery/artifacts/*/handoff/**
```

The allowlist is a single module-level constant in the hook so it cannot drift.

### 2.4 Bash-redirection coverage

The hook is currently registered on `Edit`, `Write`, `NotebookEdit`. It will be extended to also fire on `Bash`. When the Bash `command` string matches a write-redirection pattern (`>`, `>>`, `tee`, `cat <<EOF`, `dd of=`, `cp`/`mv` targeting an artifact path) pointing at an in-scope path, the same origin rule applies. This closes the heredoc bypass called out in C3. Pattern detection is a cheap regex over the command string.

### 2.5 Activation gating

Deny behavior is gated on BOTH:

- `schema_version >= 2.7` in `.delivery/config.yml`, AND
- `pipeline.enforce_self_write_block: true` in the same file

Default for fresh v2.7 configs is `true`. For tolerantly-parsed v2.6 configs the effective value is `false`. This resolves R7/C6 — the dogfood run is **forward-looking**, not self-referential.

### 2.6 Degradation contract

All new logic stays inside the existing `try/except → sys.exit(0)` wrapper in `main()`. No new dependencies. Pure stdlib. p95 overhead budget: **≤ 15ms added** (NFR-01 gives 50ms total).

**See ADR-001 for the full decision record.**

---

## 3. Config Migration Strategy: `project_type` v2.6 → v2.7

### 3.1 Decision summary

**Warn-and-drop with explicit opt-in override.** Not silent. Not a hard error.

### 3.2 Behavior matrix

| Config state | schema_version | Behavior |
|---|---|---|
| v2.6 with `project_type: GREENFIELD` | 2.6 | Parse. Log deprecation banner on stage start. Phase 1 detection runs and drives routing. Legacy `project_type` ignored for routing. |
| v2.7, no `project_type` | 2.7 | Normal operation. Phase 1 detection every run. |
| v2.7 with `routing.force_type: DOCS_ONLY` | 2.7 | Phase 1 detection runs and is logged, but routing uses `routing.force_type`. Banner announces the pin. |
| v2.7, both bare `project_type` AND `routing.force_type` | 2.7 | `routing.force_type` wins. Bare `project_type` logged as deprecated. |
| v2.6, neither key | 2.6 | Unchanged from today. |

### 3.3 Why warn-and-drop (not silent)

C1 is correct that silent drop is a behavior break wearing a compatibility costume. A user who pinned `project_type: DOCS_ONLY` intentionally deserves to know their pin is being ignored. The deprecation banner gives them one run's notice before they migrate to `routing.force_type:`.

### 3.4 Parser changes

- `SKILL.md` Phase 1: always run detection from the current user request.
- Config loader: read `project_type` if present, emit deprecation to `state.md` run log + stage banner, discard for routing.
- New key `routing.force_type` in schema v2.7. Enum matches existing project types.
- Migration recipe in `config-schema.md` "Deprecated keys" section.

**See ADR-002 for the full decision record.**

---

## 4. Isolated Adversarial Loop Convergence Algorithm

### 4.1 Termination conditions (canonical)

Terminate when ANY of:

1. **Two-clean rule**: Two *consecutive* loops return zero findings → `status: converged (two_clean)`
2. **No-new-classes rule**: Two *consecutive* loops have findings, but every finding belongs to an issue class raised in an earlier loop (no new class has appeared for 2 consecutive iterations) → `status: converged (class_saturated)`
3. **Hard cap**: `N >= max_self_correction` (default 3) → `status: cap_reached`, surfaced to the human checkpoint with residuals documented.

A single zero-finding loop is **not** sufficient — fresh reviewers produce non-monotonic critique sets (C4).

### 4.2 Issue class taxonomy

Reviewers MUST tag each finding with exactly one class from a fixed taxonomy declared in `team-patterns.md`:

```
coupling | security | data-integrity | naming | testability | performance | docs
```

A finding without a valid tag is treated as `misc` and counted as a new class (conservative — prevents taxonomy evasion).

### 4.3 Pseudocode (loop protocol)

```
function isolated_adversarial_loop(artifact, max_iter):
    loops = []
    N = 0
    while N < max_iter:
        N += 1

        # Fresh reviewer. Prompt contains ONLY the current artifact
        # plus the standard adversarial reviewer brief + taxonomy.
        # NO prior findings, NO "this is loop N", NO fix summaries.
        reviewer = dispatch_fresh_subagent(
            role="adversarial_reviewer",
            inputs=[artifact, reviewer_brief, taxonomy],
            context_leak=False,
        )
        findings = reviewer.return_findings()   # [{issue, class}, ...]
        classes  = { f.class for f in findings }
        loops.append({"findings": findings, "classes": classes, "N": N})

        # Rule 1: two-clean
        if len(findings) == 0:
            if len(loops) >= 2 and len(loops[-2]["findings"]) == 0:
                return {"status": "converged", "reason": "two_clean", "loops": loops}
            # Single clean loop: keep going, do NOT exit.
            # Architect has nothing to fix; re-dispatch reviewer on same artifact.
            continue

        # Rule 2: no-new-classes
        if len(loops) >= 3:
            prior_union_before_prev = union(l["classes"] for l in loops[:-2])
            prior_union_before_curr = union(l["classes"] for l in loops[:-1])
            prev_classes    = loops[-2]["classes"]
            current_classes = loops[-1]["classes"]
            if (prev_classes.issubset(prior_union_before_prev) and
                current_classes.issubset(prior_union_before_curr)):
                document_residuals(findings)
                return {"status": "converged", "reason": "class_saturated", "loops": loops}

        # Otherwise: Architect (fresh dispatch) revises artifact.
        artifact = dispatch_fresh_subagent(
            role="architect_revise",
            inputs=[artifact, findings],   # Architect sees current findings only.
        ).revised_artifact()

    # Rule 3: hard cap
    document_residuals(loops[-1]["findings"])
    return {"status": "cap_reached", "loops": loops}
```

### 4.4 Key invariants

- **Reviewer context isolation**: every reviewer dispatch is a fresh sub-agent with zero prior-loop context. Enforced by the dispatch wrapper.
- **Architect context scoping**: the Architect revision sub-agent sees the **current** loop's findings only, not prior loops' findings, to prevent compound patching.
- **Cap-reached is a documented exit**, not a failure. Human checkpoint decides whether to accept residuals.
- **N=1 clean pass** continues to N=2 with the same artifact. A clean first pass proves nothing.

**See ADR-003 for the full decision record.**

---

## 5. Documentation Touch Points (Edit Map)

Complete set of files the Development stage will edit. No content drafted here — only *what change goes where*.

### 5.1 delivery-flow plugin (primary)

| File | Changes | FRs |
|------|---------|-----|
| `delivery-team/skills/delivery-flow/SKILL.md` | Add "Delegation Prime Directive" section (top, post-metadata). Add "One Role = One Sub-Agent" rule block adjacent. Revise Step 4.5 to reject "simple" justifications. Add "Common Orchestrator Anti-Patterns" section (post-stages, pre-references). Update Phase 1 guidance to reference current-request detection. Bump schema_version references to 2.7. | FR-03, FR-05, FR-06, FR-07, FR-08, FR-10 |
| `.../references/config-schema.md` | Bump v2.6 → v2.7. Move `project_type` to "Deprecated keys". Add `routing.force_type` and `pipeline.enforce_self_write_block`. Document expanded `max_self_correction` use. Changelog. | FR-01, FR-02, FR-15, FR-16 |
| `.../references/setup-wizard.md` | Remove Q1 (project_type). Renumber Q2-Q10 → Q1-Q9. Note the renumbering for any external references. Wizard output has no `project_type` and declares `schema_version: 2.7`. | FR-04 |
| `.../references/project-types.md` | Reframe: project types are runtime routing decisions, not config settings. | FR-05 |
| `.../references/pipeline-stages.md` | Header note: `[PARALLEL]`/`[SEQUENTIAL]` markers mean separate sub-agents per role. Stage 4 references Isolated Adversarial Loop pattern by name; bounds loops by `max_self_correction`. | FR-11, FR-14 |
| `.../references/team-patterns.md` | Every pattern gets a "Dispatch rule:" one-liner. Add new "Isolated Adversarial Loop" variant with full protocol (setup, loop, three convergence rules, taxonomy, no-context-leak guarantee). | FR-11, FR-13 |
| `.../references/quality-gates.md` | DoD validation: each validator role is its own sub-agent invocation. Add "Known hook limitations" list mirrored from the hook docstring. | FR-09, FR-11 |

### 5.2 Hook scripts

| File | Changes | FRs |
|------|---------|-----|
| `delivery-team/hooks/enforce_pipeline_scope.py` | Extend module docstring with scope + known gaps. Add `ALLOWLIST` constant. Add layered origin detection (env var → hook input metadata → soft-deny). Extend to `Bash` tool. Add Bash-redirection pattern matcher. Add activation gating on `schema_version >= 2.7` + `pipeline.enforce_self_write_block`. Preserve try/except → sys.exit(0). | FR-09 |
| `delivery-team/hooks/hooks.json` | Register `enforce_pipeline_scope.py` on `Bash` in addition to Edit/Write/NotebookEdit. | FR-09 |
| `delivery-team/hooks/audit_agent_prompt.py` *(OPTIONAL / MAY)* | Add compound *reviewer* prompt detector (negation-aware). Emit non-blocking `systemMessage` on hit. | FR-12 |

### 5.3 Cross-cutting doc parity

| File | Changes | FRs |
|------|---------|-----|
| `CLAUDE.md` | Update "Config schema" conventions line: v2.6 → v2.7. | FR-16 |
| `README.md` | Scan for `project_type` as a config field. Remove or update. | FR-16 |
| `.claude-plugin/marketplace.json` | Scan for schema version references. Update if present (likely no-op). | FR-16 |
| `docs/**` (MkDocs site, 25 pages) | Grep for `project_type`, `schema_version: 2.6`, bare `2.6`. Update surviving references. | FR-16 (expanded per C7) |

### 5.4 NOT touched (explicit)

- Other delivery-team skills (`developer/`, `quality/`, `architect/`, `godot/`, `operations/`, `ui/`, `presentation/`, `user-feedback/`, `alias-creator/`)
- Other plugins (`agentic-flow-builder/`, `prd-quality-gate-flow/`, `research-agent/`, `prompt-engineer/`)
- Any database / SQLite component
- Any MCP server

---

## 6. Non-Functional Budget

| NFR | Budget | Architecture position |
|---|---|---|
| NFR-01 | p95 ≤ 50ms for hook | Layered detection is O(1) dict/string ops. Bash regex is one pass. Well under budget. |
| NFR-02 | stdlib only | Only `os.environ`, `re`, `fnmatch`, `pathlib`. |
| NFR-03 | v2.6 configs must parse | Tolerant parser. Warn-and-drop (ADR-002). |
| NFR-04 | doc parity is a DoD validator | Edit map §5 is the canonical grep target list. |
| NFR-05 | graceful degradation | `try/except sys.exit(0)` preserved; Layer 3 soft-deny. |
| NFR-06 | dogfood this bundle | Activation gating (§2.5) makes dogfood forward-looking. |
| NFR-07 | plugin-dev skills required | Enforced at Development-stage DoD. |
| NFR-08 | atomic merge | Single PR with all §5 edits. |

---

## 7. Risk Treatment Summary

| PRD Risk | Architecture response |
|---|---|
| R1 over-blocking | Explicit allowlist constant (§2.3) |
| R2 FR-12 brittleness | FR-12 remains MAY; negation-aware matcher if implemented |
| R3 non-convergence | Two-clean + no-new-classes + hard cap (ADR-003) |
| R4 v2.6 parse crash | Tolerant parser with try/except (ADR-002) |
| R5 doc parity drift | Explicit §5 edit map |
| R6 origin detection unreliability | Layered + soft-deny fallback (ADR-001) |
| R7 dogfood paradox | Activation gating on schema_version + flag (§2.5) |
| R8 SKILL.md anchor drift | Plan-stage grep before merge |

---

## 8. Open Questions (forwarded to Plan)

- **PQ-1**: Does Layer 2 (hook input metadata) actually receive a sub-agent identifier in the current Claude Code harness, or is Layer 1 (env var) load-bearing? Verify against harness version in use.
- **PQ-2**: Test fixture location for v2.6 legacy config (OQ-7). No test runner — recommend `delivery-team/tests/fixtures/legacy-v2.6-config.yml` exercised by a standalone Python script.
- **PQ-3**: `routing.force_type` enum — must it match exactly the Phase 1 detection vocabulary? Assume yes unless Design says otherwise.

---

## 9. ADR Index

- **ADR-001**: Origin detection mechanism for `enforce_pipeline_scope.py`
- **ADR-002**: `project_type` migration strategy (v2.6 → v2.7)
- **ADR-003**: Isolated Adversarial Loop convergence criteria

---

*"The hammer has fallen where the seams were thinnest. What remains is straight, and what remains will endure."*

— Celebrimbor

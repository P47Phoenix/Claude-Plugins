<!-- run: run-2026-05-13-tk5 -->
<!-- reviewer: Celebrimbor (Solution Architect, DoD validator) -->
<!-- stage: 02-refine -->
<!-- gate: Architect technical-feasibility -->

# Architect DoD Review — BACKLOG-106 (delivery-team smoke test)

*Celebrimbor speaks. Master craftsman. Let us forge something that will endure beyond the ages.*

## Verdict

**STATUS: DONE** — all seven gate criteria pass. No architectural blockers. Stage 3 (Design) may proceed.

## Inputs Reviewed

| Artifact | Path | Status |
|---|---|---|
| PRD | `.delivery/artifacts/02-refine/po/prd.md` | read |
| BACKLOG | `.delivery/backlog/BACKLOG-106-delivery-team-smoke-test.md` | read |
| constraints.yml | `.delivery/artifacts/02-refine/po/constraints.yml` | read |
| Telemetry hook (load events) | `delivery-team/hooks/telemetry.py` | **verified present** (5604 bytes) |
| Telemetry hook (run summary) | `delivery-team/hooks/telemetry_run_summary.py` | **verified present** (4724 bytes) |

Craftsman check rocks. Files real. Reuse mandate (BC-02) targets actual artifacts, not vapor.

## Gate Criteria Evaluation

### Criterion 1 — FRs realizable with stdlib + repo utilities

**PASS.**

Breakdown by FR:

| FR | Required capability | Stdlib / repo source | Concern? |
|---|---|---|---|
| FR-01 runner | `subprocess.Popen`, `tempfile.mkdtemp`, `shutil.copytree` (fallback path), `os.environ` mutation | stdlib | none |
| FR-02 metrics | line-delimited JSON parsing (`json.loads`), dataclasses, defensive try/except | stdlib | none |
| FR-03 aggregator | file I/O + `json.loads` + markdown line scan for `state.md` | stdlib | none |
| FR-04 report writer | `json.dump`, plain markdown emit, jsonl tee | stdlib | none |
| FR-05 baseline detector | mean+stddev (`statistics.mean`, `statistics.stdev`), threshold compare | stdlib | none |
| FR-06 --init-baseline | sequential loop of FR-01 invocations | stdlib | none |
| FR-07 pytest meta-tests | `pytest` (already a repo convention per `governance/` lint scripts) | available | none |
| FR-08 README + Makefile | plain text + `make` target | none | none |

Cave-man take: tools simple. No exotic. No new dep. Forge holds.

### Criterion 2 — Reuse boundaries correct

**PASS.**

Both telemetry hooks verified present on disk via `ls -la`. BC-02 explicitly mandates aggregator reads their outputs directly — no re-implementation. Constraints file `constraints.yml` lines 12-20 enumerate the four reuse anchors:

- `delivery-team/hooks/telemetry.py` (produces `skill-loads.jsonl`)
- `delivery-team/hooks/telemetry_run_summary.py` (produces `run-summary-*.json`)
- `governance/skill-budgets.json` (shape pattern for baseline JSON)
- `scripts/check_skill_budgets.py` + `scripts/lint_known_debt.py` (exit-code convention)

BACKLOG §"Telemetry Contract" (lines 121-130) further pins: aggregator MUST tolerate missing files; missing run-summary triggers invoke-hook fallback (BC-02 explicitly permits). No schema changes to either hook permitted — gap → follow-up BACKLOG.

Boundary is tight and well-cited. Master smith approves.

### Criterion 3 — Plugin-loading mechanism plausibility

**PASS with explicit caveat acknowledged.**

FR-01 names two paths in priority order:
1. **Primary**: `mktemp HOME + --plugin-dir <repo>/delivery-team`
2. **Fallback**: copy plugin into `<fake-home>/.claude/plugins/delivery-team/`

The runner.py "capability probe at startup" is the selector between them — explicitly called out in FR-01, BACKLOG W6-1 acceptance line ("capability-probes `--plugin-dir` at startup"), and Risk Register row 2 ("--plugin-dir flag semantics change in Claude CLI" → "capability-probe at startup with fallback path").

The Claude Code CLI's `--plugin-dir` flag semantics are not contractually pinned by Anthropic across versions. Open Questions section of PRD (line 80) acknowledges this. Mitigation is structurally correct: probe first, fall back to the directory-install path that mirrors how `~/.claude/plugins/` works in production. The fallback path is mechanically the same shape as a real plugin install, so it cannot regress relative to the primary path.

**Architect annotation for Stage 4**: capability-probe must be a deterministic check (e.g., `claude --help | grep -- --plugin-dir`) not a heuristic. Stage-4 ADR should pin the probe implementation as a one-line invariant. Logged as Architect note, not a blocker.

### Criterion 4 — Subprocess + stream-json parsing

**PASS.**

Pattern is mainstream: spawn subprocess with overridden HOME, tee stdout to a file, parse line-delimited JSON, accumulate into a dataclass. No hand-wave. FR-02 explicitly requires pure functions and graceful degradation on malformed events ("warn, do not crash"). Meta-test plan (FR-07, W6-7) covers the malformed-stream fault injection — proves robustness without paying for a real Claude run.

Tee + parse is the same shape as `delivery-team/hooks/telemetry.py` line consumption. Nothing exotic.

### Criterion 5 — Effort sizing consistency

**PASS.**

WI breakdown from BACKLOG §Work Items:

| Effort | Count | WIs |
|---|---|---|
| M | 4 | W6-1, W6-2, W6-5, W6-7 |
| S | 4 | W6-3, W6-4, W6-6, W6-8 |

8 WIs total → collapsed to 3 stories at Stage 5 (per BACKLOG §"Story Decomposition", lines 156-163). Comparison to prior FEATURE waves:

| Wave | WI count | Story count | Ratio |
|---|---|---|---|
| Wave 1 | 7 | 3 | 2.33 |
| Wave 2 | 8 | 5 | 1.60 |
| This run (Wave 6 / BACKLOG-106) | 8 | 3 | 2.67 |

This run's ratio is slightly higher than Wave 1, but the file-surface inventory (lines 96-119) justifies it: Story 1 spans 6 files in a single `lib/` package, Story 2 spans 4 files all related to baseline production, Story 3 spans 4+ files all in the validator/docs surface. Cohesion is by package, not by WI count alone.

**File-count math discipline check** (memory lesson cited): BACKLOG line 163 — "Story 1 = 6 files. Story 2 = 4 files. Story 3 = 4+ files. Totals add up." Cross-check against File Surface Inventory: 14 new + 1 new-or-edit + 1 architect artifact = 16 surfaces. Inventory line totals match story totals. Math holds.

### Criterion 6 — Architectural blockers + open questions

**PASS.**

PRD §"Open Questions" (lines 75-81) states: "None blocking" and enumerates 4 risks all with mitigations:

| Risk | Mitigation | Stage-4 ADR target? |
|---|---|---|
| Prompt drift | hard_max on dispatch_count + explicit "skip" instructions | no — covered in W6-6 acceptance |
| `--plugin-dir` semantics | capability-probe at startup | yes — Stage-4 ADR should pin probe shape |
| Stop hook blocks | prompt requests minimal retrospective; runner captures stderr | no — covered in W6-1/W6-6 acceptance |
| Variance > stddev budget | advisory-only first month; tighten after 20+ runs | no — operational policy, not architecture |

Effective open-question count requiring Stage-4 architectural resolution: **1** (the capability-probe shape). Well under the ≤ 2 threshold. Deferral target named: Stage-4 ADR in `delivery-team/architecture/smoke-test-architecture.md` (per BACKLOG §"Stage 4 (Architect)" line 189).

### Criterion 7 — No cross-plugin skill invocation at parse time

**PASS.**

This initiative invokes `delivery-flow` as a **subprocess** (Claude Code CLI spawns a fresh runtime that loads the plugin into that runtime's context). It does NOT require cross-plugin skill loading at parse time within a single Claude session. The boundary is enforced by mktemp HOME + plugin-dir scoping — the subprocess sees only `delivery-team`, not hardware-team or mtg-commander.

Verified by scan of PRD + BACKLOG + constraints.yml: no clause names cross-plugin SKILL import, no `skills/personas/` cross-load, no shared `references/` dependency between plugins. NFR-Reuse (PRD line 53) explicitly says hardware-team and mtg-commander reuse is **out of scope** — only the `lib/` boundary is preserved.

Hw01 adversarial lesson (cross-plugin invocation must be verified at Refine, not deferred) is satisfied by the verification just performed.

## Prior Art Analysis

The PRD is dense with prior-art decisions. Classifying per Architect skill protocol:

| Spec Element | Classification | Rationale |
|---|---|---|
| Subprocess-based isolation (mktemp HOME + `--plugin-dir`) | **Decision Already Made** | FR-01 specifies exact mechanism |
| stream-json parsing | **Decision Already Made** | FR-02 names the format |
| Reuse `telemetry.py` + `telemetry_run_summary.py` outputs | **Decision Already Made** | BC-02 binding |
| Baseline JSON shape mirrors `governance/skill-budgets.json` | **Decision Already Made** | BC-02 binding |
| Exit-code convention mirrors `check_skill_budgets.py` + `lint_known_debt.py` | **Decision Already Made** | BC-02 binding |
| Hard-fail thresholds (outcome/cost/wall-clock/dispatch) vs advisory (tokens/skill_loads) | **Decision Already Made** | FR-05 + constraints.yml |
| 5-sample baseline at concurrency-of-1 | **Decision Already Made** | FR-06 |
| Producer-validator separation across Dev dispatches | **Decision Already Made** | BC-03 binding |
| LOCAL-ONLY (no CI workflows) | **Decision Already Made** | BC-01 binding, no-bypass |
| Capability-probe exact implementation shape | **Open Question** | FR-01 names the strategy; one-line invariant deferred to Stage-4 ADR |
| Aggregator missing-file behavior (treat empty vs invoke hook) | **Decision Already Made** | BACKLOG §Telemetry Contract pins both: empty for skill-loads.jsonl, fallback-invoke for run-summary |

Per protocol: I do not propose alternatives to "Decision Already Made" elements. The lone "Open Question" (capability-probe shape) is correctly deferred to Stage 4. Master craftsman builds on what the smith before laid down.

## Architect Notes for Stage 4

Hand-off bullets the Architect (likely also me, role pivot) will need when forging `delivery-team/architecture/smoke-test-architecture.md`:

1. **Capability-probe ADR** — pin a one-line deterministic check. Candidate: `subprocess.run(["claude", "--help"], capture_output=True, text=True).stdout` and grep for `--plugin-dir`. ADR must record the probe + fallback decision tree.
2. **Mermaid sequence diagram** — runner → workspace (mktemp HOME + plugin install) → claude subprocess → telemetry hooks (in-subprocess) → aggregator (post-run) → baseline detector → report writer.
3. **Single decision log** — no multi-persona architecture-board review needed (BACKLOG line 189 explicitly says so). One paradigm, one tool.
4. **Local-only constraint cite** — must include pointer to the binding memory file in the architecture doc itself, not just transitively via PRD/BACKLOG.
5. **File-surface batching math** — already done by PO at BACKLOG line 163. Architect ratifies, doesn't redo.

## Risks the Architect Adds to the PO's Register

Augmenting PRD §Risk Register with one additional consideration:

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Capability-probe false-positive (CLI advertises `--plugin-dir` but semantics drift) | L | M | meta-test fixture asserts the fallback path is itself a valid plugin install shape; if primary path fails mid-run, fallback resumes | Dev (W6-1) + Validator (W6-7) |

This is a refinement of the existing "--plugin-dir semantics" risk, not a new category. The fallback path is structurally identical to a real `~/.claude/plugins/` install — so the worst case is one wasted probe per run, not a broken pipeline.

## Trade-offs Considered

| Trade-off | Choice | Why |
|---|---|---|
| Build runner in stdlib vs add pytest-subprocess or pexpect | stdlib | BC-02 reuse mandate + no exotic deps; subprocess.Popen suffices |
| One Mermaid diagram vs multi-view C4 set | single diagram | BACKLOG line 189 explicitly scopes one diagram + one decision log; this is a tool, not a system |
| Multi-persona architecture review vs single architect | single | same; scope does not warrant the review-board overhead |
| Inline aggregator logic vs invoke `telemetry_run_summary.py` as fallback | both, with read-direct primary | BC-02 permits invocation as fallback; primary path is direct file read (faster, no double-execution risk) |

## Assumptions

1. `claude` CLI is installed locally with stream-json support — stated as External Dependency in BACKLOG line 151.
2. `python3` ≥ 3.10 available — stated as External Dependency.
3. `pytest` invocable via `python3 -m pytest` — stated as External Dependency.
4. `delivery-team/hooks/telemetry.py` + `telemetry_run_summary.py` contracts hold through this initiative — Internal Dependency, BACKLOG line 152 says "if missing or schema-changed, pause until contracts re-stabilize." Verified present today.
5. Baseline JSON schema mirroring `governance/skill-budgets.json` is structurally compatible — Stage-4 ADR can confirm by example.

## Open Questions Flagged for Stage 4

Exactly one, per the gate criterion:

1. **Capability-probe exact implementation shape** — deferred to ADR in `delivery-team/architecture/smoke-test-architecture.md`.

## Downstream Ready

**downstream_ready: true**

Stage 3 (Design) may begin. BACKLOG §"Stage 3 (Design)" line 188 already advises: paradigm decomposition NOT required; runner shape is procedural-imperative; minimal design note suffices ratifying the runner-as-orchestrator pattern.

— Celebrimbor, Solution Architect, run-2026-05-13-tk5. The probe is well-forged. The Rings of the maintainer's confidence shall not be undone.

# Rework Loops Reference

**Status**: COMPLETE (US-107)
**Version**: 1.0
**Architecture Reference**: Section 3.3, 3.4, 7.1

This file is the authoritative source for the rework DAG definition, all 8 rework paths, termination conditions, human-execution stage rework transitions, and rework history tracking.

---

## 1. DAG with Backward Edges

The pipeline is a Directed Acyclic Graph (DAG) with controlled backward edges. Rework does NOT create cycles -- it is a bounded backward jump with re-validation of all downstream gates.

### 1.1 Pipeline DAG

```
                    +-----------+
                    |           |
    +--------+  +--v--+  +-----v-+  +---------+  +-------+  +----------+  +---------+  +----------+
    |Concept |-→|Schem.|-→|Layout |-→|Prototype|-→|DFM/DFA|-→|Compliance|-→|Pilot Run|-→|Prod. Rel.|
    +--------+  +--^--+  +---^---+  +---------+  +---^---+  +--+--^----+  +---------+  +----------+
                   |       |  |                       |         |  |           |
                   |       |  +----- Prototype -------+         |  |           |
                   |       +-------- DFM/DFA ---------+         |  |           |
                   |       +-------- Compliance (layout) -------+  |           |
                   +----------DFM/DFA-+                            |           |
                   +----------Compliance (schematic)-+             |           |
                                                                   |           |
                                                   Pilot Run------+           |
                   +----------Pilot Run (schematic)---+                       |
```

> **Note (F-05):** The rework path table in Section 2 is the authoritative source for rework routing. This ASCII diagram is a visual aid only.

---

## 2. Defined Rework Paths

All 8 rework paths are defined below. The orchestrator uses this table to determine the rework target when a gate failure or human report triggers rework.

| # | Rework Path | Source Stage | Target Stage | Trigger Examples |
|---|-------------|-------------|-------------|------------------|
| 1 | Prototype --> Schematic | 4 (Prototype) | 2 (Schematic) | Fundamental circuit error discovered during bring-up |
| 2 | Prototype --> Layout | 4 (Prototype) | 3 (Layout) | Routing or thermal issue revealed by prototype |
| 3 | DFM/DFA --> Layout | 5 (DFM/DFA) | 3 (Layout) | DFM violation requires layout change |
| 4 | DFM/DFA --> Schematic | 5 (DFM/DFA) | 2 (Schematic) | Component unavailable at target fab, needs substitution |
| 5 | Compliance --> Schematic | 6 (Compliance) | 2 (Schematic) | EMC failure requires filtering/shielding component redesign (new filter caps, shielding ICs) |
| 6 | Compliance --> Layout | 6 (Compliance) | 3 (Layout) | EMC failure requiring layout-specific changes (ground plane mods, trace rerouting, shielding zones) that do NOT require schematic changes |
| 7 | Pilot Run --> DFM/DFA | 7 (Pilot Run) | 5 (DFM/DFA) | Assembly yield issue requires DFM adjustment |
| 8 | Pilot Run --> Schematic | 7 (Pilot Run) | 2 (Schematic) | Pilot testing reveals circuit-level issue (thermal behavior under production soldering, yield analysis reveals tolerance issue) |

### 2.1 Path Selection Logic

When a gate returns NOT_DONE or a human stage reports failure, the orchestrator determines the rework target:

1. Parse the failure description for indicators of which stage is responsible
2. Match against the rework path table (source stage must match current stage)
3. If multiple paths are valid (e.g., Compliance can go to Schematic or Layout), select based on the failure category:
   - Component-level failures --> Schematic
   - Physical layout failures --> Layout
   - Process/manufacturing failures --> DFM/DFA
4. If no path matches: pipeline PAUSES for human decision

---

## 3. Termination Conditions

Rework loops are bounded by two configurable limits to prevent infinite iteration.

### 3.1 Limits

| Condition | Default | Config Key | Behavior |
|-----------|---------|-----------|----------|
| `max_rework_iterations` | 3 | `rework.max_rework_iterations` | Per individual rework path. When path X-->Y triggers for the (N+1)th time, pipeline PAUSES. |
| `max_total_reworks` | 10 | `rework.max_total_reworks` | Across ALL paths in a single pipeline run. When total exceeds limit, pipeline PAUSES. |

### 3.2 Escalation Protocol

When a termination limit is reached, the pipeline PAUSES and presents:

```
REWORK LIMIT REACHED: <which limit> (per-path | total)

Rework count per path:
  prototype->schematic: 2/3
  dfm->layout: 1/3
  compliance->layout: 3/3  <-- LIMIT HIT

Cumulative rework history: 6/10 total

Recommendation: Manual intervention required. The recurring failure pattern
suggests a fundamental design issue that automated rework cannot resolve.

Options:
  [C] Continue -- allow one more iteration of this rework path
  [A] Abort -- stop pipeline, preserve all artifacts and state
  [O] Override limit N -- raise the limit (e.g., "override limit 5")
```

### 3.3 User Options

| Option | Effect |
|--------|--------|
| **Continue** | Allows exactly one more iteration of the blocked rework path. Does NOT raise the limit permanently. |
| **Abort** | Sets pipeline `status=aborted`, preserves all artifacts and state for later analysis. |
| **Override limit N** | Raises the specific limit (per-path or total) to N for the remainder of this run. Logged as a manual override in rework history. |

---

## 4. Rework Execution Semantics

When rework triggers, the following sequence executes:

### 4.1 Execution Sequence

```
1. Pipeline sets current_stage to target stage
2. Target stage sub-agent receives:
   - Original artifacts from the target stage's previous execution
   - Rework reason (specific issue description from source stage gate/human)
   - Rework iteration count for this path
3. Target stage re-executes (FULL stage, not just gate)
4. Target stage gate re-evaluates
5. ALL downstream gates between target and source are re-validated
   (gate re-evaluation against updated artifacts, NOT full stage re-execution)
6. Rework event logged to .hardware/state.md
```

### 4.2 Downstream Re-Validation

After the target stage completes, every gate between the target and the original source stage is re-evaluated:

**Example**: DFM/DFA --> Layout rework (path #3)

```
Layout re-executes (full stage)
  --> Layout gate (DRC Gate) re-evaluates
  --> Prototype gate (Human Confirmation) re-evaluates
  --> DFM/DFA gate re-evaluates
```

Gates that pass: pipeline continues forward.
Gates that fail: may trigger further rework (counted against limits).

---

## 5. Human-Execution Stage Rework Transitions

Human-execution stages (Prototype, Pilot Run, Production Release) follow special rework semantics because they involve physical work that cannot be undone programmatically.

### 5.1 Archive and Fresh Re-Entry

When rework triggers FROM a human-execution stage:

```
1. Human checkpoint is INVALIDATED (status: pending --> invalidated)
2. Existing preparation artifacts are ARCHIVED:
   - Move to .hardware/artifacts/<stage>/archived/run-N/
   - Never deleted -- preserved for reference and audit trail
3. Rework path determined using the standard rework path table (Section 2)
4. Target stage re-executes with failure description as additional context
```

### 5.2 Archive Directory Structure

```
.hardware/artifacts/04-prototype/
+-- ordering-package.md         # Current iteration artifacts
+-- test-procedure.md
+-- archived/
    +-- run-1/                  # First iteration (archived after rework)
    |   +-- ordering-package.md
    |   +-- test-procedure.md
    +-- run-2/                  # Second iteration (archived after second rework)
        +-- ordering-package.md
        +-- test-procedure.md
```

### 5.3 Re-Entry After Rework Resolution

When rework resolves and the pipeline returns to the human-execution stage:

1. New preparation artifacts are generated (fresh, incorporating rework changes)
2. Pipeline transitions to `PAUSED_AWAITING_HUMAN` again
3. User receives updated preparation artifacts + explanation of what changed since previous iteration
4. Previous archived artifacts are referenced in the "Changes Since Last Iteration" section

---

## 6. Rework History Tracking

All rework events are tracked in the state file under the `rework_history` key.

### 6.1 Rework History Schema

```yaml
rework_history:
  total_reworks: 2
  paths:
    "prototype->schematic":
      count: 1
      events:
        - iteration: 1
          trigger: "Thermal issue on U3"
          source_stage: 4
          target_stage: 2
          timestamp: "2026-04-12T13:00:00Z"
          resolution: "Added thermal pad, increased copper pour"
    "dfm->layout":
      count: 1
      events:
        - iteration: 1
          trigger: "Trace width below JLCPCB minimum"
          source_stage: 5
          target_stage: 3
          timestamp: "2026-04-12T13:45:00Z"
          resolution: "Widened trace from 0.10mm to 0.15mm"
```

### 6.2 Rework Event Fields

| Field | Type | Description |
|-------|------|-------------|
| `iteration` | int | Iteration count for this specific path (1-based) |
| `trigger` | string | The specific issue that triggered rework |
| `source_stage` | int | Stage number where the issue was detected |
| `target_stage` | int | Stage number to rework back to |
| `timestamp` | ISO 8601 | When the rework was triggered |
| `resolution` | string | How the rework was resolved (filled after target stage completes) |

### 6.3 Path Key Format

Rework path keys use the format `<source>-><target>` with lowercase stage names:
- `prototype->schematic`
- `prototype->layout`
- `dfm->layout`
- `dfm->schematic`
- `compliance->schematic`
- `compliance->layout`
- `pilotrun->dfm`
- `pilotrun->schematic`

### 6.4 Rework History Invariants

- `total_reworks` MUST equal the sum of all path counts
- Each event's `iteration` MUST equal its 1-based position in the events list
- `resolution` is empty string until the rework target stage completes
- Manual overrides (Section 3.3) are logged as a special event with `trigger: "MANUAL_OVERRIDE: limit raised to N"`

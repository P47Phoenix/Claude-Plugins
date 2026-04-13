# Memory Protocol Reference

**Status**: COMPLETE (US-106)
**Version**: 1.0
**Architecture Reference**: Section 8.1, 8.2, 8.3, 8.4, 8.5, 8.6

This file is the authoritative source for the self-learning memory system: tiered chunked retrieval, memory file format, write/read protocol, pruning rules, decay mechanics, and observation injection for measuring memory influence.

---

## 1. Memory Architecture

The memory system follows delivery-flow's tiered chunked retrieval pattern, stored in `.hardware/memory/`.

### 1.1 Directory Structure

```
.hardware/memory/
+-- index.md                     # Memory index: entry IDs, tags, relevance scores
+-- lessons-concept.md           # Lessons from Concept stages
+-- lessons-schematic.md         # Lessons from Schematic stages
+-- lessons-layout.md            # Lessons from Layout stages
+-- lessons-prototype.md         # Lessons from Prototype stages
+-- lessons-dfm.md               # Lessons from DFM/DFA stages
+-- lessons-compliance.md        # Lessons from Compliance stages
+-- lessons-rework.md            # Cross-cutting rework pattern lessons
+-- lessons-general.md           # General project and process lessons
+-- lessons-archived.md          # Archived entries (excluded from index scanning)
```

### 1.2 Stage-to-File Mapping

| Stage | Memory File |
|-------|------------|
| 1 - Concept | `lessons-concept.md` |
| 2 - Schematic | `lessons-schematic.md` |
| 3 - Layout | `lessons-layout.md` |
| 4 - Prototype | `lessons-prototype.md` |
| 5 - DFM/DFA | `lessons-dfm.md` |
| 6 - Compliance | `lessons-compliance.md` |
| 7 - Pilot Run | `lessons-general.md` (no dedicated file; pilot lessons are process-oriented) |
| 8 - Production Release | `lessons-general.md` |
| Cross-cutting rework | `lessons-rework.md` |

---

## 2. Index Routing Tier (index.md)

The `index.md` file is the routing layer -- it maps every memory entry to its location, tags, and current relevance score. The orchestrator reads ONLY this file first to determine which stage files to load.

### 2.1 Index Entry Format

```yaml
- id: MEM-2026-04-12-001
  file: lessons-schematic.md
  stage: schematic
  category: component-selection
  tags: [derating, capacitor, schematic-review, ceramic]
  project: sensor-board-v2
  date: 2026-04-12
  relevance: 0.95
  applied_count: 2
  noted_count: 0
  consecutive_noted: 0
```

### 2.2 Index Invariants

- Every memory entry in a stage file MUST have a corresponding index entry
- Entry IDs are globally unique: `MEM-YYYY-MM-DD-NNN`
- Index is sorted by relevance (descending) for fast top-N retrieval
- Archived entries are REMOVED from index.md (they exist only in `lessons-archived.md`)

---

## 3. Memory Entry Format (Stage Chunks)

Each `lessons-<stage>.md` file contains a YAML list of memory entries:

```yaml
- id: MEM-2026-04-12-001
  stage: schematic
  category: component-selection
  lesson: "Capacitor C7 was derated below 50% of rated voltage. Always check capacitor derating against maximum operating voltage, not just nominal, especially for ceramic capacitors where effective capacitance drops with DC bias."
  project: sensor-board-v2
  date: 2026-04-12
  tags: [derating, capacitor, schematic-review, ceramic]
  relevance_decay: 0.95
  source_gate: schematic-review-gate
```

### 3.1 Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier: `MEM-YYYY-MM-DD-NNN` |
| `stage` | string | Yes | Originating stage name |
| `category` | string | Yes | Lesson type (component-selection, routing, thermal, compliance, process, etc.) |
| `lesson` | string | Yes | The actual lesson learned -- plain text, actionable |
| `project` | string | Yes | Project that generated this lesson |
| `date` | date | Yes | Date the lesson was captured |
| `tags` | list[string] | Yes | Searchable tags for relevance matching |
| `relevance_decay` | float | Yes | Decay rate per run: 0.0 = one-shot, 1.0 = permanent, 0.95 = slow decay |
| `source_gate` | string | No | Which gate surfaced this lesson |

### 3.2 No-Pricing Filter (SEC-02)

Memory entries MUST NOT capture specific pricing values, negotiated rates, supplier account identifiers, or supplier-specific commercial terms.

**Allowed**: Part numbers, technical rationale (e.g., "Selected MLCC over tantalum for C7 due to DC bias derating")
**Prohibited**: Unit prices (e.g., "Supplier X quoted $0.12/unit for C7"), account IDs, negotiated terms

If pricing data is detected during the write phase, it is redacted to `[PRICE REDACTED]` and event `HW-SEC-001` is logged.

---

## 4. Retrieval Protocol

### 4.1 Read Sequence (2-3 reads per stage)

The retrieval protocol is designed for the p95 < 2 second target (NFR-008).

```
Read 1: Load index.md
  +-- Scan entries for current stage tag match
  +-- Score relevance (see 4.2)
  +-- Determine which stage file(s) to load

Read 2: Load lessons-<current-stage>.md
  +-- Extract entries matching current stage + project (Tier 1: always inject)
  +-- Extract top 5 entries matching current stage from other projects (Tier 2: inject if relevant)

Read 3 (conditional): Load lessons-rework.md
  +-- Only if a rework path involves the current stage
  +-- Extract cross-cutting rework patterns relevant to this stage
```

### 4.2 Relevance Scoring

Relevance is scored using four factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Tag match | 0.4 | How many of the entry's tags match the current stage context |
| Project similarity | 0.3 | Same project = 1.0, similar project type = 0.5, different = 0.1 |
| Recency | 0.2 | Days since entry creation, normalized to [0, 1] with 90-day half-life |
| Decay factor | 0.1 | Current `relevance_decay ^ runs_since_creation` |

**Final score** = weighted sum, capped at [0.0, 1.0]

### 4.3 Memory Tiering

| Tier | Criteria | Injection Behavior |
|------|----------|--------------------|
| **Always inject** | Lessons tagged with current stage AND from same project | Mandatory injection into stage sub-agent prompt |
| **Inject if relevant** | Lessons tagged with current stage from other projects, top 5 by relevance | Injected if context budget allows |
| **Available on request** | All other lessons in `.hardware/memory/` | Sub-agent can Read from memory/ if it needs historical context |

---

## 5. Write Protocol

Memory writes occur after a pipeline run completes or aborts.

### 5.1 Write Sequence

1. Orchestrator reviews pipeline execution: gates that failed, rework paths triggered, human escalations, review findings
2. For each notable event, generate a memory entry
3. Apply no-pricing filter (SEC-02) -- redact pricing patterns before persistence
4. Write entry to the appropriate `lessons-<stage>.md` file
5. Update `index.md` with the new entry's ID, tags, and initial relevance score (1.0)
6. Cross-cutting patterns (e.g., "component X repeatedly causes rework") go to `lessons-rework.md`
7. Run cleanup/archival pass (Section 7)

### 5.2 Notable Events That Generate Memories

| Event | Target File | Category |
|-------|------------|----------|
| Gate failure (NOT_DONE) | `lessons-<stage>.md` for the failed stage | gate-failure |
| Rework triggered | `lessons-rework.md` | rework-pattern |
| Human escalation | `lessons-general.md` | escalation |
| Review finding (critical/major) | `lessons-<stage>.md` for the reviewed stage | review-finding |
| Component substitution | `lessons-schematic.md` | component-selection |
| DFM/DFA violation | `lessons-dfm.md` | manufacturing |
| Compliance failure | `lessons-compliance.md` | compliance |

### 5.3 Missing File Handling

| Condition | Event Code | Behavior |
|-----------|-----------|----------|
| `index.md` missing | HW-MEM-001 (Info) | No lessons injected. Pipeline continues normally. Create index on next write. |
| Stage file missing | HW-MEM-002 (Info) | No lessons for that stage. Pipeline continues. Create file on next write. |
| Stage file unparseable | HW-MEM-003 (Warning) | Skip memory injection for that stage. Log warning. Pipeline continues. |

---

## 6. Observation Injection (Memory Influence Observability)

To measure whether injected memories actually influence stage outcomes, each sub-agent that receives lessons reports their disposition.

### 6.1 Sub-Agent Prompt Addition

When injecting memories into a stage sub-agent prompt, append:

```
You have been provided with lessons from previous pipeline runs in the
"Lessons from Previous Runs" section above. For each injected lesson,
report its disposition in your output using one of:
  MEMORY_APPLIED: <MEM-ID> -- <brief description of how the lesson influenced a decision>
  MEMORY_NOTED: <MEM-ID> -- <brief reason why it was acknowledged but not applicable>
```

### 6.2 Orchestrator Post-Processing

After the sub-agent completes:

1. Scan output for `MEMORY_APPLIED` and `MEMORY_NOTED` signals
2. Log disposition in gate results under `memory_disposition`:
   ```yaml
   memory_disposition:
     - id: MEM-2026-04-12-001
       status: APPLIED
       detail: "Used capacitor derating lesson to flag C12"
     - id: MEM-2026-04-10-003
       status: NOTED
       detail: "Lesson about connector orientation not relevant to this board"
   ```
3. During memory write phase, update index relevance:
   - `MEMORY_APPLIED`: relevance boost +0.1 (capped at 1.0)
   - `MEMORY_NOTED` across 3+ consecutive runs (same lesson injected but never applied): relevance penalty -0.05

---

## 7. Pruning Rules and Decay

### 7.1 Relevance Decay

After each pipeline run, all memory entry relevance scores are decayed:

```
new_relevance = max(current_relevance * relevance_decay, 0.05)
```

**Decay floor**: 0.05. This ensures the archival threshold (0.1) is reachable in finite runs rather than asymptotically approaching zero.

### 7.2 Archival Rules

| Condition | Action |
|-----------|--------|
| Relevance score < 0.1 after at least 10 pipeline runs | Entry moved to `lessons-archived.md` |
| `memory_entries_limit` exceeded per stage file (default: 100) | Lowest-relevance entries archived until count <= limit |
| `MEMORY_NOTED` across 5+ consecutive runs without a single `MEMORY_APPLIED` | Relevance set to 0.0 (triggers archival on next cleanup) |

### 7.3 Archival Behavior

1. Entries in `lessons-archived.md` are excluded from `index.md` scanning and are never injected into sub-agent prompts
2. Archived entries are preserved (not deleted) for historical reference
3. Cleanup runs during the memory write phase at the end of each pipeline run (after new lessons are captured)

### 7.4 Archival Entry Format

Archived entries retain their original format with an additional `archived_date` and `archive_reason` field:

```yaml
- id: MEM-2026-01-15-003
  stage: layout
  category: routing
  lesson: "..."
  archived_date: 2026-04-12
  archive_reason: "Relevance below threshold (0.08 < 0.1) after 12 runs"
```

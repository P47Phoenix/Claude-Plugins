# kicad-happy Integration Reference

> Contract version: 1.0 | Target kicad-happy version: >=1.2.x

This reference defines the interface between hardware-team role skills and kicad-happy skills. Role sub-agents load this reference when they need to invoke a kicad-happy skill and must validate the output contract.

---

## 1. Cross-Plugin Invocation Pattern

Hardware-team role skills invoke kicad-happy skills via the **Skill tool** using the `<plugin>:<skill>` syntax. The kicad-happy plugin loads from the user's plugin cache at `~/.claude/plugins/cache/kicad-happy/kicad-happy/<version>/`.

### Invocation Flow

```
1. Role sub-agent (e.g., electrical-engineer) determines it needs a kicad-happy capability
2. Sub-agent calls: Skill("kicad-happy:<skill-name>")
3. kicad-happy SKILL.md loads into the sub-agent's context
4. Sub-agent uses the loaded skill's capabilities
5. Sub-agent validates output against the contract below (Section 4)
6. Sub-agent processes validated output or reports CONTRACT_MISMATCH
```

### Key Rules

- The **orchestrator** (hardware-flow) does NOT invoke kicad-happy skills directly
- Only **role sub-agents** invoke kicad-happy skills, and only the skills mapped to their role (Section 2)
- Each role's SKILL.md declares which kicad-happy skills it may invoke
- The sub-agent owns the decision of **when** and **how** to use kicad-happy capabilities

---

## 2. Role-to-Skill Mapping

| Hardware Role | kicad-happy Skills Consumed | Usage Context | Stage(s) |
|---|---|---|---|
| Electrical Engineer | `kicad`, `spice`, `digikey`, `mouser`, `lcsc`, `element14` | Schematic analysis, simulation, component sourcing | Schematic |
| PCB Layout Engineer | `kicad` | PCB analysis, DRC parsing, layout review | Layout, DRC Gate |
| Manufacturing Engineer | `jlcpcb`, `pcbway`, `bom`, `kidoc` | DFM rules, BOM management, manufacturing docs | DFM/DFA, Prototype, Production Release |
| Compliance Engineer | `emc`, `kidoc` | EMC pre-compliance analysis, regulatory documentation | Compliance |
| Test Engineer | `kicad` (optional) | Test point locations, connector pinouts, debug interfaces | Test Planning |
| HW Product Owner | (none directly) | Uses role outputs for trade-off decisions | N/A |

### Skill Count by Role

- Electrical Engineer: 6 skills
- PCB Layout Engineer: 1 skill
- Manufacturing Engineer: 3 skills (+ `kidoc` shared with Compliance)
- Compliance Engineer: 2 skills
- Test Engineer: 1 skill (optional -- falls back to artifact-based planning)
- **Total unique skills consumed: 11**

---

## 3. Dispatch Patterns per Skill

### 3.1 kicad-happy:kicad

**Consuming roles**: EE, PCB Layout, Test Engineer (optional)

**Dispatch pattern**:
```
Skill("kicad-happy:kicad")
```

**When to invoke**:
- EE: Schematic analysis during Schematic stage
- PCB Layout: PCB analysis and DRC parsing during Layout stage
- Test Engineer: Reading test points and debug interfaces (optional; falls back to artifacts)

**Expected input**: KiCad project path (`.kicad_pro`, `.kicad_sch`, or `.kicad_pcb` file)

**Expected output (schematic analysis)**:
| Field | Type | Description |
|---|---|---|
| `findings[]` | array of objects | Each: `id` (string), `severity` (enum: critical/major/minor/info), `category` (string), `component` (string), `net` (string), `description` (string) |
| `summary.total_findings` | integer | Total finding count |
| `summary.by_severity` | object | Counts keyed by severity level |

**Expected output (PCB/DRC analysis)**:
| Field | Type | Description |
|---|---|---|
| `drc_results[]` | array of objects | Each: `rule_id` (string), `severity` (enum), `location` (string), `description` (string) |
| `board_stats` | object | Board dimensions, layer count, component count |

### 3.2 kicad-happy:spice

**Consuming role**: EE

**Dispatch pattern**:
```
Skill("kicad-happy:spice")
```

**When to invoke**: SPICE simulation needed during Schematic stage (filter verification, divider ratios, opamp gains, crystal load caps)

**Expected input**: KiCad schematic path with subcircuits to simulate

**Expected output**:
| Field | Type | Description |
|---|---|---|
| `simulations[]` | array of objects | Each: `subcircuit` (string), `type` (string), `result` (string), `pass` (boolean) |
| `summary.pass_count` | integer | Passing simulation count |
| `summary.fail_count` | integer | Failing simulation count |

### 3.3 kicad-happy:digikey / kicad-happy:mouser / kicad-happy:lcsc / kicad-happy:element14

**Consuming role**: EE

**Dispatch pattern** (one per distributor):
```
Skill("kicad-happy:digikey")
Skill("kicad-happy:mouser")
Skill("kicad-happy:lcsc")
Skill("kicad-happy:element14")
```

**When to invoke**: Component selection during Schematic stage. Query multiple distributors for pricing, availability, and datasheet retrieval.

**Expected input**: Component search query (keyword or MPN)

**Expected output** (same contract for all four):
| Field | Type | Description |
|---|---|---|
| `parts[]` | array of objects | Each: `mpn` (string), `description` (string), `price` (number or null), `stock` (integer), `datasheet_url` (string or null) |
| `query` | string | The search query that was executed |

### 3.4 kicad-happy:jlcpcb / kicad-happy:pcbway

**Consuming role**: Manufacturing Engineer

**Dispatch pattern**:
```
Skill("kicad-happy:jlcpcb")   # when target_fab = jlcpcb
Skill("kicad-happy:pcbway")   # when target_fab = pcbway
```

**When to invoke**: DFM validation during DFM/DFA stage. Fab selection driven by `.hardware/config.yml` `target_fab` setting.

**Expected input**: KiCad PCB file path and board parameters

**Expected output**:
| Field | Type | Description |
|---|---|---|
| `dfm_rules[]` | array of objects | Each: `rule_id` (string), `parameter` (string), `min_value` (number), `board_value` (number), `pass` (boolean) |
| `assembly_constraints` | object | Assembly-specific constraints (component placement, reflow, etc.) |

### 3.5 kicad-happy:bom

**Consuming role**: Manufacturing Engineer

**Dispatch pattern**:
```
Skill("kicad-happy:bom")
```

**When to invoke**: BOM validation during DFM/DFA stage; BOM finalization during Production Release stage.

**Expected input**: KiCad project path or BOM file

**Expected output**:
| Field | Type | Description |
|---|---|---|
| `bom_entries[]` | array of objects | Each: `ref` (string), `mpn` (string), `quantity` (integer), `unit_price` (number), `sources[]` (array of strings) |
| `total_cost` | number | Total BOM cost per unit |
| `single_source_items[]` | array of strings | Component refs with only one source |

### 3.6 kicad-happy:emc

**Consuming role**: Compliance Engineer

**Dispatch pattern**:
```
Skill("kicad-happy:emc")
```

**When to invoke**: EMC pre-compliance analysis during Compliance stage.

**Expected input**: KiCad PCB file path

**Expected output**:
| Field | Type | Description |
|---|---|---|
| `checks[]` | array of objects | Each: `rule_id` (string), `category` (string), `severity` (string), `description` (string), `location` (string) |
| `risk_score` | number | Overall EMC risk score |
| `summary` | object | Summary statistics by category and severity |

### 3.7 kicad-happy:kidoc

**Consuming roles**: Compliance Engineer, Manufacturing Engineer

**Dispatch pattern**:
```
Skill("kicad-happy:kidoc")
```

**When to invoke**:
- Compliance Engineer: Regulatory documentation generation during Compliance stage
- Manufacturing Engineer: Manufacturing transfer package during Production Release stage

**Expected input**: KiCad project path and document type specification

**Expected output**:
| Field | Type | Description |
|---|---|---|
| `document` | object | Fields: `title` (string), `sections[]` (array of objects), `format` (string) |
| `generation_status` | enum | One of: `success`, `partial`, `failed` |

---

## 4. Output Contract Validation Protocol

After invoking ANY kicad-happy skill, the role sub-agent MUST validate the output before processing:

1. **Check top-level fields** are present (per the contracts in Section 3)
2. **Check array fields** are arrays (not null, not strings)
3. **Check array elements** contain required sub-fields
4. **If validation passes**: proceed with processing
5. **If validation fails**: report `HW-KCH-004: CONTRACT_MISMATCH` with:
   - Which skill was invoked
   - The contract version (1.0) and target kicad-happy version (>=1.2.x)
   - The installed kicad-happy version (if known from SessionStart hook)
   - Which fields are missing or have unexpected types
   - The raw output (first 500 characters) for diagnostic context
   - Do NOT process malformed data
   - Continue the stage with degraded capability (same as SKILL_UNAVAILABLE)

---

## 5. Error Handling

### 5.1 Skill Not Installed (HW-KCH-001)

When a kicad-happy skill is not installed, the Skill tool returns an error. The sub-agent reports:

```
SKILL_UNAVAILABLE: kicad-happy:<skill-name>
Required for: <purpose> during <stage> stage
Install: Install kicad-happy via Claude Code plugin system
Impact: <what cannot be done>. <fallback behavior>.
```

The pipeline does NOT crash. The sub-agent documents what it could not do and the gate evaluates on available data.

### 5.2 Version Mismatch (HW-KCH-002)

The SessionStart hook (`check_kicad_happy.py`) compares the installed kicad-happy version against the `dependencies.kicad_happy_version` field in `.hardware/config.yml`. On mismatch:

```
kicad-happy version X.Y.Z installed; hardware-team requires >=A.B.C.
```

This is a warning only. The pipeline continues but output contract mismatches are more likely.

### 5.3 Invocation Error (HW-KCH-003)

If a kicad-happy skill invocation errors at runtime (not missing, but fails during execution), the sub-agent reports the error in its output and the gate evaluates on available data.

### 5.4 Contract Mismatch (HW-KCH-004)

See Section 4 above. The sub-agent does NOT process malformed data. This catches silent interface drift between kicad-happy versions.

### Error Code Summary

| Code | Condition | Severity | Response |
|---|---|---|---|
| `HW-KCH-001` | Skill not installed | Major | SKILL_UNAVAILABLE signal, graceful degradation |
| `HW-KCH-002` | Version mismatch | Warning | Warn at session start, pipeline continues |
| `HW-KCH-003` | Skill invocation error | Major | Report error, gate evaluates on available data |
| `HW-KCH-004` | Output contract mismatch | Major | CONTRACT_MISMATCH signal, do not process data |

---

## 6. Reimplementation Definition (NFR-003)

A capability is **reimplemented** if a hardware-team role performs an action that would produce the same output as invoking a kicad-happy skill, without invoking that skill.

### IS Reimplementation (Prohibited)

- Parsing `.kicad_sch` files to extract BOM data instead of invoking `kicad-happy:kicad`
- Querying the DigiKey API directly instead of invoking `kicad-happy:digikey`
- Implementing EMC rule checks from scratch instead of invoking `kicad-happy:emc`
- Writing SPICE netlists and running simulations instead of invoking `kicad-happy:spice`
- Generating DFM rule checks for JLCPCB instead of invoking `kicad-happy:jlcpcb`
- Building BOM tables by parsing schematics instead of invoking `kicad-happy:bom`
- Generating engineering documents from scratch instead of invoking `kicad-happy:kidoc`

### IS NOT Reimplementation (Permitted)

- SKILL.md containing domain knowledge that guides **when/how** to invoke a kicad-happy skill
- Interpreting kicad-happy output and making engineering judgments about it
- Combining outputs from multiple kicad-happy skills into a unified report
- A review checklist item (e.g., "check capacitor derating") that triggers a kicad-happy invocation
- Validating kicad-happy output against contracts (Section 4) -- this is structural validation, not reimplementation
- Adding hardware-team-specific context to kicad-happy results (e.g., linking findings to pipeline stages)

### The Bright Line

If the action requires calling an external API, parsing a KiCad file format, or implementing domain-specific analysis rules that kicad-happy already provides, it is reimplementation. If the action is about orchestration, judgment, or context enrichment, it is not.

---

## 7. Contract Update Procedure

When kicad-happy releases a new version:

1. Run the test fixture against the new kicad-happy version
2. If HW-KCH-004 fires for any contract: the new version has a breaking change
3. Update contracts in this file (Section 3) to match the new output structure
4. Increment the contract version for each updated contract
5. Update the target kicad-happy version range
6. Document the change in the architecture changelog

This is a documentation-level maintenance loop -- no code changes required unless field semantics change.

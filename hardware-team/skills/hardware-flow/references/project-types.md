# Hardware Project Type Detection and Routing

> **Runtime detection is mandatory.** Project type is a **per-run** routing
> decision. Detection runs on **every** pipeline invocation against the current
> user request and project context. The config file does NOT pin the project
> type. Use `routing.force_type` in `.hardware/config.yml` as an opt-in
> override for repos that genuinely need an intentional pin.

## Detection Matrix

Classify every user request into one of the following hardware project types before pipeline execution begins. Classification drives stage routing, agent selection, and gate depth.

---

### PROTOTYPE

- **Signals**: "prototype", "proof of concept", "breadboard", "dev board", "evaluation board", "one-off", "first revision", "Rev A", "just get it working", "hobby project", "personal project", "maker project", "Arduino", "Raspberry Pi"
- **Confidence boosters**: No mention of volume or production, single quantity implied, hand-soldering mentioned, through-hole components preferred, no compliance requirements mentioned
- **Confidence reducers**: Mentions production volume, regulatory certification, manufacturing transfer, yield targets

### PRODUCTION

- **Signals**: "production", "mass production", "volume manufacturing", "1000+", "production run", "manufacturing transfer", "contract manufacturer", "CM", "production BOM", "production test", "yield", "first article inspection", "FAI"
- **Confidence boosters**: Specific volume numbers (>100 units), mentions CM/EMS, discusses yield targets, references production test fixtures, mentions cost-per-unit optimization
- **Confidence reducers**: "just one", "prototype", "breadboard", "quick test", no volume mentioned

### HOBBY

- **Signals**: "hobby", "fun project", "learning", "experiment", "personal", "just for me", "weekend project", "maker", "tinker", "play with", "try out"
- **Confidence boosters**: No deadline mentioned, no budget constraints, learning-oriented language, mentions breadboard or perfboard, no compliance requirements
- **Confidence reducers**: Client or customer mentioned, production intent, regulatory requirements, commercial use

### CERTIFIED

- **Signals**: "certification", "FCC", "CE mark", "UL", "IEC", "medical device", "automotive", "IATF", "ISO 13485", "DO-254", "avionics", "Class II", "Class III", "safety-critical", "SIL", "ASIL"
- **Confidence boosters**: Specific standard numbers cited, mentions pre-compliance testing, references test labs, regulatory timeline discussed, safety analysis required
- **Confidence reducers**: "no compliance needed", "hobby", "just for me", "prototype only"

---

## Signal Table

Quick-reference keyword and context clue lookup for detection.

| Signal Keyword/Phrase | Primary Type | Secondary Type | Notes |
|----------------------|-------------|----------------|-------|
| "prototype" | PROTOTYPE | -- | Default if ambiguous |
| "breadboard" | PROTOTYPE | HOBBY | Context determines: learning = HOBBY |
| "production run" | PRODUCTION | -- | Strong signal |
| "1000 units" | PRODUCTION | -- | Volume >100 = PRODUCTION signal |
| "50 units" | PRODUCTION | PROTOTYPE | Ambiguous; check other signals |
| "just for me" | HOBBY | -- | Strong personal-use signal |
| "FCC certification" | CERTIFIED | PRODUCTION | Certification implies production path |
| "CE mark" | CERTIFIED | PRODUCTION | Regulatory implies full pipeline |
| "medical device" | CERTIFIED | -- | Very strong CERTIFIED signal |
| "Rev A" | PROTOTYPE | -- | First revision = prototyping |
| "Rev C" | PRODUCTION | PROTOTYPE | Later revisions suggest maturity |
| "cost optimization" | PRODUCTION | -- | Cost focus = volume intent |
| "learning project" | HOBBY | -- | Educational intent |
| "client project" | PRODUCTION | CERTIFIED | Commercial = at least PRODUCTION |
| "safety-critical" | CERTIFIED | -- | Absolute CERTIFIED signal |
| "maker project" | HOBBY | PROTOTYPE | Context determines |
| "contract manufacturer" | PRODUCTION | CERTIFIED | CM involvement = production |
| "hand solder" | PROTOTYPE | HOBBY | Manual assembly = low volume |
| "reflow oven" | PRODUCTION | PROTOTYPE | Reflow = manufacturing process |
| "test fixture" | PRODUCTION | CERTIFIED | Production test infrastructure |

---

## Disambiguation Rules

1. **CERTIFIED always wins** when regulatory/safety signals are present. A "prototype for a medical device" is CERTIFIED (the pipeline must enforce compliance from the start, even at prototype stage).
2. **PRODUCTION vs PROTOTYPE**: If volume >100 units is mentioned, default to PRODUCTION. If volume is 1-10, default to PROTOTYPE.
3. **HOBBY vs PROTOTYPE**: If learning/personal signals dominate and there is no external stakeholder, default to HOBBY. If the user describes a functional goal (not just learning), default to PROTOTYPE.
4. **Conflicting signals require clarification**: When signals for multiple types are equally strong, ask: "Is this for personal learning, a working prototype, production manufacturing, or a certified product?"
5. **Client/commercial context escalates**: Any mention of clients, customers, or commercial sale escalates HOBBY to PROTOTYPE and PROTOTYPE to PRODUCTION at minimum.

---

## Stage Routing Matrix

Each cell defines the execution depth for that stage given the project type.

| Stage | HOBBY | PROTOTYPE | PRODUCTION | CERTIFIED |
|-------|-------|-----------|------------|-----------|
| 1. Concept | light | full | full | full |
| 2. Schematic | light | full | full | full |
| 3. Layout | light | full | full | full |
| 4. Prototype | full | full | full | full |
| 5. DFM/DFA | skip | light | full | full |
| 6. Compliance | skip | skip | full | full + extended |
| 7. Pilot Run | skip | skip | full | full |
| 8. Production Release | skip | skip | full | full |

### Notes on Routing

- **HOBBY** skips all post-prototype stages. The goal is a working board, not a product.
- **PROTOTYPE** skips compliance and production stages. DFM/DFA runs at light depth to catch obvious manufacturability issues early.
- **PRODUCTION** runs all 8 stages at full depth. This is the standard path for commercial hardware.
- **CERTIFIED** runs all 8 stages at full depth. Compliance stage runs at **extended** depth with additional evidence collection, standards traceability, and test lab preparation artifacts.

---

## Stage Depth Definitions

### Full

- All agents invoked (primary + supporting roles)
- All collaboration patterns run (evaluator-optimizer, adversarial review, DRB, BOM reconciliation, consensus as applicable)
- Full quality gate evaluation with all criteria at all severity levels (blocking, warning, suggestion)
- Self-correction enabled with maximum 3 iterations before escalation
- All kicad-happy skills invoked as mapped in `kicad-integration.md`

### Light

- Primary agent only -- no supporting agents spawned
- No adversarial review or DRB patterns executed
- Evaluator-optimizer loop still runs (always runs)
- Simplified quality gate: evaluate blocking criteria only, skip warnings and suggestions
- Self-correction enabled with maximum 2 iterations before escalation
- kicad-happy skills invoked only for primary analysis (e.g., kicad:kicad for schematic analysis, skip sourcing comparison)

### Skip

- Stage does not execute at all
- Pipeline advances directly to the next non-skipped stage
- Downstream stages receive whatever upstream artifacts are available (may be fewer than in full runs)
- No gate evaluation, no artifacts produced for this stage

### Full + Extended (CERTIFIED only)

Everything in Full, plus certification-specific augmentations:

- **Compliance stage**: Extended evidence collection for each applicable standard. Test plan generation for pre-compliance lab testing. Standards traceability matrix linking every requirement to a design artifact and test evidence.
- **DFM/DFA stage**: Extended yield analysis with statistical process control targets. Component qualification requirements per applicable standards.
- **Concept stage**: Regulatory scan produces a full standards applicability matrix (not just a checklist).
- **Production Release stage**: Full manufacturing transfer package with compliance documentation, test procedures, and qualification records.

---

## Force-Type Override

To pin the project type (rare, intentional use only):

```yaml
# .hardware/config.yml
routing:
  force_type: CERTIFIED   # Forces CERTIFIED routing on every run
```

When `routing.force_type` is set:
- Detection still runs and is logged (for audit trail)
- Routing uses the forced type instead of detected type
- A banner announces the override on every run: `"Project type forced to CERTIFIED (routing.force_type). Detected type was PROTOTYPE."`
- This is the ONLY supported way to pin the type

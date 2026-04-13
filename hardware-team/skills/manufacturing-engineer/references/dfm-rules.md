# DFM Rule Framework

This reference defines the Design for Manufacturing (DFM) rule categories, severity classification, and fab-specific rule sets used by the Manufacturing Engineer during DFM review.

## Rule Categories

DFM rules are organized into 10 categories. Each category contains multiple parameters that must be validated against the target fabrication house capabilities.

### 1. Trace Geometry
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Minimum trace width | Narrowest copper trace on any layer | 3.5mil (JLCPCB std) -- 6mil (conservative) |
| Minimum trace spacing | Narrowest gap between copper features | 3.5mil (JLCPCB std) -- 6mil (conservative) |
| Minimum trace-to-pad clearance | Gap between trace and non-connected pad | 4mil -- 8mil |
| Minimum trace-to-board-edge clearance | Gap between trace and board outline | 10mil -- 20mil |

### 2. Via Specifications
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Minimum via diameter (finished hole) | Smallest plated-through hole | 0.2mm (JLCPCB std) -- 0.3mm (conservative) |
| Minimum annular ring | Copper ring around via | 0.13mm (JLCPCB std) -- 0.15mm |
| Maximum drill aspect ratio | Depth-to-diameter ratio | 8:1 (standard) -- 10:1 (advanced) |
| Via-to-via spacing | Center-to-center or edge-to-edge | 0.254mm minimum |
| Via-in-pad | Allowed if filled and capped (increased cost) | Fab-dependent |

### 3. Drill Specifications
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Minimum drill size (PTH) | Smallest plated through-hole | 0.2mm -- 0.3mm |
| Minimum drill size (NPTH) | Smallest non-plated hole | 0.5mm -- 0.8mm |
| Drill-to-copper clearance | Non-connected copper to hole edge | 0.2mm -- 0.25mm |
| Slot width minimum | Minimum routed slot width | 0.8mm -- 1.0mm |

### 4. Layer Stack and Copper
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Layer count | Total copper layers | 1, 2, 4, 6, 8 (fab-dependent max) |
| Copper weight (outer layers) | Copper thickness in oz/ft2 | 1oz (standard), 2oz (power) |
| Copper weight (inner layers) | Copper thickness in oz/ft2 | 0.5oz -- 1oz |
| Minimum copper-to-edge clearance | Copper features to board edge | 0.2mm -- 0.5mm |

### 5. Solder Mask and Silkscreen
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Solder mask minimum web | Narrowest mask bridge between pads | 3mil -- 4mil |
| Solder mask expansion | Mask opening larger than pad | 2mil -- 3mil per side |
| Solder mask-to-trace clearance | Gap between mask opening and trace | 2mil |
| Silkscreen minimum line width | Narrowest silkscreen stroke | 5mil -- 6mil |
| Silkscreen minimum text height | Smallest readable text | 30mil -- 40mil |
| Silkscreen-to-pad clearance | Gap between silkscreen and exposed pad | 4mil -- 6mil |

### 6. Surface Finish
| Finish | Shelf Life | Flatness | Cost | Use Case |
|--------|-----------|----------|------|----------|
| HASL (leaded) | 12+ months | Moderate | Low | General purpose, non-RoHS |
| HASL (lead-free) | 12+ months | Moderate | Low | General purpose, RoHS |
| ENIG | 12+ months | Excellent | High | Fine-pitch, BGA, gold wire bond |
| OSP | 6 months | Good | Low | High-volume, short shelf life OK |
| Immersion Silver | 6 months | Good | Medium | High-frequency, press-fit |
| Immersion Tin | 6 months | Good | Medium | Press-fit connectors |

### 7. Board Outline and Mechanical
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Board outline tolerance | Dimensional accuracy of board edges | +/-0.1mm (routed), +/-0.3mm (V-score) |
| Minimum board dimension | Smallest board edge | 6mm x 6mm (JLCPCB) |
| Maximum board dimension | Largest single board | 500mm x 500mm (fab-dependent) |
| Board thickness tolerance | Accuracy of overall thickness | +/-10% |
| Castellated holes | Half-vias on board edge | Minimum 0.6mm hole, 0.35mm pad ring |

### 8. Impedance Control
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Impedance tolerance | Accuracy of controlled impedance | +/-10% (standard), +/-5% (precision) |
| Minimum impedance trace width | For controlled impedance traces | Stackup-dependent |
| Differential pair spacing tolerance | Matching of differential pairs | +/-10% |

### 9. Special Features
| Feature | DFM Impact | Notes |
|---------|-----------|-------|
| Blind vias | Increased cost, limited layer span | Layer 1-2 or 1-3 typical |
| Buried vias | Significantly increased cost | Inner layer spans only |
| Microvias | Laser-drilled, limited depth | 0.1mm typical, 1-layer span |
| Edge plating | Special process, limited fab support | Confirm fab capability first |
| Flex / rigid-flex | Specialized materials, limited fabs | Requires dedicated flex-capable fab |

### 10. Assembly-Related DFM
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Pad-to-pad spacing (different nets) | Clearance for solder bridging prevention | 6mil -- 8mil |
| Via-in-pad (assembly impact) | Risk of solder wicking into via | Must be filled and capped if under BGA |
| Thermal pad connections | Spoke-and-thermal relief vs direct | Thermal relief recommended for hand rework |
| Test pad accessibility | Probe-accessible pads for ICT | See test-point-coverage.md |

## Severity Classification

| Severity | Definition | Gate Impact |
|----------|-----------|-------------|
| Critical | Board cannot be fabricated, or fabrication would yield non-functional boards. Examples: trace width below fab absolute minimum, drill aspect ratio exceeds capability, unsupported layer count. | Blocks DFM Gate at ALL strictness levels |
| Major | Board can be fabricated but with yield risk, requires process exception, or incurs significant cost premium. Examples: trace width between absolute minimum and recommended minimum, via-in-pad without fill spec, impedance traces at tolerance boundary. | Blocks DFM Gate at standard and strict levels |
| Minor | Best practice deviation with negligible yield impact. Examples: silkscreen overlaps solder mask opening, non-optimal copper balance between layers, sub-optimal panelization. | Logged, does not block DFM Gate |

## Fab-Specific Rule Application

The MfgE does NOT maintain hardcoded fab rules. Instead:

1. **Determine target fab** from `.hardware/config.yml` (`fabrication.primary_fab`)
2. **Invoke the appropriate kicad-happy skill** (`kicad-happy:jlcpcb` or `kicad-happy:pcbway`)
3. **Receive fab-specific rules** as `dfm_rules[]` array
4. **Apply severity classification** using this framework
5. **Cross-reference** board design parameters against received rules

This approach ensures rules stay current with fab capabilities and avoids stale hardcoded values (NFR-003 compliance).

## Generic Fallback Rules

If kicad-happy fab skills are unavailable (`SKILL_UNAVAILABLE`), use these conservative generic minimums as a degraded-mode fallback. These are NOT authoritative -- they are last-resort values only.

| Parameter | Generic Minimum | Notes |
|-----------|----------------|-------|
| Trace width | 6mil / 0.15mm | Conservative for 2-layer boards |
| Trace spacing | 6mil / 0.15mm | Conservative for standard copper weight |
| Via diameter | 0.3mm | Standard mechanical via |
| Annular ring | 0.15mm | Conservative for standard process |
| Drill size (PTH) | 0.3mm | Standard mechanical drill |
| Drill aspect ratio | 8:1 | Standard process capability |
| Solder mask web | 4mil | Conservative for standard process |

Always report `USING_GENERIC_FALLBACK_RULES` in the DFM report when these values are used instead of fab-specific rules.

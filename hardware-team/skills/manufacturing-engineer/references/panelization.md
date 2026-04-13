# Panel Design Patterns

This reference defines panel design guidelines, breakaway methods, fiducial and tooling hole requirements, and utilization calculations used by the Manufacturing Engineer during panelization review.

## Panel Design Fundamentals

A panel (also called an array) groups multiple copies of a PCB for efficient manufacturing. The assembly house processes panels, not individual boards. Panel design directly affects manufacturing cost, yield, and assembly throughput.

### Panel Structure

```
+-------------------------------------------------------+
|  [TH]                                            [TH] |  <-- Tooling holes
|     [GF]                                    [GF]      |  <-- Global fiducials
|  +----------+  +----------+  +----------+             |
|  |  Board 1 |  |  Board 2 |  |  Board 3 |             |
|  |    [LF]  |  |    [LF]  |  |    [LF]  |             |
|  +----------+  +----------+  +----------+             |
|  +----------+  +----------+  +----------+             |
|  |  Board 4 |  |  Board 5 |  |  Board 6 |             |
|  |    [LF]  |  |    [LF]  |  |    [LF]  |             |
|  +----------+  +----------+  +----------+             |
|     [GF]                                    [GF]      |
|  [TH]              [TH]                     [TH]      |
+-------------------------------------------------------+
        Edge rail (clamping area -- no components)

TH = Tooling hole    GF = Global fiducial    LF = Local fiducial
```

## Breakaway Methods

### V-Score

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| Board shape | Rectangular only | V-score runs full panel width; cannot score partial lines |
| Score depth | 1/3 board thickness per side (standard) | Deeper = easier break, more edge roughness |
| Score-to-component | Minimum 1.0mm from score line to nearest component | Breakaway stress can crack ceramic components |
| Score-to-trace | Minimum 0.5mm from score line to nearest copper | Score blade may damage traces within clearance zone |
| Board thickness | 0.8mm -- 2.0mm recommended | Thinner boards may break during handling; thicker boards are hard to break |
| Edge quality | Rough break edge with protruding glass fibers | Not suitable for tight-tolerance enclosure fit |

**Best for:** Rectangular boards, no components near edges, cost-sensitive production.

### Tab-Routed (Mouse Bites)

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| Tab width | 2.0mm -- 5.0mm | Wider = stronger during assembly, harder to remove |
| Tab count per edge | Minimum 2 per long edge; 1 per short edge (>30mm) | Ensures panel rigidity during assembly |
| Mouse bite holes | 5 holes at 0.5mm diameter, 0.7mm pitch (typical) | Perforated break line within the tab |
| Tab-to-component | Minimum 2.0mm from tab edge to nearest component | Tab removal creates mechanical stress |
| Tab placement | Avoid placing tabs near traces, vias, or copper pour | Tab removal can tear copper near the tab |
| Edge quality | Requires filing/sanding for smooth finish | Tab stubs remain after break; may need post-processing |

**Best for:** Non-rectangular boards, boards with edge-mounted components, tight enclosure tolerances.

### Combination (V-Score + Tab)

Use V-score on straight edges and tabs on irregular sections. Increases panel complexity but maximizes flexibility.

## Edge Rails

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| Rail width | 5.0mm minimum (standard); 8.0mm for heavy boards | Conveyor clamp contact area |
| Rail placement | Top and bottom of panel (along conveyor travel direction) | Some assembly houses require rails on all 4 sides |
| Component clearance | No components within 3.0mm of rail inner edge | Conveyor clamp interference |
| Rail copper | Hatched ground copper on rails for thermal balance | Prevents panel warp during reflow |
| Rail fiducials | Global fiducials placed on rails (see Fiducials section) | Pick-and-place alignment reference |

## Fiducials

### Global Fiducials (Panel-Level)

| Parameter | Requirement |
|-----------|-------------|
| Count | Minimum 3 (2 diagonal + 1 for rotation detection) |
| Shape | Circular copper pad, no solder mask |
| Diameter | 1.0mm pad with 2.0mm solder mask opening (clearance ring) |
| Placement | Asymmetric -- NOT in a symmetric pattern (enables rotation detection) |
| Location | On edge rails, at least 5mm from panel edge |

### Local Fiducials (Board-Level)

| Parameter | Requirement |
|-----------|-------------|
| Count | Minimum 2 per board (for fine-pitch and BGA assembly) |
| Shape | Same as global fiducials |
| Diameter | 1.0mm pad with 2.0mm solder mask opening |
| Placement | Diagonal corners of the board, outside component area |
| When required | Fine-pitch components (<0.5mm pitch), BGA, QFN |

## Tooling Holes

| Parameter | Requirement |
|-----------|-------------|
| Count | Minimum 3 (2 diagonal + 1 for orientation) |
| Diameter | 3.2mm (standard pin) or per assembly house specification |
| Type | Non-plated through-hole (NPTH) |
| Placement | On edge rails, away from fiducials |
| Tolerance | +0.05mm / -0.00mm (slip fit for tooling pins) |

## Utilization Calculation

Panel utilization measures how efficiently the panel area is used for actual boards.

```
Utilization (%) = (Board area x Board count) / (Panel area) x 100

Where:
  Board area = Single board width x height
  Board count = Number of boards in the panel
  Panel area = Panel width x height (including rails)
```

| Utilization | Rating | Action |
|-------------|--------|--------|
| >80% | Excellent | No action needed |
| 70-80% | Good | Acceptable; consider rotating or rearranging |
| 60-70% | Fair | Rearrange boards or adjust panel size |
| <60% | Poor | Redesign panel layout; consider different panel size or board rotation |

## Fab-Specific Panel Constraints

### JLCPCB
| Parameter | Value |
|-----------|-------|
| Maximum panel size | 400mm x 500mm |
| Minimum panel size | 70mm x 70mm |
| Standard rail width | 5mm |
| Maximum boards per panel | Limited by panel area and minimum spacing |
| Panelization service | Available (JLCPCB can panelize) |

### PCBWay
| Parameter | Value |
|-----------|-------|
| Maximum panel size | 500mm x 600mm |
| Minimum panel size | 50mm x 50mm |
| Standard rail width | 5mm -- 8mm |
| Maximum boards per panel | Limited by panel area |
| Panelization service | Available (customer-supplied or PCBWay-designed) |

**Note:** These values are reference baselines. Always invoke `kicad-happy:jlcpcb` or `kicad-happy:pcbway` for current fab-specific constraints. Do NOT rely on these values as authoritative.

## Panel Design Checklist

- [ ] Breakaway method selected (V-score, tab-route, or combination)
- [ ] Board-to-board spacing adequate for breakaway method
- [ ] Edge rails present with adequate width
- [ ] Global fiducials placed asymmetrically on rails (minimum 3)
- [ ] Local fiducials placed on each board (if fine-pitch/BGA present)
- [ ] Tooling holes placed on rails (minimum 3, NPTH)
- [ ] No components within clearance zone of breakaway lines
- [ ] No traces within clearance zone of V-score lines
- [ ] Panel utilization calculated and acceptable (>70%)
- [ ] Panel size within fab house maximum
- [ ] Copper balance considered (hatched copper on rails/waste areas)

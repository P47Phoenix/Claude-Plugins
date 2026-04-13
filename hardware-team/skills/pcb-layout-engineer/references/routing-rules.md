# Routing Guidelines and Impedance Control

Reference document for the PCB Layout Engineer role. Load this file for routing-review and layout-review tasks.

---

## 1. Impedance Control

### 1.1 Common Impedance Targets

| Signal Type | Typical Z0 | Tolerance | Notes |
|------------|-----------|-----------|-------|
| USB 2.0 (differential) | 90 ohm | +/- 10% | Differential pair |
| USB 3.x (differential) | 85 ohm | +/- 10% | Tighter routing required |
| HDMI (differential) | 100 ohm | +/- 10% | Length matching critical |
| Ethernet 100BASE-TX | 100 ohm | +/- 10% | Differential pair |
| Ethernet 1000BASE-T | 100 ohm | +/- 10% | All 4 pairs matched |
| PCIe (differential) | 85 ohm | +/- 10% | Per-lane length matching |
| DDR4 (single-ended) | 40 ohm | +/- 10% | Fly-by topology |
| DDR4 (differential, CLK) | 80 ohm | +/- 10% | Clock pair |
| LVDS (differential) | 100 ohm | +/- 10% | Point-to-point |
| SPI/I2C/UART | 50 ohm (optional) | Relaxed | Short runs may not need control |
| General GPIO | 50 ohm (optional) | Relaxed | Control if trace > 2 inches |

### 1.2 Microstrip Impedance (Outer Layers)

Approximate formula for single-ended microstrip:

```
Z0 = (87 / sqrt(Er + 1.41)) * ln(5.98 * H / (0.8 * W + T))
```

Where:
- Er = dielectric constant of substrate
- H = dielectric height (trace to reference plane)
- W = trace width
- T = copper thickness

**Always validate with a field solver or the fab house's impedance calculator.** Formulas provide estimates for feasibility; the fab house's stackup-specific calculations are authoritative.

### 1.3 Differential Pair Impedance

Approximate formula for edge-coupled differential microstrip:

```
Zdiff = 2 * Z0 * (1 - 0.48 * exp(-0.96 * S / H))
```

Where:
- Z0 = single-ended impedance of one trace
- S = spacing between traces in the pair
- H = dielectric height

### 1.4 Impedance Control Checklist

- [ ] All controlled-impedance nets identified and assigned to net classes
- [ ] Trace widths calculated per stackup (reference stackup-specification.md)
- [ ] Differential pairs routed with consistent spacing (edge-coupled)
- [ ] No reference plane voids under controlled-impedance traces
- [ ] Via transitions include return path vias (stitching vias near signal vias)
- [ ] Impedance test coupons specified for fab (if required)

---

## 2. Differential Pair Routing

### 2.1 Rules

| Rule | Guideline | Rationale |
|------|-----------|-----------|
| Intra-pair spacing | Maintain constant spacing (S) along entire route | Impedance depends on coupling; spacing changes cause impedance discontinuities |
| Length matching | Match P and N within tolerance per protocol | Skew converts differential to common-mode, increasing EMI and degrading signal |
| Symmetry at pads | Route both traces symmetrically into component pads | Asymmetric pad entry causes localized impedance mismatch |
| Layer transitions | Both traces via together; add return path stitching via | Maintain coupling and reference plane continuity through layer changes |
| Bends | Use arc or mitered 45-degree bends; no 90-degree bends | 90-degree bends cause impedance discontinuities |
| Breakout | Neck-down at BGA/fine-pitch pads is acceptable if minimized | Keep necked region as short as possible (<2mm) |

### 2.2 Length Matching Tolerances

| Protocol | Max Intra-Pair Skew | Max Inter-Pair Skew | Notes |
|----------|---------------------|---------------------|-------|
| USB 2.0 | +/- 5 mil | N/A | Single pair |
| USB 3.x | +/- 5 mil | +/- 100 mil (TX/RX) | TX and RX are independent pairs |
| HDMI | +/- 5 mil intra-pair | +/- 50 mil inter-channel | 3 data + 1 clock channel |
| PCIe | +/- 5 mil | +/- 500 mil per lane | Lane-to-lane matching relaxed |
| DDR4 DQ | N/A | Match to strobe within byte lane | Fly-by topology |
| DDR4 CLK | +/- 5 mil | Match to DQ group | Differential clock |
| Ethernet | +/- 5 mil | N/A (per pair) | Each pair is independent |
| LVDS | +/- 5 mil | Application-dependent | Point-to-point |

---

## 3. Return Path Continuity

### 3.1 The Golden Rule

Every signal trace needs a continuous, low-impedance return path on its reference plane. Violations of this rule cause:
- Increased loop area (higher EMI radiation)
- Impedance discontinuities (signal reflections)
- Crosstalk between signals sharing the disturbed return path

### 3.2 Common Violations

| Violation | Impact | Fix |
|-----------|--------|-----|
| Trace crossing a plane split | Return current must detour around the split; massive loop area increase | Route trace on a different layer or bridge the split with a decoupling cap |
| Via transition without stitching via | Return current on plane has no via to follow signal to new reference plane | Add stitching via within 1mm of signal via, connecting the two reference planes |
| Signal routed over a void in the reference plane | Same as crossing a split | Re-route signal or fill the void |
| Power plane used as reference but has islands | Return current cannot flow through island boundaries | Use ground plane as reference; avoid power plane references for high-speed signals |

### 3.3 Stitching Via Requirements

- Place a return path stitching via within 1mm of every signal via that changes reference planes
- For differential pairs, place the stitching via between the two signal vias (equidistant)
- For via fences (guard vias around sensitive signals), space vias at lambda/20 or closer

---

## 4. Current Capacity (IPC-2152)

### 4.1 Trace Width vs. Current (1oz copper, outer layer, 10C rise)

| Current (A) | Minimum Width (mil) | Notes |
|------------|--------------------| ------|
| 0.5 | 10 | Most signal traces adequate |
| 1.0 | 20 | Low-power supply traces |
| 2.0 | 50 | Moderate power |
| 3.0 | 80 | Power distribution |
| 5.0 | 150 | Heavy power; consider polygon pour |
| 10.0 | 400 | Use copper pour, not trace |

**Notes:**
- Inner layer traces have approximately 50% the current capacity of outer layer traces (less convective cooling)
- Increase width by 50% for inner layers at the same current
- Temperature rise is cumulative -- adjacent high-current traces compound heating
- Always check via current capacity separately (via diameter and plating thickness)

### 4.2 Via Current Capacity

| Via Drill (mm) | Plating (um) | Approx. Current (A) | Notes |
|----------------|-------------|---------------------|-------|
| 0.3 | 25 | 0.5 | Standard microvia |
| 0.4 | 25 | 0.7 | Small through-hole |
| 0.5 | 25 | 1.0 | Standard through-hole |
| 0.8 | 25 | 1.5 | Large through-hole |
| 1.0 | 25 | 2.0 | Power via |

For higher currents, use multiple vias in parallel (via arrays on power connections).

---

## 5. Crosstalk Management

### 5.1 Spacing Rules

| Rule | Application | Guideline |
|------|------------|-----------|
| 3W rule | General signal spacing | Edge-to-edge spacing >= 2x trace width (center-to-center = 3x width) |
| 5W rule | Critical/sensitive signals | Edge-to-edge spacing >= 4x trace width for clock, reset, analog signals |
| Guard trace | Ultra-sensitive signals | Grounded guard trace with via stitching between aggressor and victim |

### 5.2 Layer-to-Layer Crosstalk

- Broadside coupling (traces on adjacent layers, overlapping) is stronger than edge coupling (traces on same layer, side by side)
- Avoid routing parallel traces on adjacent signal layers in the same direction
- Prefer orthogonal routing on adjacent layers (horizontal on one layer, vertical on the next)

---

## 6. Via Usage Guidelines

| Via Type | When to Use | Constraints |
|----------|------------|-------------|
| Through-hole | Default for most signals | Consumes all layers; uses routing space on every layer |
| Blind (L1-L2, L1-L3) | BGA breakout, HDI designs | Requires sequential lamination; check fab capability |
| Buried (L2-L3) | Internal layer connections in HDI | Requires sequential lamination; higher cost |
| Microvia (laser-drilled) | Fine-pitch BGA breakout | Typically 1-layer span only; aspect ratio limited |
| Via-in-pad (filled/capped) | Thermal pads, fine-pitch pads | Requires via filling; check fab capability and cost |

### 6.1 Via-to-Trace Transition

- Route trace from pad to via, then through via to internal/other layer
- Pad entry should be symmetric for differential pairs
- Avoid long stubs from unused via spans (back-drilling for high-speed signals >5 GHz)

---

## 7. Routing Review Checklist

Use this checklist during routing-review tasks:

- [ ] All controlled-impedance traces match calculated widths from stackup
- [ ] Differential pairs maintain constant spacing throughout route
- [ ] Differential pair length matching within protocol tolerance
- [ ] No traces crossing reference plane splits or voids
- [ ] Stitching vias placed near every signal via that changes reference planes
- [ ] Power traces sized for expected current (IPC-2152)
- [ ] Via current capacity adequate for power connections (use arrays if needed)
- [ ] Crosstalk spacing rules met for sensitive/high-speed signals
- [ ] No 90-degree bends on high-speed traces (use 45-degree or arcs)
- [ ] BGA breakout routing is feasible with available via technology
- [ ] Clock traces routed with shortest path, minimal vias, continuous reference
- [ ] Reset traces have adequate noise immunity (pull-up/pull-down, guard traces)
- [ ] Analog signals routed away from digital switching noise
- [ ] Test points accessible and connected with adequate trace width

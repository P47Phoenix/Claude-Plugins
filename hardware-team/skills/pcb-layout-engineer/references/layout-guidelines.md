# PCB Layout Best Practices

Reference document for the PCB Layout Engineer role. Load this file for layout-review and placement-analysis tasks.

---

## 1. Component Placement Rules

### 1.1 General Placement Strategy

1. **Place connectors first** -- connectors are mechanically constrained (board edge, panel cutouts, mating connectors) and anchor the rest of the layout
2. **Place power components second** -- voltage regulators, inductors, power FETs define thermal zones and set the power distribution topology
3. **Place critical ICs third** -- processors, FPGAs, ADCs/DACs, high-speed transceivers; these drive routing complexity
4. **Place support components last** -- decoupling caps, pull-ups, LEDs, test points fill remaining space

### 1.2 Decoupling Capacitor Placement

| Rule | Guideline | Rationale |
|------|-----------|-----------|
| Proximity | Decoupling caps within 2mm of IC power pin | Minimizes loop inductance of the decoupling path |
| Via placement | Via from cap pad directly to power/ground plane -- avoid routing through trace | Trace inductance defeats the capacitor's purpose |
| Grouping | Multiple caps per IC: bulk (10uF+) near IC, ceramic (100nF) at each power pin | Different caps handle different frequency ranges |
| Orientation | Cap body parallel to IC edge for shortest return path | Reduces parasitic loop area |

### 1.3 Crystal and Oscillator Placement

- Place crystal within 5mm of the IC clock pins
- No routing other than the crystal traces should pass under the crystal footprint
- Ground fill under crystal with via stitching to reduce noise coupling
- Keep crystal away from high-speed digital signals, switching regulators, and board edges

### 1.4 High-Speed Component Clustering

- Group components by signal domain (USB, Ethernet, DDR, PCIe) to minimize trace lengths
- Place series termination resistors at the source end, within 5mm of the driver pin
- Place AC coupling capacitors at the boundary between signal domains
- Maintain consistent reference plane under the entire signal path

### 1.5 Thermal Management

| Component Type | Thermal Guideline |
|---------------|-------------------|
| Voltage regulators | Place near board edge or with thermal via array to inner ground plane; maintain keep-out zone for airflow |
| Power MOSFETs | Thermal pad connected to ground plane via array of vias (minimum 4, prefer 9+) |
| High-power ICs | Exposed pad requires via array; check thermal resistance from datasheet |
| LEDs (high-power) | Copper pour on signal layer connected to thermal pad |

### 1.6 Mechanical Considerations

- **Board edge clearance**: No components within 1mm of board edge (2mm for wave solder)
- **Mounting hole clearance**: No components or traces within 3mm of mounting holes (5mm for grounded mounting)
- **Connector clearance**: Check mating connector housing dimensions; leave clearance for plug insertion/removal
- **Height restrictions**: Check enclosure height constraints; map tall components to unrestricted zones
- **Panel scoring/routing**: No components within 3mm of V-score or routing tab locations

---

## 2. Component Grouping Patterns

### 2.1 Functional Block Grouping

Group components into functional blocks matching the schematic hierarchy. Each block should be:
- Physically contiguous on the board
- Oriented with signal flow direction (input left/top, output right/bottom)
- Separated from other blocks by ground fill or keep-out zones for noise isolation

### 2.2 Analog/Digital Separation

- Separate analog and digital sections with a clear boundary
- Do NOT split the ground plane between analog and digital (single solid ground plane is preferred)
- Use component placement to create physical separation; route analog signals away from digital switching noise
- Place ADC/DAC converters at the analog-digital boundary

### 2.3 Power Supply Zones

- Each voltage regulator defines a power zone
- Input capacitors, output capacitors, and feedback resistors form a tight local group
- Switch-mode regulators need special attention: minimize the hot loop (switch node area)
- Keep sensitive analog circuits away from switching regulator zones

---

## 3. Board Area Estimation

| Complexity | Components/cm2 | Notes |
|-----------|----------------|-------|
| Low (through-hole heavy) | 0.5-1.0 | Single-sided, large packages |
| Medium (mixed SMD/TH) | 1.0-2.0 | Typical consumer electronics |
| High (SMD-dominant) | 2.0-4.0 | Dense embedded designs |
| Very high (BGA + fine-pitch) | 4.0-8.0 | Mobile, compute modules |

Use these estimates for early layout feasibility assessment. If actual density exceeds the target range, consider adding layers or increasing board size.

---

## 4. Keep-Out Zones

| Zone Type | Minimum Distance | Notes |
|-----------|-----------------|-------|
| Board edge (routed) | 0.5mm traces, 1mm components | Fab tolerance on routing |
| Board edge (V-score) | 3mm components | V-score stress can crack joints |
| Mounting hole (non-grounded) | 3mm traces and components | Screw/standoff clearance |
| Mounting hole (grounded) | 5mm components | Larger clearance for ground connection |
| Antenna area | Per antenna datasheet | Usually requires ground plane clearance on specific layers |
| High-voltage clearance | Per IPC-2221 / safety standard | Creepage and clearance per voltage rating |

---

## 5. Placement Review Checklist

Use this checklist during layout-review tasks:

- [ ] All decoupling caps within 2mm of their IC power pins
- [ ] Crystals/oscillators within 5mm of clock IC pins
- [ ] No traces routed under crystals except crystal traces
- [ ] Connectors at board edges with correct orientation
- [ ] Thermal components have adequate via arrays and copper area
- [ ] Component height map checked against enclosure constraints
- [ ] Mounting hole clearances respected
- [ ] Board edge clearances respected
- [ ] Analog and digital sections physically separated
- [ ] Switching regulator hot loops minimized
- [ ] High-speed components grouped by signal domain
- [ ] Signal flow direction is consistent (input to output)
- [ ] Test points accessible for probe contact
- [ ] Fiducials placed per assembly house requirements (if applicable)
- [ ] Polarity markings visible for polarized components

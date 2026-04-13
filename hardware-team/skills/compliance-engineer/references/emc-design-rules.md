# EMC Design Rules Reference

This reference provides EMC design rules and remediation patterns for the Compliance Engineer. These rules complement -- not replace -- the analysis performed by `kicad-happy:emc`. Use this reference to interpret kicad-happy:emc findings and recommend design changes.

## 1. Ground Plane Rules

### 1.1 Unbroken Ground Plane

**Rule:** Every signal layer must have an adjacent unbroken ground (or power) plane. Splits in ground planes create slot antennas that radiate.

**Severity if violated:** Critical (above 100 MHz signal content), Major (below 100 MHz)

**Remediation:**
- Remove ground plane splits under high-speed signal routes
- If splits are necessary for isolation (e.g., analog/digital), bridge with a narrow copper connection and route signals over the bridge point only
- Add stitching vias along both sides of any intentional split (max 1/20 wavelength spacing)

### 1.2 Ground Plane Stitching

**Rule:** Connect ground planes on different layers with stitching vias at regular intervals. Maximum spacing: lambda/20 at the highest frequency of concern.

**Remediation:** Add ground stitching vias around board perimeter and near connectors. For a 1 GHz design, maximum via spacing is approximately 15 mm.

## 2. Decoupling Rules

### 2.1 Capacitor Placement

**Rule:** Place decoupling capacitors as close as possible to IC power pins. The connection path (cap pad -> via -> power pin) must be minimized.

**Severity if violated:** Major

**Remediation:**
- Move capacitor to within 3 mm of the power pin (ideally within 1 mm for >100 MHz ICs)
- Use the shortest possible trace or direct via connection
- Place the via between the capacitor and the IC, not beyond the capacitor

### 2.2 Decoupling Strategy

**Rule:** Use a multi-value decoupling strategy: bulk (10-100 uF) for low-frequency noise, mid-range (100 nF) for general decoupling, small (1-10 nF) for high-frequency noise.

**Remediation:** Ensure each power domain has at least three decades of capacitance coverage. Check anti-resonance between parallel capacitor values.

## 3. I/O Filtering Rules

### 3.1 Connector Filtering

**Rule:** All I/O lines at board edge connectors must have EMI filtering (ferrite beads, common-mode chokes, or RC filters) appropriate to the signal type.

**Severity if violated:** Critical (unfiltered high-speed I/O), Major (unfiltered low-speed I/O)

**Remediation:**
- Add ferrite beads on power lines entering/exiting the board
- Add common-mode chokes on differential pairs (USB, Ethernet, HDMI)
- Add RC or LC filters on slow-speed signals (GPIO, analog inputs)

### 3.2 Cable Emission Control

**Rule:** Cables are the primary radiation antenna in most systems. Every cable interface must be evaluated for common-mode current.

**Remediation:** Ensure cable shields are terminated to chassis ground at the connector. For unshielded cables, add common-mode filtering at the board edge.

## 4. Clock and High-Speed Signal Rules

### 4.1 Clock Routing

**Rule:** Clock signals must be routed on internal layers with adjacent ground reference planes. Never route clocks on outer layers or across plane splits.

**Severity if violated:** Critical

**Remediation:**
- Move clock traces to inner layers
- Ensure continuous ground reference under entire clock trace length
- Keep clock traces short; avoid stubs
- Consider spread-spectrum clocking (SSC) to reduce peak emissions

### 4.2 Differential Pair Routing

**Rule:** Differential pairs must maintain consistent spacing (tightly coupled) and length matching within the specified skew budget.

**Severity if violated:** Major

**Remediation:**
- Match trace lengths within the pair to specification (typically < 5 mil for high-speed)
- Maintain constant spacing throughout the route
- Avoid routing differential pairs near board edges or plane boundaries

## 5. Board Edge and Radiation Rules

### 5.1 Trace Keepout at Board Edge

**Rule:** No signal traces within 40 mil (1 mm) of the board edge. High-speed traces should be at least 3x this distance from the edge.

**Severity if violated:** Major

**Remediation:** Move traces inward. Add ground stitching vias along the board perimeter to create a Faraday cage effect.

### 5.2 Component Placement

**Rule:** Place high-frequency components (oscillators, switching regulators, high-speed ICs) away from board edges and I/O connectors.

**Remediation:** Centralize noisy components. Create a "quiet zone" near I/O connectors with only filtered signals passing through.

## 6. Power Distribution Network (PDN) Rules

### 6.1 PDN Impedance

**Rule:** PDN impedance must be below the target impedance from DC to the highest frequency of concern. Target impedance = Vripple_allowed / Imax_transient.

**Severity if violated:** Major

**Remediation:**
- Add decoupling capacitors to address high-impedance frequency bands
- Increase power/ground plane area
- Reduce via inductance in power delivery path

### 6.2 Switching Regulator Isolation

**Rule:** Switching regulator input/output loops must be minimized. Keep the hot loop (input cap -> high-side switch -> inductor -> output cap -> ground return) as small as possible.

**Severity if violated:** Critical (for switching frequencies >500 kHz)

**Remediation:**
- Tighten component placement to minimize loop area
- Place input capacitor directly at the regulator input pins
- Use a ground plane pour under the regulator, stitched to the main ground

## 7. Return Path Rules

### 7.1 Return Path Continuity

**Rule:** Every signal must have a continuous, low-impedance return path on the adjacent reference plane. Signals crossing plane boundaries must have return path stitching vias at the crossing point.

**Severity if violated:** Critical

**Remediation:**
- Add ground stitching vias at every layer transition
- Do not route signals across plane splits
- When a signal changes reference planes, place a via connecting both reference planes within 50 mil of the signal via

## 8. Remediation Priority Matrix

When kicad-happy:emc reports multiple findings, prioritize remediation using this matrix:

| Priority | Category | Rationale |
|----------|----------|-----------|
| 1 | Return path discontinuities | Root cause of most emission issues |
| 2 | Clock/high-speed routing on outer layers | Highest radiation risk |
| 3 | Missing I/O filtering | Primary conducted emission path |
| 4 | Ground plane splits under signals | Slot antenna radiation |
| 5 | Decoupling deficiencies | PDN noise couples to everything |
| 6 | Board edge violations | Secondary radiation mechanism |
| 7 | Component placement optimization | Lowest priority, incremental improvement |

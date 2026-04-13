# Test Fixture Design Patterns Reference

This reference provides test fixture design patterns, probe types, accessibility rules, and mechanical considerations for the Test Engineer. Use this when specifying test fixtures for prototype validation or production testing.

## 1. Fixture Types

### 1.1 Bed-of-Nails (ICT) Fixture

**Purpose:** Contact multiple test points simultaneously for in-circuit testing (component value verification, shorts/opens detection).

**Key design considerations:**
- Probe density: typical maximum 100 probes per square inch (15.5 probes/cm2) on a standard fixture
- Probe pitch: minimum 50 mil (1.27 mm) center-to-center for standard spring probes; 39 mil (1.0 mm) for fine-pitch probes
- Board support: vacuum hold-down or mechanical clamp to ensure consistent probe contact
- Probe force: typical 4-8 oz (110-230 g) per probe; total force = probe count x force per probe
- Alignment: guide pins (tooling holes on PCB) with +/- 5 mil (0.127 mm) alignment accuracy

**Probe types:**
| Type | Tip Style | Best For | Min Pad Size |
|------|-----------|----------|-------------|
| Spring-loaded (standard) | Crown, serrated | Bare pads, test points | 35 mil (0.9 mm) |
| Spring-loaded (fine pitch) | Pointed, chisel | Small pads, fine-pitch | 20 mil (0.5 mm) |
| Pogo pin | Flat, concave | Power connections, high current | 40 mil (1.0 mm) |
| Kelvin probe (4-wire) | Dual contact | Precision resistance measurement | 50 mil (1.27 mm) |

**Cost factors:**
- Fixture plate: $500-$2000 (acrylic/Delrin for prototype, aluminum for production)
- Probes: $5-$20 each (standard), $20-$50 each (fine-pitch/specialty)
- Wiring: $500-$2000 for hand-wired, $2000-$5000 for PCB-based interface
- Total typical cost: $3000-$15000 for a production ICT fixture

### 1.2 Functional Test Fixture

**Purpose:** Provide power, stimulus, and measurement connections for powered functional verification of the DUT (Device Under Test).

**Key design considerations:**
- Power delivery: low-impedance connections to DUT power input; current capacity for worst-case load
- Signal routing: controlled impedance if high-speed signals are routed through the fixture
- Shielding: consider EMI shielding if fixture introduces noise into sensitive measurements
- Thermal management: ventilation or active cooling if DUT dissipates significant power during test
- Safety: current limiting, reverse polarity protection, emergency stop for powered fixtures

**Interface options:**
| Method | Speed | Reliability | Cost | Best For |
|--------|-------|------------|------|----------|
| Edge connector | Fast insert/remove | Good (connector rated for cycles) | Low | Boards with edge connector |
| Pogo pin array | Fast (drop-in) | Good (spring probes rated for 1M+ cycles) | Medium | Production volumes |
| Cable harness | Slow (manual connect) | Variable | Low | Prototype (< 10 units) |
| Zero-insertion-force (ZIF) socket | Fast | Excellent | High | Module-level test |

### 1.3 Programming Fixture

**Purpose:** Provide debug interface access for firmware loading, calibration, and serialization.

**Key design considerations:**
- Debug interface: match DUT debug connector (Tag-Connect, ARM SWD, JTAG header, UART)
- Tag-Connect: preferred for production -- no connector on DUT (pads only), reduces BOM cost
- Programming time: ensure interface speed supports acceptable cycle time
- Calibration: if DUT requires calibration (ADC trim, sensor offset), fixture must provide known reference stimulus

**Common debug interfaces:**
| Interface | Pins | Speed | Fixture Connector |
|-----------|------|-------|-------------------|
| ARM SWD | 2 data + power/ground | Fast | Tag-Connect TC2030 or pin header |
| JTAG | 4 data + power/ground | Fast | Tag-Connect TC2050 or pin header |
| UART bootloader | 2 data + power/ground | Moderate | Pogo pins to test pads |
| USB DFU | USB D+/D- + power/ground | Fast | USB connector on DUT |

### 1.4 Environmental Test Fixture

**Purpose:** Mount the DUT in an environmental chamber (thermal, humidity, vibration) while maintaining electrical monitoring connections.

**Key design considerations:**
- Temperature range: fixture materials must withstand chamber temperature extremes (-40C to +85C typical)
- Material selection: avoid plastics that outgas at temperature; use aluminum, stainless steel, or high-temp plastics (PEEK, Ultem)
- Cable routing: route cables through chamber port; use temperature-rated cables
- Vibration mounting: rigid attachment to shaker table; fixture resonance must be above test frequency range (rule of thumb: fixture first resonance > 2x max test frequency)

## 2. Test Point Design Rules

### 2.1 Test Point Placement Guidelines

| Rule | Requirement | Rationale |
|------|------------|-----------|
| Minimum pad size | 35 mil (0.9 mm) diameter for standard probes; 50 mil (1.27 mm) preferred | Reliable probe contact with alignment tolerance |
| Minimum pitch | 50 mil (1.27 mm) center-to-center between adjacent test points | Prevent probe-to-probe shorts; allow standard probe housing |
| Preferred side | Bottom (solder side) for bed-of-nails; top for manual probing | Bed-of-nails fixtures contact from below; top access for debug |
| Keep-out from components | 50 mil (1.27 mm) minimum clearance from component bodies | Probe access; prevent fixture interference with components |
| Keep-out from board edge | 100 mil (2.54 mm) minimum from board edge | Fixture clamping/vacuum seal zone |
| Power/ground test points | At least one power and one ground test point per power domain | Verify each supply independently |
| Net coverage target | 100% of nets for ICT; minimum 80% for functional test | Maximize defect detection |

### 2.2 Test Point Accessibility Assessment

When evaluating a PCB layout for test accessibility, check each test point against:

1. **Probe access** -- is there a clear path for a probe to reach the pad? Check for tall components blocking access from above/below
2. **Pad size** -- does the pad meet minimum size requirements for the selected probe type?
3. **Pitch** -- is the spacing between adjacent test points sufficient for the probe housing?
4. **Fiducials** -- are there at least two (preferably three) fiducial marks for fixture alignment?
5. **Tooling holes** -- are there tooling holes for mechanical registration? (2 minimum, 3 preferred, non-collinear)

**Accessibility categories:**
| Category | Definition | Action |
|----------|-----------|--------|
| Accessible | Pad meets all size/pitch/clearance rules | Include in fixture probe map |
| Marginal | Pad meets minimum but not preferred rules | Include with note; consider fine-pitch probe |
| Blocked | Component or keep-out prevents probe access | Request layout change or accept coverage gap |
| Missing | Net has no dedicated test point | Request test point addition or accept coverage gap |

### 2.3 Cross-Reference with PCB Layout

The TestE must cross-reference the test point plan with the PCB layout to verify:

1. All planned test points exist in the layout
2. Test points are on the correct layer (top/bottom per fixture type)
3. No test points have been moved into inaccessible locations during layout iterations
4. Fiducials and tooling holes are present and correctly positioned
5. Board outline matches fixture mechanical design assumptions

This cross-reference can use `kicad-happy:kicad` if available, or be performed manually against the layout artifacts from the PCB Layout Engineer.

## 3. Fixture Design Workflow

1. **Input gathering:** Collect board dimensions, test point list, component heights, connector locations
2. **Fixture type selection:** Determine which fixture types are needed based on test strategy
3. **Probe map creation:** Map each test point to a probe location; select probe types
4. **Mechanical design:** Define plate dimensions, guide pin locations, hold-down method
5. **Interface design:** Define electrical connections between probes and test equipment
6. **Review:** Cross-reference probe map against PCB layout; verify no conflicts
7. **Documentation:** Produce fixture specification with probe map, mechanical drawings, and interface list

## 4. Fixture Cost Estimation

| Volume Tier | Recommended Approach | Estimated Fixture Cost |
|-------------|---------------------|----------------------|
| Prototype (< 10) | Manual probing + cable harness | $100-$500 |
| Small-batch (10-100) | 3D-printed fixture + pogo pins | $500-$2000 |
| Small-batch (100-1000) | Machined fixture + spring probes | $2000-$8000 |
| Production (1000+) | Professional ICT fixture + functional test station | $5000-$20000+ |

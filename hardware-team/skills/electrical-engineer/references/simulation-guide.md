# SPICE Simulation Methodology

This reference defines the simulation methodology, convergence settings, and subcircuit validation patterns used by the Electrical Engineer during simulation-setup tasks.

## Simulation Strategy

Not every circuit requires simulation. Prioritize simulation for:

1. **Analog filters** -- Verify cutoff frequency, rolloff, passband ripple
2. **Voltage regulators / DC-DC converters** -- Verify stability, transient response, ripple
3. **Voltage dividers** -- Verify ratio accuracy with load effects (often trivial but validates assumptions)
4. **Opamp circuits** -- Verify gain, bandwidth, phase margin, stability
5. **Oscillator / crystal circuits** -- Verify load capacitance, startup margin
6. **Power supply transients** -- Verify inrush current, soft-start behavior, load step response
7. **Current sense circuits** -- Verify accuracy across operating range

Skip simulation for:
- Simple digital interconnects (review by inspection)
- Standard application circuits matching datasheet exactly (trust the datasheet)
- Passive pullup/pulldown networks (calculate by hand)

## kicad-happy:spice Integration

This role invokes `kicad-happy:spice` for all simulation tasks. The spice skill auto-detects subcircuits from KiCad schematic analysis and supports ngspice, LTspice, and Xyce (auto-detected based on installation).

**Invocation pattern:**
1. Invoke `kicad-happy:kicad` first to parse the schematic and identify subcircuits
2. Invoke `kicad-happy:spice` to run simulations on identified subcircuits
3. The spice skill handles netlist generation, simulation execution, and result parsing

**DO NOT** write SPICE netlists manually or invoke simulation tools directly. The kicad-happy:spice skill IS the simulation capability.

## Simulation Types

### AC Analysis
**Purpose:** Frequency response characterization (filters, amplifiers)
**What to verify:**
- -3dB frequency matches design target (within 10%)
- Rolloff slope matches filter order
- Passband gain matches design target
- Phase margin > 45 degrees (for feedback circuits)
- Gain margin > 6 dB (for feedback circuits)

### DC Analysis
**Purpose:** Operating point verification, voltage divider ratios, bias point analysis
**What to verify:**
- Node voltages match expected values
- Quiescent current within budget
- Component operating points within safe area

### Transient Analysis
**Purpose:** Time-domain behavior (power supply startup, load transients, pulse response)
**What to verify:**
- Startup time meets requirements
- Overshoot/undershoot within acceptable limits
- Settling time meets requirements
- Ripple amplitude within spec

### Parameter Sweep
**Purpose:** Sensitivity analysis (component tolerance effects)
**What to verify:**
- Circuit meets requirements across component tolerance range (typically +/-5% for resistors, +/-20% for ceramics)
- No instability at tolerance corners

## Convergence Settings

If simulation fails to converge, try these adjustments (in order):

1. **Increase RELTOL** -- from 0.001 (default) to 0.01
2. **Reduce TRTOL** -- from 7 (default) to 1
3. **Increase ITL1** (DC iteration limit) -- from 100 to 500
4. **Increase ITL4** (transient iteration limit) -- from 10 to 50
5. **Add GMIN stepping** -- `.options gmin=1e-12`
6. **Simplify the subcircuit** -- replace complex models with ideal versions to isolate convergence issue

## Validation Criteria

Each simulated subcircuit must have explicit pass/fail criteria defined before simulation:

```markdown
## Subcircuit: <name>

**Simulation type:** AC / DC / Transient / Sweep
**Pass criteria:**
- <parameter 1>: <target> +/- <tolerance>
- <parameter 2>: <min> to <max>

**Result:**
- <parameter 1>: <measured value> -- PASS / FAIL
- <parameter 2>: <measured value> -- PASS / FAIL

**Assessment:** PASS / FAIL
**Notes:** <any observations, warnings, or recommendations>
```

## Simulation Results Documentation

The simulation-results.md artifact must include for each subcircuit:

1. **Subcircuit identification** -- what circuit, reference designators involved
2. **Simulation type** -- AC, DC, transient, sweep
3. **Setup** -- stimulus conditions, simulation parameters
4. **Pass criteria** -- defined before reviewing results
5. **Results** -- measured values for each criterion
6. **Pass/fail assessment** -- binary per criterion and overall
7. **Recommendations** -- any design changes needed for failing subcircuits

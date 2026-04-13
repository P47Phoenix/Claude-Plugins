# Schematic Review Checklist

This reference defines the 7-category schematic review checklist used by the Electrical Engineer role during schematic-review tasks and the Schematic Review Gate.

## Review Methodology

### Forced-Find Prompting

Each review pass MUST identify at least 2 potential issues across the 7 categories. This guards against false "all clear" reviews where the reviewer skims without deep analysis. If a candidate issue is ultimately not a real problem, the reviewer must explain why it was dismissed.

### Category Coverage Tracking

For each of the 7 categories below, the reviewer MUST explicitly report:
- `CATEGORY_EXAMINED: <name>` -- the category was reviewed and findings (or lack thereof) are documented
- `CATEGORY_NOT_EXAMINED: <name>` -- the category was skipped (must include justification)

### Severity Definitions

| Severity | Definition | Gate Impact |
|----------|-----------|-------------|
| **Critical** | Safety risk, functional failure, or regulatory non-compliance. The design will not work or is unsafe. | Blocks gate in ALL strictness modes |
| **Major** | Performance degradation, reliability risk, or significant deviation from best practice. The design will work but may have problems in production or edge cases. | Blocks gate in `strict` and `standard` modes |
| **Minor** | Best practice deviation with minimal impact. The design will work but could be improved. | Blocks gate only in `strict` mode |

---

## Category 1: Power Integrity

**What to check:**
- Bulk capacitors on power input (adequate capacitance for inrush and transient demands)
- Voltage regulator input/output capacitor values match datasheet recommendations
- Power sequencing requirements met (core before I/O for FPGAs, AVCC before DVCC)
- Voltage regulator stability: output capacitor ESR within stability range
- Power rail voltage accuracy under load (dropout margin for LDOs)
- Reverse polarity protection (where applicable)
- Fuse or current limiting on power input

**Common findings:**
- Missing bulk capacitor on power input rail
- LDO output capacitor ESR outside stable range (ceramic too low, electrolytic too high)
- Incorrect power sequencing for multi-rail ICs
- Insufficient dropout margin (input voltage too close to output under load)

---

## Category 2: Signal Integrity

**What to check:**
- Series termination resistors on high-speed clock outputs
- Parallel termination on long transmission lines
- Impedance matching for controlled-impedance traces (USB, Ethernet, HDMI, DDR)
- Source-terminated vs. end-terminated appropriateness
- Clock signal routing constraints documented
- Differential pair signals identified and impedance targets specified
- AC coupling capacitors on high-speed serial links (USB, HDMI) with correct values

**Common findings:**
- Missing series termination on clock output driving a long trace
- USB D+/D- impedance not specified for PCB layout
- Missing AC coupling capacitors on high-speed differential pairs
- No guard band specification for sensitive analog signals adjacent to digital

---

## Category 3: Component Derating

**What to check:**
- Capacitor voltage rating >= 2x max applied voltage (ceramic) or >= 1.5x (electrolytic)
- Resistor power rating >= 2x calculated dissipation
- MOSFET Vds rating >= 1.5x max drain-source voltage
- Diode reverse voltage rating >= 1.5x max reverse voltage
- IC absolute maximum ratings not exceeded under any operating condition
- Temperature derating applied (reduce ratings at elevated temperature per datasheet curves)
- Inrush current within component ratings

**Common findings:**
- Ceramic capacitor rated at operating voltage (no derating -- voltage-dependent capacitance loss)
- Resistor in voltage divider dissipating near rated power
- MOSFET Vgs driven beyond absolute maximum
- Electrolytic capacitor at rated temperature with no margin

---

## Category 4: Pull-ups / Pull-downs

**What to check:**
- I2C bus pull-up resistors present with correct values (typically 2.2k-10k depending on bus speed and capacitance)
- Reset pins have proper pull-up/pull-down with decoupling capacitor for noise immunity
- Enable/shutdown pins tied to defined state (not floating)
- Unused IC inputs tied to defined logic level
- Open-drain/open-collector outputs have pull-ups
- Chip select pins have default inactive state (pull-up for active-low CS)
- GPIO pins with external connections have defined default state

**Common findings:**
- I2C pull-ups missing or wrong value for bus speed (400kHz needs lower resistance than 100kHz)
- Reset pin with pull-up but no decoupling cap (susceptible to noise glitches)
- Unused op-amp inputs floating (should be tied to reference or mid-supply)
- SPI chip select floating during boot (slave device active during MCU initialization)

---

## Category 5: Decoupling Strategy

**What to check:**
- Every IC has a decoupling capacitor (100nF ceramic minimum, placed close to VCC pin)
- High-current digital ICs have additional bulk decoupling (10uF+)
- Multi-VCC ICs have decoupling on EACH VCC pin
- Analog ICs have separate analog decoupling (low-ESR ceramic, sometimes with series ferrite)
- Decoupling capacitor values match IC datasheet recommendations
- Mixed-signal ICs have separate AVCC and DVCC decoupling
- Power entry point has bulk capacitance appropriate for load transients

**Common findings:**
- IC with multiple VCC pins but only one decoupling cap
- Analog section sharing decoupling with noisy digital section
- Decoupling capacitor value/type doesn't match datasheet recommendation
- No bulk capacitance at board power entry for load transient handling

---

## Category 6: Voltage Level Compatibility

**What to check:**
- Logic level compatibility between ICs on shared buses (3.3V device connected to 5V bus)
- Level translator present where voltage domains differ
- Input voltage thresholds (VIH/VIL) compatible with driving output levels (VOH/VOL)
- Bidirectional level translation for I2C and other bidirectional buses
- ADC input voltage range matches signal source range (no over-voltage risk)
- Mixed 3.3V/5V/1.8V designs have clear voltage domain boundaries
- Tolerance band analysis: worst-case VOL vs. VIL, worst-case VOH vs. VIH

**Common findings:**
- 3.3V GPIO driving 5V-only input without level shifter
- 5V-tolerant pin assumed but not verified in datasheet
- ADC reference voltage mismatch with input signal range
- I2C bus with mixed-voltage devices but no bidirectional level translator

---

## Category 7: Thermal Considerations

**What to check:**
- Power dissipation calculated for all significant heat sources (regulators, MOSFETs, ICs)
- Junction temperature within safe operating area under worst-case ambient temperature
- Thermal relief pads connected to ground/power planes for heat dissipation
- Heat sink requirements identified (if needed) with thermal resistance budget
- High-power components spaced for adequate airflow
- Thermal shutdown thresholds documented for ICs with thermal protection
- Copper pour area adequate for components relying on PCB copper for heat spreading

**Common findings:**
- Linear regulator dissipating significant power with no thermal pad or heat sink analysis
- High-current MOSFET with no thermal resistance calculation
- Component placed in thermally isolated area (no copper pour connection to planes)
- Worst-case ambient temperature not considered in thermal analysis

---

## Finding Report Format

Each finding MUST include all of the following fields:

```
{
  "id": "F-<sequential number>",
  "severity": "critical | major | minor",
  "category": "<exact category name from the 7 above>",
  "component": "<reference designator, e.g., C7, U3, R12>",
  "net": "<net name if applicable, e.g., VCC_3V3>",
  "location": "<schematic sheet and location>",
  "description": "<what the issue is>",
  "fix": "<specific recommended remediation>"
}
```

For net-level findings (no specific component), set `component` to null and specify `net`.
For board-level findings (no specific component or net), set both to null and include a `board_issue_id` from the defined enum (see gate-framework.md).

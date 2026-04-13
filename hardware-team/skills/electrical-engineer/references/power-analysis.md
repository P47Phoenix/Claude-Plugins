# Power Tree Analysis Patterns

This reference defines the power architecture analysis methodology, derating guidelines, power budget templates, and sequencing rules used by the Electrical Engineer during power-analysis tasks.

## Power Tree Analysis Process

### Step 1: Map the Power Tree

Document the complete power distribution network from input to load:

```
Input Source (e.g., USB 5V, Battery 3.7-4.2V, 12V barrel jack)
  |
  +-- Protection (fuse, TVS, reverse polarity)
  |
  +-- Regulator/Converter 1 --> Rail 1 (e.g., 3.3V)
  |     |
  |     +-- Load group A (MCU core, SRAM)
  |     +-- Load group B (sensors, peripherals)
  |
  +-- Regulator/Converter 2 --> Rail 2 (e.g., 1.8V)
  |     |
  |     +-- Load group C (MCU I/O, level translators)
  |
  +-- Direct pass-through --> Rail 3 (e.g., VBUS for USB downstream)
```

### Step 2: Power Budget

For each rail, calculate:

| Rail | Voltage | Load (Typ) | Load (Max) | Source Rating | Margin | Status |
|------|---------|-----------|-----------|-------------|--------|--------|
| <net> | <V> | <mA> | <mA> | <mA> | <margin %> | OK / WARNING / FAIL |

**Margin calculation:** `margin = (source_rating - load_max) / source_rating * 100`

**Margin thresholds:**
- **>30%**: OK -- comfortable margin for design changes and measurement uncertainty
- **10-30%**: WARNING -- tight; verify with worst-case analysis
- **<10%**: FAIL -- redesign required; regulator undersized or loads must be reduced

### Step 3: Efficiency Chain

For switched-mode converters, calculate the efficiency chain from input to load:

```
Input power = V_in * I_in
Converter efficiency = P_out / P_in (from datasheet at operating point)
Total system efficiency = product of all converter efficiencies in the chain
Total input current = total_load_power / (V_in * system_efficiency)
```

For battery-powered designs, this directly determines battery life.

## Derating Guidelines

### Capacitors

| Type | Voltage Derating | Notes |
|------|-----------------|-------|
| Ceramic (MLCC) | Max applied voltage <= 50% of rated voltage | Ceramic capacitors lose capacitance with applied voltage (DC bias effect). A 10uF/10V X5R cap may have only 3uF at 8V applied. |
| Electrolytic (aluminum) | Max applied voltage <= 67% of rated voltage | Higher derating at elevated temperature; check lifetime vs. ripple current |
| Tantalum | Max applied voltage <= 50% of rated voltage | Tantalum capacitors are prone to failure if voltage is not derated aggressively |
| Film | Max applied voltage <= 80% of rated voltage | More tolerant of voltage stress than ceramics |

### Resistors

| Condition | Derating |
|-----------|---------|
| Power dissipation | Max dissipation <= 50% of rated power at 25C |
| Temperature | Derate linearly above 70C per datasheet derating curve |
| Pulse handling | Check pulse power rating for inrush/transient applications |

### Semiconductors

| Component | Derating |
|-----------|---------|
| MOSFET Vds | Max Vds <= 80% of rated Vds |
| MOSFET Vgs | Max Vgs <= 70% of absolute maximum Vgs |
| Diode reverse voltage | Max Vr <= 80% of rated Vr |
| IC supply voltage | Must operate within recommended operating conditions (not absolute max) |
| Junction temperature | Tj_max <= 85% of absolute maximum Tj |

## Power Sequencing

### Common Sequencing Requirements

| Scenario | Rule |
|----------|------|
| FPGA / SoC | Core voltage BEFORE I/O voltage; check specific device datasheet |
| DDR Memory | VDD and VDDQ must rise monotonically; VTT derived from VDDQ |
| Mixed-signal IC | AVCC and DVCC often require simultaneous rise or specific order |
| USB hub / controller | VBUS sensing before port power enable |
| Level translators | Both VCC rails must be present before enabling outputs |

### Sequencing Implementation Options

| Method | Complexity | Cost | Precision |
|--------|-----------|------|-----------|
| RC delay on enable pin | Low | Low | Low (component-dependent) |
| Voltage supervisor with enable | Medium | Medium | High |
| Dedicated sequencer IC | High | High | Very high (programmable delays) |
| Software-controlled (GPIO enable) | Medium | None (uses MCU) | High (firmware-dependent) |

## Power Analysis Report Template

```markdown
# Power Analysis Report

**Project:** <project name>
**Date:** <ISO 8601>

## 1. Power Tree

<ASCII or Mermaid diagram of power distribution>

## 2. Power Budget

| Rail | Net Name | Voltage | Regulator | Efficiency | Load (Typ) | Load (Max) | Source Rating | Margin | Status |
|------|----------|---------|-----------|-----------|-----------|-----------|-------------|--------|--------|
| <rail> | <net> | <V> | <part> | <eff%> | <mA> | <mA> | <mA> | <margin%> | OK/WARN/FAIL |

**Total input power (typical):** <W>
**Total input power (maximum):** <W>
**Estimated battery life:** <hours at typical> (if applicable)

## 3. Derating Summary

| Component | Parameter | Rating | Operating Value | Derating % | Status |
|-----------|-----------|--------|----------------|-----------|--------|
| <ref des> | <parameter> | <rated> | <actual> | <derating%> | OK/WARN/FAIL |

## 4. Sequencing Requirements

| Sequence Step | Rail | Method | Enable Signal | Delay After Previous |
|--------------|------|--------|--------------|---------------------|
| 1 | <rail> | <method> | <signal> | <ms> |
| 2 | <rail> | <method> | <signal> | <ms> |

## 5. Simulation Results

<Reference to simulation-results.md for power supply transient simulations>

## 6. Findings and Recommendations

| ID | Severity | Description | Recommendation |
|----|----------|-------------|----------------|
| <id> | <severity> | <description> | <fix> |
```

## Common Power Architecture Pitfalls

1. **LDO thermal dissipation** -- Large input-output voltage differential at high current generates significant heat: P = (Vin - Vout) * Iload. Consider switching regulator if Pdiss > 500mW.
2. **Missing bulk capacitance** -- Switching converters need bulk capacitance at input for current pulses; LDOs need stable input for PSRR.
3. **Ground plane splits** -- Avoid routing high-current return paths across split ground planes; ensure star-point or continuous ground for analog/digital separation.
4. **Inrush current** -- Large input capacitance causes inrush current spikes that can trip upstream protection or cause voltage sag. Consider soft-start or inrush limiting.
5. **Reverse current on power-down** -- When Vout > Vin during power-down, current can flow backward through LDOs. Some LDOs have reverse current protection; verify in datasheet.

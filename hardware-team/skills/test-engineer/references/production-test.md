# Production Test Methodology Reference

This reference provides production test methodology, ICT/functional test flow design, failure binning, cycle time optimization, and test data management for the Test Engineer. Use this when developing production test procedures.

## 1. Production Test Flow Architecture

A production test flow is an ordered sequence of test stages. Each unit progresses through the stages; a failure at any stage routes the unit to failure analysis or scrap.

### 1.1 Standard Production Test Flow

```
Incoming Inspection
        |
        v
  Visual / AOI
        |
        v
    ICT / Flying Probe
        |
        v
    Programming
        |
        v
  Functional Test
        |
        v
  Final Inspection
        |
        v
    Pack & Ship
```

**Stage ordering rationale:**
- Visual/AOI first: catch obvious assembly defects before powering the board (solder bridges, missing components, wrong polarity)
- ICT second: verify component values and connections before applying power (catch shorts before they cause damage)
- Programming third: firmware must be loaded before functional test can run
- Functional test fourth: verify powered operation after all prerequisites pass

### 1.2 Alternative Flows

**No-ICT flow (small batch):**
```
Visual Inspection --> Programming --> Functional Test --> Final Inspection
```
Used when ICT fixture cost is not justified. Functional test must compensate with broader coverage.

**Boundary scan flow (BGA-heavy designs):**
```
AOI --> Boundary Scan (JTAG) --> Programming --> Functional Test --> Final Inspection
```
Used when BGA packages prevent physical probe access to most nets. Boundary scan tests digital connectivity through the IC's JTAG chain.

## 2. Test Stage Design

### 2.1 In-Circuit Test (ICT) / Flying Probe

**What ICT tests:**
| Test Type | Method | Detection |
|-----------|--------|-----------|
| Component presence | Capacitance measurement (unpowered) | Missing component, wrong component |
| Resistance | 4-wire (Kelvin) measurement | Wrong value, open, high-resistance joint |
| Capacitance | AC impedance measurement | Wrong value, wrong type |
| Inductance | AC impedance measurement | Wrong value, shorted turns |
| Diode/transistor | Forward voltage, gain measurement | Wrong component, reversed polarity |
| Shorts | Resistance between adjacent nets | Solder bridges, copper defects |
| Opens | Continuity between connected pads | Missing solder, cracked joint, trace break |

**ICT limits setting:**
- Resistors: nominal +/- component tolerance + 5% measurement uncertainty (e.g., 1k 1% resistor: limits = 940 to 1060 ohms)
- Capacitors: nominal +/- component tolerance + 10% measurement uncertainty (wider due to frequency-dependent behavior)
- Diodes: forward voltage Vf nominal +/- 100 mV typical
- Shorts threshold: typically < 50 ohms between adjacent nets indicates a short
- Opens threshold: typically > 10k ohms for an expected connection indicates an open

### 2.2 Functional Test

**Functional test design principles:**
1. **Power up safely** -- ramp supply voltage, monitor current; abort if current exceeds limit (protects fixture and DUT)
2. **Test in isolation** -- verify each subsystem independently before testing integrated function
3. **Measurable criteria** -- every test step must have a numeric pass/fail limit, not a subjective assessment
4. **Deterministic order** -- test order must be fixed and repeatable; do not randomize production tests
5. **Fast fail** -- arrange tests so the most common failure modes are detected earliest (reduces average test time for failing units)

**Functional test sequence template:**
| Step | Test | Stimulus | Measurement | Min | Max | Unit |
|------|------|----------|-------------|-----|-----|------|
| 1 | Supply current (idle) | Apply Vcc | Measure Icc | 0 | <max_idle_mA> | mA |
| 2 | Voltage rail 1 | Power on | Measure rail voltage | <Vnom - tol> | <Vnom + tol> | V |
| 3 | Clock frequency | Power on | Measure clock output | <Fnom - tol> | <Fnom + tol> | MHz |
| 4 | I2C device ACK | Send I2C address | Check ACK | 1 | 1 | ACK |
| 5 | ADC reading | Apply reference voltage | Read ADC value | <min_code> | <max_code> | counts |
| ... | ... | ... | ... | ... | ... | ... |

### 2.3 Programming Stage

**Programming flow:**
1. **Connect** -- establish debug interface connection (SWD/JTAG/UART/USB)
2. **Erase** -- erase target flash memory (full chip erase or sector erase)
3. **Program** -- write firmware image to flash; verify with read-back or CRC
4. **Calibration** -- if applicable, run calibration routine and store calibration data in non-volatile memory
5. **Serialization** -- assign unique serial number; store in designated memory location
6. **Lock** -- if applicable, set read protection to prevent firmware extraction
7. **Verify** -- final read-back verification of firmware CRC and serial number

**Programming time budget:**
| Flash Size | Interface | Approximate Time |
|-----------|-----------|-----------------|
| 64 KB | SWD (4 MHz) | < 2 sec |
| 256 KB | SWD (4 MHz) | 3-5 sec |
| 1 MB | SWD (4 MHz) | 10-15 sec |
| 1 MB | USB DFU (12 Mbps) | 2-3 sec |
| 16 MB (external SPI flash) | SPI (40 MHz) | 5-10 sec |

## 3. Failure Binning

### 3.1 Bin Code System

Assign a numeric bin code to every failure mode. Bin codes enable Pareto analysis and process feedback.

| Bin Range | Category | Examples |
|-----------|----------|----------|
| 0 | PASS | Unit passed all tests |
| 1-9 | Power failure | No power, over-current, wrong voltage |
| 10-19 | ICT component failure | Wrong value, missing, reversed |
| 20-29 | ICT connectivity failure | Short, open, high resistance |
| 30-39 | Programming failure | Cannot connect, verify fail, lock fail |
| 40-49 | Communication failure | I2C NACK, SPI timeout, UART error |
| 50-59 | Analog failure | ADC out of range, DAC error, sensor failure |
| 60-69 | Digital I/O failure | GPIO stuck, wrong level |
| 70-79 | Timing failure | Clock out of spec, bus timing violation |
| 80-89 | Environmental/thermal | Over-temperature, thermal shutdown |
| 90-99 | Other/undefined | Catch-all for unexpected failures |

### 3.2 Failure Disposition

| Disposition | Action | Tracking |
|-------------|--------|----------|
| Rework | Repair defect and retest | Track rework count per unit (max 2 rework cycles typical) |
| Scrap | Unit cannot be repaired economically | Record bin code for yield analysis |
| Engineering hold | Failure requires engineering investigation | Quarantine unit; create failure analysis ticket |
| Retest | Test result suspect (fixture issue, intermittent) | Retest once; if fails again, treat as real failure |

## 4. Cycle Time Optimization

### 4.1 Total Test Cycle Time Calculation

```
Total cycle time per unit = Load time
                          + Visual/AOI time
                          + ICT time
                          + Programming time
                          + Functional test time
                          + Unload time
                          + Data logging overhead
```

### 4.2 Optimization Techniques

| Technique | Savings | Trade-off |
|-----------|---------|-----------|
| Parallel programming + test | 20-40% | Requires dual-port fixture or separate stations |
| Reduce ICT to critical nets only | 10-30% | Lower coverage (compensate with functional test) |
| Fast-fail ordering | 10-20% average | Only helps when units fail (no benefit for passing units) |
| Batch programming before fixture | Variable | Adds handling step but removes programming from fixture cycle |
| Combine ICT and functional in one fixture | 30-50% | Higher fixture complexity and cost |

### 4.3 Throughput Calculation

```
Units per hour = 3600 / (total cycle time in seconds)
Units per shift (8 hr) = units per hour * 8 * utilization factor (typically 0.85)
```

## 5. Test Data Management

### 5.1 Minimum Data Per Unit

| Data Field | Purpose | Retention |
|-----------|---------|-----------|
| Serial number | Unit identification | Permanent |
| Date/time stamp | Production traceability | Permanent |
| Firmware version | Software traceability | Permanent |
| Test station ID | Equipment traceability | Permanent |
| Overall result (PASS/FAIL) | Quality metric | Permanent |
| Bin code (if FAIL) | Failure classification | Permanent |
| Test measurements (all) | Process monitoring, SPC | Minimum 2 years |
| Rework history | Quality tracking | Permanent |

### 5.2 Data Format

For small-batch production, CSV files with one row per unit are sufficient:
```
serial,datetime,firmware_version,station_id,result,bin_code,rail_3v3,rail_1v8,icc_idle,...
SN00001,2026-04-12T10:30:00Z,v1.2.3,STATION-A,PASS,0,3.301,1.802,45.2,...
SN00002,2026-04-12T10:31:15Z,v1.2.3,STATION-A,FAIL,42,3.298,1.799,45.8,...
```

For production volumes, use a database with structured schema and query capability.

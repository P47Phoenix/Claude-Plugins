# Test Strategy Frameworks Reference

This reference provides test strategy frameworks, testing type definitions, and coverage analysis methods for the Test Engineer. Use this when defining the overall test approach for a hardware product.

## 1. Test Strategy Hierarchy

A hardware test strategy is organized in layers, from broadest scope to narrowest:

| Layer | Scope | Question Answered | Owner |
|-------|-------|-------------------|-------|
| Test Philosophy | Product lifetime | What level of quality assurance does this product class require? | TestE + HW PO |
| Test Plan | Per-project | What specific tests are needed for this design? | TestE |
| Test Procedure | Per-test | How is each test executed, step by step? | TestE |
| Test Case | Per-requirement | What stimulus is applied and what response is expected? | TestE |

## 2. Testing Type Definitions

### 2.1 Functional Testing

**Purpose:** Verify that each circuit function operates within specification under nominal conditions.

**Subtypes:**
- **Power-on verification** -- rails come up in sequence, voltages within tolerance, current draw within budget
- **Communication bus verification** -- I2C devices ACK at expected addresses, SPI responds correctly, UART loopback passes
- **Analog I/O verification** -- ADC reads calibration voltage within tolerance, DAC output matches commanded value
- **Digital I/O verification** -- GPIO drive/sense matches expected logic levels
- **Timing verification** -- clock frequencies within specification, communication bus timing within protocol limits
- **End-to-end functional** -- product-level function operates as specified in the hardware PRD

**Equipment:**
- Bench power supply (programmable preferred for sequencing tests)
- Digital multimeter (DMM) -- 6.5-digit for precision measurements
- Oscilloscope -- bandwidth >= 5x highest frequency of interest
- Logic analyzer -- for bus protocol verification (optional if oscilloscope has decode)
- Signal generator -- for stimulus injection (if analog inputs present)

### 2.2 Environmental Testing

**Purpose:** Verify the product operates correctly across its specified environmental range.

**Applicable standards:**
| Test | Standard | Description |
|------|----------|-------------|
| Temperature cycling | IEC 60068-2-14 (Test N) | Thermal shock or gradual cycling between temperature extremes |
| Dry heat | IEC 60068-2-2 (Test B) | Sustained operation at maximum rated temperature |
| Cold | IEC 60068-2-1 (Test A) | Sustained operation at minimum rated temperature |
| Damp heat (steady) | IEC 60068-2-78 (Test Cab) | Sustained operation at elevated temperature and humidity |
| Vibration (sinusoidal) | IEC 60068-2-6 (Test Fc) | Sine sweep or fixed-frequency vibration |
| Shock | IEC 60068-2-27 (Test Ea) | Mechanical shock pulses |
| ESD | IEC 61000-4-2 | Electrostatic discharge immunity (contact/air discharge) |

**Applicability guidance:**
- **Consumer products:** Temperature cycling + damp heat + ESD at minimum
- **Industrial products:** Full environmental suite (thermal, humidity, vibration, shock, ESD)
- **Hobby/Maker:** ESD only (if user-facing), otherwise optional
- **Automotive/Aerospace:** Extended profiles per AEC-Q or DO standards (out of scope for Phase 1)

### 2.3 Reliability Testing

**Purpose:** Assess product lifetime and identify latent failure modes through accelerated stress testing.

**Methods:**
| Method | Description | When Used |
|--------|-------------|-----------|
| HALT (Highly Accelerated Life Testing) | Apply progressively increasing stress (temperature, vibration) until failure to find design margins | DVT phase -- find design limits |
| HASS (Highly Accelerated Stress Screening) | Apply known stress profile to production units to screen out latent defects | Production -- optional for high-reliability |
| Burn-in | Operate units at elevated temperature under power for extended duration | Production -- screen infant mortality failures |
| MTBF estimation | Statistical calculation from accelerated test data (Arrhenius model for thermal acceleration) | DVT/PVT -- estimate field reliability |

**Applicability by volume:**
- **Hobby/Maker:** Not applicable
- **Small-batch (10-1000):** HALT recommended for DVT; burn-in optional
- **Production (1000+):** HALT for DVT, optional HASS/burn-in for production screening, MTBF targets required

### 2.4 Production Screening

**Purpose:** Test every unit during manufacturing to catch assembly defects.

**Methods (in typical production flow order):**
| Method | Coverage | Cycle Time | Equipment Cost |
|--------|----------|-----------|---------------|
| Automated Optical Inspection (AOI) | Solder joint quality, component presence/orientation | 5-30 sec | $$$ |
| In-Circuit Test (ICT) | Component values, shorts, opens | 10-60 sec | $$$$ (fixture cost) |
| Flying Probe | Component values, shorts, opens (no fixture needed) | 30-300 sec | $$$ (rental) |
| Boundary Scan (JTAG) | Digital IC connectivity, stuck-at faults | 5-30 sec | $$ |
| Functional Test | Power-up, communication, basic function | 30-300 sec | $$ |
| Programming | Firmware load, calibration, serialization | 10-60 sec | $ |

**Selection guidance:**
- **Prototype (< 10 units):** Manual visual inspection + functional test + programming
- **Small-batch (10-1000):** Flying probe (or ICT if fixture cost justified) + functional test + programming
- **Production (1000+):** AOI + ICT + functional test + programming (full production line)

## 3. Test Coverage Analysis

### 3.1 Requirements Traceability

Every testable requirement from the hardware PRD must map to at least one test procedure. The traceability matrix has these columns:

| Column | Description |
|--------|-------------|
| Req ID | Requirement identifier from the hardware PRD |
| Requirement | Testable requirement text |
| Test Category | Functional / Environmental / Reliability / Screening |
| Test Procedure | Reference to the specific test procedure |
| Test Phase | DVT / PVT / ORT / Production |
| Priority | Critical / High / Medium / Low |

### 3.2 Coverage Gap Analysis

After populating the traceability matrix, identify:

1. **Untestable requirements** -- requirements that cannot be verified through testing (rewrite as testable or accept as design review items)
2. **Test-only requirements** -- requirements with no design traceability (may indicate a test that adds no value)
3. **Single-method coverage** -- requirements covered by only one test method (consider adding redundancy for critical requirements)
4. **Phase gaps** -- requirements not tested until production (should critical requirements wait that long?)

### 3.3 Test Effectiveness Estimation

For production screening, estimate test escape rate:

```
Test Escape Rate = (1 - Product of all screening detection rates)

Example:
  AOI detects 95% of solder defects
  ICT detects 99% of component defects
  Functional test detects 90% of design-related defects
  
  Combined solder defect escape: 5% (AOI miss only -- ICT may catch some)
  Combined component defect escape: 1% * 10% = 0.1% (ICT miss AND functional miss)
```

This is an estimate -- actual escape rates depend on defect type distribution and test overlap. Refine after pilot run data collection.

## 4. Test Strategy Scaling by Production Tier

| Aspect | Hobby/Maker | Small-Batch (10-1000) | Production (1000+) |
|--------|------------|----------------------|-------------------|
| Functional test | Manual bench test | Semi-automated (scripted) | Fully automated fixture |
| Environmental test | Optional ESD only | Temperature + ESD | Full suite per product class |
| Reliability test | None | HALT in DVT | HALT + burn-in/HASS |
| Production screening | Visual inspection | Flying probe + functional | AOI + ICT + functional |
| Test data logging | Manual notes | Spreadsheet/CSV | Database with traceability |
| Quality metrics | Informal | FPY tracking | Full SPC + DPMO + MTBF |

# Test Point Coverage Requirements

This reference defines test point specifications, coverage targets, and fixture compatibility requirements used by the Manufacturing Engineer when evaluating test access in PCB designs.

## Test Point Purpose

Test points provide electrical access to circuit nodes for:
- **In-Circuit Test (ICT)** -- automated probing to verify component placement, value, and solder joint integrity
- **Functional Test** -- probing to measure circuit behavior under operating conditions
- **Boundary Scan (JTAG)** -- digital scan chain for IC interconnect verification
- **Debug** -- manual probing during bring-up and failure analysis

## Test Pad Specifications

### ICT Test Pads

| Parameter | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| Pad diameter | 0.035" (0.9mm) | 0.040" (1.0mm) | Larger pads improve probe contact reliability |
| Pad-to-pad center spacing | 0.050" (1.27mm) | 0.100" (2.54mm) | Tighter pitch requires more expensive fixtures |
| Pad-to-component clearance | 0.050" (1.27mm) | 0.100" (2.54mm) | Probe access clearance |
| Pad shape | Circular or square | Circular | Circular provides better probe centering |
| Pad surface finish | HASL, ENIG, or OSP | ENIG | Consistent contact resistance across test cycles |
| Solder mask | No solder mask over test pad | -- | Exposed copper/finish required for probe contact |

### Functional Test Points

| Parameter | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| Pad diameter | 0.040" (1.0mm) | 0.050" (1.27mm) | Manual probes need larger targets |
| Via-as-test-point | 0.035" via with no mask | Dedicated pad preferred | Vias are acceptable for low-density boards |
| Clearance for clip leads | 2.0mm around pad | 3.0mm | For manual test clip attachment |

### Boundary Scan (JTAG) Access

| Requirement | Specification |
|-------------|--------------|
| JTAG chain signals | TDI, TDO, TCK, TMS, TRST (optional) must be accessible |
| Access method | Dedicated test pads or connector pinout | 
| Chain topology | Document scan chain order for all JTAG-capable ICs |
| Pull-up/pull-down | TCK, TMS need pull-ups; TDI needs pull-up; TRST needs pull-down (if used) |

## Test Coverage Targets

| Coverage Metric | Prototype | Small-Batch | Production |
|----------------|-----------|-------------|------------|
| Net coverage (ICT-accessible) | >70% | >85% | >95% |
| Power rail access | All rails | All rails | All rails |
| High-value component access | All ICs, all BGAs | All ICs, all BGAs | All components >$0.50 |
| Communication bus access | At least one point per bus | All bus signals | All bus signals |
| Boundary scan | Optional | Recommended if available | Required if ICs support JTAG |

**Coverage calculation:**
```
Net coverage (%) = (Nets with test point access / Total nets) x 100
```

Exclude power and ground nets from the ratio (they should always have access but do not count as signal nets for coverage purposes).

## Test Point Placement Guidelines

### Preferred Placement
1. **Bottom side preferred** -- ICT fixtures typically probe from the bottom; keep test pads on the bottom layer when possible
2. **Away from board edges** -- minimum 3mm from board edge (fixture clamping zone)
3. **Away from mounting holes** -- minimum 3mm from mounting hole (fixture pillar zone)
4. **Grouped by function** -- cluster related test points for logical probing sequences
5. **Near source** -- place test point as close as possible to the component it tests

### Placement Restrictions
1. **Not under components** -- test pads must not be under component bodies (probe access blocked)
2. **Not in BGA fan-out** -- avoid placing test pads in BGA escape routing area (density conflict)
3. **Not on top side under heatsinks** -- heatsinks block top-side probe access
4. **Minimum spacing from tall components** -- probe fixtures need clearance from tall parts

## Fixture Types and Constraints

### Bed-of-Nails (ICT Fixture)

| Parameter | Standard | High-Density |
|-----------|----------|-------------|
| Probe pitch | 0.100" (2.54mm) | 0.050" (1.27mm) |
| Maximum probe count | ~3000 (standard frame) | ~5000 (large frame) |
| Probe travel | 0.100" (2.54mm) | 0.075" (1.9mm) |
| Board support | Vacuum or mechanical clamp | Vacuum (required for dense boards) |
| Typical cost | $2,000 - $10,000 | $10,000 - $25,000 |
| Setup time | 2-4 weeks | 4-8 weeks |

### Flying Probe

| Parameter | Specification |
|-----------|--------------|
| Probe count | 2-8 probes (simultaneous) |
| Minimum test pad size | 0.020" (0.5mm) -- smaller than bed-of-nails |
| Test speed | Slower than bed-of-nails (seconds per board vs sub-second) |
| Fixture cost | No fixture cost (programmed, not fixturized) |
| Best for | Prototype, small-batch (<1000 units) |

### Fixture Selection Guidance

| Production Volume | Recommended Method | Rationale |
|-------------------|-------------------|-----------|
| Prototype (1-50) | Flying probe or manual | No fixture cost; flexibility for design changes |
| Small-batch (50-1000) | Flying probe | Fixture cost not justified at this volume |
| Production (>1000) | Bed-of-nails ICT | Fixture cost amortized; test speed critical for throughput |

## Test Point Coverage Review Checklist

- [ ] All power rails have at least one dedicated test point
- [ ] Ground has multiple test points distributed across the board
- [ ] All communication buses (I2C, SPI, UART) have signal access points
- [ ] High-value ICs have test access to key pins (reset, clock, data)
- [ ] BGA devices have boundary scan chain access (if JTAG-capable)
- [ ] Test pad dimensions meet minimum specifications for target fixture type
- [ ] Test pad spacing meets minimum pitch for target fixture type
- [ ] Test pads are not blocked by components, heatsinks, or mechanical features
- [ ] Test pads maintain clearance from board edges and mounting holes
- [ ] Net coverage percentage meets target for production volume tier
- [ ] Test point placement favors bottom side for ICT compatibility
- [ ] Functional test points are accessible for manual probing during debug

## Test Engineer Handoff

The Manufacturing Engineer evaluates test point coverage from a manufacturing and fixture feasibility perspective. The Test Engineer (separate role) is responsible for:
- Test strategy and test case design
- Test fixture specification and procurement
- Production test procedure development
- Validation planning

The MfgE provides the coverage assessment as input to the Test Engineer's fixture design process. The coverage assessment is included in the DFM report (test point coverage section).

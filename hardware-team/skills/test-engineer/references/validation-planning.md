# Validation Planning Reference

This reference provides validation phase planning (DVT/PVT/ORT), sample sizing, acceptance criteria, and exit criteria for the Test Engineer. Use this when planning the validation campaign for a hardware product.

## 1. Validation Phases

Hardware validation is structured in three phases, each with distinct goals and unit sources:

| Phase | Full Name | Unit Source | Goal | Pipeline Stage |
|-------|-----------|-------------|------|---------------|
| DVT | Design Validation Testing | Prototype units | Verify the DESIGN meets requirements | 4. Prototype |
| PVT | Production Validation Testing | Pilot run units | Verify the PROCESS produces conforming units | 7. Pilot Run |
| ORT | Ongoing Reliability Testing | Production units | Monitor production QUALITY over time | Post-release (periodic) |

### 1.1 DVT (Design Validation Testing)

**Objective:** Confirm that the design (schematic + layout + firmware) meets all functional, environmental, and reliability requirements specified in the hardware PRD.

**Unit source:** Prototype builds (hand-assembled or small-batch PCBA)

**Typical activities:**
1. Board bring-up (power-on, basic function verification)
2. Full functional test suite against all testable requirements
3. Environmental testing (temperature, humidity, ESD as applicable)
4. Reliability testing (HALT if applicable per volume tier)
5. EMC pre-compliance screening (informal -- CompE owns formal compliance)
6. Safety evaluation (informal -- CompE owns formal safety analysis)
7. Power consumption and thermal characterization
8. Mechanical fit check (if enclosure exists)

**DVT exit criteria:**
- All critical functional tests passed on all DVT units
- Environmental tests passed (or failure root causes identified and design changes planned)
- No safety-critical failures
- All testable requirements have verified test coverage
- Known issues documented with severity and disposition

### 1.2 PVT (Production Validation Testing)

**Objective:** Confirm that the production process (assembly line, test equipment, procedures) produces units that consistently meet requirements.

**Unit source:** Pilot run units (assembled on the production line, not prototype)

**Typical activities:**
1. Run full production test flow on all pilot units
2. Measure first-pass yield (FPY) against target
3. Perform failure analysis on all failing units
4. Verify test procedure effectiveness (are the right defects being caught?)
5. Validate cycle time meets throughput requirement
6. Compare pilot unit measurements to DVT unit measurements (process-to-process correlation)
7. Verify programming and serialization procedures work at line speed
8. Run abbreviated environmental tests on sample units (confirm no process-induced degradation)

**PVT exit criteria:**
- First-pass yield meets target (>= 95% for small-batch, >= 98% for production)
- No systematic failure modes (individual random failures are acceptable)
- Production test procedures execute within target cycle time
- Test data logging and traceability confirmed operational
- Pilot unit measurements correlate with DVT measurements (no significant shifts)

### 1.3 ORT (Ongoing Reliability Testing)

**Objective:** Monitor production quality over time by periodically sampling production units for extended testing.

**Unit source:** Random sample from production (pulled from end of production line)

**Typical activities:**
1. Pull sample units at defined intervals (e.g., weekly, per-lot, or per-N-units)
2. Run extended functional test (more comprehensive than production screening)
3. Run environmental stress (temperature cycling, humidity)
4. Run accelerated aging (burn-in or extended operation)
5. Compare results to baseline established during DVT/PVT
6. Track trend data for early warning of process drift

**ORT exit criteria (per sample):**
- All sample units pass extended functional test
- Environmental stress results within baseline +/- acceptable drift
- No new failure modes introduced since PVT
- MTBF estimate remains above target

## 2. Sample Sizing

### 2.1 DVT Sample Size

DVT sample size depends on test type and available prototype units:

| Test Type | Minimum Sample | Recommended | Rationale |
|-----------|---------------|-------------|-----------|
| Functional (full suite) | All available units | All units | Maximize data from expensive prototypes |
| Temperature cycling | 3 units | 5 units | Statistical minimum for pass/fail |
| Humidity | 2 units | 3 units | Destructive/time-consuming |
| Vibration | 2 units | 3 units | Destructive |
| HALT | 2 units | 3 units | Push to failure (destructive) |
| ESD | 3 units | 5 units | Per IEC 61000-4-2 (multiple discharge points) |

**Practical constraint:** Prototype builds are expensive. DVT sample size is often limited by budget. Prioritize: functional (all units) > ESD > temperature > humidity > vibration > HALT.

### 2.2 PVT Sample Size

PVT sample size = full pilot run (test all units). The pilot run itself is sized based on production readiness:

| Production Volume | Recommended Pilot Run Size | Rationale |
|------------------|---------------------------|-----------|
| Small-batch (10-100) | 10-20 units | Enough to calculate meaningful FPY |
| Small-batch (100-1000) | 20-50 units | Better statistical significance |
| Production (1000+) | 50-100 units | Production-representative sample |

### 2.3 ORT Sample Size

ORT sample size follows statistical sampling plans:

| Risk Level | Sample Plan | Reference |
|-----------|-------------|-----------|
| Standard | AQL-based per ISO 2859-1 (Inspection Level II) | General quality level |
| Reduced | Reduced inspection per ISO 2859-1 (after 10 consecutive lots accepted) | Proven process |
| Tightened | Tightened inspection per ISO 2859-1 (after 2 of 5 lots rejected) | Process concern |

**Simplified ORT sampling (when formal AQL not required):**
- Pull 1-3 units per production lot (or per week, whichever is more frequent)
- Run extended test + abbreviated environmental
- Maintain trend charts for key measurements

## 3. Acceptance Criteria Frameworks

### 3.1 Attribute Testing (Pass/Fail)

For tests with binary outcomes (pass or fail):

| Criteria | Formula | Example |
|----------|---------|---------|
| Zero failures | c = 0 (acceptance number) | 5 units tested, 0 failures required |
| Acceptance number | Per ISO 2859-1 sampling tables | Lot size 1000, AQL 1.0%, sample 80, accept on 2 |

### 3.2 Variable Testing (Measurements)

For tests with numeric measurements:

| Method | When to Use | How |
|--------|------------|-----|
| Specification limits | Design verification | Each measurement must fall within [min, max] from requirements |
| Cpk analysis | Process capability (PVT/ORT) | Cpk >= 1.33 indicates capable process (4-sigma) |
| Trend monitoring | Ongoing quality (ORT) | Track mean and standard deviation; alert on shift > 1.5 sigma |

### 3.3 Reliability Acceptance

| Method | Requirement | How |
|--------|------------|-----|
| MTBF demonstration | MTBF >= target hours | Test N units for T hours each; total test time >= MTBF target * chi-squared factor |
| HALT margins | Operating margin >= X degrees/G beyond spec | Push until failure; report margin between spec limit and failure point |
| Zero-failure acceptance | N units, T hours, zero failures | Confidence = 1 - (1 - R)^(N*T/mission_time) |

## 4. Validation Scheduling

### 4.1 Typical DVT Timeline

| Week | Activity | Prerequisite |
|------|----------|-------------|
| 1 | Board bring-up, power verification | Prototype boards received |
| 1-2 | Functional test (manual bench) | Bring-up complete |
| 2-3 | Automated functional test (if fixture ready) | Test fixture, firmware |
| 3-4 | Environmental testing (temperature, ESD) | Functional test passed |
| 4-6 | Reliability testing (HALT, if applicable) | Environmental test passed |
| 6 | DVT report and exit review | All tests complete |

### 4.2 Typical PVT Timeline

| Week | Activity | Prerequisite |
|------|----------|-------------|
| 1 | Pilot run production | Production line ready |
| 1-2 | Full production test on all pilot units | Pilot units assembled |
| 2 | Yield analysis, failure analysis | Test data collected |
| 2-3 | Abbreviated environmental (sample units) | FPY meets target |
| 3 | PVT report and exit review | All analysis complete |

## 5. Test Readiness Review Checklist

Before starting each validation phase, verify readiness:

| Item | DVT | PVT | Check |
|------|-----|-----|-------|
| Test strategy approved | Required | N/A (carry from DVT) | [ ] |
| Test procedures written | Required | Required (production procedures) | [ ] |
| Test equipment available and calibrated | Required | Required | [ ] |
| Test fixture built and verified | If needed | Required (production fixture) | [ ] |
| Firmware available (test build or production) | Required | Required (production build) | [ ] |
| Test data logging system operational | Recommended | Required | [ ] |
| Units available | Prototype units received | Pilot run units received | [ ] |
| Pass/fail criteria defined | Required | Required | [ ] |
| Exit criteria defined | Required | Required | [ ] |

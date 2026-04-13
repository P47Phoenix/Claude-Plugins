# Environmental Compliance Reference

This reference provides environmental regulation requirements for the Compliance Engineer, covering RoHS, REACH, and WEEE obligations.

## 1. RoHS (Restriction of Hazardous Substances)

### 1.1 Directive Overview

- **Current directive:** RoHS 3 -- Directive 2011/65/EU as amended by Delegated Directive (EU) 2015/863
- **Scope:** Electrical and electronic equipment (EEE) placed on the EU market
- **Effective dates:** Original 6 substances since 2006; 4 phthalates since July 22, 2019 (July 22, 2021 for medical devices and monitoring/control instruments)

### 1.2 Restricted Substances and Thresholds

| Substance | Maximum Concentration (by weight in homogeneous material) |
|-----------|----------------------------------------------------------|
| Lead (Pb) | 0.1% (1000 ppm) |
| Mercury (Hg) | 0.1% (1000 ppm) |
| Cadmium (Cd) | 0.01% (100 ppm) |
| Hexavalent Chromium (Cr6+) | 0.1% (1000 ppm) |
| Polybrominated Biphenyls (PBB) | 0.1% (1000 ppm) |
| Polybrominated Diphenyl Ethers (PBDE) | 0.1% (1000 ppm) |
| Bis(2-ethylhexyl) phthalate (DEHP) | 0.1% (1000 ppm) |
| Butyl benzyl phthalate (BBP) | 0.1% (1000 ppm) |
| Dibutyl phthalate (DBP) | 0.1% (1000 ppm) |
| Diisobutyl phthalate (DIBP) | 0.1% (1000 ppm) |

### 1.3 Common Exemptions

Some applications are exempt from specific substance restrictions. Exemptions have expiry dates and must be tracked.

| Exemption # | Substance | Application | Status |
|-------------|-----------|-------------|--------|
| 6(a) | Lead | Lead in high-melting-temperature solder (>85% Pb) | Valid (review pending) |
| 6(b) | Lead | Lead in solder for servers, storage, networking (until exemption expires) | Valid (review pending) |
| 6(c) | Lead | Lead in micro-electromechanical systems solder | Valid |
| 7(a) | Lead | Lead in high-temperature ceramic or glass solder | Valid |
| 7(c)-I | Lead | Lead in electrical/electronic components in glass or ceramic (e.g., piezo, thick-film resistors) | Valid |
| 15 | Lead | Lead in solder for flip-chip IC packages | Valid |

**Important:** Exemption status must be verified at each compliance review. Expired or revoked exemptions require component substitution.

### 1.4 RoHS Compliance Verification Process

1. **BOM review:** For every component on the BOM, verify a RoHS compliance declaration exists
2. **Supplier declarations:** Collect material declarations (IPC-1752A or equivalent) from component suppliers
3. **Exemption tracking:** If any component claims a RoHS exemption, document the exemption number and expiry date
4. **Custom parts:** Any custom-manufactured parts (connectors, enclosures, cables) must have material composition verified
5. **Solder paste:** Verify solder paste composition is lead-free (SAC305 or equivalent) unless an exemption applies

### 1.5 RoHS Checklist Template

```markdown
| # | BOM Ref | Component | Supplier Declaration | RoHS Status | Exemption | Notes |
|---|---------|-----------|---------------------|-------------|-----------|-------|
| 1 | C1-C20 | 100nF MLCC | Yes (IPC-1752A) | Compliant | None | |
| 2 | U1 | MCU | Yes (manufacturer website) | Compliant | None | |
| 3 | J1 | Connector | MISSING | UNKNOWN | N/A | Action: request from supplier |
```

## 2. REACH (Registration, Evaluation, Authorisation, and Restriction of Chemicals)

### 2.1 Regulation Overview

- **Regulation:** (EC) No 1907/2006
- **Scope:** All substances in articles placed on the EU market
- **Key obligation for hardware:** Article 33 -- duty to communicate if an article contains an SVHC above 0.1% w/w

### 2.2 SVHC (Substances of Very High Concern)

The SVHC Candidate List is updated biannually (typically January and July). As of the latest update, the list contains 200+ substances.

**Compliance process:**
1. Screen all materials in the product against the current SVHC Candidate List
2. If any SVHC is present above 0.1% w/w in any article, the duty to communicate applies
3. Communicate SVHC identity to the customer (at minimum, sufficient information for safe use)
4. Notify ECHA via SCIP database for articles containing SVHCs above 0.1% w/w

### 2.3 Common SVHCs in Electronics

| Substance | Where Found | Typical Threshold Risk |
|-----------|------------|----------------------|
| Lead (Pb) | Solder, component terminations, piezo ceramics | Covered by RoHS (separate obligation) |
| DEHP, BBP, DBP, DIBP | Cable insulation, plastic housings, adhesives | Covered by RoHS; also REACH obligation |
| Boric acid | Flux formulations | Check flux material safety data sheets |
| Cobalt compounds | Battery cathodes (Li-ion) | Relevant if product contains a battery |

### 2.4 REACH Compliance Verification Process

1. **SVHC screening:** Request full material disclosure (FMD) from suppliers or use industry SVHC screening tools
2. **Concentration calculation:** For each identified SVHC, calculate concentration at the article level (not product level -- each distinct article is evaluated independently)
3. **SCIP notification:** If >0.1% w/w in any article, prepare SCIP database notification
4. **Documentation:** Maintain records of SVHC screening results and supplier declarations

## 3. WEEE (Waste Electrical and Electronic Equipment)

### 3.1 Directive Overview

- **Directive:** 2012/19/EU (WEEE 2)
- **Scope:** Producers of EEE placed on the EU market
- **Key obligation:** Registration with national WEEE compliance schemes, financing of collection and recycling

### 3.2 WEEE Classification Categories

| Category | Description | Examples |
|----------|-------------|---------|
| 1 | Temperature exchange equipment | Refrigerators, heat pumps |
| 2 | Screens and monitors | TVs, monitors, laptops |
| 3 | Lamps | LED lamps, fluorescent tubes |
| 4 | Large equipment (>50 cm) | Servers, large printers |
| 5 | Small equipment (<=50 cm) | IoT devices, small sensors, embedded systems |
| 6 | Small IT and telecom (<50 cm) | Phones, routers, GPS |

### 3.3 WEEE Compliance for Hardware Projects

Most hardware projects in this pipeline fall into Category 5 or 6. Key obligations:

1. **Crossed-out wheelie bin marking:** Required on product or packaging
2. **Producer registration:** Register with WEEE compliance scheme in each EU member state where product is sold
3. **Financing:** Contribute to WEEE collection/recycling costs (typically per-unit or per-kg fee)
4. **Design for recycling:** Consider disassembly, material identification, and hazardous material removal in product design

**Note:** WEEE registration is a business/regulatory obligation, not a design issue. The CompE flags the WEEE category and marking requirement; the business handles registration.

## 4. Environmental Compliance Checklist Template

```markdown
## Environmental Compliance Checklist
**Project:** <project_name>
**Date:** <ISO 8601>

### RoHS Compliance
| Status | Detail |
|--------|--------|
| BOM RoHS screen complete | YES/NO -- <X>/<Y> components verified |
| All supplier declarations collected | YES/NO -- <missing list> |
| Exemptions documented | YES/NO/N-A -- <exemption list with expiry> |
| Solder paste compliance verified | YES/NO |
| Custom parts verified | YES/NO/N-A |

### REACH Compliance
| Status | Detail |
|--------|--------|
| SVHC screening complete | YES/NO |
| SVHCs above 0.1% w/w identified | YES/NO -- <substance list> |
| SCIP notification required | YES/NO |
| Supplier declarations on file | YES/NO |

### WEEE
| Status | Detail |
|--------|--------|
| WEEE category determined | Category <X> |
| Wheelie bin marking included | YES/NO |
| Producer registration noted | YES/NO (business action) |
```

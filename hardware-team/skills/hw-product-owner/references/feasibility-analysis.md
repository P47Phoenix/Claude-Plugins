# Feasibility Analysis Frameworks

This reference provides structured frameworks for technical feasibility assessment, trade-off analysis, and risk scoring used by the Hardware Product Owner.

## 1. Technical Feasibility Assessment

### 1.1 Assessment Dimensions

Evaluate feasibility across five dimensions. Each dimension gets a RED/YELLOW/GREEN rating.

| Dimension | GREEN (Feasible) | YELLOW (Feasible with Risk) | RED (Infeasible / Needs Redesign) |
|-----------|-----------------|---------------------------|----------------------------------|
| **Technical maturity** | Proven technology, reference designs exist | New combination of proven technologies | Unproven technology, no reference designs |
| **Component availability** | Multiple sources, stock available, standard lead times | Single source or long lead time but available | End-of-life, allocation, or sole-source with no stock |
| **Manufacturing complexity** | Standard PCB + SMT assembly | Fine-pitch BGA, HDI, flex-rigid | Exotic processes, custom tooling, untested assembly |
| **Schedule alignment** | Comfortable margin to deadline | Tight but achievable with parallel tracks | Cannot meet deadline with known approach |
| **Cost alignment** | BOM target achievable with margin | BOM target achievable but tight | BOM exceeds hard limit with current architecture |

### 1.2 Feasibility Report Template

```markdown
## Feasibility Assessment: <Product/Feature Name>

**Date:** <ISO 8601>
**Assessor:** HW Product Owner

### Summary
| Dimension | Rating | Key Finding |
|-----------|--------|-------------|
| Technical maturity | GREEN/YELLOW/RED | <one line> |
| Component availability | GREEN/YELLOW/RED | <one line> |
| Manufacturing complexity | GREEN/YELLOW/RED | <one line> |
| Schedule alignment | GREEN/YELLOW/RED | <one line> |
| Cost alignment | GREEN/YELLOW/RED | <one line> |

**Overall:** FEASIBLE / FEASIBLE WITH RISK / NOT FEASIBLE

### Detailed Findings
<Expand on each dimension with supporting data>

### Risks Identified
| Risk | Dimension | Likelihood | Impact | Mitigation |
|------|-----------|-----------|--------|-----------|
| <risk> | <dimension> | H/M/L | H/M/L | <mitigation> |

### Recommendations
1. <recommendation>

### Go/No-Go Recommendation
<PROCEED / PROCEED WITH CONDITIONS / DO NOT PROCEED>
<Conditions if applicable>
```

### 1.3 Scoring Rules

- **Any RED** dimension: Overall rating is NOT FEASIBLE unless a mitigation plan converts it to YELLOW
- **Two or more YELLOW**: Overall rating is FEASIBLE WITH RISK -- document all mitigations
- **All GREEN**: Overall rating is FEASIBLE
- **Override**: The HW PO can override with documented rationale (e.g., "RED on schedule but accepting risk because market window is critical")

## 2. Trade-Off Analysis Methodology

### 2.1 Weighted Criteria Matrix (Pugh Matrix Variant)

Use this when comparing two or more design options against multiple criteria.

**Process:**

1. **Define criteria** -- List all relevant evaluation criteria
2. **Assign weights** -- Each criterion gets a weight from 1 (low importance) to 5 (critical). Weights must be agreed with stakeholders before scoring.
3. **Score options** -- Each option scores 1-5 on each criterion. Score independently (do not compare options while scoring).
4. **Calculate weighted scores** -- Weight x Score for each cell. Sum columns.
5. **Analyze** -- Highest total wins, but check for any criterion where the winner scores < 2 (unacceptable weakness).
6. **Document** -- Use the Decision Record pattern from SKILL.md.

### 2.2 Common Trade-Off Scenarios in Hardware

| Trade-Off | Typical Tension | Resolution Pattern |
|-----------|----------------|-------------------|
| Cost vs. performance | Higher-performance ICs cost more | Define minimum acceptable performance, then optimize cost |
| Size vs. thermal | Smaller boards have less thermal margin | Thermal simulation early; consider active cooling cost |
| Schedule vs. quality | Rushing leads to respins | Identify critical path; parallelize non-critical work |
| Power vs. features | More features draw more power | Power budget allocation per subsystem with hard limits |
| Custom vs. COTS module | Custom is cheaper at volume but slower to develop | Break-even analysis: at what volume does custom win? |
| Single source vs. cost | Cheapest part may have one supplier | Require dual-source for P1 components; accept single-source for P3 |
| Layer count vs. cost | More PCB layers cost more but simplify routing | Start with minimum viable layer count; add only if routing demands |

### 2.3 Break-Even Analysis for Volume Decisions

For make-vs-buy and custom-vs-COTS decisions, calculate the break-even volume:

```
Break-even volume = NRE_cost / (per_unit_savings)

Where:
  NRE_cost = Non-recurring engineering cost of custom design
  per_unit_savings = (COTS_unit_cost - custom_unit_cost)
```

**Decision rule:**
- If expected lifetime volume > 2x break-even volume: Custom design is justified
- If expected lifetime volume < break-even volume: Use COTS
- If between 1x and 2x: Risk analysis required (what if volume is lower than expected?)

## 3. Risk Scoring Framework

### 3.1 Likelihood x Impact Matrix

|  | Impact: Low | Impact: Medium | Impact: High |
|---|---|---|---|
| **Likelihood: High** | MEDIUM risk | HIGH risk | CRITICAL risk |
| **Likelihood: Medium** | LOW risk | MEDIUM risk | HIGH risk |
| **Likelihood: Low** | LOW risk | LOW risk | MEDIUM risk |

### 3.2 Likelihood Definitions (Hardware-Specific)

| Rating | Definition | Examples |
|--------|-----------|----------|
| **High** | >50% probability, or has happened on similar projects | Component goes EOL during development; schedule slips on PCB respin; first-revision board has signal integrity issues |
| **Medium** | 10-50% probability, plausible but not expected | Supplier lead time increases; regulatory standard updated mid-project; thermal margin insufficient |
| **Low** | <10% probability, unlikely but possible | Supplier factory fire; major regulatory change; complete architecture failure |

### 3.3 Impact Definitions (Hardware-Specific)

| Rating | Definition | Consequences |
|--------|-----------|-------------|
| **High** | Project cannot ship, or BOM exceeds hard limit, or schedule slips > 4 weeks | Requires architecture change, new board spin, or stakeholder escalation |
| **Medium** | Degraded performance, BOM 5-15% over target, or schedule slips 1-4 weeks | Requires trade-off decision, workaround, or component substitution |
| **Low** | Minor inconvenience, BOM < 5% impact, schedule < 1 week | Handled within existing margin/contingency |

### 3.4 Risk Response Strategies

| Strategy | When to Use | Example |
|----------|------------|---------|
| **Avoid** | Eliminate the risk by changing the design | Switch from sole-source IC to multi-source alternative |
| **Mitigate** | Reduce likelihood or impact | Qualify alternate supplier; add thermal margin; schedule buffer |
| **Transfer** | Shift risk to another party | Use turnkey assembly (CM bears procurement risk); purchase insurance |
| **Accept** | Risk is within tolerance | Document in risk register; monitor; allocate contingency budget |

## 4. Supply Chain Risk Assessment

### 4.1 Component Risk Factors

| Factor | Low Risk | Medium Risk | High Risk |
|--------|---------|-------------|-----------|
| **Number of suppliers** | 3+ qualified sources | 2 qualified sources | Single source |
| **Lead time** | < 8 weeks | 8-16 weeks | > 16 weeks or allocation |
| **Lifecycle status** | Active, recommended for new designs | Mature, no EOL notice | NRND, EOL announced, or last-time-buy |
| **Geopolitical exposure** | Diverse supply chain | Concentrated in one region | Sole fab in geopolitically sensitive area |
| **Inventory model** | Standard distributor stock | MOQ with reasonable minimums | Custom order, long pipeline |

### 4.2 Mitigation Strategies

1. **Dual-source all P1 components** -- Identify and qualify an alternate for every critical part
2. **Buffer stock** -- For long-lead or allocation-prone components, budget for safety stock
3. **Design for substitution** -- Footprint-compatible alternates where possible (e.g., LDO pinout families)
4. **Lifecycle monitoring** -- Track component lifecycle status; react to PCN (Product Change Notices) early
5. **Approved Vendor List (AVL)** -- Maintain an AVL with minimum two approved sources per critical component

# DFA Guidelines

This reference defines the Design for Assembly (DFA) review checklist, assembly yield risk factors, and remediation guidance used by the Manufacturing Engineer during DFA review.

## Assembly Review Checklist

### 1. Component Placement Clearances

| Check | Requirement | Why It Matters |
|-------|-------------|---------------|
| Component-to-component (same side) | Minimum 0.5mm body-to-body for standard SMT; 1.0mm for tall components | Pick-and-place nozzle clearance; rework access |
| Component-to-board-edge | Minimum 1.0mm body-to-edge for routed boards; 3.0mm for V-score | Mechanical stress during depaneling; conveyor rail clearance |
| Component-to-via (unmasked) | Minimum 0.25mm pad-to-via-pad | Solder wicking into via during reflow |
| Connector overhang | Connectors must not extend beyond board edge unless mechanically supported | Assembly handling; mechanical stress on solder joints |
| Keep-out zones | No components under heatsinks, near mounting holes, or in clamping areas | Assembly interference; mechanical stress |

### 2. Orientation Consistency

| Check | Requirement | Why It Matters |
|-------|-------------|---------------|
| Polarized component marking | Pin 1 / polarity indicators visible after assembly (not under body) | Optical inspection (AOI); rework orientation |
| IC orientation consistency | All ICs on the same side should have consistent pin 1 orientation (same corner) | Reduces placement errors; simplifies inspection |
| Polarity indicator on silkscreen | Diodes, electrolytic caps, tantalum caps must have polarity marking on silkscreen | Manual inspection; rework guidance |
| Asymmetric pad patterns | Polarized components should have asymmetric pads or clear silkscreen indicators | Prevents reverse placement by pick-and-place |

### 3. Solder Paste and Stencil

| Check | Requirement | Why It Matters |
|-------|-------------|---------------|
| Stencil aperture ratio | Area ratio >= 0.66 for standard; >= 0.50 for fine-pitch (Type 4/5 paste) | Insufficient paste transfer causes opens/insufficient joints |
| Paste-to-pad alignment | Stencil apertures centered on pads; 1:1 or reduced aperture size | Misalignment causes bridging or insufficients |
| Fine-pitch QFP stencil | Aperture width <= pad width; length may be reduced 10-20% for bridge prevention | QFP pins at 0.5mm pitch are bridging-prone |
| BGA stencil apertures | Circular or square apertures; diameter = 80-90% of pad diameter for 0.8mm+ pitch; custom for smaller | BGA joint volume must be controlled |
| Thermal pad stencil | Window-pane (cross-hatch) aperture pattern for large thermal pads | Prevents voiding and mid-chip solder balls |

### 4. Thermal Relief

| Check | Requirement | Why It Matters |
|-------|-------------|---------------|
| Ground plane connections | Pads connected to ground plane via thermal relief spokes, not direct connect | Direct connect creates thermal imbalance; tombstone risk; poor hand-solder/rework |
| Power plane connections | Power pads with thermal relief unless high-current path requires direct connect | Same thermal imbalance concerns; document exception for high-current paths |
| Unequal thermal mass | Flag pad pairs where one pad connects to copper pour and the other does not | Primary cause of tombstoning on small passives |
| Large copper area pads | Pads on large copper areas need thermal relief or preheat specification | Reflow may not reach liquidus without extended soak |

### 5. Tombstone Risk Assessment

Tombstoning occurs when one end of a passive component lifts off its pad during reflow due to unequal wetting forces.

| Risk Factor | Assessment | Mitigation |
|-------------|-----------|------------|
| 0402 / 0201 passives | HIGH risk for all 0402 and smaller | Pad geometry optimization; balanced thermal; consider 0603 substitution |
| Unequal pad thermal mass | HIGH -- one pad on ground pour, other floating | Add thermal relief to ground-connected pad |
| Unequal trace routing | MEDIUM -- wide trace on one pad, thin on other | Balance copper connection width at pad |
| Pad geometry asymmetry | MEDIUM -- different pad shapes or sizes | Equalize pad geometry per IPC-7351 |
| Reflow profile | LOW to MEDIUM -- ramp rate too aggressive | Specify slower ramp rate in reflow profile (1-2 C/sec) |

### 6. BGA Assembly

| Check | Requirement | Why It Matters |
|-------|-------------|---------------|
| Via-in-pad under BGA | Must be filled and planarized (VIPPO) | Unfilled vias wick solder, creating voids and insufficient joints |
| BGA pad size | Non-solder-mask-defined (NSMD) preferred; pad = ball size minus 20% | Better self-centering during reflow |
| BGA site flatness | Board warp < 0.75% of diagonal at BGA location | Excess warp prevents ball contact during placement |
| BGA rework access | Minimum 3mm clearance around BGA for rework nozzle | BGA rework requires hot-air nozzle clearance |
| BGA X-ray inspection | Board design must allow X-ray angle for void inspection | Verify no tall components block X-ray path to BGA |

### 7. Mixed Technology

| Combination | Complexity | Guidance |
|-------------|-----------|----------|
| SMT top-side only | Low | Standard reflow process |
| SMT both sides | Medium | Double reflow; bottom-side components must survive second reflow (glue or gravity) |
| SMT + through-hole (few) | Medium | Reflow + selective soldering or hand-solder for THT |
| SMT + through-hole (many) | High | Reflow + wave solder; wave-side SMT needs glue; consider all-SMT redesign |
| SMT + press-fit | Medium | Reflow first, then press-fit insertion (no thermal exposure for press-fit) |

**Guideline:** Minimize the number of assembly process steps. Each additional step (second reflow, wave, selective, manual) adds cost and yield risk.

### 8. Moisture Sensitivity Level (MSL)

| MSL | Floor Life (at <30C / <60% RH) | Handling |
|-----|------|---------|
| MSL 1 | Unlimited | No special handling |
| MSL 2 | 1 year | Standard handling; flag for storage awareness |
| MSL 2a | 4 weeks | Dry-pack required for long storage; bake before assembly if exposed |
| MSL 3 | 168 hours (7 days) | Dry-pack required; bake before assembly if floor life exceeded |
| MSL 4 | 72 hours | Strict dry-pack; bake likely needed; flag in BOM |
| MSL 5 | 48 hours | Must bake before assembly unless just opened from dry-pack |
| MSL 5a | 24 hours | Must bake; assembly must complete within floor life after bake |
| MSL 6 | Bake before use | Always requires bake; must be assembled within reflow time limit |

**Review action:** For each plastic-packaged IC (QFP, BGA, QFN, etc.), verify MSL rating. Flag MSL 3 and above in the DFA report with handling requirements. MSL 4+ components may require special assembly scheduling.

## Assembly Complexity Rating

Rate the overall assembly complexity based on findings:

| Rating | Criteria |
|--------|----------|
| **Low** | SMT one side only; no fine-pitch (<0.5mm); no BGA; all 0603+ passives; single reflow |
| **Medium** | SMT both sides OR fine-pitch components OR BGA present OR mixed SMT+THT (few); 2 process steps max |
| **High** | Multiple BGAs OR 0402/0201 passives OR mixed SMT+wave OR 3+ process steps OR MSL 4+ components |

## Remediation Priority

When multiple DFA issues exist, prioritize fixes in this order:
1. **Critical** -- design change required before assembly (e.g., BGA via-in-pad not filled)
2. **Major** -- high yield risk, should fix before prototype (e.g., tombstone-prone layout)
3. **Minor** -- optimization for production, acceptable for prototype (e.g., orientation inconsistency)

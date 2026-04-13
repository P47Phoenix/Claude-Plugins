# Stackup Design Patterns

Reference document for the PCB Layout Engineer role. Load this file for stackup-design tasks.

---

## 1. Layer Assignment Strategy

### 1.1 Layer Types

| Type | Purpose | Design Rules |
|------|---------|-------------|
| Signal | Trace routing for signal nets | Controlled impedance; adjacent to reference plane |
| Ground | Return path reference plane; EMI shielding | Solid, unbroken copper pour; minimal splits |
| Power | Power distribution (VCC, 3V3, 5V, etc.) | Can be split into voltage islands; copper pour |
| Mixed | Signal traces + copper pour fill | Used when layer count is constrained; careful planning required |

### 1.2 Assignment Principles

1. **Every signal layer must have an adjacent ground or power plane as its reference** -- this is non-negotiable for impedance control
2. **Prefer ground planes over power planes as references** -- ground planes are solid; power planes may have splits that disrupt return paths
3. **Place high-speed signals on layers adjacent to ground planes** -- best reference plane quality
4. **Outer layers for components and short routing; inner layers for long runs** -- outer layers have microstrip geometry; inner layers have stripline (better shielding)
5. **Symmetrical stackup** -- copper distribution should be symmetric about the board center to prevent warping during lamination

---

## 2. Common Stackup Configurations

### 2.1 Two-Layer Stackup

```
Layer 1: Signal + Ground pour (Top)
         Dielectric (core): ~62 mil (1.6mm)
Layer 2: Signal + Ground pour (Bottom)
```

**Use when:** Simple designs, low component count, no controlled impedance, cost-critical
**Limitations:** No dedicated reference plane; poor EMI performance; impedance control very limited
**Impedance:** Approximate 50-ohm single-ended with careful trace/ground-pour management

### 2.2 Four-Layer Stackup (Recommended Minimum)

```
Layer 1: Signal (Top)         -- microstrip, referenced to L2
         Prepreg: ~4-8 mil
Layer 2: Ground (GND)         -- solid reference plane
         Core: ~40-47 mil
Layer 3: Power (VCC)          -- power distribution
         Prepreg: ~4-8 mil
Layer 4: Signal (Bottom)      -- microstrip, referenced to L3
```

**Use when:** Most general-purpose designs; moderate complexity; controlled impedance needed
**Advantages:** Solid ground reference for both signal layers; good EMI performance
**Caution:** L4 is referenced to power plane (L3) -- power plane splits create return path issues for L4 signals. Route sensitive signals on L1 (referenced to solid ground) when possible.

**Alternative 4-layer (signal-heavy):**
```
Layer 1: Signal (Top)
         Prepreg: ~4-8 mil
Layer 2: Ground (GND)
         Core: ~40-47 mil
Layer 3: Signal + Ground pour
         Prepreg: ~4-8 mil
Layer 4: Ground (GND) + Power islands
```

This variant provides ground reference for both internal signal layers but requires power to be routed as traces or islands on L4.

### 2.3 Six-Layer Stackup

```
Layer 1: Signal (Top)         -- microstrip, ref L2
         Prepreg: ~4-5 mil
Layer 2: Ground (GND1)        -- reference for L1 and L3
         Core: ~8-10 mil
Layer 3: Signal (Inner 1)     -- stripline, ref L2 and L4
         Prepreg: ~4-5 mil
Layer 4: Power (VCC)          -- power distribution
         Core: ~8-10 mil
Layer 5: Signal (Inner 2)     -- stripline, ref L4 and L6
         Prepreg: ~4-5 mil
Layer 6: Signal (Bottom)      -- microstrip, ref L5? No -- needs a reference

```

**Better 6-layer stackup:**
```
Layer 1: Signal (Top)         -- microstrip, ref L2
         Prepreg: ~3-5 mil
Layer 2: Ground (GND1)        -- reference for L1 and L3
         Core: ~10 mil
Layer 3: Signal (Inner 1)     -- stripline between L2 and L4
         Prepreg: ~10 mil
Layer 4: Power (VCC)          -- reference for L3 and L5 (with caveats)
         Core: ~10 mil
Layer 5: Ground (GND2)        -- reference for L6
         Prepreg: ~3-5 mil
Layer 6: Signal (Bottom)      -- microstrip, ref L5
```

**Use when:** Moderate-to-high complexity; multiple power domains; need for inner routing layers
**Advantages:** Two dedicated ground planes; all signal layers have adjacent reference planes
**Note:** L3 signal layer referenced to GND1 (L2) on top and VCC (L4) on bottom -- if power plane has splits, L3 signals crossing the split will have return path issues

### 2.4 Eight-Layer Stackup

```
Layer 1: Signal (Top)         -- microstrip, ref L2
         Prepreg: ~3-4 mil
Layer 2: Ground (GND1)        -- reference for L1, L3
         Core: ~8 mil
Layer 3: Signal (Inner 1)     -- stripline, ref L2, L4
         Prepreg: ~5 mil
Layer 4: Power (VCC1)         -- power distribution
         Core: ~20 mil        (thick core for rigidity)
Layer 5: Power (VCC2)         -- power distribution (second domain)
         Prepreg: ~5 mil
Layer 6: Signal (Inner 2)     -- stripline, ref L5, L7? or L7 is GND
         Core: ~8 mil
Layer 7: Ground (GND2)        -- reference for L6, L8
         Prepreg: ~3-4 mil
Layer 8: Signal (Bottom)      -- microstrip, ref L7
```

**Use when:** High complexity; multiple power domains; high-speed interfaces; BGA components
**Advantages:** Excellent signal integrity; multiple routing layers with solid references; good power distribution

**Preferred 8-layer for high-speed:**
```
Layer 1: Signal (Top)
Layer 2: Ground (GND1)
Layer 3: Signal (Inner 1)
Layer 4: Ground (GND2)
Layer 5: Power (VCC)
Layer 6: Signal (Inner 2)
Layer 7: Ground (GND3)
Layer 8: Signal (Bottom)
```
Every signal layer has an adjacent ground plane. Best for signal integrity but uses 3 of 8 layers for ground.

---

## 3. Impedance Calculation Parameters

### 3.1 Common Dielectric Materials

| Material | Er (typical) | Loss Tangent | Cost | Notes |
|----------|-------------|-------------|------|-------|
| FR-4 (standard) | 4.2-4.6 | 0.020-0.025 | Low | Most common; adequate to ~1 GHz |
| FR-4 (mid-loss) | 4.0-4.4 | 0.012-0.018 | Medium | Good for GHz-range signals |
| Isola 370HR | 3.9-4.2 | 0.016 | Medium | Popular mid-range material |
| Megtron 6 | 3.3-3.7 | 0.004 | High | High-speed (10+ Gbps) |
| Rogers 4003C | 3.38 | 0.0027 | Very high | RF/microwave applications |

### 3.2 Copper Weights

| Weight (oz) | Thickness (mil) | Thickness (um) | Typical Use |
|-------------|----------------|----------------|------------|
| 0.5 oz | 0.7 mil | 17.5 um | Fine-pitch, HDI inner layers |
| 1.0 oz | 1.4 mil | 35 um | Standard outer and inner layers |
| 2.0 oz | 2.8 mil | 70 um | Power-heavy designs, high current |
| 3.0 oz | 4.2 mil | 105 um | Heavy power, bus bars |

### 3.3 Standard Board Thicknesses

| Thickness | Common Applications |
|-----------|-------------------|
| 0.8 mm (31 mil) | Thin boards, flex-rigid, compact devices |
| 1.0 mm (39 mil) | Compact consumer electronics |
| 1.6 mm (63 mil) | Industry standard; most designs default to this |
| 2.0 mm (79 mil) | High layer count, structural rigidity needed |
| 2.4 mm (94 mil) | Very high layer count (12+) |

---

## 4. Copper Balance and Warpage Prevention

### 4.1 The Symmetry Rule

The stackup must be symmetric about the board center plane. For each layer N from the top, the corresponding layer from the bottom should have:
- Same copper weight
- Similar copper coverage percentage
- Same dielectric thickness to the adjacent core

### 4.2 Copper Coverage Targets

| Coverage | Assessment | Action |
|----------|-----------|--------|
| >80% | Excellent | No action needed |
| 60-80% | Good | Monitor during fabrication |
| 40-60% | Marginal | Add copper fill/thieving patterns |
| <40% | Poor | Copper thieving required; risk of warpage |

### 4.3 Copper Thieving

When a layer has low copper coverage:
1. Add copper fill (ground pour) in unused areas
2. If ground pour is not possible (noise concerns), add non-functional copper thieving patterns
3. Thieving patterns should be dots or hatched patterns that do not connect to any net
4. Fab houses may add thieving automatically if instructed -- specify in fab notes

---

## 5. Via Considerations in Stackup Design

### 5.1 Aspect Ratio Limits

| Via Type | Typical Max Aspect Ratio | Notes |
|----------|------------------------|-------|
| Through-hole (standard fab) | 8:1 | Board thickness / drill diameter |
| Through-hole (advanced fab) | 10:1 | Check with fab house |
| Blind via | 1:1 (microvia) to 4:1 | Depends on laser vs. mechanical drill |
| Buried via | 6:1 | Requires sequential lamination |

### 5.2 HDI Stackup Considerations

For designs requiring blind/buried vias or microvias:
- Sequential lamination increases cost significantly (each lamination cycle)
- 1+N+1: one microvia layer on each side of a standard core (most common HDI)
- 2+N+2: two microvia layers on each side (for fine-pitch BGAs)
- Stacked microvias require copper filling and are more expensive than staggered
- Discuss HDI requirements with the fab house early -- it significantly affects pricing

---

## 6. Stackup Design Checklist

Use this checklist during stackup-design tasks:

- [ ] Layer count determined from routing complexity and signal integrity needs
- [ ] Every signal layer has an adjacent ground or power reference plane
- [ ] High-speed signal layers are adjacent to solid ground planes (not split power planes)
- [ ] Stackup is symmetric about the center (layer types, copper weights, dielectric thicknesses)
- [ ] Impedance targets calculated for all controlled-impedance net classes
- [ ] Dielectric material selected appropriate to signal frequencies (standard FR-4 vs. low-loss)
- [ ] Copper weights selected for current requirements (outer and inner)
- [ ] Total board thickness within mechanical constraints
- [ ] Via aspect ratios within fab capability for the selected stackup
- [ ] Copper balance assessed per layer (>60% coverage target; thieving if needed)
- [ ] Stackup reviewed against target fab house capabilities (if known)
- [ ] Impedance test coupons specified (if controlled impedance is required)

---

## 7. Stackup Selection Decision Guide

| Design Characteristic | Minimum Recommended Layers |
|----------------------|--------------------------|
| Simple, single-function, no high-speed | 2 |
| Moderate complexity, one or two controlled-impedance nets | 4 |
| Multiple power domains, several high-speed interfaces | 6 |
| BGA components, DDR memory, multiple high-speed buses | 8 |
| Very high-density, multiple BGAs, 10+ Gbps signals | 10+ |

**Cost consideration:** Each additional layer pair (2 layers) increases PCB fabrication cost by approximately 30-50%. Balance signal integrity needs against budget constraints. The HW Product Owner's BOM budget allocation for PCB fabrication is the cost ceiling.

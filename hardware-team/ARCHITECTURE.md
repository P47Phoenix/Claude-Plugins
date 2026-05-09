# hardware-team — Architecture

Hardware delivery pipeline that wraps the kicad-happy skill family in an
8-stage flow analogous to `delivery-team`. One orchestrator
(`hardware-flow`) routes work to six role skills via the Agent tool,
validates artifacts at five gates, and self-corrects within bounded rework
loops. Hooks guard the edges, `.hardware/config.yml` configures behaviour,
and `kicad-happy:*` provides the underlying KiCad automation.

## Skills (7)

| Skill | Roles / Purpose |
|-------|----------------|
| `hardware-flow/` | Pipeline orchestrator: 8 stages (Concept, Schematic, Layout, Prototype, DFM/DFA, Compliance, Pilot Run, Production Release), rework loops, gate validation, kicad-happy dispatch |
| `hw-product-owner/` | Hardware Product Owner: requirements, constraints, feasibility analysis, make-vs-buy, BOM budgeting |
| `electrical-engineer/` | Electrical Engineer: schematic design, component selection (4 distributor skills), SPICE simulation, firmware interface docs |
| `pcb-layout-engineer/` | PCB Layout Engineer: physical layout, routing, stackup design, impedance control, DRC |
| `manufacturing-engineer/` | Manufacturing Engineer: DFM/DFA review, panelization, test point coverage, fab-house integration (JLCPCB, PCBWay) |
| `compliance-engineer/` | Compliance Engineer: EMC pre-compliance, safety standards (IEC 62368-1), environmental (RoHS/REACH/WEEE), market requirements (FCC/CE/UL) |
| `test-engineer/` | Test Engineer: test strategy, fixture design, production test, validation planning |

## Hooks (6 across 3 event types)

| Hook | Event | Purpose |
|------|-------|---------|
| Session validation | SessionStart | Validates `.hardware/config.yml` exists and is current, checks paused pipeline staleness |
| kicad-happy check | SessionStart | Verifies all 11 kicad-happy skills are available, reports missing dependencies |
| Pipeline bypass detection | PreToolUse (Skill) | Warns when hardware roles invoked outside hardware-flow |
| KiCad file notification | PostToolUse (Write/Edit) | Notifies when KiCad project files are modified |
| Schematic DRC | PostToolUse (Write/Edit) | Auto-runs basic DRC validation on `.kicad_sch` modifications, reports findings as warnings |
| BOM drift detection | PostToolUse (Write/Edit) | Detects when schematic changes invalidate the current BOM, warns about inconsistencies |

## Pipeline Stages

1. **Concept** — `hw-product-owner` produces requirements, constraints, BOM budget
2. **Schematic** — `electrical-engineer` produces `.kicad_sch` + simulation evidence
3. **Layout** — `pcb-layout-engineer` produces `.kicad_pcb` + DRC clean
4. **Prototype** — `electrical-engineer` + `test-engineer` validate first article
5. **DFM/DFA** — `manufacturing-engineer` reviews for fab-house readiness
6. **Compliance** — `compliance-engineer` runs EMC pre-compliance + safety checks
7. **Pilot Run** — limited production batch with `test-engineer` test fixture
8. **Production Release** — full release with `manufacturing-engineer` sign-off

Gates 1, 3, 5, 6, 8 are hard gates that block downstream work on FAIL.

## See Also

- `delivery-team/ARCHITECTURE.md` — sibling pipeline, similar orchestration patterns
- `kicad-happy/` — underlying KiCad automation skills (separate plugin install)

# Decision: Defer BACKLOG-105 (mtg-commander Wave 0) authoring

Date: 2026-05-09
PO: Aragorn (lotr, moderate)
Decision: DEFER

## Rationale

The user's standing directive is "one plugin at a time", and the binding skill-token-economy memory (Initiative Sequencing, line 123) already records that next-plugin migration is ON HOLD until delivery-team Wave 3 closes. BACKLOG-104 (Wave 3) is authored but not shipped — opening BACKLOG-105 now would create two in-flight plugin backlogs and contradict both the user directive and the memorialized ruling. The five binding rulings, the Phase 1/2 routing pattern, the stages.yml manifest pattern, and the agent-prompt-as-reference pattern all transfer cleanly to mtg-commander when authored later; nothing is lost by waiting.

Per `feedback_route_through_po.md`, the in-flight delivery-team plan is the prompt to the team — closing it before opening a new one is the disciplined call. Per `feedback_team_autonomy.md`, the PO decides this without escalation: defer.

## Revisit-trigger

delivery-team Wave 3 SHIPPED (BACKLOG-104 marked DONE; Wave 3 entry in `.delivery/memory/topics/skill-token-economy.md` flipped from PLANNED to SHIPPED with run tag). At that point the delivery-team initiative is complete (5/5 milestones) and BACKLOG-105 should be authored fresh — scope is mtg-commander Wave 0 = telemetry hook + line-budget CI gate adapted for mtg-commander, mirroring delivery-team Wave 0 (run-2026-05-03-tk0e).

## References

- `.delivery/memory/topics/skill-token-economy.md` (line 123 — initiative sequencing on hold)
- `.delivery/memory/initiative-retros/skill-token-economy-meta-retro-2026-05-09.md`
- `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md` (the predecessor that must close first)
- `.delivery/backlog/BACKLOG-100-skill-token-economy-delivery-team.md` (the Wave 0 template BACKLOG-105 will mirror)
- User feedback: `feedback_route_through_po.md`, `feedback_team_autonomy.md`

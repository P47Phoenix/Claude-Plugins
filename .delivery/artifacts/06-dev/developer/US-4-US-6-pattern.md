# US-4 + US-6: Architecture Board Pattern Documentation

**Story IDs:** US-4 (configurable Architecture Board pattern doc), US-6 (MAR iteration-2 cross-persona routing, absorbs BACKLOG-002)
**Developer:** Gimli
**Date:** 2026-04-08

## Change

Inserted a new section "Architecture Board Review (Configurable)" into `delivery-team/skills/delivery-flow/references/team-patterns.md` immediately AFTER the existing "## Pattern 3: Multi-Perspective Review Board" section and BEFORE "## Pattern 4: Decision Ownership Routing". Existing Pattern 3 content is untouched.

## Location

- File: `delivery-team/skills/delivery-flow/references/team-patterns.md`
- New section starts at line **420** (`## Architecture Board Review (Configurable)`)
- New section ends immediately before line 478 `## Pattern 4: Decision Ownership Routing`
- Inserted line range: 420 through 477 (approx. 58 lines including blank lines and separators)

## Before / After

- Top-level `## ` section count BEFORE: 9
- Top-level `## ` section count AFTER: 10 (+1)
- File length BEFORE: 908 lines
- File length AFTER: 960 lines (+52)

## Section Contents (checklist)

1. Purpose paragraph — when to use, how it differs from fixed Review Board. DONE
2. Trigger conditions — `architecture_board.enabled: true` + Stage 4 Architect. DONE
3. Protocol — 8 numbered steps (config read, persona load, parallel dispatch, signal collection, judge invoke, verdict write, convergence check, feedback loop). DONE
4. MAR iteration-2 cross-persona routing — absorbs BACKLOG-002, 2-persona and N-persona rules. DONE
5. Output artifacts — `<persona-id>-review.md` + `judge-verdict.md`. DONE
6. Deadlock handling — links to Pattern 5 Debate DEADLOCK protocol. DONE
7. Context isolation rule — no cross-contamination between reviewers; judge receives paths only. DONE

## Notes

- Pattern 3 (fixed Multi-Perspective Review Board) is preserved verbatim — the new section augments rather than replaces.
- No code changes required for this story pair; subsequent stories will wire the orchestrator to read `architecture_board` config.

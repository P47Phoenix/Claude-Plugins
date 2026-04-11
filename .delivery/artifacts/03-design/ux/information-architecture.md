# Information Architecture: Adversarial Pipeline UX

**Stage:** 03-Design | **Role:** UX Designer (Galadriel) | **Plugin:** mtg-commander
*Through the mirror I have seen how mortal builders labor -- each craft checked by a second eye that owes the first no allegiance.*

## 1. Pipeline Progress Flow
Each step is a primary/challenger pair. Progress is linear, never nested.
```
Pipeline started -- 8 steps across 4 domains.
  [1/4] Deck Builder ............. constructing 100-card list
  [1C]  Deck Challenger .......... pending
  [2/4] Rules Judge .............. pending
  [2C]  Rules Challenger ......... pending
  [3/4] Optimizer ................ pending
  [3C]  Optimization Challenger .. pending
  [4/4] Price Evaluator .......... pending
  [4C]  Price Challenger ......... pending
```
**Happy path:**

```
[2/4] Rules Judge -- spawning sub-agent...
[2/4] Rules Judge -- PASS (7/7 checks green)
[2C]  Rules Challenger -- spawning independent reviewer...
[2C]  Rules Challenger -- PASS (confirmed, no challenges)
```
**Challenge + correction:**
```
[2/4] Rules Judge -- PASS (7/7 checks green)
[2C]  Rules Challenger -- CHALLENGE (2 findings)
        1. Sylvan Library -- color identity violation (G not in Orzhov)
        2. Mana Crypt -- banned in Commander as of Sep 2024
      Returning to Rules Judge for correction (loop 1/2)...
[2/4] Rules Judge -- corrections applied (swapped 2 cards)
[2C]  Rules Challenger -- re-reviewing...
[2C]  Rules Challenger -- PASS (corrections valid)
```
**Verbosity:** Primary shows one completion line. Challenger shows verdict + numbered findings only on CHALLENGE. Corrections one line per swap. No internal reasoning. "spawning independent reviewer" distinguishes challengers from primaries.

## 2. Escalation Message Design
When `max_card_price` is set and unsubstitutable cards exceed it, the pipeline blocks with a grouped prompt.
```
------------------------------------------------------------
  PRICE GOAL EXCEEDED -- User Decision Required
------------------------------------------------------------
These cards exceed your $1.00/card goal. No substitution
preserves both synergy and legality:

| Card             | Price  | Role           | Why no substitute                    |
|------------------|--------|----------------|--------------------------------------|
| Phyrexian Altar  | $8.50  | Combo piece    | Only sac outlet at this CMC in color |
| Bolas's Citadel  | $4.20  | Card advantage | Unique top-deck engine, no analog    |

Options:
  (a) Accept exception for these cards (logged in final output)
  (b) Raise per-card goal to $___
  (c) Force budget swap (synergy may drop -- each card noted)
Your choice (a/b/c):
------------------------------------------------------------
```
Table groups exceptions for scanning. Options are lettered (not numbered) to avoid collision with step numbers. Approved exceptions log in final output.

## 3. Config File UX
Config status: one line after intake confirmation, before pipeline banner.

| Scenario | Message |
|----------|---------|
| No file | `Config: Using defaults (2 loops/step, no price goal). Create .mtg-commander.yml to customize.` |
| Loaded | `Config: .mtg-commander.yml loaded -- 2 loops/step, $1.00 card goal, escalate on exhaustion` |
| Invalid keys | `Config: .mtg-commander.yml has invalid keys [max_loops]. Defaults used for those.` |
| Parse failure | `Config: .mtg-commander.yml could not be parsed (line 4: invalid YAML). Using all defaults.` |

**Rule:** Always one to two lines. Never block pipeline for config. Show what was applied, not just what failed.

## 4. Sub-Agent Dispatch Visibility
Every spawn is surfaced. No silent background agents.
```
[3/4] Optimizer -- spawning sub-agent...
[3/4] Optimizer -- COMPLETE (synergy: 3.4, structure: valid)
[3C]  Optimization Challenger -- spawning independent reviewer...
[3C]  Optimization Challenger -- CHALLENGE (1 finding)
        1. Burnished Hart -- isolated (2 interactions, minimum 3)
      Returning to Optimizer for correction (loop 1/2)...
```
No per-step time estimates -- banner shows overall ("2-4 minutes"). "spawning..." is the activity indicator.

## 5. Loop Exhaustion UX
Three modes via `escalation.on_loop_exhaustion`:

**`warn` (default)** -- advance with inline caveat:
```
[2C]  Rules Challenger -- loops exhausted (2/2). Advancing with warnings.
      Unresolved: Sylvan Library color identity -- verify manually.
```
**`block`** -- pipeline pauses, user decides:
```
------------------------------------------------------------
  CHALLENGER LOOP EXHAUSTED -- User Decision Required
------------------------------------------------------------
[2C] Rules Challenger could not confirm after 2 loops.
Unresolved findings:
  1. Sylvan Library -- color identity may violate commander constraint
Options:
  (a) Accept current deck and continue (unresolved items logged)
  (b) Abort pipeline
Your choice (a/b):
------------------------------------------------------------
```
**`best-effort`** -- advance silently, caveats appear only in final output:
```
[2C]  Rules Challenger -- best-effort (2 loops). See final output for caveats.
```

## 6. Open Questions for Architect
1. **Challenger context scope** -- Should challengers receive ONLY the primary's output artifact, or also original intake parameters? Intake params help catch drift but leak context.
2. **Cross-domain pipelining** -- Could [1C] and [2/4] overlap, or must the pipeline be strictly sequential? Architect should decide.
3. **Escalation stacking** -- If price goal escalation and loop exhaustion block both trigger in one step, which prompt first? Recommend loop exhaustion first -- resolving it may resolve the price issue.
4. **Config versioning** -- `.mtg-commander.yml` lacks a version field. Add one for forward compat, mirroring `.delivery/config.yml`?

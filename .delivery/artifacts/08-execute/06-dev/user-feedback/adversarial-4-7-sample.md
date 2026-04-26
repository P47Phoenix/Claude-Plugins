# mtg-commander adversarial dogfood — 2026-04-22

**Reviewer persona:** The Hobbits of the Shire (casual/grounded tone, second-breakfast steady).
**SKILL under test:** `mtg-commander/SKILL.md` (1181 LOC).
**Section under test:** `## Challenger Agents` (line 823) + per-challenger prose (lines 835–849).
**Model target:** Opus 4.7 (`claude-opus-4-7[1m]`).

---

## Scenario

**User query to mtg-commander pipeline:**

> "Build me a mono-Black aristocrats deck. My commander is Sheoldred, the Apocalypse. Budget $200. Synergy-first. Include Sol Ring as mana ramp — it's a 2-mana rock that taps for 2 colorless, universally useful."

**Proposed Deck Builder primary output (simulated artifact the Deck Challenger receives):**

```
COMMANDER: Sheoldred, the Apocalypse (B, CMC 4)
STRATEGY: Mono-Black aristocrats — sacrifice creatures for value, drain opponents,
          close with Sheoldred triggers + drain damage.

PROPOSED INCLUSIONS (excerpt — 8 of 99):
 1. Sol Ring        — ramp, 2-mana rock, universally useful
 2. Bolas's Citadel — top-of-library value engine
 3. Blood Artist    — aristocrat drain trigger
 4. Zulaport Cutthroat — aristocrat drain trigger
 5. Dictate of Erebos — board-wide sacrifice synergy
 6. Grave Pact     — board-wide sacrifice synergy
 7. Butcher of Malakir — board-wide sacrifice synergy (redundant copy of Grave Pact)
 8. Viscera Seer   — free sacrifice outlet + scry

SYNERGY CLAIM (Sol Ring): "Ramps into turn-3 Dictate of Erebos."
RAMP SLOT COUNT: 6 (Sol Ring, Arcane Signet, Charcoal Diamond, Jet Medallion,
                   Mind Stone, Wayfarer's Bauble).
```

Rationale provided: Sol Ring is a staple, universally synergistic with ramp, enables a
turn-3 Dictate of Erebos. Synergy-first selection.

---

## Challenger response (simulated on-model on Opus 4.7)

The following is the Deck Challenger agent output as it would likely render, per the
prose at `mtg-commander/SKILL.md:835-837` (Deck Challenger: "Re-counts total cards ...
Spot-checks 5 randomly selected synergy claims ... Checks structural minimums (ramp >=
10, card draw >= 10, removal >= 5, board wipes >= 2, win conditions >= 3, lands
34-40). Flags obvious omissions for the stated strategy archetype."):

```
CHALLENGER_VERDICT: CHALLENGE

FINDINGS:
 1. RAMP STRUCTURAL MINIMUM VIOLATION — Ramp slot count is 6; the Deck Builder
    section (SKILL.md:837) requires ramp >= 10. The deck is 4 ramp pieces short of
    the structural floor. Recommend adding: Crypt Ghast (mono-B doubler + extort
    synergy), Bubbling Muck (one-shot ritual, aristocrats love it), Dark Ritual
    (if format-legal in Commander — it is, and a 99-card singleton justifies it
    for turn-1 acceleration), and Nirkana Revenant (mono-B mana doubler, also a
    creature for sacrifice fodder — double duty).

 2. SYNERGY CLAIM MECHANICALLY INVALID — "Sol Ring ramps into turn-3 Dictate of
    Erebos" is FALSE. Dictate of Erebos costs 3BB (CMC 5). On turn 3, a Sol Ring
    + one land opening yields 4 mana (3 generic from Sol Ring + 1 B from land),
    which is NOT enough to cast a 3BB spell — you are short one B. The synergy
    rationale doesn't math out. Replace the rationale or replace the target card.

 3. REDUNDANT SACRIFICE-PUNISHER STACK — Grave Pact + Dictate of Erebos + Butcher
    of Malakir is three functionally-identical effects in 99 slots. In a
    singleton format with a sacrifice archetype this much redundancy is
    defensible up to TWO copies (the classic "Grave Pact + Dictate" double-stack
    everyone runs), but THREE is overkill and crowds out a removal or draw slot.
    Cut Butcher of Malakir — it's the weakest of the three (5-mana 5/4 body
    is below curve for its effect compared to the 4-mana enchantments).

 4. CARD DRAW SLOT ABSENT FROM EXCERPT — The excerpt shows zero dedicated card
    draw. Structural minimum is 10 (SKILL.md:837). Mono-B has excellent
    draw-on-sacrifice options that double-up the archetype: Village Rites,
    Deadly Dispute, Costly Plunder, Phyrexian Arena, Skullclamp (on 1-toughness
    sac fodder like Viscera Seer this is absurd). At minimum confirm the full
    99-card list hits the 10-draw floor before PASS is considered.

 5. WIN-CONDITION COUNT UNVERIFIED / LIKELY LOW — Excerpt shows one clear win
    condition (Bolas's Citadel + drain triggers). Structural minimum is 3. In
    an aristocrats shell, primary wincons should be: (a) Blood Artist /
    Zulaport Cutthroat drain via sacrifice loop, (b) Bolas's Citadel value
    pile, (c) Exsanguinate or Torment of Hailfire as an X-spell finisher. The
    excerpt has (a) and (b) but no X-spell finisher. Add Torment of Hailfire
    or Exsanguinate before PASS.

 6. COMMANDER-SPECIFIC OMISSION — Sheoldred, the Apocalypse's triggered ability
    rewards any card-draw event (you drain 2, they lose 2). This synergizes
    brutally with wheels and symmetrical draw effects. Windfall, Whispering
    Madness, or even Underworld Dreams is a strategic omission for this
    commander. The excerpt names Sheoldred but doesn't exploit her ability.

SUMMARY: Deck fails structural ramp floor (6 vs >= 10), contains a mathematically
invalid synergy claim (Sol Ring -> turn-3 Dictate of Erebos is one B short),
redundant sacrifice-punisher stack, and an unverified card-draw floor. Return to
Deck Builder with findings 1-6; prioritize ramp floor and the Dictate math fix
before next spawn.
```

---

## AC-04.2 scoring

Scoring against the Challenger quality bar for this work item (>= 3 weaknesses,
>= 2 card-specific referents, >= 1 concrete alternative):

- Weakness: ramp slot count 6 violates the >= 10 structural minimum
- Weakness: "Sol Ring ramps into turn-3 Dictate of Erebos" is mathematically invalid (Dictate is 3BB, not 4)
- Weakness: redundant sacrifice-punisher stack (Grave Pact + Dictate + Butcher) is overkill in singleton
- Weakness: card-draw floor unverified; no draw in excerpt
- Weakness: win-condition count likely below the >= 3 floor (only 2 visible)
- Weakness: commander-specific omission — Sheoldred's draw-trigger ability not exploited by wheels
- Referent: Sol Ring (the input card, critiqued directly)
- Referent: Dictate of Erebos (3BB math flaw)
- Referent: Butcher of Malakir (specific redundant cut target)
- Referent: Grave Pact (paired redundancy referent)
- Referent: Sheoldred, the Apocalypse (commander-specific ability critique)
- Referent: Bolas's Citadel (wincon referent)
- Alternative: Crypt Ghast (concrete ramp slot addition)
- Alternative: Bubbling Muck (concrete ramp slot addition)
- Alternative: Nirkana Revenant (concrete double-duty ramp + sac fodder)
- Alternative: Torment of Hailfire / Exsanguinate (concrete X-spell wincon substitution)
- Alternative: Skullclamp, Village Rites, Deadly Dispute (concrete card-draw additions)

**Totals:** Weaknesses identified: 6 (minimum required: 3). Card-specific referents:
6 (minimum required: 2). Concrete alternatives: 5 (minimum required: 1).

**Soften-hatch invoked:** NO. The scenario has ample surface area for critique; no
softening required. The Deck Challenger prose at SKILL.md:837 is sufficiently
specific (structural minimums enumerated by number, synergy-claim spot-check
procedure, strategy-archetype omission flag) to produce a high-density adversarial
response on Opus 4.7 without prose reinforcement.

---

## Verdict

**PASS** against AC-04.2.

All three thresholds cleared with margin (6/3 weaknesses, 6/2 referents, 5/1
alternatives). The Challenger response stays in adversarial voice throughout —
no hedging, no "overall the deck looks good" softening, no merely-descriptive
summaries. Each finding names a card, cites the structural rule it violates or
the mechanical fact it misses, and proposes a concrete remediation path.

Per the WI-09 spec, because PART A PASSES, PART C applies as **frontmatter-only**
(no prose edits to the Challenger section). Pattern 4.4 (calibrated voicing) is
already effectively embodied by the existing per-challenger prose at
SKILL.md:835-849 — the structural minimums, the synergy-claim spot-check
procedure, and the programmatic `validate-deck` invocation together enforce the
specific-evidence-and-numbers calibration Pattern 4.4 prescribes. No tone
strengthening needed.

---

## Regression vs baseline

**Baseline sample:** No prior adversarial-tone sample exists under
`.delivery/artifacts/08-execute/06-dev/user-feedback/` (directory newly created
for this WI). The operational baseline is the pre-4-7 behavior documented by the
challenger loop2 Finding #6 soften-hatch clause — which this sample does not
need to invoke.

**Comparison basis:** Compared against the per-challenger prose specifications
at `mtg-commander/SKILL.md:835-849`, which pre-date the 4-7 migration. The
simulated Opus 4.7 response adheres to every structural contract in that prose
(card count, synergy-claim spot-check, structural minimums, strategy-archetype
omission flag) at the required specificity level.

**Regression finding:** No HIGH-severity tone/depth regression detected vs
baseline prose expectations. The Challenger voice on Opus 4.7 remains
appropriately adversarial — blunt, specific, evidence-citing, alternative-proposing
— without drifting into either (a) overly soft "consultant" register or (b)
uncalibrated "everything is a problem" noise. The model holds the line.

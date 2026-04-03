# Strategy Archetype Patterns

Reference document for the Deck Builder agent. Defines strategy archetypes with structural guidance, synergy patterns, and commander suggestions. The Deck Builder uses this to shape card selection around the user's chosen strategy.

---

## How to Use This Reference

1. Identify the user's chosen strategy from intake question 3.
2. Load the matching archetype section below.
3. Use the **typical category distribution** to guide slot allocation (these are guidelines -- structural minimums from `structural-minimums.md` always take priority).
4. Use **key synergy patterns** to find cards that interact mechanically (not just thematically).
5. Use **win conditions** to ensure the deck has a clear path to victory.

---

## 1. Aggro / Combat Damage

**Description**: Wins through creature combat. Deploys efficient threats early and turns them sideways. Favors low mana curves, haste enablers, and combat tricks.

**Key Mechanics**: Haste, double strike, extra combats, trample, pump effects, anthem effects.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Creatures (combat-oriented) | 30-35 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes | 2-3 (asymmetric preferred) |
| Win Conditions | Built into creature base |
| Lands | 34-36 |

**Win Conditions**: Lethal combat damage through evasion, extra combats, or overwhelming board presence.

**Key Synergy Patterns**:
- Anthem effects + token producers = amplified board
- Haste enablers + high-power creatures = immediate pressure
- Extra combat effects + attack triggers = multiplicative value
- Equipment + evasion = reliable commander damage

**Commander Suggestions**: Najeela, the Blade-Blossom; Isshin, Two Heavens as One; Jetmir, Nexus of Revels; Aurelia, the Warleader.

---

## 2. Voltron

**Description**: Wins by making one creature (usually the commander) large enough to kill via commander damage (21) or regular damage. Stacks auras, equipment, and pump effects on a single threat.

**Key Mechanics**: Equipment, auras, hexproof, indestructible, double strike, protection, commander damage.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Equipment/Auras | 15-20 |
| Ramp | 12-14 |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes | 2-3 |
| Protection spells | 5-8 |
| Lands | 35-37 |

**Win Conditions**: 21 commander damage, or one-shot kills with double strike + high power.

**Key Synergy Patterns**:
- Equipment + equipment-matters creatures = value beyond the voltron target
- Protection spells + commander = sustained aggression
- Double strike + power buffs = lethal math
- Tutors for key equipment (Stoneforge Mystic, Open the Armory)

**Commander Suggestions**: Uril, the Miststalker; Syr Gwyn, Hero of Ashvale; Rograkh, Son of Rohgahh; Light-Paws, Emperor's Voice.

---

## 3. Tokens / Go-Wide

**Description**: Wins by creating many creature tokens and leveraging their collective power through anthems, sacrifice outlets, or overwhelming numbers.

**Key Mechanics**: Token creation, populate, convoke, anthem effects, sacrifice, going wide.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Token producers | 15-20 |
| Anthems/pump | 5-8 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-6 |
| Board Wipes | 2-3 (one-sided preferred) |
| Sacrifice outlets | 3-5 |
| Lands | 35-37 |

**Win Conditions**: Anthem-pumped token army, Craterhoof Behemoth-style finishers, aristocrats drain with sacrifice.

**Key Synergy Patterns**:
- Token producers + anthem effects = lethal board
- Token producers + sacrifice outlets = resource conversion
- Doubling effects (Doubling Season, Anointed Procession) + any token producer = exponential output
- Convoke spells + wide board = mana efficiency

**Commander Suggestions**: Rhys the Redeemed; Chatterfang, Squirrel General; Adeline, Resplendent Cathar; Mondrak, Glory Dominus.

---

## 4. Combo

**Description**: Wins by assembling a specific combination of 2-4 cards that produces an infinite loop or game-ending effect. The rest of the deck tutors for combo pieces, draws cards, and protects the combo.

**Key Mechanics**: Infinite loops, tutors, instant-speed interaction, redundancy, protection.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Combo pieces | 6-10 (2-3 combos with redundant pieces) |
| Tutors | 5-8 |
| Ramp | 12-15 |
| Card Draw | 12-15 |
| Removal/Interaction | 8-10 |
| Board Wipes | 2-3 |
| Protection | 4-6 |
| Lands | 34-36 |

**Win Conditions**: Infinite damage, infinite mill, infinite tokens, or lock opponents out entirely.

**Key Synergy Patterns**:
- Tutor + combo piece = assembly speed
- Protection + combo turn = safe win attempt
- Redundant combo pieces = resilience (e.g., multiple cards that fill the same combo slot)
- Card draw + low curve = find pieces fast

**Common Combos** (for reference, not exhaustive):
- Thoracle combo: Thassa's Oracle + Demonic Consultation / Tainted Pact
- Sanguine Bond + Exquisite Blood (infinite life drain)
- Kiki-Jiki + Zealous Conscripts (infinite hasty tokens)
- Dramatic Reversal + Isochron Scepter + mana rocks (infinite mana)

**Commander Suggestions**: Kinnan, Bonder Prodigy; Yuriko, the Tiger's Shadow; Mizzix of the Izmagnus; Thrasios (note: partner -- rejected in v1).

---

## 5. Mill

**Description**: Wins by emptying opponents' libraries rather than reducing life totals. Uses mill effects (put cards from library into graveyard) and library exile.

**Key Mechanics**: Mill, self-mill (for synergy), library manipulation, graveyard hate (to prevent opponents benefiting from milled cards).

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Mill sources | 15-20 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes | 2-3 |
| Graveyard hate | 3-5 |
| Win Conditions | Mill-based (Bruvac, Maddening Cacophony, Traumatize) |
| Lands | 35-37 |

**Win Conditions**: Mill all opponents' libraries, Fraying Sanity + large mill effect, Bruvac doubling.

**Key Synergy Patterns**:
- Mill doublers (Bruvac) + any mill source = exponential mill
- Persistent mill (Mesmeric Orb, Altar of the Brood) + normal gameplay = passive mill
- Mass mill spells + copy effects = table-wide mill
- Graveyard hate + opponent mill = deny reanimation value from milled cards

**Commander Suggestions**: Bruvac the Grandiloquent; Phenax, God of Deception; Zellix, Sanity Flayer; The Mimeoplasm (also reanimator).

---

## 6. Graveyard Recursion (Reanimator / Aristocrats / Dredge)

**Description**: Uses the graveyard as a second hand. Fills the graveyard with powerful creatures or value pieces, then returns them to the battlefield cheaply. Aristocrats sub-type drains opponents through repeated sacrifice-and-return loops.

**Key Mechanics**: Reanimate, self-mill, sacrifice outlets, death triggers, dredge, encore, unearth.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Reanimation targets | 8-12 |
| Reanimation spells | 6-10 |
| Self-mill / enablers | 5-8 |
| Sacrifice outlets | 5-8 (aristocrats variant) |
| Death trigger payoffs | 5-8 (aristocrats variant) |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-6 |
| Board Wipes | 2-3 |
| Lands | 35-37 |

**Win Conditions**: Reanimating game-ending threats (Razaketh, Vilis), aristocrats drain (Blood Artist loops), value grinding through recursion.

**Key Synergy Patterns**:
- Self-mill + reanimation = cheat mana costs
- Sacrifice outlet + death trigger + recursion = repeatable loops
- ETB effects + reanimation = repeated ETB value
- Dredge cards + draw effects = controlled self-mill

**Commander Suggestions**: K'rrik, Son of Yawgmoth; Meren of Clan Nel Toth; Muldrotha, the Gravetide; Chainer, Nightmare Adept.

---

## 7. Life Drain / Lifegain

**Description**: Wins by gaining life and/or draining opponents' life totals through incremental or explosive effects. Often combines lifegain triggers with payoff cards that convert life changes into damage or other advantages.

**Key Mechanics**: Lifelink, extort, drain effects, lifegain triggers, life-as-resource.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Lifegain sources | 12-15 |
| Lifegain payoffs | 8-12 |
| Drain effects | 5-8 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes | 2-3 |
| Lands | 35-37 |

**Win Conditions**: Aetherflux Reservoir (50 life = 50 damage), Sanguine Bond + lifegain, Felidar Sovereign (50+ life = win), Vito + mass lifegain.

**Key Synergy Patterns**:
- Lifegain trigger + lifegain payoff (e.g., Soul Warden + Ajani's Pridemate)
- Drain effects + token production = scaled drain
- Life-as-resource cards (Necropotence, Bolas's Citadel) + high life total = card advantage
- Extort + low-cost spells = incremental drain across all opponents

**Commander Suggestions**: Karlov of the Ghost Council; Oloro, Ageless Ascetic; Willowdusk, Essence Seer; Lathiel, the Bounteous Dawn.

---

## 8. Stax / Control

**Description**: Wins by restricting what opponents can do -- taxing spells, limiting untaps, preventing draws, or breaking parity on symmetrical hate pieces. Plays the long game and wins after opponents are locked out.

**Key Mechanics**: Tax effects, stax pieces (permanents that restrict actions), counterspells, removal, resource denial.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Stax/Tax pieces | 12-16 |
| Counterspells / interaction | 8-10 |
| Ramp | 12-15 (critical -- must break parity on own stax) |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes | 3-5 |
| Win Conditions | 3-5 (compact, low-resource wins) |
| Lands | 35-37 |

**Win Conditions**: Lock opponents out entirely, then win with compact finishers (Approach of the Second Sun, lab-man effects, commander damage through empty boards).

**Key Synergy Patterns**:
- Stax pieces + mana-positive ramp = breaking parity (opponents suffer, you don't)
- Tax effects + low-cost spells = you still function, opponents can't
- Board wipes + resilient threats = clear the way for your win condition
- Asymmetric stax (affects opponents more than you)

**Commander Suggestions**: Grand Arbiter Augustin IV; Derevi, Empyrial Tactician; Urza, Lord High Artificer; Lavinia, Azorius Renegade.

---

## 9. Spellslinger

**Description**: Wins by casting a high volume of instants and sorceries, leveraging spell-matters triggers and copy effects to generate overwhelming value or storm into a win.

**Key Mechanics**: Storm, magecraft, copy effects, spell cost reduction, flashback, spell recursion.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Instants/Sorceries | 30-35 |
| Spell payoffs | 8-12 |
| Spell cost reducers | 4-6 |
| Ramp | 10-12 |
| Card Draw | 12-15 |
| Removal (as instants/sorceries) | 6-8 |
| Board Wipes | 2-3 |
| Creatures (spell-matters) | 8-12 |
| Lands | 34-36 |

**Win Conditions**: Storm count + Grapeshot/Tendrils, Aetherflux Reservoir, copied extra turns, massive X spells.

**Key Synergy Patterns**:
- Cost reducers + cantrips = chain spells for storm count
- Magecraft/prowess triggers + spell volume = growing threats
- Copy effects + powerful spells = multiplied impact
- Flashback/recursion + spell payoffs = reuse fuel

**Commander Suggestions**: Veyran, Voice of Duality; Kalamax, the Stormsire; Mizzix of the Izmagnus; Hinata, Dawn-Crowned.

---

## 10. Tribal

**Description**: Builds around a specific creature type, leveraging tribal synergies (lords, type-matters effects) to create a cohesive creature base where each member amplifies the others.

**Key Mechanics**: Creature type lords, tribal payoffs, changelings (count as all types), tribal instants/sorceries.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| On-type creatures | 25-30 |
| Lords/anthem effects | 5-8 |
| Tribal payoffs (non-creature) | 4-6 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-6 |
| Board Wipes | 2-3 (one-sided or tribal-preserving) |
| Lands | 35-37 |

**Win Conditions**: Overwhelming board presence, tribal finishers (Coat of Arms, Triumph of the Hordes), tribal combos.

**Key Synergy Patterns**:
- Lords + creature base = collective power scaling
- Tribal payoffs + high creature count = value engines
- Changelings + narrow tribal cards = fill gaps in small tribes
- Tribal lands (Cavern of Souls, Unclaimed Territory) + multicolor tribe = fixing

**Important**: Sharing a creature type alone is NOT synergy per the taxonomy. Tribal synergy counts when cards mechanically reference the type (e.g., a lord that gives +1/+1 to all Elves interacts with each Elf). Two Elves that happen to be Elves without referencing the type do not count.

**Commander Suggestions**: Edgar Markov (Vampires); Ur-Dragon (Dragons); Krenko, Mob Boss (Goblins); Lathril, Blade of the Elves (Elves).

---

## 11. +1/+1 Counters / Proliferate

**Description**: Builds around placing and multiplying +1/+1 counters, using proliferate and counter-doubling effects to grow threats exponentially.

**Key Mechanics**: +1/+1 counters, proliferate, counter doublers, modular, evolve, adapt.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Counter sources | 12-16 |
| Counter payoffs | 8-10 |
| Proliferate effects | 5-8 |
| Ramp | 10-12 |
| Card Draw | 10-12 |
| Removal | 5-6 |
| Board Wipes | 2-3 |
| Lands | 35-37 |

**Win Conditions**: Massive creatures via counters, Walking Ballista with infinite counters, Simic Ascendancy (20+ counters), Triumph of the Hordes.

**Key Synergy Patterns**:
- Counter placers + proliferate = exponential growth
- Counter doublers (Doubling Season, Hardened Scales) + any counter source = multiplication
- +1/+1 counter creatures + removal via counters (Triskelion, Walking Ballista)
- Planeswalkers + proliferate = accelerated ultimates (superfriends crossover)

**Commander Suggestions**: Atraxa, Praetors' Voice; Ezuri, Claw of Progress; Marchesa, the Black Rose; Vorinclex, Monstrous Raider.

---

## 12. Superfriends (Planeswalkers)

**Description**: Builds around planeswalkers as the primary value engines, using proliferate, protection, and board control to keep planeswalkers alive long enough to reach ultimates.

**Key Mechanics**: Planeswalkers, proliferate, board wipes (creature-only), pillowfort, loyalty counters.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Planeswalkers | 12-18 |
| Proliferate effects | 5-8 |
| Protection / Pillowfort | 5-8 |
| Ramp | 12-15 |
| Card Draw | 10-12 |
| Removal | 5-7 |
| Board Wipes (creature-only) | 3-5 |
| Lands | 36-38 |

**Win Conditions**: Planeswalker ultimates, Doubling Season + planeswalker = immediate ultimate, token armies from planeswalker abilities.

**Key Synergy Patterns**:
- Proliferate + planeswalkers = accelerated loyalty
- Doubling Season + planeswalker ETB = instant ultimate
- Board wipes (creatures only) + planeswalkers = asymmetric advantage
- Pillowfort + planeswalkers = protect investments

**Commander Suggestions**: Atraxa, Praetors' Voice; Carth the Lion; Sisay, Weatherlight Captain.

---

## 13. Group Hug

**Description**: "Helps" all players with shared resources (extra draws, extra mana, extra lands) while secretly building toward a win condition that leverages the inflated resources more effectively than opponents.

**Key Mechanics**: Symmetrical draw, mana doubling, political cards, hidden win conditions.

**Typical Category Distribution**:
| Category | Slots |
|----------|-------|
| Group hug effects | 10-14 |
| Hidden win conditions | 4-6 |
| Ramp | 10-12 |
| Card Draw | 10-12 (partially overlaps with group hug) |
| Removal | 5-7 |
| Board Wipes | 2-3 |
| Pillowfort / Protection | 4-6 |
| Lands | 36-38 |

**Win Conditions**: Approach of the Second Sun, Thassa's Oracle + draw entire deck, Insurrection (steal pumped-up boards), Molten Psyche + mass draw.

**Key Synergy Patterns**:
- Forced draw + draw punishment (Underworld Dreams, Nekusar) = damage from "gifts"
- Mana doubling + X spells = exploit shared mana better
- Political cards + pillowfort = survive until win condition
- Group draw + Notion Thief / Narset = break symmetry

**Commander Suggestions**: Kynaios and Tiro of Meletis; Kenrith, the Returned King; Phelddagrif; Nekusar, the Mindrazer (group slug variant).

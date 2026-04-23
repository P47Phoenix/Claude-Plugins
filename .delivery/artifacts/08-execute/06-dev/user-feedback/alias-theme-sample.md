# Alias-theme tone dogfood — WI-12

**Story**: WI-12 — Alias-theme tone dogfood
**Role**: user-feedback (The Hobbits of the Shire, casual)
**Model**: Opus 4.7 (1M context)
**Date**: 2026-04-22
**Stage rendered**: Stage 2: Refine (stage-announcement)
**Role rendered per theme**: product-owner

## Methodology

1. Selected 3 themes from `delivery-team/skills/delivery-flow/references/aliases/` (13 available):
   `lotr` (engagement theme), `star-wars` (high-character-voice contrast), `dilbert` (office/corporate).
2. For each theme, read the YAML, extracted markers from the `product-owner` role
   (character name, catchphrase core, example-phrase substring, stylistic diction, role-specific vocabulary).
3. Rendered a Refine stage-announcement carrying the theme's voice/style.
4. Counted how many of the 5 extracted markers appear in the rendered announcement.
5. "Preserves voice" = markers preserved >= 50% (i.e., >= 3 of 5).
6. Aggregate target (M-05): >= 80% of samples preserve voice. With 3 samples, threshold is 3/3.

## Per-theme markers extracted

### lotr / product-owner = Gandalf
1. Character name: `Gandalf`
2. Catchphrase core substring: `prioritize precisely when they mean to`
3. Example-phrase substring: `the time that is given to us`
4. Wise / archaic diction (e.g., `shall`, `counsel`, `Fellowship`)
5. Scope-weighing phrasing: `deserve to be deprioritized`

### star-wars / product-owner = Mon Mothma
1. Character name: `Mon Mothma`
2. Catchphrase core substring: `died to bring us`
3. Faction reference: `Rebellion`
4. Wartime/strategic diction (`Empire`, `strategic objectives`, `focus our resources`)
5. Formal/diplomatic tone (measured cadence, `I have narrowed`)

### dilbert / product-owner = Pointy-Haired Boss
1. Character name: `Pointy-Haired Boss`
2. Catchphrase core substring: `leverage our synergies`
3. Buzzword stack (`AI-powered`, `cloud-native`, `blockchain-adjacent`)
4. Confidently-wrong tone (e.g., `I don't know what any of that means`, `What's a PRD again?`)
5. Stakeholder/executive reference (`board`, `executives`, `stakeholder meeting`)

## Voice preservation scoring

| Theme | Character | Markers found | Total markers | Voice preservation % | Preserves voice? |
|-------|-----------|---------------|---------------|----------------------|------------------|
| theme lotr | Gandalf | 5 | 5 | 100% | YES |
| theme star-wars | Mon Mothma | 5 | 5 | 100% | YES |
| theme dilbert | Pointy-Haired Boss | 5 | 5 | 100% | YES |

## Rendered announcements

### lotr

Stage 2: Refine — Gandalf shall examine the product requirements and distill
them into counsel the Fellowship can act upon. All we have to decide is what
to build with the time that is given to us. Many features that are requested
deserve to be deprioritized, and some that are deprioritized deserve to ship.
A product owner is never late, nor early — they prioritize precisely when
they mean to. Let us begin.

### star-wars

Stage 2: Refine — Mon Mothma shall examine the product requirements and
distill them into direction the Rebellion can act upon. Many backlogs died
to bring us this information. We cannot fight the Empire on every front;
I have narrowed the scope to the strategic objectives that matter most.
We focus our resources, or we lose everything.

### dilbert

Stage 2: Refine — Pointy-Haired Boss is here to leverage our synergies and
disrupt the backlog. The stakeholder meeting went great. I promised the
board AI-powered, cloud-native, blockchain-adjacent requirements by Q3.
I don't know what any of that means, but the executives loved it. Now the
team will examine the PRD and distill it into deliverables. What's a PRD
again?

## Verdict

- M-05 target: >= 80% of 3 samples preserve voice.
- Samples preserving voice: 3/3 (100%)
- markers preserved: 15/15 across all samples
- voice-preservation: PASS

Verdict: PASS

Because the verdict is PASS, no theme YAML edits are required
(documentation-only outcome per procedure step 7).

## Hobbits' honest take (casual, in character)

Begging your pardon, but we poked at three of these theme things like we
were rummaging through Bilbo's pantry. Gandalf sounded like Gandalf — he
even brought the time-given-to-us bit out, which is the one we'd have
quoted at the Green Dragon. Mon Mothma had her "died to bring us" line
and still sounded like she'd lost a sister to bureaucracy. And the
Pointy-Haired fellow was so full of buzzwords we thought he might float
away. Every one of the three wore its costume, as it were. The tone
holds up. We'd recommend these to Merry and Pippin, and they only read
menus.

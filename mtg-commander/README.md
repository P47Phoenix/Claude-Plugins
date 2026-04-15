# MTG Commander

Build synergy-dense, format-legal, budget-compliant 100-card Commander decks via a multi-agent pipeline.

> See also: [ARCHITECTURE.md](./ARCHITECTURE.md) — internal design and Mermaid diagrams for contributors.

> *"It's a dangerous business, going out your door — especially with a stack of 99 cards and a commander. Let me pack your bags properly."* — Bilbo

---

## Quick start

Just ask. The skill triggers on natural phrasing:

- *"Build me a commander deck"*
- *"Build an EDH deck around Karador"*
- *"100-card deck, Golgari sacrifice, $75 budget"*

You'll be asked for up to **7 intake parameters** (any you skip get sensible defaults or inferred from your commander). Once confirmed, the pipeline runs and you get back:

- A categorized 100-card decklist (Commander / Ramp / Card Draw / Removal / Board Wipes / Win Conditions / Synergy Pieces / Lands)
- Format-legality verdict (color identity, banned list, singleton, 100-card count)
- Synergy density score + mana curve
- Dual-vendor pricing (TCGPlayer + Card Kingdom) with a category breakdown
- A plain-text export list, plus purchase links

---

## What it does

Four sub-agents run in sequence, each followed by an independent **Challenger** that re-verifies the primary's work in a clean context:

| Step | Primary | Challenger checks |
|------|---------|-------------------|
| 1 | **Deck Builder** — synergy-first card selection | Challenges weak picks, missed synergies |
| 2 | **Rules Judge** — format legality (color identity, banned, singleton) | Re-runs `validate-deck` programmatically |
| 3 | **Optimization Reviewer** — interaction density, structural minimums, curve | Challenges synergy tags, reviewer blind spots |
| 4 | **Price Evaluator** — budget, per-card cap, dual-vendor pricing | Re-fetches Card Kingdom, flags vendor divergence |

When anything fails, violations route back to the Deck Builder for correction. Sub-agents run independently — no context bleed between agents. Every step is adversarial by design.

---

## Intake parameters

| # | Parameter | Example |
|---|-----------|---------|
| 1 | Color identity | `BG` (Golgari), `WUB` (Esper), `WUBRG` (5-color) |
| 2 | Commander name | `Karador, Ghost Chieftain` |
| 3 | Strategy archetype | `aristocrats`, `voltron`, `tokens`, `lifegain`, `spellslinger` |
| 4 | Power level (1-10) | `6` (focused casual), `8` (high-power), `10` (cEDH) |
| 5 | Meta alignment | `casual`, `mid-power`, `high-power` |
| 6 | Total budget (USD) | `$75`, `$150`, `no budget` |
| 7 | Card restrictions | `no infinite combos`, `must include Sol Ring`, `no card over $10` |

Skip anything you don't care about — the skill infers from your commander or applies defaults.

---

## Pricing & budget

Pricing is **dual-vendor** to catch single-source drift:

- **TCGPlayer** prices via the Scryfall API
- **Card Kingdom** prices via the Archidekt API
- The budget check uses the **higher of the two totals** (conservative default) — a tiebreaker that protects you from buying on CK and finding out prices diverged 50%
- **Per-card soft goal** (optional, via config): tell the skill "stay around $1/card" and the Price Evaluator searches for cheaper functional swaps before asking you to raise the cap
- **CK divergence check**: Price Challenger flags any card where TCG/CK prices diverge by more than 30%, and escalates if the total deck diverges by more than 20%

See `mtg-commander/references/price-evaluator-guide.md` for the full pricing logic.

---

## Config file

Create `.mtg-commander.yml` in your repo (or wherever you invoke the skill) to customize pipeline behavior. Minimal example:

```yaml
version: 1
loops:
  deck_builder: 3        # give the builder 3 correction attempts before escalating
price_rules:
  max_card_price: 1.00   # soft $1/card goal (hard 15%-of-budget cap still applies)
  escalation: true       # ask before keeping over-goal cards
```

All keys are optional. Missing keys get sensible defaults, invalid keys warn without failing the pipeline.

- A fully commented example lives at `.mtg-commander.yml.example` (see US-3)
- Full schema, defaults, and validation rules are in `mtg-commander/SKILL.md` (section: Configuration)

---

## Example invocation

**You say:**
> Build me a $75 Karador aristocrats deck, $1/card goal, no infinite combos.

**What happens:**

1. The skill validates `Karador, Ghost Chieftain` on Scryfall — legal commander, color identity `WBG`, partner-less
2. Intake confirmed: Karador / WBG / aristocrats / power 6 / casual / $75 / no infinite combos, $1/card goal
3. **Deck Builder** drafts 100 cards — `Phyrexian Altar`, `Viscera Seer`, `Ashnod's Altar`, ramp, draw, removal, lands
4. **Rules Judge** runs `validate-deck` — every card's color identity confirmed inside `WBG`, no banned cards, singleton clean
5. **Optimization Reviewer** scores synergy density, flags any card with fewer than 3 interactions
6. **Price Evaluator** fetches TCG + CK prices, applies the $1/card soft goal, runs the CK divergence check
7. If anything fails, Challengers trigger a correction loop; if it passes, you get the categorized list with purchase links

---

## Troubleshooting

**Card Kingdom prices diverge from TCGPlayer.**
Expected and handled. The Price Challenger flags any card where CK/TCG differ by >30%, and escalates the whole deck if the totals diverge by >20%. Pick which vendor to optimize for when prompted — or set `price_rules.budget_source` in config to pin one.

**The pipeline loops exhaust without passing.**
Check `.mtg-commander.yml` — `escalation.on_loop_exhaustion` controls what happens: `warn` (ship best-effort with a warning), `block` (halt and ask you), or `best-effort` (silent ship). Raising `loops.*` to `3` gives the builder more attempts.

**Your commander got rejected.**
Either a typo (watch for `Did you mean: ...?` suggestions), the card is on the Commander banned list, or you named a partner/background without its pair. Re-name it or ask the skill for commander suggestions filtered by color + strategy.

**No prices returned for some cards.**
Cards with no USD price on Scryfall are excluded from budget totals and listed in `UNAVAILABLE_PRICES`. Uncommon for popular cards; more likely for recent un-sets or promos. Verify at your vendor before buying.

---

## Reference links

- **Full skill instructions:** [`SKILL.md`](SKILL.md) — the complete pipeline, agent prompts, adversarial loop protocol, and output format
- **Detailed guides** in [`references/`](references/):
  - [`intake-questions.md`](references/intake-questions.md) — full intake question set
  - [`price-evaluator-guide.md`](references/price-evaluator-guide.md) — pricing, budget, CK divergence
  - [`rules-judge-guide.md`](references/rules-judge-guide.md) — format legality checks
  - [`optimizer-guide.md`](references/optimizer-guide.md) — synergy density scoring
  - [`synergy-taxonomy.md`](references/synergy-taxonomy.md) — interaction tags
  - [`archetype-patterns.md`](references/archetype-patterns.md) — strategy templates
  - [`structural-minimums.md`](references/structural-minimums.md) — ramp/draw/removal floors
  - [`banned-list.md`](references/banned-list.md) — current Commander banned list
  - [`commander-rules.md`](references/commander-rules.md) — format rules reference
- **Repo root:** [`../README.md`](../README.md)

---

## Recently fixed

- **DEFECT-001** (closed) — Color identity determinism. Rules Judge + Rules Challenger now use the programmatic `card_lookup.py validate-deck` command. No more LLM-inferred legality calls; every card's color identity is checked against the commander's via the Scryfall API.
- **DEFECT-002** (closed) — Card Kingdom pricing divergence. The Price Challenger fetches CK prices independently via the Archidekt API, flags per-card divergence >30%, and escalates total divergence >20%. Single-vendor budget blind spots are handled.

---

> *"Go now, and build with a light heart. The road goes ever on — but your deck, at least, will be legal and synergy-dense when you reach the table."* — Bilbo

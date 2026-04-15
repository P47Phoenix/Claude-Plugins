# `.mtg-commander.yml` — Config Walkthrough

> *"A short cut to the deck builder's tools — no need to unpack the whole pantry."* — Bilbo

## 1. What this file does

`.mtg-commander.yml` lets you customize the MTG Commander pipeline's **loop counts**, **price rules**, and **escalation behavior** without editing the plugin itself. Drop one file in your working directory, tune a few knobs, and the skill picks it up on its next run.

## 2. Where it goes

Place the file in your **working directory** — the same directory you invoke the MTG skill from (typically your project root). It is **not** a plugin file; do not put it inside the `mtg-commander/` plugin directory. The skill reads it at pipeline start (right after intake confirmation).

A ready-to-copy example ships at `mtg-commander/.mtg-commander.yml.example`. Copy it to your working directory, rename it to `.mtg-commander.yml`, and edit.

## 3. Defaults (when the file is absent)

If no `.mtg-commander.yml` exists, the pipeline applies all defaults silently — except for a single-line note at the top of the run:

```
No .mtg-commander.yml found — using defaults. Create one to customize loop caps, price goals, and escalation.
```

No error. No prompt. The pipeline proceeds.

## 4. Loop counts (`loops`)

Each of the four primary agents (Deck Builder, Rules Judge, Optimization Reviewer, Price Evaluator) runs under an adversarial **Primary → Challenger → correction** loop. The loop cap controls how many correction cycles are allowed before escalation kicks in.

| Value | Behavior |
|-------|----------|
| `1`   | Faster runs, less scrutiny (quality risk) |
| `2`   | **Balanced default** |
| `3+`  | Maximum scrutiny for high-stakes builds; longer runtime |

Each key is independent — bump just `price_evaluator` if cost fidelity matters most; bump just `rules_judge` when assembling a weird-legality commander.

## 5. Price rules (`price_rules`)

### `max_card_price` (soft goal)

This is **your** preferred per-card ceiling in USD — a soft goal the Price Evaluator tries to honor by finding functional substitutes. It is **not** the hard cap.

- **Hard cap** — the per-card cap from intake (default 15% of total budget). Always enforced; non-negotiable.
- **Soft goal** — `max_card_price` from this file. When the goal cannot be met for a given card, the pipeline escalates per the rules below.

Set to `null` (or omit) to skip the soft goal entirely.

### `escalation`

- `true` — unsubstitutable over-goal cards trigger a **blocking** user prompt (accept / raise goal / force-swap).
- `false` — silent auto-substitution; if no substitute exists, the card is kept and tagged `[OVER_GOAL: $price/$goal]`. No prompt.

Turn off if you don't want interactive blocking (e.g., scripted runs).

### `budget_source`

Which vendor's totals anchor the budget check.

| Value | Meaning |
|-------|---------|
| `higher`      | **Default.** Uses `max(TCG_total, CK_total)` — conservative; protects against vendor drift. |
| `tcgplayer`   | Use TCGPlayer prices only — pick this if you buy from TCG. |
| `cardkingdom` | Use Card Kingdom prices only — pick this if you buy from CK. |

This key also controls which per-card price feeds the soft goal and hard cap checks.

## 6. Escalation modes (`escalation.on_loop_exhaustion`)

What happens when an adversarial loop runs out of attempts without a PASS verdict:

| Mode          | Behavior |
|---------------|----------|
| `warn`        | Ship the best-effort deck with warnings appended. **Non-blocking** (default). |
| `block`       | Halt the pipeline, prompt the user for a decision. **Most adversarial.** |
| `best-effort` | Output the best attempt silently; unresolved findings go to the pipeline log. No user prompt. |

## 7. Example tuning scenarios

**Strict budget brewing** — tight $1/card, user-gated:

```yaml
price_rules:
  max_card_price: 1.00
  escalation: true
escalation:
  on_loop_exhaustion: block
```

**Relaxed casual** — defaults everywhere, warnings only:

```yaml
# (empty file or just)
version: 1
```

**Maximum quality** — bumped loops, full escalation:

```yaml
loops:
  deck_builder: 3
  rules_judge: 3
  optimizer: 3
  price_evaluator: 3
price_rules:
  escalation: true
escalation:
  on_loop_exhaustion: block
```

## 8. Validation

There is **no separate validator tool**. The pipeline itself handles validation at start:

- Invalid YAML → warning + fall back to all defaults.
- Unknown keys → warning + ignored.
- Out-of-range values → warning + per-key default applied.

Graceful degradation — config mistakes **never** block a run.

## 9. See also

- `mtg-commander/README.md` — plugin overview, quick start, troubleshooting
- `mtg-commander/references/price-evaluator-guide.md` — full pricing logic, divergence checks, substitution rules
- `mtg-commander/SKILL.md` — complete schema reference (Configuration section)

> *"Adjust a line, save the file, run again. A small hobbit-sized effort for a large change in outcome."* — Bilbo

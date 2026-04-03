# Defect-002: Add Card Kingdom Pricing via Archidekt API

## Summary

Added Card Kingdom pricing to the MTG Commander plugin using the Archidekt API (`https://archidekt.com/api/cards/v2/`). The Price Evaluator now shows dual-vendor pricing (TCGPlayer + Card Kingdom) and uses the higher total for budget checks (conservative approach).

## Changes Made

### `mtg-commander/scripts/card_lookup.py`
- Added `ARCHIDEKT_BASE_URL` constant
- Added `_archidekt_limiter` (100ms delay between calls)
- Added `_archidekt_request()` helper for Archidekt API GET requests
- Added `cmd_ck_price(name)` -- single card CK + TCG price lookup via Archidekt
  - Searches across printings, returns cheapest CK price
  - Filters zero prices (Archidekt uses 0.0 for "unavailable")
  - Card name lives at `oracleCard.name` (not top-level `name`)
  - Returns CK purchase URL via `ckNormalId` field
- Added `cmd_ck_batch_price(names)` -- batch CK pricing with per-card delay
  - Returns both CK and TCG totals
  - Tracks unavailable prices per vendor
- Added CLI subcommands: `ck-price`, `ck-batch-price`

### `mtg-commander/references/price-evaluator-guide.md`
- Added step 1.1b: CK batch pricing via Archidekt after TCGPlayer fetch
- Budget check now uses `max(total_tcg, total_ck)` (conservative)
- Output format shows `TOTAL_COST: TCGPlayer: $X | Card Kingdom: $Y`
- Replaced `PRICING_DISCLAIMER` with `PRICING_NOTE` (no longer disclaiming CK)
- Updated evaluation sequence: 15 steps (was 14), CK fetch at step 5

### `mtg-commander/SKILL.md`
- Added `archidekt.com` to Required Setup WebFetch domains
- Added `ck-price` and `ck-batch-price` to Card Lookup Utility list
- Price Evaluator template: added Step 1b for CK pricing
- Updated Purchase Summary to show dual-vendor totals
- Replaced `PRICING_DISCLAIMER` with `PRICING_NOTE`

### `mtg-commander/references/api-reference.md`
- Renamed title to "API Reference (Scryfall + Archidekt)"
- Added full Archidekt API section: endpoint, params, response schema, rate limiting
- Added `ck-price` and `ck-batch-price` to CLI commands table
- Renamed "Scryfall Terms of Use" to "API Terms of Use" with Archidekt subsection

## Archidekt API Findings

- **No auth required**, free API
- **Card name** is nested at `oracleCard.name`, not top-level
- **Zero prices** (0.0) mean "unavailable", not free -- must filter them out
- **No visible rate limit headers** -- 100ms courtesy delay applied
- **`ckNormalId`** maps to Card Kingdom purchase URLs: `https://www.cardkingdom.com/catalog/item/{id}`
- **Price field names**: `prices.ck` (normal), `prices.ckfoil` (foil), `prices.tcg` (TCGPlayer)

## Test Results

```
$ python card_lookup.py ck-price --name "Sol Ring"
{
  "name": "Sol Ring",
  "price_ck": "2.29",
  "price_tcg": "1.51",
  "ck_url": "https://www.cardkingdom.com/catalog/item/324075",
  "found": true
}

$ python card_lookup.py ck-batch-price --names "Sol Ring" "Dark Ritual" "Phyrexian Arena"
{
  "total_ck": 13.77,
  "total_tcg": 9.72,
  "total_priced": 3,
  "total_cards": 3
}
```

CK prices consistently higher than TCG (expected -- CK is premium vendor). Budget check using the higher total is the right call.

# Dev Notes: US-02 -- Scryfall API Client Script (Card Finder)

**Story**: US-02 | **SP**: 8 | **Sprint**: 1
**FR Coverage**: FR-06 (all ACs), FR-05.1, FR-05.8
**File**: `mtg-commander/scripts/card_lookup.py` (481 lines)
**Developer**: Gimli

---

> *"I axed through every acceptance criterion like so many orc shields. And my code!"*

---

## Implementation Summary

Stdlib-only Python script (`urllib.request`, `json`, `time`, `sys`, `argparse`) providing 6 CLI commands for Scryfall API access. All output is JSON to stdout for machine parsing by pipeline agents.

### Commands Implemented

| Command | Endpoint | Purpose |
|---------|----------|---------|
| `validate --name` | `/cards/named?exact=` + fuzzy fallback | Exact name lookup; returns `did_you_mean` on fuzzy hit |
| `search --query` | `/cards/search?q=` | Full-text search with pagination (up to 175 results) |
| `batch --names` | `POST /cards/collection` | Batch lookup, auto-splits at 75-card chunks |
| `price --name` | `/cards/named?exact=` + `/cards/search?unique=prints` | Cheapest USD price across all printings |
| `batch-price --names` | `POST /cards/collection` | Batch pricing with total calculation |
| `random-commander --colors --strategy` | `/cards/search?q=is:commander` | Commander suggestions by color/strategy |

### Architecture Decisions

1. **75ms rate limiter** (AC 2.9): Uses `time.monotonic()` for precision. Class-based singleton ensures all requests share the same timer.
2. **Exponential backoff on 429** (AC 2.10): 1s, 2s, 4s waits, max 3 retries. 5xx retries once after 2s. Network errors retry once.
3. **Batch splitting at 75** (AC 2.5): Scryfall limit is 75 identifiers per `/cards/collection` request. Script chunks automatically.
4. **Price fallback chain** (AC 2.6): Default printing USD -> default printing USD foil -> search all printings cheapest USD -> cheapest foil -> "unavailable".
5. **Double-faced card handling** (AC 2.13): Oracle text combined from all faces with ` // ` separator. Mana cost, power/toughness taken from front face. Color identity uses the top-level field (Scryfall already combines).
6. **User-Agent header**: All requests include `MtgCommanderDeckBuilder/1.0 (Claude-Plugins)` per Scryfall API policy.

### Normalized Card Data Model (AC 2.11)

All commands that return card data use `_normalize_card()` to produce a consistent schema:

```
name, mana_cost, cmc, type_line, oracle_text, colors, color_identity,
keywords, power, toughness, legalities, prices (usd + usd_foil),
set_name, rarity, scryfall_uri, card_faces, found
```

---

## Verification

| AC | Status | Method | Notes |
|----|--------|--------|-------|
| 2.1 | PASS | `ls mtg-commander/scripts/card_lookup.py` | File exists at correct path |
| 2.2 | PASS | Code review | Only imports: urllib, json, time, sys, argparse |
| 2.3 | PASS | `validate --name "Sol Ring"` returns `found: true`; `validate --name "Sol Ringg"` returns `did_you_mean: "Sol Ring"` | Exact + fuzzy fallback working |
| 2.4 | PASS | `search --query` works | Returns paginated results |
| 2.5 | PASS | `batch --names "Sol Ring" "Dark Ritual" "Totally Fake Card"` | Sol Ring + Dark Ritual in `data`, fake card in `not_found` |
| 2.6 | PASS | `price --name "Sol Ring"` returns `$1.43` (cheapest printing) | Fallback chain exercised: default had null USD, searched all printings |
| 2.7 | PASS | Code review | `batch-price` delegates to `cmd_batch` then prices each card |
| 2.8 | PASS | Code review | `random-commander` builds Scryfall query with `is:commander` |
| 2.9 | PASS | Code review | `RateLimiter` class, 75ms minimum between calls |
| 2.10 | PASS | Code review | 429 exponential backoff (1s/2s/4s), 5xx retry once, timeout retry once |
| 2.11 | PASS | `validate --name "Sol Ring"` output | All 15 fields present in normalized model |
| 2.12 | PASS | Code review | 404 from search returns `{"results": [], "query": ...}` |
| 2.13 | PASS | `validate --name "Delver of Secrets"` | Returns combined oracle text from both faces, `card_faces` preserved |
| 2.14 | PASS | All commands | `json.dump(result, sys.stdout, indent=2)` |

### Smoke Test Results

```
$ python card_lookup.py validate --name "Sol Ring"
{"found": true, "name": "Sol Ring", "legalities": {"commander": "legal"}, ...}

$ python card_lookup.py price --name "Sol Ring"
{"name": "Sol Ring", "price_usd": "1.43", "price_source": "usd (cheapest printing)", "set_name": "Aetherdrift Commander", "found": true}

$ python card_lookup.py validate --name "Sol Ringg"
{"found": false, "query": "Sol Ringg", "did_you_mean": "Sol Ring"}

$ python card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Totally Fake Card"
{"data": [<Sol Ring>, <Dark Ritual>], "not_found": [{"name": "Totally Fake Card"}], "total_found": 2, "total_not_found": 1}

$ python card_lookup.py validate --name "Delver of Secrets"
{"found": true, "name": "Delver of Secrets // Insectile Aberration", "oracle_text": "<combined from both faces>", "card_faces": [...]}
```

All 5 smoke tests pass. No errors, no rate limiting issues, no timeouts.

---

## Risks & Notes

1. **Scryfall default printing varies**: The default printing returned by `/cards/named` may have null USD prices (promotional/commander precon printings). The price fallback chain handles this by searching all printings, but adds an extra API call.
2. **Fuzzy match sensitivity**: Scryfall's fuzzy endpoint has limits -- "Sol Rign" (2 chars off) returns 404 while "Sol Ringg" (1 char added) resolves. The `did_you_mean` feature depends on Scryfall's own matching capability.
3. **No caching**: Each invocation makes fresh API calls. For pipeline runs with 100+ card lookups, batch commands should be preferred over individual validate calls to minimize API requests.

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/06-dev/developer/us-02-notes.md
SUMMARY: card_lookup.py fully implemented: 6 CLI commands, stdlib-only, 75ms rate limiting, 429 retry, batch splitting at 75, price fallback chain. All 14 ACs pass. 5 smoke tests verified.
```

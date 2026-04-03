# API Reference (Scryfall + Archidekt)

Reference document for the Price Evaluator agent and the `card_lookup.py` script. Documents the Scryfall and Archidekt API endpoints, query syntax, rate limiting, response schemas, and error handling used by this plugin.

---

## Base URL

```
https://api.scryfall.com
```

All requests use HTTPS. Scryfall's API is free, open, and requires no authentication.

---

## Endpoints Used

### 1. `/cards/named` -- Single Card Lookup

**Purpose**: Validate a card name or fetch a single card's data.

**Method**: GET

**Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `exact` | string | Exact card name match (case-insensitive) |
| `fuzzy` | string | Fuzzy card name match (for typo correction) |

**Usage in pipeline**:
- Commander validation at intake (exact match first, fuzzy fallback)
- Individual card validation during deck construction

**Example requests**:
```
GET /cards/named?exact=Sol+Ring
GET /cards/named?fuzzy=Sol+Rign
```

**Response**: Single card object (see Card Data Model below).

**Error**: 404 if no match found (exact) or no close match (fuzzy).

---

### 2. `/cards/search` -- Card Search

**Purpose**: Find cards matching complex criteria using Scryfall search syntax.

**Method**: GET

**Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Scryfall search query (see Query Syntax below) |
| `unique` | string | `cards` (default), `prints` (all printings), `art` (unique art) |
| `order` | string | Sort order: `name`, `usd`, `cmc`, `edhrec`, etc. |
| `dir` | string | Sort direction: `auto`, `asc`, `desc` |
| `page` | integer | Page number for paginated results (default 1) |

**Usage in pipeline**:
- Deck Builder: find cards matching strategy criteria
- Optimization Reviewer: find replacement suggestions for isolated cards
- Price Evaluator: find budget-friendly alternatives

**Example requests**:
```
GET /cards/search?q=oracle%3Asacrifice+type%3Acreature+id%3AB+legal%3Acommander
GET /cards/search?q=!%22Sol+Ring%22&unique=prints&order=usd&dir=asc
```

**Response**: Paginated list object with `data` array of card objects. `has_more` indicates additional pages. `next_page` provides URL for next page.

**Error**: 404 if zero results.

---

### 3. `/cards/collection` -- Batch Card Lookup

**Purpose**: Look up multiple cards in a single request. Preferred for validating or pricing complete decklists.

**Method**: POST

**Content-Type**: `application/json`

**Body**:
```json
{
  "identifiers": [
    {"name": "Sol Ring"},
    {"name": "Dark Ritual"},
    {"name": "Blood Artist"}
  ]
}
```

**Limits**: Maximum 75 identifiers per request. For a 100-card deck, split into 2 requests (cards 1-75, cards 76-100).

**Usage in pipeline**:
- Rules Judge: batch validate all 100 card names
- Price Evaluator: batch fetch prices for all 100 cards

**Response**:
```json
{
  "data": [ /* array of found card objects */ ],
  "not_found": [ /* array of identifiers that didn't match */ ]
}
```

**Error**: 400 if body is malformed. Individual not-found cards appear in `not_found`, not as errors.

---

## Query Syntax (Scryfall Search)

Scryfall uses a structured query language for the search endpoint. Key operators:

### Card Properties

| Operator | Description | Example |
|----------|-------------|---------|
| `name:` | Card name contains | `name:blood` |
| `!` | Exact card name | `!"Sol Ring"` |
| `oracle:` or `o:` | Oracle text contains | `o:sacrifice` |
| `type:` or `t:` | Type line contains | `t:creature` |
| `id:` | Color identity (within) | `id:BG` (cards legal in BG decks) |
| `c:` | Card color (exact) | `c:B` (black cards) |
| `cmc:` or `mv:` | Mana value | `mv<=3` |
| `pow:` | Power | `pow>=5` |
| `tou:` | Toughness | `tou>=4` |
| `keyword:` or `kw:` | Has keyword | `kw:flying` |

### Format Legality

| Operator | Description | Example |
|----------|-------------|---------|
| `legal:` or `f:` | Legal in format | `f:commander` |
| `banned:` | Banned in format | `banned:commander` |
| `is:commander` | Can be used as commander | `is:commander` |

### Price Filters

| Operator | Description | Example |
|----------|-------------|---------|
| `usd:` | USD price filter | `usd<=5` |
| `usd>=` | USD price minimum | `usd>=1` |

### Combinators

| Operator | Description | Example |
|----------|-------------|---------|
| (space) | AND | `t:creature o:sacrifice` |
| `or` | OR | `t:creature or t:artifact` |
| `-` | NOT | `-t:land` |
| `()` | Grouping | `(t:creature or t:artifact) id:B` |

### Useful Compound Queries

```
# Find sacrifice-matters creatures in black, Commander legal
o:sacrifice t:creature id:B f:commander

# Find cards that trigger on creature death, in black
o:"whenever a creature dies" id:B f:commander

# Find ramp artifacts under $2
t:artifact o:"add" mv<=2 usd<=2 f:commander

# Find all printings of a card, sorted by price
!"Sol Ring" unique:prints order:usd dir:asc

# Find commanders in specific colors
is:commander id:BG

# Find cards with lifelink in white/black
kw:lifelink id:WB f:commander
```

---

## Rate Limiting

| Rule | Value |
|------|-------|
| Minimum delay between requests | 75ms (Scryfall asks for 50-100ms; we use 75ms as safe middle) |
| Rate limit response code | 429 Too Many Requests |
| Backoff strategy | Exponential: 1s, 2s, 4s (max 3 retries) |
| Preferred for bulk operations | `/cards/collection` (batch) over individual `/cards/named` calls |

**Implementation**: The `card_lookup.py` script enforces rate limiting via a `RateLimiter` class that tracks the last request timestamp and sleeps if the minimum delay has not elapsed.

---

## Error Handling

| HTTP Code | Meaning | Script Behavior |
|-----------|---------|----------------|
| 200 | Success | Parse and return card data |
| 404 | Not found | Return `{"found": false, "query": "<original>"}` |
| 422 | Bad request (invalid query) | Return error with query echoed for debugging |
| 429 | Rate limited | Exponential backoff: 1s, 2s, 4s. Max 3 retries. Then return error. |
| 5xx | Server error | Retry once after 2s. Then return error with suggestion to check status.scryfall.com |
| Timeout (10s) | No response | Retry once after 2s. Then return error. |

---

## Card Data Model

The `card_lookup.py` script normalizes Scryfall responses into this structure:

```json
{
  "name": "Blood Artist",
  "mana_cost": "{1}{B}",
  "cmc": 2.0,
  "type_line": "Creature - Vampire",
  "oracle_text": "Whenever Blood Artist or another creature dies, target opponent loses 1 life and you gain 1 life.",
  "color_identity": ["B"],
  "colors": ["B"],
  "legalities": {
    "commander": "legal"
  },
  "price_usd": "1.49",
  "set_name": "Avacyn Restored",
  "scryfall_uri": "https://scryfall.com/card/avr/86/blood-artist",
  "card_faces": null,
  "keywords": [],
  "found": true
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Canonical card name. For DFCs: `"Front // Back"` |
| `mana_cost` | string | Mana cost in `{symbol}` notation. Empty string for lands. |
| `cmc` | float | Converted mana cost / mana value |
| `type_line` | string | Full type line (e.g., "Legendary Creature - Vampire") |
| `oracle_text` | string | Rules text. For DFCs: combined from all faces. |
| `color_identity` | array | Color identity symbols: W, U, B, R, G. Empty array for colorless. |
| `legalities` | object | Format legality map. Check `legalities.commander`. |
| `price_usd` | string or null | Cheapest USD price. Null if no price available. |
| `card_faces` | array or null | Non-null for double-faced cards. Each face has its own oracle_text. |
| `keywords` | array | Keyword abilities (check for "Partner" to detect partner commanders). |
| `found` | boolean | Whether the card was found in Scryfall. |

### Null Price Handling

When `price_usd` is null:
1. Check `prices.usd_foil` -- use if available.
2. Search for other printings (`!"Card Name"&unique=prints&order=usd`) and use the cheapest.
3. If all printings have null USD price, flag as `"price_unavailable": true` and exclude from budget calculations with a warning in the Price Evaluator verdict.

---

## Archidekt API (Card Kingdom Pricing)

### Base URL

```
https://archidekt.com/api/cards/v2/
```

Free, no authentication required. Used exclusively for Card Kingdom price data.

### Endpoint: Card Search with Prices

**Purpose**: Fetch Card Kingdom (and TCGPlayer) prices for a card across printings.

**Method**: GET

**Parameters**:

| Param | Type | Description |
|-------|------|-------------|
| `name` | string | Exact card name (URL-encoded) |
| `pageSize` | integer | Max results to return (use 5 for cheapest-across-printings) |

**Example request**:
```
GET /api/cards/v2/?name=Sol+Ring&pageSize=5
```

**Response structure** (per result):

| Field Path | Type | Description |
|------------|------|-------------|
| `oracleCard.name` | string | Canonical card name |
| `prices.ck` | float | Card Kingdom normal price (0.0 = unavailable) |
| `prices.ckfoil` | float | Card Kingdom foil price (0.0 = unavailable) |
| `prices.tcg` | float | TCGPlayer price (0.0 = unavailable) |
| `ckNormalId` | integer | Card Kingdom product ID for purchase links |

**Card Kingdom purchase URL**: `https://www.cardkingdom.com/catalog/item/{ckNormalId}`

**Rate limiting**: No rate limit headers visible. The script enforces a 100ms minimum delay between requests as a courtesy.

**Error handling**: Network errors and non-200 responses return `None` from the helper, which the command handles gracefully by returning `found: false`.

---

## CLI Commands (`card_lookup.py`)

Agents invoke the Card Finder via the Bash tool:

| Command | Usage | Description |
|---------|-------|-------------|
| `validate` | `python card_lookup.py validate --name "Sol Ring"` | Check if a card exists. Returns found status + full card data. Fuzzy fallback on exact miss. |
| `search` | `python card_lookup.py search --query "o:sacrifice t:creature id:B f:commander"` | Search for cards matching Scryfall query syntax. Returns array of matching cards. |
| `batch` | `python card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Blood Artist"` | Batch lookup via `/cards/collection`. Splits at 75 cards. Returns `data` + `not_found`. |
| `price` | `python card_lookup.py price --name "Sol Ring"` | Get cheapest USD printing price for a card. Handles null USD fallback. |
| `batch-price` | `python card_lookup.py batch-price --names "Sol Ring" "Dark Ritual"` | Batch pricing for decklists. Returns all cards with TCGPlayer prices. |
| `ck-price` | `python card_lookup.py ck-price --name "Sol Ring"` | Get Card Kingdom + TCGPlayer price for a card via Archidekt API. Returns cheapest CK price across printings with purchase link. |
| `ck-batch-price` | `python card_lookup.py ck-batch-price --names "Sol Ring" "Dark Ritual" "Phyrexian Arena"` | Batch Card Kingdom pricing. Returns both CK and TCG prices per card, with vendor totals. 100ms delay between calls. |
| `random-commander` | `python card_lookup.py random-commander --colors BG` | Find commander suggestions for given color identity. |

**All commands output JSON to stdout** for machine parsing by agents. Errors are returned as JSON with an `"error"` field.

---

## API Terms of Use

### Scryfall

- Scryfall is free for personal and open-source use.
- No API key required.
- Respect rate limits (50-100ms between requests).
- Card images and data are provided under Wizards of the Coast's fan content policy.
- The `prices.usd` field reflects **TCGPlayer market price**.
- Prices are estimates based on recent market data, not guaranteed live market prices.

### Archidekt

- Archidekt API is free, no authentication required.
- No documented rate limits -- the script enforces 100ms courtesy delay.
- The `prices.ck` field reflects **Card Kingdom price**.
- Used solely for Card Kingdom pricing; card data (names, rules text, legality) comes from Scryfall.

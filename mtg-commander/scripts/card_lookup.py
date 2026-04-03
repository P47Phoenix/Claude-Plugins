#!/usr/bin/env python3
"""Scryfall API client for MTG Commander deck builder agents.

stdlib only — no pip dependencies. Outputs JSON to stdout for machine parsing.

Usage:
    python card_lookup.py validate --name "Sol Ring"
    python card_lookup.py search --query "oracle:sacrifice type:creature id:B legal:commander"
    python card_lookup.py batch --names "Sol Ring" "Dark Ritual" "Cabal Coffers"
    python card_lookup.py price --name "Sol Ring"
    python card_lookup.py batch-price --names "Sol Ring" "Dark Ritual"
    python card_lookup.py random-commander --colors BG --strategy sacrifice
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://api.scryfall.com"
USER_AGENT = "MtgCommanderDeckBuilder/1.0 (Claude-Plugins)"


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

class RateLimiter:
    """Enforce minimum delay between Scryfall API requests (75 ms default)."""

    def __init__(self, min_delay_ms: int = 75):
        self.min_delay = min_delay_ms / 1000.0
        self.last_request_time: float = 0

    def wait(self) -> None:
        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.monotonic()


_rate_limiter = RateLimiter()


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------

def _request(url: str, *, method: str = "GET", data: bytes | None = None,
             timeout: int = 10, retries_left: int = 3) -> dict:
    """Issue an HTTP request with rate limiting, retries, and error handling."""

    _rate_limiter.wait()

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)

    except urllib.error.HTTPError as exc:
        status = exc.code

        # 404 — card not found (expected for validate)
        if status == 404:
            try:
                body = exc.read().decode("utf-8")
                return json.loads(body)
            except Exception:
                return {"object": "error", "status": 404, "details": "Not found"}

        # 422 — bad request / invalid query
        if status == 422:
            try:
                body = exc.read().decode("utf-8")
                return json.loads(body)
            except Exception:
                return {"object": "error", "status": 422, "details": "Bad request"}

        # 429 — rate limited, exponential backoff
        if status == 429 and retries_left > 0:
            wait_time = 2 ** (3 - retries_left)  # 1s, 2s, 4s
            time.sleep(wait_time)
            return _request(url, method=method, data=data, timeout=timeout,
                            retries_left=retries_left - 1)

        # 5xx — server error, retry once after 2s
        if 500 <= status < 600 and retries_left > 0:
            time.sleep(2)
            return _request(url, method=method, data=data, timeout=timeout,
                            retries_left=0)

        return {
            "object": "error",
            "status": status,
            "details": f"HTTP {status} error. Check status.scryfall.com if persistent.",
        }

    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Timeout or network error — retry once
        if retries_left > 0:
            time.sleep(2)
            return _request(url, method=method, data=data, timeout=timeout,
                            retries_left=0)
        return {
            "object": "error",
            "status": 0,
            "details": f"Network error: {exc}",
        }


# ---------------------------------------------------------------------------
# Card data normalisation
# ---------------------------------------------------------------------------

def _normalize_card(card: dict) -> dict:
    """Extract the fields agents care about from a Scryfall card object."""

    # Handle double-faced / split / adventure cards
    oracle_text = card.get("oracle_text", "")
    if not oracle_text and "card_faces" in card and card["card_faces"]:
        oracle_text = " // ".join(
            face.get("oracle_text", "") for face in card["card_faces"]
        )

    mana_cost = card.get("mana_cost", "")
    if not mana_cost and "card_faces" in card and card["card_faces"]:
        mana_cost = card["card_faces"][0].get("mana_cost", "")

    power = card.get("power")
    toughness = card.get("toughness")
    if power is None and "card_faces" in card and card["card_faces"]:
        power = card["card_faces"][0].get("power")
        toughness = card["card_faces"][0].get("toughness")

    prices = card.get("prices", {}) or {}

    return {
        "name": card.get("name", ""),
        "mana_cost": mana_cost,
        "cmc": card.get("cmc", 0.0),
        "type_line": card.get("type_line", ""),
        "oracle_text": oracle_text,
        "colors": card.get("colors", []),
        "color_identity": card.get("color_identity", []),
        "keywords": card.get("keywords", []),
        "power": power,
        "toughness": toughness,
        "legalities": card.get("legalities", {}),
        "prices": {
            "usd": prices.get("usd"),
            "usd_foil": prices.get("usd_foil"),
        },
        "set_name": card.get("set_name", ""),
        "rarity": card.get("rarity", ""),
        "scryfall_uri": card.get("scryfall_uri", ""),
        "card_faces": card.get("card_faces"),
        "found": True,
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_validate(name: str) -> dict:
    """Exact name lookup with fuzzy fallback on miss."""

    encoded = urllib.parse.quote(name, safe="")
    result = _request(f"{BASE_URL}/cards/named?exact={encoded}")

    # Exact match succeeded
    if result.get("object") == "card":
        card = _normalize_card(result)
        card["found"] = True
        return card

    # Exact miss — try fuzzy for a "did you mean?" suggestion
    fuzzy_result = _request(f"{BASE_URL}/cards/named?fuzzy={encoded}")
    if fuzzy_result.get("object") == "card":
        return {
            "found": False,
            "query": name,
            "did_you_mean": fuzzy_result.get("name", ""),
        }

    return {"found": False, "query": name}


def cmd_search(query: str) -> dict:
    """Full-text search via /cards/search."""

    encoded = urllib.parse.quote(query, safe="")
    result = _request(f"{BASE_URL}/cards/search?q={encoded}")

    if result.get("object") == "error":
        # Scryfall returns 404 for zero results
        if result.get("status") == 404:
            return {"results": [], "query": query}
        return {"results": [], "query": query, "error": result.get("details", "")}

    cards = [_normalize_card(c) for c in result.get("data", [])]

    # Handle pagination — collect up to 175 results (first page often enough)
    response = {"results": cards, "query": query, "total_cards": result.get("total_cards", len(cards))}

    next_page = result.get("next_page")
    if next_page and len(cards) < 175:
        page2 = _request(next_page)
        if page2.get("object") == "list":
            cards.extend(_normalize_card(c) for c in page2.get("data", []))
            response["results"] = cards

    return response


def cmd_batch(names: list[str]) -> dict:
    """Batch lookup via /cards/collection. Splits at 75-card chunks."""

    all_found: list[dict] = []
    all_not_found: list[dict] = []

    # Split into chunks of 75 (Scryfall limit)
    for i in range(0, len(names), 75):
        chunk = names[i:i + 75]
        identifiers = [{"name": n} for n in chunk]
        payload = json.dumps({"identifiers": identifiers}).encode("utf-8")

        result = _request(f"{BASE_URL}/cards/collection", method="POST", data=payload)

        if result.get("object") == "error":
            # If the whole batch failed, mark all as not found
            all_not_found.extend({"name": n} for n in chunk)
            continue

        for card in result.get("data", []):
            all_found.append(_normalize_card(card))

        all_not_found.extend(result.get("not_found", []))

    return {
        "data": all_found,
        "not_found": all_not_found,
        "total_found": len(all_found),
        "total_not_found": len(all_not_found),
    }


def cmd_price(name: str) -> dict:
    """Get cheapest USD price for a card across printings."""

    # First: exact lookup for the card (gets default printing price)
    encoded = urllib.parse.quote(name, safe="")
    result = _request(f"{BASE_URL}/cards/named?exact={encoded}")

    if result.get("object") != "card":
        return {"found": False, "query": name}

    card = _normalize_card(result)
    prices = result.get("prices", {}) or {}
    usd = prices.get("usd")
    usd_foil = prices.get("usd_foil")

    # Try the default printing first
    if usd is not None:
        return {
            "name": card["name"],
            "price_usd": usd,
            "price_source": "usd",
            "set_name": card["set_name"],
            "found": True,
        }

    # Fallback: try foil price on this printing
    if usd_foil is not None:
        return {
            "name": card["name"],
            "price_usd": usd_foil,
            "price_source": "usd_foil",
            "set_name": card["set_name"],
            "found": True,
        }

    # Fallback: search all printings and pick cheapest USD price
    search_query = urllib.parse.quote(f'!"{name}"', safe="")
    prints_result = _request(
        f"{BASE_URL}/cards/search?q={search_query}&unique=prints&order=usd&dir=asc"
    )

    if prints_result.get("object") == "list":
        cheapest_usd = None
        cheapest_foil = None

        for printing in prints_result.get("data", []):
            p = printing.get("prices", {}) or {}
            p_usd = p.get("usd")
            if p_usd is not None:
                price_val = float(p_usd)
                if cheapest_usd is None or price_val < cheapest_usd[0]:
                    cheapest_usd = (price_val, p_usd, printing.get("set_name", ""))
            p_foil = p.get("usd_foil")
            if p_foil is not None:
                foil_val = float(p_foil)
                if cheapest_foil is None or foil_val < cheapest_foil[0]:
                    cheapest_foil = (foil_val, p_foil, printing.get("set_name", ""))

        if cheapest_usd is not None:
            return {
                "name": card["name"],
                "price_usd": cheapest_usd[1],
                "price_source": "usd (cheapest printing)",
                "set_name": cheapest_usd[2],
                "found": True,
            }
        if cheapest_foil is not None:
            return {
                "name": card["name"],
                "price_usd": cheapest_foil[1],
                "price_source": "usd_foil (cheapest printing)",
                "set_name": cheapest_foil[2],
                "found": True,
            }

    return {
        "name": card["name"],
        "price_usd": None,
        "price_source": "unavailable",
        "set_name": card["set_name"],
        "found": True,
        "warning": "Price unavailable across all printings",
    }


def cmd_batch_price(names: list[str]) -> dict:
    """Batch pricing via /cards/collection with cheapest-price selection."""

    batch_result = cmd_batch(names)
    priced: list[dict] = []
    unavailable: list[str] = []

    for card in batch_result["data"]:
        usd = card["prices"].get("usd")
        usd_foil = card["prices"].get("usd_foil")

        if usd is not None:
            priced.append({
                "name": card["name"],
                "price_usd": usd,
                "price_source": "usd",
                "set_name": card["set_name"],
            })
        elif usd_foil is not None:
            priced.append({
                "name": card["name"],
                "price_usd": usd_foil,
                "price_source": "usd_foil",
                "set_name": card["set_name"],
            })
        else:
            priced.append({
                "name": card["name"],
                "price_usd": None,
                "price_source": "unavailable",
                "set_name": card["set_name"],
            })
            unavailable.append(card["name"])

    total = sum(float(c["price_usd"]) for c in priced if c["price_usd"] is not None)

    return {
        "cards": priced,
        "not_found": batch_result["not_found"],
        "total_usd": round(total, 2),
        "price_unavailable": unavailable,
        "total_priced": len(priced) - len(unavailable),
        "total_cards": len(priced),
    }


def cmd_random_commander(colors: str = "", strategy: str = "") -> dict:
    """Find commanders matching color identity and optional strategy."""

    parts = ["is:commander", "legal:commander"]

    if colors:
        parts.append(f"id:{colors}")

    if strategy:
        parts.append(f"oracle:{strategy}")

    query = " ".join(parts)
    encoded = urllib.parse.quote(query, safe="")
    result = _request(f"{BASE_URL}/cards/search?q={encoded}")

    if result.get("object") == "error":
        return {"results": [], "query": query}

    cards = [_normalize_card(c) for c in result.get("data", [])]
    return {
        "results": cards,
        "query": query,
        "total_cards": result.get("total_cards", len(cards)),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scryfall API client for MTG Commander deck builder agents.",
        prog="card_lookup.py",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    p_validate = subparsers.add_parser("validate", help="Exact card name lookup with fuzzy fallback")
    p_validate.add_argument("--name", required=True, help="Card name to validate")

    # search
    p_search = subparsers.add_parser("search", help="Full-text card search")
    p_search.add_argument("--query", required=True, help="Scryfall search query")

    # batch
    p_batch = subparsers.add_parser("batch", help="Batch card lookup (up to 75 per request)")
    p_batch.add_argument("--names", nargs="+", required=True, help="Card names to look up")

    # price
    p_price = subparsers.add_parser("price", help="Get cheapest USD price for a card")
    p_price.add_argument("--name", required=True, help="Card name to price")

    # batch-price
    p_bprice = subparsers.add_parser("batch-price", help="Batch pricing for multiple cards")
    p_bprice.add_argument("--names", nargs="+", required=True, help="Card names to price")

    # random-commander
    p_random = subparsers.add_parser("random-commander", help="Find commanders by criteria")
    p_random.add_argument("--colors", default="", help="Color identity filter (e.g. BG, WUB)")
    p_random.add_argument("--strategy", default="", help="Strategy/oracle text filter")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate":
        result = cmd_validate(args.name)
    elif args.command == "search":
        result = cmd_search(args.query)
    elif args.command == "batch":
        result = cmd_batch(args.names)
    elif args.command == "price":
        result = cmd_price(args.name)
    elif args.command == "batch-price":
        result = cmd_batch_price(args.names)
    elif args.command == "random-commander":
        result = cmd_random_commander(args.colors, args.strategy)
    else:
        parser.print_help()
        sys.exit(1)

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()

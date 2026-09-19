# Model ID Verification (US-2 / FR-9)

- Source URL: https://platform.claude.com/docs/en/about-claude/models/overview (served as /docs/en/models/overview after redirect)
- Fetch date: 2026-09-19 (live WebFetch, not cache)
- Verdict: ALL FOUR IDs CONFIRMED. No contradiction. Allowlist unchanged. No dual-allow.

## Per-ID confirmation

| ID | Live "Claude API ID" | Live "Claude API alias" | Retirement | Result |
|---|---|---|---|---|
| claude-fable-5-1 | `claude-fable-5-1` | `claude-fable-5-1` | Not sooner than September 1, 2027 | CONFIRMED |
| claude-opus-5 | `claude-opus-5` | `claude-opus-5` | Not sooner than July 24, 2027 | CONFIRMED |
| claude-sonnet-5 | `claude-sonnet-5` | `claude-sonnet-5` | Not sooner than June 30, 2027 | CONFIRMED |
| claude-haiku-4-5-20251001 | `claude-haiku-4-5-20251001` | `claude-haiku-4-5` | Not sooner than October 15, 2026 | CONFIRMED |

## Quoted lines (verbatim from page)

    | Claude API ID | `claude-fable-5-1` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5-20251001` |
    | Claude API alias | `claude-fable-5-1` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5` |
    | Retirement | Not sooner than September 1, 2027 | Not sooner than July 24, 2027 | Not sooner than June 30, 2027 | Not sooner than October 15, 2026 |

Footnotes quoted:

- "Claude API ID: Every Claude model ID is a pinned snapshot, including the dateless IDs used from the 4.6 generation on."
- "Claude API alias: For models before the 4.6 generation, the alias is a convenience pointer that resolves to the dated ID. Dateless IDs are their own pinned snapshot; the alias row repeats them."
- Intro: "start with Claude Opus 5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work".

## Aliases vs dated IDs

- Fable 5.1, Opus 5, Sonnet 5: dateless. ID == alias. Each is its own pinned snapshot.
- Haiku 4.5: pre-4.6 generation. Dated ID `claude-haiku-4-5-20251001` is the listed API ID. Alias `claude-haiku-4-5` resolves to it. Google Cloud form is `claude-haiku-4-5@20251001`.

## Dated Haiku form accepted by API?

Yes. Dated form is the page's own "Claude API ID" value for Haiku 4.5, so it is the canonical string. Repo pin needs no change. The Q6 open item (does page show dated snapshot?) is resolved: it does.

## Discrepancies

None against the PRD or allowlist.

- Haiku 4.5 retirement: not sooner than October 15, 2026, 26 days after fetch date. Matches QA F-6 rollover note. Not blocking. Rollover = one-line `ALLOW=` edit plus four Haiku sites.
- Legacy list on page names older Opus/Sonnet generations as still available. That is not a contradiction: the guard's allowlist covers only the current lineup by design.

## AC-22 run (2026-09-19)

Commands: `test -s` on this file, then loop over the four IDs with `/usr/bin/grep -q`.
Expected: `0`, then no output. Actual: `0`, no MISSING lines. PASS. Retired-ID scan of this file: no hits.

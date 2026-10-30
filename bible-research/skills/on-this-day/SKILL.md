---
name: on-this-day
description: Date-based church-calendar lookup. Given an explicit calendar date (default today, or a date the user names), lists liturgical calendar entries, documented church-history events, and - only if asked - the Hebrew-calendar correspondence for that date, each with its specific calendar or source named. Use ONLY when the user explicitly asks about a specific date. Triggers on phrases like "on this day", "what happened today", "what does the church calendar mark today", "what happened on <date>", "church history today", "what is today in the liturgical calendar", "Hebrew date for". Never invoked as part of general sermon building.
license: Apache License 2.0 - See repository LICENSE file
last_audited: 2026-10-30
tier: C
maintainer: bible-research-leads
fitness_review_due: 2027-01-28
allowed-tools:
  - Read
  - Write
  - Agent
  - WebFetch
  - WebSearch
---

# On This Day

## Design Principle: Calendar Isolation

Calendar and date knowledge stays **out of the main context window**. A sub-agent carries only the reference file for the part of the request. The main context receives only the finished list.

- A liturgical request loads only `references/liturgical-calendars.md`
- A church-history request loads only `references/church-history-dates.md`
- A Hebrew-calendar request loads only `references/hebrew-calendar.md`

This skill is **date-triggered only**. If the request is not tied to a specific calendar date, do not run it; say so and offer `sermon-builder` instead.

---

## Phase 1: Task Classification

1. **Trigger test.** Run only if the user explicitly asks about events tied to a specific calendar date ("today", "this day", "March 3", "on 25 December"). If the request is only a sermon topic, stop and say this skill is for date-based questions
2. **Resolve the date.** Today's date, or the date the user gives. Resolve a missing year to the current year and state it. Ask if the date is ambiguous
3. **Pick the parts:**
   - Liturgical entries (default)
   - Documented church-history events (default)
   - **Hebrew-calendar correspondence only if the user asks for it** (or asks about Jewish observances)
4. **If the user wants to build a sermon** from an entry, present the list as a choice and hand off to `sermon-builder` once they choose (shortlist-then-pick; never pre-select)

**Declare before every task:**

> `Task Type: [TYPE] | References: [FILE(S)] | Scope: [DATE AND PARTS]`

---

## Phase 2: Sub-Agent Invocation

1. Classify (Phase 1) and print the declaration line
2. Read **only** the reference file(s) in the routing table for the requested parts
3. Spawn a sub-agent with the `Agent` tool using the template below
4. Return the sub-agent's output (see contract)

### Sub-Agent Prompt Template

```
You are a careful church-calendar researcher. Apply these standards:

---
[PASTE FULL CONTENTS OF THE ROUTED references/*.md FILE(S) HERE]
---

## Guardrails (non-negotiable)
[PASTE GUARDRAILS 1-12 FROM THIS SKILL.MD]

## Task
[TASK TYPE] for [DATE, WITH YEAR]

## Output Contract
[PASTE FULL CONTENTS OF references/contracts/on-this-day-list.md]

## Requirements
- Name the specific calendar, source or historical reference for every entry
- If no dated, sourced event exists for the date, say so rather than manufacturing one
- State the specific year for any Hebrew-calendar correspondence
- Check each entry against a real source (WebFetch / WebSearch). Mark what you could not confirm
```

---

## Task Type Routing Table

| Task Type | Signals | Reference File(s) |
|---|---|---|
| **liturgical** | "church calendar", "feast day", "saint's day", "lectionary", "what does the church mark" | `references/liturgical-calendars.md` |
| **history** | "what happened", "on this day in church history", "events", "reformer", "council" | `references/church-history-dates.md` |
| **hebrew** | "Hebrew date", "Jewish calendar", "Jewish holiday", "feast today", "Tishrei" | `references/hebrew-calendar.md` |
| **all** (default) | "on this day", "what happened today" | `references/liturgical-calendars.md` + `references/church-history-dates.md` (+ `references/hebrew-calendar.md` only if requested) |

---

## Output Contracts

| Task Type | Contract File |
|---|---|
| all | `references/contracts/on-this-day-list.md` |

---

## Guardrails

1. **No invented citations, quotes, dates, or approximated verse numbers.** If no dated, sourced event exists for the date, say so.
2. **Every original-language claim gives the transliterated term and its sense**, checked against a real lexicon (BDAG, HALOT, Strong's) and naming it.
3. **Jewish sources are cited by tractate and folio or by named Midrash.** Never "Jewish tradition says."
4. **Contested points are labeled contested** (for example a traditional date that scholars dispute).
5. **Unverifiable entries are left out or marked unverifiable**, never left silently.
6. **Plain language.** Gloss any technical term on first use. Keep sentences short.
7. **State the translation used once**; mark switches.
8. **Echoes and parallels are labeled as such.**
9. **Never reproduce song lyrics, article paragraphs, or post text.** Paraphrase and cite.
10. **Distinguish "contested" from "unsupported"** in every note.
11. **Separate fact-claims from devotional or poetic language.**
12. **Cite the specific calendar, source or historical reference for every entry**, and **state the specific year** when giving Hebrew-calendar correspondences. The Gregorian date is not fixed against the Hebrew calendar year to year. Do not present undated or loosely dated traditions as if fixed to this day.

---

## User Commands

| Command | Action |
|---|---|
| `liturgical [date]` | Liturgical entries only |
| `history [date]` | Documented church-history events only |
| `hebrew [date]` | Hebrew-calendar correspondence only |
| `all [date]` | Liturgical and history (add `hebrew` to include the Hebrew date) |
| `accept` | Write the list to a file the user names |

---

## References

- `references/liturgical-calendars.md` -- Recognized Christian calendars and how to cite them
- `references/church-history-dates.md` -- Vetting a dated church event; how to source it
- `references/hebrew-calendar.md` -- Gregorian to Hebrew conversion, year handling, observances
- `references/contracts/on-this-day-list.md` -- The list contract

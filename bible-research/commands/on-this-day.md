---
description: List what the church calendar and church history mark on a date (default today)
argument-hint: [date] [liturgical|history|hebrew|all]
allowed-tools: Skill, Read, Write, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:on-this-day` skill for this request: $ARGUMENTS

- If no date is given, use today's date and state it with the year
- Include the Hebrew-calendar correspondence only if the request says `hebrew` or asks about Jewish observances; state the specific year when you do
- Name the specific calendar or source for every entry, and say so if nothing dated and sourced exists for the date
- Present the result as a numbered list the user can choose from, and do not pre-select

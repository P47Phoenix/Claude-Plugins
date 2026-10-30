---
description: Verify a sermon draft - citations, history, doctrine, red team, pacing, or the full gate
argument-hint: <file path | pasted draft> [cite|history|doctrine|redteam|pacing|all]
allowed-tools: Skill, Read, Write, Edit, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:sermon-verification` skill on this input: $ARGUMENTS

Parse the input:

- If the last word is one of `cite`, `history`, `doctrine`, `redteam`, `pacing` or `all`, that is the check. `all` means the full `gate`. Everything before it is the draft: a file path (read it) or pasted text
- If no check is named, ask whether the user wants one check or `all`
- `pacing` is on demand only and is never part of `all`

Follow the skill: print the declaration line, spawn the sub-agent with only the routed reference, and return the report (single checks) or only the corrected draft with "Verification notes" (`all`).

---
description: Build a sermon - shortlist candidate passages, then break down the one you choose
argument-hint: <request> | shortlist <topic> | breakdown <number or passage> | draft | revise <file>
allowed-tools: Skill, Read, Write, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:sermon-builder` skill with this request: $ARGUMENTS

Follow the skill's workflow exactly:

- If the request is a topic or "write a sermon", the task type is `shortlist`: present 3-5 candidates and stop
- `breakdown` and `draft` need a chosen candidate (a number or passage from an earlier shortlist, or given in the request). If none is chosen, run `shortlist` or ask which one. Never pre-select
- Every output passes the verification gate and ends with "Verification notes"

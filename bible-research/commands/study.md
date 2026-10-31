---
description: Research a biblical timeline, song ideas, a word, a person, a theme, passages on a topic, or a church-history question
argument-hint: <request> | timeline <era|book|all> | song-ideas <era|book|all> | word-study <term> | person <name> | theme-trace <theme> | passages <topic> | church-history <question>
allowed-tools: Skill, Read, Write, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:research` skill with this request: $ARGUMENTS

Follow the skill's workflow exactly:

- For `timeline` and `song-ideas`, if no era, book or date range is named, stop after the declaration line and return the numbered era pick list as a question, **without any tool calls** (the list is in the skill). Never pre-select an era
- `song-ideas` builds the timeline first and derives ideas from it. Ideas are a list only: no lyrics, no song titles, no artist names, no handoff to another plugin
- Every date is a range or is marked contested, with its source named
- Every output passes the verification gate and ends with "Verification notes"

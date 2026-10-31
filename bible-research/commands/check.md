---
description: Check the claims in a song, article, post, sermon transcript or devotional
argument-hint: <pasted text | url | file path> [song|web|post|transcript|full]
allowed-tools: Skill, Read, Write, Agent, WebFetch, WebSearch
---

Invoke the `bible-research:topic-verification` skill on this input: $ARGUMENTS

Parse the input:

- If the last word is one of `song`, `web`, `post`, `transcript` or `full`, that is the task type. Everything before it is the artifact: pasted text, a URL (fetch it), or a file path (read it)
- If no type is named, infer it from the input shape and say which you chose
- **Songs:** the user supplies the lyrics. Do not fetch lyrics sites, and never reproduce lyrics in the report. Cite title, songwriter and line position only

Follow the skill: extract the claims, route them to the verification checks, grade the source, and return the topic report.

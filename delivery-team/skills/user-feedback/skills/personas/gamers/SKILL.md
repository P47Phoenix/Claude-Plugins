---
name: user-feedback-personas-gamers
description: Persona-family sub-skill for gamer personas (Casual Casey, Hardcore Hank, Speedrunner Sam, Completionist Cora, Social Sophie, Accessible Alex, Mobile Morgan). Router-dispatched from the user-feedback parent skill on GAME_DEV project type or explicit gamer focus-group request. Loads only the Category 1 profile block from references/persona-library.md.
license: Apache License 2.0 - See repository LICENSE file
tier: C
disable-model-invocation: true
parent_skill: delivery-team/skills/user-feedback/SKILL.md
axis: personas
variant: gamers
---

# Gamer Personas Sub-Skill

Router-dispatched paradigm sub-skill for gamer-family persona feedback. Not directly invokable by the model; the user-feedback parent skill loads this sub-skill only when project type is GAME_DEV or the user explicitly requests gamer personas.

## Personas Covered

| Persona | Profile Section |
|---|---|
| Casual Casey | `references/persona-library.md` § Category 1: Gamers → Casual Casey |
| Hardcore Hank | `references/persona-library.md` § Category 1: Gamers → Hardcore Hank |
| Speedrunner Sam | `references/persona-library.md` § Category 1: Gamers → Speedrunner Sam |
| Completionist Cora | `references/persona-library.md` § Category 1: Gamers → Completionist Cora |
| Social Sophie | `references/persona-library.md` § Category 1: Gamers → Social Sophie |
| Accessible Alex | `references/persona-library.md` § Category 1: Gamers → Accessible Alex (mandatory accessibility persona for game projects) |
| Mobile Morgan | `references/persona-library.md` § Category 1: Gamers → Mobile Morgan |

Reference paths above resolve relative to the parent skill `delivery-team/skills/user-feedback/`.

## Invocation Pattern

Load `../../references/persona-invocation.md` for the shared persona-agent prompt template and overlay handling. Then load the specific persona profile from the parent skill's `references/persona-library.md` Category 1 block. Spawn one sub-agent per persona per the parent skill's Phase 3 procedure.

## Game-Specific Context Hints

When preparing the artifact for gamer personas, always include genre, platform, control scheme, and any monetization model — these heavily influence persona reactions. Accessible Alex must be included in every gamer focus group regardless of count.

---
name: user-feedback-personas-web-app
description: Persona-family sub-skill for web/app user personas (Power User Pat, Average User Avery, First-Timer Fran, Non-Technical Nancy, Accessible User Ash). Router-dispatched from the user-feedback parent skill on GREENFIELD/FEATURE/WEB_APP project type. Loads only the Category 2 profile block from references/persona-library.md.
license: Apache License 2.0 - See repository LICENSE file
tier: C
disable-model-invocation: true
parent_skill: delivery-team/skills/user-feedback/SKILL.md
axis: personas
variant: web-app
---

# Web/App User Personas Sub-Skill

Router-dispatched paradigm sub-skill for web/app user persona feedback. Not directly invokable by the model; the user-feedback parent skill loads this sub-skill only when project type is GREENFIELD, FEATURE, or WEB_APP.

## Personas Covered

| Persona | Profile Section |
|---|---|
| Power User Pat | `references/persona-library.md` § Category 2: Web/App Users → Power User Pat |
| Average User Avery | `references/persona-library.md` § Category 2: Web/App Users → Average User Avery |
| First-Timer Fran | `references/persona-library.md` § Category 2: Web/App Users → First-Timer Fran |
| Non-Technical Nancy | `references/persona-library.md` § Category 2: Web/App Users → Non-Technical Nancy |
| Accessible User Ash | `references/persona-library.md` § Category 2: Web/App Users → Accessible User Ash (mandatory accessibility persona for web/app projects) |

Reference paths above resolve relative to the parent skill `delivery-team/skills/user-feedback/`.

## Invocation Pattern

Load `../../references/persona-invocation.md` for the shared persona-agent prompt template and overlay handling. Then load the specific persona profile from the parent skill's `references/persona-library.md` Category 2 block. Spawn one sub-agent per persona per the parent skill's Phase 3 procedure.

## Web/App Context Hints

When preparing the artifact for web/app personas, include device targets (desktop/tablet/mobile), browser/runtime support, and any onboarding flows. Accessible User Ash must be included in every web/app focus group regardless of count.

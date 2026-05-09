---
name: user-feedback-personas-enterprise
description: Persona-family sub-skill for enterprise / B2B personas (Admin Alice, End User Eddie, Manager Maya, IT/Security Ivan). Router-dispatched from the user-feedback parent skill on ENTERPRISE or B2B project type. Loads only the Category 3 profile block from references/persona-library.md.
license: Apache License 2.0 - See repository LICENSE file
tier: C
disable-model-invocation: true
parent_skill: delivery-team/skills/user-feedback/SKILL.md
axis: personas
variant: enterprise
---

# Enterprise / B2B Personas Sub-Skill

Router-dispatched paradigm sub-skill for enterprise/B2B persona feedback. Not directly invokable by the model; the user-feedback parent skill loads this sub-skill only when project type is ENTERPRISE or B2B.

## Personas Covered

| Persona | Profile Section |
|---|---|
| Admin Alice | `references/persona-library.md` § Category 3: Enterprise / B2B → Admin Alice |
| End User Eddie | `references/persona-library.md` § Category 3: Enterprise / B2B → End User Eddie |
| Manager Maya | `references/persona-library.md` § Category 3: Enterprise / B2B → Manager Maya |
| IT/Security Ivan | `references/persona-library.md` § Category 3: Enterprise / B2B → IT/Security Ivan (covers accessibility-adjacent governance + access concerns) |

Reference paths above resolve relative to the parent skill `delivery-team/skills/user-feedback/`.

## Invocation Pattern

Load `../../references/persona-invocation.md` for the shared persona-agent prompt template and overlay handling. Then load the specific persona profile from the parent skill's `references/persona-library.md` Category 3 block. Spawn one sub-agent per persona per the parent skill's Phase 3 procedure.

## Enterprise Context Hints

When preparing the artifact for enterprise personas, include role-based access descriptions, workflow context, and any compliance / data-residency constraints. Enterprise personas evaluate based on their organizational role; IT/Security Ivan should be included whenever the artifact touches authentication, authorization, audit, or data handling.

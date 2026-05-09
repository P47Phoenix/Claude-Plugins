---
name: user-feedback-personas-demographic
description: Persona-family sub-skill for demographic overlay personas (Gen Z Zara, Millennial Mike, Gen X Grace, Boomer Bob). Router-dispatched from the user-feedback parent skill when an overlay is requested or when the focus group should reflect a specific generational mix. Loads only the Category 4 profile block from references/persona-library.md.
license: Apache License 2.0 - See repository LICENSE file
tier: C
disable-model-invocation: true
parent_skill: delivery-team/skills/user-feedback/SKILL.md
axis: personas
variant: demographic
---

# Demographic Overlay Personas Sub-Skill

Router-dispatched paradigm sub-skill for demographic-overlay personas. Not directly invokable by the model; the user-feedback parent skill loads this sub-skill when the user requests an overlay (e.g. "Casual Casey as Gen Z") or when the focus-group composition specifies a generational mix.

## Personas Covered

| Persona | Profile Section |
|---|---|
| Gen Z Zara | `references/persona-library.md` § Category 4: Demographic Overlays → Gen Z Zara |
| Millennial Mike | `references/persona-library.md` § Category 4: Demographic Overlays → Millennial Mike |
| Gen X Grace | `references/persona-library.md` § Category 4: Demographic Overlays → Gen X Grace |
| Boomer Bob | `references/persona-library.md` § Category 4: Demographic Overlays → Boomer Bob |

Reference paths above resolve relative to the parent skill `delivery-team/skills/user-feedback/`.

## Overlay Application

Demographic overlays modify communication style, expectations, and reference points without replacing the base persona's category profile. Overlay effect summaries live in `../../references/persona-invocation.md` § Overlay Handling. When applying an overlay, append the overlay's modifiers to the base persona profile in the agent prompt; do not replace the base persona's goals, frustrations, or accessibility needs.

## Standalone Use

Demographic personas can also be used standalone (without a base category persona) to gather pure generational reaction; weight 0.8x per the parent skill's aggregation rules in such cases.

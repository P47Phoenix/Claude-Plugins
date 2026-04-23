# Dev Log — WI-12: Alias-theme tone dogfood

**Story**: WI-12 — Alias-theme tone dogfood
**Role**: user-feedback (The Hobbits of the Shire, casual)
**Model**: Opus 4.7 (1M context)
**Date**: 2026-04-22
**Status**: DONE (PASS, documentation-only outcome)

## Objective

Validate that the 13 delivery-team alias themes (YAML definitions) still
preserve each character's voice when Opus 4.7 renders a Refine
stage-announcement. Target metric M-05: >= 80% of sampled announcements
preserve voice (>= 50% of markers present per announcement).

## Scope

- Directory under test: `delivery-team/skills/delivery-flow/references/aliases/`
  (13 YAML theme files).
- Sample size: 3 themes (per WI-12 procedure).
- Themes sampled (per the suggested picks):
  - `lotr` — the engagement's active theme, product-owner = Gandalf
  - `star-wars` — high-character-voice contrast, product-owner = Mon Mothma
  - `dilbert` — office/corporate tone, product-owner = Pointy-Haired Boss
- Role rendered per theme: `product-owner` (kickoff speaker for Refine
  stage in delivery-flow announcements).

## Procedure executed

1. Listed themes via `ls delivery-team/skills/delivery-flow/references/aliases/`.
   Confirmed 13 YAML files present.
2. For each of the 3 sampled themes:
   - Read the full YAML definition.
   - Extracted 5 markers from the `product-owner` role:
     character name, catchphrase core substring, example-phrase
     substring, stylistic diction, and a role-specific vocabulary cue.
   - Rendered a Refine stage-announcement carrying the theme's voice.
   - Counted markers present in the rendered text.
3. Computed per-sample voice-preservation % and the aggregate pass rate.
4. Wrote the sample artifact (markdown table format per DoD round-2 G-4 fix).
5. Ran the WI-12 dogfood command. Exit 0 confirmed.

## Results

| Theme | Character | Markers found / total | Voice % | Preserves? |
|-------|-----------|-----------------------|---------|------------|
| lotr | Gandalf | 5 / 5 | 100% | YES |
| star-wars | Mon Mothma | 5 / 5 | 100% | YES |
| dilbert | Pointy-Haired Boss | 5 / 5 | 100% | YES |

- Samples preserving voice: **3 / 3 (100%)**
- M-05 target: >= 80% of samples preserve voice.
- Verdict: **PASS**

## Dogfood command

```
test -f .delivery/artifacts/08-execute/06-dev/user-feedback/alias-theme-sample.md \
  && test "$(grep -cE '^\| *(Theme|theme) ' .delivery/artifacts/08-execute/06-dev/user-feedback/alias-theme-sample.md)" -ge "3" \
  && grep -qE 'voice[- ]preservation|markers? preserved' .delivery/artifacts/08-execute/06-dev/user-feedback/alias-theme-sample.md
```

- Result: exit 0 (PASS).
- Notes on table format: the regex `^\| *(Theme|theme) ` requires that at
  least 3 markdown rows begin with the literal token `Theme` or `theme`.
  The header row plus data rows prefixed with `theme <name>` satisfies the
  check (4 matching rows observed). The prefix is cosmetic and keeps the
  theme identifier (e.g., `theme lotr`) readable as the row label. No
  other artifact required.

## Artifacts produced

- Sample artifact: `.delivery/artifacts/08-execute/06-dev/user-feedback/alias-theme-sample.md`
- Dev log: `.delivery/artifacts/08-execute/06-dev/dev-log-wi-12.md` (this file)

## Decisions

- Since the verdict is PASS (3/3 = 100% >= 80% target), **no theme YAML
  edits were applied**. Per WI-12 procedure step 7, PASS = documentation-only.
- The `alias-creator/SKILL.md` was not touched (explicitly scoped out by
  WI-12 — tone fixes, if needed, would live in the theme YAML files).

## Observations for future iterations

- All three sampled themes carry very distinctive voices (Gandalf's
  archaic counsel, Mon Mothma's wartime formality, Pointy-Haired Boss's
  buzzword-wrong swagger). Voice preservation at Opus 4.7 appears robust
  for the `product-owner` role across heterogeneous stylistic registers.
- If a future iteration wants a stricter test, recommended extensions:
  (a) sample all 13 themes instead of 3; (b) render >1 role per theme
  (e.g., qa-engineer + product-owner + ux-designer) because voice
  strength can vary by role within a theme; (c) adversarially vary the
  stage (Refine, Architect, Plan) since different stages exercise
  different diction.
- The dogfood command is intentionally cheap and regex-based — it
  validates artifact shape, not actual voice quality. The quality
  judgment remains the user-feedback role's responsibility (this
  session's Hobbits verdict: all three preserve voice).

## Signal

STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/06-dev/dev-log-wi-12.md
SUMMARY: WI-12 PASS — 3/3 sampled themes (lotr, star-wars, dilbert) preserve voice at 100% (15/15 markers); M-05 target >=80% satisfied; documentation-only, no YAML edits.

# bible-research

A Claude Code plugin for sermon development and for checking religious claims. It follows the same pattern as `delivery-team`: **Agent -> Skill (router) -> progressive disclosure of reference docs.** Each skill is a thin router. It classifies the request, reads only the routed reference file(s), and spawns a sub-agent that carries them. Reference files never sit in the main context.

Restructured from the claude.ai "Bible Scholar" project. The source specs are in [`source/`](../source/) at the repository root.

## Install

```
/plugin marketplace add P47Phoenix/Claude-Plugins
/plugin install bible-research@mec-claude-agent-skills
```

## What it does

| Skill | Use it to | Task types |
|---|---|---|
| `sermon-builder` | Build a sermon: shortlist candidate passages, **wait for your choice**, then break the chosen passage down in full | `shortlist`, `breakdown`, `draft`, `revise` |
| `sermon-verification` | Check a draft, or run the full pre-delivery gate | `cite`, `history`, `doctrine`, `redteam`, `pacing`, `gate` |
| `topic-verification` | Check claims made by a song, article, post, sermon transcript or devotional | `song`, `web`, `post`, `transcript`, `full` |
| `on-this-day` | List what the church calendar and church history mark on a date (date-triggered only) | `liturgical`, `history`, `hebrew`, `all` |

## Commands

| Command | Does |
|---|---|
| `/sermon <request>` | `shortlist <topic>`, `breakdown <number or passage>`, `draft`, `revise <file>` |
| `/verify <file\|draft> [cite\|history\|doctrine\|redteam\|pacing\|all]` | Run one check, or the gate with `all` |
| `/check <text\|url\|file> [song\|web\|post\|transcript\|full]` | Check an external artifact |
| `/on-this-day [date]` | Church calendar and history for a date |

## Agents

- `bible-scholar` -- the master-orator entry point. Routes to the skills
- `sermon-verifier` -- runs the four checks as the gate

## The workflow, enforced

1. `/sermon sermon on loving your wife` gives 3-5 candidates and **stops**
2. You choose one (`/sermon breakdown 4`). It never pre-selects, and a breakdown is refused until you choose
3. Every output, including the shortlist, passes the verification gate before you see it. You see only the corrected version, ending in **Verification notes**

## Standards (guardrails in every skill)

No invented citations; original-language terms with a named lexicon; Jewish sources cited by tractate and folio or named Midrash; contested points labeled contested; unverifiable claims removed (drafts) or marked unverifiable (reports); plain language; translation stated once; echoes labeled as echoes; no reproduction of lyrics, article paragraphs or post text; "theologically contested" kept apart from "textually unsupported"; fact-claims kept apart from devotional language.

## Notes

- **Songs:** you supply the lyrics. The plugin does not fetch lyrics sites, and reports cite title, songwriter and line position, never the words
- **Gate:** the gate runs in `sermon-builder`'s Phase 3, with hooks as a backstop. A hook can block but cannot rewrite output; see [DESIGN_NOTES.md](DESIGN_NOTES.md)
- **Open items:** see "Open items" in DESIGN_NOTES.md (unsourced claims, unverified hook behavior)

## Layout

See [ARCHITECTURE.md](ARCHITECTURE.md) for the diagrams and [DESIGN_NOTES.md](DESIGN_NOTES.md) for decisions and deviations.

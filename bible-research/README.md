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
| `research` | Research a sourced biblical timeline, derive a **list** of song ideas from it (asks you to pick an era first), run a word study, profile a person, trace a theme, find passages, or answer a church-history question | `timeline`, `song-ideas`, `word-study`, `person`, `theme-trace`, `passages`, `church-history` |
| `idea-team` | Run an idea past a team of simulated personas: isolated agents, facilitated rounds that bounce ideas to an honest consensus, or an interactive talk-through | `review`, `talk` |

## Commands

| Command | Does |
|---|---|
| `/sermon <request>` | `shortlist <topic>`, `breakdown <number or passage>`, `draft`, `revise <file>` |
| `/verify <file\|draft> [cite\|history\|doctrine\|redteam\|pacing\|all]` | Run one check, or the gate with `all` |
| `/check <text\|url\|file> [song\|web\|post\|transcript\|full]` | Check an external artifact |
| `/on-this-day [date]` | Church calendar and history for a date |
| `/research <request>` | `timeline <era\|book\|all>`, `song-ideas <era\|book\|all>`, `word-study <term>`, `person <name>`, `theme-trace <theme>`, `passages <topic>`, `church-history <question>` |
| `/team <idea> [review\|talk] [rounds: N] [personas: ...]` | Multi-round persona review, or talk mode (`whole team`, `bounce`, `summary`, `switch`, `add`, `drop`, `end`) |

## Agents

- `bible-scholar` -- the master-orator entry point. Routes to the skills
- `sermon-verifier` -- runs the four checks as the gate
- `idea-persona` -- one simulated reviewer per dispatch; the persona card is injected, never built in; no `Agent` tool
- `idea-facilitator` -- frames the idea, then synthesizes the rounds into the report; holds no opinion

## Research and song ideas

1. `/research song-ideas` with no era returns a numbered list of eleven eras (Primeval to Early church) and **stops**. Pick one or more, or say `all`. A run covers at most three eras; `all` goes in batches with `next`
2. One researcher per era slice runs in parallel, an assembler merges them, and the gate checks every event, reference and date before you see it
3. Every date is a range or marked **contested** with its source (Exodus early or late, Jerusalem 587 or 586 BC, crucifixion AD 30 or 33); a single year appears only when tied to a named external anchor such as the Babylonian Chronicle. A date with no located source is dropped
4. Song ideas are **creative inference, labeled as such**: event, passage, angle, register, a neutral theme, source tag. No lyrics, no song titles, no artist names, and no handoff to another plugin. The list is yours to take elsewhere

## The idea team

- **Personas** (`skills/idea-team/references/persona-library.md`): Pastor, Original-Language Scholar, Church Historian, Second-Temple and Rabbinic Scholar, Worship Leader; Skeptic, Lay Listener, Pragmatist, Creative. Roster 3-7 by topic (default 5); Skeptic and Lay Listener are always in. Add your own in `.bible-research/personas.yml`
- **Isolation with bounce:** each persona is its own agent and never shares a context with another. From round 2, each persona gets a fresh agent with the attributed digest of the previous round and must agree, rebut, refine or change its mind with a stated reason. At least two rounds; more only while positions move, up to the cap (default 3, max 4; set `rounds: N`)
- **Honest consensus:** the facilitator reports consensus, majority or split as found, who changed their mind and why, concerns ranked by agree-count (4+ critical, 3 high, 2 medium, 1 low), the Skeptic's surviving objection, and the strongest revised idea as a proposal
- **Rules:** personas are simulated viewpoints, never real people or official denominational positions; opinion is labeled opinion; fact claims need a real source; reports pass the verification gate

## The workflow, enforced

1. `/sermon sermon on loving your wife` gives 3-5 candidates and **stops**
2. You choose one (`/sermon breakdown 4`). It never pre-selects, and a breakdown is refused until you choose
3. Every output, including the shortlist, passes the verification gate before you see it. You see only the corrected version, ending in **Verification notes**

## Standards (guardrails in every skill)

No invented citations; original-language terms with a named lexicon; Jewish sources cited by tractate and folio or named Midrash; contested points labeled contested; unverifiable claims removed (drafts) or marked unverifiable (reports); plain language; translation stated once; echoes labeled as echoes; no reproduction of lyrics, article paragraphs or post text; "theologically contested" kept apart from "textually unsupported"; fact-claims kept apart from devotional language.

## Notes

- **Songs:** you supply the lyrics. The plugin does not fetch lyrics sites, and reports cite title, songwriter and line position, never the words
- **Gate:** the gate runs in `sermon-builder`'s Phase 3, `research`'s Phase 3 and `idea-team`'s Phase 4, with hooks as a backstop. A hook can block but cannot rewrite output; see [DESIGN_NOTES.md](DESIGN_NOTES.md)
- **Talk mode** is conversational and not gated turn by turn; the `summary` report is
- **Open items:** see "Open items" in DESIGN_NOTES.md (unsourced claims, unverified hook behavior)

## Layout

See [ARCHITECTURE.md](ARCHITECTURE.md) for the diagrams and [DESIGN_NOTES.md](DESIGN_NOTES.md) for decisions and deviations.

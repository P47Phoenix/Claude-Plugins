# Design Notes

Decisions, deviations from the `delivery-team` pattern, schema findings, and open items for `bible-research`. Verified against the official Claude Code docs on 2026-10-30 and with `claude plugin validate` (Claude Code 2.1.314).

## 1. The pattern extracted from delivery-team

From `delivery-team/skills/quality/SKILL.md` and `architect/SKILL.md`:

- SKILL.md is a thin router: a "Design Principle: <X> Isolation" section; Phase 1 task classification with a declaration line (`Task Type: [...] | References: [...] | Scope: [...]`); Phase 2 sub-agent invocation via the `Agent` tool with a literal prompt template that pastes only the routed `references/*.md` file(s); a routing table; output contracts in `references/contracts/`; numbered guardrails; user commands; a References index
- Reference files are read only for the routed task type
- Router line budgets are enforced by `scripts/check_skill_budgets.py` (Tier B 300, Tier C 200). The 0.1.0 skills are 134-173 lines. As of 0.2.0 `bible-research` is in `BUDGETED_PLUGINS`, so CI checks all six SKILL.md files

## 2. Deviations, and why

| Deviation | Why |
|---|---|
| **The gate lives in `sermon-builder` Phase 3, not in a hook.** Hooks (`SubagentStop`, `Stop`) are a backstop | Per the hooks docs, `Stop` and `SubagentStop` can only block or continue (`decision: "block"`, `continue: false`); no hook can rewrite or suppress a final message. A hook alone could not stop the user seeing a pre-correction draft. The skill spawns the verifier and returns only its output, which meets "the user must never see the pre-correction draft". Both hooks are deterministic **command** hooks (`hooks/gate_check.py`), not model-judged prompt hooks: no model call, no cost on non-sermon turns, and they fire only when builder-output markers are present, so a refusal or "which candidate?" reply is never blocked. They also stand down when `stop_hook_active` is set, so a block cannot loop. The `SubagentStop` hook (matcher `.*sermon-verifier`) keeps the verifier working until its output ends in "Verification notes", has no draft marker and no per-check report. The `Stop` hook blocks a main-thread reply that delivers builder output without notes. The router must spawn the verifier with `subagent_type: bible-research:sermon-verifier` so the backstop applies |
| **`topic-verification` spawns every sub-agent from the router (flat fan-out)** | The docs say subagents can spawn subagents (default depth limit 3, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`), so the brief's nested-spawning check passes on paper. Nesting was **not tested** in this build, and the docs do not describe how skill `allowed-tools` interacts with spawning. A flat design works with the depth limit at 1, so the pasted-references fallback was not needed |
| **`commands/` kept alongside `skills/`** | The brief asks for `commands/`. The docs say custom commands "have been merged into skills" and prefer `skills/` for new plugins, but nothing is deprecated. Each command is a thin wrapper that invokes its skill |
| **A `plugin.json` is present, unlike other plugins in this repo** | Other plugins here have no `.claude-plugin/plugin.json` and are registered through `marketplace.json` with `"strict": false` and a skills list. The brief asks for a manifest. The marketplace entry therefore carries only `name`, `source` and `description`: with `strict: false`, declaring components in the entry while a `plugin.json` exists gives a "conflicting manifests" error |
| **`draft` and `revise` reuse the breakdown contract** | The required layout lists three contracts (`shortlist`, `breakdown`, `verification-notes`). `draft` adds an optional section 8 (Manuscript); `revise` returns changed sections only |
| **Reference files are pasted by the router, then sub-agent reads nothing else** | Matches delivery-team ("Read only the reference file(s)... paste"). The routed files pass through main context once, transiently; unrouted files are never read. A stricter option (pass paths, let the sub-agent read) is possible but departs from the pattern |
| **`sermon-verifier` agent has no `Agent` tool** | Prevents nested spawning from the gate |
| **On This Day output carries its own "Verification notes" line, not the full gate** | The brief scopes the gate to `sermon-builder` output. The project's own best On This Day chats carry a notes line, so the contract requires one |
| **`research` reuses the `sermon-verifier` gate rather than its own checker** (0.2.0) | Timelines, song-idea lists and findings are fact-bearing content of the same kind the gate already checks. The dispatch adds one instruction (keep the contract, do not rewrite song ideas, remove an idea whose event cannot be sourced) instead of a second verifier |
| **`research` fans out one researcher per era slice, then an assembler** (0.2.0) | Same flat fan-out as `topic-verification`. A whole-Bible timeline in one agent would exceed a sensible context and lose sources; per-slice researchers keep `timeline-eras.md` sections small. The assembler renumbers `S[N]` IDs so they stay unique |
| **Era pick is mandatory; the whole Bible is never the default** (0.2.0) | Mirrors shortlist-then-pick. The user asked that the skill ask rather than guess the era; "all" is an explicit answer |
| **Song ideas are a list, labeled inference, with no handoff to `music-team`** (0.2.0) | The user asked for a list only. The anti-lyric and anti-artist rules keep the output from becoming a song draft, and keep the gate's job to the facts behind the ideas |
| **`idea-team` keeps persona isolation and still bounces ideas** (0.2.0) | `user-feedback` forbids personas seeing each other to avoid early convergence. The user wanted ideas to bounce and reach a better consensus. The resolution: fresh agents each round, with the previous round relayed as an attributed digest by the router. No two personas ever share a context; a position must be re-argued from the digest, not remembered |
| **Anti-sycophancy is a rule, not a hope** (0.2.0) | A change of position without a reason that names the argument is recorded as "unsupported change" and does not count as movement for the stop rule. The Skeptic must carry its best surviving objection into the report even when outvoted. The facilitator counts agreement only from what was said; silence is not agreement |
| **`idea-persona` and `idea-facilitator` are named agents without an `Agent` tool** (0.2.0) | Same reason as `sermon-verifier`: flat fan-out, no nesting from inside a persona. The card is injected per dispatch so one agent definition serves every persona, built-in or custom |
| **Talk mode is not gated turn by turn** (0.2.0) | A gate on every conversational reply would make talk mode unusable. Team rules still bind each turn (fact claims need a source or `[UNVERIFIED]`), and the `summary` report goes through the gate |
| **The Stop hook matches the new contracts by top-level heading plus a contract header line** (0.2.0) | A `Timeline`, `Song Ideas`, `Idea Review` or `Research Findings` top-level heading (case-insensitive, colon or dash, up to two leading words) counts only together with the contract's header line (`**Eras covered:**`, `**Personas:**`, `**Question shape:**`). The hook runs in every session where the plugin is enabled, so a delivery-team plan titled `# Timeline: Q3` or a music-team reply headed `# Song Ideas:` must not be blocked. Tests cover each heading, the variants, the era pick list, a talk turn and the project-plan false positive |
| **The gate keeps contract labels** (0.2.0) | `corrected-draft.md` said "no flags left in the text", which would have stripped the `[INFERENCE]` label every song idea needs and the `[CONTESTED]`, `[TRADITIONAL]`, `[Single-source]` and (in findings and reports) `[UNVERIFIED]` tags. The contract, the verifier agent and both gate dispatches now say those are contract labels, not flags |
| **Every idea-review report goes through the gate** (0.2.0) | The facilitator always writes the draft marker and the hook always gates the heading, so a "no claims, skip the gate" path would be blocked. The gate's notes say "no claims to check" when that is the case |
| **A research run covers at most three eras** (0.2.0) | One verifier must check every event in one context; eleven eras of events plus ideas would not fit. "All" runs in batches of three with `next`. Ideas are about 15-20 for one era, about 10 per era in a batch |
| **A single anchored year is allowed** (0.2.0) | "Always a range" would force fake ranges on 605, 597 and 701 BC, which rest on the Babylonian Chronicle and Sennacherib's prism. A single year is allowed only when the cell names its external anchor with a source ID |
| **Rounds: at least two, continue while positions move, default cap 3, max 4** (0.2.0) | The plan said "default 2 rounds, max 4". A cap of 2 would never act on round-2 movement, which defeats "bounce until consensus". The default cap is 3; the user sets `rounds: 2-4`. Flagged in the PR as an assumption |

## 3. Frontmatter fields dropped or kept

The docs list the supported SKILL.md fields. Unknown keys are silently ignored.

| Field (delivery-team) | Decision | Reason |
|---|---|---|
| `context_budget` | **Dropped** | Not a documented field; ignored by Claude Code |
| `model_awareness` | **Dropped** | Not a documented field |
| `pattern_library_version` | **Dropped** | Not a documented field |
| `phase_1_detector_model` | **Dropped** | Not a documented field |
| `allowed-tools` | Kept, as a YAML list including `Agent` | Documented; accepts a list, string or comma list. Grants pre-approval, does not restrict |
| `tier`, `last_audited`, `maintainer`, `fitness_review_due` | Kept | Repo-governance metadata (budget script, weekly fitness-review workflow). Ignored by Claude Code |
| `license` | Kept | Accepted, not acted on |

Plugin agents ignore `hooks`, `mcpServers` and `permissionMode`; none are used. Hooks ship in `hooks/hooks.json`. The `$1` / `$0` indexing in commands is 0-based, so the commands parse `$ARGUMENTS` instead.

## 4. Source material and examples

- `source/` holds the project instructions (the newer version, with the plain-language rule and the gate), the six agent specs and the On This Day skill, copied from the claude.ai project
- **Chosen examples.** The project's 32 chats were scored two ways: by the project itself and by an independent reviewer. `source/sample-breakdown-loving-your-wife.md` (the only run showing shortlist, then a user pick, then a five-part breakdown) and `source/sample-shortlist-ezekiel.md` (best shortlist) were chosen. The John 14 / Ezekiel file was **not** used because the user judged it not a good example
- **Breakdown sections 1-7 are inferred, not copied.** The brief says to model the contract on `John-14-through-Ezekiel.md` sections 1-7, but that file was not read. The seven sections come from the project instructions (five required parts) plus the scripture index and bibliography seen in the best chats. **Accepted as is by Michael (2026-10-30)**, who judged the John 14 file not a good example; revisit only if a better gold-standard breakdown turns up

## 5. Verification of the plugin

- `claude plugin validate ./bible-research` and `claude plugin validate .` (the marketplace) pass. One suggestion remains: no listing icon (`ICON_MISSING`)
- `tests/test_gate_check.py` (28 tests as of 0.2.0; 14 in 0.1.0) passes: the hook logic is covered for clean output, missing notes, leaked draft marker, per-check report leak, refusal turns, ordinary replies, malformed input, the repeat-block guard, and (0.2.0) the timeline, song-ideas, idea-review and research-findings contracts, heading variants, the era pick list, a talk turn, a non-top-level heading, and another plugin's `# Timeline:` or `# Song Ideas:` without the contract header
- An independent Opus review of 0.2.0 found 20 issues (13 should-fix, 7 nits), all applied: contract labels kept through the gate; every idea-review report gated; findings heading in the hook; second-marker requirement and case-insensitive headings; anchored single years; the single-slice song-ideas path; the three-era batch cap; a book-to-era table; "poke holes" removed from idea-team triggers; verifier agent updated for its new callers; the round rule; custom-persona restrictions on named people and official voices; and the timeline-eras wording on Daniel, Herod's death, the 587/586 split and the transfiguration references
- An independent review (Opus) found nine issues and a wrong lectionary rule; these fixes were applied: verifier gets the `sermon-verification` guardrails 1-12 and must be the `sermon-verifier` agent type; builder gets guardrails 1-12; the Stop hook became a deterministic command hook; `draft` without a breakdown loads the full breakdown references; one rule for naming a passage directly; dangling cross-skill references inlined or given full paths; `song-theology.md` goes to the doctrine check for songs; "not given" for missing attribution; the lectionary-year rule (remainder 0 is A, 1 is B, 2 is C); a Julian/Gregorian caveat for Protestant German states; Athanasian vs Nicene wording on modalism
- The Hebrew sample in `hebrew-calendar.md` (13 September 2026 is 2 Tishrei 5787, Rosh Hashanah II) was checked against the Hebcal converter
- 0.1.0: not run: the sub-agent flows end to end, nested spawning, and the slash commands
- 0.2.0 **smoke test from disk** (`claude -p ... --plugin-dir ./bible-research`, scratch dir under `D:/tmp`, 2026-10-30/31), all four passed: (1) `song-ideas` with no era stopped at the eleven-era pick list with no timeline or ideas; (2) `song-ideas Exodus and wilderness` returned the `# Song Ideas:` contract with 21 `[INFERENCE]` ideas, no lyrics or artists (the gate reworded four themes that sat near existing song titles), the Exodus date as contested with both sides sourced, and closing Verification notes, in about 9 minutes; (3) `team review` on a Ruth series, two rounds, five personas: round 2 engaged round 1 (three personas changed position with the named argument, two held), consensus / majority / split reported as found, the Skeptic's objection kept at critical, honesty line present, Verification notes present, about 20 minutes for twelve agents plus the verifier; (4) `team talk` returned the frame and a labeled Original-Language Scholar reply with opinion marked and one `[UNVERIFIED]` tag, in 90 seconds. Stderr was empty on every run: the Stop hook executed on each turn without error and blocked none of them, which confirms the hook protocol wiring (`last_assistant_message` is read, the command runs under `${CLAUDE_PLUGIN_ROOT}`). Whether the `SubagentStop` matcher fired on the verifier was not directly observable from `-p` output and stays unconfirmed
- Smoke findings fixed in the third commit: the `/research` command collided with the `research-agent` plugin's `/research` (renamed to `/study`), and the no-era path ran a slow filesystem search before asking (the pick list is now inline in SKILL.md with a no-tool-calls rule; the first run took 12 minutes, the rerun of the same path was not repeated)

## 6. Open items

### Needs source (listed from `viral-claims.md`)

- **John 14:2-3 "Jewish wedding custom"**: no source found (searches returned only sermons; a Mishnah Ketubot 5:2 mention was an unverified search snippet). Reported as unverifiable
- **Agape / phileo**: Carson's page number for John 21 not verified (secondary sources conflict); BDAG s.v. *agapao* / *agape* not opened
- **"Abba isn't Daddy"**: Barr's text not read directly; content is from a Gospel Coalition summary. Jeremias page not verified
- **"Fear not" 365**: the only source opened was a Substack post. A concordance count per translation is needed
- **Tetelestai**: Moulton and Milligan (1915) not opened; Manning's source is a blog post
- Entries for Selah and *dabar* were dropped for lack of sources

### Unverified behavior

- The hook protocol, partly confirmed in 0.2.0: the Stop hook runs on every turn from `${CLAUDE_PLUGIN_ROOT}` without error (four smoke runs). Still unconfirmed: that a `{"decision": "block", "reason": ...}` reply actually blocks a live stop (no smoke run produced gated output without notes, so no block was observed), and that the matcher `.*sermon-verifier` matches the plugin-namespaced agent type. If `last_assistant_message` is absent, the script allows the stop rather than blocking
- **Transcript visibility:** the internal draft passes through the main thread as an Agent tool result and as the verifier's input, so it appears in the session transcript view. Only the final reply is clean. The gate guarantees the user is never *shown* the draft in the reply, not that it is absent from tool traces
- `song-theology.md`: confession-by-confession citations and secondary-work page numbers are marked as items to source
- `church-history-dates.md` gives leads, marked to re-verify at use; none was opened in this build (a reviewer judged all five consistent with their recollection)

- `timeline-eras.md` (0.2.0) gives event leads by passage reference and names the chronologies that date them (Thiele, Kitchen, Finegan, Hoehner, the Babylonian Chronicle, the Gallio inscription). None of those works was opened in this build; the researcher must open the work, or a page that cites it by section, before a date appears in output, and the file says so. The era list and the known dating splits came from general knowledge and should be checked against a chronology on first real use

### Risks

- The gate depends on the router following Phase 3 (sermon-builder, research) or Phase 4 (idea-team). Hooks catch a missing notes section but cannot repair a leak
- The hook's marker patterns (`Why it fits`, `Original Context` plus `Original-Language Notes`, the four contract headings with their header lines `**Eras covered:**`, `**Personas:**`, `**Question shape:**`) must stay in step with the contracts; change them together
- `idea-team` review mode spawns (personas x rounds) + 2 agents: five personas for two rounds is twelve agents plus the verifier; the default cap of three rounds is seventeen; four rounds with seven personas is thirty. The caps exist for cost; the user can lower them with `rounds:` and `personas:`
- Isolation with bounce is only as good as the digest. If the router summarizes instead of copying entries unedited, personas converge on the router's framing; the contract forbids editing entries for that reason
- The `commands/` wrappers duplicate routing that the skills already do

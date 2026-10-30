# Design Notes

Decisions, deviations from the `delivery-team` pattern, schema findings, and open items for `bible-research`. Verified against the official Claude Code docs on 2026-10-30 and with `claude plugin validate` (Claude Code 2.1.314).

## 1. The pattern extracted from delivery-team

From `delivery-team/skills/quality/SKILL.md` and `architect/SKILL.md`:

- SKILL.md is a thin router: a "Design Principle: <X> Isolation" section; Phase 1 task classification with a declaration line (`Task Type: [...] | References: [...] | Scope: [...]`); Phase 2 sub-agent invocation via the `Agent` tool with a literal prompt template that pastes only the routed `references/*.md` file(s); a routing table; output contracts in `references/contracts/`; numbered guardrails; user commands; a References index
- Reference files are read only for the routed task type
- Router line budgets are enforced by `scripts/check_skill_budgets.py` (Tier B 300, Tier C 200). The new skills are 134-173 lines. The script only walks `BUDGETED_PLUGINS` (`delivery-team`, `music-team`); adding `bible-research` is a one-line change that was left out of scope

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
- **Breakdown sections 1-7 are inferred, not copied.** The brief says to model the contract on `John-14-through-Ezekiel.md` sections 1-7, but that file was not read. The seven sections come from the project instructions (five required parts) plus the scripture index and bibliography seen in the best chats. **Confirm or correct against the John 14 file**

## 5. Verification of the plugin

- `claude plugin validate ./bible-research` and `claude plugin validate .` (the marketplace) pass. One suggestion remains: no listing icon (`ICON_MISSING`)
- `tests/test_gate_check.py` (14 tests) passes: the hook logic is covered for clean output, missing notes, leaked draft marker, per-check report leak, refusal turns, ordinary replies, malformed input and the repeat-block guard
- An independent review (Opus) found nine issues and a wrong lectionary rule; these fixes were applied: verifier gets the `sermon-verification` guardrails 1-12 and must be the `sermon-verifier` agent type; builder gets guardrails 1-12; the Stop hook became a deterministic command hook; `draft` without a breakdown loads the full breakdown references; one rule for naming a passage directly; dangling cross-skill references inlined or given full paths; `song-theology.md` goes to the doctrine check for songs; "not given" for missing attribution; the lectionary-year rule (remainder 0 is A, 1 is B, 2 is C); a Julian/Gregorian caveat for Protestant German states; Athanasian vs Nicene wording on modalism
- The Hebrew sample in `hebrew-calendar.md` (13 September 2026 is 2 Tishrei 5787, Rosh Hashanah II) was checked against the Hebcal converter
- Not run: the sub-agent flows end to end, nested spawning, and the slash commands

## 6. Open items

### Needs source (listed from `viral-claims.md`)

- **John 14:2-3 "Jewish wedding custom"**: no source found (searches returned only sermons; a Mishnah Ketubot 5:2 mention was an unverified search snippet). Reported as unverifiable
- **Agape / phileo**: Carson's page number for John 21 not verified (secondary sources conflict); BDAG s.v. *agapao* / *agape* not opened
- **"Abba isn't Daddy"**: Barr's text not read directly; content is from a Gospel Coalition summary. Jeremias page not verified
- **"Fear not" 365**: the only source opened was a Substack post. A concordance count per translation is needed
- **Tetelestai**: Moulton and Milligan (1915) not opened; Manning's source is a blog post
- Entries for Selah and *dabar* were dropped for lack of sources

### Unverified behavior

- The hook protocol itself: that Stop and SubagentStop input includes `last_assistant_message` and `stop_hook_active`, that `{"decision": "block", "reason": ...}` on stdout blocks the stop, and that the matcher `.*sermon-verifier` matches the plugin-namespaced agent type. These came from a partly read docs page and are unconfirmed. The hook script's own logic is tested; its wiring into a live session is not. If `last_assistant_message` is absent, the script allows the stop rather than blocking
- **Transcript visibility:** the internal draft passes through the main thread as an Agent tool result and as the verifier's input, so it appears in the session transcript view. Only the final reply is clean. The gate guarantees the user is never *shown* the draft in the reply, not that it is absent from tool traces
- `song-theology.md`: confession-by-confession citations and secondary-work page numbers are marked as items to source
- `church-history-dates.md` gives leads, marked to re-verify at use; none was opened in this build (a reviewer judged all five consistent with their recollection)

### Risks

- The gate depends on the router following Phase 3. Hooks catch a missing notes section but cannot repair a leak
- The hook's marker patterns (`Why it fits`, `Original Context` plus `Original-Language Notes`) must stay in step with the shortlist and breakdown contracts; change them together
- The `commands/` wrappers duplicate routing that the skills already do

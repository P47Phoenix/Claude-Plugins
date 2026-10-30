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
| **The gate lives in `sermon-builder` Phase 3, not in a hook.** Hooks (`SubagentStop`, `Stop`) are a backstop | Per the hooks docs, `Stop` and `SubagentStop` can only block or continue (`decision: "block"`, `continue: false`); no hook can rewrite or suppress a final message. A hook alone could not stop the user seeing a pre-correction draft. The skill spawns the verifier and returns only its output, which meets "the user must never see the pre-correction draft". The `SubagentStop` hook (matcher `sermon-verifier`) keeps the verifier working until its output ends in "Verification notes" and has no draft marker. The `Stop` hook flags a main-thread reply that delivers builder output without notes |
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

- `claude plugin validate ./bible-research` passes. One suggestion remains: no listing icon (`ICON_MISSING`)
- Not run: the hooks, the sub-agent flows, nested spawning, and the slash commands. None has been exercised end to end

## 6. Open items

### Needs source (listed from `viral-claims.md`)

- **John 14:2-3 "Jewish wedding custom"**: no source found (searches returned only sermons; a Mishnah Ketubot 5:2 mention was an unverified search snippet). Reported as unverifiable
- **Agape / phileo**: Carson's page number for John 21 not verified (secondary sources conflict); BDAG s.v. *agapao* / *agape* not opened
- **"Abba isn't Daddy"**: Barr's text not read directly; content is from a Gospel Coalition summary. Jeremias page not verified
- **"Fear not" 365**: the only source opened was a Substack post. A concordance count per translation is needed
- **Tetelestai**: Moulton and Milligan (1915) not opened; Manning's source is a blog post
- Entries for Selah and *dabar* were dropped for lack of sources

### Unverified behavior

- The exact response schema for `prompt`-type `Stop` and `SubagentStop` hooks (`{"ok": true|false, "reason": ...}`) was taken from the docs summary, and the hooks page was only partly read. **Test the hooks before relying on them**
- `song-theology.md`: confession-by-confession citations and secondary-work page numbers are marked as items to source
- `church-history-dates.md` and `hebrew-calendar.md` give leads and worked examples marked to re-verify at use; the Hebrew sample date was not checked against a converter in this build

### Risks

- The gate depends on the router following Phase 3. Hooks catch a missing notes section but cannot repair a leak
- A prompt-hook check is model-judged, so it can mis-fire in either direction. Consider a command hook with a simple pattern test if it proves noisy
- The `commands/` wrappers duplicate routing that the skills already do

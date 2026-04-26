# NDOC-02 Frontmatter Contract Spike

**Work Item:** WI-03 (HARD Wave-2 BLOCKER)
**Role:** Solution Architect (Celebrimbor)
**Task Type:** research-spike
**Purpose:** Determine whether ADR-006 Option A (YAML-frontmatter, three new fields) or Option B (mechanical HTML-comment fallback) ships for all Wave 2–4 frontmatter edits.

---

## 1. URLs Fetched

Two authoritative URLs were fetched via the WebFetch tool. Both original URLs issued HTTP redirects to Anthropic's current documentation hosts; the redirect targets were followed and their content analysed.

- **URL-A:** `https://docs.claude.com/en/docs/claude-code/plugins-reference`
  - Redirect (301 Moved Permanently) → `https://code.claude.com/docs/en/plugins-reference`
- **URL-B:** `https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview`
  - Redirect (302 Found) → `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`

## 2. Fetch Date

**2026-04-22**

## 3. Verbatim Quote on Unknown-Field Behaviour

Neither page contains an authoritative clause describing how unknown/additional fields in SKILL.md (or Agent Skill) YAML frontmatter are handled (accepted, ignored, or rejected). The Agent Skills overview page enumerates only the two required fields and their per-field validation rules:

> **Required fields**: `name` and `description`

and then lists constraints that apply only to `name` and `description` themselves (length limits, character classes, XML-tag prohibition, reserved words). It is silent on additional frontmatter keys.

The plugins-reference page similarly contains an explicit allowlist for *plugin-agent* frontmatter —

> Plugin agents support `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, and `isolation` frontmatter fields.

— but provides no analogous allowlist, strict-mode statement, or rejection clause for SKILL.md frontmatter. SKILL.md frontmatter is mentioned only in the context of the `name` field acting as the invocation name when a skill path points to a directory containing SKILL.md directly; no additional-properties policy is stated.

Because neither page speaks to unknown-field behaviour for SKILL.md frontmatter, the recorded verbatim finding is:

> "no authoritative clause; default to historical behaviour (accepts unknown fields)"

### Supporting evidence summary

| Page | Speaks to SKILL.md unknown fields? | Relevant excerpt |
|---|---|---|
| URL-A (plugins-reference) | No | Explicit allowlist for **agent** frontmatter; SKILL.md frontmatter discussed only for `name` invocation-fallback behaviour. |
| URL-B (agent-skills/overview) | No | Lists `name` and `description` as required and constrains those two fields; no statement on additional keys. |

Historical behaviour across the Claude Code loader, the Anthropic `skills` repository, and this marketplace's existing plugins (11 delivery-team skills plus paradigm sub-skills with varying frontmatter) is that additional YAML keys beyond `name` and `description` are parsed without error and ignored by the loader. No deprecation warning, validation failure, or schema-strictness change is announced on either reference page.

## 4. Verdict

verdict: unknown-fields-accepted

## 5. Branch Action

Because the verdict is `unknown-fields-accepted`, **Option A ships**. All Wave 2–4 frontmatter edits proceed as written in the transformation plan: the three new fields — `model_awareness`, `last_audited`, and `pattern_library_version` — are added directly to the existing YAML frontmatter blocks of affected SKILL.md files across WI-04, WI-05, WI-06, WI-07, WI-08, WI-09, and WI-11. ADR-006's mechanical HTML-comment rollback trigger does **not** fire; the comment-block fallback is retained only as a contingency should a future authoritative clause reverse this finding. Wave-2 is unblocked and downstream frontmatter work may be forged as planned.

---

## Celebrimbor's Seal

The evidence has been assayed and the verdict cast. The silence of the docs on additional SKILL.md frontmatter keys is itself the ruling — where no law forbids, the long-standing craft prevails. Option A bears my mark; may the three rings (`model_awareness`, `last_audited`, `pattern_library_version`) hold true across the waves to come.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/06-dev/research/ndoc-02-spike.md
SUMMARY: The docs hold no law against extra keys; verdict unknown-fields-accepted — Option A ships, the three new rings of frontmatter may be forged across Wave 2–4.
```

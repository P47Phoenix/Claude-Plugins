# Dev Log — WI-05

**Work item:** WI-05 — `prompt-engineer/SKILL.md` pattern-library expansion + PAT-01 reframe
**Role:** Developer (Gimli)
**Skill:** `delivery-team:developer` + `plugin-dev:skill-development`
**Date:** 2026-04-22

## Scope executed

Five edits against `prompt-engineer/SKILL.md` (central pattern library, ADR-005) plus one G-5 carry-over in `research-agent/references/prompt-library.md`.

## Edits applied

### EDIT 1 — PAT-01 reframe (prompt-engineer/SKILL.md, Claude sub-section at ~line 81)
Rewrote the `<thinking>` bullet. Was:

> Use thinking tags `<thinking>` for reasoning visibility

Now explicitly distinguishes `<thinking>` tags (prompt scaffolds that nudge CoT in the response body) from Anthropic's extended-thinking API surface (F-13, F-29). Notes that on Opus 4.7 with adaptive thinking, manual scaffolds may duplicate the model's own reasoning (F-26, F-29) and that the API lever should be preferred.

### EDIT 2 — Model-specific optimisation sub-section
New `## Model-specific optimisation — Claude Opus 4.7` block covers:
- Adaptive thinking is the only thinking-on mode on 4.7 (F-11); `budget_tokens` surface is gone.
- Effort levers `low / medium / high / xhigh / max` (F-15), with `xhigh` as the recommended default for coding/agentic workloads.
- Sampling guidance: defaults are calibrated; don't raise temp for tool-use or code-gen on 4.7; re-test legacy `temperature: 0` patterns before porting.

### EDIT 3 — Six Pattern 4.N sub-sections
Headings match regex `^### Pattern 4\.[1-6] — ` exactly (dogfood checked):
- Pattern 4.1 — Versioned Model Reference (F-01/F-03/F-04, provenance comment format)
- Pattern 4.2 — 4.7-Aware Role Prompt Skeleton (SKILL / TASK_TYPE / ROLE / ALIAS / … / SIGNAL BLOCK shape)
- Pattern 4.3 — Manual CoT Fallback (cross-refs F-29, F-13; when to prefer API lever)
- Pattern 4.4 — Calibrated Instruction Voicing (F-28, F-25; `CRITICAL:` reserved for irreversibles)
- Pattern 4.5 — Model-Specific Optimisation Sub-section (self-referential naming convention)
- Pattern 4.6 — SKILL.md Forward-Compatibility Header (ADR-006 three-field frontmatter)

Anchor slugs (`#pattern-4-1` through `#pattern-4-6`) are citable by name from sibling SKILL.md files.

### EDIT 4 — Frontmatter extension
Added three keys alongside existing `name` / `description` / `tools` / `model`:

```yaml
model_awareness: opus-4-7
last_audited: 2026-04-22
pattern_library_version: 4-7-1
```

### EDIT 5 — G-5 carry-over (research-agent/references/prompt-library.md:10)
Line actively taught `<thinking>` as "Pattern Used" — active teaching, not passing mention. Retargeted to cite Pattern 4.3 by name:

Was: `**Pattern Used:** Step-by-Step Analyzer with internal `<thinking>` reasoning`
Now: `**Pattern Used:** Step-by-Step Analyzer with Manual CoT Fallback scaffolding (see `prompt-engineer/SKILL.md#pattern-4-3`)`

Stops the duplication that §7.4 end-state grep would flag.

## Dogfood results

Step 6 — primary contract check:
```
test "$(grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md)" = "6" \
  && grep -q '^model_awareness: opus-4-7$' prompt-engineer/SKILL.md
```
Result: **DOGFOOD_PASS**. Exactly 6 Pattern 4.N headings present at lines 363, 373, 390, 399, 406, 410. Frontmatter `model_awareness: opus-4-7` present at line 6.

Step 7 — cross-repo `<thinking>` / chain-of-thought sweep outside prompt-engineer:
```
grep -rE '<thinking>|chain[- ]of[- ]thought' --include='SKILL.md' --exclude-dir=prompt-engineer .
```
One hit: `./mtg-commander/SKILL.md` — "challengers receive the primary's output artifact and intake params only — NEVER the primary's chain-of-thought."

Analysis: this is an in-passing reference describing a challenger-agent isolation protocol. It does NOT teach `<thinking>` usage and contains no pattern guidance. Per EDIT 5's conditional ("If the line merely mentions `<thinking>` in passing with no pattern guidance, leave it alone UNLESS doing so would break §7.4"), and since WI-05 scope named only `research-agent/references/prompt-library.md:10` as the G-5 carry-over target, I left mtg-commander alone. Flagging for potential follow-up if §7.4 end-state is defined to require zero matches across all SKILL.md files rather than zero pattern-teaching matches.

## Files touched

- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/prompt-engineer/SKILL.md` (440 → 520 LOC)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/research-agent/references/prompt-library.md` (1 line retargeted)

## Constraints honoured

- Existing prose-engineer SKILL.md content preserved — additions only plus the single PAT-01 bullet reframe.
- All six Pattern 4.N headings match the required regex exactly (dogfood verified).
- Sub-sections inserted as siblings under the existing Patterns section (between Multi-Perspective Analyzer and Prompt Evaluation Criteria), so the pattern library stays contiguous.
- Frontmatter preserves all existing keys (`name`, `description`, `tools`, `model`).

## Open items / follow-up for next agent

- mtg-commander/SKILL.md chain-of-thought reference (see Step 7 analysis). Not blocking WI-05; flag for scope owner if §7.4 policy requires zero matches globally.
- Cross-skill citations to Pattern 4.1–4.6 anchors are not yet authored in sibling skills — that's downstream WIs per ADR-005 citation-by-name strategy.

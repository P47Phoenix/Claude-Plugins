# AS-IS Use Cases — <system-name>

**Phase:** 1A Behavioral Reconstruction (PO-led)
**Run:** <run-id>
**Date:** <YYYY-MM-DD>
**Evidence roots:** <repo paths, test dirs, doc dirs, telemetry sources>
**Skip justification (only if Phase 1A skipped per FR-6):** <n/a or written justification>

---

## UC-<NN>: <short name>

- **actor:** <who initiates>
- **goal:** <what they are trying to achieve>
- **preconditions:** <state required before the flow>
- **main_flow:** <ordered steps of the happy path>
- **variations:** <alternate flows, error paths, edge cases>
- **confidence:** <high | medium | low>
- **evidence_citations:**
  - `<path/to/file>:<line>` — <what this evidence shows>
  - `<path/to/file>:<line>` — <what this evidence shows>

---

<!-- Repeat H2 block per use case. Minimum 5 per FR-2. ≥1 MUST carry confidence=low. -->

---

## Example (fully populated)

## UC-03: Register a new plugin in the marketplace

- **actor:** Plugin author
- **goal:** Publish a new plugin so it appears in the marketplace listing and is installable by end users.
- **preconditions:** Plugin directory exists with `SKILL.md`, `LICENSE.txt`, and conforms to kebab-case naming. Author has write access to the repo.
- **main_flow:**
  1. Author creates `<plugin-name>/` directory with required files.
  2. Author adds a new entry to `.claude-plugin/marketplace.json` with unique id, display name, description.
  3. Author opens a PR; CI validates marketplace.json shape.
  4. PR merges to main; plugin becomes discoverable.
- **variations:**
  - Duplicate id → CI rejects PR.
  - Missing `SKILL.md` → plugin loads but skill never triggers (silent failure; observed in issue #41).
  - Author registers without creating hooks/ dir → plugin installs but event automations absent.
- **confidence:** low (single commit reference, no tests)
- **evidence_citations:**
  - `.claude-plugin/marketplace.json:1` — registry file showing plugin entry schema in use
  - `CLAUDE.md:15` — documents the plugin directory contract
  - `research-agent/SKILL.md:1` — example of a conforming plugin entry point

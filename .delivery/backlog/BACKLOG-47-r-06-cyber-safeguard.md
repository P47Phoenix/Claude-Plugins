# BACKLOG-47-r-06-cyber-safeguard: Narrow cyber-safeguard refusal check for architect security/IR references

**Label:** backlog-47
**Status:** deferred
**Created:** 2026-04-22
**Engagement:** run-2026-04-22-4x7e
**Source anchors:**
- Challenger loop2 review Finding #3 (`.delivery/artifacts/02-refine/challenger/loop2/review.md`)
- PRD §6.1 Risk R-06 — "Cyber-safeguard refusals (F-22) unexpectedly bite a downstream skill user"
- 4.7 release notes F-22 — expanded cyber-safeguard refusal posture

## Context

Opus 4.7 ships with an expanded cyber-safeguard posture (F-22) that can refuse or hedge on prompts whose prose *reads* as offensive cyber content, even when the underlying intent is defensive. The Refine-stage challenger loop2 (Finding #3) flagged that the architect skill's security / incident-response / threat-modelling role references live at `delivery-team/skills/architect/` and are the most likely site for a false-positive refusal — the role outputs include attacker phrasings ("adversary goal," "threat actor capability") that the safeguard may misread.

R-06 in the PRD risk register rates likelihood low (the repo has no cyber-offensive skills, only defensive ones) and impact low, so the PRD explicitly made this a COULD-level, optional audit. The Architect was offered the opportunity to include a narrow prose-check note in REQ-02 keystone audit and chose **not** to (see ADR deferral). Hence this NEW-BACKLOG entry to preserve the finding.

## Proposed scope

- Produce a short prose-review checklist (≤10 items) for security / IR role reference files that flags phrasings likely to trigger cyber-safeguard refusals under 4.7 (adversary framing, exploit mechanics prose, offensive-tool naming).
- Grep-audit the architect security/IR references (`delivery-team/skills/architect/references/security*.md`, `incident-response*.md`, `threat-modelling*.md`) against the checklist.
- Reword flagged sections to defensive framing ("detection signature for X" rather than "how X exploits Y") without losing technical substance.
- Add a one-line note in the architect skill's `CLAUDE.md` or SKILL.md pointing to the checklist so future edits stay aligned.

## Out of scope for this item

- Changes to plugins/skills that do not carry security/IR role content.
- Building an automated safeguard-refusal test harness (possible future item but unnecessary at current scale).
- `mtg-commander` Challenger tone or any other adversarial-by-design plugin — those are intentional and safe.

## Success criteria

- The checklist exists and is reviewable.
- Every architect security/IR reference file has been audited against it, with a log of changes (or "no change needed").
- A dogfood run invoking the security architect role produces its artifact without safeguard refusal under 4.7.
- R-06 in the risk register can be downgraded to "mitigated."

## Priority & effort (rough)

- Priority: low
- T-shirt: S
- Depends on: nothing; can be done in isolation.

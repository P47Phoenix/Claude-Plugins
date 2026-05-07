---
title: "Release Notes — Caveman-Lite Prose Discipline (run-2026-05-05-tk3)"
stage: 07-uat
author: Bilbo Baggins (operations skill, tech-writer role)
created: 2026-05-05
pipeline_id: run-2026-05-05-tk3
initiative: SKILL-TOKEN-ECONOMY
wave: caveman-lite (Step 1 of 4-step completion plan)
predecessor: run-2026-05-05-tk2 (Wave 2, commit c2e7d5a)
closes: BACKLOG-102 (W2-1, W2-2, W2-3)
adr: ADR-tk3-001
supersedes: prior tk2 release-notes (2026-05-03)
---

# Release Notes — Caveman-Lite Prose Discipline

> "I don't know half of you half as well as I should like, and I like less than half of you half as well as you deserve."
> — Bilbo, at the long-expected party. Said with a wave of the hand, then on to the song.

This release applies caveman-lite prose discipline to delivery-team agent dispatches and DoD validator review files. The change ships as one consolidated story spanning three work items (W2-1 dispatch templates, W2-2 validator template, W2-3 `prose_style:` config key + schema bump v2.8 → v2.9). Twelve of thirteen acceptance criteria are structurally verified at merge; the thirteenth — telemetry-measured ≥20% response-prose token reduction — is empirically confirmed on the next full pipeline run after merge, by Story-1 design.

## What's new

A new top-level config key `prose_style:` (default `caveman-lite`) tells the delivery-flow orchestrator to inject a PROSE STYLE directive block into every agent dispatch prompt. Caveman-lite tightens narrative-framing prose (the prose between signal block and response end, plus signal block SUMMARY fields) and DoD validator verdict prose. Articles, hedging, and pleasantries are dropped; fragments are permitted; technical terms and code or error strings stay verbatim. Artifact bodies remain in standard prose — PRDs, ADRs, release notes, and this document itself.

Auto-clarity exemptions hold: security warnings, irreversible-operation confirmations (such as `git revert` or `rm -rf` prose), multi-step migration sequences, and user-clarification responses revert to standard prose even when caveman-lite is active. The exemption mechanism is a directive embedded in the PROSE STYLE block itself; the agent is the detector, per ADR-tk3-001 Element 3. Opt-out for any project is a one-line change: `prose_style: standard` in `.delivery/config.yml` reverts behavior cleanly without touching SKILL.md or the cache-prefix hash.

## Why

This wave executes Step 1 of the 4-step Skill Token-Economy completion plan tracked in `.delivery/memory/topics/skill-token-economy.md` and BACKLOG-102. Wave 2 (predecessor `run-2026-05-05-tk2`, commit c2e7d5a) reduced structural surface; this wave reduces narrative surface on every dispatch. Initiative ACs target ≥20% response-prose token reduction and ≥25% DoD review file size reduction with no DoD pass-rate regression against the 4/7 first-try baseline. Ruling 1 of the binding skill-token-economy decisions (cache-prefix freeze) gates the SKILL.md edit; ADR-tk3-001 owns the re-freeze procedure and documents the bounded one-time cache cost.

## For users / repo maintainers

If you want the new behavior, do nothing. Existing `.delivery/config.yml` files at v2.7 or v2.8 auto-migrate to v2.9 on the first post-merge pipeline invocation; the absent `prose_style:` key defaults to `caveman-lite` and a one-line upgrade banner is surfaced.

If you want the old behavior, add a single top-level line to `.delivery/config.yml`:

```yaml
prose_style: standard
```

That reverts dispatch behavior across every stage and every role for that project. No SKILL.md edit, no hash regeneration, no pipeline restart beyond the next dispatch.

## For pipeline operators

The cache-prefix hash flipped once with this merge:

| | SHA-256 of `delivery-team/skills/delivery-flow/SKILL.md` |
|---|---|
| Before | `9d4011d11e5b83321526c41ff79dd25c9186f4c659a745feb0c13f686205926f` |
| After | `f997ec25df5328329e431309f6dd6db948d354d5360dcb4c6ac409b8815a9eb9` |

On the first post-merge dispatch, the cache-warmup prefix slice (bytes 0..2048) is invalidated and re-read from disk — roughly 2 KB, one slice. Subsequent dispatches re-warm the cache normally; this is bounded and expected, not an alert. The `## Phase 0` heading remains anchored at byte 1803, unchanged from pre-edit; only bytes past 2048 within Phase 0 shifted. ADR-tk3-001 Element 5 documents the re-freeze math and reconciles the two coexisting interpretations (cache-warmup prefix slice and whole-file hash guard).

Verify cache-prefix integrity at any time:

```bash
python3 -c "import hashlib; \
  h = hashlib.sha256(open('delivery-team/skills/delivery-flow/SKILL.md','rb').read()).hexdigest(); \
  s = open('governance/cache-prefix-hash.txt').read().split()[0]; \
  print('OK' if h == s else f'MISMATCH got {h} want {s}')"
```

## Known carry-forwards (P1)

Initiative AC-1 (telemetry-measured ≥20% response-prose token reduction) is empirically pending. The W0-1 telemetry hook at `.delivery/telemetry/skill-loads.jsonl` already emits the substrate; Stage 6 dogfood deferred the runtime measurement to the next full pipeline run, by Story-1 design. The full measurement protocol is in PRD §8 (`.delivery/artifacts/02-refine/po/prd.md`).

If the next-run delta lands below 15%, BACKLOG-102's stop-rule fires: pause Tier-2 A/B (deferred to BACKLOG-103+) and run a root-cause retro before proceeding. The defects/story stop-rule (>0.4 across any rolling 3-PR window) is also armed; current rate is 0/13 across this run.

## Tier-A budget note

`delivery-flow/SKILL.md` lands at exactly 500 of 500 lines after this merge. Headroom is zero. Future SKILL.md edits in this orchestrator must batch a same-wave reduction elsewhere or carry an explicit `Budget-Exception:` ADR pointer. The verbatim PROSE STYLE block was extracted to `delivery-team/skills/delivery-flow/references/prose-style.md` to keep the orchestrator within ceiling; Step 4 of SKILL.md now references the canonical fixture rather than inlining it.

## References

- BACKLOG-102 — `.delivery/backlog/BACKLOG-102-caveman-prose-discipline.md`
- ADR-tk3-001 — `.delivery/artifacts/04-architect/adrs/ADR-tk3-001-prose-style-config.md`
- Idea brief — `.delivery/artifacts/01-idea/po/idea-brief.md`
- PRD — `.delivery/artifacts/02-refine/po/prd.md`
- Story 1 implementation report — `.delivery/artifacts/06-dev/developer/story-1-implementation.md`
- Binding decisions — `.delivery/memory/topics/skill-token-economy.md`
- Canonical PROSE STYLE fixture — `delivery-team/skills/delivery-flow/references/prose-style.md`
- Cache-prefix hash artifact — `governance/cache-prefix-hash.txt`
- Telemetry log — `.delivery/telemetry/skill-loads.jsonl`

## Credits

Aragorn (PO, Idea) · Gandalf (PO, Refine) · Saruman of Many Colours (Architect) · Frodo (PO, Plan) · Gimli (Developer) · Sam (DevOps) · Legolas (QA) · Bilbo (Tech-Writer)

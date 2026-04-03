# Product Owner Review -- Idea Brief (Gate 1)

**Reviewer**: Product Owner (Gandalf)
**Date**: 2026-04-01
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Verdict**: DONE

---

## Criteria Evaluation

### [PASS] [blocking] Problem statement present and specific

Four distinct failure modes named with concrete evidence: popularity-driven aggregators (EDHREC solves the wrong problem), manual building cost (4-8 hours for a skilled player, inaccessible to newer players), AI hallucination of card names and rules ignorance, and budget as an afterthought rather than a shaping constraint. Each problem references observable system behavior, not vague dissatisfaction. The core philosophy -- synergy first, popularity as tiebreaker only -- is stated explicitly and threaded through every subsequent section. No ambiguity in what is broken or why.

### [PASS] [blocking] Target users identified

Four personas defined with experience level, primary need, and key constraint:
1. Experienced player exploring a new commander (time-constrained)
2. New-to-Commander player (knowledge gap on structural requirements)
3. Budget-conscious brewer at any level ($50-200 range where substitution quality matters)
4. Returning player with outdated assumptions (card pool currency gap)

Personas are distinct and non-overlapping in their primary constraint. Each maps cleanly to at least one pipeline agent's value proposition. Sufficient to validate against during UAT.

### [PASS] [blocking] Goals present and measurable

Six goals, all verifiable:
1. Format-legal 100-card decklists -- binary pass/fail via Rules Judge (exactly 100 cards, color identity, banned list, singleton, no hallucinated names).
2. Synergy-first selection -- every non-land card interacts with 3+ other cards. Countable by the Optimization Reviewer.
3. Structural minimums by power level -- 10+ ramp, 10+ draw, removal suite, calibrated land count. Countable.
4. Budget compliance with real pricing -- total and per-card caps enforced via Scryfall data. Verifiable against API responses.
5. Single-session completion -- user provides intake, receives finished decklist. Observable.
6. Valid Claude Code plugin -- registered in marketplace.json, follows conventions. Checkable by inspection.

No goal requires subjective judgment to evaluate. Goal 3's "may flex with power level" is appropriately hedged -- the flex targets will be defined during Refine, which is the right stage for that precision.

### [PASS] [warning] Scope clear (IN and OUT)

IN scope is an 8-item table covering plugin skeleton, 4 agents, Card Finder utility, reference files, and 3 named test cases. OUT scope defers 8 items (Recommander, EDHREC, multi-source pricing, platform export, deck modification mode, SQLite cache, hooks, meta-game analysis) with stated reasons for each deferral.

The v1/v2 boundary is clean: Scryfall API alone for v1, additional data sources in v2. The dependency decision is explicit and principled -- minimum viable external dependency.

One observation (non-blocking): the agent architecture section (Section 3) goes deeper into implementation than typical for an idea brief -- directory structure, component mapping, pipeline flow. This is not a problem; it simply means the Architect stage has a head start. The Refine stage should treat these as proposed, not decided.

---

## Summary

This brief defines a well-scoped GREENFIELD plugin with a clear problem (Commander deck building is a multi-constraint optimization problem that existing tools solve poorly), specific users (four personas with distinct constraints), measurable goals (six, all verifiable without subjective judgment), and bounded scope (v1 builds on Scryfall alone, v2 adds integrations).

The synergy-first philosophy is not just stated -- it is encoded into the agent architecture (Optimization Reviewer gates on 3+ interactions per card) and the goals (Goal 2). This is a brief that knows what it believes and builds accordingly.

A wizard arrives precisely when he means to -- and this brief knows precisely what it means to build.

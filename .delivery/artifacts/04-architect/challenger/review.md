# Challenger Review — Transformation Plan (Opus 4.6 → 4.7)

**Artifact:** Adversarial Review of `.delivery/artifacts/04-architect/solution/transformation-plan.md`
**Stage:** 4 / Architect — adversarial gate
**Date:** 2026-04-20
**Reviewer:** fresh Challenger, no prior context on this plan
**Inputs read:** transformation-plan.md (1→528), PRD rev 1 (1→583), scope-baseline.md (1→191), ADR-001/002/003/004/005/006 (all), `.delivery/config.yml` (dod_validators block, parallel_validators key), `delivery-team/skills/delivery-flow/SKILL.md` lines 320–375 (DISP-01 verified at 328–345)
**External spot-checks:** `https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7` (live fetch), `https://platform.claude.com/docs/en/about-claude/models/migration-guide` (live fetch)

---

## TL;DR

The plan is unusually evidence-dense: it anchors every wave to a PRD REQ, every REQ to a cited finding, and every finding to an Anthropic URL that I independently re-verified today. The "what stays / what changes" triage is honest, the scope terminus is held, and the baseline-before-edit discipline is real. I looked hard for hidden coupling, sequencing traps, and scope drift and found mostly small ones.

The structural concerns that remain are:

1. **ADR-006 is accepted-contingent on a research spike (WI-03) that has not run yet.** If the spike fails, the *accepted-already* decision has to be undone across every frontmatter edit in Waves 2–4. That is not a fatal defect — Option B is documented — but a decision with an open empirical pre-requisite should not be labelled "Accepted" in the same artifact that schedules the check.
2. **WI-06's "≥2 WebFetch calls AND ≥2 distinct hostnames" gate has no hook or telemetry infrastructure yet.** The plan says "measured via Claude Code run log / transcript" but no hook under `delivery-team/hooks/` reads tool-use events from sub-agent transcripts. This is borderline "spot-check and see if it looks right" for an AC-hardened-by-loop-2 gate.
3. **ADR-005's centralised-library choice has no explicit exit ramp** for a plugin (e.g., `mtg-commander`'s Challenger tone) whose 4.7-sensitive guidance is intrinsically plugin-local. The ADR waves at this with "pattern body lives in `prompt-engineer/`; plugin-specific instantiation lives in the plugin's own SKILL.md" but does not say what happens when the instantiation *is* the pattern.

Confidence **4/5**. Proceed with the three caveats above noted in the implementation engagement kickoff; revisions are recommended but not blocking.

---

## Confidence + Justification

**Confidence: 4/5 — Minor concerns, proceed with noted caveats.**

Reasons for not shipping (4, not 5):

- ADR-006 status mismatch (see Finding #1): an "Accepted" ADR whose viability depends on an unexecuted spike is a process smell, even though the contingency (Option B) is already documented.
- WI-06 measurement mechanics underspecified (see Finding #2).
- One quiet scope expansion around alias themes (see Finding #4) that should be explicit.

Reasons for not requiring rework (4, not 3):

- Every load-bearing Opus 4.7 claim I spot-checked matched the live Anthropic docs exactly (see Citation Spot-Check).
- The plan correctly surfaces its own weakest ADR (ADR-006) with an explicit contingency and sequences the spike in Wave 1.
- Dogfood-before-edit is applied consistently: WI-06, WI-09, WI-12 are all "no-edit unless regression."
- Sequencing is defensible: WI-05 (pattern library) gates the citation edits, REQ-10 (baseline) gates the delta metrics, REQ-09 (AS-IS count) gates the dispatch-annotation edit. Dependencies form a DAG without cycles.
- Scope terminus is honest: Section 1 names the end-state as the roadmap, not a PR.

---

## Findings Table

| # | Category | Finding | Blast-radius | Fix |
|---|---|---|---|---|
| F-C-01 | ADR fragility | **ADR-006 is the most fragile decision.** Status is "Accepted (contingent on NDOC-02 spike)" — but the spike is WI-03, not yet executed. If `grep -L "model_awareness:" **/SKILL.md` strict-validates on the 4.7 Skill tool contract (historical behaviour says no, but no one has re-verified), every frontmatter edit in Waves 2, 3, and 4 has to be re-authored as HTML comment blocks. That is ~17 files × 3 fields × 2 edit-passes if re-done mid-wave. | **Medium-wide.** Touches every keystone PR and the WI-11 backfill PR. Reversible but costly. | Downgrade ADR-006 status to "Proposed" until WI-03 completes. Or, less invasively, add a sentence to §6.1 WI-03 making it an explicit **Wave-1 gate**: "Wave 2 MUST NOT start until WI-03 verdict is recorded in `.delivery/artifacts/<impl-run>/research/ndoc-02-spike.md`." The plan implies this via §7.1 wording but does not say it in WI-03's own ACs. |
| F-C-02 | Empirical weakness | **WI-06's ≥2-hostnames gate has no measurement infrastructure.** The acceptance criterion (AC-03B.2 hardened) says "measured via Claude Code run log / transcript," but `delivery-team/hooks/` has zero hooks that count tool-use events per sub-agent. `verify_skill_load.py` checks for SKILL_LOADED signal; `flag_empirical_validation.py` flags runtime-only ACs. Neither emits a tool-call count. The implementer will end up manually reading the transcript and eyeballing the URLs — which is exactly the "spot-check and see if it looks right" failure mode the dogfooding rule warns against. | **Medium.** Affects only WI-06 directly, but WI-06 is the *only* gate that catches the grep-invisible F-07 (reason-instead-of-fetch) regression. Silent failure is the risk. | Either: (a) add a "transcript parsing script" deliverable inside WI-06 (a few lines of Python that regex-counts `WebFetch(`/`WebSearch(` calls in the sub-agent transcript and emits a JSON summary at `.delivery/artifacts/<impl-run>/observability/research-probe.json`), OR (b) name the existing SubagentStop hook extension as the measurement vehicle and log a backlog to add tool-use counting to it. The WI should not ship with "measured manually" as the implicit plan. |
| F-C-03 | Scope creep | **WI-12 "tone-strengthening of the affected theme YAML" is scope-creep-shaped.** REQ-05 / AC-05.2 says tone-strengthening of the affected theme YAML *only* if the dogfood reveals regression. WI-12 restates this faithfully. But the size of "targeted tone-strengthening" is unbounded — a failing theme could require editing `catchphrase` + all `examples` across 6+ roles × 1 theme = up to ~30 lines of prose in the worst case, and that prose has to pass its own tone judgement, implying a second dogfood sub-loop that isn't sequenced. | **Low** if no theme regresses (M-05 ≥80% target likely). **Medium** if even one theme regresses — the remediation is unscheduled. | Add an explicit "if regression" sub-flow in WI-12: "On fail, remediation PR must (a) target only the failing theme, (b) be dogfood-re-tested before merge, (c) not exceed N lines-changed without explicit Architect sign-off." Bound the failure blast radius. |
| F-C-04 | Hidden coupling | **WI-04, WI-07, WI-08 all cite "Pattern 4.2 by name" — but Pattern 4.2's exact markdown anchor is authored inside WI-05.** If WI-05's Wave-2 edit lands with a slightly different heading text (e.g., "Pattern 4.2 — Role Prompt Skeleton" vs "Pattern 4.2 — 4.7-Aware Role Prompt Skeleton"), the markdown anchor slug changes and every citation in WI-04/WI-07/WI-08 breaks silently (GitHub renders the link but it scrolls to nothing). The plan notes "stable anchor" but a stable anchor is a *convention*, not a fact until WI-05 commits. | **Low-to-medium.** Cosmetic failure mode (broken anchors) but no runtime impact. Caught by DX-M3 grep only if the grep includes anchor-resolution. | Add to WI-05 ACs: "The six Pattern headings are listed verbatim in the commit message; any downstream WI that cites by anchor MUST match the verbatim heading." Or alternatively, adopt stable HTML anchor IDs (`<a id="pattern-4-2"></a>`) in WI-05 and cite those, decoupling citation syntax from heading wording. |
| F-C-05 | Risk-mitigation gap | **ARCH-R5 (late-discovered regression in un-exercised stages) mitigation is gestural.** The mitigation row says "WI-04 dogfood covers FEATURE + DESIGN; Wave 4 dogfoods add adversarial-heavy" and then references "PRD R-08 + Contingency section with TBD-CONTINGENCY-01." But the transformation plan itself has no "Contingency — Dogfood Findings" section with a placeholder ID — that is a PRD artifact (PRD §6.1 R-08). The Architect's plan cites it rather than carrying it. A reader of the plan alone (e.g., the impl-run PO) would need to cross-reference the PRD to know what to do when a dogfood finds a Plan / Development / UAT stage regression. | **Medium.** Silent until a late-stage dogfood fails, then creates a re-plan scramble. | Add a short §6.4 "Contingency — Late-Discovered Regression" to the plan itself, carrying a TBD-CONTINGENCY-01 placeholder WI shape (what artifact, what ACs, which wave to insert into). Two paragraphs. The plan becomes self-contained. |
| F-C-06 | Pattern library landmine | **ADR-005 does not name an exit ramp for plugin-local patterns.** If `mtg-commander`'s Challenger tone turns out to want its own 4.7-era pattern (e.g., a Challenger-specific "concrete-alternatives voicing" sub-pattern surfaced by WI-09's dogfood), ADR-005's rule is "pattern body in `prompt-engineer/`; instantiation local." But a Challenger-specific voicing pattern *is* plugin-local in semantics and only its abstraction generalises. The ADR's "mitigation: Pattern body lives in `prompt-engineer/`; plugin-specific instantiation lives in the plugin's own SKILL.md with a citation" is a principle without a worked example. If/when it gets exercised, the author has to invent the split. | **Low** during this engagement (six named patterns are all cross-plugin general). **Medium-wide** long-term (the next migration may surface plugin-specific patterns and will re-open ADR-005). | Add one worked example to ADR-005 Implementation Notes: "Scenario: mtg-commander surfaces a Challenger-specific voicing pattern. Treatment: the abstract pattern (e.g., 'calibrated-confrontation voicing') goes into `prompt-engineer/SKILL.md` as Pattern 4.N; the plugin-local invocation example lives inline in `mtg-commander/SKILL.md` and cites by anchor." Tiny addition; large future-proofing gain. |
| F-C-07 | Sequencing trap | **WI-13's backlog registration depends only on WI-02 (baseline) but is fenced into Wave 4.** The WI-13 dependencies column says `WI-02`, yet the wave assignment is 4. Nothing in Wave 3 creates content that WI-13 needs. This is a minor inefficiency: WI-13 could land in Wave 1 alongside WI-02 (both are capture/registration items, both are XS, neither edits code). Fencing backlog registration to Wave 4 delays explicit scope declarations that exist today (task_budget, memory tool, caching, SDK-wiring, etc.) until after every prose edit — inverting the "declare scope first, then execute" discipline the plan otherwise upholds. | **Low.** Cosmetic — the backlog items all land eventually. | Either move WI-13 to Wave 1 (XS, parallelisable with WI-02), OR split it: "WI-13a (Wave 1): pre-declared backlog items [task_budget, memory, caching, SDK-wiring]. WI-13b (Wave 4): post-audit backlog items [over-pressure audit deferral, Galadriel on-ramp artifacts]." The second half legitimately depends on Wave 3's audit outputs. The first half does not. |
| F-C-08 | Scope shrink | **The 11 non-keystone SKILL.md files receive frontmatter-only edits (WI-11) with no prose review.** The plan is honest about this: `last_audited` is set "with a note 'frontmatter-only; no prose review performed.'" But that means 11 / 17 skill files get stamped `model_awareness: opus-4-7` without any human actually verifying the prose holds up on 4.7. Under F-25 (more literal instruction following), one of those 11 could easily harbour an inferred instruction that breaks on 4.7 — and the stamp would be technically false. | **Medium.** The stamp is a claim; the claim is untested for 65% of the surface. The DX-M1 "time-to-triage" metric becomes actively misleading if the stamp is unreliable. | Either (a) tighten `model_awareness`'s definition so "opus-4-7" means "reviewed against 4.7" and the 11 backfills get `model_awareness: opus-4-7-frontmatter-only` (honest), OR (b) add a WI-11a "quick prose skim" for the 11 files — 30-min per file max, just looking for F-25 landmines — and only stamp full `opus-4-7` after that. Current plan optimises for zero-cost backfill at the cost of stamp accuracy. |
| F-C-09 | Empirical weakness (low) | **DX-M1 "time-to-triage ≤10 seconds" is measured "informally on two-reader walkthrough."** For a metric called out in the success-metrics table, "informally on two-reader walkthrough" is exactly the spot-check failure mode. This is a smaller instance of F-C-02. | **Low.** DX-M1 is a DX nicety, not a correctness gate. | Downgrade DX-M1 to a qualitative observation ("readers report fast triage") or replace the metric with a falsifiable proxy ("`grep -c 'model_awareness:' <file>` returns 1 and the line is within the first 10 lines of the file"). Don't carry a time-measured metric with no stopwatch. |
| F-C-10 | Hidden coupling (minor) | **ADR-002 names the canonical Haiku dated ID as `claude-haiku-4-5-20251001` but the plan's M-01 regex explicitly excludes this string from its stale-ID sweep.** That is correct behaviour (the current Haiku dated ID should not match the stale-regex). But WI-10's AC-01.3 says MID-02 substitution likely targets `claude-haiku-4-5-20251001`. If Anthropic retires that dated ID between plan authoring and impl execution (the plan is a "2–4 week gap" per ARCH-R2), the substitution lands a freshly-stale ID that the M-01 regex *no longer excludes*. The mitigation (ARCH-R2 doc-delta-check) mentions this generically but doesn't name the Haiku dated ID specifically. | **Low.** Unlikely given Anthropic's typical retirement cadence, but the plan's own `ARCH-R2` scenario is the trigger. | Add to WI-10 AC-01.3: "Before substitution, re-verify the target Haiku ID against `https://platform.claude.com/docs/en/about-claude/models/overview` and update the M-01 allowlist atomically with the substitution." One-sentence fix. |

---

## Citation Spot-Check

I verified every claim the plan treats as load-bearing by fetching the live Anthropic docs today (2026-04-20).

| Claim | Plan anchor | Verified at live URL | Verdict |
|---|---|---|---|
| Canonical API model ID is `claude-opus-4-7` | PRD F-01, plan §2.2 | `whats-new-claude-4-7`: *"Claude Opus 4.7 \| API model ID: `claude-opus-4-7`"* | **CONFIRMED** exact string match. |
| `thinking: {"type": "enabled", "budget_tokens": N}` returns 400 | PRD F-11, ADR-003 Context | `whats-new-claude-4-7`: *"Setting `thinking: {"type": "enabled", "budget_tokens": N}` will return a 400 error. Adaptive thinking is the only thinking-on mode"* | **CONFIRMED** verbatim. |
| Adaptive thinking is OFF by default on 4.7 | PRD F-12, ADR-003 Context | `whats-new-claude-4-7`: *"Adaptive thinking is **off by default** on Claude Opus 4.7. Requests with no `thinking` field run without thinking."* | **CONFIRMED** verbatim. |
| New `xhigh` effort level exists | PRD F-15 | `whats-new-claude-4-7`: *"Start with the new `xhigh` effort level for coding and agentic use cases"* | **CONFIRMED**. |
| "Fewer subagents spawned by default. Steerable through prompting." | PRD F-08, ADR-001 | `whats-new-claude-4-7`: *"**Fewer subagents spawned by default.** Steerable through prompting."* | **CONFIRMED** verbatim — exactly the text F-08 quotes. This is the most load-bearing claim in the plan (drives REQ-03, REQ-09, WI-04, ARCH-R5, R-02, R-09). Confirmation is strong. |
| "Fewer tool calls by default, using reasoning more." | PRD F-07, REQ-03B | `whats-new-claude-4-7`: *"**Fewer tool calls by default,** using reasoning more. Raising effort increases tool usage."* | **CONFIRMED** verbatim. |
| `temperature`/`top_p`/`top_k` non-default = 400 | PRD §2.10, REQ-02 AC-02.2 | `whats-new-claude-4-7`: *"Starting with Claude Opus 4.7, setting `temperature`, `top_p`, or `top_k` to any non-default value will return a 400 error."* | **CONFIRMED**. |
| Tokenizer shift ~1.0–1.35x | PRD F-21, Constraint 9 | `whats-new-claude-4-7`: *"This new tokenizer may use roughly 1x to 1.35x as many tokens"* | **CONFIRMED**. |

Additionally verified against repo state:

- **`.delivery/config.yml` `dod_validators` key exists** with exactly the stage-count expectations the plan names: idea=2, refine=4, design=5, architect=5, plan=5, development=4, uat=4. (Confirmed by direct file read.)
- **`parallel_validators: true`** is indeed a boolean, not a count. (Confirmed at config line 49.)
- **DISP-01 prose location** at `delivery-team/skills/delivery-flow/SKILL.md` lines 328–345 matches the plan's line citations exactly.
- **Zero `import anthropic` / `from anthropic`** under `agentic-flow-builder/` and `prd-quality-gate-flow/` (grep confirmed). Section 3.1.1's SDK-import claim holds; R-05 downgrade and ADR-002 "direct strings" decision are both well-founded.
- **13 theme YAML files** exist at `delivery-team/skills/delivery-flow/references/aliases/` (matches plan's DEV-02-corrected path exactly).

No claim I spot-checked was wrong. No fabricated quotes, no stale doc references.

---

## Top 3 Priority Concerns

In decreasing order of "might sting the impl run if ignored":

### 1. ADR-006 "Accepted (contingent)" status — turn into a true Wave-1 gate

**Why it's top:** ADR-006 touches every SKILL.md in the repo. The fallback (Option B HTML comments) is documented but would require re-authoring every frontmatter edit in Waves 2–4 if WI-03's spike fails. A contingent acceptance should not be conflated with an executed decision.

**Concrete fix:** Amend WI-03 acceptance criterion to: "Wave 2 MUST NOT start until this spike's verdict file is present at `.delivery/artifacts/<impl-run>/research/ndoc-02-spike.md` AND the verdict is 'Option A proceed' OR Wave 2/3/4 WIs are amended to Option B syntax before dispatch." Downgrade ADR-006 status from "Accepted (contingent)" to "Proposed (pending WI-03)." One-sentence edits. Process hygiene.

### 2. WI-06's research-agent tool-use probe needs a measurement script, not an eyeball

**Why it's second:** WI-06 is the single gate that catches the grep-invisible F-07 regression (research-agent reasons instead of fetches). Its AC is hardened (≥2 calls AND ≥2 hostnames). But the measurement approach in the plan reduces to "read the transcript and count" — a manual spot-check in a plan that correctly insists elsewhere on dogfood-with-evidence.

**Concrete fix:** Add a measurement-deliverable to WI-06: a small Python script (live at `.delivery/artifacts/<impl-run>/observability/research-probe.py` or similar) that regex-counts WebFetch/WebSearch invocations in the sub-agent transcript and emits a JSON summary. Without it, the "hardened" AC is softer than the PRD rev-1 challenger-loop-2 hardening intended.

### 3. WI-11's frontmatter backfill stamps 65% of SKILL files `opus-4-7` without prose review

**Why it's third:** The plan is honest about this (the `last_audited` note says "frontmatter-only; no prose review performed"), but the `model_awareness: opus-4-7` stamp is a claim that will outlive the note. A reader in six months who greps for "4.7-ready" files gets 17 hits, 11 of which are unverified. That undermines the entire DX-M1 scannable-triage value prop.

**Concrete fix:** Either weaken the 11 backfill stamps to `model_awareness: opus-4-7-frontmatter-only` (or equivalent honest tag), OR add a lightweight prose skim to WI-11 — 30 minutes per file, looking only for F-25 landmines (inferred instructions, over-pressed language) — before stamping. The current plan optimises for zero-cost backfill at the cost of downstream trust in the marker.

---

## Adversarial Check Summary (per prompt's 8 checks)

| # | Check | Verdict |
|---|---|---|
| 1 | ADR fragility | **ADR-006** is the most vulnerable (contingent acceptance, unexecuted spike). See F-C-01. |
| 2 | Sequencing traps | Minor: WI-13 could move to Wave 1; pattern-anchor citations (WI-04/07/08 → WI-05) depend on WI-05 heading text stability. See F-C-04, F-C-07. |
| 3 | Scope creep | WI-12's theme-YAML remediation is unbounded on regression. See F-C-03. |
| 4 | Scope shrink | 11/17 SKILL.md files get stamped without prose review (WI-11). See F-C-08. |
| 5 | Empirical weakness | WI-06 transcript-parsing, DX-M1 "informal walkthrough." See F-C-02, F-C-09. |
| 6 | Hidden coupling | Pattern-library anchor syntax couples WI-04/07/08/09 to WI-05's heading text. Haiku-canonical-ID couples WI-10 AC-01.3 to Anthropic's retirement cadence. See F-C-04, F-C-10. |
| 7 | Risk-mitigation gap | ARCH-R5 (late-stage regression) points to a PRD section rather than carrying the contingency section in the plan itself. See F-C-05. |
| 8 | Pattern library landmine | ADR-005 has no worked example for plugin-local patterns that are not cross-plugin general. See F-C-06. |

---

## What I Looked For and Did Not Find

(Documenting absence so the next reviewer doesn't re-hunt.)

- **Fabricated quotes from Anthropic docs.** Every quoted Anthropic string I spot-checked is verbatim.
- **Stale or wrong line numbers.** DISP-01 at 328–345 is accurate. The 17 SKILL.md file list and 13 theme YAMLs all exist at the named paths.
- **Undocumented dependency cycles.** Wave graph is a clean DAG.
- **Net-new scope hiding as migration.** Task budgets, memory tool, prompt caching, SDK wiring are all explicitly backlog (REQ-07, ADR-004), each logged as `BACKLOG-47-*.md`.
- **Broken config assumptions.** `dod_validators.<stage>` list lengths match the plan's expected counts exactly in the live config.
- **"NEVER" / "CRITICAL" overload inside the plan itself.** The plan uses calibrated voicing throughout.
- **Collision with PRD non-goals.** Plan explicitly lists the frozen boundaries and does not cross them.

---

*"The plan holds. The keystones are the right six. The four waves fit the dogfood rule. What I name above is the cracks in the mortar, not in the stones themselves — fillable without un-forging anything."*

— Challenger (fresh; no alias)

---

**End of Challenger review.**

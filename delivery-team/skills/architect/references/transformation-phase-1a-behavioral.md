# Transformation Phase 1A — Behavioral Reconstruction (PO-led)

*By Gimli son of Glóin. Aye — before ye map the Mountain, ye must ken why folk ever delved it.*

## 1. Purpose

Phase 1A reconstructs **behavioral** use cases of a legacy system from codebase evidence. It is **PO-led** but cross-skill: the Architect is the downstream consumer in Phase 1B. Without Phase 1A, Phase 1B is a structural map of unknown territory — boxes and arrows with no story for what the system is *for*.

Output is the canonical AS-IS use-case artifact that every later transformation phase references.

## 2. Evidence sources

The PO reconstructs use cases only from **cited** evidence. Acceptable sources, in rough order of strength:

1. **Integration and end-to-end tests** — the strongest signal; a passing e2e test *is* a use case, contract-bound.
2. **CLI commands** — entry points to real workflows; argument surface reveals actors and variations.
3. **API endpoints** — route definitions, handler names, request/response schemas.
4. **UI strings** — button labels, form headings, menu items in the rendered UI.
5. **README / user-facing docs** — intended flows, where not contradicted by code.
6. **Commit messages** — why features were added; reveals historical intent of murky code paths.
7. **Issue / ticket history** — bugs, feature requests; the shape of the issue backlog hints at what users actually do.
8. **Telemetry** — event logs, feature-usage counters, dashboards (if available).
9. **Existing stale docs** — usable only as a hypothesis to confirm from stronger sources; never as sole citation.

If no evidence exists for a claim, the claim does not belong in Phase 1A.

## 3. Use-case schema (verbatim)

Every use case MUST carry these fields:

```yaml
- actor: <who initiates>
  goal: <what they want>
  preconditions: <what must be true before>
  main_flow: <numbered steps>
  variations: <alternate / exception flows>
  confidence: high | medium | low
  evidence_citations:
    - path: <file path in repo>
      what_it_shows: <one line — why this file proves the use case>
    - path: ...
      what_it_shows: ...
```

## 4. Confidence level rules

- **high** — ≥3 evidence sources converge on the same use case (e.g., an e2e test + an API endpoint + a README section all describe the same flow).
- **medium** — 1-2 sources, or partial evidence (the flow exists but variations or preconditions are inferred).
- **low** — inferred from context, a single weak source (e.g., stale docs only), or explicit gap-fill where the PO believes a use case exists but the evidence is thin.

**Required floor:** every reconstruction MUST contain ≥1 `confidence: low` entry. This is an honesty forcing function. A legacy-system reconstruction with *all* high-confidence entries is lying: it either skipped hard cases or laundered inference as certainty. If the PO cannot find a single legitimately-low-confidence use case, the PO is not looking hard enough.

## 5. Legacy trigger rule

Phase 1A is **REQUIRED** by default for any `transformation-planning` invocation. It may be skipped only if:

- **(a)** The PO explicitly asserts trusted existing use-case documentation exists for the target system and cites its location, OR
- **(b)** The target system has authoritative behavioral documentation that is younger than **6 months**.

Default is RUN. Skipping requires a written justification in the header of the (empty or stub) artifact, naming the trusted source and its date. Unjustified skips fail FR-6.

## 6. Authoring workflow

1. **Sweep evidence sources** (§2) — enumerate what exists in the target repo before writing any use case.
2. **Cluster evidence** — group files that describe the same user-facing behavior.
3. **One use case per evidence cluster** — do not invent use cases outside the clusters; do not merge clusters that touch different actors or goals.
4. **Assign confidence honestly** per §4, including the mandatory ≥1 low.
5. **Cite evidence per use case** — every entry MUST have ≥1 `evidence_citations` row with a non-empty `what_it_shows`.
6. **Write the artifact** to the path in §8.

## 7. MAR review trio

Phase 1A output is reviewed by a three-persona Multi-perspective Adversarial Review trio. This is the **second instantiation** of the configurable architecture-board pattern shipped in BACKLOG-003 — no new collaboration pattern is introduced. See `delivery-team/skills/delivery-flow/references/architecture-board-personas.md` for the pattern mechanics; the three personas below are Phase 1A-specific.

### Code Archaeologist

- **perspective:** Evidence-bound skeptic. Every confident claim must be anchored to a file on disk.
- **challenge question:** *"What is the single test or endpoint definition that proves this use case exists in the system **today**?"*
- **fails the review when:** a `confidence: high` entry rests on inference or stale docs; an entry's `evidence_citations` are thin or off-topic.

### User Advocate

- **perspective:** End-user outcome lens. Filters infrastructure noise from real user-visible behavior.
- **challenge question:** *"Would an actual end user care about this, or is it internal plumbing dressed up as a use case?"*
- **fails the review when:** a use case describes a cron job, migration script, or internal RPC that no human actor initiates or observes.

### Skeptical Tester

- **perspective:** Can a failing-then-passing regression test be written against this use case **as stated**?
- **challenge question:** *"Write me the test name and the assertion. If you can't, the use case needs more evidence or lower confidence."*
- **fails the review when:** `preconditions` or `variations` are too vague to assert against; main_flow steps are observations, not checkable actions.

Trio verdict feeds the judge persona per the standard board protocol. On BLOCK, the PO corrects Phase 1A and re-runs review before Phase 1B may start.

## 8. Output location

`.delivery/artifacts/08-transform/as-is-use-cases.md`

Outside a pipeline run, use `transform/as-is-use-cases.md` in the standalone namespace.

## 9. Minimum bar

A Phase 1A artifact is not acceptable unless ALL of:

- ≥5 use cases
- ≥1 `confidence: low` entry
- `evidence_citations` present and non-empty on **every** entry
- Every field in the §3 schema filled (no placeholders)
- MAR trio review file exists and carries a non-BLOCK judge verdict

## 10. Anti-patterns

- **Hallucinated use cases** — no citation, or citations that do not show what the `what_it_shows` claims.
- **High-confidence floor** — everything marked `high` so the PO doesn't have to defend any weak spots. Forbidden per §4.
- **Evidence-free claims** — preconditions or variations asserted without a source.
- **Scope drift into TO-BE** — describing what the system *should* do. Phase 1A is strictly descriptive; Phase 2 is where "should" begins.
- **Infrastructure masquerading as behavior** — a use case whose actor is "the scheduler" or "the deploy pipeline" is plumbing, not user behavior.

*"An axe honest about its nicks is worth two pretending to be new."* — Gimli

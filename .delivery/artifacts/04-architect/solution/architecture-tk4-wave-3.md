<!-- run: run-2026-05-09-tk4 | stage: 4 (Architect, light) | wave: 3 — closure | author: Saruman of Many Colours, Solution Architect -->

# Architecture — Wave 3 (`run-2026-05-09-tk4`)

*Saruman of Many Colours, Solution Architect. Three ADRs, one road, one summary.*

## Engagement

- **Pipeline**: `run-2026-05-09-tk4` — Wave 3, the close-out wave for the delivery-team skill token-economy initiative.
- **Authoritative inputs**: Stage 1 brief (`.delivery/artifacts/01-idea/po/idea-brief.md`) → Stage 2 PRD (`.delivery/artifacts/02-refine/po/prd.md`) → BACKLOG-104.
- **Stage 4 depth**: light — three ADRs, one summary, no design artifact (no UI surface; project type is FEATURE-execution-of-pre-planned-waves).
- **Binding decisions**: `.delivery/memory/topics/skill-token-economy.md` (5 rulings; not re-litigated).

## ADR Index

| ADR | Title | Status | One-line summary |
|---|---|---|---|
| ADR-tk4-001 | Tier-B/C closure approach | Accepted | Per-file extraction strategy with explicit batching math; 7 files closed via reference splits (architect 500→288, presentation 545→~160, ui 496→273, operations 420→255, quality 418→276, user-feedback 399→250, godot 236→**197** [round-2: deepened from 198 so post-frontmatter +3 holds Tier-C ceiling EXACTLY at 200]); honest partial-compliance reserve cited for architect (worst-case 311). |
| ADR-tk4-002 | Paradigm sub-skill pattern contract | Accepted | Canonical `<plugin>/skills/<axis>/<variant>/SKILL.md` shape with `disable-model-invocation: true` for ≥3-mutually-exclusive-variant axes; applied to research-agent (5 types) and user-feedback (4 persona families); presentation conditional on Stage 6 measurement. |
| ADR-tk4-003 | Governance frontmatter + cumulative cache-prefix re-freeze | Accepted | 3 new keys (`maintainer:`, `fitness_review_due:`, `context_budget:`) on all 13 delivery-team SKILL.md; one-time ~26KB cold-cache re-warm cost accepted; Dev runs-the-command at DoD per cache-prefix-impacting binding. |

## System Boundary Diagram

```
[Wave 3 sequencing — strict]
                                                                      
  Story 1 (W3-1) ─┐                                                   
                  │                                                   
  Story 2 (W3-2..4) ─┐                                                
                     │                                                
  Story 3 (W3-5..7) ─┤── PER-FILE EXTRACTION via ADR-tk4-001 ─────┐  
                     │   (no cache-prefix impact;                  │  
                     │    extractions land at line ≥111 in         │  
  Story 4 (W3-8) ────┘    every file, below frontmatter region)    │  
                                                                   │  
  ┌────────────────────────────────────────────────────────────────┘  
  │                                                                   
  ▼                                                                   
  REFERENCE FILES CREATED                                             
  (references/roles/, references/contracts/, references/types/,       
   references/formats/, skills/<axis>/<variant>/ for paradigm axes)   
                                                                      
                                                                      
  ───── HARD GATE — Stories 1–4 must land in working tree first ───── 
                                                                      
                                                                      
  Story 5 (W3-9) ── GOVERNANCE FRONTMATTER ROLLOUT via ADR-tk4-003    
                    (3 new keys × 13 delivery-team SKILL.md =         
                     +650 bytes total; cache-prefix region mutated    
                     on every file; +50 bytes/file at byte 0)         
                                ▼                                     
                    CACHE-PREFIX RE-FREEZE (one-time, end of Story 5) 
                    Dev runs the command → governance/cache-prefix-   
                    hash.txt regenerates with expanded scope (13      
                    files vs prior 1-file scope from ADR-tk3-001).    
                                                                      
                                                                      
  Story 6 (W3-10..12) ── parallel with Story 5 (no cache impact)      
  Story 7 (W3-13..18) ── parallel with anything                       
```

## Cache-prefix impact summary

(Consolidates from ADR-tk4-001 §"Cumulative cache-prefix impact assessment" and ADR-tk4-003 §"Cumulative cache-prefix re-freeze procedure".)

- **W3-1..W3-7 (content trims)**: ZERO cache-prefix impact. All extractions land at line ≥111 in every file; the byte-stable cache-prefix region today is the frontmatter block (lines 1–11 in most files, per PRD §3 — no `## Phase 0` headers exist).
- **W3-8 (paradigm sub-skill pattern)**: ZERO cache-prefix impact on parent skills. New sub-skill SKILL.md files are NEW files (no existing prefix). Parent router additions (~1 line at position 100) are below the prefix region.
- **W3-9 (governance frontmatter rollout)**: SOLE cache-prefix-impacting WI in the wave. +50 bytes per file × 13 delivery-team SKILL.md files = +650 bytes total. One-time ~26KB cold-cache re-warm on first Wave 3 dispatch after merge. Hash file regenerates ONCE at end of Story 5 with expanded 13-file scope. Godot lands at 197 post-extraction (round-2 ADR-tk4-001 revision) so the +3 frontmatter add holds Tier-C ceiling EXACTLY at 200; the other 6 in-scope files have ≥9-line headroom.
- **Justification for accepting the cost**: cumulative ~13,200-token reduction from W3-1..W3-7 trims pays back the ~6,500-token cold-cache cost on dispatch #1.
- **DoD validator binding**: Dev runs-the-command at Architect DoD for ADR-tk4-003 (caveman-lite Hot Lesson #1 extension; caught a byte-offset INVERSION in tk3 — without it an inverted ADR would have shipped).

## Stop-Rule Tripwire Mechanics

(Round-2 addition; QA Gate 5 closure. Operationalizes BACKLOG-104 §Stop-rule trigger #2 — caveman-lite carry-forward from BACKLOG-102.)

- **Source telemetry**: `.delivery/telemetry/skill-loads.jsonl` post-merge dispatches (W3-18 telemetry hardening makes the `prose_tokens` field reliable per dispatch).
- **Calculation**: mean response-prose tokens across the **first 3 post-merge dispatches** of any delivery-team SKILL.md, computed via `python3 scripts/compute_token_reduction.py --baseline pre-caveman-lite --window 3 --output .delivery/telemetry/stop-rule-tk4.txt`.
- **Comparison baseline**: Wave 2 archive — `.delivery/memory/archive/run-2026-05-05-tk2.md` prose-token snapshot (pre-caveman-lite reference).
- **Threshold**: if measured reduction `<15%`, **HALT pipeline before W3-9 (Story 5 governance frontmatter rollout) opens its PR**. Stories 1–4 + Story 7 admin may continue under the trigger; only W3-9 and downstream W3-10..12 hold.
- **Recovery path**: trigger BACKLOG-102 stop-rule retro on caveman-lite (binding tk3 carry-forward); architect re-evaluates whether the prose-discipline floor needs further extraction or whether caveman-lite itself needs revision. Retro outcome → Stage 4 round 3 (or Wave 4 deferral) before W3-9 may resume.
- **Tripwire output**: `.delivery/telemetry/stop-rule-tk4.txt` is the Stage 6 DoD citation artifact — narrative claims of "looks fine" are not acceptable; the file must be present and parsed before Story 5 PR opens. (If `compute_token_reduction.py` lacks `--baseline pre-caveman-lite` support today, that flag addition is folded into W3-18 telemetry hardening and ships before Story 5.)

## W3-1 partial-compliance posture

Architect Tier-B closure (500 → ≤300) lands at **288** under the canonical extraction math (5 extractions: Architecture-Style block -76, Software Roles -56, Game Roles -30, Cross-Role Tasks -23, Architecture Guardrails -27). **Status: COMPLIANT**, no partial-compliance ruling needed at architect-batching time.

If Stage 6 finds Cross-Role Tasks (24 lines) cannot extract cleanly (e.g., genuinely cross-cutting prose tied to Phase 1 router), worst-case math is **311** (+11 over Tier-B). The honest partial-compliance ruling activates: ship at ≤311 with `Budget-Exception: ADR-tk4-001` in PR body, log W3-1-residual to `governance/skill-budgets.json` with `target_wave: 4`. Stage 6 DoD runs the command and reports the actual count, not a narrative claim.

## Open questions

None at architect stage. Stage 6 owns three measurement-driven choices (called out, not architectural ambiguities):

1. **Presentation paradigm-vs-references route** (ADR-tk4-002 §Decision conditional clause). Default = references-only; Stage 6 measures dispatch shape and may upgrade to paradigm sub-skill if telemetry favors it.
2. **W3-15 STATUS-format standardize-vs-helper** (PRD §FR-7.3). Architect picks at Stage 4 by cheapness ruling: standardize. STATUS values stay verbatim (DONE / NOT_DONE / CODE_COMPLETE / PASS_WITH_NOTES). Stage 6 confirms cheapness on first dispatch.
3. **W3-17 Stage 7 entry sweep Option A vs B** (PRD §FR-7.5). Architect picks Option A (banner each stale file) for this wave: less destructive, easier to dogfood on the live DEFECT-006 instance found at run-start (PRD §3). Stage 5 sequences; Stage 6 implements.

## References

- ADR-tk4-001: `.delivery/artifacts/04-architect/adrs/ADR-tk4-001-tier-b-closure-approach.md`
- ADR-tk4-002: `.delivery/artifacts/04-architect/adrs/ADR-tk4-002-paradigm-sub-skill-pattern.md`
- ADR-tk4-003: `.delivery/artifacts/04-architect/adrs/ADR-tk4-003-governance-frontmatter-shape.md`
- Stage 1 brief: `.delivery/artifacts/01-idea/po/idea-brief.md`
- Stage 2 PRD: `.delivery/artifacts/02-refine/po/prd.md`
- Backlog: `.delivery/backlog/BACKLOG-104-skill-token-economy-delivery-team-wave-3.md`
- Binding memory: `.delivery/memory/topics/skill-token-economy.md`
- Architect stage memory: `.delivery/memory/stages/architect.md`

— Saruman of Many Colours, Architect, run-2026-05-09-tk4. *"The texts are read; the math is shown; the road is set. Onward."*

# Refine Stage — Memory

## Lessons Learned

- PRD citation discipline is the load-bearing property of any migration PRD. Every Anthropic-docs claim should cite a live URL; adversarial reviewer must independently re-fetch every load-bearing URL. 29-citation PRD with 0 fabricated quotes held under Challenger spot-check of 8. (validated: 1, last: run-2026-04-20-o4v7)

- Developer DoD runs the command — it does not read the command. On any PRD that names executable commands (grep, jq, bash, path lookups, config keys), the Developer validator must execute each command from the repo root. Reading is the prelude; running is the DoD. Three consecutive runs have confirmed the rule: run-2026-04-20-o4v7 (3 regex/path/type bugs caught), run-2026-04-22-4x7e (G-1 blocker + G-2..G-6 non-blockers caught in a single light-mode pass). "Light mode" means reduced depth of prose review, not reduced depth of command execution. (validated: 2, last: run-2026-04-22-4x7e)

- Two-loop Evaluator-Optimizer is worth the cost on multi-requirement PRDs. Loop 1: QA REVISE (11 defects). PO rev 1. Loop 2: QA ACCEPT, 0 regressions. Single-loop would have shipped with the 11 defects. (validated: 1, last: run-2026-04-20-o4v7)

- Two-loop Adversarial converges with measurable signal. confidence 3 → rev 1 → confidence 4. The rev added a 2-hostname gate to WebFetch AC that single-loop would have missed. For PRDs with ≥10 findings, the second loop usually lifts confidence by hardening an AC loop-1 surfaced but didn't close. (validated: 1, last: run-2026-04-20-o4v7)

- No new CLI dependencies in Developer-DoD commands. The WI-14 dogfood shipped with `yq` — not installed on the default dogfood host (exit 127). Refine checklist must enforce: (a) bash-only / python-with-stdlib / python-with-PyYAML equivalents, or (b) explicit install step documented in a dogfood-prereqs PRD section. A DoD command that cannot be executed by the person who must execute it is not a DoD command. (validated: 1, last: run-2026-04-22-4x7e)

- Success-gate ownership must be explicit: one WI closes one gate, or the gate is misscoped. When a §7 success-gate's scope is wider than the nearest WI's edit surface (e.g., WI-05 edits only prompt-engineer/ but §7.4 greps across research-agent/references/ too), either broaden the WI or narrow the gate. Both options were exercised in run-2026-04-22-4x7e (WI-05 AC-7 broadened); make the binding explicit at authoring time. (validated: 1, last: run-2026-04-22-4x7e)

- **PRDs derived from prior audit prose MUST run discovery commands during Refine, not trust upstream narrative.** PRD claimed "11 SKILL.md files" because the audit prose said so; actual was 13 (paradigm sub-skills under architect/skills/paradigms/ were missed). Stage 2 Dev DoD caught it via `find delivery-team -name SKILL.md | wc -l`, requiring revision. Action: PO MUST run the discovery commands (find/grep/wc) as part of Refine authoring, not just cite the audit. (validated: 1, last: run-2026-05-03-tk0e)

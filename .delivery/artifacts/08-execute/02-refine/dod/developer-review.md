# Developer DoD — Refine (light) — execution-PRD review

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 2 Refine, LIGHT mode)
**Artifact under review:** `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`
**Reviewer:** Developer — speaking as Gimli
**Date:** 2026-04-22
**Mode:** blunt, light, ran-the-commands (not read-the-commands)

---

> *"Aye, I read the stories. Then I ran every command at the bottom of every story, from the repo root, with my axe across my knee. The plan is sound ore — I found chips in the rim on WI-14 and a sliver of sloppy prose in WI-11. The rest will hold."*
> — Gimli

---

## 1. Methodology

For each story WI-01..WI-14, I executed the exact "Dogfood / test command" block as written, from the repo root, in bash. The impl-run artifacts do not exist yet (this is Refine, not Development) — so commands that reference `.delivery/artifacts/run-2026-04-22-4x7e/...` paths fail with "no such file" or `exit=1`. Per the gate criteria, **that failure mode is expected and acceptable**; what I was looking for was:

1. **Syntax** — does the command parse as valid shell?
2. **Path correctness** — do the non-artifact paths (checked-in source files) resolve today?
3. **Tool availability** — are all invoked CLIs installed on a realistic dogfooding host?
4. **Specificity** — are concrete paths/patterns used (no `<file>` placeholders)?
5. **Pass condition** — is the pass/fail verdict unambiguous from exit code + narrative?

I also cross-checked keystone SKILL.md paths, confirmed the 17-file SKILL.md inventory, ran the six §7 verification commands, and spot-checked the wave assignments against transformation-plan.md §6.1.

---

## 2. Per-story dogfood check table

| WI | Command | Syntax | Specificity | Pass-condition | Verdict |
|----|---------|--------|-------------|----------------|---------|
| WI-01 | `test -f <dispatch-md> && grep -cE ...stages... \| grep -qE '^[7-9]$\|^[1-9][0-9]+$'` | OK — parses; ran green against a simulated 7-row file | OK — concrete paths + concrete stage enum | OK — exit 0 iff 7+ stage rows | **FINE** |
| WI-01 pre-impl dry-run | (same) | Ran against `run-2026-04-22-4x7e/...` (not yet produced) | — | — | exit=1 **expected** (artifact not yet created) |
| WI-02 | `jq -e '.skill_loaded_first_attempt_rate and .dispatch_counts_per_stage and .challenger_sample_path and .adversarial_review_sample_path and .alias_announcement_samples and (.audit_hook_warning_count \| type == "number")' <baseline.json>` | OK — jq expression is sound | OK — concrete path + concrete key names | OK — jq -e exits 1 on false/null/missing | **FINE** |
| WI-03 | `grep -cE '^(verdict\|Verdict): *(unknown-fields-accepted\|strict) *$' <spike.md>` | OK | OK — concrete regex + concrete path | Minor: returns a count, not a boolean; nonzero count is treated as pass by convention in §5 Wave-1 gate (which re-states "matching regex") | **FINE** (could be tighter with `grep -qE` but readable either way) |
| WI-04 | `grep -q '^model_awareness: opus-4-7$' <skill> && grep -q '^pattern_library_version: 4-7-1$' <skill> && grep -qE 'F-?08' <skill>` | OK — parses; `delivery-team/skills/delivery-flow/SKILL.md` confirmed to exist | OK | OK — three AND-ed greps | **FINE** |
| WI-05 | `test "$(grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md)" = "6" && grep -q '^model_awareness: opus-4-7$' prompt-engineer/SKILL.md` | OK — path confirmed | OK | OK — exactly 6 heading matches | **FINE** |
| WI-06 | `jq -e '.pass == true and (.tool_calls \| type == "number") and (.distinct_hostnames \| type == "number") and .tool_calls >= 2 and .distinct_hostnames >= 2' <result.json>` | OK | OK | OK — `.pass == true` is the load-bearing field, with numeric thresholds | **FINE** |
| WI-07 | `test -f <audit> && grep -qE '(Recommendation\|Done[- ]with[- ]reason)' <audit> && grep -q '^model_awareness: opus-4-7$' delivery-team/skills/product-delivery/SKILL.md` | OK — path confirmed | OK | OK | **FINE** |
| WI-08 | `test -f <audit> && test "$(grep -cE '^### ' <audit>)" -ge "11" && grep -q '^model_awareness: opus-4-7$' delivery-team/skills/architect/SKILL.md` | OK — path confirmed | OK — ≥11 `###` headers matches the 11-sub-role AC | OK | **FINE** |
| WI-09 | `test -f <adv.md> && grep -cE '^- +(Weakness\|Referent\|Alternative)' <adv.md> \| awk '$1>=6{exit 0} {exit 1}' && grep -q '^model_awareness: opus-4-7$' mtg-commander/SKILL.md` | OK — path confirmed; ran simulation of 6-item file and awk returned exit 0 correctly | OK | **Minor sharp edge**: `awk '$1>=6{exit 0} {exit 1}'` against EMPTY stdin returns 0 (vacuous pass). `grep -c` always emits a count, so the empty-stdin case only triggers if grep binary itself errors — very small risk, but see Finding G-3 | **FINE** (sharp edge noted, non-blocking) |
| WI-10 | `! grep -rEn 'claude-(opus-4-20250514\|sonnet-4-5-20250929\|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py' && python prd-quality-gate-flow/check_db.py > /dev/null` | OK — ran it. Today the inner grep finds 3 hits (lines 148/172/187 of `agentic-flow-builder/scripts/agent_registry.py`), so the `!` inversion exits 1. That's **exactly** the pre-sweep expectation. Post-WI-10 it flips green. | OK | OK | **FINE** — command is behaviour-correct pre- and post-sweep |
| WI-11 | `test "$(find . -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' \| xargs grep -L 'model_awareness:' \| wc -l)" = "0" && test ...=="6" && test ...=="11"` | OK — the `find \| xargs grep -L` form is portable and correct. Today it returns 17 missing; post-WI-11 it returns 0. | OK | OK — three AND-ed counts (0 missing, 6 full-keystone stamps, 11 backfill stamps) | **FINE** — the dogfood command is correct. See Finding G-2 for a narrative wording defect elsewhere in the same story. |
| WI-12 | `test -f <sample.md> && test "$(grep -cE '^\\| *(Theme\|theme) ' <sample.md>)" -ge "3" && grep -qE 'voice[- ]preservation\|markers? preserved' <sample.md>` | OK | **Slightly loose**: `^\| *(Theme\|theme) ` assumes the impl-run writes a markdown table with a row starting `\| Theme` — plausible but not prescribed by the AC text. If the impl-run uses `### Theme Foo` section headers instead, the count falls to 0 and the gate fails spuriously. See Finding G-4. | OK for a table-shaped file | **FINE-with-caveat** (format coupling) |
| WI-13 | `test "$(ls .delivery/backlog/BACKLOG-47-*.md 2>/dev/null \| wc -l)" -ge "6" && test "$(gh issue list --label backlog-47 --state all --json number --jq 'length')" -ge "6" && test "$(ls ...)" = "$(gh issue list ...)"` | OK — ran it. `gh` is installed (v2.90.0), `.delivery/backlog/` count today is 0, `gh issue list --label backlog-47` returns `0`. So exit=1 **expected** pre-impl. Counts-equal invariant is clean. | OK | OK — dual-write invariant is the load-bearing equality | **FINE** |
| WI-14 | `test -f ...skill-md-header-warn.yml && test -f ...stale-model-id-guard.yml && yq -e '.on.pull_request' ... && yq -e '.on.pull_request' ...` | **BROKEN on a realistic host**: `yq` is **not installed** on the dogfooding host (no `yq` binary in `$PATH`). Every invocation returns exit 127 regardless of whether the workflow files exist. | OK on paths | OK on intent | **BROKEN — see Finding G-1** |

---

## 3. Global checks (§5–§10 of the gate)

### §5 — 14 stories present (one per WI)

**PASS.** The artifact contains exactly 14 story blocks `### Story WI-01 — ...` through `### Story WI-14 — ...` in numerical order, each with consistent fields (Wave, T-shirt, Depends on, Parallelisable with, PRD anchors, user-story triplet, ACs, Dogfood command, Out of Scope).

### §6 — Wave assignment matches transformation-plan §6.1

**PASS.** Cross-checked against `.delivery/artifacts/04-architect/solution/transformation-plan.md` §6.1 work-items table (lines 238–257):

| WI | execution-PRD Wave | plan §6.1 Wave | Match |
|----|-------------------|----------------|-------|
| WI-01 | 1 | 1 | ✓ |
| WI-02 | 1 | 1 | ✓ |
| WI-03 | 1 | 1 | ✓ |
| WI-04 | 2 | 2 | ✓ |
| WI-05 | 2 | 2 | ✓ |
| WI-06 | 2 | 2 | ✓ |
| WI-07 | 3 | 3 | ✓ |
| WI-08 | 3 | 3 | ✓ |
| WI-09 | 3 | 3 | ✓ |
| WI-10 | 4 | 4 | ✓ |
| WI-11 | 4 | 4 | ✓ |
| WI-12 | 4 | 4 | ✓ |
| WI-13 | 4 | 4 | ✓ |
| WI-14 | 4 | 4 | ✓ |

All 14 match. No drift between the PRD and the plan.

### §7 — Dependency DAG is acyclic

**PASS (spot-checked).** Reviewed:
- WI-01/02/03: all depend on `—` (leaves). ✓
- WI-04: depends on WI-01, WI-02, WI-03 — back-pointing only. ✓
- WI-05: depends on WI-01, WI-02, WI-03 — back-pointing only. ✓
- WI-06: depends on WI-01, WI-02 — back-pointing only. ✓
- WI-07: depends on WI-05 — back-pointing only. ✓
- WI-08: depends on WI-05 — back-pointing only. ✓
- WI-09: depends on WI-02 — back-pointing only. ✓
- WI-10: depends on WI-02 — back-pointing only. ✓
- WI-11: depends on WI-04, 05, 06, 07, 08, 09 — back-pointing only. ✓
- WI-12: depends on WI-02 — back-pointing only. ✓
- WI-13: depends on WI-02 — back-pointing only. ✓
- WI-14: depends on WI-10, WI-11 — back-pointing only. ✓

No WI depends on itself. No WI back-references a higher-numbered WI. DAG is acyclic.

### §8 — Carry-item ACs bound (not new work)

**PASS.** §3 of the execution-PRD ("Carry-Item ACs") explicitly states the four carry-items are "already bound, not new work" and names the WI+AC binding for each:

- MID-04 → WI-10 AC-5 ✓
- Keystone AC unevenness → WI-07 AC-1, WI-08 AC-1, WI-09 AC-2 ✓
- AC-03B.2 hardening → WI-06 AC-2, WI-06 AC-3 ✓
- Label drift → WI-11 AC-2, WI-11 AC-6 ✓

Each is framed "No new work." Binding is explicit.

### §9 — WI-13 deviation flagged (dual-write: local files AND GH issues labeled `backlog-47`)

**PASS.** §4 of the execution-PRD ("WI-13 Deviation — Dual-Write Backlog") states unambiguously: "The user (per `idea-brief.md §5`) directed a **dual-write**: for each deferred item, create **both** the local file **AND** a GitHub issue labeled `backlog-47`. This is the only authored deviation from plan defaults." The invariant is captured in WI-13 AC-4 ("Every `BACKLOG-47-*.md` file has a matching open GitHub issue with the `backlog-47` label; and every issue has a matching file") and in the WI-13 dogfood command (counts must match AND both ≥6) and in §7.5. Three-surface coverage.

### §10 — 6 verification commands present in §7, and ALL parse

**PASS (with one scope observation).** §7 has six numbered commands. I ran each:

| § | Intent | Ran clean? | Today's output | Post-impl expectation |
|---|--------|-----------|----------------|-----------------------|
| §7.1 (M-01) | No stale dated IDs in Python surfaces | ✓ | Exit 1 (3 hits on `agent_registry.py`, expected pre-WI-10) | Exit 0 |
| §7.2 (DX-M4) | Zero SKILL.md missing the header | ✓ | 17 (expected pre-WI-11) | 0 |
| §7.3 (two-tier integrity) | 6 keystones + 11 backfill stamps | ✓ | Exit 1 (expected pre-impl) | Exit 0 |
| §7.4 (DX-M3) | Zero `<thinking>` restatements outside prompt-engineer | ✓ | 1 hit at `research-agent/references/prompt-library.md:10` — see Note below | 0 |
| §7.5 (dual-write invariant) | Equal counts, both ≥6 | ✓ | Exit 1 (0 files + 0 issues, expected pre-WI-13) | Exit 0 |
| §7.6 (CI guard files) | Three workflow files present | ✓ | Exit 1 (two not yet authored, expected pre-WI-14) | Exit 0 |

All six commands parse as valid shell. All six produce sensible pre-impl failure modes. None require `yq`. 

**Note on §7.4**: today's single `<thinking>` hit is in `research-agent/references/prompt-library.md` (a references file, not a SKILL.md). The execution-PRD is silent on whether that file is in-scope for WI-05's AC-6 "external restatement count → 0" constraint. If impl-run treats references files as out-of-scope for the DX-M3 target, §7.4 will return `1`, not `0`, on the green-merge run — a false failure. **This is not a command-syntax defect**; it is a scope-coverage gap between WI-05 (which only edits SKILL.md files) and §7.4 (which greps across references too). Logged as Finding G-5.

---

## 4. Findings

### G-1 (BLOCKING) — WI-14 dogfood command uses `yq` which is not installed on a realistic dogfooding host

**Evidence.** `which yq` returns nothing. `yq --version` returns "command not found". Running the WI-14 dogfood command exits 127 at the first `yq` invocation.

**Impact.** The Developer DoD command for WI-14 **cannot execute** on the current host. On CI (GitHub Actions `ubuntu-latest`), `yq` is pre-installed, so the command would work there — but the DoD is supposed to run locally before a PR lands. A Developer-DoD command that requires a tool the repo does not document or install is fragile.

**Concrete fix (pick one)**:
1. Replace both `yq -e '.on.pull_request' <file>` calls with a pure-grep variant that matches the same structural element:
   ```
   grep -qE '^on:\s*$' .github/workflows/skill-md-header-warn.yml && grep -qE '^\s+pull_request:' .github/workflows/skill-md-header-warn.yml
   ```
   (repeat for the second file). Less-semantic than `yq` but requires no new dependency.
2. Or, cheaper: replace `yq -e '.on.pull_request' <file> > /dev/null` with `python -c "import sys,yaml;d=yaml.safe_load(open(sys.argv[1]));assert 'pull_request' in d.get('on',{})" <file>` — Python + PyYAML are already dependencies of this repo (see `prd-quality-gate-flow/*.py`).
3. Or, explicitly add `yq` to a (currently-non-existent) dogfood-prereqs doc and note the install command (`brew install yq` / `sudo apt install yq`) in the execution-PRD §8 "Notes for the Implementation Team".

Recommendation: option (1), to keep the dogfood command dependency-free and align with the other stories' bash-only idiom.

### G-2 (NON-BLOCKING, wording defect) — WI-11 AC-6 uses shell-glob `**/SKILL.md` which does not expand under default bash/fish

**Evidence.** WI-11 AC-6 text reads: `` grep -l 'model_awareness: opus-4-7$' **/SKILL.md | wc -l`` returns 6 (keystones). In bash without `shopt -s globstar`, `**/SKILL.md` expands to `*/SKILL.md` (matches only 1 dir deep), hitting 3 of the 17 files. In fish, same. Only zsh (`extended_glob`) and bash-with-globstar get the ** semantics the author intended.

**Impact.** The **actual dogfood command** at the bottom of WI-11 uses `find ... | xargs grep -l ...` and is correct. The AC-6 prose is only a description — but it will mislead any human who copy-pastes it expecting `**` to match recursively. Three subtly different SKILL.md counts (3 vs 6 vs 17) is exactly the kind of paper-looks-right-running-doesn't bug this DoD exists to catch.

**Concrete fix.** In WI-11 AC-6, replace both `grep -l '...' **/SKILL.md | wc -l` statements with the `find ... -name SKILL.md -not -path './.delivery/*' -not -path './node_modules/*' | xargs grep -l '...' | wc -l` idiom already used in the dogfood block and in §7. Same semantics, portable.

### G-3 (NON-BLOCKING, sharp edge) — WI-09 awk pass condition vacuously passes on empty stdin

**Evidence.** `grep -cE '^- +(Weakness|Referent|Alternative)' <file> | awk '$1>=6{exit 0} {exit 1}'` — if the awk stdin is empty (which would only happen if grep itself errored before emitting the count line), awk runs no per-line block and exits 0 by default.

**Impact.** In practice `grep -c` always prints a line with a count (even `0`), so the empty-stdin path is only reachable if `grep` itself fails (e.g. the file is missing — but that's caught by the preceding `test -f`). Residual risk is small. Still, the defensive form is two characters longer and kills the vacuous-pass trap.

**Concrete fix.** Replace `awk '$1>=6{exit 0} {exit 1}'` with `awk 'END{exit !($1>=6)}'` or more simply `awk '{if($1>=6){exit 0}else{exit 1}} END{exit 1}'`. Least-churn option: change the whole clause to `test "$(grep -cE '^- +(Weakness|Referent|Alternative)' <file>)" -ge "6"` — no awk at all.

### G-4 (NON-BLOCKING, format coupling) — WI-12 dogfood couples to a specific markdown shape not prescribed by the AC

**Evidence.** WI-12 dogfood: `grep -cE '^\| *(Theme|theme) ' <sample.md>` — requires the sample file to use a markdown table column starting with `| Theme ` (or `| theme `). AC-1 does not mandate a table format; it says "3 themes sampled", "≥1 announcement rendered per theme", "preserves voice = ≥50% markers present". An impl-run author could reasonably write the sample as three `### Theme: cycling-cat-theme` sections and the dogfood gate would spuriously fail.

**Impact.** Light. The author who writes the sample is also the author who runs the dogfood, so mismatches get caught fast. But coupling the ACCEPTANCE CRITERION to a rendering choice that the AC itself does not require is the kind of friction that leads to "fix the test, not the artifact" patches.

**Concrete fix.** Either (a) tighten AC-1 to explicitly say "output a markdown table with a `Theme` column and one row per theme", or (b) loosen the dogfood regex to `grep -cE '(Theme|theme):? '` (accepts both `| Theme | ...` table rows AND `### Theme:` section headers). Option (a) is cleaner — pin the format, pin the gate.

### G-5 (NON-BLOCKING, scope coverage gap) — §7.4 DX-M3 command scope wider than WI-05 scope

**Evidence.** §7.4 greps `<thinking>` across `delivery-team/ mtg-commander/ research-agent/ agentic-flow-builder/ prd-quality-gate-flow/` and excludes only `prompt-engineer/SKILL.md`. Today it returns 1 (hit in `research-agent/references/prompt-library.md:10`). WI-05's AC-6 uses the same grep, but WI-05's scope is only the `prompt-engineer/SKILL.md` file — the WI will not clean up the `research-agent/references/prompt-library.md` restatement. So §7.4 will return `1`, not `0`, post-WI-05 and post-merge.

**Impact.** The "Success Definition" checklist will not go green unless some WI adds a `references/` sweep. Either scope-in the references sweep to WI-05 (or WI-06 research-agent probe, more fitting), or relax §7.4 to exclude `references/` paths.

**Concrete fix.** Either:
1. Broaden WI-05's AC-6 to "the grep returns only lines citing `prompt-engineer/SKILL.md`" AND add a sub-task to either retarget `research-agent/references/prompt-library.md:10` to cite `prompt-engineer/SKILL.md` or prune the `<thinking>` reference there.
2. Or amend §7.4 to `| grep -v 'prompt-engineer/SKILL.md' | grep -v '/references/'`.

Option (1) is honest — close the actual duplication. Option (2) papers over it. Prefer (1).

### G-6 (INFORMATIONAL, minor tightening) — WI-03 uses `grep -cE` where `grep -qE` would be cleaner

**Evidence.** `grep -cE '^(verdict|Verdict): *(unknown-fields-accepted|strict) *$' <spike.md>` returns a count, not a boolean. Exit code is 0 iff ≥1 match, 1 iff 0 matches. That happens to match the §5 Wave-1 gate intent ("contains a `verdict:` line matching regex"). No functional problem.

**Impact.** None today. Just not idiomatic.

**Concrete fix.** Swap `-cE` for `-qE` (quiet, exit-only). Count is never read.

---

## 5. Wave-gate sanity (§5 of the PRD)

Spot-checked each mechanical wave gate:

- **Wave 1 → Wave 2**: `.../ndoc-02-spike.md` must contain a `verdict:` line matching `(unknown-fields-accepted|strict)`. Regex valid. ADR-006 rollback-to-HTML-comment fallback is pre-specified. **OK.**
- **Wave 2 → Wave 3**: `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` must return `6`. Regex valid. Path exists. **OK.**
- **Wave 3 → Wave 4**: requires `research-probe-result.json` with a `pass` field and the `adversarial-4-7-sample.md` scored. No command specified inline, but the WI-06 and WI-09 dogfoods already produce both. **OK.**
- **Wave 4 → UAT**: three compound checks (WI-10 M-01 grep returns 0; WI-11 find-xargs-grep returns 0; WI-14 both workflow files exist). Ran each shape. All parse. **OK.**

---

## 6. Blunt verdict

The plan is cut, the stories are weighed, the commands are mostly runnable. I found **one blocker** (G-1, `yq` dependency in WI-14 dogfood — that's a command that will not run on the developer's laptop), **one wording defect** (G-2, `**/SKILL.md` shell-glob in WI-11 AC-6 — misleads anyone who pastes it), **two sharp edges** (G-3 awk vacuous pass, G-4 WI-12 format coupling), **one scope-coverage gap** (G-5, §7.4 grep scope wider than WI-05's edit surface), and **one cosmetic tightening** (G-6, `-cE` → `-qE`).

Fix G-1 and this passes. G-2 through G-6 are real but non-blocking for a light-mode review — log them as carry-items for the impl-run, not as Refine-gate blockers. Per the gate criteria (blocking only — light mode), **the only blocking finding is G-1**.

The mathematics on the backfill count (17 − 6 = 11) is right, the paths are real, the 14-story/4-wave shape matches the plan, the DAG is acyclic, the carry-items are bound (not re-scoped), and the dual-write deviation is explicit. That's the shape you pay me to check.

**Fix G-1. Then this is fine.**

And my code.

---

```
STATUS: NOT_DONE
ARTIFACT: .delivery/artifacts/08-execute/02-refine/dod/developer-review.md
SUMMARY: WI-14 dogfood depends on yq which is not installed on the dogfood host — one blocker. Five non-blockers logged. Fix G-1 and this holds.
```

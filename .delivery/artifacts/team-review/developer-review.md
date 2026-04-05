# Developer Review: delivery-team Plugin

**Reviewer**: Gimli (Developer)
**Date**: 2026-04-04
**Scope**: Full code and content review of the delivery-team plugin
**Verdict**: Solid craftsmanship overall. The foundations are strong. But there are cracks that need filling before they become fissures.

---

## 1. generate_pptx.py — Code Review

**File**: `delivery-team/skills/presentation/scripts/generate_pptx.py`
**Lines**: 477

### Good Craft

- **Import guard** (lines 40-53): Clean fail-fast with helpful error message. This is the right way to handle optional dependencies. And my code approves.
- **Layout resolution** (lines 87-109): Name-first, index-fallback is a solid defensive pattern. Handles edge cases where template slide masters differ from defaults.
- **CLI argument parsing** (lines 419-457): Clean argparse with useful epilog examples and RawDescriptionHelpFormatter.
- **Directory creation** (line 408): `output_file.parent.mkdir(parents=True, exist_ok=True)` -- good defensive file handling.
- **Docstrings**: Every public function has a clear docstring. Good.

### Issues

**P1 (Bug): `generate_pptx` calls `sys.exit(1)` inside a library function (lines 344, 351, 367, 375)**

This function is both the library entry point AND called from the CLI. If anyone imports this module and calls `generate_pptx()` programmatically, errors will kill their process instead of raising exceptions. The docstring even says "Raises: FileNotFoundError, ValueError" -- but it never actually raises those; it calls `sys.exit()` instead.

Fix: Raise exceptions from `generate_pptx()`, catch them in `main()` and `sys.exit()` there.

**P2 (Design): `accent_color` parameter is accepted but barely used (lines 129-134)**

`set_text_frame_font()` applies accent color to ALL text runs, but this function is never called in the main generation flow. The accent color parameter flows through `generate_pptx` -> `populate_content_slide` -> but `populate_content_slide` never calls `set_text_frame_font()`. The title slide sets font name but not accent color (lines 147-148). The accent_color parameter is effectively dead code.

**P3 (Edge case): Widescreen dimensions for blank presentations (lines 383-385)**

`Inches(13.333)` x `Inches(7.5)` is non-standard. Standard 16:9 is 13.333 x 7.5 inches, so the values are correct, but this only applies when no template is provided. The code comment says "widescreen 16:9" which is accurate.

**P3 (Missing validation): No JSON schema validation (line 361)**

The code checks for a `slides` key and that it is a list, but individual slide objects are not validated. A slide missing `layout` or `title` won't crash (defaults are used), but a slide with `body: "string instead of list"` at line 166 would fail silently or crash at the `enumerate(items)` call.

**P4 (Style): Unused import `MSO_ANCHOR` (line 45)**

Imported but never used anywhere in the file.

**P4 (Style): Unused import `Emu` (line 43)**

Imported but never used.

---

## 2. Hook Scripts — Code Review

**Files**: `delivery-team/hooks/*.py` (6 scripts + lib/hook_utils.py)

### Good Craft

- **Shared library pattern** (`lib/hook_utils.py`): Clean separation. All hooks share input parsing, response emission, and exit codes. No duplication.
- **Graceful degradation**: Every hook silently exits on errors rather than blocking the user. `enforce_pipeline_scope.py` (line 213-217) wraps `main()` in a bare `except Exception` for belt-and-suspenders safety.
- **Shebang lines**: All hooks except `enforce_pipeline_scope.py` have `#!/usr/bin/env python3`. That one has a docstring on line 1 instead.
- **No external dependencies**: All hooks use stdlib only. Good discipline.

### Issues

**P1 (Missing Registration): `enforce_pipeline_scope.py` exists as a script but is NOT registered in `hooks.json`**

The file exists at `delivery-team/hooks/enforce_pipeline_scope.py` (218 lines of well-written code), but `hooks.json` has no entry for it. The Skill enforcement in hooks.json uses a `prompt`-type hook on `PreToolUse:Skill`, but the `enforce_pipeline_scope.py` script is a `command`-type hook that should run on `PreToolUse:Write|Edit|NotebookEdit`. This script is dead code -- it never executes.

The `setup-wizard.md` reference mentions installing an enforcement hook in the project's `.claude/settings.json`, but the plugin's own `hooks.json` does not register this script. Either the script should be registered in hooks.json, or it's intended to be project-level only (installed by the wizard). This needs clarification.

**P2 (Inconsistency): `enforce_pipeline_scope.py` uses a different `sys.path` approach (line 16-17)**

All other hooks use `sys.path.insert(0, str(Path(__file__).parent))` then `from lib.hook_utils import ...`. This hook uses `sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))` then `from hook_utils import ...`. Both work, but the inconsistency is shoddy. Pick one pattern and stick with it.

**P2 (Missing shebang): `enforce_pipeline_scope.py` (line 1)**

Every other hook script starts with `#!/usr/bin/env python3`. This one starts with a docstring. If this script were ever invoked directly on Unix, it wouldn't know which interpreter to use.

**P3 (Regex fragility): `check_config.py` (lines 21-28)**

Config values are parsed with regex (`re.search`). This works for simple YAML but will break on:
- Quoted strings with colons: `clean_code_guide: "path:with:colons"`
- Multi-line values
- Comments on the same line: `config_version: "2.6" # current`

This is a known trade-off (no pyyaml dependency), but it should be documented with a comment like "# Lightweight regex parsing -- known limitations: does not handle quoted colons or inline comments."

**P3 (Same regex fragility): `enforce_pipeline_scope.py` (lines 43-101)**

The `_parse_yaml_string` and `_parse_yaml_list` functions are more sophisticated regex-based YAML parsers, but they share the same class of fragility. The block-list parser (line 94) calculates `remaining` from byte offsets, which could be unreliable with multi-byte characters.

**P4 (Broad exception): `hook_utils.py` (line 13)**

```python
except (json.JSONDecodeError, Exception):
```
The `json.JSONDecodeError` catch is redundant since `Exception` catches everything. Should be just `except Exception:`.

**P4 (exit_block protocol): `hook_utils.py` (lines 34-36)**

`exit_block` writes JSON to stderr and exits with code 2. The Claude Code hook contract uses `decision: block` in stderr. But `validate_gdscript.py` is the only hook that calls `exit_block`. The other hooks use `emit_response` to stdout. This inconsistency in the blocking mechanism should be documented -- which protocol is correct depends on whether the hook is PreToolUse (can block) or PostToolUse (can only warn).

---

## 3. delivery-flow SKILL.md — Clarity Review

**File**: `delivery-team/skills/delivery-flow/SKILL.md`

### Good Craft

- **Phase 0 (Setup Wizard)**: Exhaustive state detection with resume/restart/abandon flow. Config version migration is well-specified.
- **Two-Channel Communication**: Clear signal/artifact separation. The 200-char rule is specific and enforceable.
- **Theme-Gated Reporting Protocol**: Well-integrated. The neutrality preservation list is essential and complete.
- **CONTINUATION DIRECTIVEs**: Explicit "do not stop, do not wait" directives at Steps 7, 9, 10. These prevent the biggest agent failure mode (unnecessary pausing).
- **Delegation Self-Check (Step 4.5)**: Clever guardrail against the orchestrator accidentally writing domain content.

### Issues

**P2 (Confusing numbering): Phase 0 has TWO numbered lists starting at 1 (lines 55, 74)**

Lines 55-72 are a numbered list 1-5 for state detection. Then line 74 starts ANOTHER numbered list 1-5 for config detection. These are sequential steps in the same phase, but the numbering resets, making it ambiguous whether they are alternatives or sequential. An LLM agent could reasonably interpret the second list as overriding the first.

Fix: Use a single numbered sequence (1-10) or clearly label subsections ("State Detection" then "Config Detection").

**P2 (Ambiguous artifact paths): SKILL.md Stage definitions vs. pipeline-stages.md conflict**

In the SKILL.md Stage 1 definition (line 549): `Output: .delivery/artifacts/01-idea-brief.md`
In the SKILL.md Stage 2 (line 592): `Output: .delivery/artifacts/02-prd.md`
In `references/pipeline-stages.md` and the docs site (`docs/user-guide/pipeline.md` line 37): `Output: .delivery/artifacts/01-idea/po/idea-brief.md` and `.delivery/artifacts/02-refine/po/prd.md`

The SKILL.md uses flat paths. The pipeline-stages reference uses namespaced paths. These are contradictory. An agent following the SKILL.md would write to a different location than one following pipeline-stages.md.

Fix: Pick one convention and enforce it everywhere. The namespaced convention (`{NN}-{stage}/{role}/`) is the correct one per the architecture (pipeline-stages.md line 3-10).

**P3 (Missing SELF-RECOVERY context): Line 286**

The SELF-RECOVERY directive says "re-read `.delivery/state.md` to determine `current_stage`" but doesn't specify what "idle" means or how to detect it. This is helpful but vague.

---

## 4. Presentation SKILL.md — v1.1 Integration Review

**File**: `delivery-team/skills/presentation/SKILL.md`

### Good Craft

- **5 new types** (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary): Well-integrated with detection keywords, pipeline auto-detection, content gate requirements, and GAME_DEV vocabulary adaptations.
- **Light mode and threshold interaction matrix** (line 89-98): Clear, no ambiguity.
- **Retrospective Summary sensitivity filter** (lines 112-119): Thoughtful audience-dependent privacy handling.
- **PPTX JSON intermediate** (line 312): Clean separation between human-reviewable markdown and machine-readable JSON.
- **Editorial passes**: Strict ordering with dependency reasoning (ADR-02 reference). Each pass has clear config toggle, heuristics, and output logs.

### Issues

**P2 (Config key drift): presentation config in SKILL.md vs config-schema.md**

SKILL.md defines `presentation.thresholds` as a map (line 531) with per-type keys. The config-schema.md template (line 282-283) shows:
```yaml
thresholds: {}
thresholds_default: 90
```
But the SKILL.md (line 78) mentions `presentation.thresholds.{type-name}` as dot-notation access. This is fine for an LLM reading config, but the actual YAML structure nests `thresholds` under `presentation`, and a real YAML parser would access it as `config['presentation']['thresholds']['sprint-review']`. The dot-notation in the SKILL.md could confuse an agent about the actual YAML structure.

**P3 (Step 3 role mismatch with v1.1 types)**

Step 3 (line 188-208) lists 5 contributing sub-agents but doesn't specify which roles map to the new types (Investor Pitch, Roadmap, Product Demo, Onboarding, Retrospective Summary). The Content Gate (Step 2) lists required artifacts per type, but Step 3 doesn't say which sub-agents to dispatch for each new type. An agent must infer that Product Owner handles "Onboarding" narrative slides, which is non-obvious.

---

## 5. Architect SKILL.md — Prior Art Analysis Review

**File**: `delivery-team/skills/architect/SKILL.md`

### Good Craft

- **Prior Art Analysis** (lines 36-79): Excellent. The condition gate ("Execute ONLY when user-provided specifications are present"), classification table, deviation protocol with burden-of-proof -- this is exactly right. This addresses the memory feedback about examining user specs first.
- **Deviation Protocol** (lines 70-75): Specific, verifiable blocker requirement. Not "might not scale" but "PostgreSQL does not support graph traversals required by the adjacency query pattern specified in Section 3.2". This is the level of specificity needed to prevent architects from overriding user decisions.
- **Guardrails** (line 497): "Respect user-provided specifications" codified at the guardrail level.

### Issues

**P3 (Skip condition ambiguity): Line 36**

"If no user-provided specs exist, note 'No prior specifications provided' and skip directly to Phase 2." But the architect sub-agent might receive upstream artifacts from the pipeline (PRD, design docs) that ARE specifications -- they are just not "user-provided" in the sense of being provided in the current request. Should pipeline-generated PRDs trigger Prior Art Analysis? The condition should clarify: "user-provided OR upstream pipeline artifacts containing architectural decisions."

---

## 6. Reference Files — Structure Review

**Files**: `delivery-team/skills/delivery-flow/references/` (19 files)

### Good Craft

- **pipeline-stages.md**: Agent Invocation Templates are well-structured with clear field specifications. Dispatch annotations ([PARALLEL]/[SEQUENTIAL], [required]/[optional]) are consistent.
- **config-schema.md**: Complete schema table with types, defaults, valid values, wizard question mapping, and consuming skills. Version history is thorough.
- **quality-gates.md**: DoD protocol is clear with self-correction loops and escalation.

### Issues

**P2 (Config template YAML validity): config-schema.md lines 178-288**

I checked the YAML template. It is valid YAML. All keys are properly indented, types are consistent, lists use bracket notation or dash notation correctly. The `decision_matrix_inputs` uses `team_size: 4` (integer) in the template but the schema table says the type is `object` with low/medium/high values. This is a type mismatch:

- Schema table (line 29): `team_size, deploy_independence, domain_complexity, change_rate (each: low/medium/high)`
- Template (line 198): `team_size: 4` (integer, not "low"/"medium"/"high")

The template should use `team_size: medium` (not `4`) to match the schema definition.

**P3 (File count in docs): docs/contributing/index.md (line 21)**

States "18+ reference files" for delivery-flow. Actual count is 19 files (plus `config-schema.json`). Minor, but accuracy matters.

---

## 7. Docs Site — Quality Review

**Files**: `docs/**/*.md` (25 pages)

### Good Craft

- **Structure**: Clean hierarchy -- getting-started, skills, user-guide, reference, contributing, architecture. Navigation is logical.
- **Installation guide**: Concise, shows the `claude plugin install` command. Lists all 11 skills.
- **Config reference**: Complete key listing matching config-schema.md (with minor omissions noted below).
- **Collaboration patterns**: Good detail for patterns 1-2, reasonable summaries for 3-6.
- **Memory reference**: Clear tiered retrieval explanation.
- **Hooks reference**: All 7 hooks documented with event, matcher, type, timeout.

### Issues

**P2 (Incomplete docs config): `docs/user-guide/config.md` is missing several presentation keys**

The docs config page (lines 141-149) lists only 5 presentation keys:
- `default_format`, `default_audience`, `speaker_notes`, `light_mode`, `thresholds_default`

But the schema defines 17 presentation keys. Missing from docs:
- `save_to_artifacts`, `marp_theme`, `staleness_warning_days`, `vocabulary_overrides`
- `pptx_template`, `pptx_font`, `pptx_accent_color`
- `narrative.emphasis`, `narrative.cutting`, `narrative.framing`, `narrative.tension`
- `thresholds` (the per-type map)

The docs example config (lines 243-250) also omits all PPTX keys, narrative keys, and several other presentation keys. Someone reading only the docs would not know about PPTX branding configuration.

**P2 (Docs config missing `pipeline.required_agent_retry_max`)**

The schema defines `pipeline.required_agent_retry_max` (line 39 of config-schema.md) but the docs config reference omits it entirely.

**P3 (Inconsistent artifact path): docs/user-guide/pipeline.md**

Line 37: `Output: .delivery/artifacts/01-idea/po/idea-brief.md`
But the SKILL.md says: `Output: .delivery/artifacts/01-idea-brief.md`
And the docs/architecture/overview.md (line 49): `01-idea/po/idea-brief.md`

Two out of three agree on the namespaced path, but the SKILL.md disagrees. Same issue as finding #3.3 above.

**P4 (Thin docs pages): `docs/skills/operations.md`, `docs/skills/godot.md`, `docs/skills/quality.md`**

I didn't read every skill doc page, but the presentation doc page (85 lines) is relatively thin compared to the actual SKILL.md (541 lines). Some docs pages may be stubs. Not a bug, but the docs should either be comprehensive or explicitly link to the source SKILL.md for full details.

---

## 8. Source vs Installed File Sync

### Issues

**P2 (Dead hook script): `enforce_pipeline_scope.py` exists but is not registered**

As noted in section 2, this script exists as a fully implemented 218-line Python file but is not registered in `hooks.json`. It is effectively dead code from the plugin's perspective. It is referenced in `setup-wizard.md` as a project-level hook, but its existence in the plugin's `hooks/` directory alongside registered hooks is misleading.

If this is intended to be project-level only (installed by the wizard into `.claude/settings.json`), it should be moved to a `scripts/` directory or clearly documented as "not a plugin hook."

---

## 9. Recent Commit Quality

```
185d802 docs: add MkDocs Material documentation site with 25 pages (#48)
22e2aa3 chore: bump version to 2.17.0
828119d feat(delivery-flow): add theme-gated reporting protocol (#59)
abbb6f3 chore: bump version to 2.16.0
1747b86 feat(presentation): add v1.1 enhancements — 5 new types, PPTX, narrative, light mode (#43-46)
8b4b80b chore: bump version to 2.15.2
4f27f76 fix(architect): add Prior Art Analysis step (#55)
8c9f119 chore: bump version to 2.15.1
80d1cc8 fix: add Agent Invocation Templates with alias injection (#58)
2f50a35 chore: post-acceptance protocol for run-2026-04-02-k3r9
```

### Assessment

- **Conventional commits**: Consistently used (`feat`, `fix`, `chore`, `docs`). Good discipline.
- **Scoped commits**: `feat(presentation)`, `fix(architect)` -- clear ownership.
- **PR references**: Issue/PR numbers in parentheses. Good traceability.
- **Version bumps**: Separate commits for version bumps. Clean.
- **Commit messages**: Descriptive without being verbose. The `1747b86` message lists all 4 PRs it covers, which is useful.

**No issues**. The commit log is clean and well-disciplined. And my code respects that.

---

## Summary of Findings

| Priority | Count | Description |
|----------|-------|-------------|
| P1 | 2 | `generate_pptx.py` sys.exit in library function; `enforce_pipeline_scope.py` dead code (not registered) |
| P2 | 7 | Dead accent_color code; inconsistent sys.path in hooks; confusing Phase 0 numbering; artifact path conflicts between SKILL.md and references; config template type mismatch; docs missing 12+ presentation keys; docs missing `required_agent_retry_max` |
| P3 | 7 | Missing JSON validation; regex fragility docs; SELF-RECOVERY vagueness; dot-notation config confusion; Prior Art skip condition; file count inaccuracy; docs artifact path inconsistency |
| P4 | 5 | Unused imports; redundant exception catch; exit_block protocol docs; missing shebang; thin docs pages |

### Top 3 Actions

1. **Fix the artifact path inconsistency** -- SKILL.md stage definitions must use the namespaced convention (`{NN}-{stage}/{role}/`) to match `pipeline-stages.md`. This is a real source of agent confusion.
2. **Decide what to do with `enforce_pipeline_scope.py`** -- either register it in `hooks.json` or move it out of the `hooks/` directory. Dead code in a hooks directory is misleading.
3. **Complete the docs config reference** -- the 12 missing presentation keys mean users reading docs alone won't discover PPTX branding, narrative intelligence toggles, or per-type thresholds.

---

*And my code! The foundations are dwarven-strong, but some of these inconsistencies would not pass inspection in the Mines of Moria. Fix the paths, register the hook, finish the docs. Then we feast.*

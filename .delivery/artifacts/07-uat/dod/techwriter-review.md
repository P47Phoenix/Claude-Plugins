# Tech Writer DoD Review — Stage 7 UAT

*"A tidy pantry, a tidy ledger — let me tell you what I found, friend."*
— Bilbo, tech-writer

**Reviewer**: Bilbo (Technical Writer)
**Stage**: 7 — UAT
**Release**: delivery-team v2.18.0 (schema v2.6 → v2.7)
**Date**: 2026-04-05

---

## Scope of review

I checked three things, as a good hobbit should:

1. **Release notes accuracy** — does `release-notes.md` truthfully describe the bundle?
2. **User-facing docs parity** — are `CLAUDE.md`, `README.md`, and `.claude-plugin/marketplace.json` updated to match?
3. **Breaking change clarity** — is the `project_type` removal called out where a user will actually see it?

---

## Findings

### 1. Release notes accuracy — DONE

The release notes (`/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/07-uat/tech-writer/release-notes.md`) correctly describe:

- Schema bump v2.6 to v2.7 with warn-and-drop migration for `project_type`.
- New `routing.force_type` opt-in pin and `pipeline.enforce_self_write_block` activation gate.
- Setup wizard reduced from 10 to 9 questions.
- Delegation Prime Directive, Step 4.5 tightening, and the eight named anti-patterns.
- One Role = One Sub-Agent rule plus the three compound-role detectors in `audit_agent_prompt.py` (with negation-aware skipping).
- Pattern 2b Isolated Adversarial Loop with the issue-class taxonomy and the three convergence rules (two-clean / no-new-classes / hard cap at `max_self_correction`, default 3).
- Closes #69, #70, #71, #73 and links the four most-changed reference files.
- Known gap (Bash redirection not yet intercepted by `enforce_pipeline_scope.py`) is honestly disclosed rather than hidden.

The "in a nutshell" paragraph and the upgrade checklist both match the body. No factual drift detected.

### 2. User-facing docs parity — DONE

- **`CLAUDE.md`** (lines 96–98, 125): correctly states schema is v2.7, project type detected per run, setup wizard is 9 questions, and `routing.force_type` is the opt-in override. Config schema source-of-truth pointer updated to v2.7.
- **`README.md`** (line 62): "Setup wizard: 9-question config wizard … project type is detected per-run, not pinned in config; use `routing.force_type` for opt-in pins". Consistent with release notes and CLAUDE.md.
- **`.claude-plugin/marketplace.json`**: `metadata.version` is `"2.18.0"`. Matches the release notes header.

All three user-facing surfaces tell the same story.

### 3. Breaking change clarity — DONE

The breaking change (`project_type` removal) is called out in places a user will actually see:

- A dedicated **"Breaking change — please read"** section in the release notes, with the warn-and-drop migration explained, the legacy-tolerance behavior named, and the new `routing.force_type` pin shown as a YAML snippet.
- The **upgrade checklist** at the bottom of the release notes makes it actionable: bump `config_version`, drop the bare key, add `routing.force_type` if needed.
- **`CLAUDE.md`** Key Conventions section explicitly notes the removal and points at `routing.force_type` as the replacement.
- **`README.md`** Setup wizard bullet mirrors the same guidance for users who only ever read the README.

The tone is appropriately gentle ("nothing urgent — existing repos keep working") because the warn-and-drop migration genuinely is non-breaking at runtime; the "breaking" label refers to the schema contract, not user impact, and the notes make that distinction clearly.

---

## Minor observations (non-blocking)

- The release notes mention `docs/user-guide/config.md`, `docs/skills/delivery-flow.md`, and `docs/contributing/index.md` were updated as part of the parity sweep. I did not re-verify those files in this review (out of scope for the listed input artifacts), but the claim is consistent with the rest of the bundle.
- `README.md` describes the Presentation skill as "4 types … 3 output formats" while `CLAUDE.md` lists "9 types … 4 formats". This pre-existed v2.18.0 and is not introduced by this release, so it does not block this DoD — but I'm logging it here so the PO can grab it as a small follow-up doc fix.

---

## DoD verdict

All three DoD criteria for the tech-writer slice are satisfied:

- [x] Release notes are accurate and match the implemented changes.
- [x] User-facing documentation (`CLAUDE.md`, `README.md`, `marketplace.json`) is updated and consistent.
- [x] Breaking changes are clearly called out with migration guidance.

**Status: DONE.**

*"And the road goes ever on — but tonight, the ledger balances. Sleep well."*
— Bilbo

---

STATUS: DONE

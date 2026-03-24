## Idea Brief

**Project Type**: FEATURE
**Date**: 2026-03-24
**GitHub Issue**: #11

### Problem Statement
The delivery-flow pipeline runs end-to-end within a single Claude Code session. When a session ends (timeout, crash, user closes terminal, context limit), all pipeline state is lost. The user must restart from Stage 1 even if Stages 1-5 were complete. For long pipeline runs (GREENFIELD with full depth), this makes the pipeline unreliable for real-world use.

### Target Users
- **Long-session user**: running a GREENFIELD or GAME_DEV pipeline that spans 7 stages with full collaboration patterns — easily 30+ minutes of work that can be lost
- **Interrupted user**: gets a phone call, closes laptop, session times out — needs to resume where they left off
- **Multi-session user**: intentionally splits pipeline across sessions (do Idea→Architect today, Dev→UAT tomorrow)

### Goals
1. Pipeline state persisted to `.delivery/state.md` after each stage completes
2. New session detects existing state and offers: Resume / Restart / Abandon
3. Resume loads all prior artifacts and continues from next incomplete stage
4. State file cleaned up after successful pipeline completion
5. Aborted runs preserve state for potential resume

### Constraints
- State file must be human-readable (markdown with YAML frontmatter, matching existing .delivery/ patterns)
- Must not conflict with existing memory system (state is current-run, memory is cross-run)
- Resume must re-read upstream artifacts from `.delivery/artifacts/` (they already persist)
- Must handle partial stage completion (stage started but not finished)

### Initial Scope
- State persistence after each stage gate passes
- Resume detection on pipeline start (Phase 0)
- Resume/Restart/Abandon prompt
- State cleanup on completion

### Out of Scope (initial)
- Mid-stage checkpointing (saving state between sub-agent calls within a stage)
- Automatic crash recovery (detecting unclean shutdown)
- Multi-pipeline state (only one active pipeline per project)

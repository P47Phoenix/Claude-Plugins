# Release Notes — Architecture Documentation Pipeline

**Writer:** Bilbo (Tech Writer)
**Release:** Architecture docs rollout, run-2026-04-11-h9i6
**Date:** 2026-04-14

## What shipped

Every plugin in the marketplace now has an `ARCHITECTURE.md` describing its internal design with Mermaid diagrams — intended for contributors, not end users.

| Plugin | Diagrams |
|--------|---------:|
| delivery-team | 4 |
| mtg-commander | 3 |
| agentic-flow-builder | 2 |
| prd-quality-gate-flow | 2 |
| research-agent | 2 |
| prompt-engineer | 1 |

**Total: 14 Mermaid diagrams across 6 plugins.**

## Where to find them

- Each plugin directory contains an `ARCHITECTURE.md` at its root (e.g., `delivery-team/ARCHITECTURE.md`).
- Each plugin `README.md` now links to its `ARCHITECTURE.md` near the top.
- Root `README.md` and `CLAUDE.md` reference the convention.

## How to render Mermaid

Most modern markdown viewers render Mermaid fenced blocks natively — including GitHub (viewed in-browser), VS Code with any Mermaid extension, Obsidian, and Typora. No special tooling required; open the file on GitHub and diagrams appear inline.

For offline rendering: `npm i -g @mermaid-js/mermaid-cli` then `mmdc -i ARCHITECTURE.md -o diagram.svg`.

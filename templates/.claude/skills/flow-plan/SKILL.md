---
name: flow-plan
description: |
  Alias for the Claude Code /flow-plan command. Use when the user says
  flow-plan or /flow-plan to create a frozen Agent Flow implementation plan.
---

# Flow Plan

Use the repo-local `.claude/commands/flow-plan.md` command contract.

## Compatibility Contract

- Same artifact as Codex: `docs/flow/{feature_name}/plan.md`.
- Same required gates: Business Flow Matrix, Regression Surface Matrix, Test
  Design Matrix, Integration Coverage Contract, Flow Knowledge Update, and
  Residual Risk Preflight when applicable.
- Same bug/regression behavior: run Bug Feedback Review and update
  `docs/agent-flow/bug-knowledge.md` when flow improvement cannot prevent the
  issue.
- Same browser behavior: include Playwright Integration Test Plan for visible or
  multi-step workflows.

When this skill is invoked in Claude Code, execute `/flow-plan` semantics rather
than inventing a separate planning flow.

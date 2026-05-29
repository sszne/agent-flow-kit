---
name: flow-impl
description: |
  Alias for the Claude Code /flow-impl command. Use when the user says
  flow-impl or /flow-impl to implement a frozen Agent Flow plan.
---

# Flow Impl

Use the repo-local `.claude/commands/flow-impl.md` command contract.

## Compatibility Contract

- Same artifact as Codex: `docs/flow/{feature_name}/implementation_report.md`.
- Same target resolution: if no argument is provided, use the most recently
  modified `docs/flow/*/plan.md`.
- Same gates: require frozen plan, required matrices, concrete waivers,
  approved current `plan-review.md`, onboarding docs, and Bug Feedback Review
  for bug/regression work.
- Same execution: task-by-task, TDD Red before Green for TDD tasks, update plan
  and implementation report after each task.
- Same evidence: run `/flow-integration-test` for visible or multi-step
  workflows before final review.

When this skill is invoked in Claude Code, execute `/flow-impl` semantics rather
than inventing a separate implementation flow.

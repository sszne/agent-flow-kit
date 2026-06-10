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
  `Plan Review Requirement`, approved current `plan-review.md` when review is
  required, onboarding docs, and Bug Feedback Review for bug/regression work.
- Same execution: task-by-task, TDD Red before Green for TDD tasks, update plan
  and implementation report after each task.
- Same evidence: choose the `/flow-integration-test` evidence lane before final
  review. Visible, multi-step, auth/session/permission/tenant,
  provider/device/deploy, external-side-effect, or high-impact workflows
  require full evidence or `BLOCKED`; low-risk non-visible changes may record
  lightweight evidence.

When this skill is invoked in Claude Code, execute `/flow-impl` semantics rather
than inventing a separate implementation flow.

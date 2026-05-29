---
name: flow-plan-review
description: |
  Alias for the Claude Code /flow-plan-review command. Use after flow-plan and
  before flow-impl/team-implement to review a frozen Agent Flow plan.
---

# Flow Plan Review

Use the repo-local `.claude/commands/flow-plan-review.md` command contract.

## Compatibility Contract

- Same artifact as Codex: `docs/flow/{feature_name}/plan-review.md`.
- Same target resolution: if no argument is provided, use the most recently
  modified `docs/flow/*/plan.md`.
- Same gate: behavior-changing implementation must not start until the current
  frozen plan has an approved, non-stale `plan-review.md`.
- Same cross-agent rule: review Codex-authored plans with Claude Code and
  Claude-authored plans with Codex, unless a concrete same-agent fallback reason
  is recorded.
- Same review focus: missed risks, DB/schema/migration, auth/permission,
  performance, dependencies/runtime, test coverage, concurrency, rollback,
  observability, privacy, rollout, stale docs, and waiver quality.

When this skill is invoked in Claude Code, execute `/flow-plan-review`
semantics rather than inventing a separate review flow.

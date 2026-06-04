---
name: flow-plan-review
description: |
  Alias for the Claude Code /flow-plan-review command. Use after flow-plan when
  review is required for high-impact work or requested as an optional readiness
  pass.
---

# Flow Plan Review

Use the repo-local `.claude/commands/flow-plan-review.md` command contract.

## Compatibility Contract

- Same artifact as Codex: `docs/flow/{feature_name}/plan-review.md`.
- Same target resolution: if no argument is provided, use the most recently
  modified `docs/flow/*/plan.md`.
- Same gate: high-impact implementation must not start until the current frozen
  plan has an approved, non-stale `plan-review.md`; smaller localized behavior
  changes may mark review optional with a concrete reason.
- Same high-impact rule: require review for multi-flow/cross-module work, auth
  or permission work, schema or migration work, deploy/CI/install/hooks/workflow
  gates, external providers or side effects, public API/shared runtime
  contracts, and user- or author-marked uncertain/high-impact work.
- Same optional-review rule: typo fixes, formatting-only edits, docs-only
  changes, and smaller localized behavior changes do not need review when they
  do not alter high-impact surfaces.
- Same workflow-doc rule: docs-only changes still need review when they update
  Agent Flow rules, skill behavior, gates, review policy, risky-path config, or
  required evidence.
- Same cross-agent rule: review Codex-authored plans with Claude Code and
  Claude-authored plans with Codex when review runs, unless a concrete
  same-agent fallback reason is recorded.
- Same review focus: missed risks, DB/schema/migration, auth/permission,
  performance, dependencies/runtime, test coverage, concurrency, rollback,
  observability, privacy, rollout, stale docs, and waiver quality.

When this skill is invoked in Claude Code, execute `/flow-plan-review`
semantics rather than inventing a separate review flow.

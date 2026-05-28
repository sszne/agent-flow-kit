---
name: flow-integration-test
description: |
  Alias for the Claude Code /flow-integration-test command. Use after
  flow-impl/team-implement for visible or multi-step business workflows.
---

# Flow Integration Test

Use the repo-local `.claude/commands/flow-integration-test.md` command contract.

## Compatibility Contract

- Same artifact as Codex:
  `docs/flow/{feature_name}/integration-test/{run_id}/`.
- Same required evidence: `index.html`, `result.md`, `test-review.md`,
  `business-flow-impact.md`, and major-step screenshots.
- Same gate result: `PASS`, `FAIL`, or `BLOCKED`.
- Same rule: blocked browser verification must be reported as `BLOCKED`, not as
  a pass.

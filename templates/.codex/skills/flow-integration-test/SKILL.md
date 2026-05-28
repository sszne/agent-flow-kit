---
name: flow-integration-test
description: |
  Run the Agent Flow Playwright integration evidence gate in Codex. Use when
  the user says /flow-integration-test or after flow-impl/team-implement for
  visible or multi-step business workflows.
---

# Flow Integration Test

Alias-compatible Codex entrypoint for the `integration-test` skill.

## Rules

- Activate `context-loader` first.
- Follow the `integration-test` skill contract.
- Read the frozen plan and implementation report.
- Save evidence under `docs/flow/{feature_name}/integration-test/{run_id}/`.
- Required evidence:
  - `index.html`
  - `result.md`
  - `test-review.md`
  - `business-flow-impact.md`
  - major-step screenshots
- Use Playwright Test as the deterministic pass/fail runner.
- If browser execution is blocked, mark the gate `BLOCKED` and name the
  unverified surface. Do not call it passed.

## Pass Criteria

- Required scenarios pass.
- Major-step screenshots exist and are linked.
- `index.html`, `test-review.md`, and `business-flow-impact.md` exist.
- Integration Coverage Contract evidence exists or has concrete waivers.
- No unhandled Critical or High findings remain.

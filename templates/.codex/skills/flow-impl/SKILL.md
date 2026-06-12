---
name: flow-impl
description: |
  Implement a frozen Agent Flow plan in Codex. Use when the user says
  /flow-impl, asks to implement the latest plan, or provides a
  docs/flow/{feature_name}/plan.md path.
---

# Flow Impl

Codex-native equivalent of Claude Code `/flow-impl`.

## Purpose

Execute a frozen `docs/flow/{feature_name}/plan.md` task by task, using TDD or
DIRECT execution as specified, then run integration evidence and review gates.

## Operating Rules

- Activate `context-loader` first.
- `$ARGUMENTS` is optional. If empty, resolve the most recently modified
  `docs/flow/*/plan.md` and announce the resolved path.
- If `$ARGUMENTS` is a plan path, use it directly. Otherwise treat it as
  `{feature_name}` and use `docs/flow/{feature_name}/plan.md`.
- Stop if no plan can be resolved, the plan is missing, or multiple latest plans
  are ambiguous.
- Require a frozen marker such as `<!-- frozen: v... -->`.
- Require the plan to include `Plan Review Requirement: Required` or
  `Optional` with a concrete reason. When review is required, require
  `docs/flow/{feature_name}/plan-review.md` to approve the current frozen
  marker before coding starts.
- Do not start behavior-changing implementation unless the frozen plan contains
  Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, and
  Integration Coverage Contract.
- Require onboarding docs for behavior-changing work:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- For bug/regression work, require Bug Feedback Review tasks before production
  implementation.
- Execute tasks one at a time in dependency order.
- For TDD tasks, write and run Red tests before production code.
- Keep implementation inside the frozen scope. Ask the user before introducing
  an unplanned behavior or design choice.
- Read repo-local `docs/agent-flow/design-principles.md` (and configured
  `design_principles_paths`) before external architecture references. During
  refactor/verify, re-check the anti-pattern rules: no vague-responsibility
  splits without named data/invariant ownership, no new
  Service/Manager/coordinator class without the plan's Service Introduction
  Rule evidence, and no aggregate-internal constraint implemented outside the
  aggregate.
- Update both `plan.md` and `implementation_report.md` after each completed
  task.
- Before final review, choose the `flow-integration-test` evidence lane.
  Visible, multi-step, auth/session/permission/tenant, provider/device/deploy,
  external-side-effect, or high-impact workflows require full evidence or
  `BLOCKED`; low-risk non-visible changes may record lightweight evidence.

## Workflow

```text
Phase 0: Resolve Plan
  latest docs/flow/*/plan.md when no argument is provided
    ->
Phase 1: Gate Check
  frozen marker + plan-review decision + required review when applicable
  + required matrices + onboarding docs + waivers
    ->
Phase 2: Red
  failing Feature/API integration, Unit, or browser-scenario coverage
    ->
Phase 3: Green
  smallest approved implementation
    ->
Phase 4: Refactor / Verify
  focused tests + lint/build + broader integration coverage
    ->
Phase 5: Integration Evidence
  flow-integration-test lane decision: full / lightweight / blocked
    ->
Phase 6: Report
  implementation_report.md + final summary with covered regression surfaces
```

## Implementation Report

Create or update `docs/flow/{feature_name}/implementation_report.md` with:

- plan version,
- completed tasks,
- files changed,
- Red/Green test results,
- integration and browser evidence,
- migration/runtime verification,
- Integration Coverage Contract rows satisfied or waived,
- remaining blockers or risks.

## Final Response

Report:

- what was implemented,
- validation commands and results,
- integration-test evidence lane, path if full, or concrete lightweight /
  `BLOCKED` / `N/A` reason,
- regression surfaces covered,
- remaining risks.

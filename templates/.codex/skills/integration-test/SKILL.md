---
name: integration-test
description: |
  Run and review Playwright integration-test evidence for a frozen flow plan.
  Use after implementation and before final team-review when visible or
  multi-step business behavior changed.
---

# Integration Test

Codex-native Playwright integration evidence gate.

Webwright decision: keep Playwright Test as the official pass/fail runner. Use Webwright-style code-as-action only as a scenario-crafting optimization for long browser flows, then promote the stable path into a deterministic Playwright Test spec.

## Purpose

Use this skill to verify implemented behavior through a real browser, preserve screenshot evidence, generate an `index.html` result summary, and review business-flow impact before passing the feature.

## Operating Rules

- Activate `context-loader` first.
- Read the frozen `docs/flow/{feature_name}/plan.md` and the implementation report.
- Use the local base URL documented in `.claude/rules/dev-environment.md`; prefer `http://localhost` when cookies/session behavior matters.
- Use Playwright Test for the official gate.
- For long or brittle flows, craft exploratory Playwright scripts in Webwright style to reduce step-by-step browser interaction, then convert the stable path into a Playwright Test spec.
- Save evidence under `docs/flow/{feature_name}/integration-test/{run_id}/`.
- Do not pass the gate if screenshots, `index.html`, test review, or business-flow impact review are missing.
- If Playwright is blocked by local browser/runtime constraints, report `BLOCKED` and do not call the integration test passed.

## Workflow

```text
Phase 1: Scope
  map Business Flow Matrix + Regression Surface Matrix + Test Design Matrix + Integration Coverage Contract
    ->
Phase 2: Execute
  craft Webwright-style exploratory script if useful, then run focused Playwright Test scenarios and capture major-step screenshots
    ->
Phase 3: Evidence
  create index.html + result.md
    ->
Phase 4: Review
  review scenario coverage + evidence completeness + business impact
    ->
Phase 5: Gate
  PASS / FAIL / BLOCKED
```

## Evidence Contract

Required output:

```text
docs/flow/{feature_name}/integration-test/{run_id}/
  index.html
  result.md
  test-review.md
  business-flow-impact.md
  screenshots/
```

`index.html` must include:

- feature name, plan version, run timestamp, base URL, branch/commit
- Playwright commands and exit status
- scenario table with PASS / FAIL / BLOCKED
- business-flow and regression-surface coverage
- Integration Coverage Contract coverage or explicit waivers
- ordered screenshot links/thumbnails
- console/network errors or "None observed"
- final gate status

## Pass Criteria

- All required Playwright scenarios pass.
- Required Feature/API integration, Unit, Browser, Migration, or waiver evidence exists for each Integration Coverage Contract row.
- Major steps have screenshots.
- `index.html`, `test-review.md`, and `business-flow-impact.md` exist.
- No unhandled Critical or High review findings remain.
- Medium findings are fixed, waived with reason, or converted to follow-up tasks.
- Blocked browser verification is reported as `BLOCKED`, not `PASS`.

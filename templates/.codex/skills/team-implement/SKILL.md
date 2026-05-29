---
name: team-implement
description: |
  Execute an approved frozen plan in Codex with TDD, business-flow coverage,
  integration coverage, and synchronized plan/report artifacts.
---

# Team Implement

Codex-native implementation workflow for `docs/flow/{feature_name}/plan.md`.

## Purpose

Use this after a plan is frozen and approved. The main Codex agent remains the manager: it owns synthesis, artifacts, verification, and final reporting.

## Operating Rules

- Activate `context-loader` first.
- Require a frozen plan marker: `<!-- frozen: v... -->`.
- Require an approved current `docs/flow/{feature_name}/plan-review.md`.
- Do not implement behavior-changing work unless the plan contains:
  - Business Flow Matrix
  - Regression Surface Matrix
  - Test Design Matrix
  - Integration Coverage Contract
- Require `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md` before behavior-changing implementation.
- Reject vague waivers such as `manual`, `low risk`, `TBD`, `later`, or blank waiver cells.
- For bug/regression work, require the plan's Bug Feedback Review to classify prior flow failure and list flow-improvement or bug-knowledge tasks before production implementation.
- Execute tasks in dependency order.
- For TDD tasks, write Red tests before production code.
- Keep implementation inside the approved scope. Ask the user if a new behavior or design choice is needed.
- Update both `plan.md` and `implementation_report.md` as tasks complete.
- For visible browser behavior or multi-step business workflows, run the `integration-test` skill after implementation and before final review.

## Workflow

```text
Phase 1: Gate Check
  verify frozen plan + matrices + task order
    ->
Phase 2: Red
  write failing Feature/API integration, Unit, or browser-scenario coverage
    ->
Phase 3: Green
  implement minimal approved change
    ->
Phase 4: Refactor
  lint/format + focused tests + broader verification
    ->
Phase 5: Integration Test
  Playwright evidence + index.html + test review + business impact review
    ->
Phase 6: Report
  update artifacts and summarize covered regression surfaces
```

## Phase 1: Gate Check

Read:

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/rules/testing.md`
- `.claude/docs/DESIGN.md`
- `docs/flow/{feature_name}/plan.md`

Stop before coding if:

- the plan is not frozen,
- `plan-review.md` is missing, stale, not approved, or same-agent without a
  concrete fallback reason,
- behavior-changing work lacks Business Flow Matrix,
- risky surfaces lack Test Design Matrix coverage,
- affected flows lack Integration Coverage Contract coverage or explicit waivers,
- required onboarding docs under `docs/agent-flow/` are missing,
- waivers are vague or lack concrete reasons/blockers,
- bug/regression work lacks Bug Feedback Review,
- schema changes lack migration enforcement notes.

## Phase 2: Red

For each TDD task:

1. Identify the related Business Flow Matrix row.
2. Identify the required Integration Coverage Contract row and case type.
3. Write the failing test first.
4. Run the focused test and confirm it fails for the expected reason.

Use project-specific commands from `.claude/rules/dev-environment.md`. Common Next.js examples:

```bash
pnpm test
pnpm test:integration
pnpm exec playwright test
```

Use Feature/API integration tests for routes, API handlers, auth/session, DB persistence, mail/PDF/export, job/queue entrypoints, external-boundary adapters, and shared workflow behavior. Use Unit tests for isolated helper/action/hook logic when it improves failure localization.

## Phase 3: Green

Implement the smallest change that passes the Red test.

Rules:

- Reuse existing shared partials, scripts, actions, services, and flows before adding local-only code.
- Do not add test-only production branches.
- Do not hide schema/data issues with broad defaults.
- Run the focused tests after the change.

## Phase 4: Refactor and Verify

Run the relevant checks:

```bash
pnpm lint
pnpm test
pnpm build
```

Broaden verification based on actual impact:

```bash
pnpm test:integration
pnpm exec playwright test
npm run build
```

For Laravel/PHP projects, use the equivalent PHPUnit/Pint/migration commands documented in the target repository. For visible behavior or multi-step business workflows, run Playwright integration evidence against the configured local base URL.

Required evidence:

- `docs/flow/{feature_name}/integration-test/{run_id}/index.html`
- major-step screenshots
- `test-review.md`
- `business-flow-impact.md`

If blocked, report `BLOCKED` and name the unverified surfaces. Do not claim the integration test passed.

## Phase 5: Report

Update `docs/flow/{feature_name}/implementation_report.md` with:

- completed tasks,
- files changed,
- tests and commands run,
- browser/migration verification,
- integration-test evidence index path,
- Integration Coverage Contract rows satisfied or waived,
- regression surfaces covered,
- remaining blockers or judgment items.

Final response should include:

```markdown
## Implementation Complete: {feature}

### Covered Regression Surfaces
- {flow/surface}: {test or verification}

### Validation
- PASS: {command}
- PASS/BLOCKED/N/A: {integration-test evidence path or reason}
- BLOCKED/N/A: {reason}

### Remaining Risks
- {risk or "None"}
```

# Testing Rules

Guidelines for testing behavior-changing work in this repository.

## Core Principles

- **TDD required for feature implementation**: write or update tests before implementation when behavior changes.
- **Impact-first test design**: start from implementation impact analysis and regression-risk inspection, not only the edited function.
- **Integration coverage required for risky changes**: routes, screens, API flows, shared Blade/JS, shared services/actions, schema/migrations, jobs, mail, PDFs, and status workflows need Feature, browser, or scenario-level coverage.
- **Focused unit tests are not enough for user-visible or shared behavior** unless the final report states the concrete low-risk reason.
- **Waivers must be concrete**: uncovered integration, browser, migration, side-effect, permission, or boundary coverage needs a clear reason or blocker. Vague waivers such as `manual`, `low risk`, `TBD`, `later`, or blank entries are not valid.
- **Migration consistency must be verified**: when code depends on a new schema shape, verify migration enforcement and validate against the migrated runtime.
- **Browser verification is required for visible behavior changes** unless a concrete blocker is reported.
- **Playwright integration evidence is required for visible or multi-step business workflows**: capture major-step screenshots, generate an `index.html` evidence summary, run test review, and complete business-flow impact review before passing.
- **Webwright-style browser work is only a scenario-crafting optimization**: use code-as-action exploratory scripts for long flows when it saves agent/browser turns, then promote the stable path into a deterministic Playwright Test spec.

## Test Levels

| Level | Use for | Commands |
| --- | --- | --- |
| Unit | Pure helpers, isolated services/actions/hooks, value transforms | Project test runner, e.g. `pnpm test`, `npm test`, `pytest`, or PHPUnit |
| Feature/API integration | Routes, API handlers, validation, auth/session, DB persistence, mail/PDF/export/job entrypoints, external-boundary adapters | Project integration runner, e.g. `pnpm test:integration`, `npm test -- --runInBand`, `pytest tests/integration`, or PHPUnit Feature tests |
| Browser / E2E | Screen transitions, modals, forms, tables, filters, displayed totals/statuses, auth redirects | Playwright/browser tools against the configured local base URL |
| Playwright integration evidence | User-visible or multi-step business workflows that need pass/fail evidence | `/flow-integration-test`, saving `docs/flow/{feature}/integration-test/{run_id}/index.html` |
| Webwright-style scenario crafting | Long or brittle browser flows where step-by-step agent interaction is inefficient | Exploratory Playwright script first, deterministic Playwright Test spec for the gate |
| Migration/runtime | New columns/tables/indexes, schema-dependent queries, deploy/startup assumptions | Project migration command plus deploy/startup enforcement check |

## Test Case Coverage

For each feature, cover:

1. Happy path: expected user or operator workflow.
2. Error cases: invalid input, forbidden transition, missing relation, validation failure.
3. Boundary values: empty, null, zero, min/max, date/time edge, long text, special characters.
4. Business workflow states: status transitions, mail side effects, PDF/export behavior, job/schedule behavior, and persisted snapshots.
5. Regression surfaces: existing routes, screens, APIs, shared partials/scripts, shared services/actions, schema-dependent paths, jobs, mail, PDFs.
6. Integration scenarios: feature-level flows proving affected entrypoints still work together.
7. Side effects: mail, PDF/export, jobs, audit logs, notifications, cache/search updates, and external API calls.

## Integration Test Style

Use Feature/API integration tests for behavior that crosses HTTP, DB, auth/session, events, mail, jobs, external-boundary adapters, or rendered views/components.

```ts
it("updates a todo only for the authenticated owner", async () => {
  // Arrange: create owner, another user, and existing todo.
  // Act: call the API or submit the form as the owner.
  // Assert: response, persisted state, and side effects.
});
```

Keep tests deterministic. Prefer factories/seed data scoped to the test over relying on local database state.

## Business Flow Matrix

Every implementation plan for non-trivial work must include a matrix like this before coding:

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Todo completion | Authenticated owner | `/todos` screen + `/api/todos/:id` | Owner marks todo complete | Missing todo, invalid status | Another user cannot update; empty title rejected | Activity log/cache update | Shared todo list could show stale state | Feature/API integration + browser |

This matrix is the bridge between business knowledge and test design. Do not skip it for order, dealer, company-order, mail, PDF, shipment, pricing, or search changes.

## Checklist

- [ ] Business flow and regression surface were explicitly inspected.
- [ ] Happy path is tested.
- [ ] Error cases are tested.
- [ ] Permission/ownership cases are tested.
- [ ] Boundary values are tested where meaningful.
- [ ] Side effects are asserted or explicitly out of scope.
- [ ] Feature/integration coverage exists for affected routes, screens, APIs, shared logic, schema-dependent paths, jobs, mail, and PDFs.
- [ ] Migration/schema changes were verified in a migrated runtime, including the enforcement path.
- [ ] Browser verification was run for visible behavior, or a concrete blocker was reported.
- [ ] Playwright major-step screenshots and `index.html` evidence exist for visible/multi-step workflows.
- [ ] Test review and business-flow impact review passed before final review.
- [ ] Tests are independent and deterministic.
- [ ] External dependencies are faked/mocked at the boundary.
- [ ] Final report names the regression surface covered by the tests.
- [ ] Any waiver has a concrete reason or blocker and is not a vague low-risk statement.

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
- **Provider/deploy happy paths need their own evidence lane**: local mocks,
  invalid/preflight checks, unauthenticated `401`, and health endpoints are
  useful but do not prove a real provider callback, deployed artifact, real
  device/app context, valid credential/session path, mail delivery, storage
  write, or other side effect.
- **Playwright integration evidence is required for high-value evidence lanes**: visible UI, multi-step business workflows, auth/session/permission/tenant behavior, provider/device/deploy behavior, external side effects, and high-impact release confidence require full `flow-integration-test` evidence or an explicit `BLOCKED` report.
- **Lightweight evidence is allowed only for low-risk non-visible work**: API-only, internal logic, docs/skill-only, static/build-only, or equivalent changes may use focused substitute evidence when the report records the concrete reason, substitute commands/reviews, and covered regression surface. It must not bypass visible, provider/deploy, auth/session, permission/tenant, external-side-effect, or high-impact evidence requirements.
- **Integration-test usefulness must be measurable**: full, lightweight, and blocked lanes should record `evidence_lane`, issue count/severity, whether a fix resulted, fix reference, whether another test would have caught it, elapsed time when available, token/work overhead when available, and blocker category.
- **Webwright-style browser work is only a scenario-crafting optimization**: use code-as-action exploratory scripts for long flows when it saves agent/browser turns, then promote the stable path into a deterministic Playwright Test spec.

## Test Levels

| Level | Use for | Commands |
| --- | --- | --- |
| Unit | Pure helpers, isolated services/actions/hooks, value transforms | Project test runner, e.g. `pnpm test`, `npm test`, `pytest`, or PHPUnit |
| Feature/API integration | Routes, API handlers, validation, auth/session, DB persistence, mail/PDF/export/job entrypoints, external-boundary adapters | Project integration runner, e.g. `pnpm test:integration`, `npm test -- --runInBand`, `pytest tests/integration`, or PHPUnit Feature tests |
| Browser / E2E | Screen transitions, modals, forms, tables, filters, displayed totals/statuses, auth redirects | Playwright/browser tools against the configured local base URL |
| Playwright integration evidence | User-visible, multi-step, auth/session/permission/tenant, provider/device/deploy, external-side-effect, or high-impact workflows that need pass/fail evidence | `/flow-integration-test`, saving `docs/flow/{feature}/integration-test/{run_id}/index.html` |
| Lightweight integration evidence | API-only, internal logic, docs/skill-only, static/build-only, or other non-visible low-risk changes | Focused commands/reviews plus recorded evidence lane, reason, substitute evidence, and covered regression surface |
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
8. Provider/deploy lanes: deployed artifact/version, real provider/device
   happy path, valid credential/session smoke, and concrete blockers when these
   cannot run.
9. Evidence-lane metrics: issues found, fixes caused, elapsed time when
   available, token/work overhead when available, and blocker category.

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
- [ ] Provider/auth/deploy risks distinguish local mock evidence from deployed
      artifact, real provider/device, valid credential/session, and blocked
      valid-path evidence.
- [ ] Full `flow-integration-test` evidence exists for visible, multi-step, auth/session/permission/tenant, provider/device/deploy, external-side-effect, and high-impact workflows, or `BLOCKED` names the exact unverified surface and minimum unblock action.
- [ ] Lightweight evidence, when used, records the low-risk reason, substitute commands/reviews, covered regression surface, and does not skip a high-risk full-gate surface.
- [ ] Effectiveness metrics are recorded: `evidence_lane`, issues found, fix result, fix reference, other-test catch likelihood, elapsed time when available, token/work overhead when available, and blocker category.
- [ ] Test review and business-flow impact review passed before final review.
- [ ] Tests are independent and deterministic.
- [ ] External dependencies are faked/mocked at the boundary.
- [ ] Final report names the regression surface covered by the tests.
- [ ] Any waiver has a concrete reason or blocker and is not a vague low-risk statement.

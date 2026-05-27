# Agent Flow Residual Risk Countermeasures

## Purpose

Agent Flow reduces implementation bugs and regressions by forcing investigation,
business-flow mapping, integration coverage design, TDD, browser evidence, and
review gates before behavior-changing work is treated as complete.

However, a workflow cannot fully remove bugs by itself. Some risks require
project-specific knowledge, runtime parity, test infrastructure, external
service controls, and reviewer discipline. This document records why those
risks remain and what should be prepared to reduce them further.

## Summary

| Residual risk | Why the flow alone cannot solve it | Required countermeasure |
| --- | --- | --- |
| Business flows are missed during discovery | The flow can ask for and structure knowledge, but it cannot know unstated business rules or hidden operator behavior | Domain-owner review, production examples, operation docs, issue history, logs, and mandatory onboarding docs |
| CI cannot fully judge natural-language plan quality | The matrix gate can detect missing sections, placeholders, and weak waivers, but cannot prove semantic completeness | More structured plan fields, stable flow IDs, schema validation, and reviewer sign-off |
| External APIs, async jobs, mail, PDF, auth, and migrations are hard to reproduce locally | The flow can require coverage, but the runtime may lack real dependencies or production-like data | Staging/sandbox environments, fakes, local service containers, deterministic seed data, and artifact capture |
| Target project has weak test infrastructure | The flow can require tests, but cannot invent reliable factories, fixtures, auth helpers, or integration runners | Test harness investment before feature work, including DB reset, auth/session helpers, and external-boundary mocks |
| Reviewers may accept incomplete coverage | The flow can add checklists and gates, but human reviewers can still miss weak assertions or bad waivers | Findings-first review discipline, required evidence links, anti-waiver rules, and ownership-based review |

## Flow-Plan Detection

`/flow-plan` must run a Residual Risk Preflight before freezing a behavior-changing
plan. The preflight does not block all risk by default; it classifies the user's
request and decides whether to warn, ask questions, add setup tasks, or mark a
blocker.

Use these risk IDs in `docs/flow/{feature_name}/plan.md`:

| Risk ID | Category | When to warn |
| --- | --- | --- |
| RR-001 | Missed business flows | The request changes business workflow, ownership, status, pricing, order, mail/PDF/export, jobs, or lifecycle behavior |
| RR-002 | Natural-language plan quality | The plan spans multiple flows/modules, uses many waivers, or relies on broad natural-language assertions |
| RR-003 | Runtime/external dependency gap | The request touches external APIs, payments, webhooks, queues, mail, PDF rendering, storage, search, cache, auth providers, or migrations |
| RR-004 | Weak test infrastructure | The repo lacks factories, fixtures, auth helpers, DB reset, integration runner, Playwright setup, or stable selectors |
| RR-005 | Reviewer/waiver quality | Verification may become manual-only, low-risk claims are present, or critical auth/data/migration behavior is affected |

When a risk applies, the plan should include:

- why the risk applies,
- warning shown to the user,
- additional requirement questions if needed,
- required environment or setup task,
- blocker or waiver reason if the risk cannot be resolved before implementation.

## 1. Missed Business Flows

### Why the Flow Cannot Fully Handle This

Business rules often live outside code:

- operator habits that are not documented,
- spreadsheet or manual back-office steps,
- customer-support exceptions,
- data cleanup scripts,
- historical bugs that shaped current behavior,
- edge cases known only to domain owners.

Agent Flow can require `Business Flow Matrix`, `Regression Surface Matrix`, and
`Integration Coverage Contract`, but it cannot infer business knowledge that is
not present in source code, docs, tests, logs, or user answers.

### Required Elements

Prepare these before behavior-changing work:

- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- domain-owner review for high-risk flows
- examples of real user/operator workflows
- known incident or regression history
- production or staging route/API inventory
- list of side effects: mail, PDF/export, jobs, audit logs, notifications, cache/search updates, external APIs

### Concrete Examples

For an authenticated TODO feature:

- Confirm actors: owner user, another user, admin/support user.
- Confirm ownership rule: users can only update their own TODOs.
- Confirm lifecycle: create, complete, reopen, delete, restore if applicable.
- Confirm side effects: activity log, notification, cache invalidation.
- Confirm regression surface: list screen, detail screen, API route, auth middleware, DB schema, audit log.

For an order-management feature:

- Confirm status transitions and forbidden transitions.
- Confirm mail/PDF/export side effects.
- Confirm whether partial updates preserve shipping, memo, pricing, and tax fields.
- Confirm whether dealer/company/customer scope changes visibility.

## 2. Natural-Language Plan Quality

### Why the Flow Cannot Fully Handle This

The matrix gate can check:

- required sections exist,
- sections have table rows,
- template placeholders are removed,
- `Integration Coverage Contract` includes required case types,
- weak waivers are rejected.

It cannot fully prove that a natural-language row is correct. For example,
`permission covered by TEST-002` may be syntactically valid, but the actual test
could assert the wrong permission rule.

### Required Elements

To reduce this risk further, add more structure:

- stable flow IDs such as `FLOW-001`,
- stable test IDs such as `TEST-001`,
- explicit `Covers flow/risk` references,
- machine-readable plan metadata when useful,
- schema validation for required columns,
- required reviewer sign-off for high-risk flows.

### Concrete Examples

Minimum structured traceability:

```markdown
| Flow ID | Flow | Required coverage |
| --- | --- | --- |
| FLOW-001 | Owner completes TODO | TEST-001, TEST-002, PW-001 |

| Test ID | Case type | Covers flow/risk |
| --- | --- | --- |
| TEST-002 | Permission | FLOW-001 cross-owner update |
```

Stronger future option:

```json
{
  "flow_id": "FLOW-001",
  "required_case_types": ["happy", "validation", "permission", "boundary", "side_effect", "regression"],
  "evidence": ["TEST-001", "TEST-002", "PW-001"]
}
```

## 3. Runtime and External Dependency Gaps

### Why the Flow Cannot Fully Handle This

Some behavior cannot be verified accurately unless the environment exists:

- real or sandbox external APIs,
- queue workers,
- scheduled jobs,
- mail delivery or mail capture,
- PDF/rendering dependencies,
- object storage,
- search indexes,
- cache/Redis,
- auth/session provider behavior,
- migrated database runtime.

Agent Flow can require verification or a blocker, but it cannot make a missing
runtime dependency behave correctly.

### Required Environment

Prepare a local or staging environment with:

- deterministic database seed/reset,
- migration command and deploy/startup enforcement path,
- queue worker execution path,
- mail capture service,
- object storage emulator,
- external API sandbox or mocked boundary,
- browser-accessible local URL,
- Playwright installed and runnable,
- screenshot, trace, and HTML report storage.

### Concrete Examples

For a Next.js app:

- `pnpm test` for unit tests.
- `pnpm test:integration` for API/route handler integration tests.
- `pnpm exec playwright test` for browser evidence.
- Prisma: `pnpm prisma migrate deploy` or project equivalent.
- Drizzle: `pnpm drizzle-kit migrate` or project equivalent.
- Mail: Mailpit/MailHog for capture.
- Storage: MinIO for S3-compatible local storage.
- External API: MSW, Nock, WireMock, or provider sandbox.
- Queue: Redis + BullMQ worker in Docker Compose.

For payment or billing:

- Stripe test mode or provider sandbox.
- Webhook signature verification in test.
- Replayable webhook fixtures.
- Idempotency tests for duplicate webhook delivery.

For search:

- OpenSearch/Elasticsearch local container or mocked adapter.
- Index refresh/rebuild command.
- Tests for stale index or missing document behavior.

## 4. Weak Test Infrastructure

### Why the Flow Cannot Fully Handle This

The flow can require Feature/API integration tests and browser evidence, but
tests will still be unreliable if the project lacks:

- factories,
- fixtures,
- isolated DB reset,
- auth/session helpers,
- external-boundary mocks,
- stable selectors,
- deterministic clock/timezone,
- reproducible local services.

Without these, agents may write broad manual checks or brittle tests.

### Required Elements

Before large behavior-changing work, prepare:

- test DB reset strategy,
- factory/fixture strategy,
- auth helper for each role/scope,
- seed data for Playwright scenarios,
- stable `data-testid` or role/label based selectors,
- fake timers or fixed clock,
- external service fakes at the adapter boundary,
- test commands documented in `.claude/rules/dev-environment.md`.

### Concrete Examples

Authenticated TODO:

- Factory: `createUser()`, `createTodo({ ownerId })`.
- Auth helper: `signInAs(user)` for Playwright and API tests.
- Permission test: another user receives `403` or not-found behavior, and the TODO is unchanged.
- Boundary test: empty title, very long title, duplicate title if relevant.
- Side-effect test: activity log row exists only after successful update.

Browser test:

- Seed owner and TODO before test.
- Open `/todos`.
- Capture screenshot before action.
- Click complete.
- Capture screenshot after completion.
- Assert visible completed state and API/database state.
- Save result to `docs/flow/{feature}/integration-test/{run_id}/index.html`.

## 5. Reviewer and Waiver Quality

### Why the Flow Cannot Fully Handle This

Review gates improve recall, but reviewers can still:

- miss a weak assertion,
- accept a vague waiver,
- focus only on changed files,
- skip adjacent workflows,
- trust a passing test without checking what it proves.

Agent Flow reduces this with `team-review`, strict waiver rules, and evidence
requirements, but reviewer judgment remains a human/process dependency.

### Required Elements

Use these controls for high-risk changes:

- findings-first review,
- required review against `Business Flow Matrix`,
- required review against `Integration Coverage Contract`,
- no vague waivers,
- evidence links for each required test,
- CODEOWNERS or domain-owner review for critical flows,
- CI-required checks for test commands and Playwright evidence,
- follow-up issues for accepted residual risks.

### Concrete Examples

Invalid waiver:

```text
manual
low risk
TBD
later
```

Valid waiver:

```text
out of scope because this change only updates copy in a static footer and no runtime entrypoint, data mutation, auth rule, or side effect is affected.
```

Valid blocker:

```text
blocked by missing payment-provider sandbox credentials; webhook duplicate-delivery coverage must be added before release.
```

## Recommended Readiness Checklist

Before behavior-changing implementation:

- [ ] `agent-flow-onboarding` has produced all three required docs.
- [ ] High-risk business flows have domain-owner confirmation.
- [ ] `Business Flow Matrix` includes normal, exception, permission, boundary, side-effect, and regression concerns.
- [ ] `Integration Coverage Contract` maps every affected flow to evidence or a concrete blocker.
- [ ] No vague waivers remain.
- [ ] Project-specific test commands are documented.
- [ ] Local/staging services needed for integration tests are available.
- [ ] Playwright can capture screenshots and produce `index.html` evidence for visible workflows.

Before release or merge:

- [ ] Unit tests pass.
- [ ] Feature/API integration tests pass.
- [ ] Migration/runtime enforcement is verified when schema changes exist.
- [ ] Browser evidence exists for visible or multi-step workflows.
- [ ] `test-review.md` and `business-flow-impact.md` are complete.
- [ ] `team-review` has checked security, quality, tests, matrix coverage, and waiver quality.

## Future Hardening Options

These are not required for the base kit, but can reduce residual risk further:

- Convert the plan matrices into machine-readable YAML or JSON blocks.
- Add schema validation for flow IDs, test IDs, and evidence links.
- Require CODEOWNERS/domain-owner sign-off for selected flows.
- Upload Playwright evidence as CI artifacts.
- Run contract tests against external-service sandboxes.
- Add nightly regression suites for high-risk business flows.
- Track production incidents back to missing flow rows or missing test case types.

---
name: business-flow-integration-test
description: |
  Create, update, or run a callable regression suite for major business-flow
  operation tests after Agent Flow onboarding. Use after onboarding when the
  user wants end-to-end business flows to become executable integration tests.
---

# Business Flow Integration Test

Create and run an onboarding-derived business-flow integration regression
suite. This is the baseline suite for major continuous operations in the
repository, not the feature-specific `flow-integration-test` evidence gate that
runs after `flow-impl`.

## Purpose

Turn confirmed `docs/agent-flow/business-flows.md` and
`docs/agent-flow/integration-scenarios.md` knowledge into executable operation
tests that can be run together to catch regressions in primary business
journeys.

Examples of the expected scenario shape:

- registration -> account verification -> first login
- logout -> login
- survey creation -> coupon creation -> campaign creation with survey/coupon
  links -> scheduled delivery -> delivered URL opens the target campaign

## When This Helps

Use this skill when the real risk is not an isolated function but whether a
business operation can still complete end to end.

It is most useful:

- right after onboarding, while the primary business-flow knowledge is fresh,
  to turn "what must not break" into executable baseline tests;
- before releases, to confirm auth, registration, delivery, reservation,
  order, payment, search, or other multi-step flows still work;
- after changing shared foundations such as auth middleware, permissions, API
  clients, schema, date/time logic, mail, delivery, jobs, or provider wiring;
- after larger refactors, to prove user-visible business outcomes survived the
  internal restructuring;
- after a repeated or costly regression, to make that full operation part of
  the standard regression route;
- when onboarding new engineers or agents, because
  `docs/agent-flow/business-flow-integration-tests.md` becomes a living
  specification of the main operations and how to run them.

Do not use this for small copy/style changes or isolated unit-level behavior.
Those should stay covered by focused unit, API, or feature tests. The split is:
`flow-integration-test` proves the current implementation plan, while
`business-flow-integration-test` proves the product's main business operations
still work as a baseline suite.

## Prerequisites

- Activate `context-loader` first.
- Required onboarding docs exist:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/source-documents.md` may exist as sidecar evidence.
- The target repo has a runnable app or API test environment, or the blocker is
  recorded before any scenario is called passable.

## Positioning

- Use this after `agent-flow-onboarding`, or later when refreshing the baseline
  business-flow regression suite.
- Do not automatically run this from `flow-impl`; invoke this skill or the
  registered runner deliberately.
- Use `flow-integration-test` for feature-specific post-implementation
  evidence under `docs/flow/{feature}/integration-test/{run_id}/`.
- Use this skill for project-wide baseline operation tests under
  `docs/agent-flow/business-flow-integration-test-runs/{run_id}/`.

## Modes

- `create` or no explicit mode: infer, confirm, create tests, register runner,
  and optionally run the suite.
- `update`: revise the suite when business flows, test infrastructure, or
  primary operations change.
- `run`: execute the registered all-suite command and collect evidence.

## Operating Rules

- Start from confirmed business flows and regression surfaces, not edited files.
- Do not create or modify executable tests until the user approves the final
  scenario list.
- Treat source-document claims that are `conflicts-with-repo`, `aspirational`,
  `stale-or-unknown`, or `needs-user-confirmation` as questions or gaps, not as
  required executable tests.
- Prefer the repository's existing Playwright, browser, Feature/API, seed, and
  reset conventions.
- Use Playwright for visible or multi-step browser behavior. Use API/feature
  integration tests where browser adds little value.
- Separate deterministic local/mock evidence from real provider, device,
  deployed-domain, mail, webhook, storage, scheduled job, or side-effect
  evidence.
- If a scenario cannot run because required data, credentials, time controls,
  provider sandbox, browser runtime, or deployed environment is unavailable,
  mark that scenario `BLOCKED`; do not call the suite passed.

## Workflow

```text
Phase 1: Scope
  read onboarding docs -> inspect existing test runner, seed/reset, auth helpers,
  local server commands, provider constraints, and package scripts
    ->
Phase 2: Infer
  draft major continuous operation tests from business flows and integration
  scenarios; group by actor and business outcome
    ->
Phase 3: Confirm
  present the inferred test list, ask about unclear operations, accept missing
  operations from the user, and get explicit approval of the final list
    ->
Phase 4: Create Or Update
  write suite spec -> create executable specs following repo conventions ->
  register an all-suite runner command
    ->
Phase 5: Execute
  run the suite when requested -> collect screenshots/logs/reports ->
  write evidence and gate decision
```

## Phase 1: Scope

Read:

- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/source-documents.md` when present
- existing test files, Playwright/Cypress/test config, package scripts, CI
  commands, seed/reset scripts, auth helpers, and local dev rules

Identify:

- target actors and permissions,
- primary happy paths and required exception paths,
- account/session setup,
- seed data and reset strategy,
- scheduled/time-based behavior,
- provider/device/deployed-domain requirements,
- where the all-suite runner should live.

## Phase 2: Infer Scenario Candidates

Create a candidate table before asking for approval:

| Candidate ID | Business flow | Actor | Continuous operation | Start state / data | Steps | Expected result | Test level | Open questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Scenario candidates should represent complete business outcomes, not isolated
button clicks. Prefer a small high-value set that protects primary revenue,
auth, permission, status, delivery, or side-effect flows.

## Phase 3: User Confirmation Gate

Before writing executable tests, present:

- the candidate table,
- assumptions about data, accounts, time, providers, and permissions,
- unclear operations as concise questions,
- missing coverage candidates the user may add,
- the proposed runner command and evidence path.

Stop and wait for the user when:

- the actor, permission, success state, side effect, or operation order is
  unclear,
- the scenario depends on real credentials or provider behavior,
- a destructive or costly side effect could be triggered,
- the user has not approved the final test list.

Proceed only after explicit approval of the final scenario list.

## Phase 4: Create Or Update The Suite

Write or update:

```text
docs/agent-flow/business-flow-integration-tests.md
```

Use this suite-spec structure:

```markdown
# Business Flow Integration Tests

## Purpose
## Confirmed Scenario Inventory
| Scenario ID | Business flow | Actor | Operation | Level | Runner target | Status |
| --- | --- | --- | --- | --- | --- | --- |

## User Confirmation
- Approved by:
- Approved at:
- Added operations:
- Deferred / blocked operations:

## Data, Seed, And Reset Strategy
## Environment And Provider Requirements
## Runner Registration
- All-suite command:
- Test file roots:
- Evidence root:

## Scenario Details
### BFIT-001 ...
## Coverage Gaps
## Maintenance Notes
```

Create executable tests using existing repo conventions. If no convention
exists, prefer:

```text
tests/business-flow/
```

Register an all-suite runner. Prefer an existing project-native script. When a
JavaScript package script is appropriate, use a clear name such as:

```text
agent-flow:business-flow-tests
```

When a package script is not appropriate, create or document a dedicated runner
such as:

```text
scripts/run-business-flow-integration-tests.sh
```

Do not hide long-running suites inside ordinary unit-test commands unless the
user explicitly asks for that CI behavior.

## Phase 5: Run Mode

When invoked to run, read
`docs/agent-flow/business-flow-integration-tests.md`, resolve the registered
all-suite command, execute it, and save evidence under:

```text
docs/agent-flow/business-flow-integration-test-runs/{YYYYMMDD-HHMMSS}/
  index.html
  result.md
  test-review.md
  business-flow-impact.md
  screenshots/
  reports/              # optional copied Playwright/API reports
  traces/               # optional traces/videos/logs
```

`index.html` must include:

- run timestamp, branch/commit, base URL, command, and exit status,
- scenario table with PASS / FAIL / BLOCKED,
- linked screenshots/reports/logs,
- business-flow and regression-surface coverage,
- console/network/provider errors or "None observed",
- final suite status.

## Pass Criteria

- The final approved scenario list exists in
  `docs/agent-flow/business-flow-integration-tests.md`.
- The all-suite runner command exists and was executed.
- Every runnable approved scenario passes.
- Blocked scenarios name the concrete blocker and affected business surface.
- Required screenshots or API reports exist for each scenario type.
- `index.html`, `result.md`, `test-review.md`, and
  `business-flow-impact.md` exist for the run.
- No unhandled Critical or High findings remain.

## Final Report

Report:

- suite spec path,
- runner command,
- scenarios created/updated/run,
- final PASS / FAIL / BLOCKED status,
- evidence path,
- blockers and follow-up operations.

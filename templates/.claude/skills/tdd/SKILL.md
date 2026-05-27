---
name: tdd
description: Implement features using Test-Driven Development with impact-first test design, integration coverage, and browser verification when needed.
disable-model-invocation: true
---

# TDD

Implement `$ARGUMENTS` using a Red -> Green -> Refactor cycle that starts from business-flow impact analysis.

## Required Context

Before writing tests:

1. Read `CLAUDE.md`, `AGENTS.md`, `.claude/rules/testing.md`, and `.claude/docs/DESIGN.md`.
2. Inspect existing related routes, controllers, models, views, migrations, jobs, mail, PDFs, shared partials/scripts, and tests.
3. Reuse existing shared implementations before adding screen-specific logic.

## Phase 1: Test Design Gate

Create or update the plan/report with these sections before implementation:

### Business Flow Matrix

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {flow} | {role/scope} | {route/screen/API/job/mail/pdf} | {happy workflow} | {validation/missing/external failure} | {forbidden/cross-scope/null/min/max} | {mail/PDF/export/job/cache/search} | {risk} | {Feature/API integration, Unit, Browser/Migration} |

### Test Case List

- [ ] Feature/API integration: happy path for the primary entrypoint
- [ ] Feature/API integration: validation, missing relation, or external-boundary failure path
- [ ] Feature/API integration: permission, ownership, tenant, or cross-scope failure path
- [ ] Feature/API integration: boundary value or lifecycle/status transition path
- [ ] Feature/API integration: affected shared workflow still preserves existing behavior
- [ ] Feature/API integration: side effects such as mail/PDF/export/job/audit/cache/search are asserted or explicitly out of scope
- [ ] Unit: pure helper/action logic, if any
- [ ] Browser: visible or multi-step behavior, if any
- [ ] Migration/runtime: schema enforcement, if any

Do not start Green implementation until the Red tests are identified.

## Phase 2: Red

Write the smallest meaningful failing test first.

Use the project-specific commands from `.claude/rules/dev-environment.md`. Common Next.js examples:

```bash
pnpm test
pnpm test:integration
pnpm exec playwright test
```

Confirm the test fails for the expected reason. If the test cannot fail because the behavior already exists, record that and move to the next uncovered risk.

## Phase 3: Green

Implement the smallest change that passes the failing test.

Rules:

- Keep changes scoped to the approved behavior.
- Reuse shared partials, scripts, actions, services, and existing flows first.
- Do not add test-only production branches.
- Do not hide data/schema issues with broad defaults.

Run the focused test again and confirm it passes.

## Phase 4: Refactor

Clean up while tests stay green.

```bash
pnpm lint
pnpm test
```

Broaden verification based on impact:

- Changed route/API handler/shared behavior: relevant Feature/API integration tests
- Changed visible UI: browser verification against the configured local base URL
- Changed frontend assets: `npm run build` or the project equivalent
- Changed schema: migration command and migration enforcement check
- Laravel/PHP projects: use equivalent PHPUnit/Pint/migration commands from the target repository

## Completion Report

```markdown
## TDD Complete: {Feature Name}

### Business Flow Coverage
- {flow}: covered by {test/browser check}

### Tests
- PASS: {command}
- PASS/blocked: {browser or migration verification}

### Implementation Files
- `{file}`: {summary}

### Remaining Risks
- {risk or "None"}
```

Final reports must name the regression surface covered. If integration/browser coverage is omitted, state the concrete low-risk reason or blocker.

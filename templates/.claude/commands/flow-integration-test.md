Specification-Driven Development: Integration Test Evidence Gate

Run deterministic Playwright integration tests after implementation and before final review. This command creates visual evidence, summarizes results in `index.html`, performs a test review, and decides whether the feature may pass.

Webwright decision: do not use autonomous Webwright runs as the sole pass/fail gate. Use Webwright-style code-as-action exploration only to reduce agent browser-interaction cost when crafting long or fragile Playwright scenarios, then convert the stable path into a deterministic Playwright Test spec.

## Rules

- Use this command after `/flow-impl` or `team-implement` when behavior-changing work affects screens, routes, forms, modals, tables, filters, auth redirects, displayed values, or multi-step business workflows.
- Use the local base URL documented in `.claude/rules/dev-environment.md`; prefer `http://localhost` when cookies/session behavior matters.
- Use Playwright Test as the official deterministic runner.
- For long-horizon flows, use Webwright-style script crafting: write exploratory Playwright scripts, inspect screenshots/logs, then promote the stable script into a Playwright Test spec with explicit assertions.
- Do not mark the feature as passed unless:
  - required Playwright scenarios passed,
  - major steps have screenshots,
  - `index.html` summarizes the test evidence,
  - test review found no unhandled Critical or High issues,
  - business-flow impact review is complete.
- If browser execution is blocked, mark the gate as `BLOCKED`, write the blocker into the evidence report, and do not claim integration-test pass.
- Generated evidence belongs under `docs/flow/{feature_name}/integration-test/{run_id}/`.

## Prerequisites

- `docs/flow/{feature_name}/plan.md` exists and is frozen.
- `docs/flow/{feature_name}/implementation_report.md` exists.
- Docker stack is running and the app is reachable at `http://localhost`.
- Playwright CLI or MCP browser tooling is available.

## Directory Structure

```text
docs/flow/{feature_name}/integration-test/{YYYYMMDD-HHMMSS}/
  index.html
  result.md
  test-review.md
  business-flow-impact.md
  screenshots/
    01-{scenario}-{step}.png
    02-{scenario}-{step}.png
  playwright-report/        # optional copied Playwright HTML report
  traces/                   # optional traces/videos/failure artifacts
```

---

## Phase 1: Scope

Read:

- `docs/flow/{feature_name}/plan.md`
- `docs/flow/{feature_name}/implementation_report.md`
- `.claude/rules/testing.md`
- `.claude/docs/DESIGN.md`

Extract required scenarios from:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- Playwright Integration Test Plan, if present

Create a scenario table before running:

| Scenario ID | Business flow | Entry point | Major steps requiring screenshots | Expected result | Risk covered |
| --- | --- | --- | --- | --- | --- |
| PW-001 | {flow} | {URL} | {step names} | {expected state} | {risk} |

If a risky affected flow has no Playwright scenario and no documented low-risk reason, stop and update the plan.
If a risky affected flow has no Feature/API integration coverage for its required exception, permission, boundary, side-effect, or regression cases, stop and update the plan or implementation report before browser-only verification.

---

## Phase 2: Craft or Execute Playwright

Run the most focused Playwright spec that covers the scenarios.

If no stable spec exists yet and the flow is long or fragile, first craft it in Webwright-style:

1. Write an exploratory Playwright script in the run workspace.
2. Use functions, locators, waits, and loops instead of repeated manual browser actions.
3. Save exploratory screenshots/logs.
4. Convert the stable path into a Playwright Test spec under `test/playwright-cli/tests/`.
5. Run the Playwright Test spec as the gate.

Default command shape:

```bash
cd test/playwright-cli
TEST_BASE_URL=http://localhost npx playwright test tests/{spec}.spec.js --reporter=list,html
```

For each scenario:

1. Navigate to the entrypoint.
2. Capture a screenshot before the first meaningful action.
3. Execute each major business step.
4. Capture a screenshot after every required major step.
5. Assert the expected final state.
6. Record console errors, network failures, and validation messages when available.

Screenshot naming:

```text
screenshots/{NN}-{scenario_id}-{step_slug}.png
```

Major steps must be named in business language, for example:

- `open-order-list`
- `filter-status`
- `open-detail-modal`
- `submit-status-change`
- `confirm-updated-total`

---

## Phase 3: Build Evidence Index

Create `docs/flow/{feature_name}/integration-test/{run_id}/index.html`.

The HTML must include:

- Feature name, plan version, run timestamp, base URL, branch/commit if available
- Commands executed and exit status
- Scenario summary table with PASS / FAIL / BLOCKED
- Business Flow Matrix coverage table
- Regression Surface Matrix coverage table
- Links or embedded thumbnails for screenshots in execution order
- Console/network errors or "None observed"
- Links to Playwright HTML report, traces, videos, or failure artifacts when available
- Final gate status: `PASS`, `FAIL`, or `BLOCKED`

Also write `result.md` with the same high-level summary for quick reading in text-only environments.

---

## Phase 4: Test Review

Perform a test review before passing the gate.

Review perspectives:

1. **Scenario Coverage Reviewer**
   - Does every affected Business Flow Matrix row have a Playwright or Feature/API integration coverage path?
   - Does every Integration Coverage Contract row have required Feature/API integration, Unit, Browser, Migration, or waiver evidence?
   - Are error, validation, permission, and boundary cases covered by Playwright or project integration tests?
   - Are explicit waivers reasonable?

2. **Evidence Reviewer**
   - Do screenshots prove the major user-visible steps?
   - Does `index.html` link to all relevant screenshots and reports?
   - Are console/network failures captured or stated as none?

3. **Business Impact Reviewer**
   - Which adjacent workflows could regress?
   - Are shared routes, screens, partials, scripts, services, mail/PDF/job paths, and status transitions covered or explicitly out of scope?
   - Is the remaining risk acceptable?

Write findings to:

```text
docs/flow/{feature_name}/integration-test/{run_id}/test-review.md
docs/flow/{feature_name}/integration-test/{run_id}/business-flow-impact.md
```

Findings format:

```markdown
## Findings
- [Critical/High/Medium/Low] {finding}

## Coverage Decision
- Business flow coverage: PASS / FAIL / BLOCKED
- Evidence completeness: PASS / FAIL / BLOCKED
- Remaining risk: {None or explanation}
```

---

## Phase 5: Gate Decision

Pass only when all conditions are satisfied:

- [ ] All required Playwright scenarios pass.
- [ ] Major-step screenshots exist and are linked from `index.html`.
- [ ] `index.html` has final status `PASS`.
- [ ] `test-review.md` exists.
- [ ] `business-flow-impact.md` exists.
- [ ] No unhandled Critical or High findings remain.
- [ ] Medium findings are fixed, waived with reason, or converted to follow-up tasks.
- [ ] Any blocked browser evidence is explicitly reported as `BLOCKED`, not `PASS`.

Update `docs/flow/{feature_name}/implementation_report.md` with:

- Playwright command(s)
- Evidence index path
- Test review result
- Business-flow impact result
- Final gate status

## User Requirements

$ARGUMENTS

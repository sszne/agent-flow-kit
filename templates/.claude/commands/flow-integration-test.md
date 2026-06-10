Specification-Driven Development: Integration Test Evidence Gate

Run deterministic Playwright integration tests after implementation and before final review. This command creates visual evidence, summarizes results in `index.html`, performs a test review, and decides whether the feature may pass.

This command is feature-specific. Use `/business-flow-integration-test` when
the goal is to create or run the onboarding-derived baseline suite for all
approved major business-flow operation tests.

Webwright decision: do not use autonomous Webwright runs as the sole pass/fail gate. Use Webwright-style code-as-action exploration only to reduce agent browser-interaction cost when crafting long or fragile Playwright scenarios, then convert the stable path into a deterministic Playwright Test spec.

## Rules

- Use this command after `/flow-impl` or `team-implement` when behavior-changing work affects screens, routes, forms, modals, tables, filters, auth redirects, displayed values, or multi-step business workflows.
- Choose and record one evidence lane before spending browser-test budget:
  - **Full Gate Required**: run the full Playwright evidence gate when visible
    UI, a multi-step business workflow, auth/session/permission/tenant
    behavior, provider/device/deploy behavior, external side effects, or
    high-impact release confidence is in scope.
  - **Lightweight Evidence Allowed**: use focused substitute evidence only for
    API-only, internal logic, docs/skill-only, static/build-only, or otherwise
    non-visible and non-high-risk changes. Record the concrete reason,
    substitute commands/reviews, and covered regression surface.
  - **Blocked Early**: when the full gate is required but the runner, base URL,
    auth session, provider credential, device tunnel, safe test data, or other
    required lane dependency is unavailable, stop as `BLOCKED` with blocker
    category, exact unverified surface, and minimum unblock action.
- Lightweight evidence must not bypass the full-gate requirement for visible,
  multi-step, auth/session/permission/tenant, provider/device/deploy,
  external-side-effect, or high-impact workflows.
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
- Full lane: Docker/app stack or documented local app runtime is running and
  the app is reachable at the configured base URL.
- Full lane: Playwright CLI or MCP browser tooling is available.
- Lightweight lane: substitute commands/reviews are available.

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

Also record the evidence lane:

| Evidence lane | Reason | Substitute evidence or blocker | Unverified surface | Minimum unblock action |
| --- | --- | --- | --- | --- |
| full / lightweight / blocked | {reason} | {commands/reviews or blocker} | {surface or none} | {action or none} |

If a risky affected flow has no Playwright scenario and no documented low-risk reason, stop and update the plan.
If a risky affected flow has no Feature/API integration coverage for its required exception, permission, boundary, side-effect, or regression cases, stop and update the plan or implementation report before browser-only verification.

If the selected lane is `lightweight`, run the substitute checks/reviews and
continue to Phase 3 with a lightweight result summary instead of creating
browser screenshots. If the selected lane is `blocked`, write `result.md` with
the blocker details and stop with `BLOCKED`.

---

## Phase 2: Craft or Execute Playwright

For the full lane, run the most focused Playwright spec that covers the
scenarios.

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
- Evidence lane and effectiveness metrics
- Commands executed and exit status
- Scenario summary table with PASS / FAIL / BLOCKED
- Business Flow Matrix coverage table
- Regression Surface Matrix coverage table
- Links or embedded thumbnails for screenshots in execution order
- Console/network errors or "None observed"
- Links to Playwright HTML report, traces, videos, or failure artifacts when available
- Final gate status: `PASS`, `FAIL`, or `BLOCKED`

Also write `result.md` with the same high-level summary for quick reading in text-only environments.

Effectiveness metrics:

```text
evidence_lane: full | lightweight | blocked
issues_found: count + severity list
fix_resulted: yes | no
fix_reference: commit / file / task / none
would_other_tests_have_caught: yes | no | unknown
elapsed_time_minutes: number | unknown
token_or_work_overhead: estimate | unknown
blocker_category: runner | base_url | auth_session | provider_credentials | device_tunnel | safe_test_data | none
```

Example:

```text
evidence_lane: full
issues_found: 1 High
fix_resulted: yes
fix_reference: TASK-004 / test/playwright-cli/tests/reservation.spec.js
would_other_tests_have_caught: no
elapsed_time_minutes: 18
token_or_work_overhead: moderate browser evidence
blocker_category: none
```

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
   - Full lane: do screenshots prove the major user-visible steps?
   - Full lane: does `index.html` link to all relevant screenshots and reports?
   - Lightweight lane: are substitute commands/reviews and covered regression surfaces concrete?
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

- [ ] Evidence lane is recorded as `full`, `lightweight`, or `blocked`.
- [ ] Full lane: all required Playwright scenarios pass.
- [ ] Full lane: major-step screenshots exist and are linked from `index.html`.
- [ ] Full lane: `index.html` has final status `PASS`.
- [ ] Full lane: `test-review.md` exists.
- [ ] Full lane: `business-flow-impact.md` exists.
- [ ] Lightweight lane: substitute evidence, covered regression surface, and low-risk reason are recorded, and no high-risk full-gate surface is skipped.
- [ ] No unhandled Critical or High findings remain.
- [ ] Medium findings are fixed, waived with reason, or converted to follow-up tasks.
- [ ] Any blocked browser evidence is explicitly reported as `BLOCKED`, not `PASS`.

Update `docs/flow/{feature_name}/implementation_report.md` with:

- Playwright command(s)
- Evidence lane and effectiveness metrics
- Evidence index path
- Test review result
- Business-flow impact result
- Final gate status

## User Requirements

$ARGUMENTS

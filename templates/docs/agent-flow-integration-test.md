# Agent Flow Integration Test

## Purpose

This document defines the integration-test gate for behavior-changing work. The goal is to make the required evidence lane, browser evidence when needed, test review, business-flow impact review, blockers, and usefulness metrics explicit before a feature is allowed to pass.

## Evidence Lane Decision

Choose one lane before spending browser-test budget:

| Lane | Use when | Required evidence |
| --- | --- | --- |
| Full Gate Required | Visible UI, multi-step workflow, auth/session/permission/tenant, provider/device/deploy, external side effect, or high-impact release confidence is in scope | Playwright Test result, major-step screenshots, `index.html`, `result.md`, `test-review.md`, `business-flow-impact.md`, coverage mapping |
| Lightweight Evidence Allowed | API-only, internal logic, docs/skill-only, static/build-only, or otherwise non-visible low-risk change | Concrete low-risk reason, substitute commands/reviews, covered regression surface, Integration Coverage Contract coverage or waiver |
| Blocked Early | Full gate is required but runner, base URL, auth session, provider credential, device tunnel, safe test data, or equivalent dependency is unavailable | `BLOCKED` result, blocker category, exact unverified surface, minimum unblock action |

Lightweight evidence must not bypass visible, multi-step,
auth/session/permission/tenant, provider/device/deploy, external-side-effect, or
high-impact evidence requirements.

## Runner Decision

Use Playwright Test as the deterministic CI runner. Do not fully replace it with Webwright for the pass/fail gate.

Webwright is useful as an agent workflow pattern for long-horizon browser exploration because it asks the agent to create reusable Playwright scripts, inspect screenshots only when useful, and keep run artifacts in a workspace. That can reduce token-heavy step-by-step browser interaction during scenario discovery or script crafting.

For this repository, the integration gate still needs stable assertions, repeatable CI behavior, Playwright HTML reports, screenshots, traces, and clear pass/fail semantics. Therefore:

- **Default gate runner**: Playwright Test under `test/playwright-cli`.
- **Agent optimization mode**: Webwright-style script crafting for complex browser flows before converting the result into a deterministic Playwright spec.
- **Not allowed as sole pass condition**: an autonomous Webwright run without deterministic assertions and the required evidence files.

## Position in the Flow

```text
Investigation
  -> /flow-plan
  -> TDD test design
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
  -> pass / fix
```

## Required Artifacts

Full lane:

```text
docs/flow/{feature_name}/integration-test/{run_id}/
  index.html
  result.md
  test-review.md
  business-flow-impact.md
  screenshots/
```

Lightweight lane: record the substitute evidence, covered regression surface,
and metrics in `result.md`, the implementation report, or an equivalent
feature evidence report.

Blocked lane: record `BLOCKED`, blocker category, exact unverified surface, and
minimum unblock action in `result.md` or the implementation report.

## Scenario Design

Playwright scenarios are selected from the frozen plan:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- Playwright Integration Test Plan, when present

Each scenario must identify:

| Field | Required content |
| --- | --- |
| Scenario ID | Stable ID such as `PW-001` |
| Business flow | The plan matrix row being verified |
| Entry point | URL, route, modal, or browser state |
| Major steps | Steps that require screenshots |
| Expected result | User-visible or persisted outcome |
| Risk covered | Regression or adjacent workflow risk |

Before browser-only verification, each Integration Coverage Contract row must have Feature/API integration, Unit, Browser, Migration, or explicit waiver evidence for required happy, exception, permission, boundary, side-effect, and regression cases.

For lightweight lanes, replace the Playwright scenario table with substitute
evidence that names the low-risk reason, commands/reviews, and covered
regression surface. If any visible, multi-step, auth/session/permission/tenant,
provider/device/deploy, external-side-effect, or high-impact surface remains,
switch back to the full lane or record `BLOCKED`.

For long or fragile flows, first draft the scenario in Webwright-style:

1. Create a small exploratory Playwright script.
2. Use code, locators, waits, and helper functions instead of one-action-at-a-time browser driving.
3. Save exploratory screenshots/logs.
4. Convert the stable path into a Playwright Test spec with explicit assertions.
5. Run the spec as the official gate.

## Screenshot Evidence

Save screenshots for the major business steps, not only failures. Use business-readable names:

```text
screenshots/01-PW-001-open-order-list.png
screenshots/02-PW-001-open-detail-modal.png
screenshots/03-PW-001-confirm-updated-status.png
```

## Result Index

`index.html` is the canonical human-readable evidence summary. It must include:

- feature name, plan version, timestamp, base URL, branch/commit
- evidence lane and effectiveness metrics
- commands executed and exit status
- scenario result table
- business-flow coverage table
- regression-surface coverage table
- screenshot thumbnails or links in execution order
- console/network errors or "None observed"
- Playwright report/trace/video links when available
- final gate status: `PASS`, `FAIL`, or `BLOCKED`

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

## Test Review

Before passing, run a test review and write `test-review.md`.

Review:

- Are all affected business-flow rows covered by Playwright, Feature/API integration tests, Unit tests, migration checks, or explicit waivers?
- Are error cases, permission failures, validation failures, boundary values, and adjacent workflow regressions covered?
- Are screenshots sufficient to prove the user-visible steps?
- Did console/network evidence reveal runtime errors?

## Business-Flow Impact Review

Write `business-flow-impact.md`.

Review:

- Adjacent routes and screens
- Shared Blade partials and shared JavaScript
- Shared services/actions
- API/Ajax entrypoints
- Schema/migration-dependent paths
- Jobs/schedules
- Mail/PDF/export paths
- Auth/permissions and status transitions

## Pass Criteria

The integration-test gate passes only when:

- evidence lane is recorded,
- full lane: all required Playwright scenarios pass,
- full lane: major-step screenshots exist,
- full lane: `index.html` exists and reports `PASS`,
- full lane: `test-review.md` exists,
- full lane: `business-flow-impact.md` exists,
- lightweight lane: substitute evidence, covered regression surface, and low-risk reason are recorded, and no high-risk full-gate surface is skipped,
- no unhandled Critical or High findings remain,
- Medium findings are fixed, explicitly waived, or converted to follow-up tasks.

Blocked browser execution is not a pass. It must be reported as `BLOCKED` with
blocker category, exact unverified surface, and minimum unblock action.

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

This skill is feature-specific. Use `business-flow-integration-test` when the
goal is the onboarding-derived baseline suite that creates or runs all approved
major business-flow operation tests.

## Evidence Lane Decision

Choose and record one evidence lane before spending browser-test budget:

1. **Full Gate Required**: run the full Playwright evidence gate when the
   change affects visible UI, a multi-step business workflow,
   auth/session/permission/tenant behavior, provider/device/deploy behavior,
   external side effects, or high-impact release confidence. Lightweight
   evidence must not be used to bypass these requirements.
2. **Lightweight Evidence Allowed**: use focused substitute evidence only when
   the change is API-only, internal logic, docs/skill-only, static/build-only,
   or otherwise non-visible and non-high-risk. Record the concrete reason, the
   substitute commands/reviews, and the covered regression surface.
3. **Blocked Early**: if the full gate is required but the runner, base URL,
   auth session, provider credential, device tunnel, safe test data, or another
   required lane dependency is unavailable, stop as `BLOCKED`. Record the
   blocker category, the exact unverified surface, and the minimum unblock
   action. Do not call the gate passed.

## Operating Rules

- Activate `context-loader` first.
- Read the frozen `docs/flow/{feature_name}/plan.md` and the implementation report.
- Select and record the evidence lane before execution.
- Use the local base URL documented in `.claude/rules/dev-environment.md`; prefer `http://localhost` when cookies/session behavior matters.
- Use Playwright Test for the official gate.
- For long or brittle flows, craft exploratory Playwright scripts in Webwright style to reduce step-by-step browser interaction, then convert the stable path into a Playwright Test spec.
- Save evidence under `docs/flow/{feature_name}/integration-test/{run_id}/`.
- In the full lane, do not pass the gate if screenshots, `index.html`, test review, or business-flow impact review are missing.
- In the lightweight lane, do not claim full browser coverage; report the substitute evidence and covered regression surface.
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
- evidence lane and effectiveness metrics
- final gate status

## Effectiveness Metrics

Record these keys in `index.html` or `result.md` for every run/lane:

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
evidence_lane: lightweight
issues_found: 0
fix_resulted: no
fix_reference: none
would_other_tests_have_caught: unknown
elapsed_time_minutes: 4
token_or_work_overhead: static review only
blocker_category: none
```

## Pass Criteria

- Full lane: all required Playwright scenarios pass.
- Lightweight lane: substitute evidence is named, commands/reviews passed, and the uncovered browser surface is explicitly out of scope.
- Required Feature/API integration, Unit, Browser, Migration, or waiver evidence exists for each Integration Coverage Contract row.
- Full lane: major steps have screenshots.
- Full lane: `index.html`, `test-review.md`, and `business-flow-impact.md` exist.
- No unhandled Critical or High review findings remain.
- Medium findings are fixed, waived with reason, or converted to follow-up tasks.
- Blocked browser verification is reported as `BLOCKED`, not `PASS`.

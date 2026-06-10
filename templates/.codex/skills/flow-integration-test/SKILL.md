---
name: flow-integration-test
description: |
  Run the Agent Flow Playwright integration evidence gate in Codex. Use when
  the user says /flow-integration-test or after flow-impl/team-implement for
  visible or multi-step business workflows.
---

# Flow Integration Test

Alias-compatible Codex entrypoint for the `integration-test` skill.

## Rules

- Activate `context-loader` first.
- Follow the `integration-test` skill contract.
- Read the frozen plan and implementation report.
- Choose one evidence lane before execution:
  - **Full Gate Required** for visible UI, multi-step business workflows,
    auth/session/permission/tenant behavior, provider/device/deploy behavior,
    external side effects, or high-impact release confidence.
  - **Lightweight Evidence Allowed** only for API-only, internal logic,
    docs/skill-only, static/build-only, or otherwise non-visible and
    non-high-risk changes, with concrete substitute evidence and covered
    regression surface recorded.
  - **Blocked Early** when the full gate is required but the runner, base URL,
    auth session, provider credential, device tunnel, or safe test data is not
    available. Record blocker category, exact unverified surface, and minimum
    unblock action.
- Save evidence under `docs/flow/{feature_name}/integration-test/{run_id}/`.
- Required evidence:
  - `index.html`
  - `result.md`
  - `test-review.md`
  - `business-flow-impact.md`
  - major-step screenshots
- Use Playwright Test as the deterministic pass/fail runner.
- This is feature-specific evidence for an implemented plan. Use
  `business-flow-integration-test` instead when the goal is to create or run
  the onboarding-derived all-business-flow regression suite.
- Record effectiveness metrics: `evidence_lane`, `issues_found`,
  `fix_resulted`, `fix_reference`, `would_other_tests_have_caught`,
  `elapsed_time_minutes`, `token_or_work_overhead`, and `blocker_category`.
- If browser execution is blocked, mark the gate `BLOCKED` and name the
  unverified surface. Do not call it passed.

## Pass Criteria

- Full lane: required scenarios pass.
- Full lane: major-step screenshots exist and are linked.
- Full lane: `index.html`, `test-review.md`, and `business-flow-impact.md` exist.
- Lightweight lane: concrete substitute evidence and covered regression surface are recorded, and no high-risk full-gate surface is being skipped.
- Integration Coverage Contract evidence exists or has concrete waivers.
- No unhandled Critical or High findings remain.

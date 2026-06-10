---
name: flow-integration-test
description: |
  Alias for the Claude Code /flow-integration-test command. Use after
  flow-impl/team-implement for visible or multi-step business workflows.
---

# Flow Integration Test

Use the repo-local `.claude/commands/flow-integration-test.md` command contract.

## Compatibility Contract

- Same artifact as Codex:
  `docs/flow/{feature_name}/integration-test/{run_id}/`.
- Same boundary: this is feature-specific evidence for an implemented plan.
  Use `business-flow-integration-test` when the goal is to create or run the
  onboarding-derived all-business-flow regression suite.
- Same evidence lanes:
  - **Full Gate Required** for visible UI, multi-step business workflows,
    auth/session/permission/tenant behavior, provider/device/deploy behavior,
    external side effects, or high-impact release confidence.
  - **Lightweight Evidence Allowed** only for API-only, internal logic,
    docs/skill-only, static/build-only, or otherwise non-visible and
    non-high-risk changes, with concrete substitute evidence and covered
    regression surface recorded.
  - **Blocked Early** when the full gate is required but the runner, base URL,
    auth session, provider credential, device tunnel, or safe test data is not
    available.
- Same required evidence: `index.html`, `result.md`, `test-review.md`,
  `business-flow-impact.md`, and major-step screenshots.
- Same metrics: `evidence_lane`, `issues_found`, `fix_resulted`,
  `fix_reference`, `would_other_tests_have_caught`, `elapsed_time_minutes`,
  `token_or_work_overhead`, and `blocker_category`.
- Same gate result: `PASS`, `FAIL`, or `BLOCKED`.
- Same rule: blocked browser verification must be reported as `BLOCKED`, not as
  a pass.

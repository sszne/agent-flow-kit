Business Flow Integration Test Suite

Create, update, or run the onboarding-derived business-flow integration
regression suite. This command delegates to the `business-flow-integration-test`
skill.

Use after `agent-flow-onboarding` when the repository needs callable operation
tests for major confirmed business flows.

## Rules

- Load local context first.
- Read `docs/agent-flow/project-structure.md`,
  `docs/agent-flow/business-flows.md`, and
  `docs/agent-flow/integration-scenarios.md`.
- This is the project-wide baseline regression suite, not the feature-specific
  `/flow-integration-test` gate after `/flow-impl`.
- Do not create or modify executable tests until the user approves the final
  scenario list.
- Do not automatically attach this to `/flow-impl`.
- Use the target repository's existing Playwright/API test conventions when
  available.
- Register one all-suite runner command and record it in
  `docs/agent-flow/business-flow-integration-tests.md`.
- When running, save evidence under
  `docs/agent-flow/business-flow-integration-test-runs/{run_id}/`.

## Expected Flow

1. Explain that Agent Flow can create major operation tests from onboarding
   business flows as a regression-prevention route.
2. Present inferred test candidates and ask about unclear operations.
3. Accept missing operations from the user and get approval of the final list.
4. Create or update the suite spec, executable tests, and all-suite runner.
5. Run the suite when requested and report PASS / FAIL / BLOCKED with evidence.

## User Requirements

$ARGUMENTS

---
name: agent-flow-onboarding
description: |
  Run full agent-flow onboarding for a new repository. Use to create project
  structure, business-flow, and integration-scenario documentation before
  adopting flow-plan, flow-impl, integration-test, and team-review gates.
---

# Agent Flow Onboarding

Run the onboarding sequence for a repo that will adopt agent-flow.

## Outputs

- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

## Sequence

1. Run `project-structure-survey`.
2. Run `business-flow-discovery`.
3. Run `integration-scenario-design`.
4. Report readiness:
   - architecture/domain/use cases documented,
   - business flows and regression surfaces documented,
   - integration-test scenarios documented,
   - open questions/blockers named.

## Required Gate

Do not start behavior-changing implementation until all three documents exist.
If a document cannot be produced, record the blocker and treat behavior-changing work as blocked rather than waived.

---
name: context-loader
description: |
  Load repo-local Agent Flow context before planning, implementation, review,
  or integration testing. Use at the start of every non-trivial repository task.
---

# Context Loader

Load the target repository's durable context before acting. This keeps Codex
aligned with the Agent Flow docs installed in the repo instead of relying on a
machine-global skill.

## When To Use

Use at the start of every non-trivial repository task, especially:

- planning or implementation work,
- bug/regression analysis,
- code review,
- test design or integration-test evidence work,
- any task touching auth, schema, routes, screens, jobs, mail/PDF/export,
  search/cache, external integrations, or shared business logic.

For tiny self-contained questions, it is acceptable to load only the directly
relevant files.

## Workflow

1. Read `.claude/rules/*.md`.
2. Read `.claude/docs/DESIGN.md` if it exists.
3. For behavior-changing work, read the onboarding docs:
   - `docs/agent-flow/project-structure.md`
   - `docs/agent-flow/business-flows.md`
   - `docs/agent-flow/integration-scenarios.md`
4. If the task references an existing plan or implementation, read the relevant
   `docs/flow/{feature_name}/plan.md`, `implementation_report.md`, and
   integration evidence.
5. If bug knowledge exists, read `docs/agent-flow/bug-knowledge.md` for similar
   regressions.
6. If a task involves a specific library and `.claude/docs/libraries/` contains
   relevant notes, read only the matching library files.
7. Continue with the requested task using the loaded constraints.

## Operating Notes

- Prefer repo-local facts over global assumptions.
- If expected context files are missing, say which ones are missing and whether
  onboarding or a smaller direct path is appropriate.
- Do not treat missing docs as permission to skip the flow gates for risky work.
- Keep context loading proportional: read what is relevant, then act.

## Key Rules To Preserve

- Behavior-changing work should start from `/flow-plan` unless the user is only
  doing new-feature discovery through `/flow-start`.
- Implementation should follow a frozen plan with Business Flow Matrix,
  Regression Surface Matrix, Test Design Matrix, and Integration Coverage
  Contract when behavior changes.
- Visible or multi-step business workflows need Playwright integration evidence
  or a concrete blocker.
- Waivers must include a concrete reason or blocker.

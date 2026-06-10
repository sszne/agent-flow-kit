---
name: context-loader
description: |
  Load repo-local Agent Flow context before planning, implementation, review,
  or integration testing. Use at the start of every non-trivial repository task.
---

# Context Loader

Load only the target repository context that is useful for the current task.
Treat `.claude/` as a shared Agent Flow documentation and rule directory, not as
Claude-only instructions that Codex must blindly obey.

## When To Use

Use at the start of every non-trivial repository task, especially:

- planning or implementation work,
- bug/regression analysis,
- code review,
- test design or integration-test evidence work,
- any task touching auth, schema, routes, screens, jobs, mail/PDF/export,
  search/cache, external integrations, or shared business logic.
- frontend planning or review that may depend on repo-local design-system
  rules, tokens, components, patterns, or brand guidance.

For tiny self-contained questions, load only the directly relevant files.

## Workflow

1. Read the repo-local agent entrypoint first:
   - Codex: prefer `AGENTS.md`.
   - Claude: prefer `CLAUDE.md`.
   - If both exist and the task is workflow-sensitive, skim both for conflicts
     or project-specific gates.
2. Read `.claude/docs/DESIGN.md` if it exists.
3. Read only the relevant files under `.claude/rules/`.
   - Treat these as shared project constraints.
   - Do not import tool-delegation rules, package-manager assumptions, or
     Claude-specific orchestration notes when they conflict with the active
     agent, repository evidence, or user request.
4. For behavior-changing work, read the onboarding docs:
   - `docs/agent-flow/project-structure.md`
   - `docs/agent-flow/business-flows.md`
   - `docs/agent-flow/integration-scenarios.md`
   - `docs/agent-flow/business-flow-integration-tests.md` when the task
     touches baseline business-flow operation tests or suite evidence.
5. If the task references an existing plan or implementation, read the relevant
   `docs/flow/{feature_name}/plan.md`, `implementation_report.md`, and
   integration evidence.
6. If bug knowledge exists, read `docs/agent-flow/bug-knowledge.md` for similar
   regressions.
7. If frontend design, screens, components, client UI, styles, public frontend
   assets, brand, tokens, or component rules are in scope, read design-system
   context when it exists:
   - `.agent-flow/config.json` `design_system_paths`
   - `docs/agent-flow/design-system.md`
   - `docs/agent-flow/design-system/`
   - `.claude/docs/DESIGN.md`
   - existing source component/style/theme files directly relevant to the
     planned surface
8. If a task involves a specific library and `.claude/docs/libraries/` contains
   relevant notes, read only the matching library files.
9. Continue with the requested task using the loaded constraints.

## Operating Notes

- Prefer repo-local facts over global assumptions.
- Keep context loading proportional: read what is relevant, then act.
- If `.claude/` is missing, do not treat that alone as a blocker.
- If required Agent Flow onboarding docs are missing for behavior-changing work,
  say which ones are missing and run/request onboarding or record the blocker.
- Do not treat missing docs as permission to skip the flow gates for risky work.
- When instructions conflict, prefer the active agent's entrypoint
  (`AGENTS.md` for Codex, `CLAUDE.md` for Claude), direct user instruction, and
  source evidence over generic shared rules.

## Key Rules To Preserve

- Behavior-changing work should start from `/flow-plan` unless the user is only
  doing new-feature discovery through `/flow-start`.
- Implementation should follow a frozen plan with Business Flow Matrix,
  Regression Surface Matrix, Test Design Matrix, Integration Coverage Contract,
  a Plan Review Requirement decision, and an approved current `plan-review.md`
  when review is required.
- Visible, multi-step, auth/session/permission/tenant, provider/device/deploy,
  external-side-effect, or high-impact workflows need full
  `flow-integration-test` evidence or a concrete `BLOCKED` result. Low-risk
  non-visible changes may use lightweight evidence only with a concrete reason,
  substitute checks, and covered regression surface.
- Waivers must include a concrete reason or blocker.

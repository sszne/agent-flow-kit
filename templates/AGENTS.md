# Agent Flow Kit Instructions

Use these repository-local instructions when working in this project with Codex
or another coding agent.

## Context First

At the start of every non-trivial repository task, load the local context:

- `AGENTS.md` first when working as Codex
- `CLAUDE.md` only when it exists and the task is workflow-sensitive
- `.claude/rules/*.md`
- `.claude/docs/DESIGN.md`
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- relevant `docs/flow/{feature_name}/` artifacts when a plan or implementation
  already exists

If these files are missing and the work changes behavior, run or request
`agent-flow-onboarding` before implementation.

Treat `.claude/` as shared Agent Flow documentation, not as Claude-only
instructions. When a shared rule conflicts with Codex behavior, direct user
instruction, or source evidence, prefer the active agent's entrypoint and the
repo evidence.

## Flow Selection

- Use `/flow-plan` for modifications to existing behavior, bug fixes,
  regressions, refactors, auth/schema/status/order/search/mail/PDF/job changes,
  and business-flow-sensitive work.
- Use `/flow-start` for new-feature discovery or greenfield scope shaping.
- If discovery shows an existing runtime path will change, switch to
  `/flow-plan` before freezing the plan.

In Codex, `/flow-plan`, `/flow-impl`, and `/flow-integration-test` map to the
same-named skills: `flow-plan`, `flow-impl`, and `flow-integration-test`.

## Implementation Gate

Do not start behavior-changing implementation unless the frozen plan contains:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- concrete waivers or blockers for any uncovered required coverage

For bug/regression work, also require a Bug Feedback Review that classifies the
prior flow failure or records why the issue could not be prevented by flow
changes.

## Test Quality

Test design must start from affected business flows and regression surfaces, not
only from the edited function.

If a change can affect routes, screens, API flows, shared logic, schema or
migrations, jobs, mail/PDF/export, search/cache, auth, or another runtime
entrypoint, add or update integration-level coverage for the affected flows.

Visible or multi-step business workflows require Playwright integration evidence
with screenshots, `index.html`, test review, and business-flow impact review.
If this is blocked, report `BLOCKED` with the concrete reason and affected
surface.

## Working Style

- Prefer the smallest change that follows existing project patterns.
- Ask concise questions when actor, permission, business outcome, data
  ownership, side effects, or success criteria are unclear.
- Keep repo-specific business knowledge in `docs/agent-flow/` when it will help
  future plans.
- Do not force an advisory-only role. When the user asks for implementation and
  the flow gates are satisfied, implement and verify the change.

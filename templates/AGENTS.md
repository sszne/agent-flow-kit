# Agent Flow Kit Instructions

Use these repository-local instructions when working in this project with Codex
or another coding agent.

## Context First

At the start of every non-trivial repository task, load the local context:

- `AGENTS.md` first when working as Codex
- `CLAUDE.md` only when it exists and the task is workflow-sensitive
- `.claude/rules/*.md`
- `.claude/docs/DESIGN.md`
- `docs/agent-flow/design-system.md` and `docs/agent-flow/design-system/`
  when frontend design, screens, components, styles, brand, tokens, or
  component rules are in scope
- `docs/agent-flow/source-documents.md` when it exists
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- relevant `docs/flow/{feature_name}/` artifacts when a plan or implementation
  already exists

If these files are missing and the work changes behavior, run or request
`agent-flow-onboarding` before implementation.

During onboarding, run `flow-document` first. Source documents are optional, but
the intake status should be recorded in `docs/agent-flow/source-documents.md`.
Treat converted requirement documents as candidate evidence only; source,
schema, routes, tests, deploy config, current repo docs, and explicit user
confirmation take priority.

Treat `.claude/` as shared Agent Flow documentation, not as Claude-only
instructions. When a shared rule conflicts with Codex behavior, direct user
instruction, or source evidence, prefer the active agent's entrypoint and the
repo evidence.

## Flow Selection

- Use `/flow-plan` for modifications to existing behavior, bug fixes,
  regressions, refactors, auth/schema/status/order/search/mail/PDF/job changes,
  and business-flow-sensitive work.
- Do not require `/flow-plan` when the requested change is display-only and is
  limited to minor style changes, layout adjustments, or visible text changes.
  If the same request touches runtime behavior, data flow, permissions, API
  behavior, workflow order, validation, side effects, tests, install behavior,
  CI gates, or Agent Flow contracts, keep `/flow-plan` required.
- Use `/flow-start` for new-feature discovery or greenfield scope shaping.
- If discovery shows an existing runtime path will change, switch to
  `/flow-plan` before freezing the plan.

In Codex, `/flow-plan`, `/flow-plan-review`, `/flow-impl`, and
`/flow-integration-test` map to the same-named skills: `flow-plan`,
`flow-plan-review`, `flow-impl`, and `flow-integration-test`.

For frontend behavior-changing plans, `flow-plan` uses `flow-design` as a
support skill when design-system guidance may apply. If local design-system
components or tokens match the planned UI, the plan should apply them or record
a concrete waiver.

## Implementation Gate

Do not start behavior-changing implementation unless the frozen plan contains:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- Plan Review Requirement decision with `Required` or `Optional` and a concrete reason
- approved `docs/flow/{feature_name}/plan-review.md` for the current frozen
  plan when review is required
- concrete waivers or blockers for any uncovered required coverage

For bug/regression work, also require a Bug Feedback Review that classifies the
prior flow failure or records why the issue could not be prevented by flow
changes.

`flow-plan-review` is mandatory only for large-scale or high-impact work. Use
cross-agent review by default when review runs: Codex-created plans are
reviewed by Claude Code, and Claude-created plans are reviewed by Codex. A
same-agent review is acceptable only when `plan-review.md` records a concrete
fallback reason or blocker.

Treat these as review-required high-impact changes by default: multi-flow or
cross-module changes; auth, permission, tenant, ownership, session, security, or
privacy changes; schema, migration, data compatibility, backfill, rollback, or
destructive data changes; deploy, CI, install, hooks, workflow gates,
risky-path config, or Agent Flow contract changes; external providers,
webhooks, mail/PDF, storage, search/cache, queues, jobs, schedules, or other
side effects; public API contracts or shared runtime entrypoints; and any
change the user or plan author marks as uncertain or high impact.

`flow-plan-review` is optional for clearly non-high-impact work, including
small localized behavior changes and non-behavioral typo, formatting-only, or
docs-only changes. If a docs-only change updates Agent Flow rules, skill
behavior, gates, review policy, risky-path config, or required evidence, treat
it as high-impact workflow work and keep the review gate.

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

Frontend plans that affect screens, components, client UI, styles, or public
frontend assets should include design-system applicability evidence when a
design system is present. If no design system is found, record the searched
paths and fallback source/component patterns.

## Working Style

- Prefer the smallest change that follows existing project patterns.
- Ask concise questions when actor, permission, business outcome, data
  ownership, side effects, or success criteria are unclear.
- Keep repo-specific business knowledge in `docs/agent-flow/` when it will help
  future plans.
- Do not force an advisory-only role. When the user asks for implementation and
  the flow gates are satisfied, implement and verify the change.

---
name: flow-plan
description: |
  Alias for the Claude Code /flow-plan command. Use when the user says
  flow-plan or /flow-plan to create a frozen Agent Flow implementation plan.
---

# Flow Plan

Use the repo-local `.claude/commands/flow-plan.md` command contract.

## Compatibility Contract

- Same artifact as Codex: `docs/flow/{feature_name}/plan.md`.
- Same required gates: Business Flow Matrix, Regression Surface Matrix, Test
  Design Matrix, Integration Coverage Contract, Plan Review Requirement, Flow
  Knowledge Update, and Residual Risk Preflight when applicable.
- Same questioning behavior: include `Questioning Decision` in every plan and
  require a source-backed `No Questions Rationale` when no questions are asked.
- Same goal-confirmation behavior: confirm desired user experience, business
  outcome, root-cause target, and accepted completion signal before freeze; ask
  when the requester goal is ambiguous.
- Same display-only boundary: do not force flow-plan for minor style changes,
  layout adjustments, or visible text changes unless runtime behavior, data
  flow, permissions, API behavior, workflow order, validation, side effects,
  tests, install behavior, CI gates, or Agent Flow contracts may change.
- Same runtime behavior: include Runtime Causality Gate when production-only,
  deploy/runtime/provider, browser-network, auth/session, secret/binding,
  remote data, or external-runtime symptoms may be involved.
- Same onboarding/UI behavior: confirm step names, order, exclusions, action
  placement, resume/fallback path, and blocked evidence lanes before
  implementation.
- Same frontend design-system behavior: run the Frontend Design System Gate for
  screens, components, frontend routes, client UI, styles, public frontend
  assets, brand, tokens, or component rules; apply matching design-system rules
  or record concrete waivers.
- Same design-principles behavior: run the Design Principles Gate for
  behavior-changing work affecting modules, services/actions, domain logic,
  shared logic, data ownership, or new classes/modules/dependencies; read
  repo-local `docs/agent-flow/design-principles.md` and configured
  `design_principles_paths` before external architecture references; include a
  `Design Principles Compliance` section applying matching rules (including the
  vague-responsibility, Service Introduction Rule, and aggregate-encapsulation
  anti-pattern checks) or record concrete waivers.
- Same provider/auth/deploy behavior: distinguish local mock coverage,
  deployed-artifact checks, real provider/device happy paths, valid
  credential/session paths, and concrete blockers.
- Same bug/regression behavior: run Bug Feedback Review and update
  `docs/agent-flow/bug-knowledge.md` when flow improvement cannot prevent the
  issue.
- Same bug-knowledge behavior: classify matching prevention patterns before
  task design when a bug/regression is preventable by better planning or tests.
- Same browser behavior: include Playwright Integration Test Plan for visible or
  multi-step workflows.
- Same author metadata: Claude Code-authored plans include
  `<!-- plan_author: claude-code -->`.
- Same plan-review decision: mark review `Required` for large-scale or
  high-impact work and `Optional` for smaller localized changes with a concrete
  reason. The frozen plan must pass `/flow-plan-review` before `/flow-impl` or
  `team-implement` only when review is required.

When this skill is invoked in Claude Code, execute `/flow-plan` semantics rather
than inventing a separate planning flow.

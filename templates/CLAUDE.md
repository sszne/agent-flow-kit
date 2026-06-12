# Agent Flow Kit

This repository uses Agent Flow Kit for plan-first implementation, regression
control, and browser/integration evidence.

## Context First

Before non-trivial repository work, read:

- `CLAUDE.md` first when working as Claude
- `AGENTS.md` when Codex or cross-agent behavior may matter
- `.claude/rules/*.md`
- `.claude/docs/DESIGN.md`
- `docs/agent-flow/design-system.md` and `docs/agent-flow/design-system/`
  when frontend design, screens, components, styles, brand, tokens, or
  component rules are in scope
- `docs/agent-flow/design-principles.md` when behavior-changing work affects
  modules, services, domain logic, shared logic, or data ownership
- `docs/agent-flow/source-documents.md` when it exists
- `docs/agent-flow/business-flow-integration-tests.md` when business-flow
  baseline operation tests are in scope
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- relevant `docs/flow/{feature_name}/` artifacts

If behavior-changing work starts before the onboarding docs exist, run
`agent-flow-onboarding` first or record the blocker.

During onboarding, run `/flow-document` first. Source documents are optional,
but the intake status should be recorded in
`docs/agent-flow/source-documents.md`. Treat converted requirement documents as
candidate evidence only; source, schema, routes, tests, deploy config, current
repo docs, and explicit user confirmation take priority.

Treat `.claude/` as shared Agent Flow documentation. Load only the rules and
docs relevant to the current task, and avoid importing tool-delegation or
package-manager assumptions when they conflict with the active agent,
repository evidence, or direct user instruction.

## Main Flow

```text
agent-flow-onboarding
  -> /flow-document
  -> project-structure-survey
  -> business-flow-discovery
  -> integration-scenario-design
  -> /business-flow-integration-test when requested
  -> /flow-start or /flow-plan
  -> /flow-plan-review when required or requested
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
```

Use `/flow-plan` for existing behavior changes, bug fixes, regressions,
refactors, auth/schema/status/order/search/mail/PDF/job changes, and
business-flow-sensitive work.

Do not require `/flow-plan` when the requested change is display-only and is
limited to minor style changes, layout adjustments, or visible text changes. If
the same request touches runtime behavior, data flow, permissions, API behavior,
workflow order, validation, side effects, tests, install behavior, CI gates, or
Agent Flow contracts, keep `/flow-plan` required.

Use `/flow-start` only for new-feature discovery or greenfield scope shaping.
If discovery touches an existing runtime path, switch to `/flow-plan`.

Use `/business-flow-integration-test` after onboarding when the repository needs
a callable regression suite for major confirmed business-flow operations. This
suite is created through user-confirmed scenarios and is not automatically run
from `/flow-impl`.

Codex uses the same workflow names as skills: `flow-plan`, `flow-plan-review`,
`flow-impl`, and `flow-integration-test`. Both tools write the same artifacts under
`docs/flow/{feature_name}/`.

For frontend behavior-changing plans, `flow-plan` uses `flow-design` as a
support skill when design-system guidance may apply. If local design-system
components or tokens match the planned UI, the plan should apply them or record
a concrete waiver.

For behavior-changing plans that affect modules, services, domain logic, shared
logic, or data ownership, `flow-plan` runs the Design Principles Gate against
`docs/agent-flow/design-principles.md` (and configured
`design_principles_paths`). Matching rules — including the
vague-responsibility, Service Introduction Rule, and aggregate-encapsulation
anti-pattern checks — must be applied or concretely waived, and the plan must
include a `Design Principles Compliance` section.

## Quality Gates

Behavior-changing plans need:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- Plan Review Requirement decision with `Required` or `Optional` and a concrete reason
- approved `docs/flow/{feature_name}/plan-review.md` for the current frozen
  plan when review is required
- concrete waivers or blockers for uncovered coverage

Implementation should stay inside the frozen plan. If a new behavior or design
choice appears, update the plan or ask the user before proceeding.

Run `/flow-plan-review` after the plan is frozen and before implementation when
the plan marks review as required or configured high-impact paths are changed.
Use cross-agent review by default when review runs: Claude Code-created plans
are reviewed by Codex, and Codex-created plans are reviewed by Claude Code. A
same-agent review must record a concrete fallback reason or blocker in
`plan-review.md`.

Treat these as review-required high-impact changes by default: multi-flow or
cross-module changes; auth, permission, tenant, ownership, session, security, or
privacy changes; schema, migration, data compatibility, backfill, rollback, or
destructive data changes; deploy, CI, install, hooks, workflow gates,
risky-path config, or Agent Flow contract changes; external providers,
webhooks, mail/PDF, storage, search/cache, queues, jobs, schedules, or other
side effects; public API contracts or shared runtime entrypoints; and any
change the user or plan author marks as uncertain or high impact.

`/flow-plan-review` is optional for clearly non-high-impact work, including
small localized behavior changes and non-behavioral typo, formatting-only, or
docs-only changes. If a docs-only change updates Agent Flow rules, skill
behavior, gates, review policy, risky-path config, or required evidence, treat
it as high-impact workflow work and keep the review gate.

Visible or multi-step business workflows require Playwright integration evidence
with screenshots, `index.html`, test review, and business-flow impact review.

`/flow-integration-test` should use a conditional evidence lane:

- Full Gate Required: visible UI, multi-step workflows,
  auth/session/permission/tenant, provider/device/deploy, external side
  effects, or high-impact release confidence.
- Lightweight Evidence Allowed: API-only, internal logic, docs/skill-only,
  static/build-only, or otherwise non-visible low-risk changes, with a
  concrete reason, substitute checks, and covered regression surface.
- Blocked Early: if a required full gate cannot run, report `BLOCKED` with the
  blocker category, exact unverified surface, and minimum unblock action.

Every lane should record effectiveness metrics: issues found, whether a fix
resulted, fix reference, whether another test would have caught it, elapsed
time when available, token/work overhead when available, and blocker category.

The onboarding-derived `/business-flow-integration-test` suite is the
project-wide baseline for major continuous operations. `/flow-integration-test`
remains the feature-specific evidence gate after implementation.

Frontend plans that affect screens, components, client UI, styles, or public
frontend assets should include design-system applicability evidence when a
design system is present. If no design system is found, record the searched
paths and fallback source/component patterns.

Plans that affect modules, services, domain logic, shared logic, or data
ownership should include design-principles compliance evidence when a
design-principles document is present. If none is found, record the searched
paths and the fallback source conventions used.

## Documentation

When `/flow-plan` uncovers reusable business-flow, permission, exception,
side-effect, or integration-scenario knowledge, update:

- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/bug-knowledge.md` when the knowledge comes from a bug that
  cannot be fully prevented by flow improvements

---
name: flow-plan
description: |
  Create a frozen Agent Flow implementation plan in Codex. Use when the user
  says /flow-plan, asks for flow-plan, or requests changes to existing behavior,
  bug fixes, regressions, refactors, auth/schema/status/job/mail/PDF/search
  work, or other business-flow-sensitive implementation.
---

# Flow Plan

Codex-native equivalent of Claude Code `/flow-plan`.

## Purpose

Turn a user request into `docs/flow/{feature_name}/plan.md` through codebase
analysis, requirement questioning, business-flow mapping, test design, and a
readiness gate. Do not implement during this skill.

## Operating Rules

- Activate `context-loader` first.
- Treat `flow-plan` as the canonical entry point for existing behavior changes,
  bug fixes, regressions, refactors, and business-flow-sensitive work.
- Prefer the smallest implementation that fits existing source patterns.
- Do not leave business ambiguity unresolved. If actors, permissions, data
  ownership, current vs desired behavior, side effects, entrypoints, success
  criteria, or rollout assumptions are unclear, ask the user before freezing.
- Do not silently skip requirement questioning. Before writing the plan,
  classify whether questions are required. If none are required, record a
  source-backed "No Questions Rationale" in the plan and in the user-facing
  summary.
- Behavior-changing work requires onboarding docs:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- A frozen plan for behavior-changing work must include:
  - Business Flow Matrix
  - Regression Surface Matrix
  - Test Design Matrix
  - Integration Coverage Contract
  - Flow Knowledge Update
  - Residual Risk Preflight when applicable
  - Runtime Causality Gate when runtime, deploy, external provider, secret,
    binding, remote data, or production-only symptoms may be involved
  - Bug Feedback Review for bug/regression work
  - Playwright Integration Test Plan for visible or multi-step workflows
- Include plan author metadata near the frozen marker:
  `<!-- plan_author: codex -->`.
- Tell the user that `flow-plan-review` must approve the frozen plan before
  `flow-impl` or `team-implement` starts.
- Waivers must include a concrete reason or blocker. Reject vague entries such
  as `N/A`, `manual`, `low risk`, `TBD`, `later`, or blank cells.

## Workflow

```text
Phase 1: Scope
  load context -> inspect code/docs/tests -> analyze intent/current state
  -> bug feedback review when applicable
  -> residual risk preflight
  -> runtime causality gate when applicable
  -> flow knowledge update check
  -> classify requirement questions
  -> ask user only required questions, or record No Questions Rationale
    ->
Phase 2: Sketch
  select minimal existing-pattern design
  -> ask design/library questions only when needed
  -> map business flows, regression surfaces, tests, and integration coverage
    ->
Phase 3: Readiness
  write docs/flow/{feature_name}/plan.md
  -> verify readiness checklist
  -> freeze plan only when ambiguity and required gates are resolved
```

## Requirement Questioning Decision

Questioning is not optional; the agent must make an explicit decision before
writing the plan.

Questions are required when any of these are unclear:

- target actor, role, permission, tenant, store, company, or customer scope,
- desired business outcome, current behavior, desired behavior, or success
  criteria,
- data ownership, lifecycle, status transition, deletion/retention, migration,
  backfill, or existing-data compatibility,
- user-visible entrypoint, screen placement, wording, workflow order, or
  operator/customer-facing copy,
- side effects such as mail, PDF/export, jobs, notifications, audit logs,
  cache/search updates, or external APIs,
- compatibility with an existing business flow, integration scenario, auth
  path, schema contract, or shared service.

Questions may be skipped only when all of these are true:

- actor/scope, current behavior, desired behavior, and success criteria are
  directly supported by user wording or source evidence,
- affected screens, routes, APIs, jobs, mail/PDF/export paths, schema, shared
  services, and external dependencies have been inspected or ruled out,
- permission/ownership, exception paths, boundary values, lifecycle rules, and
  side effects can be described without guessing,
- migration, backfill, deploy/runtime enforcement, and existing-data
  compatibility are either not involved or source-backed,
- onboarding docs, existing plans, tests, and code do not conflict with the
  planned behavior,
- any remaining assumptions are source-backed, low-risk, explicitly out of
  scope, or recorded as concrete blockers/waivers.

If questions are skipped, the plan must include a "No Questions Rationale" that
cites the evidence used to avoid questions. Lack of obvious ambiguity is not
enough; the rationale must explain why implementation would not require a
business-rule guess.

## Runtime Causality Gate

Before proposing behavior-changing code, classify whether the symptom may be
caused by runtime, deployment, provider, secret/binding, remote data, or
environment state instead of application source code.

Run this gate when any trigger is present:

- browser reports CORS, `ERR_FAILED`, network failure, or opaque 5xx symptoms,
- the request is production-only, staging-only, or cannot be reproduced locally,
- Cloudflare Workers/Pages/D1/R2/KV/Durable Objects, Vercel, AWS, GCP, Fly,
  Supabase, Firebase, queues, search, cache, storage, mail, payment, auth
  provider, webhook, or another external runtime is involved,
- auth/session/cookie/password reset/secret/deploy artifact behavior is
  involved,
- logs or browser output mention `503`, `1102`, `exceededCpu`,
  `exceededMemory`, timeout, worker exception, missing binding, migration
  drift, stale deploy, or provider rejection,
- setup, reset, migration, deploy, or command execution reports success, but
  the follow-up use path still fails,
- existing smoke checks exercise only shallow paths such as preflight, invalid
  input, unauthenticated `401`, or health checks while the happy path or
  side-effect path is unproven.

When triggered, add `Runtime Causality Gate` to the plan and fill this table
before implementation design is frozen:

```markdown
| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | GitHub Actions, deploy log, release SHA, runtime script version | current / stale / unknown |
| Browser symptom vs server outcome | DevTools plus server/runtime logs captured for the same request | browser symptom / app error / runtime limit |
| Runtime log | wrangler tail, provider logs, app logs, queue logs, webhook logs | ok / exception / exceededCpu / timeout / provider error |
| Representative paths | preflight, invalid path, valid happy path, side-effect path | shallow only / full path covered / blocked |
| Environment bindings | secrets, env vars, D1/DB binding, storage bucket, provider config | aligned / mismatch / unknown |
| Remote data state | read-only query, admin diagnostic, migration status, seed/version marker | expected / stale / unknown |
| Classification | evidence-backed conclusion | code defect / environment-ops defect / data defect / deploy artifact mismatch / provider-runtime defect / inconclusive |
```

Do not treat browser CORS text as root-cause evidence by itself. If the gate is
triggered and server-side/runtime evidence is unavailable, record a concrete
blocker or add a setup task before code-changing tasks. If the classification is
inconclusive, keep the implementation plan focused on gathering evidence rather
than speculative fixes.

## Required Plan Shape

Use this structure unless the target repo already has a stricter local template:

```markdown
# {Feature Title}

## 1. Requirements
### 1.1 Current State
### 1.2 Intent And Ambiguity Resolution
### 1.3 Goal
### 1.4 Scope / Non-Goals
### 1.5 Acceptance Criteria
### 1.6 Questioning Decision And User Answers

## 2. Design
### 2.1 Affected Files And Modules
### 2.2 Implementation Approach
### 2.3 Design Policy And Library Selection
### 2.4 Risks And Mitigations
### 2.5 Residual Risk Preflight
### 2.6 Runtime Causality Gate
### 2.7 Bug Feedback Review
### 2.8 Flow Knowledge Update
### 2.9 Business Flow Matrix
### 2.10 Regression Surface Matrix
### 2.11 Test Design Matrix
### 2.12 Integration Coverage Contract
### 2.13 Playwright Integration Test Plan
### 2.14 Migration / Runtime Enforcement
### 2.15 Open Questions

## 3. Tasks
- [ ] TASK-001 ...

## 4. Readiness
- [ ] Requirements map to tasks
- [ ] User intent and current-state analysis is documented
- [ ] Requirement questioning was performed, or No Questions Rationale is documented with source evidence
- [ ] Business/product ambiguity has been resolved or explicitly blocked
- [ ] Required onboarding docs exist for behavior-changing work
- [ ] Flow Knowledge Update target is explicit
- [ ] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
- [ ] Runtime Causality Gate is complete or explicitly not triggered
- [ ] Business flows map to required tests or blockers
- [ ] Integration Coverage Contract has concrete coverage or waivers
- [ ] Validation commands are identified

<!-- frozen: v1 YYYY-MM-DD -->
<!-- plan_author: codex -->
```

## User-Facing Behavior

If questions are needed, stop after presenting:

- understanding so far,
- code/doc evidence,
- assumptions not yet safe,
- up to five prioritized questions.

If no questions remain, write or update the plan and clearly state whether it is
frozen or still blocked. Include a short "No Questions Rationale" that cites the
source evidence used to avoid questions, such as existing docs, routes, tests,
schema, or explicit user wording.

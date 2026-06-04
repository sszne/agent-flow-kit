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
- Do not force `flow-plan` for display-only requests that are limited to minor
  style changes, layout adjustments, or visible text changes. Keep `flow-plan`
  required when the change also touches runtime behavior, data flow,
  permissions, API behavior, workflow order, validation, side effects, tests,
  install behavior, CI gates, or Agent Flow contracts.
- Prefer the smallest implementation that fits existing source patterns.
- Do not leave business ambiguity unresolved. If actors, permissions, data
  ownership, current vs desired behavior, side effects, entrypoints, success
  criteria, or rollout assumptions are unclear, ask the user before freezing.
- Confirm the requester's goal before freezing. If the desired user experience,
  business outcome, root-cause target, or accepted completion signal is unclear,
  ask the user instead of choosing one plausible interpretation.
- Every plan must include a `Questioning Decision`. If no user questions are
  asked, include a source-backed `No Questions Rationale`; do not rely on a
  silent assumption that the request is obvious.
- Behavior-changing work requires onboarding docs:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- A frozen plan for behavior-changing work must include:
  - Questioning Decision and No Questions Rationale when no questions are asked
  - Business Flow Matrix
  - Regression Surface Matrix
  - Test Design Matrix
  - Integration Coverage Contract
  - Plan Review Requirement with `Required` or `Optional` and a concrete reason
  - Flow Knowledge Update
  - Residual Risk Preflight when applicable
  - Runtime Causality Gate when runtime, deploy, external provider, secret,
    binding, remote data, or production-only symptoms may be involved
  - Bug Feedback Review for bug/regression work
  - Playwright Integration Test Plan for visible or multi-step workflows
- Onboarding, setup, wizard, modal, or user-guidance UI plans must confirm step
  names, step order, excluded elements, action placement, resume/fallback path,
  and blocked evidence lanes before rich UI implementation.
- Provider, auth, LIFF, LINE, Google, deploy, or smoke-test plans must separate
  local mock coverage, deployed-artifact checks, real provider/device happy
  paths, valid credential/session paths, and concrete blockers.
- Mark `Plan Review Requirement: Required` for large-scale or high-impact
  changes: multi-flow/cross-module work; auth, permission, tenant, session,
  security, or privacy changes; schema/migration/data-compatibility changes;
  deploy, CI, install, hook, workflow-gate, risky-path config, or Agent Flow
  contract changes; external providers, webhooks, mail/PDF, storage,
  search/cache, queues, jobs, schedules, side effects, public API contracts, or
  shared runtime entrypoints. For smaller localized changes, mark
  `Requirement: Optional` with the reason review is not mandatory.
- Bug/regression plans must search `docs/agent-flow/bug-knowledge.md`, classify
  any matching prevention pattern, and add flow-improvement tasks before
  implementation tasks when the bug is preventable by better planning or tests.
- Include plan author metadata near the frozen marker:
  `<!-- plan_author: codex -->`.
- Tell the user whether `flow-plan-review` is required before `flow-impl` or
  `team-implement`, or optional but available for an extra readiness pass.
- Waivers must include a concrete reason or blocker. Reject vague entries such
  as `N/A`, `manual`, `low risk`, `TBD`, `later`, or blank cells.

## Workflow

```text
Phase 1: Scope
  load context -> inspect code/docs/tests -> analyze intent/current state
  -> confirm requester goal and completion signal
  -> write questioning decision
  -> bug feedback review when applicable
  -> residual risk preflight
  -> runtime causality gate when applicable
  -> flow knowledge update check
  -> ask user only required questions
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

## Goal Confirmation Gate

Before writing or freezing the plan, identify the requester's intended outcome.
The plan must distinguish:

- observed symptom or requested change,
- desired user experience or business outcome,
- root-cause target when the request is a bug/regression,
- accepted completion signal, including whether deployed or valid-path proof is
  required.

Questions are required when the same report could reasonably mean different
goals, such as:

- improving an error message versus preventing the error from happening,
- keeping a user in their current state versus showing a retry screen,
- removing the root cause versus adding diagnostics or logging,
- local source-code repair versus deployed artifact or valid-session proof.

Do not infer the goal from the easiest source change. Source evidence can
support a no-question decision only when it also supports the desired outcome.
If the requester has already stated the goal explicitly, record that wording in
`Intent And Ambiguity Resolution`, `Goal`, and `No Questions Rationale`.

## Questioning Decision Gate

Before writing or freezing the plan, explicitly decide whether user questions
are required.

Questions are required when any of these are unclear and cannot be resolved from
source evidence, existing docs, or a direct user answer:

- actor, role, store/tenant/customer scope, permission, or ownership,
- current behavior versus desired behavior,
- desired user experience, root-cause target, or accepted completion signal,
- business outcome, success criteria, or completion signal,
- data lifecycle, state transition, side effect, or external dependency,
- visible step names, order, wording, placement, or user workflow,
- provider/runtime/deploy lane needed to prove the actual risk.

For detailed compatibility with older plans, this is the same gate previously
called requirement questioning. The generated plan should use the canonical
heading `Questioning Decision`.

If no questions are asked, add a `Questioning Decision` section or table with:

```markdown
| Item | Decision |
| --- | --- |
| Questions asked | No |
| Requirement questions asked | No |
| Goal Confirmation | {explicit user wording or source-backed reason the desired outcome is unambiguous} |
| No Questions Rationale | {source-backed reason the plan can be frozen without user input} |
| User answers | None required / {answers already provided by user} |
| Unsafe assumptions? | None blocking / {explicit blocker} |
```

Do not freeze a plan with unresolved ambiguity. If the only safe next step is
evidence gathering, write the plan around that investigation instead of
speculative implementation.

## Detailed Questioning Criteria

Questions are required when any of these are unclear:

- target actor, role, permission, tenant, store, company, or customer scope,
- desired business outcome, current behavior, desired behavior, or success
  criteria,
- desired user experience, root-cause target, accepted completion signal, or
  whether the request is about symptom presentation versus cause removal,
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
- desired outcome/user experience and accepted completion signal are explicit
  in user wording or unambiguously supported by source/runtime evidence,
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
business-rule or requester-goal guess.

## Onboarding And UI Guidance Plans

When a request changes onboarding, setup guidance, a wizard, modal, tutorial,
first-login rail, admin guide, or other visible multi-step instruction flow, the
plan must confirm these before implementation:

- user role and scope, such as owner, store manager, staff, customer, store, or
  account,
- current step model and requested step names,
- required step order and completion semantics,
- elements explicitly excluded, such as screenshots, docs links, old URL panels,
  optional confirmations, or support links,
- where each action appears relative to the instruction it supports,
- resume/fallback route or modal reopening behavior,
- safe recipient/provider boundaries for test sends or external actions,
- browser/provider evidence lane and the exact blocker if it cannot run.

## Provider, Auth, Deploy, And Smoke Evidence

Local mock tests are required for deterministic coverage, but they are not full
proof when the reported risk is a deployed artifact, provider callback, real
device/app context, safe production credential, or valid session path.

For these plans, map evidence lanes separately:

- local mock/unit/integration coverage,
- deployed bundle, release, Worker, or script version check,
- real provider or sandbox happy path,
- valid credential/session path when auth is in scope,
- device or app context when device-specific provider behavior is in scope,
- concrete blocker with required credential, environment, operator action, or
  manual checklist when a lane is unavailable.

Do not mark a provider/auth/deploy issue complete using only preflight, invalid
input, unauthenticated `401`, or health checks if the valid path or side effect
is the failure being planned.

## Bug Knowledge Pattern Reuse

For bug/regression work, search `docs/agent-flow/bug-knowledge.md` before task
design and classify any matching prevention pattern:

- requirement/questioning gap,
- business-flow or matrix gap,
- valid-path coverage gap,
- runtime/deploy/provider evidence gap,
- implementation drift,
- UI-intent or action-placement gap,
- non-preventable external/runtime/data behavior.

If a matching preventable pattern exists, add a flow-improvement task before
production implementation tasks. If the bug is not preventable by flow changes,
append or update bug knowledge with future detection and response guidance.

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
### 1.3 Questioning Decision
### 1.4 Goal
### 1.5 Scope / Non-Goals
### 1.6 Acceptance Criteria
### 1.7 User Answers

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
### 2.13 Plan Review Requirement
### 2.14 Playwright Integration Test Plan
### 2.15 Migration / Runtime Enforcement
### 2.16 Open Questions

## 3. Tasks
- [ ] TASK-001 ...

## 4. Readiness
- [ ] Requirements map to tasks
- [ ] User intent and current-state analysis is documented
- [ ] Goal Confirmation is documented, including desired outcome and completion
      signal
- [ ] Questioning Decision is documented
- [ ] No Questions Rationale is source-backed when no questions were asked
- [ ] Business/product ambiguity has been resolved or explicitly blocked
- [ ] Required onboarding docs exist for behavior-changing work
- [ ] Flow Knowledge Update target is explicit
- [ ] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
- [ ] Runtime Causality Gate is complete or explicitly not triggered
- [ ] Onboarding/UI plans confirm step names, order, exclusions, action
      placement, resume/fallback path, and blocked evidence lanes
- [ ] Provider/auth/deploy plans separate mock, deployed-artifact, real
      provider/device, valid-path, and blocker evidence
- [ ] Bug/regression work classifies matching `docs/agent-flow/bug-knowledge.md`
      prevention patterns before task design
- [ ] Business flows map to required tests or blockers
- [ ] Integration Coverage Contract has concrete coverage or waivers
- [ ] Plan Review Requirement is `Required` or `Optional` with a concrete reason
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

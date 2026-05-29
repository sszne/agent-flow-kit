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
### 1.6 User Answers

## 2. Design
### 2.1 Affected Files And Modules
### 2.2 Implementation Approach
### 2.3 Design Policy And Library Selection
### 2.4 Risks And Mitigations
### 2.5 Residual Risk Preflight
### 2.6 Bug Feedback Review
### 2.7 Flow Knowledge Update
### 2.8 Business Flow Matrix
### 2.9 Regression Surface Matrix
### 2.10 Test Design Matrix
### 2.11 Integration Coverage Contract
### 2.12 Playwright Integration Test Plan
### 2.13 Migration / Runtime Enforcement
### 2.14 Open Questions

## 3. Tasks
- [ ] TASK-001 ...

## 4. Readiness
- [ ] Requirements map to tasks
- [ ] User intent and current-state analysis is documented
- [ ] Business/product ambiguity has been resolved or explicitly blocked
- [ ] Required onboarding docs exist for behavior-changing work
- [ ] Flow Knowledge Update target is explicit
- [ ] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
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
frozen or still blocked.

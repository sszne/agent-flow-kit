---
name: flow-start
description: |
  Kick off a new project or feature in Codex by coordinating worker agents for codebase
  mapping, design exploration, and plan drafting. Use when the user says /flow-start,
  wants to start a feature from scratch, or asks for scope/design/tasks before coding.
---

# Flow Start

Codex-native kickoff skill for turning a rough request into an implementation-ready plan.

## Purpose

Use this skill when the user wants to:

- Start a new feature with a clear plan before editing code
- Convert a vague idea into concrete scope, design, and tasks
- Understand which files, modules, and risks are involved before implementation

Do not use this as the default entry point for changes to existing behavior. For bug fixes, regressions, refactors of existing flows, or work touching existing order/dealer/company/mail/PDF/job/search/status/auth/schema behavior, use the stricter `/flow-plan` contract instead.

This skill is plan-first and manager-led. The main Codex agent owns synthesis and user interaction; worker agents gather bounded inputs in parallel.

## Operating Rules

- Activate `context-loader` first.
- Run as a manager by default and use worker agents for bounded subtasks.
- Keep ownership of synthesis, decisions, and shared artifacts in the main agent.
- Ask concise questions in Japanese only when the answer materially changes behavior, data shape, or rollout risk.
- Prefer minimal changes that fit existing conventions.
- Save the plan to `docs/flow/{feature_name}/plan.md` so it can be handed to later implementation work.
- Include plan author metadata near the frozen marker:
  `<!-- plan_author: codex -->`.
- Use parallel workers by default for codebase mapping and design inputs, but only the manager updates shared artifacts.
- For behavior-changing work, include Business Flow Matrix, Regression Surface Matrix, and Test Design Matrix before freezing.
- For behavior-changing work, include an Integration Coverage Contract that maps each affected flow to required happy, exception, permission, boundary, side-effect, and regression coverage or an explicit waiver.
- For behavior-changing work, require `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md`; if missing, run onboarding first.
- Run a residual-risk preflight before plan freeze. If the request may involve missed business flows, natural-language plan ambiguity, runtime/external dependency gaps, weak test infrastructure, or waiver/reviewer risk, warn the user and capture countermeasures or blockers in the plan.
- If discovery shows the request is actually a modification of an existing runtime path, switch to the `/flow-plan` structure before freezing.
- Before drafting the plan, explicitly analyze user intent against the current repository state.
- If actors, business outcome, scope, data ownership, entrypoints, success criteria, side effects, or rollout assumptions are unclear, stop and ask detailed requirement questions before drafting or freezing the plan.
- Ask design policy and library-selection questions when architecture, SDK, ORM, auth, queue, browser-test tooling, or other dependency choices are not decided by existing local patterns.

## Workflow

```
Phase 1: UNDERSTAND
  manager launches codebase/context workers
    ->
Phase 2: DESIGN
  manager integrates worker findings into design
    ->
Phase 3: PLAN
  manager drafts and freezes the plan
```

## Phase 1: Understand

### Step 1: Load shared context

Run the `context-loader` skill first and follow the rules in `.claude/rules/` and `.claude/docs/DESIGN.md`.

### Step 2: Launch discovery workers

Use worker agents by default for parallel discovery. Recommended worker set:

1. `Codebase Mapper`
   - Locate related routes, controllers, models, views, jobs, services, migrations, and tests
   - Identify the existing patterns that should be preserved
   - Check for nearby docs under `docs/`, `.claude/docs/`, and existing `docs/flow/` plans
   - Identify shared partials, shared scripts, actions, mail/PDF/export paths, and browser entrypoints

2. `Constraint Reader`
   - Extract constraints from `DESIGN.md`, rules, and any local docs relevant to the feature
   - Flag rollout, auth, data, or integration concerns
   - Flag migration enforcement, browser verification, and existing business workflow constraints

3. `Plan Skeleton Drafter` (optional for larger features)
   - Turn the current understanding into a first-pass task skeleton
   - Suggest dependency ordering and validation points
   - Draft Red test and verification tasks before implementation tasks

The manager reviews worker output, resolves overlap, and summarizes the current state in a compact "Project Brief".

### Step 3: Analyze intent and current state

Before asking or drafting, the manager must summarize:

- User intent in business/product terms
- Target actors, roles, permissions, and ownership scope if known
- Current repository/runtime state confirmed from files and docs
- Existing related code, missing capability, or product opportunity
- Likely affected routes, screens, APIs, schemas, jobs, mail/PDF/export paths, integrations, or shared services
- Assumptions not yet safe
- Smallest likely scope that satisfies the intent

If the repository does not contain the relevant runtime, or if the request may belong in another repo, ask where the feature should be implemented before planning further.

### Step 4: Clarify only what matters

Ask the user only the smallest set of questions needed to remove ambiguity. Use up to 5 questions, ordered by recommendation priority. Good question categories:

- Goal: what outcome should exist after completion?
- Scope: what should be included and explicitly excluded?
- Actors and permissions: who performs the workflow and under which tenant/store/company/customer scope?
- Current vs desired behavior: what is missing or changing?
- Data rules: ownership, lifecycle, retention, deletion, status transitions, migration/backfill expectations
- Entry points and side effects: screens, APIs, jobs, mail, PDF/export, notifications, audit logs, external APIs
- Constraints: existing APIs, DB limits, auth rules, rollout constraints
- Success criteria: what should be verifiable after implementation?

Present questions with:

- Understanding so far
- Confirmed from code
- Assumptions not yet safe
- Recommended option first

Do not ask implementation-detail questions if worker findings and repository structure already suggest the right answer. If ambiguity remains after the user answers, repeat intent/current-state analysis and ask again before writing or freezing the plan.

### Step 5: Write the Project Brief

Create a short brief in the plan:

```markdown
## Project Brief
- Intent:
- Current state:
- Confirmed from code:
- Assumptions resolved:
- Goal:
- Scope:
- Non-goals:
- Constraints:
- Affected areas:
- Validation:
```

## Phase 2: Design

### Step 6: Choose the minimal fitting approach

Design against the existing codebase, not against an idealized architecture. The manager should integrate worker findings rather than letting workers finalize architecture independently.

- Reuse existing patterns before inventing new ones
- Keep file count and moving parts low unless complexity requires separation
- Note DB, API, UI, auth, queue, mail, or batch impacts explicitly
- Call out migrations, backfills, or operational steps if needed
- Convert business workflow knowledge into explicit test obligations
- Convert normal, error/exception, permission/ownership, boundary, and side-effect paths into integration-test obligations before implementation

### Step 7: Ask design policy and library-selection questions when needed

Ask this only when the decision materially affects architecture, dependency risk, data shape, test strategy, security, performance, or rollout.

Questions are required when:

- Existing project patterns do not clearly decide the architecture or dependency choice
- A new package, framework, SDK, ORM, auth library, queue, browser-test tool, or external service would be introduced
- Multiple local patterns exist and choosing the wrong one would make future maintenance or testing harder
- A library decision changes security, data ownership, migration strategy, deployment, licensing, bundle size, runtime support, or operational risk
- The minimal no-new-library approach is possible but has meaningful tradeoffs against adding a dependency

When asking, present:

- Existing-pattern / no-new-library option first when viable
- Alternative architecture or library options
- Pros and cons
- Decision criteria for user/business impact, maintenance, tests, security, and operations

When no question is needed, document the reason in the plan, for example: "No new library: existing repository/service pattern covers this use case."

### Step 8: Identify risks and tradeoffs

Document the highest-signal risks only:

- Behavioral regressions
- Data integrity or migration risks
- Permission/auth mismatches
- Performance or rollout concerns
- Missing tests or hard-to-verify areas
- Business-flow regressions across adjacent order/dealer/company/mail/PDF/job/search/status paths
- Residual risks from `docs/agent-flow-residual-risk-countermeasures.md`, including missing domain knowledge, weak test infrastructure, external dependencies, and waiver quality

If multiple valid designs exist, recommend one clearly and explain why it is the best local fit.

### Step 9: Manager-worker rules

When workers are active:

- The manager owns the Project Brief, final design choices, and `plan.md`
- Workers return summaries, candidate tasks, and risks, but do not finalize shared artifacts
- Workers should have bounded asks and should not duplicate the same exploration unless perspectives differ
- If a worker uncovers a plan-changing issue, the manager decides whether to ask the user or re-scope the plan

## Phase 3: Plan

### Step 10: Create the plan artifact

Save the plan to `docs/flow/{feature_name}/plan.md`.

Use this structure:

```markdown
# {Feature Title}

## 1. Requirements
### 1.1 Current state
### 1.2 Intent and ambiguity resolution
### 1.3 Goal
### 1.4 Scope / Non-goals
### 1.5 Acceptance criteria

## 2. Design
### 2.1 Affected files and modules
### 2.2 Implementation approach
### 2.3 Design Policy and Library Selection
### 2.4 Risks and mitigations
### 2.5 Residual Risk Preflight
### 2.6 Business Flow Matrix
### 2.7 Regression Surface Matrix
### 2.8 Test Design Matrix
### 2.9 Integration Coverage Contract
### 2.10 Migration / Runtime Enforcement
### 2.11 Open questions

## 3. Tasks
- [ ] TASK-001 ...
- [ ] TASK-002 ...

## 4. Readiness
- [ ] Requirements map to tasks
- [ ] User intent and current-state analysis is documented
- [ ] Business/product ambiguity has been resolved through user answers or explicitly blocked
- [ ] Required onboarding docs exist for behavior-changing work
- [ ] Residual Risk Preflight warnings have countermeasures, setup tasks, or concrete blockers
- [ ] Design policy and library-selection decisions are documented, or explicitly unnecessary because existing patterns decide them
- [ ] Validation commands are identified
- [ ] Risks and assumptions are documented
- [ ] Business flows map to tests or documented blockers
- [ ] Each affected flow maps to required happy, exception, permission, boundary, side-effect, and regression coverage or explicit waivers
- [ ] Regression surfaces map to verification
```

Task lists should be implementation-ready:

- Use stable IDs such as `TASK-001`
- Order tasks by dependency
- Keep each task large enough to matter, but small enough to execute safely
- Mark whether tasks involve code, schema, config, or verification when useful
- Put Red test tasks before Green implementation tasks for TDD work
- Include browser, migration, mail/PDF/job, and build verification tasks when applicable

For decomposition guidance, read `references/task-patterns.md`.

### Step 11: Freeze only when coherent

Once the plan is internally consistent and ready for execution, add a frozen marker at the top:

```markdown
<!-- frozen: v1 YYYY-MM-DD -->
<!-- plan_author: codex -->
```

If the user asks for changes, update the plan and refresh the frozen version only after re-checking consistency.

### Step 12: Close with a concrete handoff

Report:

- What will change
- Which areas are affected
- The main risks
- The exact next step

If the user wants implementation immediately, continue into `/team-implement` style execution with the manager retaining artifact ownership.
Do not start coding until `flow-plan-review` approves the current frozen plan
when review is required. If review is optional, record the optional-review
reason before implementation.

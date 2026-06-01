Specification-Driven Development: Phase 1-3 (SCOPE / SKETCH / READINESS GATE)

User requirements from interactive questioning are combined with codebase analysis to produce a frozen plan document. This prompt guides the creation of a comprehensive implementation plan through structured dialogue.

## Rules

- Never leave ambiguity. Investigate thoroughly before implementation starts.
- Propose minimal necessary implementation based on existing source code.
- Treat `/flow-plan` as the canonical entry point for modifications to existing behavior, bug fixes, regressions, and business-flow-sensitive work.
- Use `/flow-start` only when the work is primarily new-feature discovery or greenfield scope shaping. If the request modifies an existing runtime path, continue here.
- Comments inside `<!-- -->` are AI instructions. `{}` denotes replacement text.
- Architecture reference: fetch from (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/architecture.md). If unavailable, skip and note in plan.
- Code style reference: fetch from (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/code-style-review.md). If unavailable, skip and note in plan.
- Plan template: use the template defined in this document (no external template fetch needed).
- Save plan to `docs/flow/{feature_name}/plan.md`.
- Include plan author metadata near the frozen marker: `<!-- plan_author: claude-code -->`.
- The plan is updated incrementally across phases. Do NOT batch work across phases.
- Before writing the implementation design, explicitly analyze the user's request intent against the current codebase state and ask requirement questions when intent, business behavior, actors, data ownership, entrypoints, or success criteria are unclear.
- If requirement questions are needed, stop after presenting the questions. Do not draft or freeze a plan that carries unresolved business ambiguity.
- Do not silently skip requirement questioning. If no requirement questions are needed, write a source-backed "No Questions Rationale" in the plan before freezing and mention it in the user-facing summary.
- For behavior-changing work, the plan MUST include Business Flow Matrix, Regression Surface Matrix, and Test Design Matrix before freeze.
- Business Flow Matrix rows MUST carry enough domain knowledge for test design: normal path, error/exception paths, permission or ownership paths, boundary paths, side effects, and required integration coverage.
- Test Design Matrix rows MUST trace back to business flows and classify each case as happy, validation, permission, missing relation, boundary, side effect, regression, migration, or browser evidence.
- Behavior-changing work MUST NOT proceed unless `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md` exist. If they are missing, run `agent-flow-onboarding` first.
- When requirement questioning confirms new reusable business-flow knowledge, update `docs/agent-flow/business-flows.md` and/or `docs/agent-flow/integration-scenarios.md`, or document why the knowledge is feature-local and should stay only in this plan.
- Waivers are only valid when they include a concrete reason or blocker. Vague entries such as `N/A`, `manual`, `low risk`, `TBD`, or `later` are not acceptable for uncovered required coverage.
- Before requirements questioning, run the Residual Risk Preflight. If the request may involve business-flow gaps, natural-language plan ambiguity, external/runtime dependency gaps, weak test infrastructure, or waiver/reviewer risk, show a warning and capture required countermeasures in the plan.
- Before proposing behavior-changing code for production-only, browser-network, deploy, auth/session, provider, secret/binding, remote data, or external-runtime symptoms, run the Runtime Causality Gate. Classify whether the likely cause is code, environment/ops, data, deploy artifact, provider/runtime, or inconclusive using runtime evidence when available.
- For bug reports or regressions, run the Bug Feedback Review. If a previous `docs/flow/{feature}/plan.md` exists, identify which part of the prior flow failed and improve the project flow when possible. If the bug cannot be prevented by flow changes, append the lesson to `docs/agent-flow/bug-knowledge.md`.
- Treat order, company-order, dealer-order, pricing, mail, PDF, shipment, search, status transition, auth, and schema changes as business-flow sensitive by default.
- For visible browser behavior or multi-step business workflows, the plan MUST include a Playwright Integration Test Plan before freeze.

## Prerequisites

- Source code exists in the working directory.
- User has provided a feature overview (via $ARGUMENTS).

## Directory Structure

- docs/flow/{feature_name}/
    - plan.md (created in this phase)
    - implementation_report.md (created in /flow-impl phase)

---

## Phase 1: SCOPE

Goal: Fully understand the user's requirements with zero ambiguity.

### Step 1: Load external documents

Fetch architecture and code style documents from the URLs above. If fetch fails, note the failure and continue with local conventions only.

### Step 2: Codebase analysis

Use Glob, Grep, and Read to directly analyze the codebase. Identify:
- Existing onboarding docs under `docs/agent-flow/`; if missing for behavior-changing work, stop and run onboarding first
- Existing related code and patterns
- Current architecture conventions
- Database schema (if applicable)
- API structure (if applicable)
- Business workflows and status transitions
- Related shared partials, scripts, services/actions, jobs, mail, PDFs, and browser entrypoints
- Existing tests that cover the same or adjacent behavior
- Previous `docs/flow/*/plan.md`, `implementation_report.md`, integration evidence, and `docs/agent-flow/bug-knowledge.md` when the request is a bug report or regression

### Step 3: Intent and current-state analysis

Before asking or writing, create a concise internal analysis of the user's request using the Intent and Current-State Analysis Checklist below.

The analysis must answer:
- What business outcome is the user likely asking for?
- Who are the actors and affected user roles?
- What current behavior or missing capability exists in the codebase?
- Which routes, screens, commands, jobs, APIs, schemas, shared services, mail/PDF/export paths, or external integrations could be affected?
- Which parts are confirmed from source evidence, and which parts are assumptions?
- What is the smallest implementation that satisfies the likely intent without expanding scope?

If the repository does not contain the relevant runtime, mark that as a blocking ambiguity and ask where implementation should happen.

### Step 4: Bug Feedback Review

Run this step when the user's request is a bug report, regression, production incident, QA finding, support report, or failure after a previous implementation.

Search for prior context:

- `docs/flow/*/plan.md`
- `docs/flow/*/implementation_report.md`
- `docs/flow/*/integration-test/*/test-review.md`
- `docs/flow/*/integration-test/*/business-flow-impact.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/bug-knowledge.md`

If a previous plan exists, classify the flow failure:

| Failure ID | Flow failure point | Examples | Required response |
| --- | --- | --- | --- |
| BF-001 | Requirement/questioning gap | Actor, permission, lifecycle, or side effect was not asked | Add missing question pattern to current plan and update business-flow docs |
| BF-002 | Business Flow Matrix gap | Affected workflow or exception path was absent | Add flow row or exception path to `docs/agent-flow/business-flows.md` |
| BF-003 | Regression Surface Matrix gap | Shared service, API, job, mail/PDF, schema, cache/search, or UI surface was missed | Update regression surface docs and required verification |
| BF-004 | Test Design Matrix gap | Happy path existed but validation, permission, boundary, side effect, or regression case was missing | Add test case type to current plan and integration scenarios |
| BF-005 | Integration Coverage Contract gap | Required coverage was waived, vague, or mapped to weak evidence | Tighten coverage contract and waiver rule for this project |
| BF-006 | Residual Risk Preflight miss | External/runtime/test-infrastructure/reviewer risk was not flagged | Add a project-specific trigger to residual-risk notes or bug knowledge |
| BF-007 | Implementation drift | Implementation changed behavior outside the frozen plan | Add implementation/review guard and regression test |
| BF-008 | Evidence/review gap | Playwright, integration evidence, or team-review missed the bug | Add review checklist item or evidence requirement |
| BF-009 | Not preventable by flow | Production-only data, provider outage, unknown legacy behavior, or rare concurrency issue | Document as bug knowledge with detection and response guidance |

If the bug can be prevented by improving the flow, add a "Flow Improvement Task" before implementation tasks. Examples:

- update `docs/agent-flow/business-flows.md`
- update `docs/agent-flow/integration-scenarios.md`
- update `docs/agent-flow/bug-knowledge.md`
- update `.claude/rules/testing.md`
- update `.claude/docs/DESIGN.md`
- update `.agent-flow/config.json` risky paths
- add or strengthen Feature/API integration, Unit, Browser, Migration, or review evidence

If the bug cannot be prevented by flow changes, append an entry to `docs/agent-flow/bug-knowledge.md` with the trigger, symptoms, diagnosis, why the flow could not catch it, and future response.

### Step 5: Residual Risk Preflight

Before requirements questioning, inspect the user's request, onboarding docs, current code, and known runtime/test constraints against `docs/agent-flow-residual-risk-countermeasures.md`.

Classify whether the request may hit any of these residual-risk categories:

| Risk ID | Category | Trigger examples | Required warning / countermeasure |
| --- | --- | --- | --- |
| RR-001 | Missed business flows | New or changed business workflow, status transition, auth/tenant scope, operator workflow, pricing, order, mail/PDF/export, jobs, data lifecycle | Warn that undocumented business rules may exist; require domain-owner/user confirmation and Business Flow Matrix coverage |
| RR-002 | Natural-language plan quality | Large matrix, cross-module behavior, vague scope, many waivers, multiple flows sharing tests | Warn that CI can only check structure; require stable flow IDs, test IDs, explicit traceability, and reviewer sign-off |
| RR-003 | Runtime/external dependency gap | External API, payment, webhook, queue, schedule, mail, PDF/rendering, storage, search, cache, auth provider, migration/deploy path | Warn that local flow cannot prove real runtime behavior without sandbox/fake/staging; require environment or blocker |
| RR-004 | Weak test infrastructure | Missing factories/fixtures, no integration runner, no auth helper, no DB reset, no Playwright setup, unstable selectors | Warn that required tests may be blocked; require test harness preparation tasks before implementation |
| RR-005 | Reviewer/waiver quality | Manual-only verification, low-risk claims, unresolved blockers, critical auth/data/migration changes | Warn that waiver abuse can hide regressions; require concrete waiver reasons and team-review focus |

If any risk applies:

- Present a short `Residual Risk Warning` before or alongside requirement questions.
- Ask only the minimum additional questions needed to confirm the risk, environment, or blocker.
- Add `Residual Risk Preflight` to the plan.
- Add required setup or blocker tasks before implementation tasks.
- Do not freeze the plan if a required environment or domain answer is missing and no concrete blocker is acceptable.

### Step 6: Runtime Causality Gate

Before implementation design, classify whether the symptom could be caused by
environment/runtime state rather than source code. This gate is required when
any of these triggers are present:

- browser reports CORS, `ERR_FAILED`, network failure, or opaque 5xx symptoms,
- the problem appears only in production/staging or cannot be reproduced
  locally,
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
- smoke checks cover only shallow paths such as preflight, invalid input,
  unauthenticated `401`, or health checks while the valid happy path or
  side-effect path is unproven.

When triggered, add a `Runtime Causality Gate` section to the plan and fill:

| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | GitHub Actions, deploy log, release SHA, runtime script version | current / stale / unknown |
| Browser symptom vs server outcome | DevTools plus server/runtime logs captured for the same request | browser symptom / app error / runtime limit |
| Runtime log | wrangler tail, provider logs, app logs, queue logs, webhook logs | ok / exception / exceededCpu / timeout / provider error |
| Representative paths | preflight, invalid path, valid happy path, side-effect path | shallow only / full path covered / blocked |
| Environment bindings | secrets, env vars, DB/D1 binding, storage bucket, provider config | aligned / mismatch / unknown |
| Remote data state | read-only query, admin diagnostic, migration status, seed/version marker | expected / stale / unknown |
| Classification | evidence-backed conclusion | code defect / environment-ops defect / data defect / deploy artifact mismatch / provider-runtime defect / inconclusive |

Do not treat browser CORS text as root-cause evidence by itself. If runtime
evidence is unavailable, record a concrete blocker or add a setup task before
code-changing tasks. If classification remains inconclusive, focus the plan on
evidence gathering rather than speculative fixes.

### Step 7: Flow Knowledge Update Check

Before requirements questioning and again after user answers, compare the request and confirmed answers with `docs/agent-flow/business-flows.md` and `docs/agent-flow/integration-scenarios.md`.

Classify whether the plan discovers reusable project knowledge:

| Knowledge type | Examples | Required response |
| --- | --- | --- |
| New business flow | New login gate, onboarding path, order status transition, operator workflow, external-service setup flow | Add or update a row in `docs/agent-flow/business-flows.md` |
| New exception or permission path | Role-specific block, cross-tenant behavior, missing setup state, partial external verification | Add exception/permission/boundary details to the relevant business-flow row |
| New side effect or external dependency | Mail/PDF/job/webhook/cache/search/indexing/payment/provider call | Add side effect and regression risk to business-flow docs |
| New integration scenario | Multi-step browser flow, auth redirect, external provider mock/sandbox path, safe test delivery | Add or update `docs/agent-flow/integration-scenarios.md` |
| Feature-local knowledge only | One-off copy, temporary experiment, unreusable admin-only task | Keep in the plan and write the reason in Flow Knowledge Update |

If reusable knowledge is found:

- Add a DIRECT task before implementation to update `docs/agent-flow/business-flows.md` and/or `docs/agent-flow/integration-scenarios.md`.
- Reflect the same knowledge in the plan's Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, and Integration Coverage Contract.
- Do not freeze the plan until the update target and task are explicit.

If no reusable knowledge is found:

- Document "No reusable project-level flow knowledge discovered" with a concrete reason in the plan.

### Step 8: Requirements questioning

Use the Requirements Question Template below. Ask a maximum of 5 questions in selection format. Order by recommendation priority. Only ask questions where the answer is genuinely ambiguous -- skip questions with obvious answers.

Questions are required when any of these are unclear:
- Target actor, role, permission, or tenant/store/company/customer scope
- Desired business outcome or success criteria
- Current behavior vs desired behavior
- Data ownership, lifecycle, status transition, or deletion/retention rule
- User-visible entrypoint, screen placement, wording, or workflow order
- Side effects such as mail, PDF/export, jobs, notifications, audit logs, or external APIs
- Migration or data backfill expectations
- Compatibility with an existing shared flow

Questions may be skipped only when all of these are true:
- Actor/scope, current behavior, desired behavior, and success criteria are directly supported by user wording or source evidence.
- Affected screens, routes, APIs, jobs, mail/PDF/export paths, schema, shared services, and external dependencies have been inspected or ruled out.
- Permission/ownership, exception paths, boundary values, lifecycle rules, and side effects can be described without guessing.
- Migration, backfill, deploy/runtime enforcement, and existing-data compatibility are either not involved or source-backed.
- Onboarding docs, existing plans, tests, and code do not conflict with the planned behavior.
- Any remaining assumptions are source-backed, low-risk, explicitly out of scope, or recorded as concrete blockers/waivers.

Do not treat "no obvious ambiguity" as enough. If questions are skipped, the No Questions Rationale must explain why implementation would not require a business-rule guess.

When questions are needed, present:
- A short "Understanding so far" summary.
- A short "Confirmed from code" list with file/path evidence.
- A short "Assumptions not yet safe" list.
- Up to 5 requirement questions using the Requirements Question Template.

When no questions are needed, do not proceed silently. Record:
- Questioning decision: `No questions needed`
- Evidence used: concrete files, routes, tests, schema, docs, or explicit user wording
- Safe assumptions: any assumptions that remain but are low-risk or out of scope, with reason
- User-facing summary: one short sentence explaining why planning can proceed without questions

### Step 9: Iterate

If ambiguity remains after user answers, return to Step 3. Repeat until all requirements are clear. Re-run the Flow Knowledge Update Check whenever answers add or change business-flow, exception, permission, side-effect, or integration-scenario knowledge.

### Step 10: Escalation check

Evaluate whether this feature requires EARS formal notation using the following criteria:

| Condition | Use EARS |
|-----------|----------|
| Payment/billing logic | Yes |
| Authentication/authorization changes | Yes |
| Data migration (irreversible operations) | Yes |
| 3+ state transitions | Yes |
| External API integration with 3+ conditional branches | Yes |
| None of the above | No -- use acceptance criteria checklist |

If EARS is needed, write requirements using the EARS Notation Template below. Otherwise, write acceptance criteria as a checklist.

### Step 11: Write plan.md "Requirements" section

Create `docs/flow/{feature_name}/plan.md` and write the Requirements section
using the plan template.

---

## Phase 2: SKETCH

Goal: Design the implementation approach and decompose into tasks.

### Step 12: Implementation questioning

Use the Implementation Question Template below. Present:
- Entity structure options with Pros/Cons and code examples
- Architecture alternatives with command/query tables
- Technical detail choices in selection format
- Design policy and library-selection choices when the decision materially affects architecture, dependency risk, data shape, test strategy, security, performance, or rollout

Only ask questions where multiple valid approaches exist. Skip sections where the answer is obvious from existing code.

If implementation questions are needed, first restate the resolved requirement intent and the minimal codebase-conforming direction, then ask only the implementation questions that cannot be decided from existing patterns.

Design policy and library-selection questions are required when:
- Existing project patterns do not clearly decide the architecture or dependency choice
- A new package, framework, SDK, ORM, auth library, queue, browser-test tool, or external service would be introduced
- Multiple local patterns exist and choosing the wrong one would make future maintenance or testing harder
- A library decision changes security, data ownership, migration strategy, deployment, licensing, bundle size, runtime support, or operational risk
- The minimal no-new-library approach is possible but has meaningful tradeoffs against adding a dependency

When no question is needed, document the reason in Design Decisions, for example: "No new library: existing repository/service pattern covers this use case."

### Step 13: Iterate

If implementation ambiguity remains, return to Step 12. Repeat until all design decisions are clear.

### Step 14: On-demand artifact check

Generate additional sections based on these conditions:

| Artifact | Condition |
|----------|-----------|
| Architecture overview | Always |
| Bug Feedback Review | Bug reports, regressions, QA findings, production incidents, or failures after prior implementation |
| Schema section | DB changes (table/column/relation additions) |
| API endpoints | API additions or modifications |
| Mermaid diagram | 3+ component data flow OR 4+ step sequence |
| Business Flow Matrix | Always for behavior-changing work |
| Regression Surface Matrix | Always for behavior-changing work |
| Test Design Matrix | Always for TDD tasks and risky DIRECT tasks |
| Integration Coverage Contract | Always for behavior-changing work |
| Flow Knowledge Update | Always for behavior-changing work; required when confirmed answers add reusable business-flow, exception, permission, side-effect, or integration-scenario knowledge |
| Residual Risk Preflight | Always when any residual risk category applies |
| Runtime Causality Gate | Production-only, deploy/runtime/provider, browser-network, auth/session, secret/binding, remote data, or external-runtime symptoms |
| Playwright Integration Test Plan | Visible browser behavior OR multi-step business workflow |

### Step 13: Task decomposition

Break the implementation into tasks:
- Assign each task a unique ID: TASK-001, TASK-002, etc.
- Classify each task as **TDD** (coding, business logic, tests) or **DIRECT** (setup, config, docs)
- Identify dependencies between tasks
- Order tasks respecting dependencies
- Add a checkbox to each task for progress tracking
- Put Red test tasks before implementation tasks for TDD work
- Include explicit verification tasks for browser, migration, mail/PDF/job, or build checks when applicable
- Put required residual-risk setup tasks before implementation tasks, for example test harness setup, sandbox credentials, seed/reset, or domain confirmation
- Put required `docs/agent-flow/*` knowledge update tasks before implementation tasks when Flow Knowledge Update identifies reusable project knowledge
- Put required flow-improvement or bug-knowledge tasks before implementation tasks for bug/regression work

### Step 14: Write plan.md "Design" and "Tasks" sections

Update `docs/flow/{feature_name}/plan.md` with Design and Tasks sections (sections 2 and 3 of the plan template).

---

## Phase 3: READINESS GATE

Goal: Verify plan completeness and consistency before freezing.

### Step 13: Architecture compliance

Re-read the architecture document. Verify all design decisions comply. Note any deviations.

### Step 14: Code style compliance

Re-read the code style document. Verify all code examples and naming conventions in the plan comply.

### Step 15: Consistency check

Verify traceability:
- Every requirement maps to at least one task
- Every task maps to at least one requirement
- Every requirement traces back to user intent, codebase evidence, or an explicit user answer
- Every assumption is either resolved, marked out of scope, or listed as a blocker
- Every triggered residual-risk warning has a resolved countermeasure, setup task, or concrete blocker
- Design decisions are consistent with requirements
- Task dependencies form a valid DAG (no cycles)
- Every affected business flow maps to at least one test or documented low-risk/blocker reason
- Every affected business flow maps normal, error/exception, permission/ownership, boundary, and side-effect paths to tests or explicit waivers
- Every risky regression surface maps to Feature, Unit, Browser, Migration, or manual verification coverage
- Every required integration scenario has deterministic setup, assertions, and evidence expectations
- Visible browser workflows map to at least one Playwright scenario and major-step screenshots
- Requirement questioning was performed, or No Questions Rationale is documented with source evidence

### Step 16: Issue classification

Classify any found issues:
- **Blocking**: Must be resolved before implementation (inconsistencies, missing requirements)
- **Non-blocking**: Should be noted but won't prevent implementation (minor style issues, optimization opportunities)
- **Info**: Observations for awareness (potential future improvements)

### Step 17: Present blocking issues

If blocking issues exist, present a maximum of 3 to the user for resolution. After resolution, return to Step 15.

### Step 18: Freeze and approve

- Add `<!-- frozen: v1 {YYYY-MM-DD} -->` tag to the top of plan.md
- Add `<!-- plan_author: claude-code -->` next to the frozen tag
- Write the READINESS section (section 4 of the plan template)
- Present the complete plan to the user and instruct that `/flow-plan-review`
  must approve it before `/flow-impl` or `team-implement`
- If the user requests changes, remove the frozen tag, make changes, and restart from Step 15

---

## Requirements Question Template

<!--
Collect only essential information for plan creation. Ask about behavior, not implementation details.
Maximum 5 questions. Order by recommendation priority (highest first).
Skip questions where the answer is obvious from existing code.
If Residual Risk Preflight found risks, include the warning before questions.
-->

## Residual Risk Warning

The request appears to involve the following residual-risk categories:

| Risk ID | Why it may apply | What must be confirmed or prepared |
| --- | --- | --- |
| RR-{NNN} | {Source-backed reason from prompt/code/docs} | {Domain answer, environment, test harness, sandbox, reviewer sign-off, or blocker} |

## Bug Feedback Warning

This request appears to be a bug report or regression. I will compare it against any previous flow plan and classify whether the problem came from the planning flow, implementation drift, verification gap, review gap, or a project-specific issue that should become bug knowledge.

| Prior artifact | Found? | How it will be used |
| --- | --- | --- |
| Previous `docs/flow/*/plan.md` | Yes/No | Identify missed requirements, matrices, coverage, residual-risk warnings, or waivers |
| Previous implementation report | Yes/No | Check implementation drift and verification evidence |
| Previous integration evidence | Yes/No | Check screenshot, HTML, test review, and business-flow impact coverage |
| Existing bug knowledge | Yes/No | Reuse known symptoms, triggers, and response guidance |

## Understanding So Far

- User intent: {What the user appears to want in business terms}
- Current state from code: {What was confirmed from files/routes/schema/tests}
- Smallest likely scope: {Minimal behavior change that satisfies the intent}

## Assumptions Not Yet Safe

- {Assumption that must be confirmed or disproven before implementation}

To create the plan, please answer the following questions. Multiple selections are allowed.

## Requirements Analysis

### {Question title}
{Question about behavior, not technical details. e.g., "What capabilities should the coupon feature have?"}

a-1. [{Proposed option title} (Recommended)]: [{Description}]
a-2. [{Proposed option title}]: [{Description}]
a-3. [{Proposed option title}]: [{Description}]

### {Question title}
{Another behavioral question}

b-1. [{Proposed option title} (Recommended)]: [{Description}]
b-2. [{Proposed option title}]: [{Description}]

---

## Implementation Question Template

<!--
Collect implementation decisions. Only ask where multiple valid approaches exist.
Do NOT force questions for every section -- skip where the answer is clear.
-->

## Resolved Requirement Intent

- {Requirement intent already confirmed by user answers and codebase evidence}
- {Existing implementation pattern that should be followed}

## Remaining Implementation Ambiguity

- {Only list implementation choices that cannot be resolved from existing code}

## Entity Structure

### {Question title}
{e.g., "Multiple entity designs are possible for the coupon. Which approach do you prefer?"}

e-a-1. [{Proposed approach} (Recommended)]

{Brief description of the approach}

Pros:
- {Advantage}
Cons:
- {Disadvantage}

```
{Code example showing the entity/model structure}
```

e-a-2. [{Alternative approach}]

{Brief description}

Pros:
- {Advantage}
Cons:
- {Disadvantage}

```
{Code example}
```

## Architecture

### Architecture Structure

a-a-1. Architecture Option 1

{Description, e.g., "Handle coupon validation and update with a single query and command."}

Pros:
- {Advantage}
Cons:
- {Disadvantage}

| Name | Description | Arguments | Return / Error Types | Implementation |
| --- | --- | --- | --- | --- |
| {path} | {description} | {args} | {return type} | {new/modify} |

a-a-2. Architecture Option 2

{Description}

| Name | Description | Arguments | Return / Error Types | Implementation |
| --- | --- | --- | --- | --- |

## Technical Details

<!--
Ask about ORM selection, new library installs, SDK selection, auth/session dependency, queues, browser-test tooling, etc.
Skip if all required functionality exists in already-installed libraries.
-->

### {Question title}
{e.g., "What persistence mechanism should be used?"}

t-a-1. [{Option}]
t-a-2. [{Option}]

## Design Policy and Library Selection

<!--
Ask this only when architecture policy or dependency choice cannot be resolved from existing code and docs.
Prefer the smallest approach that matches local conventions. If a new library is proposed, include no-new-library and existing-pattern options when viable.
-->

### {Question title}
{e.g., "Which implementation policy should this feature follow?"}

d-a-1. [{Existing local pattern / no new library (Recommended)}]

{Why this is likely best for this codebase}

Pros:
- {Advantage}
Cons:
- {Tradeoff}

d-a-2. [{New library or alternate architecture}]

{Why this might be worth considering}

Pros:
- {Advantage}
Cons:
- {Dependency, migration, security, or rollout risk}

Decision criteria:
- User/business impact: {impact}
- Maintenance impact: {impact}
- Test impact: {impact}
- Security/operations impact: {impact}

---

## EARS Notation Template

<!-- Used only when escalation check triggers EARS. -->

### Normal Requirements (SHALL)

- REQ-{NNN}: The system SHALL {behavior}.

### Conditional Requirements (WHEN/IF-THEN)

- REQ-{NNN}: WHEN {condition}, the system SHALL {behavior}.
- REQ-{NNN}: IF {condition} THEN the system SHALL {behavior}.

### Constraint Requirements (MUST)

- REQ-{NNN}: The system MUST {constraint}.

---

## Intent and Current-State Analysis Checklist

<!--
Use this before requirements questioning. This section is a working checklist for the agent;
include the results in plan.md only where useful.
-->

| Item | Question | Required evidence |
| --- | --- | --- |
| User intent | What business result or operator/user workflow is being requested? | User prompt plus nearby docs/issues if available |
| Actor and permission | Who performs the action, and under which role, tenant, store, company, or customer scope? | Routes, middleware, policies, guards, existing screen ownership |
| Current state | What currently happens, and where is it implemented? | Files, routes, controllers/actions, views/components, schema, tests |
| Desired behavior | What should be different after the change? | User answer or explicit acceptance criterion |
| Business rules | What state transitions, validation, lifecycle, retention, pricing, notification, or ownership rules apply? | Existing domain/service/config/test evidence |
| Entry points | Which screens, APIs, commands, jobs, mail/PDF/export paths, or external integrations can trigger or observe the behavior? | Route lists, command lists, job/mail/PDF services, frontend entrypoints |
| Exception paths | What validation failures, permission failures, missing relations, external failures, and boundary values must be preserved? | Existing validation, policies, error handling, service failure paths, tests |
| Residual risk | Does the request touch undocumented business rules, natural-language ambiguity, external/runtime dependencies, weak test infrastructure, or waiver/reviewer risk? | `docs/agent-flow-residual-risk-countermeasures.md`, onboarding docs, runtime/test config, user answers |
| Bug feedback | Is this a bug/regression with a previous plan or known bug pattern? Which flow step failed? | Prior `docs/flow/*`, implementation reports, integration evidence, review notes, `docs/agent-flow/bug-knowledge.md` |
| Flow knowledge update | Did questioning confirm reusable business-flow, exception, permission, side-effect, or integration-scenario knowledge missing from onboarding docs? | `docs/agent-flow/business-flows.md`, `docs/agent-flow/integration-scenarios.md`, user answers |
| Regression surfaces | What adjacent shared flows can break even if not directly edited? | Shared partials/scripts/services/actions/schema/tests |
| Minimal scope | What is the smallest codebase-conforming change that satisfies the intent? | Existing patterns and alternatives considered |
| Open questions | Which unknowns would cause implementation rework or business-rule guesses? | Questions to user; block freeze until resolved |

---

## plan.md Template

```markdown
# {feature_name} Plan

<!-- frozen: v{N} {YYYY-MM-DD} -->
<!-- plan_author: claude-code -->

## 1. Requirements

### 1.1 Overview
{Feature overview and background}

### 1.2 Current State Analysis
{Analysis of existing codebase relevant to this feature}

### 1.3 Intent and Ambiguity Resolution
{Summarize user intent, confirmed source evidence, user answers, remaining assumptions, and why any unanswered items are safe or out of scope. If unresolved ambiguity remains, do not freeze the plan.}

### 1.4 Residual Risk Preflight
<!-- Include when any residual risk category applies. If none applies, write "No residual-risk category triggered beyond normal behavior-change risk." -->

| Risk ID | Category | Applies? | Evidence | Warning to user | Required countermeasure / environment | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RR-001 | Missed business flows | Yes/No | {prompt/code/docs evidence} | {warning shown or N/A} | {domain-owner answer, examples, logs, onboarding docs} | Resolved / Blocked / Accepted with reason |
| RR-002 | Natural-language plan quality | Yes/No | {matrix/scope evidence} | {warning shown or N/A} | {stable IDs, traceability, reviewer sign-off} | Resolved / Blocked / Accepted with reason |
| RR-003 | Runtime/external dependency gap | Yes/No | {external API/job/mail/PDF/storage/search/auth/migration evidence} | {warning shown or N/A} | {sandbox/fake/staging/local service/credentials} | Resolved / Blocked / Accepted with reason |
| RR-004 | Weak test infrastructure | Yes/No | {test harness/config evidence} | {warning shown or N/A} | {factories, fixtures, DB reset, auth helper, Playwright setup} | Resolved / Blocked / Accepted with reason |
| RR-005 | Reviewer/waiver quality | Yes/No | {waiver/manual/critical flow evidence} | {warning shown or N/A} | {concrete waiver reason, team-review focus, CODEOWNERS/domain review} | Resolved / Blocked / Accepted with reason |

### 1.5 Bug Feedback Review
<!-- Required for bug reports, regressions, QA findings, production incidents, or failures after prior implementation. If not applicable, write "Not applicable: not a bug/regression request." -->

| Item | Result |
| --- | --- |
| Previous plan found | Yes/No: {path or reason} |
| Previous implementation report found | Yes/No: {path or reason} |
| Previous integration evidence found | Yes/No: {path or reason} |
| Existing bug-knowledge entry found | Yes/No: {entry or reason} |

| Failure ID | Flow failure point | Evidence | Flow improvement possible? | Required action |
| --- | --- | --- | --- | --- |
| BF-{NNN} | {Requirement gap / Matrix gap / Coverage gap / Implementation drift / Evidence gap / Not preventable by flow} | {source evidence} | Yes/No | {update business-flow docs, integration scenarios, testing rules, bug knowledge, or current plan} |

Bug knowledge update:
- Needed: Yes/No
- Target: `docs/agent-flow/bug-knowledge.md`
- Entry summary: {trigger, symptoms, root cause, why flow did/did not catch it, future response}

### 1.6 Runtime Causality Gate
<!-- Required when production-only, deploy/runtime/provider, browser-network, auth/session, secret/binding, remote data, or external-runtime symptoms may be involved. If not triggered, write "Not triggered: {source-backed reason}." -->

| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | {GitHub Actions/deploy log/release SHA/runtime script version or blocker} | current / stale / unknown |
| Browser symptom vs server outcome | {DevTools + server/runtime logs for same request or blocker} | browser symptom / app error / runtime limit / unknown |
| Runtime log | {wrangler tail/provider logs/app logs/queue logs/webhook logs or blocker} | ok / exception / exceededCpu / timeout / provider error / unknown |
| Representative paths | {preflight/invalid/valid happy path/side-effect path evidence} | shallow only / full path covered / blocked |
| Environment bindings | {secrets/env vars/DB binding/storage bucket/provider config evidence} | aligned / mismatch / unknown |
| Remote data state | {read-only query/admin diagnostic/migration status/seed marker or blocker} | expected / stale / unknown |
| Classification | {evidence-backed conclusion} | code defect / environment-ops defect / data defect / deploy artifact mismatch / provider-runtime defect / inconclusive |

Required response:
- If classification is `inconclusive`, implementation tasks must gather evidence before speculative code changes.
- If runtime evidence is unavailable, record the blocker and the exact command, credential, or operator access needed.
- Do not use browser CORS/network text alone as root-cause evidence.

### 1.7 Flow Knowledge Update
<!-- Required for behavior-changing work. Capture whether confirmed requirement answers should update project-level business-flow docs. -->

| Item | Result |
| --- | --- |
| Existing business-flow docs reviewed | Yes/No: `docs/agent-flow/business-flows.md` |
| Existing integration-scenario docs reviewed | Yes/No: `docs/agent-flow/integration-scenarios.md` |
| New reusable business flow found | Yes/No: {flow name or reason} |
| New exception / permission / boundary path found | Yes/No: {path or reason} |
| New side effect / external dependency found | Yes/No: {side effect or reason} |
| New integration scenario found | Yes/No: {scenario or reason} |
| Feature-local only | Yes/No: {why it should remain only in this plan} |

Required documentation updates:

| Target document | Update needed? | Summary of update | Task ID |
| --- | --- | --- | --- |
| `docs/agent-flow/business-flows.md` | Yes/No | {business-flow row, exception path, permission path, side effect, regression risk} | TASK-{NNN} or N/A |
| `docs/agent-flow/integration-scenarios.md` | Yes/No | {scenario, setup, assertions, evidence, mock/sandbox requirement} | TASK-{NNN} or N/A |

### 1.8 Questioning Decision
<!-- Required. If no questions were asked, this is the guardrail that prevents silent planning. -->

- Requirement questions asked: Yes/No
- No Questions Rationale: {If No, cite the source-backed reason questions were unnecessary}
- User answers used: {If Yes, summarize answers; if No, write "No new user answers required"}
- Remaining safe assumptions: {Assumptions that are source-backed, low-risk, or explicitly out of scope}

### 1.9 Requirements List
<!-- EARS notation if escalated, otherwise acceptance criteria checklist -->

#### Acceptance Criteria
- [ ] {Criterion}
- [ ] {Criterion}

### 1.10 Scope
**In scope:**
- {Item}

**Out of scope:**
- {Item}

## 2. Design

### 2.1 Architecture Overview
{Always included. High-level design description.}

### 2.2 Schema Changes
<!-- Include only if DB changes are needed -->

### 2.3 API Endpoints
<!-- Include only if API additions/modifications are needed -->

### 2.4 Data Flow
<!-- Include only if 3+ component data flow or 4+ step sequence -->
<!-- Use Mermaid diagram when applicable -->

### 2.5 Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| {Decision} | {Why} | {What else was evaluated} |

### 2.6 Design Policy and Library Selection

<!-- Include when design policy, dependency choice, SDK/ORM/auth/queue/test-tool selection, or no-new-library decision matters. -->

| Decision Area | Selected Approach | Why It Fits | Alternatives Considered | New Dependency? | Risk / Mitigation |
| --- | --- | --- | --- | --- | --- |
| {Architecture/library/tooling area} | {Selected approach} | {Rationale} | {Alternatives} | Yes/No | {Risk and mitigation} |

### 2.7 Business Flow Matrix
<!-- Required for behavior-changing work. This turns domain knowledge into implementation and test obligations. -->

| Flow | Actor / scope | Entry point | Existing behavior | New behavior | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {Order/dealer/company/mail/PDF/job/search/status flow} | {role/tenant/company/customer scope} | {route/screen/API/job/mail/PDF} | {current behavior} | {expected behavior} | {happy workflow} | {validation, missing relation, external failure, rollback, not found} | {forbidden, cross-tenant, min/max/null/empty edge cases} | {mail/PDF/export/job/audit/cache/search/index changes} | {what could regress} | {Feature/API integration, Unit, Browser, Migration, Manual with reason} |

### 2.8 Regression Surface Matrix
<!-- Inspect indirect effects, not only directly edited files. -->

| Surface | Affected? | Covered flows | Evidence | Required verification |
| --- | --- | --- | --- | --- |
| Routes/controllers/API handlers | Yes/No | {flow IDs} | {files/routes inspected} | {Feature/API integration/manual check/N/A} |
| Screens/components/client JS | Yes/No | {flow IDs} | {views/components/scripts inspected} | {Browser/Playwright check/N/A} |
| Shared services/actions/hooks | Yes/No | {flow IDs} | {shared implementation inspected} | {Regression unit/integration test/N/A} |
| Schema/migrations | Yes/No | {flow IDs} | {migrations/deploy path inspected} | {migration command/enforcement check/N/A} |
| Jobs/schedules/queues | Yes/No | {flow IDs} | {commands/jobs inspected} | {Feature/command integration test/N/A} |
| Mail/PDF/export/notifications | Yes/No | {flow IDs} | {templates/services inspected} | {render/assertion/manual check/N/A} |
| Auth/permissions/tenant scope | Yes/No | {flow IDs} | {middleware/policies/session inspected} | {permission integration/browser check/N/A} |
| External APIs/storage/cache/search | Yes/No | {flow IDs} | {clients/adapters/config inspected} | {mocked-boundary integration test/N/A} |

### 2.9 Test Design Matrix
<!-- Red tests must be listed before implementation starts. -->

| Test ID | Level | Case type | Target | Data setup / preconditions | Scenario | Assertions | Covers flow/risk | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | Feature/API integration | Happy | {test file} | {seed/factory/auth/session setup} | {primary business workflow} | {DB/API/side-effect assertions} | {flow/risk} | {command/report path} |
| TEST-002 | Feature/API integration | Validation / permission / missing relation / boundary / side effect / regression | {test file} | {invalid/cross-scope/missing/external-failure setup} | {exception workflow} | {error response, no partial write, no forbidden exposure, side effect absent/present} | {flow/risk} | {command/report path} |
| TEST-003 | Unit | Pure logic | {test file} | {input object/value} | {isolated rule} | {return/error value} | {flow/risk} | {command/report path} |
| TEST-004 | Browser / Playwright | Browser evidence | {screen/spec} | {seeded user and route state} | {visible multi-step workflow} | {visible result and screenshots} | {flow/risk} | {index.html/screenshots} |

### 2.10 Integration Coverage Contract
<!-- Required for behavior-changing work. Every affected flow needs coverage or a named waiver before implementation starts. -->

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| {Flow ID/name} | {Feature/API integration + Unit + Browser/Migration as needed} | {Happy, validation, permission, missing relation, boundary, side effect, regression} | {N/A or concrete reason} |

Coverage rules:
- Each affected business flow must have at least one Feature/API integration test or an explicit low-risk waiver.
- Each changed shared service/action/hook must have either direct unit coverage or coverage through an integration test that exercises the shared path.
- Validation, permission, missing relation, and boundary cases may be grouped only when the assertion proves the same business rule.
- Side effects such as mail, PDF/export, jobs, audit logs, notifications, cache/search updates, and external API calls must be asserted or explicitly out of scope.
- Browser-visible or multi-step workflows require Playwright evidence unless blocked with a concrete reason.
- Waivers must include a reason marker such as `because`, `reason`, `blocked by`, `out of scope`, `理由`, `根拠`, `ブロック`, or `対象外`.
- `N/A`, `manual`, `low risk`, `TBD`, `later`, and blank waiver entries are invalid unless the row is fully covered and no waiver is being used.

### 2.11 Migration / Runtime Enforcement
<!-- Required when schema or deploy/startup assumptions are involved. -->

- Migration needed: Yes/No
- Migration enforcement path: {entrypoint/deploy/startup path or N/A}
- Runtime validation command: `{command or N/A}`

### 2.12 Playwright Integration Test Plan
<!-- Required for visible browser behavior or multi-step business workflows. -->

| Scenario ID | Business flow | Entry point | Major steps requiring screenshots | Expected result | Risk covered |
| --- | --- | --- | --- | --- | --- |
| PW-001 | {flow from Business Flow Matrix} | {URL/modal/state} | {step 1, step 2, step 3} | {expected browser-visible result} | {regression risk} |

Evidence output:
- `docs/flow/{feature_name}/integration-test/{run_id}/index.html`
- `docs/flow/{feature_name}/integration-test/{run_id}/screenshots/`
- `docs/flow/{feature_name}/integration-test/{run_id}/test-review.md`
- `docs/flow/{feature_name}/integration-test/{run_id}/business-flow-impact.md`

## 3. Tasks

### 3.1 Overview
- Total tasks: {N}
- TDD tasks: {N}
- DIRECT tasks: {N}

### 3.2 Task List

#### TASK-001: {Task title}
- [ ] **Completed**
- **Type**: TDD / DIRECT
- **Requirements**: {REQ-NNN or acceptance criteria reference}
- **Dependencies**: {TASK-NNN or "None"}
- **Details**:
  - {Implementation detail}
- **Test Requirements**:
  - [ ] {Test item}
  - [ ] Red test written before implementation
  - [ ] Feature/API integration coverage written for affected business flow, or waiver documented
  - [ ] Error/permission/boundary/side-effect cases covered where required by the Integration Coverage Contract
  - [ ] Relevant regression surface covered or explicitly waived with reason

## 4. READINESS

### 4.1 Consistency Check
- [ ] Every requirement has at least one task
- [ ] Every task maps to at least one requirement
- [ ] User intent and current-state analysis is documented
- [ ] Requirement questioning was performed, or No Questions Rationale is documented with source evidence
- [ ] Required onboarding docs exist: `project-structure.md`, `business-flows.md`, and `integration-scenarios.md`
- [ ] Residual Risk Preflight is documented, or explicitly unnecessary because no residual-risk category applies beyond normal behavior-change risk
- [ ] Triggered residual-risk warnings have countermeasures, setup tasks, or concrete blockers
- [ ] Runtime Causality Gate is documented, or explicitly not triggered with source-backed reason
- [ ] Triggered runtime-causality checks classify code/environment/data/deploy/provider/inconclusive before behavior-changing implementation tasks
- [ ] Bug Feedback Review is documented for bug/regression work, or explicitly unnecessary because this is not a bug/regression request
- [ ] Flow Knowledge Update is documented for behavior-changing work, including target docs or a concrete feature-local reason
- [ ] Required `docs/agent-flow/business-flows.md` and `docs/agent-flow/integration-scenarios.md` update tasks are included before implementation when reusable flow knowledge is found
- [ ] Flow improvement or bug-knowledge tasks are included when a prior flow gap or non-preventable bug pattern is identified
- [ ] Business ambiguity has been resolved through user answers or explicitly blocked
- [ ] `/flow-plan-review` must be run after freeze and before implementation
- [ ] Design decisions are consistent with requirements
- [ ] Design policy and library-selection decisions are documented, or explicitly unnecessary because existing patterns decide them
- [ ] Task dependencies have no cycles
- [ ] Architecture compliance verified
- [ ] Code style compliance verified
- [ ] Business Flow Matrix covers affected workflows
- [ ] Regression Surface Matrix covers indirect effects
- [ ] Test Design Matrix maps risks to tests before implementation
- [ ] Integration Coverage Contract maps each affected flow to required happy, exception, permission, boundary, side-effect, and regression coverage or explicit waivers
- [ ] Every waiver/blocker has a concrete reason; no vague waiver remains
- [ ] Migration enforcement is documented when schema changes exist
- [ ] Browser verification plan is documented for visible behavior
- [ ] Playwright Integration Test Plan maps visible/multi-step workflows to screenshot evidence

### 4.2 Notes
<!-- Non-blocking and Info items -->
- {Note}
```

---

## User Requirements

$ARGUMENTS

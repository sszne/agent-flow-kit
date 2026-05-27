Specification-Driven Development: Phase 1-3 (SCOPE / SKETCH / READINESS GATE)

User requirements from interactive questioning are combined with codebase analysis to produce a frozen plan document. This prompt guides the creation of a comprehensive implementation plan through structured dialogue.

## Rules

- Never leave ambiguity. Investigate thoroughly before implementation starts.
- Propose minimal necessary implementation based on existing source code.
- Treat `/flow-plan` as the canonical entry point for modifications to existing behavior, bug fixes, regressions, and business-flow-sensitive work.
- Use `/startproject` only when the work is primarily new-feature discovery or greenfield scope shaping. If the request modifies an existing runtime path, continue here.
- Comments inside `<!-- -->` are AI instructions. `{}` denotes replacement text.
- Architecture reference: fetch from (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/architecture.md). If unavailable, skip and note in plan.
- Code style reference: fetch from (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/code-style-review.md). If unavailable, skip and note in plan.
- Plan template: use the template defined in this document (no external template fetch needed).
- Save plan to `docs/flow/{feature_name}/plan.md`.
- The plan is updated incrementally across phases. Do NOT batch work across phases.
- Before writing the implementation design, explicitly analyze the user's request intent against the current codebase state and ask requirement questions when intent, business behavior, actors, data ownership, entrypoints, or success criteria are unclear.
- If requirement questions are needed, stop after presenting the questions. Do not draft or freeze a plan that carries unresolved business ambiguity.
- For behavior-changing work, the plan MUST include Business Flow Matrix, Regression Surface Matrix, and Test Design Matrix before freeze.
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
- Existing related code and patterns
- Current architecture conventions
- Database schema (if applicable)
- API structure (if applicable)
- Business workflows and status transitions
- Related shared partials, scripts, services/actions, jobs, mail, PDFs, and browser entrypoints
- Existing tests that cover the same or adjacent behavior

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

### Step 4: Requirements questioning

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

When questions are needed, present:
- A short "Understanding so far" summary.
- A short "Confirmed from code" list with file/path evidence.
- A short "Assumptions not yet safe" list.
- Up to 5 requirement questions using the Requirements Question Template.

### Step 5: Iterate

If ambiguity remains after user answers, return to Step 3. Repeat until all requirements are clear.

### Step 6: Escalation check

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

### Step 7: Write plan.md "Requirements" section

Create `docs/flow/{feature_name}/plan.md` and write the Requirements section (sections 1.1-1.5 of the plan template).

---

## Phase 2: SKETCH

Goal: Design the implementation approach and decompose into tasks.

### Step 8: Implementation questioning

Use the Implementation Question Template below. Present:
- Entity structure options with Pros/Cons and code examples
- Architecture alternatives with command/query tables
- Technical detail choices in selection format

Only ask questions where multiple valid approaches exist. Skip sections where the answer is obvious from existing code.

If implementation questions are needed, first restate the resolved requirement intent and the minimal codebase-conforming direction, then ask only the implementation questions that cannot be decided from existing patterns.

### Step 9: Iterate

If implementation ambiguity remains, return to Step 8. Repeat until all design decisions are clear.

### Step 10: On-demand artifact check

Generate additional sections based on these conditions:

| Artifact | Condition |
|----------|-----------|
| Architecture overview | Always |
| Schema section | DB changes (table/column/relation additions) |
| API endpoints | API additions or modifications |
| Mermaid diagram | 3+ component data flow OR 4+ step sequence |
| Business Flow Matrix | Always for behavior-changing work |
| Regression Surface Matrix | Always for behavior-changing work |
| Test Design Matrix | Always for TDD tasks and risky DIRECT tasks |
| Playwright Integration Test Plan | Visible browser behavior OR multi-step business workflow |

### Step 11: Task decomposition

Break the implementation into tasks:
- Assign each task a unique ID: TASK-001, TASK-002, etc.
- Classify each task as **TDD** (coding, business logic, tests) or **DIRECT** (setup, config, docs)
- Identify dependencies between tasks
- Order tasks respecting dependencies
- Add a checkbox to each task for progress tracking
- Put Red test tasks before implementation tasks for TDD work
- Include explicit verification tasks for browser, migration, mail/PDF/job, or build checks when applicable

### Step 12: Write plan.md "Design" and "Tasks" sections

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
- Design decisions are consistent with requirements
- Task dependencies form a valid DAG (no cycles)
- Every affected business flow maps to at least one test or documented low-risk/blocker reason
- Every risky regression surface maps to Feature, Unit, Browser, Migration, or manual verification coverage
- Visible browser workflows map to at least one Playwright scenario and major-step screenshots

### Step 16: Issue classification

Classify any found issues:
- **Blocking**: Must be resolved before implementation (inconsistencies, missing requirements)
- **Non-blocking**: Should be noted but won't prevent implementation (minor style issues, optimization opportunities)
- **Info**: Observations for awareness (potential future improvements)

### Step 17: Present blocking issues

If blocking issues exist, present a maximum of 3 to the user for resolution. After resolution, return to Step 15.

### Step 18: Freeze and approve

- Add `<!-- frozen: v1 {YYYY-MM-DD} -->` tag to the top of plan.md
- Write the READINESS section (section 4 of the plan template)
- Present the complete plan to the user for final approval
- If the user requests changes, remove the frozen tag, make changes, and restart from Step 15

---

## Requirements Question Template

<!--
Collect only essential information for plan creation. Ask about behavior, not implementation details.
Maximum 5 questions. Order by recommendation priority (highest first).
Skip questions where the answer is obvious from existing code.
-->

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
Ask about ORM selection, new library installs, etc.
Skip if all required functionality exists in already-installed libraries.
-->

### {Question title}
{e.g., "What persistence mechanism should be used?"}

t-a-1. [{Option}]
t-a-2. [{Option}]

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
| Regression surfaces | What adjacent shared flows can break even if not directly edited? | Shared partials/scripts/services/actions/schema/tests |
| Minimal scope | What is the smallest codebase-conforming change that satisfies the intent? | Existing patterns and alternatives considered |
| Open questions | Which unknowns would cause implementation rework or business-rule guesses? | Questions to user; block freeze until resolved |

---

## plan.md Template

```markdown
# {feature_name} Plan

<!-- frozen: v{N} {YYYY-MM-DD} -->

## 1. Requirements

### 1.1 Overview
{Feature overview and background}

### 1.2 Current State Analysis
{Analysis of existing codebase relevant to this feature}

### 1.3 Intent and Ambiguity Resolution
{Summarize user intent, confirmed source evidence, user answers, remaining assumptions, and why any unanswered items are safe or out of scope. If unresolved ambiguity remains, do not freeze the plan.}

### 1.4 Requirements List
<!-- EARS notation if escalated, otherwise acceptance criteria checklist -->

#### Acceptance Criteria
- [ ] {Criterion}
- [ ] {Criterion}

### 1.5 Scope
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

### 2.6 Business Flow Matrix
<!-- Required for behavior-changing work. This turns domain knowledge into implementation and test obligations. -->

| Flow | Entry point | Existing behavior | New behavior | Regression risk | Test coverage |
| --- | --- | --- | --- | --- | --- |
| {Order/dealer/company/mail/PDF/job/search/status flow} | {route/screen/API/job/mail/PDF} | {current behavior} | {expected behavior} | {what could regress} | {Feature/Unit/Browser/Migration/Manual with reason} |

### 2.7 Regression Surface Matrix
<!-- Inspect indirect effects, not only directly edited files. -->

| Surface | Affected? | Evidence | Required verification |
| --- | --- | --- | --- |
| Routes/controllers | Yes/No | {files/routes inspected} | {Feature test/manual check/N/A} |
| Screens/Blade/JS | Yes/No | {views/scripts inspected} | {Browser check/N/A} |
| API/Ajax flows | Yes/No | {endpoints inspected} | {Feature/browser check/N/A} |
| Shared partials/scripts/services/actions | Yes/No | {shared implementation inspected} | {Regression test/N/A} |
| Schema/migrations | Yes/No | {migrations/deploy path inspected} | {php artisan migrate/enforcement check/N/A} |
| Jobs/schedules | Yes/No | {commands/jobs inspected} | {Feature/command test/N/A} |
| Mail/PDF/export | Yes/No | {templates/services inspected} | {render/assertion/manual check/N/A} |
| Auth/permissions | Yes/No | {middleware/policies inspected} | {Feature/browser check/N/A} |

### 2.8 Test Design Matrix
<!-- Red tests must be listed before implementation starts. -->

| Test ID | Level | Target | Scenario | Expected result | Covers flow/risk |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Feature | {test file} | {scenario} | {expected result} | {flow/risk} |
| TEST-002 | Browser | {screen} | {scenario} | {expected result} | {flow/risk} |

### 2.9 Migration / Runtime Enforcement
<!-- Required when schema or deploy/startup assumptions are involved. -->

- Migration needed: Yes/No
- Migration enforcement path: {entrypoint/deploy/startup path or N/A}
- Runtime validation command: `{command or N/A}`

### 2.10 Playwright Integration Test Plan
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
  - [ ] Relevant regression surface covered or explicitly waived with reason

## 4. READINESS

### 4.1 Consistency Check
- [ ] Every requirement has at least one task
- [ ] Every task maps to at least one requirement
- [ ] User intent and current-state analysis is documented
- [ ] Business ambiguity has been resolved through user answers or explicitly blocked
- [ ] Design decisions are consistent with requirements
- [ ] Task dependencies have no cycles
- [ ] Architecture compliance verified
- [ ] Code style compliance verified
- [ ] Business Flow Matrix covers affected workflows
- [ ] Regression Surface Matrix covers indirect effects
- [ ] Test Design Matrix maps risks to tests before implementation
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

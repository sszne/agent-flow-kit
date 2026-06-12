Specification-Driven Development: Phase 4-6 (IMPLEMENT / INTEGRATION TEST / REVIEW)

Execute the frozen implementation plan task by task, following TDD or DIRECT methodology per task type, then perform a comprehensive review. This prompt guides disciplined implementation that stays faithful to the approved plan.

## Rules

- `$ARGUMENTS` is optional. If empty, resolve the plan from the most recently modified `docs/flow/*/plan.md` and treat its parent directory name as `{feature_name}`.
- If `$ARGUMENTS` is provided, interpret it as either `{feature_name}` or a direct `docs/flow/{feature_name}/plan.md` path.
- Always announce the resolved plan path before implementation starts. If no plan can be resolved, stop and ask the user which plan to implement.
- The plan (`docs/flow/{feature_name}/plan.md`) MUST have a frozen tag (`<!-- frozen: v{N} ... -->`). If not frozen, abort and instruct the user to run `/flow-plan` first.
- The plan MUST include `Plan Review Requirement: Required` or `Optional` with
  a concrete reason. When review is required, `docs/flow/{feature_name}/plan-review.md`
  MUST exist and approve the current frozen plan. If missing, stale,
  `CHANGES_REQUIRED`, `BLOCKED`, or same-agent without a concrete fallback
  reason, abort and instruct the user to run `/flow-plan-review` first.
- Execute tasks one at a time in dependency order. NEVER batch multiple tasks together.
- TDD tasks follow Red-Green-Refactor strictly.
- DIRECT tasks follow Execute-Verify.
- Do NOT make technical choices not covered in the plan without user confirmation.
- Architecture reference: read repo-local `docs/agent-flow/design-principles.md` and configured `design_principles_paths` first. Fetch (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/architecture.md) only as a fallback reference when no repo-local design-principles document exists. On conflict, the repo-local document wins; record the conflict. If neither is available, skip and note.
- Code style reference: fetch from (https://raw.githubusercontent.com/sszne/sample-test/refs/heads/main/docs/code-style-review.md). If unavailable, skip and note.
- Save implementation report to `docs/flow/{feature_name}/implementation_report.md`.
- Update task checkboxes in plan.md as each task completes.
- Update the implementation report after each task -- do NOT defer to the end.
- All tests must pass before reporting completion.
- Before final review, choose the `/flow-integration-test` evidence lane.
  Visible, multi-step, auth/session/permission/tenant, provider/device/deploy,
  external-side-effect, or high-impact workflows require full evidence or
  `BLOCKED`; low-risk non-visible changes may record lightweight evidence.
- Do not start production implementation unless the frozen plan contains Business Flow Matrix, Regression Surface Matrix, and Test Design Matrix for behavior-changing work.
- Do not start production implementation unless the frozen plan contains an Integration Coverage Contract for behavior-changing work.
- Do not start behavior-changing implementation unless `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md` exist.
- Do not accept vague waivers. Waivers must state a concrete reason or blocker.
- For bug/regression work, do not start production implementation until the plan's Bug Feedback Review has classified any previous-flow failure and listed required flow-improvement or bug-knowledge tasks.
- Red tests must be written and confirmed failing before Green implementation for TDD tasks.

## Prerequisites

- `/flow-plan` has been completed and plan.md is frozen.
- `/flow-plan-review` has approved the current frozen plan when the plan marks
  review required or configured high-impact paths are changed.
- Either `$ARGUMENTS` identifies the plan, or at least one `docs/flow/*/plan.md` exists so the latest plan can be resolved.

## Directory Structure

- docs/flow/{feature_name}/
    - plan.md (created in /flow-plan, updated here with checkboxes)
    - implementation_report.md (created in this phase)

---

## Phase 4: IMPLEMENT

### Step 0: Resolve target plan

Resolve the implementation target before reading the plan:

1. If `$ARGUMENTS` is empty:
   - Find all `docs/flow/*/plan.md` files.
   - Select the most recently modified plan file.
   - Set `{feature_name}` to the selected plan's parent directory name.
   - Announce: `Resolved /flow-impl target: docs/flow/{feature_name}/plan.md`.
2. If `$ARGUMENTS` points to a plan file path such as `docs/flow/foo/plan.md`:
   - Use that file directly.
   - Set `{feature_name}` to the parent directory name.
3. Otherwise:
   - Treat `$ARGUMENTS` as `{feature_name}`.
   - Use `docs/flow/{feature_name}/plan.md`.

Stop and ask the user when:

- no `docs/flow/*/plan.md` exists,
- the resolved plan path does not exist,
- multiple candidate plans have the same latest modified timestamp and the intended target is ambiguous.

Do not ask for `{feature_name}` merely because `$ARGUMENTS` is empty when a latest plan can be resolved.

### Step 1: Load plan and verify frozen status

Read `docs/flow/{feature_name}/plan.md`. Verify the `<!-- frozen: ... -->` tag exists. If missing, stop and inform the user.

Read the plan's `Plan Review Requirement`. If it is `Required`, read
`docs/flow/{feature_name}/plan-review.md` and verify:

- it references the same `docs/flow/{feature_name}/plan.md`;
- `Reviewed frozen marker` matches the current frozen marker from plan.md;
- `Review status` is `APPROVED`;
- `Plan author` is `codex`, `claude-code`, or `unknown`;
- `Reviewer agent` is `codex` or `claude-code`;
- reviewer and author are different unless `Same-agent fallback` contains a
  concrete reason or blocker.

If review is required and any check fails, stop before coding and run
`/flow-plan-review`. If review is optional, record that the plan gives a
concrete optional-review reason and continue.

Verify the plan includes the required quality gates:

- Business Flow Matrix for behavior-changing work
- Regression Surface Matrix for indirect effects
- Test Design Matrix for TDD/risky tasks
- Integration Coverage Contract for behavior-changing work
- Plan Review Requirement decision
- Approved, current `plan-review.md` when review is required
- Agent-flow onboarding docs for behavior-changing work
- Bug Feedback Review for bug/regression work
- Migration/runtime enforcement notes when schema changes exist
- Evidence lane decision for `flow-integration-test`; full Playwright
  Integration Test Plan when visible, multi-step,
  auth/session/permission/tenant, provider/device/deploy, external-side-effect,
  or high-impact workflows exist

If any required section is missing, stop and update the plan before coding.

### Step 2: Load architecture and code style documents

Read the repo-local design-principles document first
(`docs/agent-flow/design-principles.md` and configured
`design_principles_paths`). Fetch the external architecture and code style
documents from the URLs above only as fallback. If nothing is available, note
the gap and continue with local conventions.

### Step 3: Initialize implementation report

Create `docs/flow/{feature_name}/implementation_report.md` using the Implementation Report Template below with initial (empty) state.

### Step 4: Execute tasks sequentially

For each task in the plan (respecting dependency order):

#### 4a. For TDD tasks:

**Red:**
- Write failing tests that define the expected behavior
- Run tests to confirm they fail
- Prefer Feature/API integration tests for routes, API handlers, auth, DB persistence, mail/PDF/export, job, queue, notification, and shared workflow entrypoints
- Add Unit tests for isolated helper/action/hook logic where an integration test would hide the failure cause
- Cover the case types required by the Integration Coverage Contract: happy, validation, permission, missing relation, boundary, side effect, regression, migration, or browser evidence
- If a required case type cannot be tested before implementation, document the blocker before writing production code

**Green:**
- Write the minimum implementation to make tests pass
- Run tests to confirm they pass

**Refactor:**
- Improve code quality while keeping tests green
- Apply code style conventions
- Apply architecture patterns

#### 4b. For DIRECT tasks:

**Execute:**
- Perform the setup, configuration, or documentation work as specified

**Verify:**
- Confirm the work is complete and functional

#### 4c. After each task (both TDD and DIRECT):

1. **Code style check**: Verify implementation follows the code style document
2. **Architecture check**: Verify implementation follows the design-principles
   document (or fallback architecture document), including the anti-pattern
   rules: no vague-responsibility splits, no new Service/Manager class without
   the plan's Service Introduction Rule evidence, and no aggregate-internal
   constraint implemented outside the aggregate
3. **Update plan.md**: Change `- [ ] **Completed**` to `- [x] **Completed**` for the task
4. **Update implementation report**: Add task completion details
5. **Regression surface check**: Confirm the related Business Flow Matrix, Test Design Matrix, and Integration Coverage Contract rows are covered
   - Reject vague waivers such as `manual`, `low risk`, `TBD`, `later`, or blank waiver cells
   - For bug/regression work, confirm Bug Feedback Review tasks are completed before reporting the fix complete
6. **Progress report**: Inform the user which task was completed and what comes next
7. If any unplanned technical decision is needed, ask the user before proceeding

---

## Phase 5: INTEGRATION TEST

### Step 5: Run integration evidence gates

Run the server-side Feature/API integration tests required by the Integration Coverage Contract. Then choose the `/flow-integration-test` evidence lane. For visible behavior, forms, modals, tables, filters, auth redirects, displayed values, multi-step business workflows, auth/session/permission/tenant, provider/device/deploy, external-side-effect, or high-impact workflows, run the full lane or record `BLOCKED`. For low-risk non-visible changes, record lightweight substitute evidence and the covered regression surface.

Full-lane required evidence:

- Feature/API integration command output
- `docs/flow/{feature_name}/integration-test/{run_id}/index.html`
- major-step screenshots under `screenshots/`
- `test-review.md`
- `business-flow-impact.md`

Do not continue to final review if the integration-test gate is `FAIL` or `BLOCKED`.

If lightweight evidence is used, document the concrete low-risk reason, substitute commands/reviews, covered regression surface, and effectiveness metrics in `implementation_report.md`.

## Phase 6: REVIEW

### Step 6: Verify all tasks complete

Confirm every task in plan.md has `- [x] **Completed**` checked.

### Step 7: Code style review

Re-read the code style document. Verify all implemented code complies. Fix any violations.

### Step 8: Architecture review

Re-read the repo-local design-principles document (or the fallback
architecture document). Verify all implemented code complies, including the
anti-pattern rules: design splits must name owned data and invariants; new
Service/Manager/coordinator classes must match the plan's Service Introduction
Rule evidence; constraints protecting an aggregate's invariant must live
inside the aggregate. Fix any violations, or ask the user when a fix would
leave the frozen plan.

### Step 9: Run all tests

Execute the full test suite. All tests must pass. If any fail, fix them before proceeding.

Use the project-specific commands from `.claude/rules/dev-environment.md`. Common examples:

```bash
pnpm test
pnpm test:integration
pnpm build
```

Broaden based on impact:

```bash
pnpm test -- --runInBand
pnpm exec playwright test
npm run build
```

For Laravel/PHP projects, use the equivalent focused and broad commands such as `./vendor/bin/phpunit`, `./vendor/bin/pint --dirty`, and migration validation. For visible, multi-step, auth/session/permission/tenant, provider/device/deploy, external-side-effect, or high-impact workflows, run the full `/flow-integration-test` lane against the configured local base URL. If blocked, record the blocker category, exact unverified surface, and minimum unblock action; do not report browser verification as passed. For low-risk non-visible changes, record lightweight substitute evidence and the covered regression surface.

### Step 10: Readiness checklist verification

Re-verify all items in plan.md section "4. READINESS" checklist are satisfied.

### Step 11: Finalize implementation report

Complete the implementation report with:
- All task details
- Quality check results
- Integration-test evidence lane, path when full, gate status, and metrics
- Remaining tasks (if any)
- Observations and next actions

### Step 12: Final report

Present the completed implementation report to the user with:
- Summary of what was implemented
- Test results
- Integration-test evidence index path
- Any remaining items or recommendations

---

## TDD Cycle Details

### Red

- Write tests that define the behavior specified in the task
- Tests should cover: happy path, validation errors, permission/ownership failures, missing relations, boundary values, side effects, and regression surfaces required by the Integration Coverage Contract
- Run tests and confirm they FAIL (this validates the test is meaningful)

### Green

- Write the minimum code to make failing tests pass
- Prioritize passing tests over code quality at this stage
- Run tests and confirm they PASS

### Refactor

- Improve code while keeping all tests green
- Apply naming conventions from code style document
- Apply structural patterns from architecture document
- Remove duplication, improve readability
- Run tests again to confirm they still PASS

---

## Implementation Report Template

```markdown
# {feature_name} Implementation Report

## Overview

- **Plan version**: {frozen version from plan.md}
- **Start date**: {YYYY-MM-DD}
- **Completion date**: {YYYY-MM-DD or "In progress"}
- **Total tasks**: {N}
- **Completed tasks**: {N}

## Task Implementation Details

### TASK-001: {Task title}
- **Type**: TDD / DIRECT
- **Status**: Completed / In Progress / Blocked
- **Implementation summary**:
  - {What was done}
- **Files changed**:
  - {file path}: {description of change}
- **Test results**:
  - {Test outcome}
- **Notes**:
  - {Any observations, issues encountered, decisions made}

## Quality Check

### Code Style
- [ ] All implementations follow code style document

### Architecture
- [ ] All implementations follow the design-principles document (or fallback architecture document)
- [ ] No design split is justified only by vague "responsibility" wording without named data/invariant ownership
- [ ] No new Service/Manager/coordinator class holds logic its data owner could hold, unless the plan records Service Introduction Rule evidence
- [ ] Constraints protecting an aggregate's invariant are enforced inside the aggregate

### Tests
- [ ] All unit tests pass
- [ ] All integration tests pass (if applicable)
- [ ] Test coverage meets target
- [ ] Business Flow Matrix coverage is satisfied
- [ ] Regression Surface Matrix coverage is satisfied
- [ ] Integration Coverage Contract is satisfied, or uncovered rows have explicit waivers/blockers
- [ ] Integration-test evidence lane completed or blocker documented
- [ ] Full lane: `index.html`, screenshots, test review, and business-flow impact review are linked when applicable
- [ ] Lightweight lane: substitute evidence, low-risk reason, covered regression surface, and metrics are recorded when applicable
- [ ] Migration/runtime enforcement verified when applicable

## Remaining Tasks

- {Any tasks not completed, with reason}

## Observations and Next Actions

- {Lessons learned, recommendations, follow-up items}
```

---

## User Requirements

$ARGUMENTS

---
name: team-implement
description: |
  Parallel implementation using Agent Teams. Spawns teammates per module/layer,
  each owning separate files to avoid conflicts. Uses shared task list with
  dependencies for autonomous coordination. Run after /flow-start or /flow-plan
  approval, plus flow-plan-review approval when review is required.
metadata:
  short-description: Parallel implementation with Agent Teams
---

# Team Implement

**Parallel implementation using Agent Teams. Executes based on the plan approved in `/flow-start` or `/flow-plan`.**

## Prerequisites

- `/flow-start` or `/flow-plan` is complete and the plan has been approved by the user
- The plan records whether `/flow-plan-review` is required or optional
- `/flow-plan-review` has approved the current frozen plan when review is required
- Architecture is documented in `.claude/docs/DESIGN.md`
- Task list has been created

## Workflow

```
Step 1: Analyze Plan & Design Team
  Analyze task dependencies from the plan and determine team composition
    ↓
Step 2: Test Design Gate
  Freeze business-flow coverage and Red tests before implementation
    ↓
Step 3: Spawn Agent Team
  Launch Teammates per module/layer with file ownership
    ↓
Step 4: Monitor & Coordinate
  Lead monitors, integrates, and manages quality
    ↓
Step 5: Integration & Verification
  After all tasks complete, run integration tests
```

---

## Step 1: Analyze Plan & Design Team

**Identify parallelizable workstreams from the task list.**

### Team Design Principles

1. **File ownership separation**: Each Teammate owns a different set of files
2. **Respect dependencies**: Dependent tasks go to the same Teammate or execute in dependency order
3. **Appropriate granularity**: Target 5-6 tasks per Teammate

### Common Team Patterns

**Pattern A: Module-Based (Recommended)**
```
Teammate 1: Module A (models, core logic)
Teammate 2: Module B (API, endpoints)
Teammate 3: Tests (unit + integration)
```

**Pattern B: Layer-Based**
```
Teammate 1: Data layer (models, DB)
Teammate 2: Business logic (services)
Teammate 3: Interface layer (API/CLI)
```

**Pattern C: Feature-Based**
```
Teammate 1: Feature X (all layers)
Teammate 2: Feature Y (all layers)
Teammate 3: Shared infrastructure
```

### Anti-patterns

- Two Teammates editing the same file → overwrite risk
- Too many tasks per Teammate → risk of prolonged idle time
- Overly complex dependencies → coordination costs outweigh benefits
- Implementers writing production code before the business-flow test matrix is complete
- Tester working only after implementation instead of defining Red tests first

---

## Step 2: Test Design Gate

**Before implementation starts, convert business knowledge into test obligations.**

The Lead must update the plan or implementation report with:

1. Business Flow Matrix
2. Regression Surface Matrix
3. Test Design Matrix
4. Integration Coverage Contract
5. Red test list
6. Browser/migration verification plan

Before behavior-changing implementation starts, verify these onboarding documents exist:

- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

Required matrix:

```markdown
| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {flow} | {role/scope} | {route/screen/API/job/mail/pdf} | {happy workflow} | {validation/missing/external failure} | {forbidden/cross-tenant/null/min/max} | {mail/PDF/export/job/cache/search} | {risk} | {Feature/API integration, Unit, Browser, Migration} |
```

Do not spawn production-code implementers until this gate is complete. If a task is truly low-risk, record why each uncovered integration/browser case is not required. Vague waivers such as `manual`, `low risk`, `TBD`, `later`, or blank waiver cells are invalid.

---

## Step 3: Spawn Agent Team

**Launch the team based on the plan.**

```
Create an agent team for implementing: {feature}

Each teammate receives:
- Project Brief from CLAUDE.md
- Architecture from .claude/docs/DESIGN.md
- Library constraints from .claude/docs/libraries/
- Their specific task assignments

Spawn teammates:

1. **Implementer-{module}** for each module/workstream
   Prompt: "You are implementing {module} for project: {feature}.

   Read these files for context:
   - CLAUDE.md (project context)
   - .claude/docs/DESIGN.md (architecture)
   - .claude/docs/libraries/ (library constraints)

   Your assigned tasks:
   {task list for this teammate}

   Your file ownership:
   {list of files this teammate owns}

   Rules:
   - ONLY edit files in your ownership set
   - Follow existing codebase patterns
   - Write type hints on all functions
   - Use the project-specific verification commands documented in `.claude/rules/dev-environment.md`
   - Do not implement outside the frozen plan or test matrix
   - Communicate with other teammates if you need interface changes

   When done with each task, mark it completed in the task list.

   IMPORTANT — Work Log:
   When ALL your assigned tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/{your-teammate-name}.md

   Use this format:
   # Work Log: {your-teammate-name}
   ## Summary
   (1-2 sentence summary of what you accomplished)
   ## Tasks Completed
   - [x] {task}: {brief description of what was done}
   ## Files Modified
   - `{file path}`: {what was changed and why}
   ## Key Decisions
   - {decision made during implementation and rationale}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

2. **Tester** (required for behavior-changing work)
   Prompt: "You are the Tester for project: {feature}.

   Read:
   - CLAUDE.md, .claude/docs/DESIGN.md
   - .claude/rules/testing.md
   - Existing test patterns in tests/
   - The Business Flow Matrix and Regression Surface Matrix
   - The Test Design Matrix and Integration Coverage Contract

   Your tasks:
   - Write or update Red tests before production implementation starts
   - Cover affected routes/API handlers/shared behavior with Feature/API integration tests
   - Cover validation, permission/ownership, missing relation, boundary, side-effect, and regression cases required by the Integration Coverage Contract
   - Identify unit-only cases separately
   - Identify the integration-test evidence lane: full for visible,
     multi-step, auth/session/permission/tenant, provider/device/deploy,
     external-side-effect, or high-impact behavior; lightweight only for
     low-risk non-visible work; blocked when a required full lane cannot run
   - Run targeted project-specific test commands after each test file
   - Report failing tests to the relevant implementer

   Common command examples:
   - pnpm test
   - pnpm test:integration
   - pnpm exec playwright test

   IMPORTANT — Work Log:
   When ALL your assigned tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/{your-teammate-name}.md

   Use this format:
   # Work Log: {your-teammate-name}
   ## Summary
   (1-2 sentence summary of what you accomplished)
   ## Tasks Completed
   - [x] {task}: {brief description of what was done}
   ## Files Modified
   - `{file path}`: {what was changed and why}
   ## Key Decisions
   - {decision made during implementation and rationale}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

Use delegate mode (Shift+Tab) to prevent Lead from implementing directly.
Wait for all teammates to complete their tasks.
```

---

## Step 4: Monitor & Coordinate

**Lead focuses on monitoring and integration, not implementing.**

### Monitoring Checklist

- [ ] Check task list progress (Ctrl+T)
- [ ] Review each Teammate's output (Shift+Up/Down)
- [ ] Verify no file conflicts
- [ ] Check if any Teammate is stuck

### Intervention Triggers

| Situation | Response |
|-----------|----------|
| Teammate not making progress for a long time | Send a message to check, re-instruct if needed |
| File conflict detected | Reassign file ownership |
| Tests keep failing | Send message to the relevant Implementer |
| Unexpected technical issue | Consult Codex (via subagent) |

### Quality Gates (via Hooks)

`TeammateIdle` hook and `TaskCompleted` hook automatically run quality checks:

- Business-flow matrix coverage
- Integration Coverage Contract coverage
- Focused tests
- Migration enforcement check when schema changes
- Integration-test evidence lane requirements: full / lightweight / blocked
- Formatting/linting before completion

---

## Step 5: Integration & Verification

**After all tasks are complete, run integration verification.**

```bash
# Run project-specific focused checks from .claude/rules/dev-environment.md
pnpm lint
pnpm test

# Broaden when impact warrants it
pnpm test:integration
pnpm exec playwright test
npm run build
```

For Laravel/PHP projects, use the equivalent PHPUnit/Pint/migration commands documented by the target repository.

### Integration Report

```markdown
## Implementation Complete: {feature}

### Completed Tasks
- [x] {task 1}
- [x] {task 2}
...

### Quality Checks
- Business Flow Matrix: PASS / FAIL
- Regression Surface Matrix: PASS / FAIL
- Integration Coverage Contract: PASS / FAIL
- Focused tests: PASS / FAIL
- Lint/format: PASS / FAIL
- Integration-test evidence lane: full / lightweight / blocked / N/A
- Migration enforcement: PASS / BLOCKED / N/A

### Next Steps
Run `/team-review` for parallel review
```

### Cleanup

```
Clean up the team
```

---

## Tips

- **Delegate mode**: Use Shift+Tab to prevent Lead from implementing directly
- **Task granularity**: 5-6 tasks per Teammate is optimal
- **File conflict prevention**: Module-level ownership separation is the most important factor
- **Separate Tester**: Having a dedicated Tester separate from Implementers enables a TDD-like workflow
- **Cost awareness**: Each Teammate is an independent Claude instance (high token consumption)

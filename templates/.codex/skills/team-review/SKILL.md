---
name: team-review
description: |
  Review an implemented feature in Codex by coordinating reviewer workers.
  Use after implementation when you need structured findings across security,
  code quality, and test coverage based on the actual changed files or diff scope.
---

# Team Review

Codex-native review skill for collecting review scope, inspecting code locally, and reporting prioritized findings.

## Purpose

Use this skill when the user wants to:

- Review a completed implementation before merge or release
- Get structured findings across security, quality, and test coverage
- Review a feature described by a diff, a changed-file set, or a `docs/flow/{feature_name}` artifact

For behavior-changing work, this skill is the required review gate. A normal `/review`-style single-pass review is acceptable as a quick supplemental check for docs/config-only work, but it is not enough when the change can affect routes, screens, APIs, shared logic, schema/migrations, jobs, mail, PDF/export, auth, search, pricing, totals, or status transitions.

This skill is findings-first and manager-led. The main Codex agent owns scope selection and final synthesis; reviewer workers inspect bounded perspectives in parallel.

## Operating Rules

- Activate `context-loader` first.
- Gather the actual review scope before judging anything.
- Prefer reviewing changed files and their immediate dependencies, not the whole repository.
- Compare the implementation against the frozen plan's Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, and Integration Coverage Contract.
- Treat missing matrix coverage as a review finding unless the implementation is explicitly documented as low-risk docs/config-only work.
- Report findings first, ordered by severity, with file references.
- If there are no findings, say so explicitly and note any remaining risk or validation gaps.
- Use reviewer workers by default for distinct perspectives, but keep final synthesis in the manager.

## Workflow

```text
Phase 1: SCOPE
  manager identifies diff and affected files
    ->
Phase 2: REVIEW
  reviewer workers inspect security + quality + tests
    ->
Phase 3: REPORT
  manager synthesizes findings and residual risks
```

## Phase 1: Scope

### Step 1: Identify the review target

Determine the narrowest valid scope using the best available signal:

- `git diff` against the relevant base branch or commit
- User-specified changed files
- Files referenced by `docs/flow/{feature_name}/plan.md` or `implementation_report.md`

Also inspect nearby dependencies when needed to confirm behavior.

### Step 2: Capture review context

Before reviewing, gather:

- Changed files
- Relevant tests
- Any referenced plan or implementation report
- Any known constraints from `.claude/docs/DESIGN.md` and `.claude/rules/`
- Matrix and Integration Coverage Contract coverage from the frozen plan, including migration/runtime enforcement when schema changes exist

The manager owns the final review scope and passes bounded slices to reviewer workers.

## Phase 2: Review

### Step 3: Launch reviewer workers by perspective

Use reviewer workers by default:

1. `Security Reviewer`
   - auth, validation, data exposure, destructive paths, secrets

2. `Quality Reviewer`
   - logic errors, regressions, maintainability, convention drift

3. `Test Reviewer`
   - missing coverage, weak assertions, missing failure-path verification
   - matrix coverage, Integration Coverage Contract evidence, adjacent business-flow regressions, migration/runtime enforcement
   - vague waiver detection for uncovered integration, browser, migration, side-effect, permission, boundary, or regression cases
   - Bug Feedback Review coverage for bug/regression work, including flow-improvement or bug-knowledge updates

Use the repository's existing conventions as the baseline. Do not invent a different architecture during review.

### Step 4: Classify findings

Use these priorities:

- `Critical`: security flaw, data loss, or severe correctness issue
- `High`: user-visible bug, authorization problem, broken workflow, missing critical test
- `Medium`: maintainability issue with meaningful risk
- `Low`: minor cleanup or consistency issue

If a concern is only speculative, label it clearly as a risk or open question, not a confirmed bug.

## Phase 3: Report

### Step 5: Produce a findings-first review

Default output shape:

```markdown
## Findings
1. [High] ...
2. [Medium] ...

## Open Questions
- ...

## Change Summary
- ...
```

For each finding include:

- Severity
- File and line
- Why it matters
- What change would address it

### Step 6: Handle no-finding cases correctly

If no findings are discovered:

- State that explicitly
- Mention remaining risks, if any
- Call out unverified areas, such as tests you could not run

### Step 7: Manager-reviewer rules

- The manager owns the final report and prioritization
- Reviewers should return findings, not rewrite the same narrative
- Avoid duplicate review of the same file set unless perspectives differ materially
- If a reviewer is uncertain, surface it as a risk or open question instead of inflating severity

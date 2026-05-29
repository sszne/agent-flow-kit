---
name: flow-plan-review
description: |
  Review a frozen Agent Flow plan in Codex. Use after flow-plan and before
  flow-impl/team-implement to create docs/flow/{feature_name}/plan-review.md.
---

# Flow Plan Review

Codex-native equivalent of Claude Code `/flow-plan-review`.

## Purpose

Review the current frozen `docs/flow/{feature_name}/plan.md` before
implementation starts. The review is an implementation-readiness gate, not a
code review.

## Operating Rules

- Activate `context-loader` first.
- If no target is provided, resolve the most recently modified
  `docs/flow/*/plan.md` and announce the resolved path.
- Require a frozen marker such as `<!-- frozen: v... -->`.
- Read the plan, local Agent Flow docs, relevant code/schema/tests, and any
  prior implementation or integration evidence that could affect risk.
- Save the review to `docs/flow/{feature_name}/plan-review.md`.
- Cross-agent review is required by default:
  - review `claude-code` authored plans with `codex`;
  - Codex-authored plans should normally be reviewed by Claude Code instead;
  - if Codex must review a Codex-authored or unknown-author plan, record a
    concrete `Same-agent fallback` reason.
- Do not approve if the plan has unresolved business ambiguity, missing
  coverage, stale flow knowledge, vague waivers, or an unhandled high-risk
  DB/auth/performance/dependency issue.

## Required Review Focus

- Missed risks, especially combined conditions.
- DB/schema/migration order, missing related data, backfill, rollback, future
  extensibility, join-table/index needs, and runtime enforcement.
- Auth, permission, tenant, ownership, and session scope.
- Performance, query count, cache/search/indexing, queue, schedule, and load.
- Dependency, external-service, mail/PDF/storage/provider, runtime, and deploy
  assumptions.
- Test design and integration coverage against the Business Flow Matrix,
  Regression Surface Matrix, Test Design Matrix, and Integration Coverage
  Contract.
- Concurrency, idempotency, rollback/deploy sequencing, observability, privacy,
  staged rollout, stale `docs/agent-flow/*` knowledge, and waiver quality.

## Required Output

Write `docs/flow/{feature_name}/plan-review.md` with this exact metadata block
near the top:

```markdown
# {feature_name} Plan Review

- Reviewed plan: `docs/flow/{feature_name}/plan.md`
- Reviewed frozen marker: `<!-- frozen: v{N} {YYYY-MM-DD} -->`
- Plan author: `codex` / `claude-code` / `unknown`
- Reviewer agent: `codex`
- Review status: `APPROVED` / `CHANGES_REQUIRED` / `BLOCKED`
- Same-agent fallback: `N/A` or `reason ...` / `blocked by ...`
```

Then include:

```markdown
## Summary
## Missed Risk Review
## DB / Schema / Migration Review
## Auth / Permission / Tenant Review
## Performance / Query / Load Review
## Dependency / Runtime / External-Service Review
## Test And Integration Coverage Review
## Extra Review Items
## Findings
## Implementation Readiness Decision
```

Use `APPROVED` only when implementation may start without plan changes. Use
`CHANGES_REQUIRED` when the plan must be updated and re-frozen. Use `BLOCKED`
when required evidence, domain answers, environment, or cross-agent review
cannot be obtained.

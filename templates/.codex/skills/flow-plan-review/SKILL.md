---
name: flow-plan-review
description: |
  Review a frozen Agent Flow plan in Codex. Use after flow-plan when review is
  required for high-impact work or requested as an optional readiness pass.
---

# Flow Plan Review

Codex-native equivalent of Claude Code `/flow-plan-review`.

## Purpose

Review the current frozen `docs/flow/{feature_name}/plan.md` before
implementation starts when review is required for large-scale/high-impact work,
or whenever the user or agent requests an optional readiness pass. The review is
an implementation-readiness gate, not a code review.

## Operating Rules

- Activate `context-loader` first.
- If no target is provided, resolve the most recently modified
  `docs/flow/*/plan.md` and announce the resolved path.
- Require a frozen marker such as `<!-- frozen: v... -->`.
- Read the plan, local Agent Flow docs, relevant code/schema/tests, and any
  prior implementation or integration evidence that could affect risk.
- Save the review to `docs/flow/{feature_name}/plan-review.md`.
- Require this gate for large-scale or high-impact work: multi-flow or
  cross-module changes; auth, permission, tenant, ownership, session, security,
  or privacy changes; schema, migration, data compatibility, backfill,
  rollback, or destructive data changes; deploy, CI, install, hooks, workflow
  gates, risky-path config, or Agent Flow contract changes; external providers,
  webhooks, mail/PDF, storage, search/cache, queues, jobs, schedules, or other
  side effects; public API contracts or shared runtime entrypoints; and any
  change the user or plan author marks as uncertain or high impact.
- Treat review as optional for clearly non-high-impact work, including small
  localized behavior changes and non-behavioral typo, formatting-only, or
  docs-only changes.
- If a docs-only change updates Agent Flow rules, skill behavior, gates, review
  policy, risky-path config, or required evidence, treat it as high-impact
  workflow work and run the review.
- Cross-agent review is required by default when review runs:
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

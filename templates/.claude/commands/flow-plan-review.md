Plan Review Gate: cross-agent review for a frozen Agent Flow plan when review
is required for high-impact work or requested as an optional readiness pass.

## Rules

- Run this after `/flow-plan` freezes `docs/flow/{feature_name}/plan.md` and
  before `/flow-impl` or `team-implement` starts when the plan marks review as
  required or configured high-impact paths are changed.
- This command may also be run for smaller changes when the user or agent wants
  an optional readiness pass.
- `$ARGUMENTS` is optional. If empty, resolve the most recently modified
  `docs/flow/*/plan.md`.
- Review evidence MUST be saved to `docs/flow/{feature_name}/plan-review.md`.
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
  - plans authored by `codex` must be reviewed by `claude-code`;
  - plans authored by `claude-code` must be reviewed by `codex`;
  - plans authored by `unknown` should be reviewed by the active non-author
    agent when known, or record why cross-agent identity cannot be proven.
- A same-agent review is valid only when `Same-agent fallback: reason ...` or
  `Same-agent fallback: blocked by ...` is recorded with a concrete reason.
- Do not approve a stale review. The review must quote the current frozen marker
  from the plan and must be updated whenever the plan is re-frozen.
- Use the corrected command name `flow-plan-review`; do not create or promote a
  `flow-plan-reveiw` alias.

## Required Review Focus

Review the plan against the real repository state, onboarding docs, current
schema, affected routes/screens/jobs/services, and tests. Look especially for:

- risks missed by `flow-plan`, including problems that only happen when
  conditions combine;
- DB/schema/migration risks: missing related data, migration order, backfill,
  rollback, future extensibility, join-table needs, indexes, and deploy/runtime
  enforcement;
- auth, permission, tenant, ownership, and session risks;
- performance, query count, indexing, cache, queue, and load risks;
- dependency, external service, runtime environment, mail/PDF/storage/search,
  schedule, or provider gaps;
- test and integration coverage gaps;
- concurrency, idempotency, and race conditions;
- observability, logs, auditability, and production diagnosis;
- data privacy and sensitive-data exposure;
- feature flag, rollout, or staged-release needs;
- stale `docs/agent-flow/*` knowledge;
- vague waivers or weak manual verification claims.

## Output Contract

Write `docs/flow/{feature_name}/plan-review.md` with this exact metadata block
near the top:

```markdown
# {feature_name} Plan Review

- Reviewed plan: `docs/flow/{feature_name}/plan.md`
- Reviewed frozen marker: `<!-- frozen: v{N} {YYYY-MM-DD} -->`
- Plan author: `codex` / `claude-code` / `unknown`
- Reviewer agent: `claude-code` / `codex`
- Review status: `APPROVED` / `CHANGES_REQUIRED` / `BLOCKED`
- Same-agent fallback: `N/A` or `reason ...` / `blocked by ...`
```

Then include these sections:

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

Use `Review status: APPROVED` only when implementation may start without plan
changes. Use `CHANGES_REQUIRED` when the plan must be updated and re-frozen.
Use `BLOCKED` when required evidence, domain answers, environment, or cross-agent
review cannot be obtained.

## User Requirements

$ARGUMENTS

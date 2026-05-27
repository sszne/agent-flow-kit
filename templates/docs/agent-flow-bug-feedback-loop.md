# Agent Flow Bug Feedback Loop

## Purpose

Bug reports should improve the project-specific workflow over time.

When a bug or regression is reported, `/flow-plan` should not only plan the fix.
It should also inspect whether a previous plan existed and decide whether the
bug was caused by a gap in the flow, implementation drift, weak evidence, or a
project-specific condition that cannot be fully prevented by generic rules.

## When This Applies

Run the Bug Feedback Review when the user request is any of these:

- bug report,
- regression,
- QA finding,
- production incident,
- support report,
- "this was fixed before but broke again",
- "after the previous implementation, this related flow is broken".

## Required Inputs

Search for:

- `docs/flow/*/plan.md`
- `docs/flow/*/implementation_report.md`
- `docs/flow/*/integration-test/*/test-review.md`
- `docs/flow/*/integration-test/*/business-flow-impact.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/bug-knowledge.md`

## Failure Classification

| Failure ID | Flow failure point | Typical signal | Required response |
| --- | --- | --- | --- |
| BF-001 | Requirement/questioning gap | Actor, permission, lifecycle, ownership, side effect, or success criteria was never asked | Add a question pattern and update business-flow docs |
| BF-002 | Business Flow Matrix gap | Affected workflow, exception path, or side effect was absent | Add matrix row or missing path |
| BF-003 | Regression Surface Matrix gap | Shared service, API, job, mail/PDF, schema, cache/search, or UI surface was missed | Add regression surface and verification |
| BF-004 | Test Design Matrix gap | Required case type was missing | Add Red test and integration scenario |
| BF-005 | Integration Coverage Contract gap | Required coverage was waived, vague, or mapped to weak evidence | Tighten contract and waiver rule |
| BF-006 | Residual Risk Preflight miss | Runtime/external/test-infra/reviewer risk was not warned | Add project-specific residual-risk trigger |
| BF-007 | Implementation drift | Code changed behavior outside the frozen plan | Add implementation guard and review focus |
| BF-008 | Evidence/review gap | Screenshot, HTML, test review, business-flow impact review, or team-review missed it | Add evidence/review checklist item |
| BF-009 | Not preventable by flow | Production-only data, provider outage, legacy hidden behavior, rare timing/concurrency | Append bug knowledge with future detection/response |

## Flow Improvement Rule

If the bug could have been prevented by better flow knowledge, update at least
one of these before or alongside the bug fix:

- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/bug-knowledge.md`
- `.claude/rules/testing.md`
- `.claude/docs/DESIGN.md`
- `.agent-flow/config.json`
- the current `docs/flow/{feature}/plan.md`

Examples:

- A permission regression was missed:
  - Add cross-scope permission path to `business-flows.md`.
  - Add Feature/API integration scenario to `integration-scenarios.md`.
  - Add required case type to the current `Integration Coverage Contract`.

- A webhook duplicate-delivery bug was missed:
  - Add duplicate webhook delivery to `bug-knowledge.md`.
  - Add idempotency test requirement to `integration-scenarios.md`.
  - Add sandbox/webhook fixture requirement to the current plan.

- A cache/search stale-data bug was missed:
  - Add cache/search to regression surfaces.
  - Add index refresh/rebuild verification.
  - Add Playwright or API assertion proving the updated value is visible.

## Non-Preventable Bug Rule

If the bug cannot reasonably be prevented by flow changes, append a
`docs/agent-flow/bug-knowledge.md` entry.

Examples:

- external provider outage with no sandbox reproduction,
- rare production data shape not present in any environment,
- legacy manual operation unknown to current stakeholders,
- intermittent timing issue that requires long-running monitoring.

The entry must include:

- trigger,
- symptoms,
- root cause,
- why the prior flow could not catch it,
- future detection or response,
- whether a regression test, monitor, runbook, or alert is needed.

## Plan Requirements

For bug/regression work, `docs/flow/{feature}/plan.md` should include:

- previous plan found or not found,
- previous implementation/evidence found or not found,
- failure classification,
- whether flow improvement is possible,
- flow improvement tasks,
- bug-knowledge update task when needed,
- regression tests that prove the bug cannot recur.

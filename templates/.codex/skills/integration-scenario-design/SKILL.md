---
name: integration-scenario-design
description: |
  Design integration-test scenarios from business-flow documentation. Use during
  agent-flow onboarding to create Playwright/Feature/API scenario matrices and
  screenshot evidence requirements before implementation work begins.
---

# Integration Scenario Design

Create `docs/agent-flow/integration-scenarios.md`.

## Prerequisites

- `docs/agent-flow/project-structure.md` exists.
- `docs/agent-flow/business-flows.md` exists.
- `docs/agent-flow/source-documents.md` may exist as optional sidecar evidence.

## Rules

- Start from business flows and regression surfaces, not from edited files.
- Do not create required scenarios solely from source-document claims that are
  `conflicts-with-repo`, `aspirational`, `stale-or-unknown`, or
  `needs-user-confirmation`.
- If source documents mention a high-risk future flow that is not confirmed in
  `business-flows.md`, record it as a coverage gap or open question rather than
  required coverage.
- Prefer deterministic, seedable, repeatable scenarios.
- Use Playwright for visible/multi-step browser behavior.
- Use Feature/API tests for server behavior, validation, permission, mail/PDF/job, and persistence where browser adds little value.
- Every high-risk business flow needs coverage or an explicit blocker/waiver.
- Every Integration Coverage Contract row needs Feature/API integration, Unit, Browser, Migration, or waiver evidence.
- For flows that depend on external runtimes, deployed artifacts, provider
  callbacks, remote data, env/secrets/bindings, auth/session cookies, or
  production-only behavior, include runtime-causality scenarios that distinguish
  shallow checks from the valid happy path and side-effect path.
- Identify candidate major operation tests that can later be confirmed and
  made executable by `business-flow-integration-test`. Do not treat those
  candidates as approved executable tests until that follow-up skill gets user
  confirmation.

## Workflow

1. Read project structure and business-flow docs.
2. Read source-document intake if present, and identify any unconfirmed claims
   that must remain coverage gaps or open questions.
3. Classify each confirmed flow and required case type by verification level: Unit, Feature/API, Playwright, migration/runtime, manual/blocker.
4. Draft Playwright scenarios with major screenshot steps.
5. Draft non-browser integration scenarios for server-side surfaces.
6. Define seed data and reset strategy.
7. Define runtime/provider smoke and causality checks.
8. Define pass/fail evidence requirements.
9. Record business-flow integration-test candidates and open questions for the
   post-onboarding `business-flow-integration-test` follow-up.

## Output Template

```markdown
# Integration Scenarios

## Scenario Matrix
| Scenario ID | Level | Business flow | Case type | Entry point | Data setup | Steps | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Playwright Scenarios
| Scenario ID | Entry point | Major steps requiring screenshots | Assertions | Screenshot names |
| --- | --- | --- | --- | --- |

## Server Integration Scenarios
| Scenario ID | Test type | Case type | Target | Data setup | Assertions | Covers |
| --- | --- | --- | --- | --- | --- | --- |

## Runtime / Provider Smoke Scenarios
| Scenario ID | Runtime surface | Trigger / risk | Evidence command or source | Representative paths | Expected classification |
| --- | --- | --- | --- | --- | --- |
| RUNTIME-001 | {deploy/provider/runtime} | {production-only, browser-network, auth/session, binding, remote data, provider callback} | {smoke command, provider log, deploy version check, read-only diagnostic} | {preflight/invalid/valid/side-effect path} | code / environment-ops / data / deploy artifact / provider-runtime / inconclusive |

## Business Flow Integration Test Candidates
| Candidate ID | Business flow | Continuous operation | Suggested level | Data / environment needs | Questions before executable test |
| --- | --- | --- | --- | --- | --- |

## Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Scenario IDs | Waiver / blocker |
| --- | --- | --- | --- | --- |

## Seed / Reset Strategy
- ...

## Evidence Contract
- Playwright evidence root: `docs/flow/{feature}/integration-test/{run_id}/`
- Required files: `index.html`, `result.md`, `test-review.md`, `business-flow-impact.md`, `screenshots/`

## Coverage Gaps
| Gap | Reason | Follow-up |
| --- | --- | --- |

## Source Document Gaps
| Claim ID | Reason not covered as required scenario | Follow-up |
| --- | --- | --- |
```

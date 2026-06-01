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

## Rules

- Start from business flows and regression surfaces, not from edited files.
- Prefer deterministic, seedable, repeatable scenarios.
- Use Playwright for visible/multi-step browser behavior.
- Use Feature/API tests for server behavior, validation, permission, mail/PDF/job, and persistence where browser adds little value.
- Every high-risk business flow needs coverage or an explicit blocker/waiver.
- Every Integration Coverage Contract row needs Feature/API integration, Unit, Browser, Migration, or waiver evidence.
- For flows that depend on external runtimes, deployed artifacts, provider
  callbacks, remote data, env/secrets/bindings, auth/session cookies, or
  production-only behavior, include runtime-causality scenarios that distinguish
  shallow checks from the valid happy path and side-effect path.

## Workflow

1. Read project structure and business-flow docs.
2. Classify each flow and required case type by verification level: Unit, Feature/API, Playwright, migration/runtime, manual/blocker.
3. Draft Playwright scenarios with major screenshot steps.
4. Draft non-browser integration scenarios for server-side surfaces.
5. Define seed data and reset strategy.
6. Define runtime/provider smoke and causality checks.
7. Define pass/fail evidence requirements.

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
```

---
name: business-flow-discovery
description: |
  Build business-flow documentation through dialogue after project structure
  survey. Use during agent-flow onboarding to turn architecture/domain/use-case
  understanding into exhaustive business-flow and regression-surface knowledge.
---

# Business Flow Discovery

Create `docs/agent-flow/business-flows.md`.

## Prerequisites

- `docs/agent-flow/project-structure.md` exists.

## Rules

- Start from the project structure survey.
- Ask the user concise questions only where business behavior is ambiguous.
- Prefer flow coverage over implementation detail.
- Include normal, error, permission, boundary, status, mail/PDF/export, job, and integration paths where relevant.
- Do not mark a flow complete if adjacent regression surfaces are unknown.
- Do not use vague waivers. If coverage is not required or is blocked, record the concrete reason or blocker.

## Workflow

1. Read `docs/agent-flow/project-structure.md`.
2. Draft candidate business flows from use cases.
3. Ask the user for missing business rules and priority/risk.
4. Produce Business Flow Matrix.
5. Produce Regression Surface Matrix.
6. Record unresolved questions.

## Output Template

```markdown
# Business Flows

## Flow Inventory
| Flow ID | Flow | Actor | Entry point | Priority | Risk |
| --- | --- | --- | --- | --- | --- |

## Business Flow Matrix
| Flow ID | Actor / scope | Entry point | Existing behavior | Expected behavior | Normal path | Error/exception paths | Permission/ownership/boundary paths | Side effects | Regression risk | Required verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Regression Surface Matrix
| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| Routes/controllers/API | | | |
| Screens/views/client JS | | | |
| Shared services/actions | | | |
| Schema/migrations | | | |
| Jobs/schedules | | | |
| Mail/PDF/export | | | |
| Auth/permissions | | | |
| External APIs/storage/cache/search | | | |

## Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |

Waiver rules:
- Valid: includes a concrete `because`, `reason`, `blocked by`, `out of scope`, `理由`, `根拠`, `ブロック`, or `対象外`.
- Invalid: `N/A`, `manual`, `low risk`, `TBD`, `later`, blank, or any waiver without a reason.

## User-confirmed Decisions
- ...

## Open Questions
- ...
```

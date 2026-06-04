---
name: business-flow-discovery
description: |
  Build business-flow documentation through dialogue after project structure
  survey. Use during agent-flow onboarding to turn architecture/domain/use-case
  understanding into exhaustive business-flow and regression-surface knowledge.
---

# Business Flow Discovery

Create `docs/agent-flow/business-flows.md` and the companion draw.io diagram
`docs/agent-flow/business-flows.drawio`.

## Prerequisites

- `docs/agent-flow/project-structure.md` exists.
- `docs/agent-flow/source-documents.md` may exist as optional sidecar evidence.

## Rules

- Start from the project structure survey.
- If `docs/agent-flow/source-documents.md` exists, read the claim ledger before
  drafting flows.
- Use only `confirmed` or explicitly user-confirmed source-document claims in
  Business Flow Matrix expected behavior.
- Do not treat `conflicts-with-repo`, `aspirational`, `stale-or-unknown`, or
  `needs-user-confirmation` claims as current behavior or required future
  behavior. Convert them into open questions, blockers, or stale/aspirational
  notes.
- Ask the user concise questions only where business behavior is ambiguous.
- Prefer flow coverage over implementation detail.
- Include normal, error, permission, boundary, status, mail/PDF/export, job, and integration paths where relevant.
- Do not mark a flow complete if adjacent regression surfaces are unknown.
- Do not use vague waivers. If coverage is not required or is blocked, record the concrete reason or blocker.
- Keep `docs/agent-flow/business-flows.md` canonical. The draw.io diagram is a
  human-readable companion artifact, not a replacement for the required
  matrices.
- The draw.io diagram must use Flow IDs that match the Flow Inventory and show
  actors/entrypoints, normal paths, error/exception paths,
  permission/ownership/boundary paths, side effects/integrations, and
  unresolved questions/blockers where known.
- If a useful diagram cannot be produced, record the concrete blocker in
  `business-flows.md` instead of silently omitting it.

## Workflow

1. Read `docs/agent-flow/project-structure.md`.
2. Read `docs/agent-flow/source-documents.md` if it exists, then separate
   confirmed claims from conflicts, aspirational notes, stale/unknown notes, and
   claims that need user confirmation.
3. Draft candidate business flows from use cases and confirmed claims only.
4. Ask the user for missing business rules, priority/risk, and any
   `needs-user-confirmation` claims that would affect matrices.
5. Produce Business Flow Matrix.
6. Produce Regression Surface Matrix.
7. Create `docs/agent-flow/business-flows.drawio`.
8. Validate the `.drawio` file as well-formed XML when practical.
9. Record unresolved questions.

## Output Template

```markdown
# Business Flows

## Flow Inventory
| Flow ID | Flow | Actor | Entry point | Priority | Risk |
| --- | --- | --- | --- | --- | --- |

## Diagram
- Draw.io file: `docs/agent-flow/business-flows.drawio`
- Diagram status: created / blocked because ...
- Consistency check: Flow IDs in the diagram match the Flow Inventory.

## Source Document Claim Handling
| Claim status | Handling decision | Notes |
| --- | --- | --- |
| confirmed | May inform Flow Inventory / Business Flow Matrix |  |
| conflicts-with-repo | Open question or conflict note only |  |
| aspirational / stale-or-unknown / needs-user-confirmation | Open question, blocker, or future-scope note only |  |

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

## Draw.io Artifact Contract

Create `docs/agent-flow/business-flows.drawio` as a diagrams.net/draw.io XML
file. The diagram should be readable when opened in draw.io and should include:

- flow nodes labeled with the same Flow IDs used in `business-flows.md`,
- actor or system boundary nodes for each major actor/scope,
- entrypoint labels for routes, screens, jobs, APIs, commands, or external
  triggers,
- normal path arrows,
- error/exception branches,
- permission/ownership/boundary branches,
- side-effect or integration nodes such as mail, PDF/export, jobs, storage,
  search/cache, or external APIs,
- unresolved question or blocker nodes for flows that are not yet complete.

When practical, validate the generated file with:

```bash
python3 - <<'PY'
import xml.etree.ElementTree as ET
ET.parse("docs/agent-flow/business-flows.drawio")
PY
```

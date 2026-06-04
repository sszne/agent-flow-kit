---
name: flow-document
description: |
  Collect optional service requirement documents at the start of Agent Flow
  onboarding, convert them to Markdown when markitdown is available, and create
  a guarded claim ledger for later project-structure and business-flow work.
---

# Flow Document Intake

Run this skill at the start of `agent-flow-onboarding`.

This skill is mandatory to execute during onboarding, but source documents are
optional. If no documents exist, record that status and continue onboarding.

## Outputs

- `docs/agent-flow/source-documents.md`
- Optional raw document folder: `docs/agent-flow/source-documents/raw/`
- Optional converted Markdown folder:
  `docs/agent-flow/source-documents/converted/`

`docs/agent-flow/source-documents.md` is a sidecar evidence ledger. It is not one
of the required onboarding gate documents and does not replace:

- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

## Source Priority

Use this priority when claims conflict:

```text
source/schema/routes/tests/deploy config > current repo docs > user confirmation > converted requirement docs
```

Requirement documents can describe product intent, future scope, sales framing,
or stale architecture. They must not become source-of-truth by default.

## Claim Statuses

Every imported claim must use one of these statuses:

- `confirmed`: supported by current repo evidence or explicit user confirmation.
- `conflicts-with-repo`: contradicts current source, schema, routes, tests,
  deploy config, or current repo docs.
- `aspirational`: describes future or desired behavior not confirmed in the repo.
- `stale-or-unknown`: age, ownership, or current validity cannot be established.
- `needs-user-confirmation`: potentially useful but not safe to use without a
  user decision.

Only `confirmed` claims, and claims explicitly confirmed by the user during
onboarding, may feed downstream Business Flow Matrix expected behavior.

## Workflow

1. Ask whether service explanation, requirements, sales, design, proposal, or
   specification documents exist.
2. If documents exist, ask the user to provide paths or place files under
   `docs/agent-flow/source-documents/raw/`.
3. Inspect the provided files. Prefer file metadata and a quick content skim
   before drawing conclusions.
4. If `markitdown` is installed, convert supported non-Markdown documents to
   Markdown under `docs/agent-flow/source-documents/converted/`.
   - Check with `command -v markitdown`.
   - Use `markitdown "$input" -o "$output"`.
   - Keep the original file and record conversion status.
5. If `markitdown` is missing or conversion fails, record the concrete blocker
   and continue with any readable Markdown/text content.
6. Build a claim ledger. Extract only claims that could affect architecture,
   domain models, use cases, business flows, data ownership, permissions,
   integrations, non-functional requirements, or open implementation questions.
7. Verify claims against current repo evidence when practical.
8. Write or update `docs/agent-flow/source-documents.md`.
9. Report the intake status before continuing to `project-structure-survey`.

## Output Template

```markdown
# Source Documents

## Intake Status
- Status: no-documents-provided / converted / conversion-blocked / partial
- markitdown: available / unavailable / failed because ...
- Last updated:

## Source Priority
source/schema/routes/tests/deploy config > current repo docs > user confirmation > converted requirement docs

## Document Inventory
| Document ID | Original path | Converted path | Type | Conversion status | Notes |
| --- | --- | --- | --- | --- | --- |

## Claim Ledger
| Claim ID | Source | Claim | Category | Status | Repo evidence | Onboarding action |
| --- | --- | --- | --- | --- | --- | --- |

Allowed statuses: `confirmed`, `conflicts-with-repo`, `aspirational`,
`stale-or-unknown`, `needs-user-confirmation`.

## Conflicts And Stale/Aspirational Notes
| Claim ID | Conflict / uncertainty | Required follow-up |
| --- | --- | --- |

## Open Questions
- ...
```

## Downstream Rules

- `project-structure-survey` may use this ledger only as candidate evidence.
  Repo source, schema, routes, tests, package files, and deploy config remain
  stronger evidence.
- `business-flow-discovery` may use only `confirmed` or user-confirmed claims in
  Business Flow Matrix expected behavior.
- `conflicts-with-repo`, `aspirational`, `stale-or-unknown`, and
  `needs-user-confirmation` claims must become open questions, blockers, or
  stale/aspirational notes before they influence implementation plans.
- `integration-scenario-design` must not create required test scenarios solely
  from unconfirmed document claims.

---
name: agent-flow-onboarding
description: |
  Run full agent-flow onboarding for a new repository. Use to create project
  structure, business-flow, and integration-scenario documentation before
  adopting flow-plan, flow-impl, integration-test, and team-review gates.
---

# Agent Flow Onboarding

Run the onboarding sequence for a repo that will adopt agent-flow.

## Outputs

- `docs/agent-flow/source-documents.md` (sidecar evidence ledger; content is
  optional and absence of source documents is not a blocker)
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/business-flows.drawio` (companion diagram for human review)
- `docs/agent-flow/integration-scenarios.md`

Optional follow-up output after onboarding:

- `docs/agent-flow/business-flow-integration-tests.md` (confirmed executable
  operation-test suite spec, created by `business-flow-integration-test`)

## Sequence

1. Run `flow-document`.
   - If service requirement/source documents exist, convert them with
     `markitdown` when available and create a guarded claim ledger.
   - If no source documents exist, record `no-documents-provided` in
     `docs/agent-flow/source-documents.md` and continue.
2. Run `project-structure-survey`.
3. Run `business-flow-discovery`.
4. Run `integration-scenario-design`.
5. Report readiness:
   - source document intake executed and status recorded,
   - architecture/domain/use cases documented,
   - business flows and regression surfaces documented,
   - business-flow draw.io diagram created or a concrete blocker recorded,
   - integration-test scenarios documented,
   - runtime-causality evidence sources documented, including deploy/version
     checks, runtime logs, smoke commands, bindings/secrets, remote data
     diagnostics, provider sandboxes, or concrete blockers,
   - open questions/blockers named.
6. Explain the recommended follow-up:
   - Agent Flow can use the confirmed business-flow docs to propose major
     operation tests as a regression-prevention route.
   - Tell the user to invoke `business-flow-integration-test` to infer the
     test list, ask about unclear operations, accept missing operations, get
     approval, create executable tests, and register an all-suite runner.
   - Do not create those executable operation tests inside onboarding unless
     the user explicitly asks to continue into the follow-up skill.

## Required Gate

Do not start behavior-changing implementation until all three documents exist.
If a document cannot be produced, record the blocker and treat behavior-changing work as blocked rather than waived.

`docs/agent-flow/source-documents.md` is a mandatory-execution sidecar, not a
required implementation gate document. Missing service documents should be
recorded as `no-documents-provided`, not treated as an onboarding blocker.

The draw.io diagram does not replace the three required Markdown documents. If
the diagram cannot be produced, record the blocker in
`docs/agent-flow/business-flows.md` and include it in the readiness report.

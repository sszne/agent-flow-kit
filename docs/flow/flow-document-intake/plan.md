# Flow Document Intake Plan

## 1. Requirements

### 1.1 Current State
- `agent-flow-onboarding` currently starts with `project-structure-survey`, then
  runs `business-flow-discovery` and `integration-scenario-design`.
- `business-flow-discovery` starts from `docs/agent-flow/project-structure.md`
  and writes `docs/agent-flow/business-flows.md` plus the companion draw.io
  diagram.
- The kit has no dedicated step for collecting requirement/specification
  documents before onboarding.
- `markitdown` is not part of this kit. It may be installed globally on a user's
  machine, but the kit must not require it as a dependency.
- The sample `yoyaku-hub` requirement deck showed the risk clearly: a converted
  document can contain useful product intent while also containing aspirational
  or stale claims that conflict with the effective repository source of truth.

### 1.2 Goal Confirmation
- Requester goal: add an onboarding-start document intake flow so service
  requirement materials can be converted and used to improve business-flow
  discovery.
- Accepted completion signal: Agent Flow Kit templates include a `/flow-document`
  / `flow-document` workflow, onboarding runs it first, and later onboarding
  steps use its output only through explicit source-priority and claim-status
  guardrails.

### 1.3 Questioning Decision
- Decision: No additional user questions required.
- No Questions Rationale:
  - The user specified the intended skill name, onboarding timing, markitdown
    behavior, and primary risk.
  - The previous investigation resolved the key ambiguity: proceed with a
    mandatory-execution sidecar, not an authoritative source-of-truth step.
  - Existing kit docs provide the affected flows, required artifacts, and
    validation style for workflow-contract changes.

### 1.4 Scope / Non-Goals
In scope:
- Add `flow-document` skill templates for Codex and Claude Code.
- Add a Claude slash-command wrapper for `/flow-document`.
- Update manifest, gitignore exceptions, README, and onboarding skill templates.
- Update project-structure, business-flow, and integration-scenario templates so
  they read document-intake output safely.
- Update kit-local `docs/agent-flow/*` knowledge for the new onboarding flow.

Out of scope:
- Bundling or installing `markitdown`.
- Building a deterministic document parser or semantic classifier.
- Making converted requirement documents a required CI/matrix-gate artifact.
- Treating requirement documents as authoritative over source/schema/routes/tests.
- Moving or rewriting target-repo requirement documents automatically.

### 1.5 Acceptance Criteria
- `flow-document` exists under both:
  - `templates/.codex/skills/flow-document/SKILL.md`
  - `templates/.claude/skills/flow-document/SKILL.md`
- `/flow-document` exists for Claude Code.
- `agent-flow-onboarding` runs `flow-document` first and reports document-intake
  status.
- `flow-document` creates or updates `docs/agent-flow/source-documents.md`.
- The source document ledger classifies imported claims as:
  - `confirmed`
  - `conflicts-with-repo`
  - `aspirational`
  - `stale-or-unknown`
  - `needs-user-confirmation`
- Source priority is explicit:
  `source/schema/routes/tests/deploy config > current repo docs > user confirmation > converted requirement docs`.
- `business-flow-discovery` uses only confirmed or user-confirmed claims in the
  Business Flow Matrix; conflicts and uncertain claims become open questions or
  notes.
- `project-structure-survey` may use intake as candidate evidence but must verify
  repository facts against real repo evidence.
- `integration-scenario-design` does not create required scenarios solely from
  unconfirmed document claims.
- README explains that the step is mandatory to run during onboarding but
  optional in content; absence of source documents is recorded, not treated as a
  blocker.
- Claude and Codex skill templates remain aligned.

## 2. Design

### 2.1 Affected Files And Modules
| File | Change |
| --- | --- |
| `templates/.codex/skills/flow-document/SKILL.md` | New Codex skill for source document intake, conversion, and claim ledger |
| `templates/.claude/skills/flow-document/SKILL.md` | Mirror Codex skill |
| `templates/.claude/commands/flow-document.md` | New Claude slash-command wrapper |
| `manifest.json` | Add `flow-document` as an entry skill / canonical flow step |
| `templates/gitignore.agent-flow.fragment` | Ensure new skill directories remain tracked after install |
| `README.md` | Document the updated onboarding sequence and sidecar output |
| `templates/AGENTS.md` | Mention document intake in context-first onboarding docs |
| `templates/CLAUDE.md` | Mirror AGENTS guidance |
| `templates/.codex/skills/agent-flow-onboarding/SKILL.md` | Run `flow-document` first and report status |
| `templates/.claude/skills/agent-flow-onboarding/SKILL.md` | Mirror Codex onboarding skill |
| `templates/.codex/skills/project-structure-survey/SKILL.md` | Read intake ledger as candidate evidence only |
| `templates/.claude/skills/project-structure-survey/SKILL.md` | Mirror Codex survey skill |
| `templates/.codex/skills/business-flow-discovery/SKILL.md` | Apply claim-status guardrails before matrix generation |
| `templates/.claude/skills/business-flow-discovery/SKILL.md` | Mirror Codex business-flow skill |
| `templates/.codex/skills/integration-scenario-design/SKILL.md` | Avoid scenarios from unconfirmed claims |
| `templates/.claude/skills/integration-scenario-design/SKILL.md` | Mirror Codex scenario skill |
| `docs/agent-flow/business-flows.md` | Record the new Agent Flow Kit flow |
| `docs/agent-flow/integration-scenarios.md` | Add static review scenarios for document-intake guardrails |
| `docs/agent-flow/project-structure.md` | Record new skill and sidecar artifact type |

### 2.2 Implementation Approach
1. Add `flow-document` skill:
   - Ask the user to provide or place service documents if they exist.
   - Suggested raw location:
     `docs/agent-flow/source-documents/raw/`.
   - Suggested converted location:
     `docs/agent-flow/source-documents/converted/`.
   - If `markitdown` is available, convert supported non-Markdown files to
     Markdown.
   - If `markitdown` is not available or conversion fails, record the blocker
     and continue with available Markdown/text evidence.
   - Always write `docs/agent-flow/source-documents.md`, even when no documents
     are provided.
2. Add claim ledger rules:
   - Do not copy claims directly into onboarding matrices.
   - Each claim must have status, source, repo evidence, and onboarding action.
   - Conflicts and uncertain claims become questions or notes, not expected
     behavior.
3. Update onboarding sequence:
   - `flow-document`
   - `project-structure-survey`
   - `business-flow-discovery`
   - `integration-scenario-design`
4. Update downstream skills:
   - Survey verifies claims against repo source.
   - Business-flow discovery uses confirmed claims only.
   - Integration scenario design records unconfirmed-doc scenario requests as
     coverage gaps or questions.
5. Update distribution metadata and docs.

### 2.3 Source Document Ledger Contract
`docs/agent-flow/source-documents.md` should include:

```markdown
# Source Documents

## Intake Status
- Status: no-documents-provided / converted / conversion-blocked / partial
- markitdown: available / unavailable / failed because ...

## Source Priority
source/schema/routes/tests/deploy config > current repo docs > user confirmation > converted requirement docs

## Document Inventory
| Document ID | Original path | Converted path | Type | Conversion status | Notes |
| --- | --- | --- | --- | --- | --- |

## Claim Ledger
| Claim ID | Source | Claim | Category | Status | Repo evidence | Onboarding action |
| --- | --- | --- | --- | --- | --- | --- |

## Conflicts And Stale/Aspirational Notes
| Claim ID | Conflict / uncertainty | Required follow-up |
| --- | --- | --- |

## Open Questions
- ...
```

### 2.4 Risks And Mitigations
| Risk | Mitigation |
| --- | --- |
| Aspirational documents reduce matrix accuracy | Requirement documents produce a claim ledger, not matrix conclusions |
| Stale docs override real repo behavior | Explicit source priority puts source/schema/routes/tests first |
| Agents silently copy conflict claims into expected behavior | Business-flow discovery may use only confirmed/user-confirmed claims |
| Onboarding becomes blocked when no docs exist | `flow-document` records `no-documents-provided`; required three Markdown onboarding docs remain unchanged |
| markitdown is unavailable | Record conversion blocker and continue with available files |
| Claude/Codex behavior diverges | Mirror skill templates and review parity |

### 2.5 Residual Risk Preflight
| Warning | Countermeasure |
| --- | --- |
| Natural-language classification can still be wrong | Require repo evidence and claim status for each imported claim |
| Converted files may contain layout noise | Claim ledger extracts only actionable claims; noisy text can be ignored with reason |
| User may expect requirement docs to define future behavior | `needs-user-confirmation` status prevents unconfirmed future scope from entering matrices |
| Mandatory execution could feel like process overhead | Absence of documents is a short recorded status, not a blocker |

### 2.6 Bug Feedback Review
This is a workflow hardening change, not a bug/regression report. The prevention
pattern is: requirement documents can be stale or aspirational, so document
claims must be classified before they influence business-flow matrices.

### 2.7 Flow Knowledge Update
- Update kit-local `docs/agent-flow/business-flows.md` to add the new
  document-intake flow.
- Update kit-local `docs/agent-flow/integration-scenarios.md` with static review
  coverage for source-priority and claim-status guardrails.
- Update kit-local `docs/agent-flow/project-structure.md` so the new skill and
  sidecar artifact are visible in future plans.

### 2.8 Business Flow Matrix
| Flow ID | Actor / scope | Entry point | Existing behavior | Expected behavior | Normal path | Error/exception paths | Permission/ownership/boundary paths | Side effects | Regression risk | Required verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-002 | Coding agent onboarding a target repo | `agent-flow-onboarding` | Onboarding starts with repo structure survey | Onboarding first runs `flow-document`, records source-document status, then continues to required docs | Run document intake, survey repo, discover flows, design scenarios, report readiness | No source docs; markitdown unavailable; conversion fails; source claims conflict with repo evidence | Document claims cannot override source/schema/routes/tests/deploy config | Writes `docs/agent-flow/source-documents.md` plus existing required docs | Later plans trust stale requirement claims | Template review and source-priority checklist |
| AFK-003 | Coding agent and user inventorying flows | `business-flow-discovery` | Flow inventory starts from project-structure survey and user questions | Flow inventory can use confirmed source-document claims while conflicts become questions | Read survey and source-doc ledger, draft flows, classify claims, write matrices and diagram | Ledger missing; claims unconfirmed; conflicts with repo | Only confirmed/user-confirmed claims enter expected behavior | Updates `business-flows.md` and draw.io | Business matrix includes aspirational or stale behavior | Documentation review against claim ledger rules |
| AFK-004 | Coding agent designing verification | `integration-scenario-design` | Scenario design starts from business-flow docs | Scenario design treats unconfirmed source-doc claims as gaps/questions, not required scenarios | Read project/flow docs, classify coverage, map confirmed flows | Requirement docs mention future flow not confirmed in repo | Future/uncertain flows need user confirmation before required coverage | Writes integration scenario docs | Tests are designed for non-existent or future behavior | Template review and coverage contract review |
| AFK-001 | Developer installing kit | `install.py` | Manifest validates existing entry/support skills | New flow-document skill is distributed with both tool templates and gitignore exceptions | Install or dry-run enumerates new files | Missing SKILL.md path; gitignore excludes new skill | Target-local docs remain preserved | Copies new skill docs and command | Partial install makes `/flow-document` unavailable | Installer dry-run and manifest validation |

### 2.9 Regression Surface Matrix
| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| New skill distribution | AFK-001, AFK-002 | `manifest.json`, skill directories, gitignore fragment | Installer dry-run and path review |
| Onboarding sequence | AFK-002 | `agent-flow-onboarding` templates, README | Documentation review for first-step execution and non-blocking no-doc status |
| Source priority policy | AFK-002, AFK-003, AFK-004 | `flow-document`, survey, flow, scenario skill templates | Targeted `rg` checks for claim statuses and priority wording |
| Business-flow matrix generation | AFK-003 | `business-flow-discovery` templates | Verify only confirmed/user-confirmed claims may enter matrices |
| Integration scenario generation | AFK-004 | `integration-scenario-design` templates | Verify unconfirmed claims become gaps/questions |
| Claude/Codex parity | AFK-002 through AFK-004 | Mirrored template files | `cmp -s` or focused diff review |
| README and entry guidance | AFK-001 through AFK-004 | README, AGENTS, CLAUDE | Documentation review |

### 2.10 Test Design Matrix
| Test ID | Level | Target | Scenario | Expected result | Covers flow/risk |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Static review | `flow-document` skill templates | Confirm ledger contract, markitdown optional behavior, source priority, and claim statuses | Both tool templates define the same guarded intake workflow | AFK-002 stale/noisy document risk |
| TEST-002 | Static review | `agent-flow-onboarding` templates | Confirm `flow-document` is first and readiness reports status | Mandatory execution without weakening required docs | AFK-002 sequence risk |
| TEST-003 | Static review | downstream onboarding skills | Confirm survey/flow/scenario templates consume only verified claims | Conflicts/uncertain claims become questions/gaps | AFK-003, AFK-004 matrix accuracy |
| TEST-004 | CLI smoke | Installer dry-run | Run dry-run against a temporary target | Manifest validation passes with new skills | AFK-001 distribution |
| TEST-005 | Syntax smoke | Python files | Run `py_compile` on installer, hooks, and scripts | Python files parse | AFK-001, AFK-009 incidental regression |
| TEST-006 | Targeted grep | Updated docs/templates | Search for `source-documents.md`, claim statuses, and source priority | Guardrail wording exists in the intended files | Documentation regression |

### 2.11 Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-001 | Installer dry-run and Python syntax smoke | Happy, exception, boundary, regression | None |
| AFK-002 | Template review for onboarding sequence and readiness reporting | Happy, exception, regression | Automated agent execution is out of scope because onboarding is a natural-language workflow |
| AFK-003 | Template review for claim-status guarded matrix generation | Happy, exception, permission, boundary, side effect, regression | Automated semantic proof is out of scope because claim classification requires human/source review |
| AFK-004 | Template review for scenario-design handling of unconfirmed claims | Happy, exception, boundary, regression | Automated scenario execution is out of scope because this change affects planning docs |

### 2.12 Playwright Integration Test Plan
No Playwright run is required because this change affects agent workflow
templates and Markdown documentation, not a visible web runtime.

### 2.13 Migration / Runtime Enforcement
- Migration needed: No.
- Runtime behavior changed: No product runtime; this is Agent Flow workflow
  behavior.
- Validation commands:
  - `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py`
  - `python3 install.py --target /tmp/agent-flow-kit-flow-document-smoke --dry-run`
  - targeted `rg` checks for source-document guardrails.

### 2.14 Open Questions
- None blocking the minimal implementation.
- Future enhancement: add a deterministic helper that inventories files and
  invokes markitdown, after observing several real onboarding runs.

## 3. Tasks
- [x] TASK-001: Add Codex `flow-document` skill.
- [x] TASK-002: Add Claude `flow-document` skill and slash command.
- [x] TASK-003: Update manifest and gitignore fragment for distribution.
- [x] TASK-004: Update onboarding skill templates and README sequence.
- [x] TASK-005: Update survey, business-flow, and scenario-design skill
  guardrails.
- [x] TASK-006: Update AGENTS/CLAUDE template context guidance.
- [x] TASK-007: Update kit-local `docs/agent-flow/*` knowledge.
- [x] TASK-008: Run validation commands and review diff.

## 4. Readiness
- [x] Requirements map to tasks.
- [x] User intent and risk are documented.
- [x] Business/product ambiguity has been resolved or explicitly blocked.
- [x] Required onboarding docs exist for behavior-changing workflow work.
- [x] Flow Knowledge Update target is explicit.
- [x] Residual Risk Preflight warnings have countermeasures.
- [x] Business flows map to required tests or blockers.
- [x] Integration Coverage Contract has concrete coverage or waivers.
- [x] Validation commands are identified.
- [x] Plan review exists or a same-agent fallback is recorded before
  implementation starts.

<!-- frozen: v1 2026-06-04 by Codex -->
<!-- plan_author: codex -->

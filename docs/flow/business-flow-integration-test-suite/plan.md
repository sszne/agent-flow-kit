# Business Flow Integration Test Suite

## 1. Requirements

### 1.1 Current State

Agent Flow Kit onboarding currently produces durable project docs:
`source-documents.md`, `project-structure.md`, `business-flows.md`,
`business-flows.drawio`, and `integration-scenarios.md`.

`flow-integration-test` verifies a specific implemented feature after
`flow-impl` or `team-implement`, but the kit does not yet provide an
onboarding follow-up that turns the confirmed business-flow inventory into a
re-runnable regression suite for major end-to-end operations.

### 1.2 Intent And Ambiguity Resolution

The requester wants business-flow integration tests to become a clearer
regression-prevention route. After onboarding, the agent should explain that it
can infer major operation tests from business flows, present the inferred list,
ask about unclear operations, accept missing operations from the user, confirm
the final list, create the integration tests, and register a callable entry so
all operation tests run together.

No clarification is required for this kit change because the user specified the
workflow order, gave concrete examples, and explicitly said this should not be
integrated into `flow-impl` at this stage to avoid large token usage.

### 1.3 Goal

Add a portable Agent Flow entrypoint that target repositories can invoke after
onboarding to create and run a confirmed business-flow integration regression
suite.

### 1.4 Scope / Non-Goals

In scope:

- Add a new Claude/Codex skill for business-flow integration-test suite
  creation and execution.
- Add a Claude slash command wrapper for the new skill.
- Register the new entrypoint in `manifest.json` and the documented canonical
  flow.
- Update onboarding, integration-scenario, README, AGENTS, CLAUDE, and
  `docs/agent-flow/*` guidance so the suite is discoverable after onboarding.
- Define output artifacts, user-confirmation gates, runner registration, and
  execution/pass criteria.

Out of scope:

- Automatically running the suite from `flow-impl`.
- Forcing every target repo to create the suite during initial onboarding.
- Adding a new generic hook that executes long Playwright suites
  automatically.
- Implementing app-specific Playwright tests inside this kit repository.

### 1.5 Acceptance Criteria

- `business-flow-integration-test` is available as an entry skill for both
  Claude and Codex.
- Claude users can invoke an aligned slash command.
- Onboarding docs say the next step is to propose and confirm major
  business-flow operation tests.
- The new workflow requires explicit user approval before creating or changing
  target-repo tests.
- The workflow defines a suite spec, executable runner, evidence directory, and
  all-tests command contract.
- Existing `flow-integration-test` remains feature-specific and is not merged
  with the new onboarding follow-up.

### 1.6 User Answers

- Requirement questions asked: No.
- User answers: The user explicitly requested the five-step workflow and
  stated that `flow-impl` integration is out of scope for now.
- No Questions Rationale: The desired sequencing, example business flows,
  registration expectation, and non-goal are specified in the request and align
  with existing onboarding and integration-test docs.

## 2. Design

### 2.1 Affected Files And Modules

- `manifest.json`
- `README.md`
- `templates/AGENTS.md`
- `templates/CLAUDE.md`
- `templates/.codex/skills/agent-flow-onboarding/SKILL.md`
- `templates/.claude/skills/agent-flow-onboarding/SKILL.md`
- `templates/.codex/skills/integration-scenario-design/SKILL.md`
- `templates/.claude/skills/integration-scenario-design/SKILL.md`
- `templates/.codex/skills/business-flow-integration-test/SKILL.md`
- `templates/.claude/skills/business-flow-integration-test/SKILL.md`
- `templates/.claude/commands/business-flow-integration-test.md`
- `templates/.codex/skills/flow-integration-test/SKILL.md`
- `templates/.claude/skills/flow-integration-test/SKILL.md`
- `templates/.claude/commands/flow-integration-test.md`
- `templates/.codex/skills/integration-test/SKILL.md`
- `templates/.claude/skills/integration-test/SKILL.md`
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

### 2.2 Implementation Approach

Create `business-flow-integration-test` as an entry skill that supports two
modes:

- `create` / default: after onboarding, read business-flow and integration
  scenario docs, infer major continuous operation tests, ask focused questions
  for unclear operations, confirm the final test list with the user, create
  concrete Playwright/API specs in the target repo, and register an all-suite
  runner.
- `run`: execute the previously registered all-suite command, collect evidence,
  and report PASS / FAIL / BLOCKED.

Define portable target-repo artifacts:

- `docs/agent-flow/business-flow-integration-tests.md`: suite specification,
  confirmed scenarios, runner command, data/seed/reset assumptions, and open
  blockers.
- Test files under the target repo's existing e2e/integration convention, or
  `tests/business-flow/` when no convention exists.
- A runner command registered in `package.json`, project test config, or a
  script such as `scripts/run-business-flow-integration-tests.*`.
- Evidence under
  `docs/agent-flow/business-flow-integration-test-runs/{run_id}/`.

Keep the skill agent-guided rather than hook-driven. Long browser suites should
be run deliberately by invoking the skill or the registered command, not by
implicit hooks during every implementation turn.

### 2.3 Design Policy And Library Selection

Use the target repository's existing Playwright/API test infrastructure when
available. If no browser runner exists, the skill should add the smallest
project-native setup needed or record a concrete blocker. Do not add a test
framework that conflicts with established repo patterns.

### 2.4 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Inferred flows become wrong or too broad | Require a user confirmation gate before creating tests. |
| The suite duplicates feature-specific `flow-integration-test` work | Document that this suite is an onboarding regression baseline, while `flow-integration-test` is feature evidence. |
| Long browser suites consume too many tokens or runtime minutes | Keep the suite callable on demand and out of `flow-impl`. |
| External-provider flows cannot run locally | Record real-provider/device blockers and keep deterministic mock/API coverage separate. |
| Target repos have different test layouts | Prefer existing conventions and fall back to `tests/business-flow/` only when none exist. |

### 2.5 Residual Risk Preflight

| Residual risk | Countermeasure / blocker |
| --- | --- |
| Natural-language business-flow docs cannot fully determine all app operations. | The skill asks unclear-operation questions and accepts user-added operations before suite creation. |
| Some operation tests require seeded accounts, email, time travel, provider callbacks, or deployed domains. | The suite spec must record seed/reset commands, time controls, provider lanes, and blockers before marking a scenario runnable. |
| Generic kit docs cannot prove target-repo test behavior. | Validation for this change is template/manifest/docs review plus installer dry-run; app-specific proof happens in target repos. |

### 2.6 Bug Feedback Review

Not a bug/regression report. This is a workflow hardening request to prevent
future regressions.

### 2.7 Flow Knowledge Update

Update Agent Flow docs to add a new AFK flow for business-flow integration
suite creation and execution, and clarify how it relates to AFK-002, AFK-004,
AFK-008, and AFK-009.

### 2.8 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-002 | Coding agent onboarding a repo | `agent-flow-onboarding` | Onboarding reports readiness and points to `business-flow-integration-test` as the next regression-baseline step | Required docs missing; suite creation blocked until docs exist | Does not edit app code during onboarding follow-up explanation | Writes onboarding docs only | User assumes integration suite exists when it was only designed | Template review |
| AFK-004 | Coding agent designing scenarios | `integration-scenario-design` | Scenario docs identify candidate coverage and feed suite creation | Unconfirmed source-document claims remain gaps | Required scenarios must come from confirmed repo/user evidence | Writes scenario docs | Candidate scenarios become executable tests without confirmation | Template review |
| AFK-008 | Coding agent collecting feature evidence | `flow-integration-test` | Feature-specific evidence remains after implementation | Confused with onboarding regression suite | N/A | Writes `docs/flow/{feature}/integration-test/` | Teams run only feature evidence and miss baseline flows | Template wording review |
| AFK-011 | Coding agent plus user creating regression baseline | `business-flow-integration-test` | Infer major operations, ask questions, confirm list, create specs, register all-suite runner, run on demand | Missing docs, unclear operation, no browser runner, unseedable provider, failing suite | User-approved flow list defines test ownership; provider/device blockers are explicit | Writes suite spec, tests/scripts, and run evidence | Main business journeys regress without a callable all-flow test route | Manifest validation, docs review, installer dry-run |

### 2.9 Regression Surface Matrix

| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| Manifest and installer validation | AFK-001, AFK-011 | `manifest.json`, template skill paths | `python3 -m json.tool`, installer dry-run |
| Onboarding templates | AFK-002, AFK-011 | `agent-flow-onboarding` skills | Cross-tool template review |
| Scenario design templates | AFK-004, AFK-011 | `integration-scenario-design` skills | Cross-tool template review |
| Integration-test templates | AFK-008, AFK-011 | `flow-integration-test`, `integration-test` | Wording review for feature-specific vs baseline suite split |
| README / entrypoint guidance | AFK-001 through AFK-011 | README, AGENTS, CLAUDE | Grep/review for new command and non-goal |
| Agent Flow docs | AFK-002, AFK-004, AFK-008, AFK-011 | `docs/agent-flow/*` | Documentation review |

### 2.10 Test Design Matrix

| Test ID | Level | Target | Scenario | Expected result |
| --- | --- | --- | --- | --- |
| TEST-001 | JSON | `manifest.json` | Parse with `python3 -m json.tool` | Valid JSON |
| TEST-002 | Syntax | Python templates | Run `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py` | Python files parse |
| TEST-003 | Installer smoke | Templates | Run installer dry-run to a temporary target | New skill paths validate and files classify |
| TEST-004 | Static parity | Claude/Codex skills | Compare or grep for new skill and workflow terms | Both tool surfaces expose the same contract |
| TEST-005 | Docs review | README and Agent Flow docs | Grep for `business-flow-integration-test` | New entrypoint is discoverable |

### 2.11 Integration Coverage Contract

| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-001 | Installer dry-run validates manifest skill presence | Happy, exception, regression | None |
| AFK-002 | Onboarding template review for follow-up explanation | Happy, regression | None |
| AFK-004 | Scenario-design template review for suite-candidate handoff | Happy, boundary, regression | None |
| AFK-008 | Integration-test template review for feature-specific boundary | Regression | None |
| AFK-011 | Manifest/docs/template review for create/run workflow and runner contract | Happy, exception, permission, boundary, side effect, regression | App-specific Playwright execution is out of scope because this kit has no target application; target repos run the generated suite. |

### 2.12 Plan Review Requirement

- Requirement: Required.
- Reason: This change modifies Agent Flow contracts, entry skills, slash-command
  surface, onboarding guidance, and installed workflow behavior.
- Triggered criteria: Agent Flow contract changes, workflow entrypoint changes,
  and installed template changes.

### 2.13 Playwright Integration Test Plan

No Playwright browser evidence is required in this kit repository because the
change has no visible app workflow. The new skill requires Playwright/API
evidence in target repositories when it creates executable business-flow
scenarios.

### 2.14 Migration / Runtime Enforcement

No schema migration or runtime service change. Validation is static template
and installer verification.

### 2.15 Open Questions

None for the kit implementation. Target repositories will use the new skill to
ask project-specific operation and data questions before creating tests.

## 3. Tasks

- [ ] TASK-001 Add frozen plan and same-agent fallback plan review.
- [ ] TASK-002 Add Claude/Codex `business-flow-integration-test` skill and Claude command.
- [ ] TASK-003 Register the entrypoint in `manifest.json` and user-facing flow docs.
- [ ] TASK-004 Update onboarding, scenario-design, and integration-test templates.
- [ ] TASK-005 Update Agent Flow docs for AFK-011.
- [ ] TASK-006 Run JSON, Python syntax, installer dry-run, and static discovery checks.

## 4. Readiness

- [x] Requirements map to tasks.
- [x] User intent and current-state analysis is documented.
- [x] Business/product ambiguity has been resolved or explicitly blocked.
- [x] Required onboarding docs exist for behavior-changing work.
- [x] Flow Knowledge Update target is explicit.
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers.
- [x] Business flows map to required tests or blockers.
- [x] Integration Coverage Contract has concrete coverage or waivers.
- [x] Validation commands are identified.

<!-- frozen: v1 2026-06-10 by Codex -->
<!-- plan_author: codex -->

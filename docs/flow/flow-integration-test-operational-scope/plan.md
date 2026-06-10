# Flow Integration Test Operational Scope

## 1. Requirements

### 1.1 Current State

Agent Flow Kit currently ships `flow-integration-test` and `integration-test`
templates as a strict Playwright evidence gate for visible or multi-step
business workflows. The installed `AGENTS.md`, `CLAUDE.md`,
`.claude/rules/testing.md`, README, and Agent Flow docs describe browser
evidence as the normal path when visible workflows are affected.

The current template wording does not yet encode the operational evaluation
rule adopted in `yoyaku-hub`: distinguish high-value full evidence from
low-risk lightweight evidence, and record effectiveness metrics so the team can
measure whether the integration-test step actually finds defects worth its
token and labor cost.

This checkout already contains unrelated in-progress changes for the
`business-flow-integration-test` suite. Those changes touch some of the same
files, so this plan must preserve the existing feature-specific vs baseline
suite boundary while adding the conditional evidence-lane policy.

### 1.2 Intent And Ambiguity Resolution

The requester asked to reflect the previously accepted recommended rule change
into `agent-flow-kit` after it was applied in a target repository. The intended
policy is clear:

- keep the full Playwright evidence gate when it protects visible,
  multi-step, auth/session/permission/tenant, provider/device/deploy,
  external-side-effect, or high-impact release confidence;
- allow focused lightweight evidence for low-risk non-visible changes when
  concrete substitute checks and covered regression surfaces are recorded;
- stop early as `BLOCKED` when a required full gate cannot run, instead of
  spending excessive tokens on unavailable browser/runtime/provider setup;
- collect fixed metrics on defects found, fixes caused, overhead, and blockers
  so later operations can judge usefulness.

No clarification is required because the user approved the recommended
operational rule and explicitly requested that the distribution kit inherit it.

### 1.3 Goal

Update Agent Flow Kit so newly installed or refreshed repositories receive the
conditional `flow-integration-test` evidence-lane contract and effectiveness
metrics, without weakening the required full gate for high-risk workflows.

### 1.4 Scope / Non-Goals

In scope:

- Update Claude and Codex `integration-test` and `flow-integration-test`
  templates.
- Update the Claude `/flow-integration-test` command template.
- Update installed `AGENTS.md` and `CLAUDE.md` guidance.
- Update shared testing/design docs and Agent Flow docs.
- Update README user guidance where the evidence gate is described.
- Add plan/review/report artifacts for this kit change.
- Run static validation, manifest/install smoke, and grep checks.

Out of scope:

- Changing installer copy/update behavior.
- Adding automated telemetry collection or a persistent metrics database.
- Changing the separate `business-flow-integration-test` baseline-suite
  workflow.
- Running app-level Playwright tests in this kit repository, which has no
  application under test.

### 1.5 Acceptance Criteria

- All installed surfaces define the same three evidence lanes:
  `Full Gate Required`, `Lightweight Evidence Allowed`, and `Blocked Early`.
- High-risk surfaces cannot be downgraded to lightweight evidence by vague
  wording.
- Lightweight evidence requires a concrete reason, substitute checks, and the
  covered regression surface.
- Required full evidence that cannot run is reported as `BLOCKED` with blocker
  category, exact unverified surface, and minimum unblock action.
- Evidence artifacts and final reports can record fixed effectiveness metrics.
- Existing `business-flow-integration-test` wording remains separate from
  feature-specific `flow-integration-test`.
- Installer smoke and static checks pass.

### 1.6 User Answers

- Requirement questions asked: No.
- User answers: The user asked to reflect the approved recommended
  `flow-integration-test` operational rule into `agent-flow-kit`.
- No Questions Rationale: The target policy was already accepted in the
  previous target-repo update, and the affected kit surfaces are discoverable
  from the current templates, manifest, README, and Agent Flow docs.

## 2. Design

### 2.1 Affected Files And Modules

- `README.md`
- `templates/AGENTS.md`
- `templates/CLAUDE.md`
- `templates/.claude/commands/flow-integration-test.md`
- `templates/.claude/commands/flow-impl.md`
- `templates/.claude/skills/flow-integration-test/SKILL.md`
- `templates/.claude/skills/integration-test/SKILL.md`
- `templates/.claude/skills/context-loader/SKILL.md`
- `templates/.claude/skills/flow-impl/SKILL.md`
- `templates/.claude/skills/team-implement/SKILL.md`
- `templates/.codex/skills/flow-integration-test/SKILL.md`
- `templates/.codex/skills/integration-test/SKILL.md`
- `templates/.codex/skills/context-loader/SKILL.md`
- `templates/.codex/skills/flow-impl/SKILL.md`
- `templates/.codex/skills/team-implement/SKILL.md`
- `templates/.claude/rules/testing.md`
- `templates/.claude/docs/DESIGN.md`
- `templates/docs/agent-flow-integration-test.md`
- `templates/docs/agent-flow-hardening.md`
- `templates/docs/agent-flow-residual-risk-countermeasures.md`
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

### 2.2 Implementation Approach

Add a shared evidence-lane contract to the integration-test templates:

1. **Full Gate Required**: run full Playwright evidence when visible UI,
   multi-step workflow, auth/session/permission/tenant, provider/device/deploy,
   external side effect, or high-impact release confidence is in scope.
2. **Lightweight Evidence Allowed**: use focused non-browser evidence only when
   the change is API-only, internal logic, docs/skill-only, static/build-only,
   or otherwise non-visible and non-high-risk. Require a concrete reason,
   substitute command results, and the covered regression surface.
3. **Blocked Early**: if a full gate is required but cannot run, stop with
   `BLOCKED`, including blocker category, exact unverified surface, and minimum
   unblock action.

Add a fixed metrics block to the evidence output guidance:

```text
evidence_lane: full | lightweight | blocked
issues_found: count + severity list
fix_resulted: yes | no
fix_reference: commit / file / task / none
would_other_tests_have_caught: yes | no | unknown
elapsed_time_minutes: number | unknown
token_or_work_overhead: estimate | unknown
blocker_category: runner | base_url | auth_session | provider_credentials | device_tunnel | safe_test_data | none
```

Keep this as a documentation/workflow contract. Do not add runtime metrics
storage or change installer behavior.

### 2.3 Design Policy And Library Selection

Use existing Markdown template patterns only. No new dependencies.

### 2.4 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Lightweight lane becomes a broad escape hatch | Explicitly deny lightweight use for visible, multi-step, auth/session/permission/tenant, provider/device/deploy, external-side-effect, and high-impact changes unless the lane is blocked and recorded. |
| Agents keep spending tokens on impossible browser setup | Add `Blocked Early` preflight and required blocker fields. |
| Metrics become inconsistent across target repos | Publish a fixed key list in templates and docs. |
| Claude/Codex templates diverge | Update matching Claude and Codex skill surfaces together and verify with grep. |
| Existing business-flow baseline-suite work is overwritten | Preserve current `business-flow-integration-test` references and only add feature-specific evidence-lane wording. |

### 2.5 Residual Risk Preflight

| Residual risk | Countermeasure / blocker |
| --- | --- |
| Natural-language lane selection cannot be fully enforced by static checks. | Keep high-risk categories explicit in all entrypoint docs and make ambiguous risk default to full gate or blocker. |
| Historical effectiveness metrics before this change are incomplete. | The new contract starts forward-looking measurement; prior runs remain qualitative evidence. |
| Target repos may customize `AGENTS.md` / `CLAUDE.md`. | Installer preserves local-first files; target repos must manually merge protected local guidance during refresh. |

### 2.6 Bug Feedback Review

Not a bug/regression request. This is workflow hardening for future
integration-test usefulness evaluation.

### 2.7 Flow Knowledge Update

Update AFK-008 in `docs/agent-flow/business-flows.md` and
`docs/agent-flow/integration-scenarios.md` so the kit's own business-flow docs
record conditional evidence lanes and metrics. Update
`docs/agent-flow/project-structure.md` if the integration evidence domain model
or existing test surface needs the new lane contract.

### 2.8 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-008 | Coding agent verifying a feature implementation | `flow-integration-test` / `integration-test` | Agent chooses evidence lane, runs full Playwright when required, or records lightweight evidence with rationale | Required browser/app/provider setup unavailable; no safe data; missing base URL | Auth/session/permission/tenant/provider/device/deploy risks require full evidence or explicit blocker | Writes `docs/flow/{feature}/integration-test/{run_id}/` when full gate runs; writes report evidence for lightweight/blocked lanes | Full gate overused wastes tokens; lightweight overused misses visible workflow regressions | Template review, grep checks, installer smoke |
| AFK-011 | Coding agent plus user creating/running baseline suite | `business-flow-integration-test` | Baseline suite remains separate from feature-specific evidence | User confuses baseline suite with feature gate | User-approved business-flow list defines suite ownership | Writes baseline suite spec and run evidence | Contract confusion causes duplicated or skipped checks | Wording review preserving the boundary |

### 2.9 Regression Surface Matrix

| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| Integration-test skill templates | AFK-008 | Claude/Codex `integration-test` and `flow-integration-test` skills | Static grep for lanes, high-risk guards, metrics, blocker fields |
| Claude slash command | AFK-008 | `templates/.claude/commands/flow-integration-test.md` | Static grep and documentation review |
| Installed entrypoint guidance | AFK-008, AFK-011 | `templates/AGENTS.md`, `templates/CLAUDE.md` | Static grep for conditional lane wording and baseline-suite boundary |
| Shared testing/design docs | AFK-008 | `.claude/rules/testing.md`, `.claude/docs/DESIGN.md` | Static grep and docs review |
| Kit Agent Flow docs | AFK-008 | `docs/agent-flow/*` | Documentation review and grep |
| Installer/manifest consistency | AFK-001, AFK-008 | `manifest.json`, `install.py`, templates | JSON parse, py_compile, installer dry-run |

### 2.10 Test Design Matrix

| Test ID | Level | Target | Scenario | Expected result |
| --- | --- | --- | --- | --- |
| TEST-001 | Static grep | Integration-test templates and docs | Search for `Full Gate Required`, `Lightweight Evidence Allowed`, `Blocked Early`, and metrics keys | All relevant surfaces expose the lane contract |
| TEST-002 | Static grep | High-risk guard wording | Search for visible/multi-step/auth/session/provider/deploy/external side effect/high-impact terms | High-risk workflows remain full-gate or blocked |
| TEST-003 | JSON | `manifest.json` | Run `python3 -m json.tool manifest.json` | Manifest parses |
| TEST-004 | Syntax | Python installer/hooks/scripts | Run `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py` | Python files parse |
| TEST-005 | Installer smoke | Templates | Run `python3 install.py --target /tmp/agent-flow-kit-operational-scope-smoke --dry-run` after initializing target as git | Manifest/template validation passes |
| TEST-006 | Hygiene | Full diff | Run `git diff --check` | No whitespace errors |

### 2.11 Integration Coverage Contract

| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-001 | Installer dry-run plus manifest/Python validation | Happy, exception, regression | None |
| AFK-008 | Template and docs review for evidence lanes, metrics, high-risk guards, and blocked path | Happy, exception, permission, boundary, side effect, regression | App-level Playwright execution is out of scope because this kit repository has no application under test |
| AFK-011 | Wording review for baseline-suite boundary preservation | Regression | None |

### 2.12 Plan Review Requirement

- Requirement: Required.
- Reason: This change modifies Agent Flow skill behavior, evidence gates,
  required evidence wording, installed templates, and shared workflow docs.
- Triggered criteria: Agent Flow contract changes, workflow gates, required
  evidence, installed template changes, and cross-agent behavior alignment.

### 2.13 Playwright Integration Test Plan

No Playwright browser evidence is required in this kit repository because the
change has no visible app workflow. Target repositories will apply the updated
evidence-lane contract when they run feature-specific `flow-integration-test`.

### 2.14 Migration / Runtime Enforcement

- Migration / Runtime Enforcement: No database migration or runtime service
  change.
- Runtime validation command: JSON parse, Python syntax, installer dry-run,
  static grep checks, and `git diff --check`.

### 2.15 Open Questions

None.

## 3. Tasks

- [x] TASK-001 Create and review the frozen plan for this Agent Flow contract
      change.
- [x] TASK-002 Update Claude/Codex `integration-test` and
      `flow-integration-test` templates with evidence lanes and metrics.
- [x] TASK-003 Update implementation/context entrypoints that invoke or
      summarize `flow-integration-test`.
- [x] TASK-004 Update installed `AGENTS.md`, `CLAUDE.md`, shared testing rules,
      and design decision docs.
- [x] TASK-005 Update README, installed docs, and kit Agent Flow docs for
      AFK-008 and the conditional evidence-lane policy.
- [x] TASK-006 Run static validation, installer smoke, and diff hygiene checks.
- [x] TASK-007 Write implementation report with validation results and any
      remaining blockers.

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

<!-- frozen: v2 2026-06-10 by Codex -->
<!-- plan_author: codex -->

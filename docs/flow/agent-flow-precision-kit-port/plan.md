# Agent Flow Precision Kit Port

## 1. Requirements

### 1.1 Current State

- The user asked to transplant the useful parts of the current
  `yoyaku-hub` Agent Flow precision changes into
  `/Users/suzukisatoshi/Desktop/デスクトップ - 鈴木聡士のMacBook Pro/git/agent-sytem/agent-flow-kit`.
- The target repository is the portable kit. It distributes workflow behavior
  through `templates/.codex/skills/*`, `templates/.claude/commands/*`,
  `templates/.claude/skills/*`, `templates/.claude/rules/*`,
  `templates/docs/*`, `README.md`, and `templates/scripts/agent-flow-matrix-gate.py`.
- Kit onboarding docs exist:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- The kit already contains:
  - mandatory `flow-plan-review` handoff in `README.md`, `templates/AGENTS.md`,
    `templates/CLAUDE.md`, and flow-plan templates;
  - a Runtime Causality Gate in Codex and Claude flow-plan surfaces;
  - matrix-gate validation for `Questioning Decision` or
    `Questioning Decision And User Answers`;
  - `No Questions Rationale` guidance, but not the newer explicit
    `Questioning Decision` output shape across all templates;
  - no portable bug prevention pattern taxonomy in
    `templates/docs/agent-flow/bug-knowledge.md`;
  - no explicit provider/auth/deploy lane checklist in
    `templates/.claude/rules/testing.md`.
- The current target worktree has unrelated untracked
  `docs/flow/authenticated-todo-list/`; this plan must not modify or stage it.

### 1.2 Intent And Ambiguity Resolution

User intent: make the recently accepted Agent Flow accuracy improvements
available as reusable kit behavior, not only as `yoyaku-hub` local rules.

Portable changes to bring over:

1. Explicit `Questioning Decision` section in every plan, with source-backed
   `No Questions Rationale` when no questions are asked.
2. Onboarding/setup/UI guidance checklist for step names, order, exclusions,
   action placement, resume/fallback paths, safe recipient/provider boundaries,
   and blocked evidence lanes.
3. Provider/auth/deploy evidence lanes that distinguish local mocks from
   deployed artifacts, real provider/device happy paths, valid
   credential/session paths, and blockers.
4. Bug-knowledge prevention pattern taxonomy so bug/regression planning can
   classify preventable failures before task design.
5. Testing-rule wording that prevents shallow checks from replacing valid-path
   provider/auth/deploy evidence.

Non-portable `yoyaku-hub` details, such as LINE-specific business-flow rows,
admin route names, store onboarding state, and local app verification commands,
must not be copied into the kit.

### 1.3 Questioning Decision

| Item | Decision |
| --- | --- |
| Questions asked | No |
| Requirement questions asked | No |
| No Questions Rationale | The user explicitly identified the target kit path and asked to port the useful parts of the just-finished Agent Flow precision change. Source evidence in the kit shows the portable extension points: `templates/.codex/skills/flow-plan/SKILL.md`, `templates/.claude/commands/flow-plan.md`, `templates/.claude/skills/flow-plan/SKILL.md`, `templates/.claude/rules/testing.md`, `templates/docs/agent-flow/bug-knowledge.md`, `README.md`, and `docs/agent-flow/*`. The target change is workflow-template guidance, not app business logic, so actor, data ownership, runtime route, schema, and side-effect questions are not needed. |
| User answers | No additional user answers required; the request itself chooses the target repository and scope. |
| Unsafe assumptions | None blocking. The implementation must avoid repo-specific `yoyaku-hub` product details and avoid unrelated untracked `docs/flow/authenticated-todo-list/`. |

### 1.4 Goal

Update Agent Flow Kit so future installs inherit the planning precision
improvements that reduce preventable bugs, ambiguous no-question plans,
repeated UI/onboarding correction loops, and shallow provider/auth/deploy
verification.

### 1.5 Scope / Non-Goals

In scope:

- Portable template changes for Codex and Claude `flow-plan`.
- Portable testing-rule and bug-knowledge template updates.
- Kit-owned Agent Flow docs describing the new planning-precision behavior.
- README guidance where useful for installed-kit users.
- Static validation, Python syntax validation, and installer dry-run smoke.

Out of scope:

- Application/runtime behavior changes.
- Installer classification logic changes unless validation reveals a required
  packaging issue.
- `yoyaku-hub` product-specific flows, LINE-specific credentials, admin routes,
  or verification commands.
- Unrelated untracked `docs/flow/authenticated-todo-list/`.
- Browser/Playwright evidence because this is documentation and template
  behavior only.

### 1.6 Acceptance Criteria

- [x] Codex `flow-plan` template requires `Questioning Decision` and
      source-backed `No Questions Rationale`.
- [x] Claude command and Claude skill compatibility surfaces match the same
      planning precision behavior.
- [x] Flow-plan templates include onboarding/UI precision checks.
- [x] Flow-plan templates and testing rules include provider/auth/deploy
      evidence lanes and reject shallow valid-path substitutes.
- [x] Bug-knowledge template includes a prevention pattern taxonomy.
- [x] Kit `docs/agent-flow/*` documents AFK planning precision and coverage
      expectations.
- [x] README mentions the new precision guarantees without overloading install
      instructions.
- [x] Validation commands pass or have concrete blockers.

### 1.7 User Answers

No additional user answers were required for this plan.

## 2. Design

### 2.1 Affected Files And Modules

| File | Change |
| --- | --- |
| `templates/.codex/skills/flow-plan/SKILL.md` | Add explicit `Questioning Decision`, onboarding/UI, provider/auth/deploy, and bug pattern reuse requirements. |
| `templates/.claude/commands/flow-plan.md` | Mirror the Codex behavior in the slash-command contract and readiness checks. |
| `templates/.claude/skills/flow-plan/SKILL.md` | Add compatibility bullets for the new shared behavior. |
| `templates/.claude/rules/testing.md` | Add provider/auth/deploy evidence lane rules and checklist items. |
| `templates/docs/agent-flow/bug-knowledge.md` | Add prevention pattern taxonomy. |
| `docs/agent-flow/business-flows.md` | Update kit AFK-005 planning flow with precision-specific expectations. |
| `docs/agent-flow/integration-scenarios.md` | Add planning evidence rules for installed workflows. |
| `README.md` | Summarize portable precision guarantees for users installing the kit. |
| `docs/flow/agent-flow-precision-kit-port/plan-review.md` | Required gate artifact before implementation. |
| `docs/flow/agent-flow-precision-kit-port/implementation_report.md` | Implementation report after porting. |

### 2.2 Implementation Approach

Apply the smallest template/doc updates that make the kit distribute the useful
parts of the `yoyaku-hub` precision hardening:

1. Preserve existing Runtime Causality Gate and plan-review behavior.
2. Rename or supplement old `Requirement Questioning Decision` wording so
   explicit `Questioning Decision` remains the canonical plan output while
   preserving matrix-gate compatibility.
3. Add portable guidance only; avoid product-specific examples from
   `yoyaku-hub`.
4. Keep docs and templates aligned instead of adding a new validator unless the
   existing `agent-flow-matrix-gate.py` validation is insufficient.

### 2.3 Design Policy And Library Selection

No new library is needed. This is a Markdown/template update plus static
validation. Existing Python validation and installer smoke commands are enough
for kit-level confidence.

### 2.4 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Kit templates diverge between Codex and Claude | Update Codex, Claude command, and Claude skill compatibility together; run targeted `rg` checks. |
| Repo-specific `yoyaku-hub` language leaks into the portable kit | Use generic provider/auth/deploy/onboarding terms and review changed text for LINE/admin/store-specific wording. |
| Existing matrix gate already expects `Questioning Decision`, but templates remain inconsistent | Align template section names and readiness checks with `agent-flow-matrix-gate.py`. |
| Plan-review gate blocks implementation | Create `plan-review.md` before implementation; if cross-agent review is unavailable in this Codex session, record a same-agent fallback reason per kit contract. |
| Unrelated dirty/untracked files are mixed into final scope | Keep edits to planned paths and report existing `docs/flow/authenticated-todo-list/` separately. |

### 2.5 Residual Risk Preflight

| Risk ID | Applies? | Evidence | Countermeasure |
| --- | --- | --- | --- |
| RR-001 Missed business flows | Yes | This changes AFK-005 planning behavior for installed repos. | Update `docs/agent-flow/business-flows.md` and `docs/agent-flow/integration-scenarios.md`. |
| RR-002 Natural-language plan quality | Yes | The purpose is to improve semantic plan quality beyond structural checks. | Add named output fields, readiness checks, and bug taxonomy. |
| RR-003 Runtime/external dependency gap | Partial | Provider/auth/deploy evidence is the target planning rule, not a runtime incident. | Add evidence lane guidance; no runtime gate evidence is required for this docs-only change. |
| RR-004 Weak test infrastructure | Partial | Kit has no dedicated unit test suite for natural-language skills. | Use targeted `rg`, `git diff --check`, `py_compile`, and installer dry-run smoke. |
| RR-005 Reviewer/waiver quality | Yes | The kit requires plan-review for behavior-changing work. | Create `plan-review.md` before implementation. |

### 2.6 Runtime Causality Gate

| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | No deployed app/runtime is affected; kit docs/templates only. | not triggered |
| Browser symptom vs server outcome | No browser symptom or server request exists. | not triggered |
| Runtime log | No runtime service is involved. | not triggered |
| Representative paths | Template guidance only; installer smoke validates distribution surface. | docs-only |
| Environment bindings | No env vars, secrets, DB, storage, provider config, or deployed artifact changes. | not involved |
| Remote data state | No remote data. | not involved |
| Classification | Docs/template workflow hardening, not runtime-causality bug. | not triggered |

### 2.7 Bug Feedback Review

This is not a single product bug fix, but it is based on prior preventable
rework patterns identified in Agent Flow evaluation:

| Pattern | Prior symptom | Preventable? | Required response |
| --- | --- | --- | --- |
| Requirement/questioning gap | Plans could skip questions without a named decision and later need intent corrections. | Yes | Require `Questioning Decision` and source-backed `No Questions Rationale`. |
| UI-intent or action-placement gap | User correction loops around onboarding step order, labels, exclusions, and action placement. | Yes | Add onboarding/UI checklist before implementation. |
| Runtime/deploy/provider evidence gap | Local or shallow checks could pass while real provider/deploy paths remained unproven. | Yes | Add provider/auth/deploy evidence lanes. |
| Valid-path coverage gap | Invalid/preflight/health checks could substitute for the happy path. | Yes | Add testing-rule language against shallow substitutes. |
| Implementation drift | Workflow lessons could stay local to one repo instead of entering the kit. | Yes | Port portable rules into templates and kit docs. |

### 2.8 Flow Knowledge Update

Reusable kit-level flow knowledge is discovered. Update targets:

- `docs/agent-flow/business-flows.md`: strengthen AFK-005 planning behavior.
- `docs/agent-flow/integration-scenarios.md`: add planning evidence rules.
- `templates/docs/agent-flow/bug-knowledge.md`: add reusable prevention
  taxonomy for installed repositories.

### 2.9 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Existing behavior | Expected behavior | Normal path | Error/exception paths | Permission/ownership/boundary paths | Side effects | Regression risk | Required verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-005 | Coding agent planning behavior change in an installed repo | `flow-plan`, `/flow-plan`, `templates/scripts/agent-flow-matrix-gate.py` | Plans require matrices, review handoff, runtime causality, and some no-question rationale; templates are less explicit than current kit gate and recent repo-local hardening. | Every plan records a named `Questioning Decision`, confirms UI/onboarding precision when relevant, separates provider/auth/deploy evidence lanes, and reuses bug prevention taxonomy before tasks. | Load context, inspect docs/code, decide questions, classify relevant precision patterns, write/freeze plan, hand off to plan review. | Missing source evidence, unresolved user intent, concrete provider evidence blocker, stale docs, vague waiver. | Installed repo local docs remain authoritative; kit template must not overwrite repo-specific business facts. | Writes `docs/flow/{feature}/plan.md` in target repos; may update `docs/agent-flow/*`. | Weak plans allow preventable rework or shallow verification. | Static template checks, matrix-gate compatibility review, installer dry-run. |
| AFK-006 | Reviewing agent | `flow-plan-review` | Reviews required before implementation. | Review sees explicit decision/evidence fields and can reject stale or weak coverage more easily. | Inspect plan, compare matrices and evidence lanes, approve or require changes. | Same-agent fallback, missing plan marker, weak No Questions Rationale. | Cross-agent preferred; fallback reason required. | Writes `plan-review.md`. | Review can miss semantic gaps if template wording remains vague. | Plan-review artifact and targeted review of changed fields. |
| AFK-009 | CI / reviewer | `agent-flow-matrix-gate.py` | Gate already validates `Questioning Decision` / `Questioning Decision And User Answers`. | Template wording aligns with the gate so generated plans satisfy and explain the validation contract. | Risky diff triggers gate; gate checks plan sections and review markers. | Missing plan/review, placeholders, weak waivers, missing No Questions Rationale. | Config remains target-tunable. | CI pass/fail in installed repos. | Template/gate mismatch creates false failures or weak passes. | `py_compile`, targeted `rg`, installer dry-run. |

### 2.10 Regression Surface Matrix

| Surface | Affected flows | Impact | Required verification |
| --- | --- | --- | --- |
| Codex flow-plan template | AFK-005 | Changes plan output contract for Codex users. | Targeted `rg`; docs review. |
| Claude flow-plan command/skill | AFK-005, AFK-006 | Keeps Claude behavior aligned with Codex. | Targeted `rg`; docs review. |
| Testing rules template | AFK-005, AFK-008 | Changes installed repos' test expectations. | Targeted `rg`; no Python runtime. |
| Bug-knowledge template | AFK-005 | Adds taxonomy for bug/regression planning. | Targeted `rg`. |
| Kit docs and README | AFK-001, AFK-005, AFK-009 | Communicates portable workflow guarantees. | Documentation review. |
| Matrix gate script | AFK-009 | No planned code change; existing validation should remain parseable. | `python3 -m py_compile templates/scripts/agent-flow-matrix-gate.py`. |
| Installer packaging | AFK-001 | Template file contents change but install logic should not. | Installer dry-run smoke. |

### 2.11 Test Design Matrix

| Test ID | Level | Surface | Command / Review | Expected result | Covers |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Static grep | Questioning decision | `rg -n "Questioning Decision|No Questions Rationale" ...` | Required terms exist in Codex, Claude command/skill, README, and plan. | AFK-005, AFK-009 |
| TEST-002 | Static grep | UI/onboarding precision | `rg -n "step names|step order|excluded elements|action placement|resume/fallback|blocked evidence lanes|onboarding/UI" ...` | Portable UI guidance appears in flow-plan surfaces and docs. | AFK-005 |
| TEST-003 | Static grep | Provider/auth/deploy evidence lanes | `rg -n "local mock|deployed artifact|real provider|valid credential|valid session|concrete blocker|provider/auth/deploy|shallow checks" ...` | Evidence lane terms appear in flow-plan/testing/docs. | AFK-005, AFK-008 |
| TEST-004 | Static grep | Bug prevention taxonomy | `rg -n "Prevention Pattern Taxonomy|prevention pattern|Requirement/questioning gap|Valid-path coverage gap|Runtime/deploy/provider evidence gap|UI-intent|implementation drift" ...` | Taxonomy appears in bug knowledge and flow-plan surfaces. | AFK-005 |
| TEST-005 | Syntax | Python kit scripts | `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py` | Python files parse. | AFK-001, AFK-009 |
| TEST-006 | Installer smoke | Packaging | `python3 install.py --target /tmp/agent-flow-kit-precision-smoke --dry-run` | Manifest/template validation and dry-run complete. | AFK-001 |
| TEST-007 | Diff hygiene | Planned files | `git diff --check -- {planned paths}` | No whitespace errors. | All |

### 2.12 Integration Coverage Contract

| Flow ID | Required coverage | Required case types | Scenario IDs / Tests | Waiver / blocker |
| --- | --- | --- | --- | --- |
| AFK-001 | Installer dry-run and Python syntax checks | Happy, exception, boundary, side effect, regression | TEST-005, TEST-006 | None. |
| AFK-005 | Documentation/template checks for planning precision | Happy, exception, permission, boundary, side effect, regression | TEST-001, TEST-002, TEST-003, TEST-004, TEST-007 | Automated natural-language execution is out of scope because skills are agent workflow docs; targeted grep and plan-review are the concrete evidence. |
| AFK-006 | Plan-review artifact before implementation | Happy, exception, regression | `docs/flow/agent-flow-precision-kit-port/plan-review.md` | Same-agent fallback allowed only because Claude Code review is not available in this Codex desktop session; fallback reason must be recorded. |
| AFK-008 | Provider/auth/deploy test expectation docs | Happy, exception, permission, boundary, side effect, regression | TEST-003 | Browser evidence is out of scope because no visible app behavior changes. |
| AFK-009 | Gate compatibility and syntax | Happy, exception, boundary, regression | TEST-001, TEST-005 | No gate code change is planned; fixture tests are out of scope because validation logic is unchanged. |

### 2.13 Playwright Integration Test Plan

No Playwright run is required. This change modifies Markdown workflow
templates and docs only; no browser UI or multi-step app workflow exists in the
kit runtime.

### 2.14 Migration / Runtime Enforcement

No DB schema, migration, runtime route, auth middleware, provider config, or
deployed artifact changes are planned.

### 2.15 Open Questions

None.

## 3. Tasks

- [x] TASK-001: Update Codex `flow-plan` template with explicit
      `Questioning Decision`, onboarding/UI, provider/auth/deploy, and bug
      pattern reuse requirements. Type: DIRECT. Depends on: none.
- [x] TASK-002: Update Claude `/flow-plan` command template to mirror the same
      precision requirements, plan shape, and readiness checks. Type: DIRECT.
      Depends on: TASK-001.
- [x] TASK-003: Update Claude `flow-plan` skill compatibility contract. Type:
      DIRECT. Depends on: TASK-002.
- [x] TASK-004: Add prevention pattern taxonomy to
      `templates/docs/agent-flow/bug-knowledge.md`. Type: DIRECT. Depends on:
      TASK-001.
- [x] TASK-005: Update `templates/.claude/rules/testing.md` with
      provider/auth/deploy evidence lane expectations. Type: DIRECT. Depends
      on: TASK-001.
- [x] TASK-006: Update kit `docs/agent-flow/business-flows.md` and
      `docs/agent-flow/integration-scenarios.md` with planning-precision flow
      knowledge. Type: DIRECT. Depends on: TASK-001.
- [x] TASK-007: Update `README.md` with a short summary of the portable
      planning-precision guarantees. Type: DIRECT. Depends on: TASK-001.
- [x] TASK-008: Create implementation report and mark plan tasks complete after
      validation. Type: DIRECT. Depends on: TASK-001..TASK-007.
- [x] TASK-009: Run TEST-001..TEST-007 and record results. Type: DIRECT.
      Depends on: TASK-008.

## 4. Readiness

- [x] Requirements map to tasks.
- [x] User intent and current-state analysis is documented.
- [x] Questioning Decision is documented.
- [x] No Questions Rationale is source-backed when no questions were asked.
- [x] Business/product ambiguity has been resolved or explicitly blocked.
- [x] Required onboarding docs exist for behavior-changing work.
- [x] Flow Knowledge Update target is explicit.
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers.
- [x] Runtime Causality Gate is complete or explicitly not triggered.
- [x] Onboarding/UI plans confirm step names, order, exclusions, action
      placement, resume/fallback path, and blocked evidence lanes.
- [x] Provider/auth/deploy plans separate mock, deployed-artifact, real
      provider/device, valid-path, and blocker evidence.
- [x] Bug/regression work classifies reusable prevention patterns before task design.
- [x] Business flows map to required tests or blockers.
- [x] Integration Coverage Contract has concrete coverage or waivers.
- [x] Validation commands are identified.

<!-- frozen: v1 2026-06-02 -->
<!-- plan_author: codex -->

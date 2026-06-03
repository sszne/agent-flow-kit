# Flow Plan Goal Confirmation Kit Port

<!-- frozen: v1 2026-06-03 by Codex -->

## 1. Requirements

### 1.1 Current State

- The user wants to incorporate the recent `flow-plan` goal-confirmation
  improvement into `agent-flow-kit`, the reusable distribution source.
- The motivating incident came from `wellogi/yoyaku-hub`: the first admin auth
  `429` fix improved the visible error state, but the requester goal was to
  prevent logged-in users from being suddenly logged out by `429` during normal
  operation.
- The kit already includes planning precision improvements:
  - explicit `Questioning Decision` and source-backed `No Questions Rationale`;
  - Runtime Causality Gate;
  - provider/auth/deploy evidence lanes;
  - bug-knowledge prevention taxonomy;
  - mandatory plan-review for behavior-changing work with a non-behavioral
    exception boundary.
- Current kit wording still does not explicitly force a plan to confirm the
  requester's desired user experience / outcome / completion signal when a bug
  report can be interpreted at multiple layers:
  - message or UI feedback improvement;
  - state/session preservation;
  - root-cause elimination;
  - diagnostic-only work;
  - deployed/valid-path proof.

### 1.2 Intent And Ambiguity Resolution

- User intent: port the repo-local Goal Confirmation Gate improvement into the
  source kit so new installations inherit it.
- Ambiguity resolution:
  - No product/runtime question is needed because the target is the kit workflow
    contract, not application behavior.
  - The desired rule is explicit: when requester goal is ambiguous, `flow-plan`
    must ask until the goal is confirmed before freezing.
  - The target surfaces are discoverable from existing kit docs and prior
    workflow-rule changes.

### 1.3 Questioning Decision

| Item | Decision |
| --- | --- |
| Questions needed? | No |
| No Questions Rationale | The user explicitly supplied the target repository and the desired workflow improvement: add goal confirmation to `agent-flow-kit` so ambiguous requester goals are questioned until confirmed. Existing kit evidence shows the reusable flow-plan surfaces and docs that must be updated. |
| Unsafe assumptions? | None blocking. Exact wording can follow the frozen repo-local plan and existing kit planning precision style. |

### 1.4 Goal

- Add Goal Confirmation Gate behavior to `agent-flow-kit`.
- Ensure future installed `/flow-plan` / `flow-plan` runs confirm the
  requester's desired outcome before freezing when a request is ambiguous.
- Keep Codex and Claude planning surfaces aligned.
- Preserve the no-question path for explicit or source-backed goals.

### 1.5 Scope / Non-Goals

- In scope:
  - `templates/.codex/skills/flow-plan/SKILL.md`
  - `templates/.claude/commands/flow-plan.md`
  - `templates/.claude/skills/flow-plan/SKILL.md`
  - `README.md`
  - `templates/docs/agent-flow/bug-knowledge.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
  - implementation report and validation evidence
- Possible in scope if validation shows installer/package references need it:
  - `templates/AGENTS.md`
  - `templates/CLAUDE.md`
  - `templates/scripts/agent-flow-matrix-gate.py`
- Out of scope:
  - Application runtime behavior.
  - `wellogi/yoyaku-hub` runtime code.
  - New CI enforcement that semantically proves goal quality.
  - Broad redesign of `flow-plan-review`.

### 1.6 Acceptance Criteria

- Codex `flow-plan` template includes a named Goal Confirmation Gate.
- Claude `/flow-plan` command includes the same goal-confirmation rule.
- Claude `flow-plan` skill compatibility contract mentions the same behavior.
- README explains that `flow-plan` must confirm desired outcome / user
  experience / completion signal before freeze when ambiguity exists.
- Bug-knowledge template/taxonomy includes requester-goal mismatch as a
  requirement/questioning gap.
- Agent-flow business/integration docs describe planning precision checks for
  desired outcome, root-cause target, and completion signal.
- Validation commands confirm the new wording across target surfaces.
- `git diff --check` passes.

### 1.7 User Answers

- The user stated the prior goal mismatch:
  - actual requester goal: `ログイン状態での操作で突然429によってログアウトさせないようにしたい`;
  - prior plan target: `429 エラーの表示改善`.
- The user requested that `flow-plan` explicitly ask the requester until the
  goal is confirmed when the requester goal is ambiguous.
- The user requested incorporating that improvement into `agent-flow-kit`.

## 2. Design

### 2.1 Affected Files And Modules

- `templates/.codex/skills/flow-plan/SKILL.md`
  - Add Goal Confirmation Gate as a required part of planning.
  - Update Operating Rules, Workflow, Questioning Decision Gate, required plan
    shape, and readiness checklist.
- `templates/.claude/commands/flow-plan.md`
  - Mirror the same gate in the slash-command contract.
  - Add it to intent/current-state analysis and requirement-questioning rules.
- `templates/.claude/skills/flow-plan/SKILL.md`
  - Add compatibility bullet so Claude skill inherits the same rule.
- `README.md`
  - Summarize the new gate in kit capabilities and usage guidance.
- `templates/docs/agent-flow/bug-knowledge.md`
  - Update prevention taxonomy to name desired-outcome / requester-goal
    mismatch.
- `docs/agent-flow/business-flows.md`
  - Update AFK-005 planning precision rows with desired outcome / root-cause
    target / completion signal.
- `docs/agent-flow/integration-scenarios.md`
  - Update planning precision scenario/checks.

### 2.2 Implementation Approach

1. Add `Goal Confirmation Gate` to Codex flow-plan template.
   - Required before freezing any plan.
   - Must identify observed symptom/request, desired outcome/user experience,
     root-cause target when relevant, and accepted completion signal.
   - Questions are required when these are ambiguous.
   - No-question skip is allowed only when the desired outcome is explicit in
     the prompt or unambiguously supported by source/runtime/business evidence.
2. Mirror equivalent wording in Claude `/flow-plan`.
3. Update Claude skill compatibility contract.
4. Update README and reusable docs.
5. Update bug-knowledge taxonomy.
6. Validate with targeted `rg` and `git diff --check`.

### 2.3 Design Policy And Library Selection

- No new libraries.
- Keep the change as workflow-contract text and documentation.
- Preserve existing kit style: explicit gates, concrete blockers, and concise
  no-question rationale rather than broad process overhead.

### 2.4 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| The new gate adds too much ceremony to obvious requests. | State that questions are required only when the requester goal is ambiguous; explicit goals can proceed with source-backed `No Questions Rationale`. |
| Codex and Claude templates drift. | Update Codex skill, Claude command, and Claude skill in the same implementation. |
| Natural-language goal quality cannot be fully CI-validated. | Add targeted grep validation and make plan-review responsible for semantic rejection. |
| Installer omits updated docs/templates. | Update only files already in `templates/` or top-level docs installed/distributed by the kit. |
| The rule overfits to auth/429. | Use generic examples: symptom display vs state preservation vs root-cause elimination vs deployed proof. |

### 2.5 Residual Risk Preflight

| Warning | Countermeasure |
| --- | --- |
| This is docs/skill text, but it changes future agent behavior and planning contracts. | Treat as behavior-affecting workflow work with frozen plan and validation. |
| Automated validation can confirm wording exists but cannot prove future agents ask perfect questions. | Require plan-review to inspect goal confirmation and add README/bug-knowledge guidance. |
| Prior kit changes have multiple surfaces and can diverge if one is missed. | Validate across `templates/.codex`, `templates/.claude`, README, and agent-flow docs. |

### 2.6 Runtime Causality Gate

| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | No app deployment involved. | not applicable |
| Browser symptom vs server outcome | Historical 429 incident motivates the rule, but this change edits kit workflow text. | historical context only |
| Runtime log | No runtime logs needed for workflow-template changes. | not applicable |
| Representative paths | No app/API route changes. | not applicable |
| Environment bindings | No environment or binding changes. | not applicable |
| Remote data state | No remote data changes. | not applicable |
| Schema/migration alignment | No schema changes. | not applicable |
| Classification | Workflow contract improvement for planning precision. | workflow change |

### 2.7 Bug Feedback Review

| Question | Review |
| --- | --- |
| Affected failure pattern | Requirement/questioning gap: the prior plan targeted symptom presentation while the requester expected root-cause/session-preservation behavior. |
| Prior flow miss | Existing kit `Questioning Decision` rules mention success criteria, but do not separately require confirmation of desired user experience / root-cause target when multiple interpretations exist. |
| Preventable by flow? | Yes. A Goal Confirmation Gate would require asking whether the goal is display improvement, state preservation, root-cause elimination, diagnostics, or deployed proof. |
| Flow improvement task | Add Goal Confirmation Gate to kit flow-plan templates and bug-knowledge taxonomy before implementation guidance. |

### 2.8 Flow Knowledge Update

- Update kit docs so installed projects inherit this lesson:
  - requester goal / desired outcome ambiguity is a requirement/questioning gap;
  - plans must separate observed symptom from desired outcome and completion
    signal;
  - bug/regression plans must identify whether the accepted goal is symptom
    presentation, root-cause elimination, or valid-path/deployed proof.

### 2.9 Business Flow Matrix

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-005 planning precision | Coding agent using installed kit | `flow-plan`, `/flow-plan` | Agent confirms desired outcome/user experience and completion signal before freezing | Ambiguous requester goal stops for questions | Requester owns the goal; source evidence can support but not replace unclear intent | Frozen plan; possible flow-doc updates | Plan targets message polish while requester expected root-cause behavior | Targeted grep and plan-review checklist language |
| AFK-006 plan review | Reviewing agent | `flow-plan-review` | Reviewer can reject missing goal confirmation or weak no-question rationale | Same-agent or shallow review misses intent mismatch | Review must compare prompt, plan goal, tests, and completion signal | `plan-review.md` in installed repos | Implementation proceeds from wrong goal | README/docs wording plus existing review contract |
| AFK-009 matrix/CI gate | CI/reviewer | `agent-flow-matrix-gate.py`, natural-language plan review | Structural checks still validate Questioning Decision and reviewers inspect semantic goal fit | CI cannot prove intent match | Human review remains required for natural-language goal semantics | CI pass/fail only if gate applies | False confidence from wording-only validation | `rg` validation; no code change unless needed |

### 2.10 Regression Surface Matrix

| Surface | Risk | Guardrail |
| --- | --- | --- |
| Codex flow-plan template | Codex users do not inherit Goal Confirmation Gate. | Update `templates/.codex/skills/flow-plan/SKILL.md`. |
| Claude flow-plan command/skill | Claude and Codex generate different planning contracts. | Update both Claude command and skill compatibility text. |
| README | Users do not understand why/when the gate asks questions. | Add concise capability and usage guidance. |
| Bug knowledge taxonomy | Future bug plans do not classify requester-goal mismatch. | Update `templates/docs/agent-flow/bug-knowledge.md`. |
| Agent-flow docs | Integration scenario/review expectations omit goal confirmation. | Update `docs/agent-flow/*` as kit-local project docs. |
| Matrix gate | Structural validation may not enforce new semantic rule. | Keep as reviewer responsibility unless a simple non-brittle validation is feasible. |

### 2.11 Test Design Matrix

| Test ID | Level | Target | Case | Assertion |
| --- | --- | --- | --- | --- |
| T-001 | Static grep | Codex flow-plan | Goal Confirmation Gate wording | Required gate exists and mentions desired outcome / completion signal. |
| T-002 | Static grep | Claude command | Same goal gate | Claude command contains equivalent rule. |
| T-003 | Static grep | Claude skill | Compatibility contract | Skill mentions goal confirmation behavior. |
| T-004 | Static grep | README and docs | User-facing/documented behavior | README/docs mention goal ambiguity and no-question boundary. |
| T-005 | Static grep | Bug knowledge | Prevention pattern | requester-goal / desired-outcome mismatch is classified. |
| T-006 | Diff hygiene | changed files | formatting | `git diff --check` passes. |

### 2.12 Integration Coverage Contract

| Flow | Required Coverage | Status Before Implementation | Waiver / Blocker |
| --- | --- | --- | --- |
| AFK-005 planning precision | Codex/Claude flow-plan surfaces include gate wording | Missing explicit Goal Confirmation Gate | No waiver. |
| AFK-006 plan review | README/docs make semantic review target clear | Existing review gate, but no explicit goal-confirmation review language | No waiver if docs are updated. |
| AFK-009 matrix/CI gate | Structural gate remains compatible | Existing `Questioning Decision` validation | Semantic enforcement waived because natural-language goal fit requires review; targeted wording validation is required. |
| Runtime app behavior | Runtime/browser tests | Not applicable | Concrete reason: kit workflow docs/templates only, no app runtime. |

### 2.13 Playwright Integration Test Plan

- Playwright evidence is not required.
- Concrete reason: this change affects Agent Flow workflow templates and docs,
  not a visible application UI or browser route.

### 2.14 Migration / Runtime Enforcement

- No schema, migration, Worker, Pages, database, or external provider runtime
  changes.

### 2.15 Open Questions

- None blocking.
- If implementation finds generated install output or package manifest changes
  are required, keep them within the same kit-distribution scope and document
  why.

## 3. Tasks

- [x] TASK-001 Update `templates/.codex/skills/flow-plan/SKILL.md` with Goal Confirmation Gate.
- [x] TASK-002 Update `templates/.claude/commands/flow-plan.md` with equivalent Goal Confirmation Gate.
- [x] TASK-003 Update `templates/.claude/skills/flow-plan/SKILL.md` compatibility contract.
- [x] TASK-004 Update README and reusable agent-flow docs with goal-confirmation guidance.
- [x] TASK-005 Update bug-knowledge taxonomy with requester-goal mismatch.
- [x] TASK-006 Run targeted `rg` validation across templates/docs.
- [x] TASK-007 Run `git diff --check`.
- [x] TASK-008 Create implementation report.

## 4. Readiness

- [x] Requirements map to tasks
- [x] User intent and current-state analysis is documented
- [x] Questioning Decision is documented
- [x] No Questions Rationale is source-backed when no questions were asked
- [x] Business/product ambiguity has been resolved or explicitly blocked
- [x] Required onboarding docs exist for behavior-changing workflow work
- [x] Flow Knowledge Update target is explicit
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
- [x] Runtime Causality Gate is complete or explicitly not triggered
- [x] Onboarding/UI plan fields are not applicable because this is workflow-template text only
- [x] Provider/auth/deploy lanes are used only as examples and do not require runtime evidence
- [x] Schema plan records no migration/runtime change
- [x] Bug/regression plan classifies matching bug-knowledge patterns
- [x] Business flows map to required tests or blockers
- [x] Integration Coverage Contract has concrete coverage or waivers
- [x] Validation commands are identified

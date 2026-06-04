# Flow Plan Review High Impact Only

## 1. Requirements

### 1.1 Current State

`flow-plan-review` is currently required for all behavior-changing work. The
README, `templates/AGENTS.md`, `templates/CLAUDE.md`, the Claude/Codex review
templates, and `templates/scripts/agent-flow-matrix-gate.py` all treat an
approved `docs/flow/{feature_name}/plan-review.md` as a gate before
implementation for behavior-affecting changes.

### 1.2 Intent And Ambiguity Resolution

The requester asked whether `flow-plan-review` is currently mandatory and said
they want it to be optional except for large-scale or high-impact changes. The
desired policy is clear enough to proceed: keep the review available and
recommended, but require it only when the change has a large blast radius or
touches high-risk surfaces.

### 1.3 Goal

Change Agent Flow Kit so normal behavior-changing work can proceed from a
frozen `flow-plan` without a mandatory `flow-plan-review`, while high-impact
work still requires an approved current review artifact.

### 1.4 Scope / Non-Goals

In scope:

- Update user-facing README guidance and installed `AGENTS.md` / `CLAUDE.md`
  templates.
- Update Claude and Codex `flow-plan-review` templates.
- Update planning templates to require an explicit plan-review requirement
  decision.
- Update matrix-gate enforcement so review is required only for high-impact
  changes or when the plan marks review as required.
- Update Agent Flow docs that describe AFK-006 and matrix-gate coverage.

Out of scope:

- Removing `flow-plan` as the default behavior-changing entrypoint.
- Removing cross-agent review support.
- Building a full test harness around every matrix-gate scenario.

### 1.5 Acceptance Criteria

- The answer to the current-state question is documented: review is no longer
  universally mandatory for every behavior-changing change after this update.
- High-impact criteria are explicit and conservative.
- Plans must record whether review is `Required` or `Optional`, with a reason.
- Matrix gate requires `plan-review.md` only when review is required by the
  plan or by configured high-impact paths.
- Documentation and Claude/Codex templates use the same policy.

### 1.6 User Answers

- Requirement questions asked: No.
- User answers: The user explicitly requested that `flow-plan-review` be
  optional except for large-scale or high-impact changes.
- No Questions Rationale: The requester named the exact workflow gate and the
  desired required/optional boundary; repository docs and gate script identify
  the affected surfaces.

## 2. Design

### 2.1 Affected Files And Modules

- `README.md`
- `templates/AGENTS.md`
- `templates/CLAUDE.md`
- `templates/.codex/skills/flow-plan/SKILL.md`
- `templates/.claude/skills/flow-plan/SKILL.md`
- `templates/.claude/commands/flow-plan.md`
- `templates/.codex/skills/flow-plan-review/SKILL.md`
- `templates/.claude/skills/flow-plan-review/SKILL.md`
- `templates/.claude/commands/flow-plan-review.md`
- `templates/.agent-flow/config.json`
- `templates/scripts/agent-flow-matrix-gate.py`
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`

### 2.2 Implementation Approach

Add a new `Plan Review Requirement` decision to behavior-changing plans:

- `Requirement: Required` for large-scale or high-impact changes.
- `Requirement: Optional` for smaller, localized behavior changes where the
  plan explains why cross-agent review is not mandatory.

Define high-impact review triggers in docs and config:

- Multiple business flows, modules, apps, packages, or teams are affected.
- Auth, permission, tenant, ownership, session, security, or privacy changes.
- Schema, migrations, data compatibility, backfill, rollback, destructive data,
  or runtime-enforced data contracts are affected.
- Deploy, CI, install behavior, workflow gates, hooks, risky-path config, or
  Agent Flow contracts change.
- External providers, webhooks, mail/PDF, storage, search/cache, queues, jobs,
  schedules, or other side effects are affected.
- Public API contracts or shared runtime entrypoints are affected.
- The plan author, user, or reviewer marks the change as high-impact or
  uncertain enough to need cross-agent review.

Update the matrix gate so it:

1. Still requires a frozen plan and matrices for behavior-affecting changes.
2. Requires a `Plan Review Requirement` section in changed plans.
3. Requires review only when the plan says `Required` or when changed files
   match configurable `plan_review_required_*` paths.
4. Rejects a plan that marks review optional while high-impact paths are
   changed.

### 2.3 Design Policy And Library Selection

Use the existing standard-library Python script and config pattern. Do not add
dependencies.

### 2.4 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Small changes lose useful review feedback | Keep review recommended and manually invokable. |
| High-impact work is misclassified as optional | Add explicit criteria, config defaults, and gate rejection for configured high-impact paths. |
| Existing docs diverge between Claude and Codex | Update README, AGENTS, CLAUDE, slash command, and both skill templates together. |
| Matrix gate becomes too strict for old plans | Require the new decision only for changed behavior-affecting plans checked by the updated gate. |

### 2.5 Residual Risk Preflight

| Residual risk | Countermeasure / blocker |
| --- | --- |
| Natural-language impact classification cannot be fully automated. | Use configurable high-impact path detection plus a required plan decision and reason. |
| Target repositories may need custom high-impact paths. | Add config keys in `.agent-flow/config.json` and document that defaults are conservative starting points. |

### 2.6 Bug Feedback Review

Not a bug/regression request. No prior runtime failure is being classified.

### 2.7 Flow Knowledge Update

Update AFK-006 and AFK-009 in `docs/agent-flow/business-flows.md`,
`docs/agent-flow/project-structure.md`, and
`docs/agent-flow/integration-scenarios.md` to record the new optional-by-default
review policy for non-high-impact behavior changes.

### 2.8 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-005 | Coding agent planning behavior-changing work | `flow-plan` | Agent writes frozen plan, including review requirement decision | Missing decision or vague optional reason | High-impact work must not be classified as optional | Writes `docs/flow/{feature}/plan.md` | Implementation proceeds without review for a high-impact change | Static documentation review plus matrix-gate smoke |
| AFK-006 | Reviewing agent | `flow-plan-review` | Review is run for high-impact work or when requested | Review skipped for work that should be high-impact | Same-agent fallback still requires concrete reason when review runs | Writes `plan-review.md` only when triggered | Process drag if review stays mandatory for all changes; missed risk if high-impact work skips review | Template review plus matrix-gate high-impact/optional checks |
| AFK-009 | CI / reviewer | `agent-flow-matrix-gate.py` | Gate validates plan matrices and review requirement decision; requires review only for required cases | Missing review decision, stale review, optional marker on configured high-impact paths | Config can tune high-impact paths | CI pass/fail | False positives or false negatives in path detection | Python syntax plus targeted temporary git fixtures |

### 2.9 Regression Surface Matrix

| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| README / installed guidance | AFK-005, AFK-006 | `README.md`, `templates/AGENTS.md`, `templates/CLAUDE.md` | Grep/documentation review for consistent required/optional boundary |
| Planning templates | AFK-005 | `flow-plan` command and skills | Grep review for `Plan Review Requirement` output contract |
| Plan review templates | AFK-006 | `flow-plan-review` command and skills | Grep review for high-impact-only required policy |
| Matrix gate | AFK-009 | `templates/scripts/agent-flow-matrix-gate.py` | `py_compile` and temporary git fixture checks |
| Config defaults | AFK-009 | `templates/.agent-flow/config.json` | JSON parse and fixture checks using high-impact path defaults |

### 2.10 Test Design Matrix

| Test ID | Level | Target | Scenario | Expected result |
| --- | --- | --- | --- | --- |
| TEST-001 | Syntax | Python gate script | Run `python3 -m py_compile` | Script parses |
| TEST-002 | Static grep | Docs/templates | Search for stale universal mandatory wording | No stale behavior-changing-universal review requirement remains |
| TEST-003 | Fixture | Matrix gate optional review | Behavior-affecting app change plus frozen plan with `Requirement: Optional` and no review | Gate passes |
| TEST-004 | Fixture | Matrix gate high-impact path | Migration/schema/config style high-impact change plus plan with `Requirement: Optional` and no review | Gate fails and asks for required review |
| TEST-005 | Fixture | Matrix gate required review | High-impact change plus approved current `plan-review.md` | Gate passes |

### 2.11 Integration Coverage Contract

| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-005 | Plan template review for review requirement decision | Happy, exception, boundary, regression | None; static template review is enough because this is an agent-doc workflow |
| AFK-006 | Plan-review template review and same-agent fallback policy | Happy, exception, boundary, regression | Cross-agent execution is blocked in this Codex desktop session; same-agent review artifact records the blocker |
| AFK-009 | Matrix-gate syntax and fixture smoke for optional vs required review | Happy, exception, boundary, side effect, regression | None for gate logic changes |

### 2.12 Plan Review Requirement

- Requirement: Required.
- Reason: This change modifies Agent Flow workflow gates, review policy,
  matrix-gate behavior, and installed templates, which is explicitly
  high-impact under the new policy.
- Triggered criteria: workflow gates, review policy, CI gate behavior, installed
  agent contracts.

### 2.13 Playwright Integration Test Plan

No Playwright evidence is required because this repository change has no visible
browser workflow.

### 2.14 Migration / Runtime Enforcement

- Migration / Runtime Enforcement: No schema migration.
- Migration enforcement path: Not applicable because no database schema changes.
- Runtime validation command: `python3 -m py_compile ...` and targeted
  matrix-gate fixture commands.

### 2.15 Open Questions

None.

## 3. Tasks

- [x] TASK-001 Update README and installed entrypoint guidance.
- [x] TASK-002 Update flow-plan and flow-plan-review templates.
- [x] TASK-003 Update `.agent-flow/config.json` and matrix-gate enforcement.
- [x] TASK-004 Update Agent Flow docs for AFK-006/AFK-009.
- [x] TASK-005 Run syntax, grep, and matrix-gate fixture checks.

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

<!-- frozen: v1 2026-06-04 by Codex -->
<!-- plan_author: codex -->

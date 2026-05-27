# Agent Flow Hardening Plan

<!-- frozen: v1 2026-05-27 -->

## 1. Requirements

### 1.1 Goal

Create a transferable agent workflow for medium-sized projects that fits GPT-5.5+ style reasoning, supports team operation, and prevents implementation regressions caused by missing business-flow context.

### 1.2 Scope

In scope:

- Align Claude/Codex rules with transferable project-specific defaults.
- Make planning require business-flow impact analysis.
- Make TDD start from Red tests and integration coverage for affected workflows.
- Make Claude and Codex share the same repo-local quality gate hooks.
- Track selected workflow contract files through `.gitignore` exceptions.
- Split `/flow-start` and `/flow-plan` by use case.
- Make `team-review` the required review gate for behavior-changing work.
- Add CI matrix enforcement for behavior-affecting PRs.
- Remove legacy project-local `kairo-*` commands and `sdd-*` skills.
- Add a Playwright integration-test evidence gate with screenshots, `index.html`, test review, and business-flow impact review.
- Evaluate Webwright and decide whether it should replace or augment Playwright in the integration-test gate.
- Document remaining blockers and judgment items.

Out of scope:

- Application feature implementation.
- Full cleanup of legacy `.docs/` contents.
- Rewriting all older TDD helper command templates.

### 1.3 Acceptance Criteria

- [ ] Project-specific commands replace Python/uv-only defaults in active development rules.
- [ ] Plans require Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, and Integration Coverage Contract.
- [ ] Implementation flow stops before coding when required matrices or coverage contract are missing.
- [ ] Claude and Codex both invoke the integration-test quality gate from repo-local files.
- [ ] Codex has a native `team-implement` skill for frozen plan execution.
- [ ] Workflow contract files are no longer hidden by `.gitignore`.
- [ ] `/flow-plan` is mandatory for modifications; `/flow-start` is reserved for new-feature discovery.
- [ ] `team-review` is mandatory for behavior-changing work.
- [ ] CI rejects behavior-affecting PRs without frozen plan matrices.
- [ ] Project-local `kairo-*` commands and `sdd-*` skills are removed.
- [ ] Visible/multi-step workflows require Playwright integration evidence before final review.
- [ ] Webwright replacement decision is documented.
- [ ] Remaining blockers and judgment items are documented.

## 2. Design

### 2.1 Recommended Workflow

```text
Investigation
  -> Requirements/design with user questions
  -> Business Flow Matrix
  -> Regression Surface Matrix
  -> Test Design Matrix
  -> Integration Coverage Contract
  -> Red tests
  -> Green implementation
  -> Refactor
  -> Unit/Feature/browser/migration verification
  -> Playwright integration evidence
  -> Test review and business-flow impact review
  -> Review
```

### 2.2 Business Flow Matrix

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Planning workflow | Agent/operator | `/flow-plan`, `/flow-start` | Requirements/tasks are mapped to business flows before freeze | Missing business context blocks freeze | Out-of-scope or low-risk paths require explicit waiver | Plan artifacts and CI gate update | Related routes/screens/mail/PDF/jobs can be missed | Plan readiness gate |
| Implementation workflow | Agent/operator | `/flow-impl`, `/team-implement` | Red tests and coverage contract exist before Green implementation | Missing test design blocks coding | Required cases need evidence or explicit waiver | Implementation report update | Unit-only completion hides integration regressions | Implementation gate + report |
| Review workflow | Agent/operator | `team-review`, `/review` | `team-review` compares implementation to matrices and coverage contract | Missing review evidence blocks merge/release | Docs/config-only changes can use low-risk waiver | Review reports | Single-pass review can miss indirect regression/test gaps | Team review matrix comparison |
| Claude/Codex hook workflow | Agent/operator | `.claude/settings.json`, `.codex/hooks.json` | Both tools call shared repo-local integration gate | Invalid hook config fails validation | Missing hook files are rejected during install/compile checks | Hook logs/config updates | Team transfer breaks or one tool misses the gate | JSON validation + hook compile |
| CI workflow | CI/operator | `.github/workflows/agent-flow-matrix.yml` | Risky runtime paths require a frozen plan with matrices and Integration Coverage Contract | Missing plan markers fail CI | Browser-visible changes require Playwright Integration Test Plan | Obsolete workflow files must not exist | Team members merge without planning evidence | CI matrix gate script |
| Integration-test workflow | Agent/operator | `/flow-integration-test` | Playwright scenarios save screenshots, `index.html`, and test/business-flow reviews | Blocked browser execution records `BLOCKED`, not `PASS` | Feature/API integration covers server-only paths | Evidence artifacts | Visual or multi-step regressions pass without evidence | Evidence gate before final review |
| Webwright evaluation | Agent/operator | Long browser flows | Use Webwright-style exploratory Playwright scripts before deterministic specs | Exploratory failures inform spec design | Autonomous success cannot replace assertions | Playwright specs/reports | Autonomous web-agent success is not deterministic CI pass/fail | Playwright Test remains the gate |

### 2.3 Regression Surface Matrix

| Surface | Current risk | Hardening action |
| --- | --- | --- |
| Active rules | Some files were Python/uv-oriented despite transferable repo targets | Replace active dev/testing/TDD rules with project-specific verification guidance |
| Planning artifact | Plan template lacked required business-flow/test matrices and coverage contract | Add required matrices, Integration Coverage Contract, and readiness checks |
| Implementation artifact | Implementation flow did not stop when matrices or coverage contract were missing | Add pre-code gate to `/flow-impl` and `team-implement` |
| Codex repo-local hooks | `.codex/hooks.json` referenced missing `.codex/hooks/*.py` files and absolute local paths | Route Codex hooks to shared `.claude/hooks/*.py` with relative paths |
| Model naming | Several prompts referenced older `gpt-5.4` examples | Move examples toward `gpt-5.5-codex` |
| Workflow tracking | `.claude/`, `.codex/`, and flow plans were ignored as local artifacts | Unignore only selected workflow contract files while keeping logs/caches local |
| Review enforcement | `team-review` and `/review` had no clear required/optional boundary | Require `team-review` for behavior-changing work and keep `/review` as a supplemental fast pass |
| PR enforcement | Hooks could guide but not enforce matrix completion | Add CI gate for frozen plan matrices on risky path changes |
| Legacy workflow removal | Old `kairo-*` commands and `sdd-*` skills could continue to confuse agents | Remove project-local files and fail the CI gate if they are reintroduced |
| Playwright evidence | Browser checks were easy to report but hard to inspect later | Save screenshots, result summary, test review, and business-flow impact review under `docs/flow/{feature}/integration-test/{run_id}/` |
| Webwright-style crafting | Step-by-step browser driving can be token-heavy on long flows | Let the agent write reusable exploratory Playwright scripts first, then convert stable behavior to deterministic specs |

### 2.4 Test Design Matrix

| Test ID | Level | Target | Scenario | Expected result | Covers flow/risk |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Static validation | `.claude/settings.json`, `.codex/hooks.json` | Parse hook configuration as JSON | Valid JSON | Hook portability |
| TEST-002 | Static validation | `.claude/hooks/*.py`, `.codex/hooks/*.py` | Compile Python hook scripts | No syntax errors | Hook runtime safety |
| TEST-003 | Static validation | workflow docs | Search for stale active `gpt-5.4` and `uv run pytest` guidance | No stale guidance in active core flow files | GPT-5.5+ and project-specific command alignment |
| TEST-004 | CI/local static validation | `scripts/agent-flow-matrix-gate.py` | Run matrix gate against current working tree | Workflow-only changes pass; risky changes would require frozen matrices | CI enforcement |
| TEST-005 | Static validation | integration-test workflow docs | Verify `/flow-plan`, `/flow-impl`, testing rules, and Codex skill reference the Playwright evidence gate | Integration-test gate is reachable from the canonical flow | Evidence workflow |

### 2.5 Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| Planning workflow | Static validation + plan readiness | Happy, missing matrix, missing coverage contract | N/A |
| Implementation workflow | Static validation + implementation gate | Happy, missing Red tests, missing integration coverage | N/A |
| CI workflow | Matrix gate script | Happy, missing plan marker, browser-visible missing Playwright plan | N/A |

### 2.6 Remaining Blockers

- Legacy `.docs/` still contains stale issue/architecture notes with old line numbers. This can confuse agents during broad research.
- Browser verification still depends on available MCP/browser tooling and a running local stack.
- CI enforcement depends on the risky path list in `scripts/agent-flow-matrix-gate.py`; add new runtime entrypoints there when the app grows.
- Project-specific test commands still need confirmation during onboarding before this workflow is copied to another repository.
- Generated Playwright evidence is intentionally ignored by git; upload it as a CI artifact if team retention is required.

### 2.7 Judgment Items

- Resolved: `/flow-plan` is mandatory for modifications and business-flow-sensitive work; `/flow-start` remains for new-feature discovery.
- Resolved: `team-review` is mandatory for behavior-changing work; `/review` is supplemental.
- Resolved: project-local `kairo-*` commands and `sdd-*` skills are abolished; canonical replacements are `/flow-plan` and `/flow-impl`.
- Resolved: visible/multi-step workflows require `/flow-integration-test` before final review.
- Resolved: Webwright is not a full replacement for Playwright Test; use Webwright-style crafting for long browser scenarios when it saves agent turns.
- Decide whether `.docs/` should be archived/removed after consolidating still-current content into `docs/`.
- Resolved: CI enforces plan matrices and Integration Coverage Contract for behavior-affecting PRs.
- Decide whether model names should be hardcoded (`gpt-5.5-codex`) or left as a local alias such as `CODEX_DEEP_MODEL`.

## 3. Tasks

- [x] TASK-001: Align active development/testing/TDD rules with project-specific defaults.
- [x] TASK-002: Add business-flow and regression-surface gates to plan/implementation workflows.
- [x] TASK-003: Make Claude/Codex use shared repo-local integration quality gate.
- [x] TASK-004: Add Codex-native `team-implement` skill.
- [x] TASK-005: Add `.gitignore` exceptions for selected workflow contract files.
- [x] TASK-006: Decide and document `/flow-start` vs `/flow-plan` usage.
- [x] TASK-007: Decide and document `team-review` vs `/review` usage.
- [x] TASK-008: Add CI matrix gate for behavior-affecting PRs.
- [x] TASK-009: Remove legacy project-local `kairo-*` commands and `sdd-*` skills.
- [x] TASK-010: Add Playwright integration-test evidence gate.
- [x] TASK-011: Evaluate Webwright and document the hybrid decision.
- [x] TASK-012: Record remaining blockers and judgment items.

## 4. Readiness

- [x] Requirements map to tasks.
- [x] Validation commands are identified.
- [x] Risks and assumptions are documented.
- [x] Business flows map to test/verification obligations.
- [x] Integration Coverage Contract maps required cases to evidence or waivers.
- [x] Remaining blockers are explicit.

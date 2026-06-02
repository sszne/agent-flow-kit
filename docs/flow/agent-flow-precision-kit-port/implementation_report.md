# Agent Flow Precision Kit Port Implementation Report

## Summary

Ported the portable parts of the recent Agent Flow precision hardening into
Agent Flow Kit templates and kit-owned documentation.

The change strengthens future installed workflows by requiring:

- explicit `Questioning Decision` and source-backed `No Questions Rationale`;
- onboarding/UI precision checks for step names, order, exclusions, action
  placement, resume/fallback paths, and blocked evidence lanes;
- provider/auth/deploy evidence lanes that separate local mocks from deployed
  artifacts, real provider/device paths, valid credential/session paths, and
  blockers;
- bug/regression prevention pattern classification before task design;
- testing-rule wording that prevents shallow checks from replacing valid-path
  or side-effect evidence.

## Plan And Review

- Plan: `docs/flow/agent-flow-precision-kit-port/plan.md`
- Frozen marker: `<!-- frozen: v1 2026-06-02 -->`
- Plan review: `docs/flow/agent-flow-precision-kit-port/plan-review.md`
- Review status: `APPROVED`
- Same-agent fallback: used because Claude Code review was not callable in this
  Codex desktop session.

## Completed Tasks

| Task | Status | Notes |
| --- | --- | --- |
| TASK-001 Update Codex `flow-plan` template | Done | Added explicit questioning, onboarding/UI, provider/auth/deploy, and bug-knowledge reuse rules. |
| TASK-002 Update Claude `/flow-plan` command | Done | Mirrored the same precision rules, template guidance, and readiness checks. |
| TASK-003 Update Claude `flow-plan` skill | Done | Added compatibility bullets for the shared behavior. |
| TASK-004 Add bug prevention taxonomy | Done | Added `Prevention Pattern Taxonomy` to `templates/docs/agent-flow/bug-knowledge.md`. |
| TASK-005 Update testing rules | Done | Added provider/deploy happy-path evidence lane principle and checklist item. |
| TASK-006 Update kit Agent Flow docs | Done | Updated AFK planning precision in `business-flows.md` and `integration-scenarios.md`. |
| TASK-007 Update README | Done | Added concise install/user-facing guidance for the new precision guarantees. |
| TASK-008 Create report and mark completion | Done | This report records implementation scope and validation. |
| TASK-009 Run validation | Done | Static, syntax, and installer dry-run checks passed. |

## Files Changed

- `README.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `templates/.codex/skills/flow-plan/SKILL.md`
- `templates/.claude/commands/flow-plan.md`
- `templates/.claude/skills/flow-plan/SKILL.md`
- `templates/.claude/rules/testing.md`
- `templates/docs/agent-flow/bug-knowledge.md`
- `docs/flow/agent-flow-precision-kit-port/plan.md`
- `docs/flow/agent-flow-precision-kit-port/plan-review.md`
- `docs/flow/agent-flow-precision-kit-port/implementation_report.md`

## Validation

| Test ID | Command | Result |
| --- | --- | --- |
| TEST-001 | `rg -n "Questioning Decision\|No Questions Rationale" templates/.codex/skills/flow-plan/SKILL.md templates/.claude/commands/flow-plan.md templates/.claude/skills/flow-plan/SKILL.md README.md docs/flow/agent-flow-precision-kit-port/plan.md` | Pass |
| TEST-002 | `rg -n "step names\|step order\|excluded elements\|action placement\|resume/fallback\|blocked evidence lanes\|onboarding/UI" templates/.codex/skills/flow-plan/SKILL.md templates/.claude/commands/flow-plan.md templates/.claude/skills/flow-plan/SKILL.md README.md docs/agent-flow/business-flows.md docs/agent-flow/integration-scenarios.md docs/flow/agent-flow-precision-kit-port/plan.md` | Pass |
| TEST-003 | `rg -n "local mock\|deployed artifact\|deployed-artifact\|real provider\|provider/device\|valid credential\|valid credential/session\|valid session\|concrete blocker\|shallow checks\|provider/auth/deploy" templates/.codex/skills/flow-plan/SKILL.md templates/.claude/commands/flow-plan.md templates/.claude/skills/flow-plan/SKILL.md templates/.claude/rules/testing.md README.md docs/agent-flow/business-flows.md docs/agent-flow/integration-scenarios.md docs/flow/agent-flow-precision-kit-port/plan.md` | Pass |
| TEST-004 | `rg -n "Prevention Pattern Taxonomy\|prevention pattern\|Requirement/questioning gap\|Valid-path coverage gap\|Runtime/deploy/provider evidence gap\|UI-intent\|implementation drift\|Bug Knowledge Pattern Reuse" templates/docs/agent-flow/bug-knowledge.md templates/.codex/skills/flow-plan/SKILL.md templates/.claude/commands/flow-plan.md templates/.claude/skills/flow-plan/SKILL.md docs/flow/agent-flow-precision-kit-port/plan.md` | Pass |
| TEST-005 | `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py` | Pass |
| TEST-006 | `mkdir -p /tmp/agent-flow-kit-precision-smoke`, `git init /tmp/agent-flow-kit-precision-smoke`, then `python3 install.py --target /tmp/agent-flow-kit-precision-smoke --dry-run` | Pass |
| TEST-007 | `git diff --check -- README.md templates/.codex/skills/flow-plan/SKILL.md templates/.claude/commands/flow-plan.md templates/.claude/skills/flow-plan/SKILL.md templates/.claude/rules/testing.md templates/docs/agent-flow/bug-knowledge.md docs/agent-flow/business-flows.md docs/agent-flow/integration-scenarios.md docs/flow/agent-flow-precision-kit-port/plan.md docs/flow/agent-flow-precision-kit-port/plan-review.md` | Pass |

Initial installer dry-run attempts against a missing directory and then a
non-git directory failed as expected. The final dry-run passed after preparing a
git target repository.

## Integration Evidence

No Playwright or browser evidence was required. This change affects workflow
templates and Markdown documentation only.

## Scope Notes

The pre-existing untracked `docs/flow/authenticated-todo-list/` directory was
left untouched.

## Follow-up Refinement

Added a plan-review scope boundary after user feedback: clearly non-behavioral
typo fixes, formatting-only edits, and docs-only changes do not require
`flow-plan-review` when they do not alter workflow contracts, runtime behavior,
test expectations, install behavior, CI gates, or user-facing behavior.
Docs-only changes that update Agent Flow rules, skill behavior, gates, review
policy, risky-path config, or required evidence still require review.

## Remaining Risks

- No automated semantic test can prove natural-language plan completeness.
  Matrix-gate checks and plan-review remain the enforcement layer.
- The review used a same-agent fallback because cross-agent review was not
  callable in this session.

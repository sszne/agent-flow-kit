# Agent Flow Kit

This repository uses Agent Flow Kit for plan-first implementation, regression
control, and browser/integration evidence.

## Context First

Before non-trivial repository work, read:

- `CLAUDE.md` first when working as Claude
- `AGENTS.md` when Codex or cross-agent behavior may matter
- `.claude/rules/*.md`
- `.claude/docs/DESIGN.md`
- `docs/agent-flow/project-structure.md`
- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- relevant `docs/flow/{feature_name}/` artifacts

If behavior-changing work starts before the onboarding docs exist, run
`agent-flow-onboarding` first or record the blocker.

Treat `.claude/` as shared Agent Flow documentation. Load only the rules and
docs relevant to the current task, and avoid importing tool-delegation or
package-manager assumptions when they conflict with the active agent,
repository evidence, or direct user instruction.

## Main Flow

```text
agent-flow-onboarding
  -> /flow-start or /flow-plan
  -> /flow-plan-review
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
```

Use `/flow-plan` for existing behavior changes, bug fixes, regressions,
refactors, auth/schema/status/order/search/mail/PDF/job changes, and
business-flow-sensitive work.

Do not require `/flow-plan` when the requested change is display-only and is
limited to minor style changes, layout adjustments, or visible text changes. If
the same request touches runtime behavior, data flow, permissions, API behavior,
workflow order, validation, side effects, tests, install behavior, CI gates, or
Agent Flow contracts, keep `/flow-plan` required.

Use `/flow-start` only for new-feature discovery or greenfield scope shaping.
If discovery touches an existing runtime path, switch to `/flow-plan`.

Codex uses the same workflow names as skills: `flow-plan`, `flow-plan-review`,
`flow-impl`, and `flow-integration-test`. Both tools write the same artifacts under
`docs/flow/{feature_name}/`.

## Quality Gates

Behavior-changing plans need:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- approved `docs/flow/{feature_name}/plan-review.md` for the current frozen plan
- concrete waivers or blockers for uncovered coverage

Implementation should stay inside the frozen plan. If a new behavior or design
choice appears, update the plan or ask the user before proceeding.

Run `/flow-plan-review` after the plan is frozen and before implementation. Use
cross-agent review by default: Claude Code-created plans are reviewed by Codex,
and Codex-created plans are reviewed by Claude Code. A same-agent review must
record a concrete fallback reason or blocker in `plan-review.md`.

Do not require `/flow-plan-review` for clearly non-behavioral work such as typo
fixes, formatting-only edits, or docs-only changes that do not alter workflow
contracts, runtime behavior, test expectations, install behavior, CI gates, or
user-facing behavior. If a docs-only change updates Agent Flow rules, skill
behavior, gates, review policy, risky-path config, or required evidence, treat
it as behavior-changing workflow work and keep the review gate.

Visible or multi-step business workflows require Playwright integration evidence
with screenshots, `index.html`, test review, and business-flow impact review.

## Documentation

When `/flow-plan` uncovers reusable business-flow, permission, exception,
side-effect, or integration-scenario knowledge, update:

- `docs/agent-flow/business-flows.md`
- `docs/agent-flow/integration-scenarios.md`
- `docs/agent-flow/bug-knowledge.md` when the knowledge comes from a bug that
  cannot be fully prevented by flow improvements

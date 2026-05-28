# Agent Flow Hardening

## Purpose

This document records the intended transferable agent workflow for this repository and future medium-sized projects.

## Canonical Feature Workflow

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
  -> Bug feedback loop for regressions
  -> Review
```

## Required Planning Gates

Behavior-changing work must not proceed to implementation until the plan includes:

- Business Flow Matrix
- Regression Surface Matrix
- Test Design Matrix
- Integration Coverage Contract
- Migration/runtime enforcement notes when schema changes exist
- Browser verification plan when visible behavior changes
- Playwright Integration Test Plan when visible behavior or multi-step business workflows change

## Business Flow Matrix

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {flow} | {role/scope} | {route/screen/API/job/mail/PDF} | {happy workflow} | {validation/missing/external failure} | {forbidden/cross-scope/null/min/max} | {mail/PDF/export/job/cache/search} | {what could regress} | {Feature/API integration, Unit, Browser, Migration, Manual with reason} |

## Regression Surface Matrix

| Surface | Affected? | Evidence | Required verification |
| --- | --- | --- | --- |
| Routes/controllers | Yes/No | {files/routes inspected} | {Feature test/manual check/N/A} |
| Screens/Blade/JS | Yes/No | {views/scripts inspected} | {Browser check/N/A} |
| API/Ajax flows | Yes/No | {endpoints inspected} | {Feature/browser check/N/A} |
| Shared partials/scripts/services/actions | Yes/No | {shared implementation inspected} | {Regression test/N/A} |
| Schema/migrations | Yes/No | {migrations/deploy path inspected} | {php artisan migrate/enforcement check/N/A} |
| Jobs/schedules | Yes/No | {commands/jobs inspected} | {Feature/command test/N/A} |
| Mail/PDF/export | Yes/No | {templates/services inspected} | {render/assertion/manual check/N/A} |
| Auth/permissions | Yes/No | {middleware/policies inspected} | {Feature/browser check/N/A} |

## Test Design Matrix

| Test ID | Level | Target | Scenario | Expected result | Covers flow/risk |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Feature | {test file} | {scenario} | {expected result} | {flow/risk} |
| TEST-002 | Browser | {screen} | {scenario} | {expected result} | {flow/risk} |

## Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| {flow} | {Feature/API integration + Unit + Browser/Migration as needed} | {Happy, validation, permission, missing relation, boundary, side effect, regression} | {N/A or concrete reason} |

## Playwright Integration Test Plan

| Scenario ID | Business flow | Entry point | Major steps requiring screenshots | Expected result | Risk covered |
| --- | --- | --- | --- | --- | --- |
| PW-001 | {flow} | {URL/modal/state} | {step names} | {expected browser-visible state} | {risk} |

Evidence is generated under:

```text
docs/flow/{feature_name}/integration-test/{run_id}/
  index.html
  result.md
  test-review.md
  business-flow-impact.md
  screenshots/
```

## Implemented Hardening

- Active testing rules now use project-specific TDD, Feature/API integration, browser, and migration verification instead of generic Python-only defaults.
- `.gitignore` now tracks selected workflow contract files under `.claude/`, `.codex/`, and `docs/flow/**/plan.md` while leaving local logs/caches ignored.
- `/flow-start` is positioned for new-feature discovery and greenfield feature slices.
- `/flow-plan` is positioned as the canonical entry point for modifications, bug fixes, regressions, and business-flow-sensitive work.
- `agent-router.py` biases risky prompts to `/flow-plan` even when the user does not explicitly type `/flow-plan`.
- `flow-plan-required-gate.py` blocks behavior-affecting edits until a frozen `docs/flow/{feature}/plan.md` exists.
- `/flow-plan` requires business-flow, regression-surface, test-design matrices, and an Integration Coverage Contract.
- `/flow-plan` includes Flow Knowledge Update so newly confirmed reusable business-flow and integration-scenario knowledge is written back to `docs/agent-flow/*` instead of staying only in a feature plan.
- `/flow-impl` stops before coding if required matrices or the Integration Coverage Contract are missing.
- `/flow-impl` can omit arguments after `/flow-plan`; it resolves the latest `docs/flow/*/plan.md` as the implementation target.
- Claude and Codex hook configuration both call the shared repo-local integration-test quality gate.
- Codex has a native `team-implement` skill for frozen plan execution.
- `team-review` is now the required review gate for behavior-changing work; `/review` is supplemental for small low-risk checks.
- CI includes `agent-flow-matrix.yml`, which blocks behavior-affecting PRs unless a frozen `docs/flow/{feature}/plan.md` contains the required matrices and Integration Coverage Contract. Browser-visible file changes also require a Playwright Integration Test Plan.
- Legacy project-local `kairo-*` commands and `sdd-*` skills have been removed. References now point to `/flow-plan` and `/flow-impl`, and the CI gate fails if those files are reintroduced.
- `/flow-integration-test` defines the Playwright evidence gate: major-step screenshots, `index.html`, test review, and business-flow impact review must pass before final review.
- `/flow-plan` includes a Bug Feedback Review for bug reports and regressions. When a previous plan exists, the agent classifies the failed flow step and updates project-specific flow docs when possible. Non-preventable bugs are appended to `docs/agent-flow/bug-knowledge.md`.
- Webwright was evaluated as a replacement candidate. The workflow keeps Playwright Test as the deterministic gate and adopts Webwright-style code-as-action only for crafting long browser scenarios before converting them into Playwright specs.

## Entrypoint Decision

| Entry point | Required use | Strength | Weakness | Decision |
| --- | --- | --- | --- | --- |
| `/flow-start` | New features, greenfield slices, ambiguous product exploration | Good at broad discovery and parallel codebase mapping | Can over-expand scope for focused modifications | Keep as discovery/kickoff only |
| `/flow-plan` | Existing behavior changes, bug fixes, regressions, refactors, business-flow-sensitive work | Stronger requirement/design/test traceability and readiness gate | Heavier than needed for pure exploration | Make mandatory for modifications and inject safety routing when detected |

## Review Gate Decision

| Review path | Best use | Strength | Weakness | Decision |
| --- | --- | --- | --- | --- |
| `team-review` | Behavior-changing implementation before merge/release | Higher recall through security, quality, and test reviewers; can compare implementation to plan matrices | More time/context cost | Mandatory gate for behavior-changing work |
| `/review` | Small docs/config-only changes or quick supplemental check | Fast and low overhead | Lower coverage for indirect regression surfaces and test matrix gaps | Optional supplement only |

## Remaining Blockers

- Browser verification still depends on a running local stack and available MCP/browser tooling.
- CI matrix enforcement depends on the risky path list in `scripts/agent-flow-matrix-gate.py`; update that list when new runtime entrypoints are added.
- `.docs/` still needs a current/stale split before this workflow is copied to other repositories.
- Project-specific test commands still need confirmation during onboarding before the workflow is copied to another repository.
- Generated Playwright evidence under `docs/flow/**/integration-test/` is ignored by git. CI or PR workflows should upload it as an artifact when team-wide retention is needed.

See `docs/agent-flow-residual-risk-countermeasures.md` for why these risks
cannot be fully solved by workflow rules alone and which project-specific
environment, test, and review controls should be prepared.

## Judgment Items

- Resolved: `/flow-plan` is mandatory for modifications and business-flow-sensitive work; `/flow-start` remains for new-feature discovery.
- Resolved: `team-review` is mandatory for behavior-changing work; `/review` is supplemental.
- Resolved: CI enforces required plan matrices for behavior-affecting PRs.
- Resolved: project-local `kairo-*` commands and `sdd-*` skills are abolished; canonical replacements are `/flow-plan` and `/flow-impl`.
- Resolved: visible/multi-step workflows require `/flow-integration-test` evidence before final review.
- Resolved: Webwright is not a full Playwright Test replacement for this gate; use it as a scenario-crafting pattern when it reduces agent/browser turns.
- Decide whether `.docs/` should be archived after still-current content is moved to `docs/`.
- Decide whether model names should be hardcoded (`gpt-5.5-codex`) or configured through a local alias such as `CODEX_DEEP_MODEL`.

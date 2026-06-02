# Agent Flow Kit

Transferable Claude/Codex workflow package for medium-sized repositories.

## What It Provides

- repo-local `.claude/` commands, rules, hooks, and skills
- repo-local `.codex/` hooks and skills
- repo-local `CLAUDE.md` / `AGENTS.md` guidance plus a local
  `context-loader` skill so installed workflows do not depend on machine-global
  instructions
- CI matrix gate for required plan matrices
- onboarding skills for new repositories
- Playwright integration-test evidence gate
- mandatory cross-agent `flow-plan-review` gate before implementation
- explicit `Questioning Decision` and source-backed `No Questions Rationale`
  requirements before a behavior-changing plan can freeze
- Integration Coverage Contract that maps each business flow to happy, exception, permission, boundary, side-effect, and regression coverage
- Runtime Causality Gate that forces production-only, deploy/runtime/provider,
  browser-network, secret/binding, remote data, and auth/session symptoms to be
  classified before speculative code changes
- provider/auth/deploy evidence lanes that separate local mocks from deployed
  artifacts, real provider/device happy paths, valid credential/session paths,
  and concrete blockers

## Onboarding Sequence

Run these before behavior-changing implementation starts in a new repository:

1. `agent-flow-onboarding`
2. `project-structure-survey`
3. `business-flow-discovery`
4. `integration-scenario-design`

Required Markdown outputs:

```text
docs/agent-flow/project-structure.md
docs/agent-flow/business-flows.md
docs/agent-flow/integration-scenarios.md
```

Companion business-flow diagram:

```text
docs/agent-flow/business-flows.drawio
```

Behavior-changing work is blocked until the three Markdown onboarding documents
exist. The `.drawio` file is a companion diagram for human review of the
business-flow inventory; `business-flows.md` remains the canonical matrix
artifact.
During onboarding, `project-structure-survey` inventories runtime-causality
evidence sources such as deploy version checks, provider/runtime logs, smoke
commands, env/secrets/bindings, remote data diagnostics, and provider sandbox
availability. `integration-scenario-design` then records runtime/provider smoke
scenarios so future `/flow-plan` runs can distinguish code defects from
environment, data, deploy, or provider/runtime causes.
The CI matrix gate also rejects risky changes when the required plan sections are
empty, contain template placeholders, or rely on vague waivers.

## Install

Dry run:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --dry-run
```

The dry run classifies existing differing files instead of reporting only
`skip existing`:

- `recommend overwrite`: portable workflow assets such as commands, hooks,
  skills, `.codex/hooks.json`, CI workflow, and matrix-gate scripts. These are
  intended to track the kit. Runtime impact is limited to lightweight
  hook/script dispatch; apply when the new workflow gate is desired.
- `preserve local (manual-merge)`: target-local config, repository instructions,
  design docs, environment/testing rules, and historical flow docs. These often
  contain stack-specific decisions and should be merged intentionally instead of
  overwritten.
- `preserve local`: unknown existing paths outside the portable allowlist.

Install:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo
```

Apply the recommended existing-file updates while still preserving local
project docs/config:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --apply-recommended-updates
```

Preview that recommended update set without writing:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --dry-run --apply-recommended-updates
```

Overwrite existing workflow files:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --force
```

After install, review:

- `.agent-flow/config.json`
- `CLAUDE.md`
- `AGENTS.md`
- `.claude/settings.json`
- `.claude/skills/*/SKILL.md`
- `.claude/hooks/*.py`
- `.codex/skills/*/SKILL.md`
- `.codex/hooks/*.py`
- `.claude/docs/DESIGN.md`

The default `.agent-flow/config.json` is tuned for common Next.js repositories.
Adjust the path lists when installing into another stack.

If the target repo already has `.claude/settings.json`, the installer merges the Agent Flow hook snippet and writes a timestamped backup before updating it.
The merge treats repo-local hook scripts such as `.claude/hooks/agent-router.py`
as the same hook even if the shell wrapper changed, so repeated installs update
the existing entry instead of registering duplicates.

With `--force`, unchanged files are skipped instead of backed up again. Changed
files still receive `*.agent-flow-backup-*` backups before overwrite.

Prefer `--apply-recommended-updates` for normal kit upgrades. Use `--force` only
when you intentionally want to replace target-local guidance as well.

The installer validates that entry skills and hook scripts are present in the kit before copying files. If `SKILL.md` files are missing from the distributed kit, installation fails instead of creating a partial workflow.

The kit includes only distribution-safe global guidance. In particular, it
ships the local `context-loader` behavior and lightweight agent instructions,
but it does not force a machine-specific advisory-only Codex role or personal
global skills that could conflict with `/flow-impl` or `team-implement`.
The local `context-loader` is tool-neutral: Codex should prefer `AGENTS.md`,
Claude should prefer `CLAUDE.md`, and `.claude/` is treated as shared Agent Flow
documentation whose relevant parts are loaded proportionally.

## Safe Routing

Installed hooks bias toward `/flow-plan` for safety. When a user prompt looks
like an existing behavior change, bug fix, regression, refactor, auth/schema
change, or business-flow-sensitive task, `agent-router.py` injects a safety
gate reminder that `/flow-plan` is the canonical entry point before
implementation.

In addition, `flow-plan-required-gate.py` blocks edits to behavior-affecting
paths unless a frozen `docs/flow/{feature_name}/plan.md` exists. The default
path list is tuned for common Next.js repositories and can be customized in
`.agent-flow/config.json`.

Use `/flow-start` for new-feature discovery and greenfield scope shaping only.
If discovery shows that an existing runtime path will change, switch to
`/flow-plan` before freezing the plan or editing behavior-changing files.

`/flow-plan-review` must run after `/flow-plan` and before `/flow-impl` or
`team-implement`. It writes `docs/flow/{feature_name}/plan-review.md`; Codex
plans should be reviewed by Claude Code, and Claude Code plans should be
reviewed by Codex unless a concrete same-agent fallback reason is recorded.

`/flow-impl` can be run after `/flow-plan-review` without arguments. When no
argument is provided, it resolves the most recently modified
`docs/flow/*/plan.md` and uses that plan as the implementation target.

## Gate Order

```text
Project survey
  -> Business-flow discovery
  -> Integration-scenario design
  -> /flow-start or /flow-plan
  -> /flow-plan-review
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
```

## Claude Code / Codex Usage

The workflow names are intentionally aligned. Claude Code users can invoke the
slash commands, while Codex users can invoke the same names as skills or plain
instructions.

Codex users should prefer the `flow-plan` skill, not a separate lightweight
prompt. If a legacy `~/.codex/prompts/flow-plan.md` or repo-local prompt exists,
it should delegate to the skill and must preserve `Questioning Decision`,
source-backed `No Questions Rationale`, Residual Risk Preflight, Flow Knowledge
Update, the matrices, and the `flow-plan-review` handoff. Questions may be
skipped only when actor/scope, current behavior, desired behavior, success
criteria, affected entrypoints, side effects, migration/data compatibility, and
conflicts with existing docs/tests/code are all resolved by source evidence or
explicit scope control.

For onboarding/setup UI work, `flow-plan` must confirm step names, order,
excluded elements, action placement, resume/fallback behavior, and blocked
evidence lanes before implementation. For provider/auth/deploy issues, local
mocks and shallow checks such as preflight, invalid input, unauthenticated
`401`, or health endpoints do not replace real provider/device, deployed
artifact, valid credential/session, or side-effect evidence unless the plan
records the concrete blocker.

| Goal | Claude Code | Codex |
| --- | --- | --- |
| Load local context | `context-loader` skill | `context-loader` skill |
| New-feature discovery | `/flow-start {feature}` | `flow-start {feature}` |
| Existing behavior plan | `/flow-plan {request}` | `flow-plan {request}` |
| Plan review gate | `/flow-plan-review {feature}` | `flow-plan-review {feature}` |
| Implement latest frozen plan | `/flow-impl` | `flow-impl` |
| Implement a specific plan | `/flow-impl {feature}` | `flow-impl {feature}` |
| Browser evidence gate | `/flow-integration-test {feature}` | `flow-integration-test {feature}` |
| Parallel implementation | `team-implement` skill | `team-implement` skill |
| Review gate | `team-review` skill | `team-review` skill |

Both tools write the same artifacts under `docs/flow/{feature_name}/` and read
the same project knowledge under `docs/agent-flow/`.

## Webwright Decision

Playwright Test remains the deterministic pass/fail gate. Webwright-style code-as-action can be used to craft long browser scenarios, but the stable path must be promoted to a Playwright Test spec with assertions and evidence output.

## Residual Risk Countermeasures

The workflow reduces bugs and regressions, but some risks require domain
knowledge, runtime parity, test infrastructure, and reviewer discipline. See
`docs/agent-flow-residual-risk-countermeasures.md` after installation for the
recommended countermeasures and concrete environment examples.
`/flow-plan` uses this document as the basis for Residual Risk Preflight
warnings before a behavior-changing plan is frozen.
When runtime-causality triggers are present, `/flow-plan` must also record
active deployed version, browser symptom vs server outcome, runtime logs,
representative shallow and valid paths, bindings/secrets, remote data state, and
an evidence-backed classification before implementation tasks.

## Bug Feedback Loop

Bug and regression reports should improve the project-specific flow. See
`docs/agent-flow-bug-feedback-loop.md` after installation. When a previous plan
exists, `/flow-plan` classifies where the prior flow failed and adds flow
improvement tasks when possible. If the bug cannot be prevented by flow changes,
it is recorded in `docs/agent-flow/bug-knowledge.md`.

## Flow Knowledge Updates

Onboarding documents are intentionally broad. During `/flow-plan`, requirement
questions may uncover new project-specific business flows, exception paths,
permission rules, side effects, or integration scenarios. When that knowledge is
reusable beyond the current feature, `/flow-plan` records a Flow Knowledge Update
and adds tasks to update `docs/agent-flow/business-flows.md` and/or
`docs/agent-flow/integration-scenarios.md` before implementation.

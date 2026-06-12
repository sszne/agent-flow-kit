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
- onboarding-derived business-flow integration regression suites that infer,
  confirm, create, register, and run major operation tests on demand
- conditional Playwright integration-test evidence gate with lightweight and
  blocked lanes for low-risk or unavailable cases
- high-impact `flow-plan-review` gate before large-scale or high-risk
  implementation, with optional review for smaller behavior changes
- Goal Confirmation Gate that confirms the requester's desired user experience,
  business outcome, root-cause target, and accepted completion signal before a
  plan freezes when the goal is ambiguous
- explicit `Questioning Decision` and source-backed `No Questions Rationale`
  requirements before a behavior-changing plan can freeze
- Integration Coverage Contract that maps each business flow to happy, exception, permission, boundary, side-effect, and regression coverage
- Runtime Causality Gate that forces production-only, deploy/runtime/provider,
  browser-network, secret/binding, remote data, and auth/session symptoms to be
  classified before speculative code changes
- provider/auth/deploy evidence lanes that separate local mocks from deployed
  artifacts, real provider/device happy paths, valid credential/session paths,
  and concrete blockers
- design-system-aware frontend planning through the `flow-design` support skill,
  so frontend plans prefer repo-local tokens, components, patterns, and voice
  rules when they exist

## Onboarding Sequence

Run `agent-flow-onboarding` before behavior-changing implementation starts in a
new repository. During onboarding, run these steps in order:

1. `flow-document`
2. `project-structure-survey`
3. `business-flow-discovery`
4. `integration-scenario-design`

After onboarding, run `business-flow-integration-test` when the repository
should have a callable regression suite for major business-flow operations. The
skill explains the purpose, infers tests from the confirmed business flows,
asks about unclear operations, accepts missing operations from the user, gets
approval of the final list, creates executable tests, and registers an
all-suite runner. This follow-up is deliberately separate from `flow-impl` so
long baseline suites run only when invoked.

`flow-document` is mandatory to run at the start of onboarding, but source
documents are optional. If service requirement, proposal, design, or product
materials exist, the step converts them with `markitdown` when it is already
installed and writes a guarded claim ledger. If no documents exist, it records
`no-documents-provided` and onboarding continues.

Sidecar source-document ledger:

```text
docs/agent-flow/source-documents.md
docs/agent-flow/source-documents/raw/
docs/agent-flow/source-documents/converted/
```

The ledger is not a required implementation gate document. It exists to classify
document claims as confirmed, conflicting, aspirational, stale/unknown, or
needing user confirmation. Converted documents must not override repository
source, schema, routes, tests, deploy config, current repo docs, or explicit user
confirmation.

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

Optional business-flow integration suite spec after the follow-up:

```text
docs/agent-flow/business-flow-integration-tests.md
docs/agent-flow/business-flow-integration-test-runs/{run_id}/
```

### When Business-Flow Integration Tests Help

This follow-up is useful when the risk is not an isolated function but whether
the real business operation can still complete end to end.

Use it especially:

- right after onboarding, while the primary business-flow knowledge is fresh,
  to turn "what must not break" into executable baseline tests;
- before releases, to confirm auth, registration, delivery, reservation,
  order, payment, search, or other multi-step flows still work;
- after changing shared foundations such as auth middleware, permissions, API
  clients, schema, date/time logic, mail, delivery, jobs, or provider wiring;
- after larger refactors, to prove user-visible business outcomes survived the
  internal restructuring;
- after a repeated or costly regression, to make that full operation part of
  the standard regression route;
- when onboarding new engineers or agents, because
  `docs/agent-flow/business-flow-integration-tests.md` becomes a living
  specification of the main operations and how to run them.

Do not use this for small copy/style changes or isolated unit-level behavior.
Those should stay covered by focused unit, API, or feature tests. The split is:
`flow-integration-test` proves the current implementation plan, while
`business-flow-integration-test` proves the product's main business operations
still work as a baseline suite.

`flow-integration-test` itself is conditional:

- **Full Gate Required**: visible UI, multi-step workflows,
  auth/session/permission/tenant, provider/device/deploy, external side
  effects, and high-impact release confidence require full Playwright evidence
  or an explicit `BLOCKED` result.
- **Lightweight Evidence Allowed**: API-only, internal logic, docs/skill-only,
  static/build-only, or otherwise non-visible low-risk changes can use focused
  substitute evidence when the concrete reason, substitute commands/reviews,
  and covered regression surface are recorded.
- **Blocked Early**: if a required full gate cannot run, stop with `BLOCKED`
  and record blocker category, exact unverified surface, and minimum unblock
  action.

Every lane records effectiveness metrics such as issues found, whether a fix
resulted, fix reference, whether another test would have caught it, elapsed
time when available, token/work overhead when available, and blocker category.

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
- `docs/agent-flow/design-system.md`
- `docs/agent-flow/design-system/`
- `docs/agent-flow/design-principles.md`

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

The required-plan gate intentionally passes display-only edits without a frozen
plan when they are limited to minor style fixes, layout adjustments, or visible
text changes. This exception is narrow: anything that changes runtime behavior,
data flow, permissions, API behavior, workflow order, validation, side effects,
tests, install behavior, CI gates, or Agent Flow contracts still requires
`/flow-plan`. The hook and matrix gate can classify style files directly and
allow simple UI markup edits such as `className`/`style`/visible text changes;
ambiguous component edits stay blocked until a plan exists.

For frontend behavior-changing work that does require `/flow-plan`, the plan
must also run the Frontend Design System Gate. `flow-plan` uses `flow-design` as
a support skill to search configured design-system paths, local
`docs/agent-flow/design-system.md`, `docs/agent-flow/design-system/`,
`.claude/docs/DESIGN.md`, and relevant source components/styles. If matching
tokens, components, patterns, or voice rules exist, the plan should apply them
or record a concrete waiver. If no design system exists, the plan records the
searched paths and fallback source/component patterns.

This keeps Payn-like design-system imports generic: the kit can preserve and
apply a target repo's design-system rules, but it does not ship any brand's
tokens or components as defaults.

For behavior-changing work that affects modules, services, domain logic, shared
logic, or data ownership, the plan must also run the Design Principles Gate.
`flow-plan` reads repo-local `docs/agent-flow/design-principles.md` (and
configured `design_principles_paths`) before any external architecture
reference, then records a `Design Principles Compliance` section that applies
matching rules or concrete waivers. The shipped default principles require
side-effect-free loosely coupled modules and guard three anti-patterns:
design splits justified only by vague "responsibility" wording, Service-pattern
abuse that breaks encapsulation, and aggregate-internal constraints implemented
outside the aggregate. `flow-impl` re-checks the same rules during architecture
review, and the matrix gate requires the compliance section for
module-affecting behavior plans (`design_principles_affecting_prefixes`, with
`design_principles_excluded_segments`/`_extensions` so migration/config-only
work under broad module roots does not trigger).

Use `/flow-start` for new-feature discovery and greenfield scope shaping only.
If discovery shows that an existing runtime path will change, switch to
`/flow-plan` before freezing the plan or editing behavior-changing files.

`/flow-plan` must record a `Plan Review Requirement` decision before freezing.
Use `Requirement: Required` for large-scale or high-impact work, and
`Requirement: Optional` for smaller localized behavior changes where the plan
explains why cross-agent review is not mandatory.

`/flow-plan-review` must run after `/flow-plan` and before `/flow-impl` or
`team-implement` when the plan says review is required or when configured
high-impact paths are changed. It writes
`docs/flow/{feature_name}/plan-review.md`; Codex plans should be reviewed by
Claude Code, and Claude Code plans should be reviewed by Codex unless a
concrete same-agent fallback reason is recorded. It remains available and
recommended whenever the user or agent wants another readiness pass.

Treat these as high-impact review-required changes by default: multi-flow or
cross-module changes; auth, permission, tenant, ownership, session, security, or
privacy changes; schema, migration, data compatibility, backfill, rollback, or
destructive data changes; deploy, CI, install, hooks, workflow gates, risky-path
config, or Agent Flow contract changes; external providers, webhooks, mail/PDF,
storage, search/cache, queues, jobs, schedules, or other side effects; public
API contracts or shared runtime entrypoints; and any change the user or plan
author marks as uncertain or high impact.

`/flow-plan-review` is optional for clearly non-high-impact work, including
small localized behavior changes and non-behavioral typo, formatting-only, or
docs-only changes. A docs-only change that updates Agent Flow rules, skill
behavior, gates, review policy, risky-path config, or required evidence is
high-impact workflow work and still requires review.

`/flow-impl` can be run after a frozen plan, and after `/flow-plan-review` when
review is required. When no argument is provided, it resolves the most recently
modified `docs/flow/*/plan.md` and uses that plan as the implementation target.

## Gate Order

```text
Source document intake
  -> Project survey
  -> Business-flow discovery
  -> Integration-scenario design
  -> Business-flow integration-test suite when requested
  -> /flow-start or /flow-plan
  -> /flow-plan-review when required or requested
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
Update, Frontend Design System Gate when triggered, the matrices, and the
`Plan Review Requirement` decision. Questions may be skipped only when
actor/scope, current behavior, desired behavior, success criteria, affected
entrypoints, side effects, migration/data compatibility, design-system
applicability for frontend plans, and conflicts with existing docs/tests/code
are all resolved by source evidence or explicit scope control.

`flow-plan` must also confirm the requester's goal before freezing. When a bug
or change request could mean several different outcomes, such as improving an
error message, preserving user state, removing the root cause, adding
diagnostics, or proving the deployed valid path, the agent asks which outcome is
intended. The no-question path remains valid when the desired outcome and
completion signal are explicit in the user request or unambiguously supported by
source/runtime evidence.

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
| Source document intake | `/flow-document` | `flow-document` |
| Business-flow regression suite | `/business-flow-integration-test` | `business-flow-integration-test` |
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
For preventable requirement gaps, the review must distinguish the observed
symptom from the requester's desired outcome, root-cause target, and completion
signal before implementation tasks are accepted.

## Flow Knowledge Updates

Onboarding documents are intentionally broad. During `/flow-plan`, requirement
questions may uncover new project-specific business flows, exception paths,
permission rules, side effects, or integration scenarios. When that knowledge is
reusable beyond the current feature, `/flow-plan` records a Flow Knowledge Update
and adds tasks to update `docs/agent-flow/business-flows.md` and/or
`docs/agent-flow/integration-scenarios.md` before implementation.

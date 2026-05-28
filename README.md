# Agent Flow Kit

Transferable Claude/Codex workflow package for medium-sized repositories.

## What It Provides

- repo-local `.claude/` commands, rules, hooks, and skills
- repo-local `.codex/` hooks and skills
- CI matrix gate for required plan matrices
- onboarding skills for new repositories
- Playwright integration-test evidence gate
- Integration Coverage Contract that maps each business flow to happy, exception, permission, boundary, side-effect, and regression coverage

## Onboarding Sequence

Run these before behavior-changing implementation starts in a new repository:

1. `agent-flow-onboarding`
2. `project-structure-survey`
3. `business-flow-discovery`
4. `integration-scenario-design`

Required outputs:

```text
docs/agent-flow/project-structure.md
docs/agent-flow/business-flows.md
docs/agent-flow/integration-scenarios.md
```

Behavior-changing work is blocked until these onboarding documents exist.
The CI matrix gate also rejects risky changes when the required plan sections are
empty, contain template placeholders, or rely on vague waivers.

## Install

Dry run:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --dry-run
```

Install:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo
```

Overwrite existing workflow files:

```bash
python3 agent-flow-kit/install.py --target /path/to/repo --force
```

After install, review:

- `.agent-flow/config.json`
- `.claude/settings.json`
- `.claude/skills/*/SKILL.md`
- `.claude/hooks/*.py`
- `.codex/skills/*/SKILL.md`
- `.codex/hooks/*.py`
- `.claude/docs/DESIGN.md`

The default `.agent-flow/config.json` is tuned for common Next.js repositories.
Adjust the path lists when installing into another stack.

If the target repo already has `.claude/settings.json`, the installer merges the Agent Flow hook snippet and writes a timestamped backup before updating it.

The installer validates that entry skills and hook scripts are present in the kit before copying files. If `SKILL.md` files are missing from the distributed kit, installation fails instead of creating a partial workflow.

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

## Gate Order

```text
Project survey
  -> Business-flow discovery
  -> Integration-scenario design
  -> /flow-start or /flow-plan
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
```

## Webwright Decision

Playwright Test remains the deterministic pass/fail gate. Webwright-style code-as-action can be used to craft long browser scenarios, but the stable path must be promoted to a Playwright Test spec with assertions and evidence output.

## Residual Risk Countermeasures

The workflow reduces bugs and regressions, but some risks require domain
knowledge, runtime parity, test infrastructure, and reviewer discipline. See
`docs/agent-flow-residual-risk-countermeasures.md` after installation for the
recommended countermeasures and concrete environment examples.
`/flow-plan` uses this document as the basis for Residual Risk Preflight
warnings before a behavior-changing plan is frozen.

## Bug Feedback Loop

Bug and regression reports should improve the project-specific flow. See
`docs/agent-flow-bug-feedback-loop.md` after installation. When a previous plan
exists, `/flow-plan` classifies where the prior flow failed and adds flow
improvement tasks when possible. If the bug cannot be prevented by flow changes,
it is recorded in `docs/agent-flow/bug-knowledge.md`.

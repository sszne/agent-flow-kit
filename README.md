# Agent Flow Kit

Transferable Claude/Codex workflow package for medium-sized repositories.

## What It Provides

- repo-local `.claude/` commands, rules, hooks, and skills
- repo-local `.codex/` hooks and skills
- CI matrix gate for required plan matrices
- onboarding skills for new repositories
- Playwright integration-test evidence gate

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

If the target repo already has `.claude/settings.json`, the installer merges the Agent Flow hook snippet and writes a timestamped backup before updating it.

The installer validates that entry skills and hook scripts are present in the kit before copying files. If `SKILL.md` files are missing from the distributed kit, installation fails instead of creating a partial workflow.

## Gate Order

```text
Project survey
  -> Business-flow discovery
  -> Integration-scenario design
  -> /flow-plan
  -> /flow-impl or team-implement
  -> /flow-integration-test
  -> team-review
```

## Webwright Decision

Playwright Test remains the deterministic pass/fail gate. Webwright-style code-as-action can be used to craft long browser scenarios, but the stable path must be promoted to a Playwright Test spec with assertions and evidence output.

# Business Flow Integration Test Suite Implementation Report

## Summary
- Added `business-flow-integration-test` as a Claude/Codex entry skill for
  creating, updating, and running an onboarding-derived business-flow
  regression suite.
- Added Claude `/business-flow-integration-test` command wrapper.
- Updated onboarding and scenario-design templates so the post-onboarding
  suite is discoverable, user-confirmed, and separate from `flow-impl`.
- Updated integration-test templates to keep `flow-integration-test`
  feature-specific.
- Updated manifest, README, AGENTS/CLAUDE templates, and kit-local
  `docs/agent-flow/*` knowledge with AFK-011.

## Implemented Tasks
- [x] TASK-001: Add frozen plan and same-agent fallback plan review.
- [x] TASK-002: Add Claude/Codex `business-flow-integration-test` skill and
  Claude command.
- [x] TASK-003: Register the entrypoint in `manifest.json` and user-facing flow
  docs.
- [x] TASK-004: Update onboarding, scenario-design, and integration-test
  templates.
- [x] TASK-005: Update Agent Flow docs for AFK-011.
- [x] TASK-006: Run JSON, Python syntax, installer dry-run, and static discovery
  checks.

## Validation
| Command | Result |
| --- | --- |
| `python3 -m json.tool manifest.json` | Pass |
| `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py` | Pass |
| `cmp -s templates/.codex/skills/business-flow-integration-test/SKILL.md templates/.claude/skills/business-flow-integration-test/SKILL.md` | Pass |
| `git init /tmp/agent-flow-kit-business-flow-suite-smoke && python3 install.py --target /tmp/agent-flow-kit-business-flow-suite-smoke --dry-run` | Pass; dry-run lists Claude/Codex `business-flow-integration-test` skills and Claude command |
| `rg -n "business-flow-integration-test|business-flow-integration-tests|business-flow-integration-test-runs|Business Flow Integration Test Candidates|AFK-011" ...` | Pass |
| `git diff --check` | Pass |

## Notes
- The new suite is deliberately on-demand and not automatically invoked by
  `flow-impl`.
- Kit-level browser execution is out of scope because this repository does not
  contain a target application. Target repositories must run the registered
  suite and record PASS / FAIL / BLOCKED evidence after executable tests are
  generated.
- `py_compile` generated `__pycache__` directories during validation; they were
  removed before final review.

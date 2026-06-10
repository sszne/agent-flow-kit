# Project Structure Survey

## Repository Snapshot
- Stack: Python 3 installer plus Markdown/JSON/Python templates for Claude Code, Codex, GitHub Actions, and Agent Flow documentation.
- Runtime entrypoints:
  - `install.py`: copies templates into a target repository and classifies existing files.
  - `templates/.claude/commands/*.md`: Claude Code slash-command entrypoints.
  - `templates/.claude/skills/*/SKILL.md`: Claude Code skill templates.
  - `templates/.codex/skills/*/SKILL.md`: Codex skill templates.
  - `templates/.claude/hooks/*.py` and `templates/.codex/hooks/*.py`: workflow gates and quality hooks.
  - `templates/scripts/agent-flow-matrix-gate.py`: CI plan-quality gate.
  - `templates/docs/agent-flow/design-system.md`: optional target-repo design-system documentation template used by frontend planning.
  - `business-flow-integration-test`: onboarding follow-up entrypoint that creates, updates, and runs a callable regression suite for major confirmed business-flow operation tests.
- Local run commands:
  - `python3 install.py --target /path/to/repo --dry-run`
  - `python3 install.py --target /path/to/repo --dry-run --apply-recommended-updates`
  - `python3 install.py --target /path/to/repo --force`
- Test commands:
  - No dedicated test suite is present.
  - Use installer dry-run to validate template completeness and install classification.
  - Use `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py` for Python syntax validation.

## Architecture
| Area | Files/directories | Responsibility | Notes |
| --- | --- | --- | --- |
| Installer | `install.py` | Validate template completeness, copy files, merge settings hooks, update `.gitignore`, classify existing target files | Pure Python standard library |
| Manifest | `manifest.json` | Declares entry and support skills plus canonical flow | Installer validates listed skills exist for both Claude and Codex |
| Agent entrypoints | `templates/AGENTS.md`, `templates/CLAUDE.md` | Repo-local guidance copied to target repositories | Local-first files; manual merge when target already has local guidance |
| Claude workflow templates | `templates/.claude/commands/`, `templates/.claude/skills/`, `templates/.claude/hooks/` | Claude Code commands, skills, and workflow hooks | Portable workflow assets |
| Codex workflow templates | `templates/.codex/skills/`, `templates/.codex/hooks/`, `templates/.codex/hooks.json` | Codex skills and hook configuration | Portable workflow assets |
| Shared rules/design docs | `templates/.claude/rules/`, `templates/.claude/docs/` | Shared Agent Flow documentation for target repos | Local-first, target-specific after install |
| CI gate | `templates/.github/workflows/agent-flow-matrix.yml`, `templates/scripts/agent-flow-matrix-gate.py` | Reject behavior-affecting changes without required plan matrices, plan review, and onboarding docs | Default risky paths are tuned for common Next.js repos |
| Reference assets | `references/claude-settings-hooks.json` | Hook snippet merged into target `.claude/settings.json` | Installer de-duplicates repo-local hook scripts |
| Flow docs | `docs/flow/` | Planning artifacts for changes to this kit | Existing example plan is currently untracked in this checkout |

## Domain Model
| Model/entity | Source evidence | Relationships | Business meaning |
| --- | --- | --- | --- |
| Kit template file | `templates/**` | Copied to a target repository by `install.py` | A reusable workflow artifact installed into product repos |
| Entry skill | `manifest.json` `entry_skills` | Must exist under both `.claude/skills/` and `.codex/skills/` | User-facing workflow action such as onboarding, planning, implementation, or review |
| Support skill | `manifest.json` `support_skills` | Must exist under both tool skill directories | Shared helper skill used by entry workflows |
| Required onboarding document | `manifest.json` `required_onboarding_docs`; `agent-flow-matrix-gate.py` | Produced during `agent-flow-onboarding`; required before behavior-changing implementation | Durable project knowledge for future plans and tests |
| Source document ledger | `docs/agent-flow/source-documents.md`; `flow-document` skill | Optional sidecar produced at onboarding start | Classifies requirement/source-document claims without making them source-of-truth |
| Design-system document | `docs/agent-flow/design-system.md`, `docs/agent-flow/design-system/`; `flow-design` skill | Optional frontend planning context | Records repo-local tokens, components, patterns, voice rules, source priority, and waiver rules |
| Plan | `docs/flow/{feature}/plan.md`; `agent-flow-matrix-gate.py` markers | Must contain matrices, Plan Review Requirement, and frozen marker before implementation | Traceable change design and coverage contract |
| Plan review | `docs/flow/{feature}/plan-review.md`; `agent-flow-matrix-gate.py` markers | Required for high-impact implementation; optional for smaller localized changes | Cross-agent missed-risk review |
| Integration evidence | Skill docs and README evidence contract | Produced under `docs/flow/{feature}/integration-test/{run_id}/` for full evidence; recorded in reports for lightweight or blocked lanes | Conditional feature-specific verification with lane decision, Playwright/business-flow artifacts when required, and effectiveness metrics |
| Business-flow integration suite | `business-flow-integration-test` skill; `docs/agent-flow/business-flow-integration-tests.md` | Created after onboarding from confirmed business flows and user-approved scenario inventory | Re-runnable project-wide regression baseline for major continuous operations |

## Use Cases
| Use case | Actor | Entry point | Core flow | Evidence |
| --- | --- | --- | --- | --- |
| Install Agent Flow Kit into a repository | Developer / coding agent | `python3 install.py --target ...` | Validate templates, copy or classify files, merge settings hooks, update `.gitignore` | `README.md`, `install.py` |
| Preview safe kit updates | Developer / coding agent | `install.py --dry-run --apply-recommended-updates` | Classify existing file differences and show recommended overwrites | `README.md`, `install.py` |
| Onboard a target repository | Coding agent | `agent-flow-onboarding` skill | Produce project structure, business-flow, and integration-scenario docs | `templates/.codex/skills/agent-flow-onboarding/SKILL.md` |
| Intake source documents | Coding agent plus user | `flow-document` skill or `/flow-document` command | Convert optional service documents with markitdown when available and create a guarded claim ledger | `templates/.codex/skills/flow-document/SKILL.md` |
| Discover business flows | Coding agent plus user | `business-flow-discovery` skill | Build flow inventory, business-flow matrix, regression surface matrix, and coverage contract | `templates/.codex/skills/business-flow-discovery/SKILL.md` |
| Create or run business-flow regression suite | Coding agent plus user | `business-flow-integration-test` skill or `/business-flow-integration-test` command | Infer major operation tests from onboarding docs, ask about unclear operations, confirm final list, create executable tests, register all-suite runner, and run on demand | `templates/.codex/skills/business-flow-integration-test/SKILL.md` |
| Plan a behavior-changing change | Coding agent | `flow-plan` skill or `/flow-plan` command | Load context, inspect code/docs/tests, clarify ambiguity, write frozen plan | `README.md`, skill templates |
| Analyze frontend design-system fit | Coding agent | `flow-design` support skill called by `flow-plan` | Search configured design-system paths, compare planned UI with tokens/components/patterns, return applicability and component-match matrices | `templates/.codex/skills/flow-design/SKILL.md`, `templates/.claude/skills/flow-design/SKILL.md` |
| Review plan readiness | Opposite or fallback agent | `flow-plan-review` skill or command | Check missed risks, migration/auth/runtime/test coverage, decide readiness | `README.md`, `agent-flow-matrix-gate.py` |
| Implement a frozen plan | Coding agent | `flow-impl` or `team-implement` | Apply plan tasks after gates are satisfied | README canonical flow |
| Verify feature-specific implementation evidence | Coding agent | `flow-integration-test` | Choose full, lightweight, or blocked evidence lane; produce Playwright artifacts when required; record substitute evidence or blockers and effectiveness metrics | README and integration-test skill templates |
| Enforce workflow in CI | GitHub Actions | `agent-flow-matrix-gate.py` | Check risky diffs for onboarding docs, frozen plan, Plan Review Requirement, required plan review, matrices, and waiver quality | CI workflow and script |

## Runtime / Operations
| Concern | Evidence | Risk |
| --- | --- | --- |
| Template parity | Manifest validates both Claude and Codex skill paths | Divergence between tool templates can produce different workflow behavior |
| Target-local preservation | `LOCAL_FIRST_FILES` and `LOCAL_FIRST_PREFIXES` in `install.py` | Overwriting local project knowledge could erase repo-specific rules |
| Safe updates | `SAFE_UPDATE_PREFIXES` and `SAFE_UPDATE_FILES` in `install.py` | Portable workflow assets should be updateable without touching local docs |
| Hook merge idempotency | `HOOK_SCRIPT_PATTERN` and settings merge logic in `install.py` | Repeated installs must not register duplicate hooks |
| Workflow gate strictness | `agent-flow-matrix-gate.py` required markers and waiver checks | Overly broad defaults can block non-Next.js repos until config is tuned |
| Frontend design-system planning | `flow-design`, `flow-plan`, `design_system_paths`, matrix gate | Plans can become boilerplate unless applicability includes searched paths, component matches, and concrete waivers |
| Integration evidence lane selection | `flow-integration-test`, `integration-test`, testing rules | Overuse of full Playwright evidence wastes token/work budget; overuse of lightweight evidence can miss visible or provider/deploy regressions |
| Documentation-first behavior | README canonical flow and skill templates | Missing onboarding docs should block behavior-changing implementation |

## Existing Test Surface
| Level | Location/command | Coverage notes |
| --- | --- | --- |
| Syntax | `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py` | Validates Python files parse |
| Installer smoke | `python3 install.py --target /tmp/agent-flow-kit-smoke --dry-run` | Validates manifest skill presence and dry-run file classification |
| Matrix gate smoke | `python3 templates/scripts/agent-flow-matrix-gate.py --help` | Validates CLI argument parsing; stronger checks need a temporary git fixture |
| Manual documentation review | `templates/.claude/skills/*`, `templates/.codex/skills/*`, README | Needed for template wording, cross-tool consistency, evidence-lane guardrails, and effectiveness metrics |

## Open Questions
- Should this kit add automated tests around installer update classification and matrix-gate failure cases?
- Should Claude and Codex skill templates remain identical where possible, or should tool-specific instructions intentionally diverge?
- Should diagram artifacts created during onboarding be mandatory for all repositories or required only when business-flow inventory contains more than one flow?

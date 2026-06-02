# Integration Scenarios

## Scenario Matrix
| Scenario ID | Level | Business flow | Case type | Entry point | Data setup | Steps | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCN-001 | CLI smoke | AFK-001 | Happy, regression | `install.py --dry-run` | Temporary empty target directory | Run installer dry-run against target | Templates are enumerated without writing files; manifest validation passes | Command output |
| SCN-002 | CLI smoke | AFK-001 | Boundary, side effect | `install.py --dry-run --apply-recommended-updates` | Temporary target with existing differing safe-update and local-first files | Run dry-run update preview | Safe files are recommended/previewed; local-first files are preserved | Command output |
| SCN-003 | Syntax | AFK-001, AFK-009 | Regression | Python files | Current checkout | Run `python3 -m py_compile` on installer, hooks, and scripts | Python files parse | Command output |
| SCN-004 | Documentation review | AFK-002 | Happy, exception, regression | `agent-flow-onboarding` skill docs | Current template docs | Confirm onboarding sequence and outputs are explicit | Three required docs and blocker behavior are documented | Review notes |
| SCN-005 | Documentation review | AFK-003 | Happy, boundary, regression, side effect | `business-flow-discovery` skill docs | Current template docs | Confirm matrix output and draw.io artifact expectations match | Business-flow docs remain canonical and diagram is cross-linked | Review notes |
| SCN-006 | XML validation | AFK-003 | Exception, boundary, regression | `docs/agent-flow/business-flows.drawio` in a target onboarding run | Generated draw.io file | Parse diagram as XML and check `<mxfile>` root | Diagram is structurally valid draw.io XML | Command output |
| SCN-007 | Matrix gate smoke | AFK-005, AFK-006, AFK-009 | Happy, exception, regression | `agent-flow-matrix-gate.py` | Temporary git fixture when gate logic changes | Create risky diff with/without plan markers and plan review | Gate rejects missing docs/review and accepts complete artifacts | Fixture output |
| SCN-008 | Evidence artifact review | AFK-008 | Happy, side effect, regression | `docs/flow/{feature}/integration-test/{run_id}/` | Feature with visible workflow | Confirm index, screenshots, result, test review, and business-flow impact docs exist | Evidence is auditable | Artifact review |
| SCN-009 | Planning precision review | AFK-005, AFK-006, AFK-009 | Happy, exception, permission, boundary, side effect, regression | `flow-plan` templates and generated `docs/flow/{feature}/plan.md` | Behavior-changing request with possible ambiguity or provider evidence risk | Confirm `Questioning Decision`, `No Questions Rationale` when applicable, onboarding/UI precision, provider/auth/deploy evidence lanes, and prevention taxonomy classification | Plan freezes only after ambiguity, valid-path evidence lanes, and reusable bug patterns are resolved or blocked | Plan review notes |

## Playwright Scenarios
| Scenario ID | Entry point | Major steps requiring screenshots | Assertions | Screenshot names |
| --- | --- | --- | --- | --- |
| PW-001 | Target repository visible workflow changed by a future feature | Initial screen, main user action, result state, error/permission state where relevant | No console/network failures; displayed state matches expected business outcome | Defined per feature plan |

No Playwright scenario is required for the current Agent Flow Kit repository unless a change introduces a visible UI or browser-run workflow. Draw.io diagram generation is a documentation artifact; XML validation and human review are the required checks.

## Server Integration Scenarios
| Scenario ID | Test type | Case type | Target | Data setup | Assertions | Covers |
| --- | --- | --- | --- | --- | --- | --- |
| SRV-001 | CLI smoke | Happy, regression | `install.py --dry-run` | Temporary target directory | Dry-run completes and validates manifest template paths | AFK-001 |
| SRV-002 | CLI fixture | Boundary, side effect | `install.py` update classification | Temporary target with existing files | Safe-update, local-first, preserve-local classifications match policy | AFK-001 |
| SRV-003 | Static syntax | Regression | Python files | Current checkout | `py_compile` succeeds | AFK-001, AFK-009 |
| SRV-004 | Static XML parse | Exception, boundary | Generated `.drawio` file | Generated diagram artifact | XML parser accepts the file and root is draw.io-compatible | AFK-003 |
| SRV-005 | Git fixture | Happy, exception, regression | `agent-flow-matrix-gate.py` | Temporary git repo with risky diffs | Complete plan/review passes; missing markers fail | AFK-005, AFK-006, AFK-009 |

## Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Scenario IDs | Waiver / blocker |
| --- | --- | --- | --- | --- |
| AFK-001 | Installer smoke and syntax checks; fixture checks when installer logic changes | Happy, exception, boundary, side effect, regression | SCN-001, SCN-002, SCN-003, SRV-001, SRV-002, SRV-003 | None for installer changes |
| AFK-002 | Documentation review | Happy, exception, regression | SCN-004 | Automated execution is out of scope because onboarding is an agent-guided documentation workflow |
| AFK-003 | Documentation review plus draw.io XML validation | Happy, exception, boundary, side effect, regression | SCN-005, SCN-006, SRV-004 | Browser rendering is out of scope because the repo does not ship draw.io CLI/runtime |
| AFK-004 | Documentation review against business-flow docs | Happy, exception, permission, boundary, regression | Covered by future feature-specific plan checks | Automated scenario execution is out of scope because this flow writes planning docs |
| AFK-005 | Matrix-gate validation and plan-review handoff | Happy, exception, permission, boundary, side effect, regression | SCN-007, SRV-005 | None for gate logic changes |
| AFK-005 planning precision | Template and plan-review validation of `Questioning Decision`, `No Questions Rationale`, onboarding/UI precision, provider/auth/deploy evidence lanes, and bug prevention taxonomy | Happy, exception, permission, boundary, side effect, regression | SCN-009 | Automated semantic proof is out of scope because plans are natural-language artifacts; matrix gate and plan review remain required. |
| AFK-006 | Plan-review marker validation | Happy, exception, regression | SCN-007, SRV-005 | Cross-agent execution may be blocked by unavailable opposite agent; same-agent fallback must record the blocker |
| AFK-007 | Feature-specific planned validation | Happy, exception, permission, boundary, side effect, regression | Defined in each feature plan | Feature-specific waiver required if omitted |
| AFK-008 | Evidence artifact review when visible workflow exists | Happy, exception, permission, boundary, side effect, regression | SCN-008, PW-001 | Blocked only when no runnable browser/app exists; blocker must name surface |
| AFK-009 | Gate smoke or fixture checks | Happy, exception, boundary, regression | SCN-003, SCN-007, SRV-003, SRV-005 | None for gate logic changes |

## Seed / Reset Strategy
- Use temporary directories under `/tmp` for installer smoke checks.
- Use temporary git repositories for matrix-gate fixtures so the current checkout is not mutated.
- For generated draw.io files, validate the target file directly with Python XML parsing.
- Do not depend on a network service, browser session, or user profile for kit-level checks.

## Evidence Contract
- CLI evidence: command output in final report or implementation report.
- Plan evidence: `docs/flow/{feature}/plan.md`.
- Plan review evidence: `docs/flow/{feature}/plan-review.md`.
- Browser evidence root when applicable: `docs/flow/{feature}/integration-test/{run_id}/`.
- Required browser files when applicable: `index.html`, `result.md`, `test-review.md`, `business-flow-impact.md`, `screenshots/`.

## Planning Evidence Rules

- Every behavior-changing plan must record a `Questioning Decision`. If no
  questions are asked, the `No Questions Rationale` must cite concrete user
  wording, source files, docs, tests, schema, routes, or explicit scope control.
- Onboarding, setup, wizard, modal, tutorial, first-login rail, admin guide, or
  other visible multi-step guidance plans must confirm desired step names and
  order, excluded elements, action placement relative to matching instructions,
  resume/fallback route, safe recipient/provider boundaries, and blocked
  evidence lanes.
- Real provider/device happy-path evidence is required when the risk is a
  provider callback, device/app context, valid credential/session, deployed
  artifact, mail delivery, storage write, webhook, or other side effect. If it
  cannot run, the plan must record the exact credential, environment, operator
  action, or blocker while keeping deterministic mock evidence.
- Preflight, invalid input, unauthenticated `401`, and health checks are useful
  but cannot replace the valid path or side-effect path when that path is the
  reported risk.
- Bug/regression plans must classify matching entries in
  `docs/agent-flow/bug-knowledge.md` by prevention pattern before task design.

## Coverage Gaps
| Gap | Reason | Follow-up |
| --- | --- | --- |
| No dedicated installer unit tests | The current repo ships no test harness | Add fixture tests when installer logic changes |
| No draw.io rendering check | The repo does not include draw.io CLI/runtime | Validate XML and rely on human opening in draw.io unless a rendering tool is added |
| No automated agent-skill execution test | Skills are natural-language workflows | Keep output contracts explicit and validate generated artifacts where possible |

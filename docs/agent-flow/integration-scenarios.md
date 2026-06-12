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
| SCN-007 | Matrix gate smoke | AFK-005, AFK-006, AFK-009 | Happy, exception, regression | `agent-flow-matrix-gate.py` | Temporary git fixture when gate logic changes | Create risky diff with optional review, high-impact diff without review, high-impact diff with approved review, and display-only style/layout/text diffs | Gate accepts optional-review smaller changes, rejects missing review for high-impact changes, accepts complete required-review artifacts, and accepts classified display-only changes | Fixture output |
| SCN-008 | Evidence artifact review | AFK-008 | Happy, side effect, regression | `docs/flow/{feature}/integration-test/{run_id}/` and implementation report | Feature with visible/high-risk workflow or low-risk non-visible change | Confirm evidence lane is recorded; full lane has index, screenshots, result, test review, and business-flow impact docs; lightweight lane has substitute evidence and covered regression surface; blocked lane names blocker and unverified surface | Evidence is auditable and lane-appropriate | Artifact/review notes |
| SCN-009 | Planning precision review | AFK-005, AFK-006, AFK-009 | Happy, exception, permission, boundary, side effect, regression | `flow-plan` templates and generated `docs/flow/{feature}/plan.md` | Behavior-changing request with possible ambiguity or provider evidence risk | Confirm Goal Confirmation, `Questioning Decision`, `No Questions Rationale` when applicable, onboarding/UI precision, provider/auth/deploy evidence lanes, and prevention taxonomy classification | Plan freezes only after requester goal, ambiguity, valid-path evidence lanes, and reusable bug patterns are resolved or blocked | Plan review notes |
| SCN-010 | Documentation review | AFK-002, AFK-003, AFK-004, AFK-010 | Happy, exception, boundary, side effect, regression | `flow-document` and onboarding skill docs | Current template docs | Confirm source documents create a claim ledger, not source-of-truth, and unconfirmed claims cannot enter matrices or required scenarios | Claim statuses, source priority, and downstream restrictions are explicit | Review notes |
| SCN-011 | Matrix gate fixture | AFK-005, AFK-009 | Happy, validation, exception, boundary, regression | `agent-flow-matrix-gate.py` | Temporary git repo with browser-affecting behavior change and frozen plans with/without design-system applicability (reusable driver: `docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py`) | Run gate against missing-section, complete-section, and no-doc-without-evidence variants | Missing `Design System Applicability` fails; a `Design system found: No` claim without searched-path/fallback evidence fails; complete section with searched paths and fallback/design evidence passes | Fixture output |
| SCN-012 | Documentation / manifest review | AFK-002, AFK-004, AFK-008, AFK-011 | Happy, exception, permission, boundary, side effect, regression | `business-flow-integration-test` skill docs and generated suite spec contract | Current template docs | Confirm onboarding hands off to a user-confirmed business-flow operation suite, executable tests are not created before approval, one all-suite runner is registered, and feature-specific `flow-integration-test` remains separate | Entry skill exists for Claude/Codex, command exists for Claude, and suite evidence contract is explicit | Review notes and installer dry-run |
| SCN-013 | Matrix gate fixture | AFK-005, AFK-009 | Happy, validation, boundary, regression | `agent-flow-matrix-gate.py` | Temporary git repo with module-code behavior change and frozen plans with/without design-principles compliance | Run gate against missing-section, complete-section, weak-waiver, no-doc-without-evidence, migrations-only, and broad-root config/migration-only variants | Missing or weak `Design Principles Compliance` fails for module-affecting plans; complete section passes; migration/config-only diffs (including under broad module roots) do not trigger | Fixture output |

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
| SRV-005 | Git fixture | Happy, exception, regression | `agent-flow-matrix-gate.py` | Temporary git repo with risky diffs | Optional-review plan passes for smaller behavior changes; high-impact paths require approved review; missing markers fail; display-only style/layout/text diffs pass without a plan | AFK-005, AFK-006, AFK-009 |
| SRV-006 | Git fixture | Happy, validation, exception, boundary, regression | `agent-flow-matrix-gate.py` | Temporary git repo with browser-affecting diff | Frontend behavior plan without `Design System Applicability` fails; a no-doc claim without searched-path/fallback evidence fails; equivalent plan with paths-inspected and fallback evidence passes | AFK-005, AFK-009 |
| SRV-007 | Installer smoke | Happy, exception, regression | `install.py --dry-run` | Temporary target directory | Manifest validation finds `business-flow-integration-test` for both Claude and Codex | AFK-001, AFK-011 |
| SRV-008 | Git fixture | Happy, validation, boundary, regression | `agent-flow-matrix-gate.py` | Temporary git repo with module-code diff | Module-affecting behavior plan without `Design Principles Compliance` fails; weak waivers fail; complete section passes; migrations-only and broad-root config/migration-only diffs do not trigger | AFK-005, AFK-009 |

## Business Flow Integration Test Candidates
| Candidate ID | Business flow | Continuous operation | Suggested level | Data / environment needs | Questions before executable test |
| --- | --- | --- | --- | --- | --- |
| BFIT-CANDIDATE-001 | Target repo primary confirmed flow | Major operation sequence inferred from onboarding docs | Playwright or Feature/API | Target-specific seed/reset, auth, time, provider, or deployed-domain requirements | Confirmed by the user during `business-flow-integration-test` before executable tests are created |

## Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Scenario IDs | Waiver / blocker |
| --- | --- | --- | --- | --- |
| AFK-001 | Installer smoke and syntax checks; fixture checks when installer logic changes | Happy, exception, boundary, side effect, regression | SCN-001, SCN-002, SCN-003, SRV-001, SRV-002, SRV-003 | None for installer changes |
| AFK-002 | Documentation review | Happy, exception, regression | SCN-004 | Automated execution is out of scope because onboarding is an agent-guided documentation workflow |
| AFK-003 | Documentation review plus draw.io XML validation | Happy, exception, boundary, side effect, regression | SCN-005, SCN-006, SRV-004 | Browser rendering is out of scope because the repo does not ship draw.io CLI/runtime |
| AFK-004 | Documentation review against business-flow docs | Happy, exception, permission, boundary, regression | Covered by future feature-specific plan checks | Automated scenario execution is out of scope because this flow writes planning docs |
| AFK-005 | Matrix-gate validation and plan-review requirement decision | Happy, exception, permission, boundary, side effect, regression | SCN-007, SRV-005 | None for gate logic changes |
| AFK-005 planning precision | Template and plan-review validation of Goal Confirmation, `Questioning Decision`, `No Questions Rationale`, Plan Review Requirement, onboarding/UI precision, design-principles compliance, provider/auth/deploy evidence lanes, and bug prevention taxonomy | Happy, exception, permission, boundary, side effect, regression | SCN-009, SCN-013 | Automated semantic proof is out of scope because plans are natural-language artifacts; matrix gate and required reviews remain the enforcement layer. |
| AFK-005 frontend design-system planning | Template, plan-review, and matrix-gate validation of `Design System Applicability`, component matching, searched paths, and concrete design waivers | Happy, exception, boundary, regression | SCN-011, SRV-006 | Automated visual/design semantic proof is out of scope because design-system matching is a natural-language workflow; the plan section, component matrix, and review gate remain the enforcement layer. |
| AFK-006 | Plan-review marker validation when review is required | Happy, exception, regression | SCN-007, SRV-005 | Cross-agent execution may be blocked by unavailable opposite agent; same-agent fallback must record the blocker. Smaller localized behavior changes, typo fixes, formatting-only edits, and docs-only edits may mark review optional when they do not alter high-impact surfaces. |
| AFK-007 | Feature-specific planned validation | Happy, exception, permission, boundary, side effect, regression | Defined in each feature plan | Feature-specific waiver required if omitted |
| AFK-008 | Conditional evidence-lane review; full Playwright artifact check when visible/high-risk workflow exists | Happy, exception, permission, boundary, side effect, regression | SCN-008, PW-001 | Lightweight evidence is allowed only for non-visible low-risk changes with substitute checks and covered regression surface; required full evidence can be blocked only with blocker category, exact unverified surface, and minimum unblock action |
| AFK-009 | Gate smoke or fixture checks, including display-only bypass and behavior-change rejection | Happy, exception, boundary, regression | SCN-003, SCN-007, SRV-003, SRV-005 | None for gate logic changes |
| AFK-010 | Source-document intake template review plus downstream guardrail review | Happy, exception, boundary, side effect, regression | SCN-010 | Automated semantic validation is out of scope because claim classification depends on repo evidence and user confirmation |
| AFK-011 | Business-flow integration suite template, command, manifest, and installer review; generated target-repo suite execution when created | Happy, exception, permission, boundary, side effect, regression | SCN-012, SRV-007 | Kit-level browser execution is out of scope because this repository has no application under test; target repos must run the registered suite and record PASS/FAIL/BLOCKED evidence. |

## Seed / Reset Strategy
- Use temporary directories under `/tmp` for installer smoke checks.
- Use temporary git repositories for matrix-gate fixtures so the current checkout is not mutated.
- For generated draw.io files, validate the target file directly with Python XML parsing.
- Do not depend on a network service, browser session, or user profile for kit-level checks.

## Evidence Contract
- CLI evidence: command output in final report or implementation report.
- Plan evidence: `docs/flow/{feature}/plan.md`.
- Plan review requirement evidence: `Plan Review Requirement` in
  `docs/flow/{feature}/plan.md`.
- Plan review evidence when required: `docs/flow/{feature}/plan-review.md`.
- Plan review optional path: allowed for smaller localized behavior changes and
  non-behavioral typo, formatting-only, or docs-only work that does not alter
  high-impact surfaces. Docs-only changes to Agent Flow rules, skill behavior,
  gates, review policy, risky-path config, or required evidence still require
  review.
- Browser evidence root when applicable: `docs/flow/{feature}/integration-test/{run_id}/`.
- Required browser files when applicable: `index.html`, `result.md`, `test-review.md`, `business-flow-impact.md`, `screenshots/`.
- Business-flow baseline suite spec:
  `docs/agent-flow/business-flow-integration-tests.md`.
- Business-flow baseline suite evidence when run:
  `docs/agent-flow/business-flow-integration-test-runs/{run_id}/`.

### Integration-Test Evidence Lanes

| Lane | Use when | Required evidence |
| --- | --- | --- |
| Full Gate Required | Visible UI, multi-step workflow, auth/session/permission/tenant, provider/device/deploy, external side effect, or high-impact release confidence is in scope | Playwright Test result, major-step screenshots, `index.html`, `result.md`, `test-review.md`, `business-flow-impact.md`, coverage mapping |
| Lightweight Evidence Allowed | API-only, internal logic, docs/skill-only, static/build-only, or otherwise non-visible low-risk change | Concrete low-risk reason, substitute commands/reviews, covered regression surface, Integration Coverage Contract coverage or waiver |
| Blocked Early | Full gate is required but runner, base URL, auth session, provider credential, device tunnel, safe test data, or equivalent dependency is unavailable | `BLOCKED` result, blocker category, exact unverified surface, minimum unblock action |

Lightweight evidence must not bypass visible, multi-step,
auth/session/permission/tenant, provider/device/deploy, external-side-effect, or
high-impact evidence requirements.

### Effectiveness Metrics

Record these keys for every full, lightweight, or blocked lane so operations
can evaluate whether the gate finds defects worth its overhead:

```text
evidence_lane: full | lightweight | blocked
issues_found: count + severity list
fix_resulted: yes | no
fix_reference: commit / file / task / none
would_other_tests_have_caught: yes | no | unknown
elapsed_time_minutes: number | unknown
token_or_work_overhead: estimate | unknown
blocker_category: runner | base_url | auth_session | provider_credentials | device_tunnel | safe_test_data | none
```

## Planning Evidence Rules

- Every behavior-changing plan must record a `Questioning Decision`. If no
  questions are asked, the `No Questions Rationale` must cite concrete user
  wording, source files, docs, tests, schema, routes, or explicit scope control.
- Frontend behavior-changing plans must run the Frontend Design System Gate when
  screens, components, frontend routes, client UI, styles, public frontend
  assets, brand, tokens, component rules, or design-system attachments are in
  scope. The plan must include `Design System Applicability`; if no design
  system is found, it must record searched paths and fallback source/component
  evidence.
- Every behavior-changing plan must confirm the requester's desired outcome and
  accepted completion signal before freezing. If a bug report could mean
  symptom display, state preservation, root-cause elimination, diagnostics, or
  deployed valid-path proof, ask the requester which goal is intended.
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
- Source-document claims from `docs/agent-flow/source-documents.md` may improve
  business-flow discovery only after they are confirmed by repo evidence or the
  user. Conflicting, aspirational, stale/unknown, and needs-confirmation claims
  remain open questions, blockers, or future-scope notes.

## Coverage Gaps
| Gap | Reason | Follow-up |
| --- | --- | --- |
| No dedicated installer unit tests | The current repo ships no test harness | Add fixture tests when installer logic changes |
| No draw.io rendering check | The repo does not include draw.io CLI/runtime | Validate XML and rely on human opening in draw.io unless a rendering tool is added |
| No automated agent-skill execution test | Skills are natural-language workflows | Keep output contracts explicit and validate generated artifacts where possible |

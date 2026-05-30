# Business Flow Draw.io Diagrams Plan

## 1. Requirements

### 1.1 Current State
- `business-flow-discovery` currently creates `docs/agent-flow/business-flows.md` with flow inventory, Business Flow Matrix, Regression Surface Matrix, Integration Coverage Contract, confirmed decisions, and open questions.
- Both Claude and Codex templates contain the same business-flow discovery output contract.
- `agent-flow-onboarding` currently lists three required outputs:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`
- The kit has no draw.io generation helper, no draw.io dependency, and no current diagram artifact contract.
- This checkout now has Agent Flow onboarding docs for the kit itself under `docs/agent-flow/`.

### 1.2 Intent And Ambiguity Resolution
- User intent: During onboarding business-flow inventory, create a draw.io diagram so humans can understand and audit flows more easily.
- Resolved by conservative scope:
  - Use draw.io-compatible `.drawio` XML artifacts because they are portable and can be opened by diagrams.net/draw.io without adding a runtime dependency.
  - Keep Markdown matrices as canonical; the diagram is an auditable companion artifact, not a replacement.
  - Generate one default diagram file at `docs/agent-flow/business-flows.drawio`.
  - Require the diagram to include discovered flows, actors/entrypoints, normal path transitions, exception/permission/boundary branches when known, side effects, and open-question markers.
  - Add validation guidance using XML well-formedness rather than a draw.io renderer.

### 1.3 Goal
Make onboarding output easier for people to review by extending business-flow discovery and onboarding guidance to produce a draw.io companion diagram aligned with `business-flows.md`.

### 1.4 Scope / Non-Goals
In scope:
- Update Claude and Codex `business-flow-discovery` skill templates.
- Update Claude and Codex `agent-flow-onboarding` skill templates.
- Update README onboarding output guidance.
- Add or update plan/test guidance so diagram generation is reviewed and validated.

Out of scope:
- Adding a new Python or Node dependency for diagram rendering.
- Building a full automatic matrix-to-drawio converter.
- Replacing Mermaid, Markdown matrices, or integration scenario docs.
- Making diagram creation a browser/E2E workflow.

### 1.5 Acceptance Criteria
- `business-flow-discovery` instructs agents to create `docs/agent-flow/business-flows.drawio`.
- The diagram contract is explicit enough for consistent human-readable output:
  - actors and entrypoints are visible,
  - flow IDs match the Flow Inventory,
  - normal/error/permission/boundary paths are represented,
  - side effects and integrations are represented,
  - unresolved questions/blockers are represented,
  - the Markdown file links to the diagram.
- Claude and Codex skill templates remain aligned.
- Onboarding output lists the diagram artifact as a companion output.
- README mentions the optional/companion diagram output.
- Validation includes XML well-formedness for `.drawio` files.

### 1.6 User Answers
- User requested draw.io diagram creation during onboarding business-flow inventory for human understandability.
- No further product clarification is required for this minimal workflow-template change.

## 2. Design

### 2.1 Affected Files And Modules
| File | Change |
| --- | --- |
| `templates/.codex/skills/business-flow-discovery/SKILL.md` | Add diagram artifact rules, workflow step, output contract, and Markdown cross-link expectation |
| `templates/.claude/skills/business-flow-discovery/SKILL.md` | Mirror Codex changes |
| `templates/.codex/skills/agent-flow-onboarding/SKILL.md` | List draw.io as a companion output and readiness item |
| `templates/.claude/skills/agent-flow-onboarding/SKILL.md` | Mirror Codex changes |
| `README.md` | Mention companion draw.io output during onboarding |
| `docs/agent-flow/business-flows.md` | Record the new flow knowledge if implementation confirms final artifact policy |
| `docs/agent-flow/integration-scenarios.md` | Keep XML validation scenario aligned if final implementation changes validation |

### 2.2 Implementation Approach
1. Extend `business-flow-discovery` rules:
   - Keep `docs/agent-flow/business-flows.md` as the required canonical output.
   - Add `docs/agent-flow/business-flows.drawio` as a companion artifact.
   - Require diagram-to-matrix consistency by matching Flow IDs.
2. Extend workflow:
   - After matrices are drafted, create the draw.io diagram.
   - Add a cross-link from `business-flows.md` to the `.drawio` file.
   - Validate `.drawio` as XML when practical.
3. Extend output template:
   - Add a `Diagram` section to `business-flows.md`.
   - Add a concise draw.io contract outside the Markdown fenced template so agents know what the `.drawio` file must contain.
4. Update onboarding output/readiness text to mention the companion diagram.
5. Update README required outputs text to include the companion diagram without weakening the three required onboarding docs.

### 2.3 Design Policy And Library Selection
- No dependency is added.
- `.drawio` XML is selected because it is the native portable draw.io format and can be validated with Python standard-library XML parsing.
- A helper script is intentionally deferred because the current workflow is agent-authored documentation, and a script would need a larger schema/design decision.

### 2.4 Risks And Mitigations
| Risk | Mitigation |
| --- | --- |
| Diagram drifts from `business-flows.md` | Require matching Flow IDs and a Markdown link to the diagram |
| Agents produce invalid draw.io XML | Add XML well-formedness validation guidance |
| Diagram replaces required matrices | State that Markdown matrices remain canonical and required |
| Claude/Codex templates diverge | Apply mirrored edits and review both files |
| The artifact becomes too heavy for simple repos | Define as companion output; unresolved or tiny cases can record a concrete blocker/reason |

### 2.5 Residual Risk Preflight
| Warning | Countermeasure |
| --- | --- |
| Natural-language diagram instructions can still produce inconsistent layouts | Define the required diagram content and validation criteria, not a decorative style |
| Runtime/tooling gap: draw.io renderer is not bundled | Use XML validation and human-openable `.drawio` artifact |
| Reviewer risk: humans may trust a pretty diagram over matrices | Keep matrices canonical and require Flow ID cross-reference |

### 2.6 Bug Feedback Review
This is not a bug/regression report. No prior flow failure is being classified.

### 2.7 Flow Knowledge Update
- Update `docs/agent-flow/business-flows.md` after implementation if the final policy differs from this plan.
- Current reusable knowledge: business-flow discovery should produce a draw.io companion artifact for human auditability while keeping Markdown matrices canonical.

### 2.8 Business Flow Matrix
| Flow ID | Actor / scope | Entry point | Existing behavior | Expected behavior | Normal path | Error/exception paths | Permission/ownership/boundary paths | Side effects | Regression risk | Required verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-003 | Coding agent and user inventorying flows | `business-flow-discovery` | Text-only flow inventory and matrices | Text matrices plus `docs/agent-flow/business-flows.drawio` diagram aligned by Flow ID | Read structure survey, draft flows, ask missing rules, write matrices, create draw.io diagram, link diagram | Flow cannot be safely diagrammed because required business rules are unknown; XML is invalid | Diagram must show permission/ownership/boundary branches where known; unresolved areas remain explicit | Writes a new `.drawio` artifact in target docs | Humans can miss gaps if diagram is missing or inconsistent | Template review plus XML validation guidance |
| AFK-002 | Coding agent onboarding a target repo | `agent-flow-onboarding` | Required outputs are three Markdown docs | Onboarding reports three required docs plus companion business-flow diagram when produced | Run survey, business-flow discovery, integration scenario design, report readiness including diagram status | Diagram blocked by ambiguity or invalid artifact | Behavior-changing implementation remains blocked if required docs are missing; diagram blocker must be concrete | Writes target docs and companion artifact | Onboarding readiness report may omit diagram status | Documentation review |
| AFK-001 | Developer installing kit | `install.py` | Installer copies all template files | Updated skill/README templates are copied or recommended for safe update | Validate manifest and dry-run install | Missing template file or syntax issue | Local-first docs remain preserved | Copies updated docs into target repo | Template update might not be distributed | Installer dry-run |

### 2.9 Regression Surface Matrix
| Surface | Affected flows | Evidence | Required verification |
| --- | --- | --- | --- |
| Skill output contracts | AFK-002, AFK-003 | `business-flow-discovery` and `agent-flow-onboarding` templates | Review Claude and Codex template parity |
| Documentation install distribution | AFK-001 | `install.py`, `manifest.json` | Installer dry-run validates listed skill files exist |
| README guidance | AFK-001, AFK-002 | README onboarding section | Documentation review |
| Generated diagram artifacts | AFK-003 | Planned `.drawio` output | XML well-formedness command documented |
| Existing required onboarding docs | AFK-002, AFK-005 | Matrix gate and manifest | Ensure draw.io addition does not weaken required three-doc gate |

### 2.10 Test Design Matrix
| Test ID | Level | Target | Scenario | Expected result | Covers flow/risk |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | Static review | Claude/Codex `business-flow-discovery` | Compare diagram rules and output contract | Both templates require the same artifact and consistency rules | Template parity |
| TEST-002 | Static review | Claude/Codex `agent-flow-onboarding` | Compare output/readiness wording | Both templates mention diagram as companion output without replacing required docs | Onboarding consistency |
| TEST-003 | CLI smoke | Installer | Run `python3 install.py --target /tmp/agent-flow-kit-drawio-smoke --dry-run` | Manifest validation and dry-run complete | Distribution safety |
| TEST-004 | Syntax smoke | Python files | Run `python3 -m py_compile ...` | Python files parse | No incidental Python breakage |
| TEST-005 | XML validation guidance | Planned draw.io artifact contract | Confirm docs include a concrete XML parse command or equivalent guidance | Agents have a deterministic validation path | Invalid diagram risk |

### 2.11 Integration Coverage Contract
| Flow ID | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-003 | Template review and XML validation guidance | Happy, exception, boundary, permission, side effect, regression | Browser rendering is out of scope because the kit does not ship draw.io CLI/runtime |
| AFK-002 | Template review for onboarding output/readiness | Happy, exception, regression | Automated agent execution is out of scope because onboarding is a natural-language skill workflow |
| AFK-001 | Installer dry-run and Python syntax smoke | Happy, exception, boundary, regression | None |

### 2.12 Playwright Integration Test Plan
No Playwright run is required for this change because it changes documentation templates and generated `.drawio` artifacts, not a visible web runtime. If a future implementation adds a browser-based diagram editor or preview, that feature must add Playwright evidence.

### 2.13 Migration / Runtime Enforcement
- Migration needed: No.
- Migration enforcement path: Not applicable because no schema or database runtime changes are planned.
- Runtime validation command:
  - `python3 -m py_compile install.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py templates/scripts/*.py`
  - `python3 install.py --target /tmp/agent-flow-kit-drawio-smoke --dry-run`

### 2.14 Open Questions
- None blocking the minimal plan.
- Future enhancement question: whether to add a deterministic matrix-to-drawio generator script after observing real onboarding outputs.

## 3. Tasks
- [x] TASK-001: Update Codex `business-flow-discovery` skill with draw.io artifact contract.
- [x] TASK-002: Mirror the same contract in Claude `business-flow-discovery`.
- [x] TASK-003: Update Codex and Claude `agent-flow-onboarding` outputs/readiness text.
- [x] TASK-004: Update README onboarding output guidance.
- [x] TASK-005: Review generated documentation for diagram/matrix consistency wording.
- [x] TASK-006: Run Python syntax smoke.
- [x] TASK-007: Run installer dry-run smoke.
- [x] TASK-008: Update `docs/agent-flow/business-flows.md` or `integration-scenarios.md` only if implementation changes the final policy from this plan.

## 4. Readiness
- [x] Requirements map to tasks
- [x] User intent and current-state analysis is documented
- [x] Business/product ambiguity has been resolved or explicitly blocked
- [x] Required onboarding docs exist for behavior-changing work
- [x] Flow Knowledge Update target is explicit
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
- [x] Business flows map to required tests or blockers
- [x] Integration Coverage Contract has concrete coverage or waivers
- [x] Validation commands are identified
- [x] `docs/flow/business-flow-drawio-diagrams/plan-review.md` exists and approves the current frozen plan

<!-- frozen: v1 2026-05-30 by Codex -->
<!-- plan_author: codex -->

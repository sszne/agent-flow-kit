# Design System Aware Flow Plan

<!-- frozen: v1 2026-06-08 -->
<!-- plan_author: codex -->

## 1. Requirements

### 1.1 Current State

- The user wants Agent Flow Kit to import and prefer design-system guidance
  during frontend planning.
- The user approved the direction from the prior analysis: keep `flow-plan` as
  the planning entry point, add a separate `flow-design` support skill for
  design-system reasoning, and call it from `flow-plan` when frontend design is
  in scope.
- The attached Payn design guideline HTML is implementation-oriented evidence:
  it contains brand tokens, typography, spacing, radius, shadows, iconography,
  components such as buttons, header, hero, feature blocks, stats, pricing, and
  token JSON. It should be treated as an example of the kind of design system
  Agent Flow Kit must support, not as a hard-coded Payn-specific kit rule.
- Current kit distribution surfaces:
  - `manifest.json` declares entry and support skills and validates skill
    presence during install.
  - `templates/.codex/skills/flow-plan/SKILL.md` is the detailed Codex planning
    contract.
  - `templates/.claude/commands/flow-plan.md` is the detailed Claude slash
    command contract.
  - `templates/.claude/skills/flow-plan/SKILL.md` is a compatibility wrapper.
  - `templates/.codex/skills/context-loader/SKILL.md` and
    `templates/.claude/skills/context-loader/SKILL.md` load repo-local context.
  - `templates/AGENTS.md`, `templates/CLAUDE.md`, `README.md`, and
    `docs/agent-flow/*` document the portable workflow contract.
  - `templates/scripts/agent-flow-matrix-gate.py` validates plan quality in CI.
- Existing onboarding docs for this repository are present:
  - `docs/agent-flow/project-structure.md`
  - `docs/agent-flow/business-flows.md`
  - `docs/agent-flow/integration-scenarios.md`

### 1.2 Intent And Ambiguity Resolution

User intent: make frontend plans design-system aware without turning
`flow-plan` into a large design-analysis skill.

Resolved direction:

1. Add `flow-design` as a support skill, not an independent canonical planning
   entry point.
2. Add a `Frontend Design System Gate` to `flow-plan`.
3. When the gate is triggered, `flow-plan` invokes `flow-design` during the
   design phase.
4. If a planned UI maps to design-system components or tokens, the plan must
   follow those rules or record a concrete exception.
5. If no design-system artifact exists, the plan records the searched paths and
   falls back to existing source/component patterns.

Non-goals:

- Do not hard-code Payn-specific colors, components, or brand voice into the
  portable kit.
- Do not replace business-flow planning, regression-surface mapping, or
  Playwright evidence with design review.
- Do not make display-only direct edits require `flow-plan`; the existing
  display-only exception remains narrow and unchanged.
- Do not add a new external parsing dependency unless implementation proves the
  existing shell/Markdown/HTML inspection path is insufficient.

### 1.3 Questioning Decision

| Item | Decision |
| --- | --- |
| Questions asked | No |
| Requirement questions asked | No |
| Goal Confirmation | The user explicitly approved the prior direction: proceed with `flow-design` delegation and `flow-plan` frontend application. |
| No Questions Rationale | The user already chose the architectural direction. Repository evidence shows the extension points: `manifest.json`, Codex/Claude `flow-plan` surfaces, `context-loader`, AGENTS/CLAUDE templates, README, onboarding docs, and the matrix gate. This is a workflow-contract change, not product-specific business logic; actor, tenant, data ownership, schema, runtime route, and provider questions are not needed. |
| User answers | The user approved continuing with the support-skill delegation direction. |
| Unsafe assumptions? | None blocking. The implementation must keep the design-system mechanism generic and must not bake the Payn sample into portable kit behavior. |

### 1.4 Goal

Update Agent Flow Kit so frontend behavior-changing plans preferentially inspect
repo-local design-system artifacts, match planned UI against available
components/tokens/patterns, and freeze only when the plan either applies the
matching rules or records concrete waivers.

### 1.5 Scope / Non-Goals

In scope:

- Add `flow-design` support skill templates for Codex and Claude.
- Add design-system paths to context loading and user-facing instructions.
- Extend `flow-plan` templates with a `Frontend Design System Gate`.
- Add required plan output for design-system applicability and component
  matching when frontend planning is triggered.
- Add an optional target-repo design-system documentation template.
- Update `manifest.json`, README, AGENTS/CLAUDE templates, and kit-local
  onboarding docs.
- Update the matrix gate so behavior-affecting frontend plans must contain the
  design-system applicability section, while allowing that section to record
  "no design system found" with searched-path evidence.
- Validate through static grep checks, Python syntax checks, installer dry-run,
  and a focused matrix-gate fixture.

Out of scope:

- Importing the Payn design system as a permanent kit default.
- Implementing a visual renderer, Figma client, browser snapshot comparison, or
  design-token compiler.
- Requiring `flow-design` for direct display-only edits that are already allowed
  to skip `flow-plan`.
- Changing application UI code in any target repository.
- Changing install overwrite policy beyond adding portable templates and docs.

### 1.6 Acceptance Criteria

- [x] `flow-design` exists under both
      `templates/.codex/skills/flow-design/SKILL.md` and
      `templates/.claude/skills/flow-design/SKILL.md`.
- [x] `manifest.json` lists `flow-design` as a support skill, not as a canonical
      entry step.
- [x] `context-loader`, `templates/AGENTS.md`, and `templates/CLAUDE.md`
      instruct agents to read design-system docs when frontend planning is in
      scope.
- [x] `flow-plan` defines a `Frontend Design System Gate` with trigger
      conditions for screens, components, client JS, styles, public frontend
      assets, design-system attachments, branding, tokens, and component
      requests.
- [x] `flow-plan` requires a `Design System Applicability` section or table when
      frontend planning is triggered.
- [x] `flow-plan` requires a `Component Match Matrix` when planned UI maps to
      known design-system components.
- [x] Matching component/token/pattern rules must be planned for use unless the
      plan records a concrete waiver.
- [x] If no design system is available, the plan records the searched paths and
      falls back to existing source/component patterns.
- [x] The matrix gate rejects behavior-affecting frontend plans that omit the
      design-system applicability section.
- [x] README and kit-local onboarding docs explain the new support-skill flow.
- [x] Validation commands pass or record concrete blockers.

### 1.7 User Answers

No additional user answers were required. The user approved the support-skill
delegation direction.

## 2. Design

### 2.1 Affected Files And Modules

| File / area | Planned change |
| --- | --- |
| `templates/.codex/skills/flow-design/SKILL.md` | New Codex support skill for design-system intake, summarization, and frontend plan applicability analysis. |
| `templates/.claude/skills/flow-design/SKILL.md` | Mirror the Codex support skill for Claude parity. |
| `manifest.json` | Add `flow-design` to `support_skills`; keep `canonical_flow` unchanged. |
| `templates/.codex/skills/flow-plan/SKILL.md` | Add `Frontend Design System Gate`, invocation guidance for `flow-design`, required plan sections, and readiness checks. |
| `templates/.claude/commands/flow-plan.md` | Mirror the detailed gate and plan-template requirements. |
| `templates/.claude/skills/flow-plan/SKILL.md` | Add compatibility bullets for the new frontend design-system behavior. |
| `templates/.codex/skills/context-loader/SKILL.md` | Load design-system docs when frontend planning is in scope. |
| `templates/.claude/skills/context-loader/SKILL.md` | Mirror context-loader behavior. |
| `templates/AGENTS.md` / `templates/CLAUDE.md` | Add context-first guidance for `docs/agent-flow/design-system.md` and `docs/agent-flow/design-system/` when frontend work is planned. |
| `templates/docs/agent-flow/design-system.md` | New optional target-repo template describing design-system storage, source priority, tokens, components, patterns, and waivers. |
| `templates/.agent-flow/config.json` | Add optional default design-system path list for new installs. Existing target repos will preserve local config and can manual-merge. |
| `templates/scripts/agent-flow-matrix-gate.py` | Require `Design System Applicability` for behavior-affecting frontend plans when browser-affecting files are changed. |
| `README.md` | Explain design-system-aware frontend planning and `flow-design` support skill. |
| `docs/agent-flow/project-structure.md` | Record the new support skill and optional design-system docs. |
| `docs/agent-flow/business-flows.md` | Add or update the Agent Flow business flow for design-system-aware frontend planning. |
| `docs/agent-flow/integration-scenarios.md` | Add static and fixture scenarios for design-system plan coverage. |

### 2.2 Implementation Approach

Implement the smallest generic mechanism:

1. Add `flow-design` as a support skill.
   - It reads repo-local design-system artifacts from configured/default paths.
   - It can summarize an attached or repo-local design-system document into a
     durable `docs/agent-flow/design-system.md` or
     `docs/agent-flow/design-system/{name}.md` when the user asks to import it.
   - It produces plan-ready analysis rather than a separate implementation
     plan.
2. Extend `flow-plan` with a frontend-specific gate.
   - Trigger on frontend route/screen/component/client JS/style/public asset
     work, user wording about UI/design/brand/tokens/components, or an explicit
     design-system attachment.
   - Call `flow-design` before final implementation design.
   - Require design-system applicability output in the plan.
3. Keep `flow-plan` as the canonical planning artifact.
   - `flow-design` never freezes `docs/flow/{feature}/plan.md` by itself.
   - It returns design-system findings that `flow-plan` incorporates into
     `Design Policy And Library Selection`, `Design System Applicability`, and
     task/test matrices.
4. Add matrix-gate enforcement only for plans that already require
   behavior-changing frontend planning.
   - If changed files are browser-affecting and a plan is required, the plan
     must contain `Design System Applicability`.
   - The section may say "No design system found" only with searched-path
     evidence and fallback source/component patterns.
5. Preserve existing display-only bypass.
   - Direct minor style/layout/text edits that meet the existing presentation
     exception are not newly blocked.

### 2.3 Design System Contract

`docs/agent-flow/design-system.md` should use a compact structure like:

```markdown
# Design System

## Source Priority
Explicit user-provided design-system docs > repo-local design-system docs >
existing source/components/styles > general design taste.

## Intake Status
- Status: imported / no-design-system / partial / blocked
- Sources reviewed: ...

## Tokens
| Token group | Names | Values / roles | Usage |
| --- | --- | --- | --- |

## Components
| Component | Variants | Required rules | Allowed exceptions |
| --- | --- | --- | --- |

## Patterns
| Pattern | Applies to | Rules |
| --- | --- | --- |

## Voice / Copy
| Area | Do | Avoid |
| --- | --- | --- |

## Waiver Rules
- Waivers require a concrete reason, such as legacy component incompatibility,
  accessibility improvement, missing token, or explicit user instruction.
```

`flow-design` plan output should include:

```markdown
### Design System Applicability

| Check | Result | Evidence |
| --- | --- | --- |
| Design system searched | Yes | {paths} |
| Design system found | Yes/No | {source paths or fallback reason} |
| Applies to this plan | Yes/No/Partial | {screens/components/tokens matched} |
| Required waivers | Yes/No | {summary} |

### Component Match Matrix

| Planned UI | Design System Match | Rule To Apply | Source | Exception / Waiver |
| --- | --- | --- | --- | --- |
| Primary CTA | Button / Primary | Use primary token, radius, size, focus state | design-system.md | None |
```

### 2.4 Design Policy And Library Selection

| Decision Area | Selected Approach | Why It Fits | Alternatives Considered | New Dependency? | Risk / Mitigation |
| --- | --- | --- | --- | --- | --- |
| Skill shape | `flow-design` as support skill | Keeps `flow-plan` canonical while isolating design-system reasoning | Put all logic inside `flow-plan`; create independent `flow-design` entry flow | No | Support skill may be overlooked; mitigate with explicit `flow-plan` gate and matrix-gate section requirement. |
| Design-system storage | Optional `docs/agent-flow/design-system.md` plus `docs/agent-flow/design-system/` | Matches existing Agent Flow durable docs and preserves repo-local rules | Store only in `.claude/docs/DESIGN.md`; store in source-documents ledger | No | Target repos may already have local docs; installer preserves existing local files. |
| Enforcement | Require plan section for behavior-affecting frontend plans | Gives reviewers and CI a concrete check without making semantic design proof impossible | No CI enforcement; fully semantic component validator | No | False positives possible; allow "no design system found" with searched-path evidence. |
| Parsing | Agent-led extraction from HTML/Markdown/JSON/CSS using existing tools | Avoids new dependency and works with attached HTML like Payn guidelines | Bundle parser or token compiler | No | Extraction can be imperfect; mitigate with source snippets, component match matrix, and waivers. |
| Display-only bypass | Preserve existing bypass | User requested frontend planning behavior, not stricter direct edit blocking | Force all UI edits through plan | No | Minor direct edits may skip design-system check; documented as out of scope to avoid process drag. |

### 2.5 Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| `flow-plan` becomes too large and harder to maintain | Put detailed design-system analysis in `flow-design`; `flow-plan` only owns trigger and output contract. |
| Claude/Codex behavior diverges | Add both skill templates and mirror flow-plan wording across Codex skill, Claude command, and Claude compatibility skill. |
| Payn-specific sample leaks into portable kit | Use Payn only as an example in implementation validation notes; do not add Payn tokens as defaults. |
| Design-system section becomes vague boilerplate | Matrix gate checks section presence; plan template requires searched paths, match results, and concrete waivers. |
| Existing target repos lose local design rules | `docs/agent-flow/*` and `.agent-flow/config.json` are target-local or preserve-local under installer behavior; use manual merge for existing repos. |
| Gate false positives for frontend repos without a design system | Allow a valid section that records no design system found, searched paths, and fallback component/source patterns. |
| Display-only exception undermines design consistency | Keep scope limited to flow-plan frontend planning; note future enhancement if user wants direct display-only compliance checks. |

### 2.6 Residual Risk Preflight

| Risk ID | Category | Applies? | Evidence | Warning to user | Required countermeasure / environment | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RR-001 | Missed business flows | Yes | This changes AFK planning behavior for frontend workflows in installed repos. | Frontend planning can miss design-system constraints if not made explicit. | Update AFK business-flow docs and require design-system applicability in plans. | Resolved by planned docs/gate tasks |
| RR-002 | Natural-language plan quality | Yes | Design-system matching is semantic and cannot be fully proven by structure. | The matrix gate can require sections but cannot prove visual quality. | Require component match matrix, source evidence, waivers, and plan review. | Resolved by planned output contract |
| RR-003 | Runtime/external dependency gap | No | No runtime/provider/deploy path is involved. | N/A | N/A | Not triggered |
| RR-004 | Weak test infrastructure | Partial | Skills are natural-language workflows; current kit uses static and fixture validation. | There is no automated agent execution harness. | Use grep checks, py_compile, installer dry-run, and matrix-gate fixture. | Accepted with concrete validation |
| RR-005 | Reviewer/waiver quality | Yes | This is an Agent Flow contract and CI gate change. | Weak waivers could hide design-system drift. | Mark plan review required and require concrete design-system waivers. | Resolved by review requirement |

### 2.7 Runtime Causality Gate

Not triggered: this request changes workflow templates, documentation, and CI
gate behavior for planning. It does not involve a deployed app, provider,
secret, binding, remote data state, browser-network symptom, or production-only
runtime failure.

| Check | Evidence | Result |
| --- | --- | --- |
| Active deployed version | No deployed app/runtime is affected. | not triggered |
| Browser symptom vs server outcome | No browser symptom or server request exists. | not triggered |
| Runtime log | No runtime service is involved. | not triggered |
| Representative paths | Template and gate validation only. | docs/CI workflow only |
| Environment bindings | No secrets, env vars, DB, storage, or provider config. | not involved |
| Remote data state | No remote data. | not involved |
| Classification | Workflow-contract enhancement. | not triggered |

### 2.8 Bug Feedback Review

Not applicable: this is not a bug/regression report. It is a workflow
enhancement request. The prevention lesson is related to future UI drift:
frontend plans should not invent component behavior when a local design system
already defines matching components/tokens.

### 2.9 Flow Knowledge Update

Reusable kit-level flow knowledge is found.

| Item | Result |
| --- | --- |
| Existing business-flow docs reviewed | Yes: `docs/agent-flow/business-flows.md` |
| Existing integration-scenario docs reviewed | Yes: `docs/agent-flow/integration-scenarios.md` |
| New reusable business flow found | Yes: design-system-aware frontend planning in installed repos |
| New exception / permission / boundary path found | Yes: no design system found, partial component match, conflicting existing source pattern, display-only bypass |
| New side effect / external dependency found | No runtime side effect; CI gate behavior changes |
| New integration scenario found | Yes: matrix-gate fixture for frontend plan missing/present design-system section |
| Feature-local only | No: this should become portable kit knowledge |

Required documentation updates:

| Target document | Update needed? | Summary of update | Task ID |
| --- | --- | --- | --- |
| `docs/agent-flow/project-structure.md` | Yes | Add `flow-design`, optional design-system docs, and gate validation surface. | TASK-009 |
| `docs/agent-flow/business-flows.md` | Yes | Add/update AFK flow for design-system-aware frontend planning and CI enforcement. | TASK-009 |
| `docs/agent-flow/integration-scenarios.md` | Yes | Add static/gate scenario coverage for design-system applicability. | TASK-009 |

### 2.10 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Existing behavior | New behavior | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-001 | Developer installing kit into a target repo | `install.py --target ...` | Installer validates skills listed in `manifest.json` and copies templates. | Installer distributes `flow-design`, optional design-system docs, and updated flow-plan/gate behavior. | Validate manifest, copy new support skill/docs, preserve target-local config/docs. | Missing `SKILL.md`, target has existing local design-system docs, config manual merge needed. | Target-local design-system docs and config must not be overwritten without force. | Writes target workflow files and optional docs. | Partial install leaves flow-plan referring to missing flow-design. | Installer dry-run, manifest validation, py_compile. |
| AFK-005 | Coding agent planning frontend behavior changes | `flow-plan` / `/flow-plan` | Plans inspect business flows and UI precision, but do not require design-system matching. | Frontend plans run the design-system gate, incorporate `flow-design` findings, and record applicability/component match/waivers. | Load context, search design-system docs, run flow-design, map planned UI to tokens/components/patterns, write frozen plan. | No design system found; partial match; conflict with source pattern; vague waiver; user-provided attachment not yet imported. | Repo-local docs and explicit user design-system input outrank generic taste; existing source patterns are fallback when no design system exists. | Writes `docs/flow/{feature}/plan.md`; may update `docs/agent-flow/design-system.md` when importing. | Frontend plans invent inconsistent components or miss brand rules. | Static grep, plan-template review, matrix-gate fixture. |
| AFK-006 | Reviewing agent | `flow-plan-review` | Reviews plan risks and readiness. | Review checks design-system applicability and component-match waivers for frontend plans. | Inspect frozen plan, design-system source evidence, component match matrix, and waivers. | Missing section, no searched paths, vague waiver, stale design-system source. | Same-agent fallback must record reason if cross-agent unavailable. | Writes `plan-review.md`. | Review approves a frontend plan that ignores existing design rules. | Plan-review required before implementation. |
| AFK-009 | CI / reviewer | `agent-flow-matrix-gate.py` | Gate checks matrices, questioning decision, review requirement, and display-only bypass. | For browser-affecting behavior changes that require a plan, gate also requires design-system applicability. | Compute changed files, classify browser-affecting paths, locate plan, validate required section. | No git base, no plan, section missing, plan records no design system without searched paths. | Config remains target-tunable; display-only bypass remains narrow. | CI pass/fail. | Gate false negatives let frontend plans skip design-system reasoning. | Focused git fixture tests. |

### 2.11 Regression Surface Matrix

| Surface | Affected? | Covered flows | Evidence | Required verification |
| --- | --- | --- | --- | --- |
| Skill templates | Yes | AFK-001, AFK-005, AFK-006 | `templates/.codex/skills/*`, `templates/.claude/skills/*`, `templates/.claude/commands/flow-plan.md` | Static grep and documentation review |
| Manifest validation | Yes | AFK-001 | `manifest.json`, `install.py validate_templates()` | Installer dry-run |
| Context loading | Yes | AFK-005 | `context-loader`, AGENTS/CLAUDE templates | Static grep |
| CI/matrix gate | Yes | AFK-009 | `templates/scripts/agent-flow-matrix-gate.py` | py_compile and focused git fixture |
| Local-first docs/config | Yes | AFK-001, AFK-005 | `install.py` safe/local-first classification, `templates/.agent-flow/config.json`, new docs template | Installer dry-run and review |
| README/user guidance | Yes | AFK-001, AFK-005 | `README.md` | Documentation review |
| Browser runtime / Playwright | No | N/A | No app UI changes | No Playwright required |
| Schema/migrations/auth/providers | No | N/A | No runtime data or provider change | N/A |

### 2.12 Test Design Matrix

| Test ID | Level | Case type | Target | Data setup / preconditions | Scenario | Assertions | Covers flow/risk | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | Static grep | Regression | Flow-design distribution | Current checkout | Search for `flow-design`, `Design System Applicability`, `Component Match Matrix`, and `Frontend Design System Gate` across templates/docs. | Required terms exist in intended files. | AFK-005, AFK-006 | Command output |
| TEST-002 | Static grep | Regression | Design-system docs/context loading | Current checkout | Search for `docs/agent-flow/design-system.md`, `docs/agent-flow/design-system/`, and configured design-system paths. | Context guidance and docs template are present. | AFK-001, AFK-005 | Command output |
| TEST-003 | Syntax | Regression | Python scripts/hooks | Current checkout | Run `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py`. | Python files parse. | AFK-001, AFK-009 | Command output |
| TEST-004 | Installer smoke | Happy, boundary | Manifest/template distribution | Temporary target directory | Run `python3 install.py --target /tmp/agent-flow-kit-design-system-smoke --dry-run`. | Installer validates manifest and enumerates new support skill/doc files. | AFK-001 | Command output |
| TEST-005 | Matrix-gate fixture | Happy, exception, regression | `agent-flow-matrix-gate.py` | Temporary git repo with browser-affecting change and frozen plan | Run fixture where frontend plan omits section, then includes section. | Missing `Design System Applicability` fails; complete section passes. | AFK-009 | Fixture output |
| TEST-006 | Diff hygiene | Regression | Planned files | Current checkout | Run `git diff --check`. | No whitespace errors. | All | Command output |

### 2.13 Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-001 | Installer dry-run and manifest validation | Happy, exception, boundary, regression | None. |
| AFK-005 | Static template/docs checks for design-system gate and component matching | Happy, exception, boundary, regression | Automated semantic design proof is out of scope because agent skills are natural-language workflows; `flow-design` output contract, plan-review, and matrix-gate section validation are the concrete controls. |
| AFK-006 | Required plan-review before implementation | Happy, exception, regression | None; this is an Agent Flow contract change, so review is required. |
| AFK-009 | Matrix-gate fixture for frontend section requirement | Happy, exception, boundary, regression | None for gate code change. |

### 2.14 Plan Review Requirement

- Requirement: Required
- Reason: This changes Agent Flow contract behavior, support-skill
  distribution, context loading, README/user guidance, and CI/matrix gate
  enforcement. These are explicitly high-impact workflow-gate and installed-kit
  behavior changes.
- Triggered criteria: workflow gates, CI gate, install/distribution behavior,
  risky-path config/docs, shared Agent Flow contract, frontend planning
  behavior.

### 2.15 Playwright Integration Test Plan

No Playwright run is required for this kit change. The change affects workflow
templates, docs, and matrix-gate validation, not a visible browser runtime. If
future implementation adds a browser-rendered design-system preview, that
separate work must add Playwright evidence.

### 2.16 Migration / Runtime Enforcement

- Migration needed: No.
- Runtime validation: No deployed runtime.
- Enforcement path: Matrix-gate validation for frontend behavior-affecting
  plans.
- Validation commands:
  - `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py`
  - `python3 install.py --target /tmp/agent-flow-kit-design-system-smoke --dry-run`
  - focused matrix-gate git fixture for browser-affecting plan with/without
    `Design System Applicability`
  - targeted `rg` checks for design-system gate terms
  - `git diff --check`

### 2.17 Open Questions

None blocking.

Future optional decisions:

- Whether to promote `flow-design` from support skill to entry skill after it
  proves useful across several repositories.
- Whether to add visual screenshot comparison or design-token compilation after
  real target repos establish stable design-system artifact formats.
- Whether to tighten direct display-only edit checks against design-system
  rules; this plan intentionally leaves the current display-only bypass intact.

## 3. Tasks

### 3.1 Overview

- Total tasks: 12
- TDD / fixture tasks: 2
- DIRECT tasks: 10

### 3.2 Task List

#### TASK-001: Add `flow-design` support skill templates
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-001, AC-002, AC-006
- **Dependencies**: None
- **Details**:
  - Add `templates/.codex/skills/flow-design/SKILL.md`.
  - Add `templates/.claude/skills/flow-design/SKILL.md`.
  - Define modes for design-system import/summarization and frontend plan
    applicability analysis.
  - Require source paths, component matches, token/pattern findings, and
    waiver notes.
- **Test Requirements**:
  - [x] Covered by TEST-001.

#### TASK-002: Add optional design-system documentation template
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-003, AC-004, AC-007
- **Dependencies**: TASK-001
- **Details**:
  - Add `templates/docs/agent-flow/design-system.md`.
  - Include token, component, pattern, voice/copy, source-priority, and waiver
    sections.
  - Keep the template generic; do not include Payn-specific defaults.
- **Test Requirements**:
  - [x] Covered by TEST-002 and TEST-004.

#### TASK-003: Update manifest and optional config defaults
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-002, AC-003
- **Dependencies**: TASK-001, TASK-002
- **Details**:
  - Add `flow-design` to `manifest.json` `support_skills`.
  - Keep `canonical_flow` unchanged.
  - Add optional design-system path configuration to
    `templates/.agent-flow/config.json` for new installs.
- **Test Requirements**:
  - [x] Covered by TEST-004.

#### TASK-004: Update context-loading and entrypoint instructions
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-003
- **Dependencies**: TASK-002
- **Details**:
  - Update Codex and Claude `context-loader` skills.
  - Update `templates/AGENTS.md` and `templates/CLAUDE.md`.
  - Load design-system docs proportionally only when frontend/design work is in
    scope.
- **Test Requirements**:
  - [x] Covered by TEST-002.

#### TASK-005: Extend Codex `flow-plan` with Frontend Design System Gate
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-004 through AC-008
- **Dependencies**: TASK-001, TASK-004
- **Details**:
  - Add trigger conditions.
  - Require invoking `flow-design` when triggered.
  - Add required plan sections and readiness checklist items.
  - Preserve display-only bypass wording.
- **Test Requirements**:
  - [x] Covered by TEST-001.

#### TASK-006: Extend Claude `flow-plan` command and skill compatibility
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-004 through AC-008
- **Dependencies**: TASK-005
- **Details**:
  - Mirror detailed behavior in `templates/.claude/commands/flow-plan.md`.
  - Add compatibility bullets to
    `templates/.claude/skills/flow-plan/SKILL.md`.
- **Test Requirements**:
  - [x] Covered by TEST-001.

#### TASK-007: Update matrix gate for frontend design-system section enforcement
- [x] **Completed**
- **Type**: TDD / fixture
- **Requirements**: AC-009
- **Dependencies**: TASK-005, TASK-006
- **Details**:
  - Extend `templates/scripts/agent-flow-matrix-gate.py` to detect
    browser-affecting behavior plans and require
    `Design System Applicability`.
  - Accept a complete section that records no design system found with searched
    paths and fallback evidence.
  - Keep presentation-only bypass unchanged.
- **Test Requirements**:
  - [x] Add focused fixture for missing section failure.
  - [x] Add focused fixture for section present pass.
  - [x] Covered by TEST-003 and TEST-005.

#### TASK-008: Update README and user guidance
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-010
- **Dependencies**: TASK-005, TASK-006
- **Details**:
  - Explain `flow-design` as a support skill.
  - Explain frontend plan design-system applicability and waivers.
  - Explain that Payn-like systems can be imported, while the kit remains
    generic.
- **Test Requirements**:
  - [x] Covered by TEST-001 and documentation review.

#### TASK-009: Update kit-local Agent Flow docs
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-010
- **Dependencies**: TASK-001 through TASK-008
- **Details**:
  - Update `docs/agent-flow/project-structure.md`.
  - Update `docs/agent-flow/business-flows.md`.
  - Update `docs/agent-flow/integration-scenarios.md`.
- **Test Requirements**:
  - [x] Covered by TEST-001 and TEST-002.

#### TASK-010: Run validation commands
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-011
- **Dependencies**: TASK-001 through TASK-009
- **Details**:
  - Run py_compile.
  - Run installer dry-run.
  - Run targeted rg checks.
  - Run matrix-gate fixture.
  - Run git diff hygiene.
- **Test Requirements**:
  - [x] TEST-001 through TEST-006.

#### TASK-011: Create required plan review artifact before implementation
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Plan Review Requirement
- **Dependencies**: Current frozen plan
- **Details**:
  - Create `docs/flow/design-system-aware-flow-plan/plan-review.md` before
    implementation.
  - Prefer cross-agent review if available; otherwise record a concrete
    same-agent fallback reason.
- **Test Requirements**:
  - [x] Review artifact includes reviewed plan path, frozen marker,
    reviewer/agent metadata, status, findings, and decision.

#### TASK-012: Write implementation report after changes
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Implementation traceability
- **Dependencies**: TASK-010, TASK-011
- **Details**:
  - Write `docs/flow/design-system-aware-flow-plan/implementation_report.md`.
  - Include files changed, deviations from plan, validations, blockers, and
    residual risk.
- **Test Requirements**:
  - [x] Report includes command outcomes and any blockers.

## 4. Readiness

- [x] Requirements map to tasks.
- [x] User intent and current-state analysis is documented.
- [x] Goal Confirmation is documented, including desired outcome and completion
      signal.
- [x] Questioning Decision is documented.
- [x] No Questions Rationale is source-backed because no questions were asked.
- [x] Business/product ambiguity has been resolved or explicitly blocked.
- [x] Required onboarding docs exist for behavior-changing work.
- [x] Flow Knowledge Update target is explicit.
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or
      blockers.
- [x] Runtime Causality Gate is explicitly not triggered with source-backed
      reason.
- [x] Bug/regression review is explicitly not applicable.
- [x] Business flows map to required tests or blockers.
- [x] Integration Coverage Contract has concrete coverage or waivers.
- [x] Plan Review Requirement is `Required` with a concrete reason.
- [x] Validation commands are identified.
- [x] No Playwright evidence is required because no visible browser runtime is
      changed.

Implementation may proceed only after `flow-plan-review` is completed for this
frozen plan.

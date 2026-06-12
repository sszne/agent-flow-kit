# Design Principles Gate

<!-- frozen: v2 2026-06-12 -->
<!-- plan_author: claude-code -->

## 1. Requirements

### 1.1 Current State

- The user wants Agent Flow Kit to enforce reference to a repo-local
  architecture design-principles document (設計指針) during planning and
  implementation, so that functions with cohesive responsibilities are built as
  side-effect-free, loosely coupled modules.
- The user named three recurring anti-patterns the mechanism must guard
  against:
  1. design confusion caused by invoking vague "responsibility" (責務)
     arguments without a concrete ownership rule;
  2. Service-pattern abuse that breaks encapsulation by pulling domain logic
     out of the objects that own the data;
  3. implementing constraints outside the aggregate that should be
     encapsulated inside it.
- The user approved a 4-layer approach modeled on the existing Frontend Design
  System Gate: (1) a `templates/docs/agent-flow/design-principles.md` template,
  (2) a Design Principles Gate in `flow-plan` with a required plan section,
  (3) `flow-impl` architecture review referencing the same document, and
  (4) structural validation in `agent-flow-matrix-gate.py` modeled on
  `validate_design_system_applicability`.
- Current kit surfaces relevant to this change:
  - `templates/.claude/commands/flow-plan.md` and
    `templates/.claude/commands/flow-impl.md` fetch an architecture reference
    from a hard-coded external URL with "if unavailable, skip and note"
    semantics; there is no repo-local design-principles document.
  - `templates/.codex/skills/flow-plan/SKILL.md` has the Frontend Design
    System Gate but no architecture-principles equivalent.
  - `templates/.claude/skills/flow-plan/SKILL.md` and
    `templates/.claude/skills/flow-impl/SKILL.md` are compatibility wrappers.
  - `templates/.codex/skills/context-loader/SKILL.md` and the Claude mirror
    load design-system docs but not design-principles docs.
  - `templates/AGENTS.md` / `templates/CLAUDE.md` Context First lists do not
    mention a design-principles document.
  - `templates/.agent-flow/config.json` has `design_system_paths` but no
    design-principles equivalents.
  - `templates/scripts/agent-flow-matrix-gate.py` validates
    `Design System Applicability` for browser-affecting plans; no equivalent
    exists for module/architecture-affecting plans.
- Existing onboarding docs for this repository are present:
  `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`,
  `docs/agent-flow/integration-scenarios.md`.

### 1.2 Intent And Ambiguity Resolution

User intent: make architecture design-principles guidance a mandatory,
evidence-backed reference for behavior-changing module work, the same way
design-system guidance is mandatory for frontend work.

Resolved direction:

1. Add an optional-but-default target-repo document
   `docs/agent-flow/design-principles.md` distributed from
   `templates/docs/agent-flow/design-principles.md`, seeded with the user's
   principles and anti-patterns as adaptable defaults.
2. Add a `Design Principles Gate` to `flow-plan` (Codex skill, Claude command,
   Claude compatibility skill) that triggers for behavior-changing work
   touching modules, services, domain logic, shared logic, or data ownership.
3. Source priority: explicit user-provided principles > repo-local
   `docs/agent-flow/design-principles.md` > existing source conventions >
   external architecture URL (kept as fallback only).
4. The plan must include a `Design Principles Compliance` section recording
   searched paths, applicability, applied rules per anti-pattern, and concrete
   waivers. "No design principles document found" is valid only with searched
   paths and fallback source-convention evidence.
5. `flow-impl` architecture review reads the same local document first and
   re-checks the anti-pattern list before completion.
6. The matrix gate requires the section when changed risky files include
   module-code paths (`design_principles_affecting_prefixes`).

Non-goals:

- Do not build a semantic architecture analyzer; structural CI validation plus
  agent-led semantic compliance is the contract (same as design-system gate).
- Do not remove the external architecture URL outright; keep it as a fallback
  reference so existing installs do not silently lose guidance.
- Do not add a new support skill; the principles document is compact enough to
  read directly from `flow-plan`/`flow-impl` (unlike multi-artifact design
  systems that justified `flow-design`).
- Do not change application code in any target repository.
- Do not change the display-only bypass.

### 1.3 Questioning Decision

| Item | Decision |
| --- | --- |
| Requirement questions asked | No |
| Goal Confirmation | The user explicitly approved the proposed 4-layer mechanism ("お願いします") after seeing the concrete deliverables table, and supplied the seed principles and three anti-patterns verbatim. |
| No Questions Rationale | The user already chose the architectural direction and the enforcement model (mirror the Frontend Design System Gate). Repository evidence shows every extension point: the design-system precedent plan (`docs/flow/design-system-aware-flow-plan/plan.md`), gate script validator structure, config keys, context-loader/AGENTS/CLAUDE mirror surfaces, and installer classification. This is a workflow-contract change with no product actor, tenant, schema, runtime route, or provider ambiguity. |
| User answers used | The user's message defines the seed principle (side-effect-free loosely coupled modules) and the three anti-patterns; the user approved local-doc priority over the external architecture URL. |
| Remaining safe assumptions | Naming the document `design-principles.md` (English, matching kit conventions) for the user's 設計指針.md; seeding the template with the user's principles as adaptable defaults rather than an empty skeleton, because the user asked for these specific rules to be enforced. Both follow directly from the request and kit language rules. |

### 1.4 Goal

Behavior-changing plans for module/service/domain work must show evidence that
repo-local design principles were searched and applied (or concretely waived),
implementation must re-verify the same principles, and CI must reject plans
that skip the section — making 「設計指針.md を必ず参照する」 an enforced
contract instead of a convention.

### 1.5 Scope / Non-Goals

In scope:

- `templates/docs/agent-flow/design-principles.md` (new).
- Design Principles Gate in `flow-plan` surfaces (Codex skill, Claude command,
  Claude compatibility skill) with required plan section and readiness checks.
- Local-first architecture reference in `flow-plan`/`flow-impl` Claude
  commands (external URL demoted to fallback).
- `flow-impl` architecture review + completion checklist updates (Claude
  command, Codex skill, Claude compatibility skill).
- `context-loader` skills, `templates/AGENTS.md`, `templates/CLAUDE.md`
  context-first and quality-gate guidance.
- `templates/.agent-flow/config.json`: `design_principles_paths`,
  `design_principles_affecting_prefixes`, `design_principles_affecting_files`,
  `design_principles_excluded_segments`, `design_principles_excluded_extensions`.
- `templates/scripts/agent-flow-matrix-gate.py`:
  `validate_design_principles_compliance` (including weak-waiver rejection)
  plus negative-filtered trigger wiring.
- `README.md` and kit-local `docs/agent-flow/*` updates.
- Static grep checks, py_compile, installer dry-run, matrix-gate git fixture.

Out of scope:

- A new support skill or `manifest.json` change (no skill is added).
- Semantic/AST-based architecture validation.
- Retroactive enforcement on previously frozen plans in target repos.
- Changing installer overwrite policy (new template paths already classify:
  `docs/` template is local-first via target docs; commands/skills/scripts are
  safe-update).

### 1.6 Acceptance Criteria

- [x] AC-001: `templates/docs/agent-flow/design-principles.md` exists with
      Source Priority, Intake Status, Core Principles (side-effect-free pure
      logic, loose coupling, encapsulation), an Anti-Patterns table covering
      the three user-named patterns with required responses, decision rules
      for introducing Service classes, and Waiver Rules mirroring
      `design-system.md` (invalid-waiver list included).
- [x] AC-002: `flow-plan` (Codex skill + Claude command) defines a
      `Design Principles Gate` with trigger conditions for behavior-changing
      module/service/domain/shared-logic/data-ownership work, search paths
      (`design_principles_paths`, `docs/agent-flow/design-principles.md`,
      `.claude/docs/DESIGN.md`, existing source conventions), and local-first
      priority over the external architecture URL.
- [x] AC-003: the plan template requires a `Design Principles Compliance`
      section with checks `design principles searched` / `design principles
      found` / `applies to this plan` / `required waivers` plus a per-rule
      application table; READINESS checklists updated in both flow-plan
      surfaces; Claude compatibility skill gains a parity bullet.
- [x] AC-004: `flow-impl` Claude command architecture review reads the local
      design-principles document first, re-checks the three anti-patterns
      before completion, and the completion checklist includes them; Codex
      skill and Claude compatibility skill gain matching requirements.
- [x] AC-005: `context-loader` (both tools), `templates/AGENTS.md`, and
      `templates/CLAUDE.md` instruct reading `docs/agent-flow/design-principles.md`
      when behavior-changing module/domain work is in scope.
- [x] AC-006: `templates/.agent-flow/config.json` adds `design_principles_paths`,
      `design_principles_affecting_prefixes`/`_files`, and the negative-filter
      keys `design_principles_excluded_segments`/`_extensions` with defaults.
- [x] AC-007: `agent-flow-matrix-gate.py` requires `Design Principles
      Compliance` when risky changed files match module-code paths after the
      negative filter, accepts "no design principles document found" only with
      searched-path and fallback evidence, rejects weak waiver values in the
      compliance tables using the existing `WEAK_WAIVER_VALUES` /
      `WAIVER_REASON_MARKERS` helpers, and passes py_compile plus a focused
      git fixture (missing section fails; complete section passes;
      migration-only change does not trigger; config/migration-only change
      under a broad module root such as `src/db/migrations/` or `src/config/`
      does not trigger; weak waiver such as `low risk` or `manual` fails).
- [x] AC-008: README and kit-local `docs/agent-flow/*` document the new gate.
- [x] AC-009: validation commands pass or record concrete blockers.

### 1.7 Residual Risk Preflight

| Risk ID | Category | Applies? | Evidence | Warning to user | Required countermeasure / environment | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RR-001 | Missed business flows | Yes | This changes AFK planning/implementation behavior for module work in all installed repos. | Plans could miss architecture constraints if the gate trigger is too narrow. | Trigger from configurable module-code prefixes; update AFK business-flow docs. | Resolved by planned gate trigger + docs tasks |
| RR-002 | Natural-language plan quality | Yes | Principle compliance is semantic; CI can only check structure. | The gate cannot prove a Service is justified, only that the plan addressed it. | Require per-anti-pattern application rows, concrete waivers, plan review; same contract as design-system gate. | Resolved by output contract |
| RR-003 | Runtime/external dependency gap | No | No runtime/provider/deploy path involved. | N/A | N/A | Not triggered |
| RR-004 | Weak test infrastructure | Partial | Skills are natural-language workflows; kit uses static + fixture validation. | No automated agent execution harness exists. | grep checks, py_compile, installer dry-run, matrix-gate git fixture. | Accepted with concrete validation |
| RR-005 | Reviewer/waiver quality | Yes | Agent Flow contract + CI gate change under `scripts/`. | Weak waivers could hide architecture drift. | Plan review Required; invalid-waiver list in the new document and validator. | Resolved by review requirement |

### 1.8 Bug Feedback Review

Not applicable: not a bug/regression request. This is a workflow enhancement.
The prevention lesson it encodes: implementation drift toward Service-pattern
abuse and leaked aggregate constraints should be caught at plan time, not in
review.

### 1.9 Runtime Causality Gate

Not triggered: this request changes workflow templates, documentation, and CI
gate behavior. No deployed app, provider, secret, binding, remote data, or
browser-network symptom is involved.

### 1.10 Flow Knowledge Update

| Item | Result |
| --- | --- |
| Existing business-flow docs reviewed | Yes: `docs/agent-flow/business-flows.md` (AFK-005, AFK-007, AFK-009) |
| Existing integration-scenario docs reviewed | Yes: `docs/agent-flow/integration-scenarios.md` (SCN-011/SRV-006 precedent) |
| New reusable business flow found | Yes: design-principles-aware planning/implementation in installed repos |
| New exception / permission / boundary path found | Yes: no principles doc found; partial applicability; principle conflict with existing source pattern; vague waiver |
| New side effect / external dependency found | No runtime side effect; CI gate behavior changes |
| New integration scenario found | Yes: matrix-gate fixture for module-affecting plan with/without the compliance section |
| Feature-local only | No: portable kit knowledge |

Required documentation updates:

| Target document | Update needed? | Summary of update | Task ID |
| --- | --- | --- | --- |
| `docs/agent-flow/project-structure.md` | Yes | Add design-principles document and gate validation surface. | TASK-008 |
| `docs/agent-flow/business-flows.md` | Yes | Extend AFK-005/AFK-007/AFK-009 rows with design-principles gate behavior. | TASK-008 |
| `docs/agent-flow/integration-scenarios.md` | Yes | Add SCN-013/SRV-008 design-principles gate fixture scenarios. | TASK-008 |

## 2. Design

### 2.1 Affected Files And Modules

| File / area | Planned change |
| --- | --- |
| `templates/docs/agent-flow/design-principles.md` | New target-repo template: source priority, intake status, core principles, anti-patterns with required responses, Service-introduction decision rule, waiver rules. |
| `templates/.claude/commands/flow-plan.md` | Local-first architecture reference rule; new Step 8.3 `Design Principles Gate`; on-demand artifact rows; plan-template section `Design Principles Compliance` (inserted after Component Match Matrix; later sections renumbered); Step 15 consistency bullets; Phase 3 architecture-compliance step reads local doc first; READINESS checklist items. |
| `templates/.codex/skills/flow-plan/SKILL.md` | Mirror: `## Design Principles Gate` section after Frontend Design System Gate; plan-section list and readiness checklist updates. |
| `templates/.claude/skills/flow-plan/SKILL.md` | Compatibility bullet: same design-principles behavior. |
| `templates/.claude/commands/flow-impl.md` | Local-first architecture reference; architecture review step checks the principles doc and anti-pattern list; completion checklist items. |
| `templates/.codex/skills/flow-impl/SKILL.md` | Require design-principles re-check before completion for module work. |
| `templates/.claude/skills/flow-impl/SKILL.md` | Compatibility bullet. |
| `templates/.codex/skills/context-loader/SKILL.md` + Claude mirror | Load design-principles docs when behavior-changing module/domain work is in scope. |
| `templates/AGENTS.md` / `templates/CLAUDE.md` | Context First list entry; Quality Gates mention of Design Principles Compliance. |
| `templates/.agent-flow/config.json` | Add `design_principles_paths`, `design_principles_affecting_prefixes`, `design_principles_affecting_files`, `design_principles_excluded_segments`, `design_principles_excluded_extensions`. |
| `templates/scripts/agent-flow-matrix-gate.py` | `DESIGN_PRINCIPLES_COMPLIANCE_MARKER`, `DEFAULT_DESIGN_PRINCIPLES_*` defaults (prefixes, files, excluded segments, excluded extensions), `is_design_principles_path()`, `validate_design_principles_compliance()` with weak-waiver rejection, `main()` trigger wiring. |
| `README.md` | Document the gate alongside the design-system section. |
| `docs/agent-flow/project-structure.md`, `business-flows.md`, `integration-scenarios.md` | Kit-local knowledge updates. |

### 2.2 Implementation Approach

1. Document contract first: write `design-principles.md` template seeded with
   the user's principles as defaults that target repos adapt during
   onboarding/intake (Intake Status mirrors design-system.md).
2. Plan gate: trigger when the request changes runtime behavior in modules,
   services/actions, domain logic, shared logic, data ownership, or introduces
   new classes/modules/dependencies between modules. Display-only and
   docs-only work does not trigger. The gate searches configured paths and
   requires the compliance section; conflicts between the principles doc and
   existing source conventions must be recorded and confirmed, mirroring the
   design-system conflict rule.
3. Compliance section shape (added to plan templates):

```markdown
### Design Principles Compliance

| Check | Result | Evidence |
| --- | --- | --- |
| Design principles searched | Yes | {paths inspected} |
| Design principles found | Yes/No/Partial | {source paths or reason none found} |
| Applies to this plan | Yes/No/Partial | {modules/services/aggregates affected} |
| Required waivers | Yes/No | {summary of concrete waivers or "None"} |

| Principle / anti-pattern | Affected design element | How the plan applies it | Exception / waiver |
| --- | --- | --- | --- |
| {side-effect-free module / responsibility rule / service-pattern abuse / aggregate encapsulation} | {module/class/function} | {applied rule or fallback convention} | {None or concrete reason} |
```

4. Implementation re-check: `flow-impl` architecture review reads the same
   document and re-verifies the anti-pattern list; completion checklist gains
   the three anti-pattern items.
5. CI: `validate_design_principles_compliance` follows the
   `validate_design_system_applicability` structure (section present, no
   placeholders, ≥1 table row, required check phrases, "found: no" requires
   searched/fallback markers) and additionally enforces waiver strength:
   waiver/exception cells in the compliance tables that are not
   `None`/`N/A`-equivalent must contain a `WAIVER_REASON_MARKERS` marker and
   must not be a `WEAK_WAIVER_VALUES` entry (reusing the existing Integration
   Coverage Contract helpers), and a `Required waivers | Yes` check row must
   carry non-weak evidence. Trigger: any risky changed file matching
   `design_principles_affecting_prefixes` (default: `app/`, `pages/`,
   `components/`, `src/`, `lib/`, `hooks/`, `services/`, `features/`,
   `server/`, `packages/`, `apps/`) or `design_principles_affecting_files`
   (default: empty), MINUS an explicit negative filter so migration/config-only
   work under broad module roots does not trigger:
   `design_principles_excluded_segments` (default: `migrations`, `config`,
   `infra`, `docker` — matched against directory segments, catching
   `src/db/migrations/`, `lib/config/`, `packages/*/migrations/`) and
   `design_principles_excluded_extensions` (default: `.md`, `.json`, `.yml`,
   `.yaml`, `.toml`, `.ini`, `.env`, `.sql`, `.csv`, `.txt`, `.lock` — so
   config/data/migration-SQL-only diffs under `src/` do not trigger).
   Presentation-only paths are already excluded upstream.
6. External URL demotion: the architecture-reference rule in both Claude
   commands becomes "read `docs/agent-flow/design-principles.md` (and
   configured `design_principles_paths`) first; fetch the external
   architecture URL only as a fallback reference; on conflict, the repo-local
   document wins and the conflict is recorded".

### 2.3 Design Policy And Library Selection

| Decision Area | Selected Approach | Why It Fits | Alternatives Considered | New Dependency? | Risk / Mitigation |
| --- | --- | --- | --- | --- | --- |
| Gate shape | Inline gate in `flow-plan`, no new skill | Principles doc is one compact file; design systems needed `flow-design` because artifacts are multi-format | New `flow-principles` support skill | No | If the doc grows multi-file, promote to a support skill later; documented in Open Questions. |
| Document location | `docs/agent-flow/design-principles.md` template | Matches design-system.md placement and installer local-first behavior for target docs | `.claude/rules/architecture-principles.md`; extending `.claude/docs/DESIGN.md` | No | Rules files are tool-scoped and DESIGN.md is a decision log; agent-flow docs are the durable cross-agent home. |
| Seed content | Ship the user's principles/anti-patterns as adaptable defaults | The user asked for these specific rules to be enforced; an empty skeleton would not change agent behavior on day one | Empty skeleton like design-system.md | No | Target repos with different philosophies adapt during intake; Intake Status records adaptation. |
| Enforcement | Structural CI section check + agent semantic compliance + plan review | Proven contract from the design-system gate; CI cannot prove semantics (RR-002) | No CI check; semantic validator | No | False sense of security mitigated by per-anti-pattern table rows and concrete-waiver rules. |
| Trigger scope | Module-code prefixes subset of risky prefixes | Migration/config/infra-only changes have no module design surface; avoids gate noise | Require for every behavior-changing plan | No | Config-tunable per target repo via `design_principles_affecting_prefixes`. |
| External URL | Keep as fallback only | Removing it could silently drop guidance for repos relying on it | Delete the URL rules | No | Local-first wording makes precedence explicit. |

### 2.4 Design System Applicability

Not triggered: this plan changes workflow templates, CI gate logic, and
documentation only. No screens, components, frontend routes, client UI,
styles, or public frontend assets are affected (searched: changed-file list in
section 2.1; no browser-affecting paths).

### 2.5 Design Principles Compliance

| Check | Result | Evidence |
| --- | --- | --- |
| Design principles searched | Yes | `docs/agent-flow/design-principles.md` (kit root: absent), `.claude/docs/DESIGN.md` (template only), `.agent-flow/config.json` (absent at kit root) |
| Design principles found | No | This kit repo has no design-principles document yet; this plan creates the template. |
| Applies to this plan | Partial | Fallback to existing kit conventions: validator functions mirror `validate_design_system_applicability` (single-purpose functions, no shared mutable state); config keys mirror `design_system_paths` naming. |
| Required waivers | No | None — fallback source conventions are followed. |

| Principle / anti-pattern | Affected design element | How the plan applies it | Exception / waiver |
| --- | --- | --- | --- |
| Side-effect-free loosely coupled modules | `validate_design_principles_compliance()` | Pure function over plan text appending to an errors list, identical to sibling validators; no global state. | None |
| Vague-responsibility confusion | Gate trigger wiring in `main()` | Trigger computed from explicit config-backed path sets, not heuristic judgment. | None |
| Service-pattern abuse / aggregate encapsulation | Document + plan-template contract | These are semantic rules enforced through the new document and plan section, not kit Python code. | None |

### 2.6 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Existing behavior | New behavior | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-001 | Developer installing kit | `install.py --target ...` | Installer copies templates with local-first/safe-update classification. | Also distributes `design-principles.md` template and updated commands/skills/gate/config. | Validate manifest, copy files, preserve target-local docs/config. | Existing target `docs/agent-flow/design-principles.md` or local config must not be overwritten without force. | Target docs are local-first; commands/skills/scripts are safe-update. | Writes target workflow files. | Partial update leaves flow-plan requiring a section the gate does not know. | Installer dry-run, py_compile. |
| AFK-005 | Coding agent planning module behavior changes | `flow-plan` / `/flow-plan` | Plans require matrices and frontend design-system applicability but no architecture-principles evidence; external architecture URL is primary. | Module-affecting plans run the Design Principles Gate, record compliance per anti-pattern, and prefer the repo-local document over the external URL. | Load context, search principle paths, map affected modules/services/aggregates to rules, write compliance section, freeze. | No principles doc found; partial applicability; principle conflicts with existing source pattern; vague waiver; new Service class proposed without justification. | Repo-local doc and explicit user input outrank external URL and general taste; conflicts require confirmation. | Writes `docs/flow/{feature}/plan.md`. | Plans keep inventing Services or leaking aggregate constraints; or gate noise on non-module changes. | Static grep, plan-template review, matrix-gate fixture. |
| AFK-007 | Coding agent implementing | `flow-impl`, `team-implement` | Architecture review re-reads the external architecture document. | Architecture review re-reads the repo-local principles doc first and re-checks the three anti-patterns before completion. | Resolve plan, implement tasks, run principle re-check in review steps, report. | Implementation introduces an unplanned Service or out-of-aggregate constraint → plan update or user confirmation required. | Frozen-plan boundary unchanged. | Implementation report records compliance. | Drift between plan-time compliance and shipped code. | Static grep on flow-impl surfaces; review checklist. |
| AFK-009 | CI / reviewer | `agent-flow-matrix-gate.py` | Gate validates matrices, waivers, review, design-system section for browser changes. | For module-affecting behavior changes, gate also requires `Design Principles Compliance`. | Compute changed files, classify module paths, validate section. | Section missing; placeholders; "found: no" without searched/fallback evidence; migration-only change must not trigger. | Trigger paths config-tunable per target repo. | CI pass/fail. | False negatives let module plans skip principles; false positives block schema-only work. | py_compile + focused git fixture. |

### 2.7 Regression Surface Matrix

| Surface | Affected? | Covered flows | Evidence | Required verification |
| --- | --- | --- | --- | --- |
| Skill templates (Codex/Claude flow-plan, flow-impl, context-loader) | Yes | AFK-005, AFK-007 | Files listed in 2.1 | Static grep + documentation review |
| Slash commands (`flow-plan.md`, `flow-impl.md`) | Yes | AFK-005, AFK-007 | `templates/.claude/commands/*` | Static grep + review |
| CI/matrix gate | Yes | AFK-009 | `templates/scripts/agent-flow-matrix-gate.py` | py_compile + git fixture (new section trigger; existing design-system and review checks unchanged) |
| Installer/manifest | Yes (distribution only) | AFK-001 | `install.py` template iteration; no manifest change | Installer dry-run |
| Config template | Yes | AFK-005, AFK-009 | `templates/.agent-flow/config.json` | JSON parse via gate config load + dry-run |
| AGENTS/CLAUDE/README/onboarding docs | Yes | AFK-001, AFK-005 | Files listed in 2.1 | Documentation review + grep |
| Browser runtime / Playwright | No | N/A | No app UI changes | None |
| Schema/migrations/auth/providers | No | N/A | No runtime data or provider change | N/A |

### 2.8 Test Design Matrix

| Test ID | Level | Case type | Target | Data setup / preconditions | Scenario | Assertions | Covers flow/risk | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | Static grep | Regression | Gate terms across surfaces | Current checkout | Search `Design Principles Gate`, `Design Principles Compliance`, `design-principles.md`, `design_principles_paths` across templates/docs/README. | Required terms exist in all intended files; both Codex and Claude surfaces match. | AFK-005, AFK-007 | Command output |
| TEST-002 | Syntax | Regression | Python scripts | Current checkout | `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py templates/.claude/hooks/*.py templates/.codex/hooks/*.py` | All parse. | AFK-001, AFK-009 | Command output |
| TEST-003 | Installer smoke | Happy, boundary | Template distribution | Temp target dir | `python3 install.py --target {tmp} --dry-run` | New template enumerated; manifest validation passes. | AFK-001 | Command output |
| TEST-004 | Matrix-gate git fixture | Happy, validation, boundary, regression | `agent-flow-matrix-gate.py` | Temp git repo with frozen plan + module-code diff | Run gate with (a) module diff, plan missing section → fail; (b) module diff, complete section → pass; (c) root `migrations/`-only diff, no section → pass (not triggered); (d) "found: no" without searched paths → fail; (e) config/migration-only diff under a broad module root (`src/db/migrations/`, `src/config/`) → pass without section (not triggered); (f) complete section with weak waiver (`low risk`/`manual`) → fail. | Exit codes and error messages match expectations; existing checks still pass. | AFK-009 | Fixture output |
| TEST-005 | JSON/config | Validation | `templates/.agent-flow/config.json` | Current checkout | Parse JSON; confirm new keys present. | Valid JSON with three new keys. | AFK-005, AFK-009 | Command output |
| TEST-006 | Diff hygiene | Regression | All changed files | Current checkout | `git diff --check` | No whitespace errors. | All | Command output |

### 2.9 Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-001 | Installer dry-run + py_compile | Happy, boundary, regression | None. |
| AFK-005 | Static template checks for gate, section contract, source priority | Happy, validation, boundary, regression | Automated semantic proof of principle compliance is out of scope because plans are natural-language artifacts; the section contract, per-anti-pattern rows, concrete-waiver rules, and plan review are the enforcement layer (same waiver as the design-system gate). Permission cases out of scope because no actor/tenant model exists in kit templates. |
| AFK-007 | Static checks on flow-impl surfaces + review checklist content | Happy, regression | Side-effect cases out of scope because flow-impl changes are documentation-contract only; no runtime side effects exist. |
| AFK-009 | py_compile + git fixture for trigger, pass, fail, and not-triggered paths | Happy, validation, boundary, regression, side effect (CI pass/fail) | None for gate code change. |

### 2.10 Plan Review Requirement

- Requirement: Required
- Reason: This changes Agent Flow contract behavior (planning and
  implementation gates), CI/matrix gate enforcement under `scripts/`, install
  distribution content, and shared workflow templates for all installed
  repos — explicitly review-required high-impact workflow-gate work.
- Triggered criteria: workflow gates, CI gate, install/distribution behavior,
  Agent Flow contract changes, `scripts/` high-impact path.

### 2.11 Migration / Runtime Enforcement

- Migration needed: No.
- Migration enforcement path: N/A.
- Runtime validation command: N/A (no deployed runtime). Enforcement is the
  matrix gate; validation commands listed in 2.8.

### 2.12 Playwright Integration Test Plan

Not required: this change affects workflow templates, documentation, and CI
gate validation. No visible browser behavior or multi-step business UI
workflow exists. Evidence lane for `/flow-integration-test`: Lightweight
Evidence Allowed (docs/skill/CI-gate-only change) with the substitute checks
in 2.8.

## 3. Tasks

### 3.1 Overview

- Total tasks: 11
- TDD / fixture tasks: 1 (TASK-007)
- DIRECT tasks: 10

### 3.2 Task List

#### TASK-001: Create plan review artifact (gate for implementation)
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Plan Review Requirement
- **Dependencies**: Frozen plan
- **Details**: Create `docs/flow/design-principles-gate/plan-review.md` via
  cross-agent review (Codex reviews this claude-code plan). If Codex is
  unavailable, record a concrete same-agent fallback reason.
- **Test Requirements**:
  - [ ] Review artifact contains required metadata and APPROVED status before
        implementation tasks run.

#### TASK-002: Add `templates/docs/agent-flow/design-principles.md`
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-001
- **Dependencies**: TASK-001
- **Details**: Source Priority, Intake Status, Core Principles, Anti-Patterns
  table (three user patterns + required responses), Service-introduction
  decision rule, Waiver Rules with invalid-waiver list.
- **Test Requirements**:
  - [ ] Covered by TEST-001, TEST-003.

#### TASK-003: Update `templates/.agent-flow/config.json`
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-006
- **Dependencies**: TASK-002
- **Details**: Add `design_principles_paths`,
  `design_principles_affecting_prefixes`, `design_principles_affecting_files`,
  `design_principles_excluded_segments`, `design_principles_excluded_extensions`.
- **Test Requirements**:
  - [ ] Covered by TEST-005.

#### TASK-004: Extend Claude `flow-plan` command
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-002, AC-003
- **Dependencies**: TASK-002
- **Details**: Local-first architecture reference rule; Step 8.3 gate;
  artifact-condition rows; plan-template section insertion and renumbering;
  consistency/READINESS checklist items; Phase 3 compliance step update.
- **Test Requirements**:
  - [ ] Covered by TEST-001.

#### TASK-005: Extend Codex `flow-plan` skill + Claude compatibility skill
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-002, AC-003
- **Dependencies**: TASK-004
- **Details**: Mirror gate section, plan-section list, readiness checklist in
  `templates/.codex/skills/flow-plan/SKILL.md`; parity bullet in
  `templates/.claude/skills/flow-plan/SKILL.md`.
- **Test Requirements**:
  - [ ] Covered by TEST-001.

#### TASK-006: Extend `flow-impl` surfaces
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-004
- **Dependencies**: TASK-002
- **Details**: Claude command (local-first reference, architecture review
  step, completion checklist); Codex skill bullet; Claude compatibility skill
  bullet.
- **Test Requirements**:
  - [ ] Covered by TEST-001.

#### TASK-007: Extend matrix gate with `validate_design_principles_compliance`
- [x] **Completed**
- **Type**: TDD / fixture
- **Requirements**: AC-007
- **Dependencies**: TASK-003, TASK-004
- **Details**: Marker/defaults/validator/trigger wiring modeled on the
  design-system validator, plus the negative filter
  (`is_design_principles_path()` with excluded segments/extensions) and
  weak-waiver rejection reusing `WEAK_WAIVER_VALUES` /
  `WAIVER_REASON_MARKERS`; build git fixture covering fail, pass,
  not-triggered (root and broad-module-root), and weak-waiver cases before
  finalizing the change.
- **Test Requirements**:
  - [ ] Fixture (a)–(f) from TEST-004 pass.
  - [ ] TEST-002 passes.

#### TASK-008: Update context-loader, AGENTS.md, CLAUDE.md, README, kit-local docs
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-005, AC-008
- **Dependencies**: TASK-004, TASK-005, TASK-006
- **Details**: Both context-loader skills; Context First lists and Quality
  Gates wording in `templates/AGENTS.md`/`templates/CLAUDE.md`; README gate
  section; kit-local `project-structure.md`, `business-flows.md`
  (AFK-005/007/009 rows), `integration-scenarios.md` (SCN-013, SRV-008).
- **Test Requirements**:
  - [ ] Covered by TEST-001.

#### TASK-009: Run validation commands
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-009
- **Dependencies**: TASK-002 through TASK-008
- **Details**: TEST-001 through TEST-006.
- **Test Requirements**:
  - [ ] All commands pass or blockers recorded.

#### TASK-010: Write implementation report
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Traceability
- **Dependencies**: TASK-009
- **Details**: `docs/flow/design-principles-gate/implementation_report.md`
  with files changed, deviations, validation outcomes, evidence lane, and
  effectiveness metrics.
- **Test Requirements**:
  - [ ] Report includes command outcomes and lane metrics.

#### TASK-011: Final consistency pass
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-001 through AC-009
- **Dependencies**: TASK-010
- **Details**: Confirm Codex/Claude wording parity and that no template
  placeholder leaked into shipped files.
- **Test Requirements**:
  - [ ] Targeted grep for `{` placeholders in new sections outside intended
        template examples.

## 4. READINESS

### 4.1 Consistency Check
- [x] Every requirement maps to at least one task; every task maps to a requirement.
- [x] User intent and current-state analysis is documented.
- [x] Questioning Decision is documented; No Questions Rationale is source-backed.
- [x] Required onboarding docs exist (`project-structure.md`, `business-flows.md`, `integration-scenarios.md`).
- [x] Residual Risk Preflight documented with countermeasures.
- [x] Runtime Causality Gate explicitly not triggered with source-backed reason.
- [x] Frontend Design System Gate explicitly not triggered with source-backed reason.
- [x] Design Principles Compliance documented for this plan itself (fallback conventions; no doc exists yet at kit root).
- [x] Bug Feedback Review explicitly not applicable.
- [x] Flow Knowledge Update targets and task are explicit (TASK-008).
- [x] Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, Integration Coverage Contract are concrete; waivers carry reasons.
- [x] Plan Review Requirement is `Required` with a concrete reason; TASK-001 gates implementation.
- [x] Task dependencies form a valid DAG.
- [x] No migration; no Playwright evidence required (lightweight lane with substitute checks).

### 4.2 Notes
- v2 incorporates the two blocking findings from the Codex plan review of v1:
  (1) negative trigger filter (`design_principles_excluded_segments` /
  `design_principles_excluded_extensions`) so migration/config-only work under
  broad module roots does not trigger, with fixture case (e); (2) weak-waiver
  rejection inside `Design Principles Compliance` reusing the existing waiver
  helpers, with fixture case (f).
- Future option: promote the gate to a `flow-principles` support skill if
  target repos grow multi-file principle docs (mirrors the `flow-design`
  promotion note).
- Future option: add bug-knowledge prevention-pattern entries when a target
  repo's regression traces back to a principle violation the gate missed.

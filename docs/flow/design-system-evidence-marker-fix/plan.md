# Design System Evidence Marker Fix

<!-- frozen: v1 2026-06-12 -->
<!-- plan_author: claude-code -->

## 1. Requirements

### 1.1 Current State

- `validate_design_system_applicability` in
  `templates/scripts/agent-flow-matrix-gate.py` has an unreachable
  weak-evidence branch: when a plan records `Design system found | No`, the
  validator requires one of several evidence markers in the section, but the
  marker tuple includes the bare word `searched`.
- The required check label `design system searched` always appears in the same
  section (its absence is already reported by the required-phrase loop), so the
  bare `searched` marker is always satisfied and the error
  "Design System Applicability may record no design system found only when
  searched paths and fallback source/component evidence are documented." can
  never fire.
- The sibling validator `validate_design_principles_compliance` in the same
  file already shipped with the corrected behavior: its marker tuple excludes
  bare `searched` and carries an inline comment explaining the label
  collision. The deviation note in
  `docs/flow/design-principles-gate/implementation_report.md` (TASK-007) and
  its Observations section explicitly recommend this follow-up: "align it with
  the new evidence-bearing marker list and add a fixture case."
- The existing design-system gate fixture contract (SCN-011 / SRV-006 in
  `docs/agent-flow/integration-scenarios.md`) covers missing-section and
  complete-section variants only; it has no no-doc-without-evidence case, which
  is why the dead branch shipped unverified.

### 1.2 Intent And Ambiguity Resolution

User intent: make the design-system weak-evidence enforcement actually fire,
mirroring the already-reviewed design-principles fix, and prove both directions
(fail without evidence, pass with fallback evidence) with a git fixture.

Resolved direction:

1. Remove the bare `"searched"` entry from the marker tuple in
   `validate_design_system_applicability`, leaving only evidence-bearing
   markers: `paths inspected`, `fallback`, `existing source`,
   `existing component`, `source pattern`.
2. Add the same explanatory inline comment used by
   `validate_design_principles_compliance` (label collision rationale).
3. Build a focused temporary-git-repo fixture proving: (a) a browser-affecting
   plan recording `Design system found | No` without searched-path/fallback
   evidence fails the gate with the weak-evidence error; (b) the same plan
   with concrete `paths inspected` + `fallback` evidence passes; (c) a
   `Design system found | Yes` complete section still passes (regression).
4. Update SCN-011 / SRV-006 scenario rows so the no-doc-without-evidence
   variant is part of the durable fixture contract.

Non-goals:

- Do not change the design-principles validator, trigger wiring, config keys,
  or any other gate behavior.
- Do not change the marker semantics beyond removing the dead entry (the
  evidence-bearing list stays aligned with the design-principles validator's
  design-system-appropriate equivalents: `existing component` instead of
  `existing convention`/`source convention`).
- Do not add a CI workflow to this kit repository.

### 1.3 Questioning Decision

| Item | Decision |
| --- | --- |
| Requirement questions asked | No |
| Goal Confirmation | The request specifies the exact code change (remove bare `searched` from the tuple), the exact surviving markers, the fixture cases to add, the reference precedent, and the validation commands. |
| No Questions Rationale | The fix was already designed and review-approved once: `validate_design_principles_compliance` in the same file shipped with the identical correction and inline comment (see `docs/flow/design-principles-gate/plan.md` AC-007 and `implementation_report.md` TASK-007 deviation note, which names this exact follow-up). Repository evidence fully determines the change; no actor, schema, runtime, or provider ambiguity exists. |
| User answers used | The request text itself: marker list, fixture cases, fixture reference (`docs/flow/design-principles-gate/implementation_report.md` cases a-g), and required `python3 -m py_compile` validation. |
| Remaining safe assumptions | Fixture driver script is committed under `docs/flow/design-system-evidence-marker-fix/` as durable evidence (the scenario contract keeps using temporary git repositories at run time, so the current checkout is never mutated). |

### 1.4 Goal

The design-system no-doc weak-evidence branch becomes reachable and enforced:
plans claiming "no design system found" without documented searched paths and
fallback source/component evidence fail the gate, and the behavior is locked
in by a reusable git fixture.

### 1.5 Scope / Non-Goals

In scope:

- `templates/scripts/agent-flow-matrix-gate.py`: marker tuple fix + comment in
  `validate_design_system_applicability` only.
- New fixture driver
  `docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py`
  (builds temporary git repos, runs the gate, asserts exit codes and
  messages).
- `docs/agent-flow/integration-scenarios.md`: extend SCN-011 and SRV-006 rows
  with the no-doc-without-evidence variant.
- Validation: `python3 -m py_compile` on the gate script and the fixture,
  fixture run, `git diff --check`.

Out of scope:

- All other validators, trigger wiring, config schema, installer, manifest,
  flow-plan/flow-impl templates, README.
- `docs/agent-flow/bug-knowledge.md` (bug is fully preventable by flow
  improvement; see 1.8).

### 1.6 Acceptance Criteria

- [x] AC-001: the marker tuple in `validate_design_system_applicability`
      contains exactly `paths inspected`, `fallback`, `existing source`,
      `existing component`, `source pattern` (bare `searched` removed), with
      the label-collision comment mirroring the design-principles validator.
- [x] AC-002: fixture case (a) — browser-affecting diff with a frozen plan
      recording `Design system found | No` and no evidence markers — exits
      non-zero and reports the weak-evidence error message.
- [x] AC-003: fixture case (b) — same diff with `paths inspected` and
      `fallback` evidence in the section — exits 0.
- [x] AC-004: fixture case (c) — `Design system found | Yes` complete
      section — exits 0 (regression guard for the common path).
- [x] AC-005: `python3 -m py_compile templates/scripts/agent-flow-matrix-gate.py
      docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py`
      passes.
- [x] AC-006: SCN-011 and SRV-006 rows document the no-doc-without-evidence
      fail variant.
- [x] AC-007: no other behavior of the gate script changes
      (`git diff` limited to the marker tuple + comment in the gate script).

### 1.7 Residual Risk Preflight

| Risk ID | Category | Applies? | Evidence | Warning to user | Required countermeasure / environment | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RR-001 | Missed business flows | Partial | Newly enforced error could fail existing target-repo plans that legitimately claim "no design system" but used wording without the surviving markers. | Target repos updating the gate may see new CI failures until plans add `paths inspected`/`fallback` wording — this is the intended enforcement, same contract the design-principles validator already ships. | Fixture case (b) documents the passing wording; SCN-011/SRV-006 rows updated. | Accepted: intended tightening, mirrors reviewed precedent |
| RR-002 | Natural-language plan quality | Yes | Marker matching is substring-based; evidence quality stays semantic. | CI proves marker presence, not evidence truth. | Same contract as design-principles gate: structural CI + plan review. | Accepted by precedent |
| RR-003 | Runtime/external dependency gap | No | No runtime/provider/deploy path involved. | N/A | N/A | Not triggered |
| RR-004 | Weak test infrastructure | Partial | Kit has no unit-test harness; fixtures are the gate's regression net. | Dead branches can ship when fixtures omit a case — exactly this bug. | Commit the fixture driver as a durable artifact; extend scenario contract rows. | Resolved by TASK-003/TASK-004 |
| RR-005 | Reviewer/waiver quality | Yes | CI gate change under `scripts/` (high-impact path). | Unreviewed gate change could alter enforcement for all installed repos. | Plan review Required (cross-agent Codex review). | Resolved by TASK-001 |

### 1.8 Bug Feedback Review

| Item | Result |
| --- | --- |
| Previous plan found | Yes: `docs/flow/design-system-aware-flow-plan/plan.md` (introduced the validator) and `docs/flow/design-principles-gate/plan.md` (fixed the sibling). |
| Previous implementation report found | Yes: `docs/flow/design-principles-gate/implementation_report.md` — TASK-007 deviation note and Observations name this exact follow-up. |
| Previous integration evidence found | Yes: design-principles fixture cases (a)-(g) recorded in the same report; SCN-011/SRV-006 describe the original design-system fixture without a no-doc case. |
| Existing bug-knowledge entry found | No: `docs/agent-flow/bug-knowledge.md` does not exist in this repository. |

| Failure ID | Flow failure point | Evidence | Flow improvement possible? | Required action |
| --- | --- | --- | --- | --- |
| BF-004 | Test Design Matrix gap | SCN-011/SRV-006 fixture contract covered missing-section and complete-section variants only, so the no-doc weak-evidence branch shipped without a case proving it can fire. | Yes | Add fixture cases (a)/(b)/(c) and extend SCN-011/SRV-006 rows (TASK-003, TASK-004). |

Bug knowledge update:

- Needed: No
- Target: `docs/agent-flow/bug-knowledge.md`
- Entry summary: not needed — the bug class (validator branch whose trigger
  marker collides with an always-present label) is fully preventable by the
  flow improvement shipped here: every weak-evidence branch gets a fixture
  case proving it fires, now encoded in the SCN-011/SRV-006 contract.

### 1.9 Runtime Causality Gate

Not triggered: this request changes CI gate validation logic and fixture/doc
artifacts in the kit repository. No deployed app, provider, secret, binding,
remote data, or browser-network symptom is involved.

### 1.10 Flow Knowledge Update

| Item | Result |
| --- | --- |
| Existing business-flow docs reviewed | Yes: `docs/agent-flow/business-flows.md` AFK-009 row already describes gate rejection behavior generically; no row change required. |
| Existing integration-scenario docs reviewed | Yes: `docs/agent-flow/integration-scenarios.md` SCN-011, SRV-006. |
| New reusable business flow found | No new flow; existing AFK-009 enforcement is corrected. |
| New exception / permission / boundary path found | Yes: no-doc claim without searched-path/fallback evidence now fails for browser-affecting plans. |
| New side effect / external dependency found | No. |
| New integration scenario found | Yes: no-doc-without-evidence fail variant joins the SCN-011/SRV-006 fixture contract. |
| Feature-local only | No: portable kit knowledge. |

Required documentation updates:

| Target document | Update needed? | Summary of update | Task ID |
| --- | --- | --- | --- |
| `docs/agent-flow/integration-scenarios.md` | Yes | Extend SCN-011 and SRV-006 with the no-doc-without-evidence fail variant. | TASK-004 |
| `docs/agent-flow/business-flows.md` | No | AFK-009 already covers "rejects risky changes with missing/weak evidence" generically. | — |
| `docs/agent-flow/bug-knowledge.md` | No | Preventable by flow improvement (1.8). | — |

## 2. Design

### 2.1 Affected Files And Modules

| File / area | Planned change |
| --- | --- |
| `templates/scripts/agent-flow-matrix-gate.py` | Remove `"searched",` from the no-design-system marker tuple in `validate_design_system_applicability`; add the label-collision comment mirroring `validate_design_principles_compliance`. |
| `docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py` | New fixture driver: builds temporary git repos (base commit with onboarding docs + gate script + component, feature branch with browser-affecting diff + plan variant), runs the gate with `--base`, asserts exit codes and stderr messages for cases (a)/(b)/(c). |
| `docs/agent-flow/integration-scenarios.md` | SCN-011 / SRV-006 row extension. |

### 2.2 Implementation Approach

1. Marker tuple fix (mirror of the reviewed design-principles correction):

```python
    # Note: bare "searched" would always match the "design system searched"
    # check label itself, so only evidence-bearing markers are accepted here.
    if no_design_system and not any(
        marker in lower_section
        for marker in (
            "paths inspected",
            "fallback",
            "existing source",
            "existing component",
            "source pattern",
        )
    ):
```

2. Fixture design. Each case builds a temporary git repo shaped so only the
   target validator branch varies:
   - Base commit: `docs/agent-flow/{project-structure,business-flows,integration-scenarios}.md`
     (onboarding docs must exist), `scripts/agent-flow-matrix-gate.py` (copy of
     the fixed script; `REPO_ROOT` resolves to the fixture repo), and
     `components/widget.tsx`.
   - Feature branch: behavior-changing edit to `components/widget.tsx`
     (multi-line logic change so the presentation-only classifier cannot
     bypass it) plus `docs/flow/test-feature/plan.md`.
   - The plan variant carries everything the gate requires so only the
     Design System Applicability section differs per case: frozen marker,
     four required matrices with concrete rows, Integration Coverage Contract
     with waiver column and all six case types, Questioning Decision with
     No Questions Rationale, Plan Review Requirement `Optional` with a
     concrete reason (`components/` is not a review-required prefix, so no
     plan-review.md is needed), a valid Design Principles Compliance section
     (`components/*.tsx` also matches the design-principles trigger), and a
     Playwright Integration Test Plan marker (required for browser changes).
   - Case (a): `Design system found | No`, evidence cells deliberately free of
     all five markers → expect exit 1 and the weak-evidence message.
   - Case (b): same, but searched row says `Paths inspected: ...` and found
     row says `fallback: existing component patterns ...` → expect exit 0.
   - Case (c): `Design system found | Yes` with concrete evidence → expect
     exit 0.
   - Gate invocation: `python3 scripts/agent-flow-matrix-gate.py --base main`
     run inside the fixture repo.
3. Scenario contract: extend SCN-011 steps/expected-result and SRV-006
   assertions with "no-doc claim without searched-path/fallback evidence
   fails".

### 2.3 Design Policy And Library Selection

| Decision Area | Selected Approach | Why It Fits | Alternatives Considered | New Dependency? | Risk / Mitigation |
| --- | --- | --- | --- | --- | --- |
| Marker list | Exact mirror of the reviewed design-principles fix (minus convention-specific entries, plus `existing component`) | Same bug class, same reviewed remedy; keeps the two validators symmetric | Inventing a new evidence grammar | No | None — strict subset removal of a dead entry |
| Fixture location | Committed driver under `docs/flow/design-system-evidence-marker-fix/` | RR-004: ad-hoc temp fixtures let this dead branch ship once already; a committed driver is rerunnable evidence | /tmp-only ad-hoc script (precedent) | No | Driver still builds repos in `tempfile` dirs, so the checkout is never mutated |
| Fixture scope | Three cases focused on the changed branch | The broader gate surface is already covered by SCN-007/SRV-005 and the design-principles fixture; focused cases keep signal high | Re-running the full (a)-(g) suite | No | Case (c) guards the common found-Yes path |

### 2.4 Design System Applicability

Not triggered: this plan changes CI gate logic, a fixture script, and
documentation. No screens, components, frontend routes, client UI, styles, or
public frontend assets are affected (searched: changed-file list in 2.1; no
browser-affecting paths).

### 2.5 Design Principles Compliance

| Check | Result | Evidence |
| --- | --- | --- |
| Design principles searched | Yes | `docs/agent-flow/design-principles.md` (kit root: absent), `templates/docs/agent-flow/design-principles.md` (template for target repos), `.claude/docs/DESIGN.md` (template only) |
| Design principles found | No | The kit repository itself has no design-principles document; fallback to existing source pattern: sibling validator `validate_design_principles_compliance` in the same file defines the corrected marker contract this change mirrors. |
| Applies to this plan | Partial | Validator stays a side-effect-free pure function over plan text; no new coupling, class, or service is introduced. |
| Required waivers | No | None — fallback source conventions are followed. |

| Principle / anti-pattern | Affected design element | How the plan applies it | Exception / waiver |
| --- | --- | --- | --- |
| Side-effect-free loosely coupled modules | `validate_design_system_applicability()` | Change is data-only (tuple literal + comment); function signature, purity, and call sites unchanged. | None |
| Vague-responsibility confusion | Marker tuple | Responsibility stays explicit: tuple holds evidence markers only; the colliding check label is excluded by documented rule. | None |
| Service-pattern abuse / aggregate encapsulation | N/A | No new orchestration or extracted logic. | None |

### 2.6 Business Flow Matrix

| Flow ID | Actor / scope | Entry point | Existing behavior | New behavior | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AFK-009 | CI / reviewer | `agent-flow-matrix-gate.py` | Browser-affecting plans claiming `Design system found | No` always pass the weak-evidence check because bare `searched` matches the check label. | The weak-evidence error fires unless the section documents `paths inspected`/`fallback`/`existing source`/`existing component`/`source pattern` evidence. | Compute changed files, detect browser change, validate section, pass with evidence. | No-doc claim without evidence markers → fail with the weak-evidence message; missing section / placeholders / missing check rows fail as before. | Trigger paths remain config-tunable (`browser_affecting_prefixes`/`_files`). | CI pass/fail only. | Newly enforced error could surprise target repos with thin no-doc wording; found-Yes path must stay green. | Fixture cases (a)/(b)/(c) + py_compile. |
| AFK-005 | Coding agent planning frontend work | `flow-plan` | Plan template already instructs recording searched paths and fallback evidence for no-doc claims. | Unchanged template; CI now actually enforces the existing instruction. | Write Design System Applicability with evidence. | Thin no-doc wording now blocks at gate instead of silently passing. | None. | Plan artifacts only. | Low: instruction already documented in flow-plan/design-system templates. | SCN-011 contract row update. |

### 2.7 Regression Surface Matrix

| Surface | Affected? | Covered flows | Evidence | Required verification |
| --- | --- | --- | --- | --- |
| `validate_design_system_applicability` no-doc branch | Yes (intended) | AFK-009 | 2.2 step 1 | Fixture cases (a)/(b) |
| `validate_design_system_applicability` found-Yes path | Must stay green | AFK-009 | Same function | Fixture case (c) |
| Other validators (design-principles, review, migration, coverage contract, questioning) | No code change | AFK-009 | Diff limited to one tuple + comment | Fixture plans exercise them implicitly (all must pass in cases b/c); py_compile |
| flow-plan/flow-impl templates, installer, config, manifest | No | — | Not touched | `git diff --check` scope check |
| Browser runtime / Playwright | No | — | No app UI | None |
| Schema/migrations/auth/providers | No | — | No runtime data or provider change | None |

### 2.8 Test Design Matrix

| Test ID | Level | Case type | Target | Data setup / preconditions | Scenario | Assertions | Covers flow/risk | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | Syntax | Regression | Gate script + fixture driver | Current checkout | `python3 -m py_compile templates/scripts/agent-flow-matrix-gate.py docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py` | Both parse. | AFK-009 | Command output |
| TEST-002 | Git fixture | Validation, boundary | No-doc branch (case a) | Temp git repo, browser diff, plan with found-No and marker-free evidence cells | Run gate with `--base main` | Exit 1; stderr contains "may record no design system found only". | AFK-009 / AC-002 | Fixture output |
| TEST-003 | Git fixture | Happy, boundary | No-doc branch with evidence (case b) | Same repo shape; section carries `Paths inspected:` and `fallback:` wording | Run gate | Exit 0. | AFK-009 / AC-003 | Fixture output |
| TEST-004 | Git fixture | Happy, regression | Found-Yes path (case c) | Same repo shape; `Design system found | Yes` | Run gate | Exit 0. | AFK-009 / AC-004 | Fixture output |
| TEST-005 | Static diff review | Regression | Whole gate script | Current checkout | `git diff templates/scripts/agent-flow-matrix-gate.py` | Diff touches only the marker tuple and comment. | AC-007 | Diff output |
| TEST-006 | Diff hygiene | Regression | All changed files | Current checkout | `git diff --check` | No whitespace errors. | All | Command output |

### 2.9 Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| AFK-009 | py_compile + git fixture for fail, pass-with-evidence, and found-Yes paths | Happy, validation, boundary, regression, side effect (CI pass/fail) | None. |
| AFK-005 | Scenario-contract row update (SCN-011/SRV-006) | Happy, regression | Permission cases out of scope because no actor/tenant model exists in kit templates (same waiver as prior gate plans). Live target-repo verification out of scope because target repos receive the change via installer updates; fixture is the contract evidence. |

### 2.10 Plan Review Requirement

- Requirement: Required
- Reason: This changes CI/matrix gate enforcement under `scripts/`
  (plan-review-required high-impact path) and alters Agent Flow contract
  behavior for every installed repository, even though the diff is one tuple
  entry plus a comment.
- Triggered criteria: workflow gates, CI gate behavior, `scripts/` high-impact
  path, Agent Flow contract change.

### 2.11 Migration / Runtime Enforcement

- Migration needed: No.
- Migration enforcement path: N/A.
- Runtime validation command: N/A (no deployed runtime). Enforcement is the
  matrix gate itself; validation commands listed in 2.8.

### 2.12 Playwright Integration Test Plan

Not required: CI gate logic, fixture, and documentation only — no visible
browser behavior or multi-step business UI workflow. Evidence lane for
`/flow-integration-test`: Lightweight Evidence Allowed with TEST-001 through
TEST-006 as substitute evidence.

## 3. Tasks

### 3.1 Overview

- Total tasks: 6
- TDD / fixture tasks: 1 (TASK-003)
- DIRECT tasks: 5

### 3.2 Task List

#### TASK-001: Create plan review artifact (gate for implementation)
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Plan Review Requirement (2.10)
- **Dependencies**: Frozen plan
- **Details**: Cross-agent review — Codex reviews this claude-code plan;
  write `docs/flow/design-system-evidence-marker-fix/plan-review.md` with the
  required metadata and APPROVED status. If Codex is unavailable, record a
  concrete same-agent fallback reason.
- **Test Requirements**:
  - [ ] Review artifact metadata matches the current frozen marker and is
        APPROVED before TASK-002 runs.

#### TASK-002: Fix the marker tuple in `validate_design_system_applicability`
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-001, AC-007
- **Dependencies**: TASK-001
- **Details**: Remove `"searched",`; add the label-collision comment mirroring
  `validate_design_principles_compliance`. No other lines change.
- **Test Requirements**:
  - [ ] TEST-001, TEST-005.

#### TASK-003: Build and run the focused git fixture
- [x] **Completed**
- **Type**: TDD / fixture
- **Requirements**: AC-002, AC-003, AC-004
- **Dependencies**: TASK-002
- **Details**: Write
  `docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py`
  per 2.2 step 2; run cases (a)/(b)/(c); confirm case (a) error text matches
  the weak-evidence message.
- **Test Requirements**:
  - [ ] TEST-002, TEST-003, TEST-004 pass.

#### TASK-004: Update integration-scenario contract rows
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-006
- **Dependencies**: TASK-003
- **Details**: Extend SCN-011 steps/expected-result and SRV-006 assertions in
  `docs/agent-flow/integration-scenarios.md` with the no-doc-without-evidence
  fail variant.
- **Test Requirements**:
  - [ ] Row text names the new variant.

#### TASK-005: Run validation commands
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: AC-005, AC-007
- **Dependencies**: TASK-002 through TASK-004
- **Details**: TEST-001 through TEST-006.
- **Test Requirements**:
  - [ ] All commands pass or blockers recorded.

#### TASK-006: Write implementation report
- [x] **Completed**
- **Type**: DIRECT
- **Requirements**: Traceability
- **Dependencies**: TASK-005
- **Details**:
  `docs/flow/design-system-evidence-marker-fix/implementation_report.md` with
  files changed, validation outcomes, evidence lane, and effectiveness
  metrics.
- **Test Requirements**:
  - [ ] Report includes command outcomes and lane metrics.

## 4. READINESS

### 4.1 Consistency Check
- [x] Every requirement maps to at least one task; every task maps to a requirement.
- [x] User intent and current-state analysis is documented.
- [x] Questioning Decision is documented; No Questions Rationale is source-backed.
- [x] Required onboarding docs exist (`project-structure.md`, `business-flows.md`, `integration-scenarios.md`).
- [x] Residual Risk Preflight documented with countermeasures.
- [x] Runtime Causality Gate explicitly not triggered with source-backed reason.
- [x] Frontend Design System Gate explicitly not triggered with source-backed reason (2.4).
- [x] Design Principles Compliance documented for this plan itself (2.5, fallback source pattern).
- [x] Bug Feedback Review documented with BF classification and prevention action (1.8).
- [x] Flow Knowledge Update targets and task are explicit (TASK-004).
- [x] Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, Integration Coverage Contract are concrete; waivers carry reasons.
- [x] Plan Review Requirement is `Required` with a concrete reason; TASK-001 gates implementation.
- [x] Task dependencies form a valid DAG.
- [x] No migration; no Playwright evidence required (lightweight lane with substitute checks).

### 4.2 Notes
- The fix is intentionally asymmetric in one detail: the design-system marker
  list keeps `existing component` (component evidence fits frontend fallback)
  where the design-principles list uses `existing convention`/`source
  convention`. Both lists share `paths inspected`, `fallback`,
  `existing source`, `source pattern`.
- Committing the fixture driver (rather than the prior ad-hoc /tmp pattern) is
  the flow improvement that prevents this bug class from recurring (1.8).

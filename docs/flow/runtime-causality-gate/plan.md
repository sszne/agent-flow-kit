# Runtime Causality Gate For Flow Plan

## 1. Requirements

### 1.1 Current State

- `flow-plan` already requires Residual Risk Preflight, Bug Feedback Review, Business Flow Matrix, Regression Surface Matrix, Test Design Matrix, and Integration Coverage Contract.
- Runtime/external dependency risk exists as `RR-003`, but the current template does not force agents to classify whether a production-only symptom is caused by code, environment, deployed artifact, binding/secret, remote data, or provider/runtime behavior before proposing code changes.
- Install-time onboarding surveys runtime entrypoints and operations, but it does not explicitly inventory runtime-causality signals such as deploy platform, active release verification, provider sandboxes, log/tail commands, smoke commands, bindings/secrets, and production-only failure modes.
- Recent auth/CORS/Cloudflare work showed that browser CORS symptoms can be misleading when Worker runtime outcomes such as `exceededCpu` or app-level `401` are the real cause.

### 1.2 Intent And Ambiguity Resolution

- User intent: write the proposed policy into `agent-flow-kit` so installed repos improve `flow-plan` behavior and detect environment-caused issues earlier.
- Ambiguity resolution: no user question is required because the requested policy is explicit and the target repo/file family is supplied.
- No Questions Rationale: existing kit files show the relevant extension points: `templates/.codex/skills/flow-plan/SKILL.md`, `templates/.claude/commands/flow-plan.md`, onboarding skills, and residual-risk documentation. The change is process guidance, not app runtime behavior.

### 1.3 Goal

- `flow-plan` must include a Runtime Causality Gate when symptoms may involve deployment, external runtime, provider, secrets/bindings, remote data, browser/network masking, or production-only behavior.
- Agent Flow onboarding must help installed repos discover and document these runtime-causality signals so future plans can use concrete commands/evidence instead of guessing.
- The gate must prevent jumping to behavior-changing code when the failure classification is still unknown and runtime evidence is available or required.

### 1.4 Scope / Non-Goals

In scope:

- Update Codex and Claude flow-plan templates.
- Update onboarding survey/scenario templates so install-time onboarding inventories runtime causality evidence.
- Update residual-risk docs with the policy and checklist.
- Update README summary if useful.

Non-goals:

- Do not implement repo-specific Cloudflare commands into every target repo.
- Do not add hard CI validation for the new section in this change.
- Do not overwrite target repos or run installer.

### 1.5 Acceptance Criteria

- `flow-plan` instructions define trigger conditions for Runtime Causality Gate.
- Required plan shape/readiness includes runtime-causality classification when applicable.
- Onboarding prompts collect runtime/deploy/log/smoke/binding/provider evidence.
- Integration scenario design includes provider/runtime smoke and blocker documentation.
- Documentation clearly answers: yes, install-time onboarding can detect likely environment-caused risk and improve future `flow-plan` checks by writing project-specific evidence into `docs/agent-flow/*`.

### 1.6 Questioning Decision And User Answers

- Questioning decision: no questions needed.
- Evidence used: user explicitly requested the policy; kit template files and residual-risk docs identify the implementation points.
- User answer captured: proceed with the proposed Runtime Causality Gate policy and make onboarding detect this class of risk.

## 2. Design

### 2.1 Affected Files And Modules

- `templates/.codex/skills/flow-plan/SKILL.md`
- `templates/.claude/commands/flow-plan.md`
- `templates/.claude/skills/flow-plan/SKILL.md`
- `templates/.codex/skills/project-structure-survey/SKILL.md`
- `templates/.claude/skills/project-structure-survey/SKILL.md`
- `templates/.codex/skills/integration-scenario-design/SKILL.md`
- `templates/.claude/skills/integration-scenario-design/SKILL.md`
- `templates/docs/agent-flow-residual-risk-countermeasures.md`
- `README.md`

### 2.2 Implementation Approach

1. Add a Runtime Causality Gate to flow-plan:
   - trigger examples: browser CORS/ERR_FAILED, Cloudflare/Pages/D1/R2/KV/Worker/edge runtime, production-only symptoms, auth/session/cookie/secret/deploy artifacts, `503`, `1102`, `exceededCpu`, `timeout`, reset/deploy success followed by use-path failure;
   - required classification: code defect, environment/ops defect, data defect, deploy artifact mismatch, provider/runtime defect, inconclusive;
   - required evidence table: active deployed version, browser symptom vs server outcome, runtime logs, representative path, bindings/secrets, data state, classification.
2. Add the gate to plan readiness.
3. Update onboarding project survey to inventory runtime-causality signals during install-time onboarding.
4. Update integration scenario design to require runtime/provider smoke scenarios and blocker language.
5. Update residual-risk docs and README.

### 2.3 Design Policy And Library Selection

- No new dependency.
- Keep the policy portable: describe evidence classes and examples, not Cloudflare-only commands as mandatory defaults.
- Mention Cloudflare as an example because it is a common Worker/D1/Pages runtime, but keep the gate equally applicable to Vercel, AWS, GCP, Fly, Supabase, Firebase, Stripe, LINE, mail providers, queues, and search services.

### 2.4 Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Gate becomes too heavy for simple local bugs | Planning slows down | Trigger only when runtime/environment indicators are present. |
| Agents treat the gate as checklist theater | Still misses cause | Require classification and representative path evidence, not just section presence. |
| Onboarding guesses commands incorrectly | Bad docs | Require inferred facts to be labeled and blockers to be explicit. |
| Cloudflare-specific language narrows portability | Kit less reusable | Use provider-neutral language with Cloudflare examples. |

### 2.5 Residual Risk Preflight

- RR-003 applies: external runtime/deploy/provider behavior can invalidate local-only conclusions.
- RR-005 applies: vague manual waivers can hide production-only failures.
- Countermeasure: new Runtime Causality Gate before code-change design when triggered.

### 2.6 Bug Feedback Review

- Failure classification: Residual Risk Preflight miss and Integration Coverage Contract gap.
- Prior weakness: invalid/preflight paths can pass while valid/happy side-effect paths fail only in deployed runtime.
- Flow improvement: add Runtime Causality Gate to `flow-plan` and onboarding docs so future plans classify causality before edits.

### 2.7 Flow Knowledge Update

- Reusable kit-level process knowledge discovered.
- Update target: flow-plan templates, onboarding skill templates, residual-risk docs, README.

### 2.8 Business Flow Matrix

| Flow | Actor / scope | Entry point | Normal path | Error / exception paths | Permission / ownership / boundary paths | Side effects | Regression risk | Required test coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FLOW-001 runtime-aware planning | Agent using installed kit | `flow-plan` / `/flow-plan` | Triggered runtime risk is classified before implementation design | Runtime evidence unavailable, stale deploy, browser symptom masks server outcome, shallow smoke only | Applies to auth, tenant, provider, deploy and production data boundaries | Plan may add setup/blocker tasks before code | Agents repeatedly patch code for environment/data/provider causes | Template review, docs grep, smoke of wording across Codex/Claude |
| FLOW-002 onboarding runtime inventory | Agent onboarding a target repo | `agent-flow-onboarding`, `project-structure-survey`, `integration-scenario-design` | Repo docs capture deploy platform, logs, smoke, bindings/secrets, provider sandboxes and blockers | Missing runtime access, unknown provider, no smoke command | Target repo local docs preserve stack-specific commands | Future plans use documented evidence sources | Installed repos keep weak environment detection | Template review and README docs |

### 2.9 Regression Surface Matrix

| Surface | Files | Regression Concern | Coverage |
| --- | --- | --- | --- |
| Codex flow-plan skill | `templates/.codex/skills/flow-plan/SKILL.md` | Codex plans omit runtime causality gate | Grep/review required sections |
| Claude flow-plan command/skill | `templates/.claude/commands/flow-plan.md`, `templates/.claude/skills/flow-plan/SKILL.md` | Claude and Codex drift | Grep/review parity |
| Onboarding survey | `project-structure-survey/SKILL.md` | Installed repos fail to inventory deploy/log/smoke/bindings | Template review |
| Scenario design | `integration-scenario-design/SKILL.md` | Integration docs omit provider/runtime smoke | Template review |
| Residual-risk docs | `agent-flow-residual-risk-countermeasures.md` | Policy not discoverable after install | README/docs review |

### 2.10 Test Design Matrix

| Test | Command / Tool | Covers | Required Result |
| --- | --- | --- | --- |
| Status review | `git diff --check` | formatting/whitespace | Pass |
| Policy grep | `rg -n "Runtime Causality Gate|runtime-causality|exceededCpu|active deployed" templates README.md` | required wording present | Pass |
| Installer syntax | `python3 -m py_compile install.py templates/scripts/agent-flow-matrix-gate.py` | touched repo still has valid Python helpers | Pass |
| Diff review | `git diff -- templates README.md` | scope and parity | Review |

### 2.11 Integration Coverage Contract

- Required: Codex and Claude flow-plan surfaces must include the new gate.
- Required: onboarding docs must collect runtime-causality evidence sources.
- Required: scenario design must express provider/runtime smoke and blocker expectations.
- Waiver: no installer end-to-end copy test is required because this is template text only and no installer logic changes.

### 2.12 Playwright Integration Test Plan

- Not applicable: no visible application UI changes.
- Waiver reason: this modifies workflow text templates and docs only.

### 2.13 Migration / Runtime Enforcement

- No schema/runtime migration.
- Installer behavior unchanged.

### 2.14 Open Questions

- None blocking.

## 3. Tasks

- [x] TASK-001 Update flow-plan templates with Runtime Causality Gate triggers, evidence table, classification, and readiness item.
- [x] TASK-002 Update onboarding survey/scenario templates to inventory runtime-causality evidence after install.
- [x] TASK-003 Update residual-risk docs and README with the policy and onboarding answer.
- [x] TASK-004 Run text/syntax validation and diff hygiene.
- [x] TASK-005 Report remaining untracked unrelated files without staging them.

## 4. Readiness

- [x] Requirements map to tasks
- [x] User intent and current-state analysis is documented
- [x] Requirement questioning was performed, or No Questions Rationale is documented with source evidence
- [x] Business/product ambiguity has been resolved or explicitly blocked
- [x] Required onboarding docs exist for behavior-changing work
- [x] Flow Knowledge Update target is explicit
- [x] Residual Risk Preflight warnings have countermeasures, setup tasks, or blockers
- [x] Business flows map to required tests or blockers
- [x] Integration Coverage Contract has concrete coverage or waivers
- [x] Validation commands are identified

<!-- frozen: v1 2026-06-01 by Codex -->
<!-- plan_author: codex -->

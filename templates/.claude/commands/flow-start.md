Project kickoff command for turning a rough feature request into an implementation-ready plan.

## Rules

- Follow the workflow and constraints defined in `.claude/skills/flow-start/SKILL.md`.
- Activate the shared context first by loading `.claude/rules/` and `.claude/docs/DESIGN.md`.
- Treat this command as the entry point to the planning flow only. Do not start implementation unless the user explicitly asks for it after plan approval.
- Use this command for new features, greenfield feature slices, or ambiguous product exploration.
- For modifications to existing behavior, bug fixes, regressions, or work that touches existing order/dealer/company/mail/PDF/job/search/status/auth/schema flows, route to `/flow-plan` instead.
- Save the resulting plan to `docs/flow/{feature_name}/plan.md`.
- Include plan author metadata near the frozen marker:
  `<!-- plan_author: claude-code -->`.
- If `$ARGUMENTS` is empty, ask the user for the feature or project they want to plan before proceeding.
- Reuse existing code paths, docs, and patterns before proposing new structures.
- Before drafting the plan, explicitly analyze user intent against the current repository state and ask detailed requirement questions when actors, business outcome, scope, data ownership, entrypoints, success criteria, or rollout assumptions are unclear.
- If requirement questions are needed, stop after presenting the questions. Do not draft or freeze a plan that carries unresolved product or business ambiguity.
- Ask design policy and library-selection questions when multiple architecture or dependency choices are viable and the existing codebase does not clearly decide the answer.
- For behavior-changing work, include an Integration Coverage Contract that maps each affected flow to happy, exception, permission, boundary, side-effect, and regression coverage or explicit waivers.
- For behavior-changing work, require `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md`; if missing, run `agent-flow-onboarding` first.
- Run a residual-risk preflight before plan freeze. If the request may involve missed business flows, natural-language plan ambiguity, runtime/external dependency gaps, weak test infrastructure, or waiver/reviewer risk, warn the user and capture countermeasures or blockers in the plan.

## Prerequisites

- Source code exists in the current working directory.
- `.claude/skills/flow-start/SKILL.md` is available.
- The user has provided, or will provide, the target feature or project idea.

## Directory Structure

- docs/flow/{feature_name}/
  - plan.md (created by this command)

---

## Phase 1: Kickoff

### Step 1: Load context

Read the project rules from `.claude/rules/` and the latest design decisions from `.claude/docs/DESIGN.md`.

### Step 2: Resolve the target

Interpret `$ARGUMENTS` as the feature or project to plan.

- If `$ARGUMENTS` contains a short feature name, use it directly as the planning target.
- If `$ARGUMENTS` contains a broader request, summarize it into a concise feature name before creating artifacts.
- If the target is still ambiguous, ask the minimum necessary follow-up question in Japanese.

### Step 3: Analyze intent and current state

Before drafting a Project Brief, summarize:

- User intent in business/product terms
- Target actors, roles, permissions, and ownership scope if known
- Current repository/runtime state confirmed from files and docs
- Missing capability or rough product opportunity
- Likely affected routes, screens, APIs, schemas, jobs, mail/PDF/export paths, integrations, or shared services
- Assumptions not yet safe
- Smallest likely scope that satisfies the intent

If the repository does not contain the relevant runtime, or if the request may belong in another repo, ask where the feature should be implemented before planning further.

### Step 4: Ask detailed requirement questions when needed

Ask up to 5 questions in Japanese, ordered by recommendation priority. Questions should clarify behavior and product intent before implementation details:

- Goal and success criteria
- Actors, permissions, tenant/store/company/customer scope
- Included and excluded workflows
- Data ownership, lifecycle, retention, deletion, or status transitions
- Required screens, entrypoints, wording, and workflow order
- Side effects such as mail, PDF/export, notifications, jobs, audit logs, external APIs, or migrations

Present questions with:

- Understanding so far
- Confirmed from code
- Assumptions not yet safe
- Recommended option first

If ambiguity remains after the user answers, repeat intent/current-state analysis and ask again before writing or freezing the plan.

---

## Phase 2: Planning Flow

### Step 5: Execute the `flow-start` skill

Run the workflow from `.claude/skills/flow-start/SKILL.md`:

1. Understand the current codebase and constraints
2. Clarify missing requirements with detailed intent/current-state questions
3. Produce a compact Project Brief
4. Ask design policy and library-selection questions when the existing codebase does not decide them
5. Convert business-flow knowledge into Integration Coverage Contract obligations
6. Add Residual Risk Preflight warnings and countermeasures when applicable
7. Design the minimal fitting approach
8. Write `docs/flow/{feature_name}/plan.md`
9. Freeze the plan only when it is coherent
10. Run `/flow-plan-review` before implementation starts

### Step 6: Present the handoff

Report the following to the user:

- What will change
- Which areas are affected
- Main risks
- The exact next step: `/flow-plan-review` before `/flow-impl` or `team-implement`

---

## User Requirements

$ARGUMENTS

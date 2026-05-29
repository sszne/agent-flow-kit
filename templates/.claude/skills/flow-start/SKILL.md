---
name: flow-start
description: |
  Start a new project/feature with multi-agent collaboration (Opus 4.6 + Agent Teams).
  Phase 1: Codebase understanding (Opus subagent 1M context + Claude user interaction).
  Phase 2: Parallel research & design (Agent Teams: Researcher + Architect).
  Phase 3: Plan synthesis & user approval.
  Implementation is handled separately by /team-implement.
metadata:
  short-description: Project kickoff with Agent Teams (Plan phase)
---

# Flow Start

**Project kickoff skill leveraging Opus 1M context and Agent Teams.**

## Overview

This skill handles the planning phases (Phase 1-3). Plan review is done via
`/flow-plan-review`. Implementation is done via `/team-implement`, and final
review via `/team-review`.

```

## Operating Rules

- Load `.claude/rules/` and `.claude/docs/DESIGN.md` before planning.
- Do not start implementation from this skill.
- Before drafting the plan, explicitly analyze user intent against the current repository state.
- If actors, business outcome, scope, data ownership, entrypoints, success criteria, side effects, or rollout assumptions are unclear, stop and ask detailed requirement questions before drafting or freezing the plan.
- Ask design policy and library-selection questions when architecture, SDK, ORM, auth, queue, browser-test tooling, or other dependency choices are not decided by existing local patterns.
- For behavior-changing work, require an Integration Coverage Contract that maps each affected flow to happy, exception, permission, boundary, side-effect, and regression coverage or an explicit waiver.
- For behavior-changing work, require `docs/agent-flow/project-structure.md`, `docs/agent-flow/business-flows.md`, and `docs/agent-flow/integration-scenarios.md`; if missing, run onboarding first.
- Run a residual-risk preflight before plan freeze. If the request may involve missed business flows, natural-language plan ambiguity, runtime/external dependency gaps, weak test infrastructure, or waiver/reviewer risk, warn the user and capture countermeasures or blockers in the plan.
- Prefer the smallest approach that fits existing codebase conventions.
- If discovery shows the request is actually a modification of an existing runtime path, switch to the `/flow-plan` structure before freezing.
/flow-start <feature>     ← This skill (planning)
    ↓ After approval
/flow-plan-review           ← Cross-agent plan review
    ↓ After approval
/team-implement             ← Parallel implementation
    ↓ After completion
/team-review                ← Parallel review
```

## Workflow

```
Phase 1: UNDERSTAND (Opus 1M context + Claude Lead)
  Opus subagent analyzes the codebase (1M context), Claude interacts with the user
    ↓
Phase 2: RESEARCH & DESIGN (Agent Teams — Parallel)
  Researcher (Opus) ←→ Architect (Codex) communicate bidirectionally for research and design
    ↓
Phase 3: PLAN & APPROVE (Claude Lead + User)
  Integrate research and design, create plan and get user approval
```

---

## Phase 1: UNDERSTAND (Opus Subagent + Claude Lead)

**Analyze the codebase with Opus subagent's 1M context while Claude interacts with the user.**

> Main orchestrator context is precious. Large-scale codebase analysis is delegated to Opus subagent (1M context).

### Step 1: Analyze Codebase with Opus Subagent

Use a general-purpose subagent (Opus) to analyze the entire codebase:

```
# Via general-purpose subagent (recommended)
Task tool:
  subagent_type: "general-purpose"
  prompt: |
    Analyze this codebase comprehensively:
    - Directory structure and organization
    - Key modules and their responsibilities
    - Existing patterns and conventions
    - Dependencies and tech stack
    - Test structure

    Use Glob, Grep, and Read tools to explore the codebase thoroughly.

    Save analysis to .claude/docs/research/{feature}-codebase.md
    Return concise summary (5-7 key findings).
```

To supplement the subagent's analysis, Claude can use Glob/Grep/Read to inspect specific files.

### Step 2: Intent and current-state analysis

Before asking or drafting, Claude Lead must summarize:

- User intent in business/product terms
- Target actors, roles, permissions, and ownership scope if known
- Current repository/runtime state confirmed from files and docs
- Existing related code, missing capability, or product opportunity
- Likely affected routes, screens, APIs, schemas, jobs, mail/PDF/export paths, integrations, or shared services
- Assumptions not yet safe
- Smallest likely scope that satisfies the intent

If the repository does not contain the relevant runtime, or if the request may belong in another repo, ask where the feature should be implemented before planning further.

### Step 3: Requirements Gathering

Ask the user questions to clarify requirements. Use up to 5 questions, ordered by recommendation priority.

1. **Purpose**: What do you want to achieve?
2. **Scope**: What to include / exclude?
3. **Actors and permissions**: Who performs the workflow and under which tenant/store/company/customer scope?
4. **Current vs desired behavior**: What is missing or changing?
5. **Data rules**: Ownership, lifecycle, retention, deletion, status transitions, migration/backfill expectations.
6. **Entry points and side effects**: Screens, APIs, jobs, mail, PDF/export, notifications, audit logs, external APIs.
7. **Constraints**: Existing APIs, DB limits, auth rules, rollout constraints.
8. **Success criteria**: How do you determine completion?

Present questions with:

- Understanding so far
- Confirmed from code
- Assumptions not yet safe
- Recommended option first

If ambiguity remains after the user answers, repeat intent/current-state analysis and ask again before writing or freezing the plan.

### Step 4: Create Project Brief

Combine codebase understanding + requirements into a "Project Brief":

```markdown
## Project Brief: {feature}

### Intent
{User intent in business/product terms}

### Current State
- Architecture: {existing architecture summary}
- Relevant code: {key files and modules}
- Patterns: {existing patterns to follow}
- Confirmed from code: {source-backed facts}
- Assumptions resolved: {answers or evidence}

### Goal
{User's desired outcome in 1-2 sentences}

### Scope
- Include: {list}
- Exclude: {list}

### Constraints
- {technical constraints}
- {library requirements}

### Success Criteria
- {measurable criteria}
```

This brief is passed to Phase 2 teammates as shared context.

---

## Phase 2: RESEARCH & DESIGN (Agent Teams — Parallel)

**Launch Researcher and Architect in parallel via Agent Teams with bidirectional communication.**

> Key difference from subagents: Teammates can communicate with each other.
> Researcher's findings change Architect's design, and Architect's requests trigger new research.

### Design Policy and Library Selection Gate

Before finalizing architecture, ask design policy or library-selection questions when the decision materially affects architecture, dependency risk, data shape, test strategy, security, performance, or rollout.

Questions are required when:

- Existing project patterns do not clearly decide the architecture or dependency choice
- A new package, framework, SDK, ORM, auth library, queue, browser-test tool, or external service would be introduced
- Multiple local patterns exist and choosing the wrong one would make future maintenance or testing harder
- A library decision changes security, data ownership, migration strategy, deployment, licensing, bundle size, runtime support, or operational risk
- The minimal no-new-library approach is possible but has meaningful tradeoffs against adding a dependency

When asking, present the existing-pattern / no-new-library option first when viable, then alternatives with pros, cons, and decision criteria for user/business impact, maintenance, tests, security, and operations. When no question is needed, document why existing patterns decide the choice.

### Team Setup

```
Create an agent team for project planning: {feature}

Spawn two teammates:

1. **Researcher** — Uses WebSearch/WebFetch for external research (Opus 1M context)
   Prompt: "You are the Researcher for project: {feature}.

   Your job: Research external information needed for this project.

   Project Brief:
   {project brief from Phase 1}

   Tasks:
   1. Research libraries and tools: usage patterns, constraints, best practices
   2. Find latest documentation and API specifications
   3. Identify common pitfalls and anti-patterns
   4. Look for similar implementations and reference architectures
   5. If a new dependency is proposed, compare it with a no-new-library or existing-pattern approach

   How to research:
   - Use WebSearch for comprehensive research:
     WebSearch: '{topic} best practices constraints recommendations'
   - Use WebFetch for targeted documentation lookup

   Save all findings to .claude/docs/research/{feature}.md
   Save library docs to .claude/docs/libraries/{library}.md

   Communicate with Architect teammate:
   - Share findings that affect design decisions
   - Respond to Architect's research requests
   - Flag constraints that limit implementation options

   IMPORTANT — Work Log:
   When ALL your tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/researcher.md

   Use this format:
   # Work Log: Researcher
   ## Summary
   (1-2 sentence summary of what you researched)
   ## Tasks Completed
   - [x] {task}: {brief description of findings}
   ## Sources Consulted
   - {URL or source}: {what was found}
   ## Key Findings
   - {finding}: {relevance to project}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

2. **Architect** — Uses Codex CLI for design and planning
   Prompt: "You are the Architect for project: {feature}.

   Your job: Use Codex CLI to design the architecture and create implementation plan.

   Project Brief:
   {project brief from Phase 1}

   Tasks:
   1. Design architecture (modules, interfaces, data flow)
   2. Select patterns (considering existing codebase conventions)
   3. Create step-by-step implementation plan with dependencies
4. Identify risks and mitigation strategies, including residual risks from `docs/agent-flow-residual-risk-countermeasures.md`
5. Translate normal, error/exception, permission/ownership, boundary, and side-effect paths into integration-test obligations
6. Decide whether architecture/library choices are already determined by local patterns or require a user question before plan freeze

   How to consult Codex:
   codex exec --model gpt-5.5-codex --sandbox read-only --full-auto "{question}" 2>/dev/null

   Update .claude/docs/DESIGN.md with architecture decisions.

   Communicate with Researcher teammate:
   - Request specific library/tool research
   - Share design constraints that need validation
   - Adjust design based on Researcher's findings

   IMPORTANT — Work Log:
   When ALL your tasks are complete, write a work log file to:
     .claude/logs/agent-teams/{team-name}/architect.md

   Use this format:
   # Work Log: Architect
   ## Summary
   (1-2 sentence summary of what you designed)
   ## Tasks Completed
   - [x] {task}: {brief description of what was done}
   ## Design Decisions
   - {decision}: {rationale}
   ## Codex Consultations
   - {question asked to Codex}: {key insight from response}
   ## Communication with Teammates
   - → {recipient}: {summary of message sent}
   - ← {sender}: {summary of message received}
   ## Issues Encountered
   - {issue}: {how it was resolved}
   (If none, write 'None')
   "

Wait for both teammates to complete their tasks.
```

### Why Bidirectional Communication Matters

```
Example interaction flow:

Researcher: "httpx has a connection pool limit of 100 by default"
    → Architect: "Need to add connection pool config to design"
    → Architect: "Also research: does httpx support HTTP/2 multiplexing?"
    → Researcher: "Yes, via httpx[http2]. Requires h2 dependency."
    → Architect: "Updated design to use HTTP/2 for the API client module"
```

Without Agent Teams (old subagent approach), this would require:
1. Gemini subagent finishes → returns summary
2. Claude reads summary → creates new Codex subagent prompt
3. Codex subagent finishes → returns summary
4. If Codex needs more info → another Gemini subagent round

Agent Teams collapses this into a single parallel session with real-time interaction.

---

## Phase 3: PLAN & APPROVE (Claude Lead)

**Integrate Agent Teams results, create an implementation plan, and request user approval.**

### Step 1: Synthesize Results

Read outputs from Phase 2:
- `.claude/docs/research/{feature}.md` — Researcher findings
- `.claude/docs/libraries/{library}.md` — Library documentation
- `.claude/docs/DESIGN.md` — Architecture decisions

### Step 2: Create Implementation Plan

Create task list using TodoWrite:

```python
{
    "content": "Implement {specific task}",
    "activeForm": "Implementing {specific task}",
    "status": "pending"
}
```

Task breakdown should follow `references/task-patterns.md`.

### Step 3: Update CLAUDE.md

Add project context to CLAUDE.md for cross-session persistence:

```markdown
---

## Current Project: {feature}

### Context
- Goal: {1-2 sentences}
- Key files: {list}
- Dependencies: {list}

### Architecture
- {Key architecture decisions from Architect}

### Library Constraints
- {Key constraints from Researcher}

### Decisions
- {Decision 1}: {rationale}
- {Decision 2}: {rationale}
```

### Step 4: Present to User

Present the plan to the user:

```markdown
## Project Plan: {feature}

### Intent and Ambiguity Resolution
{User intent, confirmed source evidence, user answers, and assumptions that are resolved or still blocked}

### Codebase Analysis
{Key findings from Phase 1 — 3-5 bullet points}

### Research Findings (Researcher)
{Key findings — 3-5 bullet points}
{Library constraints and recommendations}

### Design Direction (Architect)
{Architecture overview}
{Key design decisions with rationale}

### Design Policy and Library Selection
{Selected approach, alternatives considered, dependency impact, and risk mitigation. If no new library is needed, state why existing patterns decide the choice.}

### Task List ({N} items)
{Task list with dependencies}

### Risks and Considerations
{From Architect's analysis}

### Next Steps
1. Shall we proceed with this plan?
2. After approval, run `/flow-plan-review`
3. After plan-review approval, start parallel implementation with `/team-implement`
4. After implementation, run parallel review with `/team-review`

---
Shall we proceed with this plan?
```

---

## Output Files

| File | Author | Purpose |
|------|--------|---------|
| `.claude/docs/research/{feature}.md` | Researcher | External research findings |
| `.claude/docs/libraries/{lib}.md` | Researcher | Library documentation |
| `.claude/docs/DESIGN.md` | Architect | Architecture decisions |
| `CLAUDE.md` (updated) | Lead | Cross-session project context |
| Task list (internal) | Lead | Implementation tracking |

---

## Tips

- **Phase 1**: Opus subagent (1M context) analyzes the codebase while Claude interacts with the user
- **Phase 2**: Agent Teams bidirectional communication allows Researcher (Opus) and Architect (Codex) to influence each other
- **Phase 3**: After plan approval, run `/flow-plan-review`, then proceed to
  parallel implementation with `/team-implement`
- **Ctrl+T**: Toggle task list display
- **Shift+Up/Down**: Navigate between teammates (when using Agent Teams)

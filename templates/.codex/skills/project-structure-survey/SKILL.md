---
name: project-structure-survey
description: |
  Survey a repository before adopting the agent-flow workflow. Use when starting
  agent-flow onboarding in a new repo to document architecture, domain models,
  use cases, runtime entrypoints, tests, and operational risks.
---

# Project Structure Survey

Create `docs/agent-flow/project-structure.md`.

## Rules

- Inspect the real repository before writing conclusions.
- Prefer source files, routes, migrations/schema, tests, config, package files, and deployment files over old notes.
- If `docs/agent-flow/source-documents.md` exists, read it as candidate
  evidence only. Do not let converted requirement documents override source,
  schema, routes, tests, package files, deploy config, current repo docs, or
  explicit user confirmation.
- When a source-document claim conflicts with repo evidence, label the conflict
  and carry it as an open question instead of treating it as current
  architecture or expected behavior.
- Do not edit application code.
- If a fact is inferred, label it as inferred.
- Keep stale or missing areas explicit.
- Inventory runtime-causality evidence sources: deploy platform, release/version
  checks, runtime logs/tail commands, smoke commands, env/secrets/bindings,
  remote data diagnostics, provider sandboxes, and production-only failure
  modes. Label unknown access or missing commands as blockers.

## Workflow

1. Read `docs/agent-flow/source-documents.md` if it exists and note candidate
   claims, conflicts, and open questions.
2. Identify the stack and runtime entrypoints from real repo evidence.
3. Map architecture boundaries: apps, modules, controllers, services/actions, views, jobs, APIs, build/deploy paths.
4. Map domain models from schema/migrations/models/types.
5. Map use cases from routes/controllers/screens/jobs/tests/docs.
6. Map existing tests and verification commands.
7. Map runtime-causality evidence sources and blockers.
8. Write the document.

## Output Template

```markdown
# Project Structure Survey

## Repository Snapshot
- Stack:
- Runtime entrypoints:
- Local run commands:
- Test commands:

## Architecture
| Area | Files/directories | Responsibility | Notes |
| --- | --- | --- | --- |

## Domain Model
| Model/entity | Source evidence | Relationships | Business meaning |
| --- | --- | --- | --- |

## Use Cases
| Use case | Actor | Entry point | Core flow | Evidence |
| --- | --- | --- | --- | --- |

## Source Document Intake
| Claim status | How it affected this survey | Notes |
| --- | --- | --- |
| confirmed |  |  |
| conflicts-with-repo |  |  |
| aspirational / stale-or-unknown / needs-user-confirmation |  |  |

## Runtime / Operations
| Concern | Evidence | Risk |
| --- | --- | --- |

## Runtime Causality Inventory
| Signal | Evidence source / command | Known blocker | Notes |
| --- | --- | --- | --- |
| Active deployed version |  |  | GitHub Actions, release SHA, provider deployment ID, Worker script version, etc. |
| Runtime logs |  |  | Provider logs, `wrangler tail`, app logs, queue logs, webhook logs, etc. |
| Smoke / representative paths |  |  | Include shallow and valid happy/side-effect paths where available. |
| Environment bindings |  |  | Secrets, env vars, database/D1 binding, storage bucket, provider config. |
| Remote data diagnostics |  |  | Read-only queries, admin diagnostics, migration status, seed/version markers. |
| Provider sandbox / mock boundary |  |  | External API sandbox, local fake, mock adapter, or unavailable reason. |
| Production-only failure modes |  |  | CORS masking, opaque 5xx, timeout, CPU/memory, stale deploy, provider rejection. |

## Existing Test Surface
| Level | Location/command | Coverage notes |
| --- | --- | --- |

## Open Questions
- ...
```

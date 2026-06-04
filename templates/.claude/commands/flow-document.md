Source document intake command for Agent Flow onboarding.

## Rules

- Follow the workflow and constraints defined in
  `.claude/skills/flow-document/SKILL.md`.
- Run this command at the start of onboarding before
  `project-structure-survey`.
- Treat source documents as optional sidecar evidence, not as source-of-truth.
- If service explanation, requirement, design, proposal, or specification files
  exist, ask the user to provide paths or place them under
  `docs/agent-flow/source-documents/raw/`.
- If `markitdown` is installed, convert supported files to Markdown under
  `docs/agent-flow/source-documents/converted/`.
- Always write or update `docs/agent-flow/source-documents.md`, even when no
  source documents are provided.
- Classify every imported claim as `confirmed`, `conflicts-with-repo`,
  `aspirational`, `stale-or-unknown`, or `needs-user-confirmation`.
- Do not let converted documents override source, schema, routes, tests, deploy
  config, current repo docs, or explicit user confirmation.

## User Requirements

$ARGUMENTS

# Development Environment

Project development environment and toolchain. The default template is tuned for common Next.js repositories; adjust this file during onboarding when the target stack differs.

## Runtime

- App: Next.js / TypeScript
- Package manager: confirm during onboarding (`pnpm`, `npm`, `yarn`, or `bun`)
- Main application paths: `app/`, `pages/`, `src/`, `components/`, `lib/`
- Data layer: confirm during onboarding (`prisma/`, `drizzle/`, `supabase/`, direct SQL, or external API)

## Local Development

```bash
pnpm install
pnpm dev
```

If the repository uses `npm`, `yarn`, or `bun`, replace the commands with the project-local equivalents. Prefer the commands already present in `package.json` scripts.

## Verification Commands

Use focused checks during implementation, then broaden before completion:

```bash
pnpm lint
pnpm test
pnpm test:integration
pnpm build
```

If Playwright is configured:

```bash
pnpm exec playwright test
```

## API / Server Integration Tests

Route handlers, server actions, auth/session behavior, database persistence, background jobs, mail/export, and external-boundary adapters need Feature/API integration coverage when affected.

Use the repository's established test runner and setup pattern. Do not rely only on unit tests when behavior crosses runtime boundaries.

## Migrations

Schema changes are deploy-critical.

- If a task adds files under `prisma/migrations/`, `drizzle/`, `supabase/migrations/`, `db/migrations/`, `database/migrations/`, or another migration path, run the project migration command before reporting verification complete.
- If code reads or writes a new column/table, confirm where migration execution is enforced.
- Do not add application fallbacks that hide an unmigrated schema unless the user explicitly asks for compatibility work.

## Formatting / Linting

Use the project-local formatter/linter:

```bash
pnpm lint
```

Avoid broad formatting unless the task is explicitly about formatting. Keep diffs scoped.

## Browser Verification

Use browser-driven verification for visible UI flows:

- Prefer `http://localhost` over `http://127.0.0.1` when cookies/session behavior matters.
- If Playwright CLI cannot launch Chromium because of local permission errors, use the attached browser tooling.
- For UI changes, verify the rendered screen, modal, transition, displayed values, and console/network errors when relevant.

## Completion Checklist

- [ ] Relevant unit tests were run.
- [ ] Feature/API integration or scenario coverage was added/updated for risky route, screen, API, shared logic, mail/export, job, external adapter, or schema changes.
- [ ] Browser verification was run for visible behavior, or a concrete blocker was reported.
- [ ] Migration command was run when migrations were added or schema-dependent code changed.
- [ ] Lint/format command was run before completion.
- [ ] Build command was run when frontend assets, route handlers, or build-time config changed.

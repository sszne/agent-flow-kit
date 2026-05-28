# Project Design Document

> This document tracks durable design decisions for this repository.

## Overview

- Purpose:
- Primary users:
- Runtime entrypoints:

## Architecture

| Area | Responsibility | Notes |
| --- | --- | --- |

## Agent Flow Decisions

| Decision | Rationale | Alternatives Considered | Date |
| --- | --- | --- | --- |
| Behavior-changing work must start from `/flow-plan` and include Business Flow Matrix, Regression Surface Matrix, and Test Design Matrix | Prevents implementation from missing adjacent business flows and regression surfaces | Ad hoc implementation; post-review only | YYYY-MM-DD |
| Prompt routing should bias risky work to `/flow-plan` even when the user does not explicitly invoke it | Makes safe operation the default for bug fixes, regressions, refactors, auth/schema/status/order/search/mail/PDF/job changes, and existing runtime path changes | Relying on users to always remember `/flow-plan` | YYYY-MM-DD |
| Behavior-affecting edits should be blocked until a frozen flow plan exists | Prevents accidental direct implementation when `/flow-plan` was forgotten or skipped | Reminder-only prompt routing | YYYY-MM-DD |
| Behavior-changing work must include an Integration Coverage Contract before implementation | Ensures every affected business flow maps happy, exception, permission, boundary, side-effect, and regression cases to integration/unit/browser/migration coverage or explicit waivers | Relying on broad test names without case-type traceability | YYYY-MM-DD |
| Visible or multi-step workflows require Playwright integration-test evidence before final review | Makes browser verification auditable through screenshots, `index.html`, test review, and business-flow impact review | Informal browser checks only | YYYY-MM-DD |

## TODO

- [ ] Run `agent-flow-onboarding`
- [ ] Confirm project-specific test commands
- [ ] Confirm project-specific behavior-affecting paths in `.agent-flow/config.json`

## Changelog

| Date | Changes |
| --- | --- |

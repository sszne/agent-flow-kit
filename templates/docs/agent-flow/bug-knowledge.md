# Bug Knowledge

This file accumulates project-specific bug and regression knowledge that cannot
be fully prevented by generic flow rules.

Use it when a bug report reveals:

- a hidden business rule,
- production-only data shape,
- external-service behavior,
- rare timing/concurrency condition,
- legacy behavior not discoverable from code,
- weak test infrastructure,
- reviewer or waiver failure pattern.

## Entry Template

```markdown
## BUG-{YYYYMMDD}-{short-slug}

- Date:
- Related flow plan:
- Related implementation report:
- Related issue / incident / support report:
- Affected business flow:
- Symptoms:
- Trigger / reproduction:
- Root cause:
- Why the prior flow did not catch it:
- Flow improvement possible: Yes/No
- Flow improvements made:
  - [ ] `docs/agent-flow/business-flows.md`
  - [ ] `docs/agent-flow/integration-scenarios.md`
  - [ ] `.claude/rules/testing.md`
  - [ ] `.claude/docs/DESIGN.md`
  - [ ] `.agent-flow/config.json`
  - [ ] Other:
- If not preventable by flow, future detection / response:
- Required regression tests:
- Required runtime / environment:
- Owner / reviewer notes:
```

## Entries

<!-- Append newest entries below. -->

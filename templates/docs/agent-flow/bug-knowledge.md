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

## Prevention Pattern Taxonomy

Before task design for bug/regression work, classify each relevant bug-knowledge
entry into one or more prevention patterns. The pattern classification must feed
the current plan's Bug Feedback Review and task ordering.

| Pattern | Signal | Required planning response |
| --- | --- | --- |
| Requirement/questioning gap | Actor, store/account scope, lifecycle, completion signal, or requested workflow order was not asked before freeze | Add required questions or a source-backed `Questioning Decision`; block freeze until answered or explicitly scoped out. |
| Business-flow or matrix gap | Affected workflow, exception path, permission path, boundary case, or side effect was absent from Business Flow, Regression Surface, Test Design, or Integration Coverage matrices | Update `docs/agent-flow/business-flows.md` and/or `docs/agent-flow/integration-scenarios.md` before implementation tasks. |
| Valid-path coverage gap | Tests or smoke covered preflight, invalid input, unauthenticated `401`, or health only while the valid path failed | Add happy-path, side-effect, valid credential/session, or provider completion coverage, or record the exact blocker. |
| Runtime/deploy/provider evidence gap | Local mock or source inspection passed while deployed bundle, Worker/script, provider callback, device context, or remote data failed | Run Runtime Causality Gate and add deployed-artifact, provider/device, remote-data, or credential-lane evidence tasks. |
| Implementation drift | Implementation changed behavior, scope, data shape, or UI outside the frozen plan | Add implementation/review guard and regression test; update the plan before implementation continues. |
| UI-intent or action-placement gap | Repeated user feedback corrected step labels, order, exclusions, screenshots, docs links, or button placement | Add onboarding/UI checklist requirements before rich UI implementation. |
| Non-preventable external/runtime/data behavior | Provider outage, credential revocation, unknown legacy data, rare race, or production-only condition was not knowable from code/docs/tests/user answers | Keep as bug knowledge with detection and response guidance; do not blame the planning flow without evidence. |

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

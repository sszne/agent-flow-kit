---
name: flow-design
description: |
  Analyze repo-local or user-provided design-system artifacts for frontend
  planning. Use as a support skill from flow-plan when screens, components,
  frontend routes, client UI, styles, public frontend assets, brand, tokens, or
  component rules are in scope.
---

# Flow Design

Support skill for design-system-aware frontend planning. This skill does not
freeze `docs/flow/{feature}/plan.md` by itself; it returns design-system
findings that `flow-plan` must incorporate into the implementation plan.

## Purpose

Help `flow-plan` prefer existing design-system rules when frontend work is in
scope. If planned UI maps to existing tokens, components, patterns, or voice
rules, the plan should apply those rules or record a concrete waiver.

## Inputs

Read only the relevant artifacts:

- explicit user-provided design-system files or attachments,
- `.agent-flow/config.json` `design_system_paths` when configured,
- `docs/agent-flow/design-system.md`,
- files under `docs/agent-flow/design-system/`,
- `.claude/docs/DESIGN.md`,
- existing source components, style tokens, theme files, CSS variables,
  Tailwind/theme config, Storybook or component-library docs when present.

If a document is large, summarize only the parts that affect the planned
frontend surface. Do not import brand-specific rules from a sample document into
the portable Agent Flow Kit unless the target repo explicitly owns that design
system.

## Source Priority

Use this priority when sources conflict:

```text
explicit user-provided design-system docs > repo-local design-system docs >
existing source/components/styles > general design taste
```

If repo-local source differs from a design-system document, report the conflict
instead of guessing which one is current.

## Workflow

1. Identify whether frontend design-system analysis is needed.
   - Triggered by screens, frontend routes, components, client JS, styles,
     public frontend assets, brand, tokens, component requests, or explicit
     design-system attachments.
2. Search the design-system paths listed above.
3. Summarize discovered tokens, components, patterns, and voice/copy rules that
   could affect the plan.
4. Compare the planned UI against the discovered rules.
5. Classify each planned UI item:
   - `exact-match`: design system has a directly matching component/pattern.
   - `partial-match`: rules exist but adaptation is needed.
   - `no-match`: no relevant component/pattern was found.
   - `conflict`: design-system guidance and source implementation disagree.
6. Return plan-ready sections for `flow-plan`.
7. If the user asked to import a design system, write or update
   `docs/agent-flow/design-system.md` or a scoped file under
   `docs/agent-flow/design-system/`.

## Required Output For Flow Plan

When `flow-plan` calls this skill, return:

```markdown
### Design System Applicability

| Check | Result | Evidence |
| --- | --- | --- |
| Design system searched | Yes | {paths inspected} |
| Design system found | Yes/No/Partial | {source paths or reason none found} |
| Applies to this plan | Yes/No/Partial | {screens/components/tokens matched} |
| Required waivers | Yes/No | {summary of concrete waivers or "None"} |

### Component Match Matrix

| Planned UI | Design System Match | Rule To Apply | Source | Exception / Waiver |
| --- | --- | --- | --- | --- |
| {UI item} | {exact-match / partial-match / no-match / conflict} | {token/component/pattern rule or fallback source pattern} | {file/path/section} | {None or concrete reason} |
```

If no design system is found, the applicability section must still record the
searched paths and the fallback source/component/style evidence that will guide
the plan.

## Waiver Rules

Waivers must include a concrete reason, such as:

- legacy component incompatibility,
- accessibility improvement over the documented design,
- missing token or incomplete component guidance,
- explicit user instruction,
- conflict with current source evidence,
- target repo has no design-system artifact after searched-path review.

Invalid waivers: `N/A`, `manual`, `low risk`, `TBD`, `later`, blank, or a
generic "not applicable" without searched-path evidence.

## Output Discipline

- Keep findings scoped to the planned frontend surface.
- Cite file paths, section names, tokens, or component names used as evidence.
- Do not invent missing design rules.
- Prefer existing local components and tokens over new abstractions when they
  satisfy the design-system rule.
- If design evidence is insufficient, make the uncertainty visible in
  `flow-plan` instead of silently choosing a visual direction.

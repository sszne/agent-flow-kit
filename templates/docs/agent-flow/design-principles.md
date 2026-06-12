# Design Principles

Use this document to record durable architecture design principles for
behavior-changing planning and implementation. `flow-plan` reads this document
when modules, services, domain logic, shared logic, or data ownership are in
scope, and `flow-impl` re-checks it during architecture review.

## Source Priority

```text
explicit user-provided design-principles docs > repo-local design-principles
docs > existing source conventions > external architecture references
```

When this document conflicts with existing source conventions, record the
conflict and ask for confirmation before treating either source as
authoritative.

## Intake Status

- Status: default-principles / adapted / imported / blocked
- Sources reviewed:
- Last updated:
- Notes:

The principles below ship as kit defaults. Adapt them to the repository during
onboarding or the first design-principles intake and record the adaptation in
this section.

## Core Principles

| Principle | Rule | Why |
| --- | --- | --- |
| Side-effect-free modules | Build cohesive features as modules whose core logic is pure functions; isolate I/O, persistence, and external calls at module boundaries (adapters/entrypoints). | Pure cores are testable in isolation and reduce dependency-order problems. |
| Loose coupling | Modules depend on small explicit interfaces, not on other modules' internals; avoid cross-module reach-through into foreign state. | Changes stay local and the regression surface shrinks. |
| Encapsulation over orchestration | State transitions and invariants live with the data that owns them; callers ask the owner to act instead of reading fields and deciding outside. | Prevents invariant drift across call sites. |
| Explicit data ownership | Each piece of state has one owning module/aggregate; other code accesses it through the owner's interface. | Removes ambiguous write paths. |

## Anti-Patterns

| Anti-pattern | Signal | Required response |
| --- | --- | --- |
| Vague "responsibility" reasoning | A design split is justified only by the word "responsibility" (責務) without naming the owned data, invariant, or reason to change | Restate the design in terms of owned state and invariants; if ownership cannot be named, the split is not justified |
| Service-pattern abuse | A new `*Service` / `*Manager` / `*Helper` class pulls logic out of the object that owns the data, leaving anemic models and broken encapsulation | Move behavior to the owning entity/aggregate/module; a Service is allowed only for cross-aggregate coordination or external-boundary orchestration, and the plan must state why the owner cannot hold the logic |
| Constraints outside the aggregate | A validation or state-transition rule that protects an aggregate's invariant is implemented in a caller, controller, or separate validator | Encapsulate the constraint inside the aggregate so no code path can bypass it; callers may pre-check for UX, but the owner enforces |

## Service Introduction Rule

A plan that introduces a new Service/Manager/coordinator class must record:

- the data or invariant the class does NOT own (why the logic cannot live on
  an owning entity/aggregate/module),
- the aggregates/modules it coordinates,
- the side effects it isolates at the boundary.

If none of these apply, put the logic on the owning module instead.

## Waiver Rules

Waivers require a concrete reason, such as a documented framework constraint,
incremental migration away from an existing legacy pattern, performance
evidence requiring denormalized access, explicit user instruction, or no
design-principles artifact found after searched-path review.

Invalid waivers: `N/A`, `manual`, `low risk`, `TBD`, `later`, blank, or a
generic "not applicable" without searched-path evidence.

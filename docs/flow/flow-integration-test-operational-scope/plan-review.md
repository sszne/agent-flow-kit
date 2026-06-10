# flow-integration-test-operational-scope Plan Review

- Reviewed plan: `docs/flow/flow-integration-test-operational-scope/plan.md`
- Reviewed frozen marker: `<!-- frozen: v2 2026-06-10 by Codex -->`
- Plan author: `codex`
- Reviewer agent: `claude-code`
- Review status: `APPROVED`
- Same-agent fallback: `N/A`

## Summary

The v2 plan converts `flow-integration-test` from a single heavy evidence ceremony
into a conditional three-lane evidence model: `Full Gate Required`,
`Lightweight Evidence Allowed`, and `Blocked Early`. It keeps full Playwright
evidence mandatory for visible, multi-step, auth/session/permission/tenant,
provider/device/deploy, external-side-effect, and high-impact workflows while
allowing low-risk non-visible work to record focused substitute evidence.

The v2 plan is implementation-ready. Claude Code re-reviewed the added
surfaces for `flow-impl`, `team-implement`, `context-loader`, and installed
documentation and found no new blocker.

## Missed Risk Review

No blocking missed risks found. The primary risk is that lightweight evidence
could become a broad escape hatch. The plan mitigates this with explicit
high-risk categories, blocker semantics, and required substitute evidence.

## DB / Schema / Migration Review

No database or migration changes are planned. Schema/data compatibility remains
outside the implementation scope.

## Auth / Permission / Tenant Review

No auth implementation changes are planned. The plan explicitly keeps
auth/session/permission/tenant changes in the full-gate-or-blocked category.

## Performance / Query / Load Review

No runtime performance path is affected. The change is a Markdown/template
contract update.

## Dependency / Runtime / External-Service Review

No new dependency is introduced. Provider, device, deployed-domain, and other
external-side-effect paths are explicitly protected from lightweight
downgrades unless the gate is blocked and the blocker is recorded.

## Test And Integration Coverage Review

The planned validation is appropriate for this kit repository:

- static grep for evidence lanes, high-risk guard wording, blocker fields, and
  metrics keys;
- JSON validation for `manifest.json`;
- Python syntax validation for installer/hooks/scripts;
- installer dry-run smoke against a temporary git target;
- `git diff --check`.

App-level Playwright evidence is correctly waived because this kit repository
has no application under test.

## Extra Review Items

Claude Code noted three implementation-phase recommendations:

- include concrete example values for the metrics keys to reduce formatting
  drift;
- verify the installer dry-run command shape against the current `install.py`;
- explicitly state that lightweight evidence does not bypass existing
  provider/deploy and visible-behavior evidence requirements.

These are non-blocking and should be handled during implementation.

## Findings

No Critical, High, or Medium findings.

Low / informational:

- Add small metrics examples during implementation.
- Preserve the existing `business-flow-integration-test` baseline-suite
  boundary.
- Keep Claude and Codex integration-test surfaces aligned.
- Include the additional `flow-impl`, `team-implement`, `context-loader`, and
  installed docs surfaces in the implementation grep checklist.

## Implementation Readiness Decision

APPROVED. Implementation may start from this frozen plan.

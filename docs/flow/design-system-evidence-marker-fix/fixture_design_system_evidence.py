#!/usr/bin/env python3
"""Focused git fixture for the design-system no-doc weak-evidence branch.

Builds temporary git repositories (the current checkout is never mutated) and
runs the matrix gate against a browser-affecting diff with three
Design System Applicability variants:

(a) "Design system found | No" without searched-path/fallback evidence
    -> the gate must fail with the weak-evidence error.
(b) "Design system found | No" with paths-inspected + fallback evidence
    -> the gate must pass.
(c) "Design system found | Yes" complete section
    -> the gate must pass (regression guard for the common path).

Usage:
    python3 docs/flow/design-system-evidence-marker-fix/fixture_design_system_evidence.py
    python3 ...fixture_design_system_evidence.py /path/to/agent-flow-matrix-gate.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_GATE_SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "scripts"
    / "agent-flow-matrix-gate.py"
)

WEAK_EVIDENCE_ERROR = "may record no design system found only"

ONBOARDING_DOCS = (
    "project-structure.md",
    "business-flows.md",
    "integration-scenarios.md",
)

BASE_COMPONENT = """export function Widget({ items }: { items: string[] }) {
  return items.length;
}
"""

# Multi-line logic change so the presentation-only classifier cannot bypass it.
CHANGED_COMPONENT = """export function Widget({ items }: { items: string[] }) {
  if (items.length === 0) {
    return 0;
  }
  const filtered = items.filter((item) => item.trim().length > 0);
  return filtered.length;
}
"""

# Case (a): found-No with evidence cells deliberately free of all accepted
# markers (paths inspected / fallback / existing source / existing component /
# source pattern). Only the always-present check label contains "searched".
CASE_A_SECTION = """## Design System Applicability

| Check | Result | Evidence |
| --- | --- | --- |
| Design system searched | Yes | Looked under docs/agent-flow and styles directories |
| Design system found | No | No design-system document exists in this repository |
| Applies to this plan | No | No shared tokens or component rules to apply |
| Required waivers | No | None |
"""

CASE_B_SECTION = """## Design System Applicability

| Check | Result | Evidence |
| --- | --- | --- |
| Design system searched | Yes | Paths inspected: docs/agent-flow/design-system.md, styles/, components/ui/ |
| Design system found | No | Not found; fallback: existing component patterns in components/widget.tsx |
| Applies to this plan | No | Fallback source patterns applied instead |
| Required waivers | No | None |
"""

CASE_C_SECTION = """## Design System Applicability

| Check | Result | Evidence |
| --- | --- | --- |
| Design system searched | Yes | docs/agent-flow/design-system.md |
| Design system found | Yes | docs/agent-flow/design-system.md defines tokens and component rules |
| Applies to this plan | Yes | Widget uses existing button and list tokens |
| Required waivers | No | None |
"""


def plan_text(design_system_section: str) -> str:
    """Plan carrying every gate requirement so only the section under test varies."""
    return f"""# Test Feature Plan

<!-- frozen: v1 2026-06-12 -->
<!-- plan_author: claude-code -->

## Questioning Decision

- Requirement questions asked: No
- No Questions Rationale: behavior derived from components/widget.tsx in the fixture repository
- User answers: none required

## Business Flow Matrix

| Flow | Actor | Entry point | Normal path | Error paths | Permission paths | Side effects | Regression risk | Required coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Widget filtering | Visitor | /widgets | Filtered count shown | Empty list shows zero | None | None | Count display | Unit and browser |

## Regression Surface Matrix

| Surface | Affected? | Evidence | Required verification |
| --- | --- | --- | --- |
| Widget component | Yes | components/widget.tsx | Unit and browser check |

## Test Design Matrix

| Test ID | Level | Case type | Target | Scenario | Assertions |
| --- | --- | --- | --- | --- | --- |
| T-001 | Unit | Happy | Widget | Render with items | Count matches |

## Integration Coverage Contract

| Flow | Required coverage | Required case types | Waiver / blocker if not covered |
| --- | --- | --- | --- |
| Widget filtering | Unit and browser | Happy, validation, permission, boundary, side effect, regression | None |

{design_system_section}

## Design Principles Compliance

| Check | Result | Evidence |
| --- | --- | --- |
| Design principles searched | Yes | docs/agent-flow/design-principles.md reviewed |
| Design principles found | Yes | docs/agent-flow/design-principles.md |
| Applies to this plan | Yes | Widget stays a pure presentational component |
| Required waivers | No | None |

| Principle / anti-pattern | Affected design element | How the plan applies it | Exception / waiver |
| --- | --- | --- | --- |
| Side-effect-free modules | Widget | Pure filtering helper inside the component | None |

## Plan Review Requirement

- Requirement: Optional
- Reason: localized single-component display logic change without auth, schema, provider, or shared-service impact

## Playwright Integration Test Plan

Single screen check: load /widgets and confirm the filtered count renders.
"""


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.com", *args],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def build_repo(root: Path, gate_script: Path, design_system_section: str) -> Path:
    root.mkdir(parents=True)
    run_git(root, "-c", "init.defaultBranch=main", "init")

    for doc in ONBOARDING_DOCS:
        path = root / "docs" / "agent-flow" / doc
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {doc}\n\nFixture onboarding doc.\n", encoding="utf-8")

    scripts_dir = root / "scripts"
    scripts_dir.mkdir()
    shutil.copy(gate_script, scripts_dir / "agent-flow-matrix-gate.py")

    component = root / "components" / "widget.tsx"
    component.parent.mkdir(parents=True)
    component.write_text(BASE_COMPONENT, encoding="utf-8")

    run_git(root, "add", "-A")
    run_git(root, "commit", "-m", "base")

    run_git(root, "checkout", "-b", "feature")
    component.write_text(CHANGED_COMPONENT, encoding="utf-8")
    plan_path = root / "docs" / "flow" / "test-feature" / "plan.md"
    plan_path.parent.mkdir(parents=True)
    plan_path.write_text(plan_text(design_system_section), encoding="utf-8")
    run_git(root, "add", "-A")
    run_git(root, "commit", "-m", "feature change")
    return root


def run_gate(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/agent-flow-matrix-gate.py", "--base", "main"],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> int:
    gate_script = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_GATE_SCRIPT
    if not gate_script.is_file():
        print(f"Gate script not found: {gate_script}", file=sys.stderr)
        return 2

    cases = (
        ("a", CASE_A_SECTION, 1, WEAK_EVIDENCE_ERROR),
        ("b", CASE_B_SECTION, 0, ""),
        ("c", CASE_C_SECTION, 0, ""),
    )
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, section, expected_exit, expected_message in cases:
            repo = build_repo(Path(tmp) / f"case-{name}", gate_script, section)
            result = run_gate(repo)
            ok = result.returncode == expected_exit
            if ok and expected_message:
                ok = expected_message in result.stderr
            status = "PASS" if ok else "FAIL"
            print(f"case ({name}): {status} (exit={result.returncode}, expected={expected_exit})")
            if result.stdout.strip():
                print(f"  stdout: {result.stdout.strip()}")
            if result.stderr.strip():
                print(f"  stderr: {result.stderr.strip()}")
            if not ok:
                failures.append(name)

    if failures:
        print(f"FAILED cases: {', '.join(failures)}")
        return 1
    print("All fixture cases passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

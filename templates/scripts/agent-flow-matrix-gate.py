#!/usr/bin/env python3
"""CI gate for behavior-changing work plans.

Behavior-affecting changes must ship with a frozen plan that includes
the business-flow, regression-surface, and test-design matrices used by the
agent workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_RISKY_PREFIXES = (
    "app/",
    "pages/",
    "components/",
    "src/",
    "lib/",
    "hooks/",
    "services/",
    "features/",
    "server/",
    "packages/",
    "apps/",
    "public/",
    "styles/",
    "config/",
    "prisma/",
    "drizzle/",
    "supabase/",
    "db/",
    "migrations/",
    "docker/",
    "infra/",
)

DEFAULT_RISKY_FILES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lockb",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "middleware.js",
    "middleware.ts",
    "tsconfig.json",
    "jsconfig.json",
    "tailwind.config.js",
    "tailwind.config.ts",
    "postcss.config.js",
    "postcss.config.mjs",
    "prisma/schema.prisma",
    "drizzle.config.js",
    "drizzle.config.ts",
    "vercel.json",
    "docker-compose.yml",
    "Dockerfile",
}

REQUIRED_PLAN_MARKERS = (
    "Business Flow Matrix",
    "Regression Surface Matrix",
    "Test Design Matrix",
    "Integration Coverage Contract",
)

REQUIRED_PLAN_REVIEW_MARKERS = (
    "Missed Risk Review",
    "DB / Schema / Migration Review",
    "Auth / Permission / Tenant Review",
    "Performance / Query / Load Review",
    "Dependency / Runtime / External-Service Review",
    "Test And Integration Coverage Review",
    "Extra Review Items",
    "Findings",
    "Implementation Readiness Decision",
)

REQUIRED_ONBOARDING_DOCS = (
    "docs/agent-flow/project-structure.md",
    "docs/agent-flow/business-flows.md",
    "docs/agent-flow/integration-scenarios.md",
)

MIGRATION_MARKERS = (
    "Migration / Runtime Enforcement",
    "Migration enforcement path",
    "Runtime validation command",
)

DEFAULT_BROWSER_RISKY_PREFIXES = (
    "app/",
    "pages/",
    "components/",
    "src/pages/",
    "src/app/",
    "src/components/",
    "src/features/",
    "src/ui/",
    "src/styles/",
    "styles/",
    "public/",
)

DEFAULT_BROWSER_RISKY_FILES = {
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "tailwind.config.js",
    "tailwind.config.ts",
    "postcss.config.js",
    "postcss.config.mjs",
}

DEFAULT_MIGRATION_PREFIXES = (
    "prisma/migrations/",
    "drizzle/",
    "supabase/migrations/",
    "db/migrations/",
    "database/migrations/",
    "migrations/",
)

DEFAULT_MIGRATION_FILES = {
    "prisma/schema.prisma",
    "drizzle.config.js",
    "drizzle.config.ts",
}

REQUIRED_CONTRACT_CASE_TYPES = {
    "happy": ("happy", "normal", "正常"),
    "validation": ("validation", "invalid", "バリデーション", "検証"),
    "permission": ("permission", "ownership", "auth", "authorization", "権限", "認可", "所有"),
    "boundary": ("boundary", "edge", "境界"),
    "side effect": ("side effect", "side-effect", "side effects", "mail", "pdf", "job", "副作用"),
    "regression": ("regression", "デグレ", "回帰"),
}

WEAK_WAIVER_VALUES = {
    "",
    "-",
    "todo",
    "tbd",
    "later",
    "manual",
    "manual check",
    "low risk",
    "n/a",
    "na",
    "none",
    "なし",
    "未定",
}

WAIVER_REASON_MARKERS = (
    "because",
    "reason",
    "blocked by",
    "blocker",
    "out of scope",
    "low-risk reason",
    "理由",
    "根拠",
    "ブロック",
    "対象外",
    "低リスク",
)

OBSOLETE_WORKFLOW_PATHS = (
    ".claude/commands/kairo-design.md",
    ".claude/commands/kairo-implement.md",
    ".claude/commands/kairo-requirements.md",
    ".claude/commands/kairo-task-verify.md",
    ".claude/commands/kairo-tasks.md",
    ".claude/skills/sdd-1-plan/SKILL.md",
    ".claude/skills/sdd-2-impl/SKILL.md",
)


def load_config() -> dict:
    config_path = REPO_ROOT / ".agent-flow" / "config.json"
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Invalid .agent-flow/config.json: {exc}") from exc


def git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def git_optional(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def changed_files(base: str | None) -> list[str]:
    if base:
        merge_base = git(["merge-base", base, "HEAD"])
        output = git(["diff", "--name-only", f"{merge_base}...HEAD"])
    else:
        names: set[str] = set()
        has_head = bool(git_optional(["rev-parse", "--verify", "HEAD"]))
        diff_args = [["diff", "--name-only", "--cached"], ["ls-files", "--others", "--exclude-standard"]]
        if has_head:
            diff_args.insert(0, ["diff", "--name-only", "HEAD"])
        for args in diff_args:
            names.update(line for line in git_optional(args).splitlines() if line)
        return sorted(names)

    return sorted(line for line in output.splitlines() if line)


def is_risky(path: str, prefixes: tuple[str, ...], files: set[str]) -> bool:
    return path in files or any(path.startswith(prefix) for prefix in prefixes)


def is_plan(path: str) -> bool:
    return bool(re.fullmatch(r"docs/flow/[^/]+/plan\.md", path))


def plan_review_path(plan_path: str) -> str:
    return str(Path(plan_path).with_name("plan-review.md")).replace("\\", "/")


def read_plan(paths: list[str]) -> str:
    parts: list[str] = []
    for raw_path in paths:
        path = REPO_ROOT / raw_path
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def extract_section(text: str, marker: str) -> str:
    heading = re.search(rf"^#+\s+.*{re.escape(marker)}.*$", text, re.MULTILINE)
    if not heading:
        return ""
    next_heading = re.search(r"^#+\s+", text[heading.end() :], re.MULTILINE)
    if not next_heading:
        return text[heading.end() :]
    return text[heading.end() : heading.end() + next_heading.start()]


def extract_frozen_marker(plan_text: str) -> str:
    match = re.search(r"<!--\s*frozen:\s*[^>]*-->", plan_text)
    if match:
        return " ".join(match.group(0).split())
    return ""


def extract_plan_author(plan_text: str) -> str:
    match = re.search(r"<!--\s*plan_author:\s*([A-Za-z0-9_-]+)\s*-->", plan_text)
    if match:
        return match.group(1).strip().lower()

    frozen = extract_frozen_marker(plan_text).lower()
    if "by codex" in frozen:
        return "codex"
    if "by claude" in frozen:
        return "claude-code"
    return "unknown"


def normalize_metadata_value(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def review_metadata(review_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in review_text.splitlines():
        match = re.match(r"^-\s+([^:]+):\s*(.+?)\s*$", line.strip())
        if not match:
            continue
        key = match.group(1).strip().lower()
        metadata[key] = normalize_metadata_value(match.group(2))
    return metadata


def has_concrete_fallback(value: str) -> bool:
    fallback_lc = value.strip().lower()
    if fallback_lc in WEAK_WAIVER_VALUES or fallback_lc in {"n/a", "na", "none", "-"}:
        return False
    return any(marker in fallback_lc for marker in WAIVER_REASON_MARKERS)


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def data_rows(section: str) -> list[list[str]]:
    rows = table_rows(section)
    if len(rows) < 2:
        return []
    return rows[1:]


def contains_placeholder(text: str) -> bool:
    return bool(re.search(r"\{[^}\n]+\}", text))


def validate_table_section(plan_text: str, marker: str, errors: list[str]) -> None:
    section = extract_section(plan_text, marker)
    if not section.strip():
        errors.append(f"Plan section is empty or missing content: {marker}.")
        return
    rows = data_rows(section)
    if not rows:
        errors.append(f"Plan section requires at least one concrete table row: {marker}.")
        return
    if contains_placeholder("\n".join("|".join(row) for row in rows)):
        errors.append(f"Plan section still contains template placeholders: {marker}.")


def validate_integration_coverage_contract(plan_text: str, errors: list[str]) -> None:
    section = extract_section(plan_text, "Integration Coverage Contract")
    rows = table_rows(section)
    if len(rows) < 2:
        errors.append("Integration Coverage Contract requires a table with at least one concrete flow row.")
        return

    header = [cell.lower() for cell in rows[0]]
    waiver_index = next((idx for idx, cell in enumerate(header) if "waiver" in cell or "blocker" in cell), None)
    if waiver_index is None:
        errors.append("Integration Coverage Contract table requires a waiver/blocker column.")

    lower_section = section.lower()
    for case_type, aliases in REQUIRED_CONTRACT_CASE_TYPES.items():
        if not any(alias.lower() in lower_section for alias in aliases):
            errors.append(f"Integration Coverage Contract is missing required case type: {case_type}.")

    for row in rows[1:]:
        row_text = " | ".join(row)
        if contains_placeholder(row_text):
            errors.append("Integration Coverage Contract still contains template placeholders.")
            continue
        if waiver_index is None or waiver_index >= len(row):
            continue
        waiver = row[waiver_index].strip()
        waiver_lc = waiver.lower()
        if waiver_lc in {"n/a", "na", "none", "-", "なし", "該当なし"}:
            continue
        if waiver_lc in WEAK_WAIVER_VALUES or "todo" in waiver_lc or "tbd" in waiver_lc:
            errors.append(f"Waiver/blocker is too vague: {waiver}")
            continue
        if not any(marker in waiver_lc for marker in WAIVER_REASON_MARKERS):
            errors.append(
                "Waiver/blocker must include a concrete reason marker "
                "(because/reason/blocked by/out of scope/理由/根拠/ブロック/対象外): "
                + waiver
            )


def validate_questioning_decision(plan_text: str, errors: list[str]) -> None:
    section = extract_section(plan_text, "Questioning Decision")
    if not section.strip():
        section = extract_section(plan_text, "Questioning Decision And User Answers")
    if not section.strip():
        errors.append(
            "Plan must document requirement questioning or a source-backed No Questions Rationale."
        )
        return

    if contains_placeholder(section):
        errors.append("Questioning Decision still contains template placeholders.")

    lower_section = section.lower()
    if "requirement questions asked" not in lower_section and "questions asked" not in lower_section:
        errors.append("Questioning Decision must state whether requirement questions were asked.")

    if "user answers" not in lower_section:
        errors.append("Questioning Decision must summarize user answers or state that none were required.")

    no_questions_match = re.search(
        r"(?:requirement\s+)?questions\s+asked\s*:\s*(no|いいえ|なし)",
        lower_section,
    )
    if no_questions_match:
        if "no questions rationale" not in lower_section:
            errors.append("Questioning Decision must include No Questions Rationale when no questions were asked.")
        elif any(
            weak in lower_section
            for weak in (
                "no questions rationale: n/a",
                "no questions rationale: -",
                "no questions rationale: none",
            )
        ):
            errors.append("No Questions Rationale must include concrete source evidence, not a weak placeholder.")


def validate_plan_review(plan_path: str, plan_text: str, errors: list[str]) -> None:
    review_relative = plan_review_path(plan_path)
    review_file = REPO_ROOT / review_relative
    if not review_file.exists():
        errors.append(
            f"Behavior-affecting changes require approved plan review: {review_relative}."
        )
        return

    review_text = review_file.read_text(encoding="utf-8")
    metadata = review_metadata(review_text)
    frozen_marker = extract_frozen_marker(plan_text)
    plan_author = extract_plan_author(plan_text)

    if not frozen_marker:
        errors.append(f"{plan_path} has no frozen marker to review.")
        return

    required_fields = {
        "reviewed plan",
        "reviewed frozen marker",
        "plan author",
        "reviewer agent",
        "review status",
        "same-agent fallback",
    }
    missing_fields = sorted(field for field in required_fields if field not in metadata)
    if missing_fields:
        errors.append(
            f"{review_relative} is missing required metadata: {', '.join(missing_fields)}."
        )
        return

    reviewed_plan = metadata["reviewed plan"].strip("`")
    if reviewed_plan != plan_path:
        errors.append(
            f"{review_relative} reviews {reviewed_plan}, but expected {plan_path}."
        )

    reviewed_frozen = " ".join(metadata["reviewed frozen marker"].split())
    if reviewed_frozen != frozen_marker:
        errors.append(
            f"{review_relative} is stale: reviewed frozen marker does not match current plan."
        )

    status = metadata["review status"].strip("`").upper()
    if status != "APPROVED":
        errors.append(f"{review_relative} must be APPROVED, found {status}.")

    review_plan_author = metadata["plan author"].strip("`").lower()
    if review_plan_author not in {"codex", "claude-code", "unknown"}:
        errors.append(
            f"{review_relative} has invalid Plan author: {metadata['plan author']}."
        )
    if review_plan_author != plan_author:
        errors.append(
            f"{review_relative} plan author {review_plan_author} does not match "
            f"{plan_path} author {plan_author}."
        )

    reviewer = metadata["reviewer agent"].strip("`").lower()
    if reviewer not in {"codex", "claude-code"}:
        errors.append(
            f"{review_relative} has invalid Reviewer agent: {metadata['reviewer agent']}."
        )

    fallback = metadata["same-agent fallback"]
    if reviewer == review_plan_author and review_plan_author != "unknown":
        if not has_concrete_fallback(fallback):
            errors.append(
                f"{review_relative} is same-agent review without a concrete fallback reason."
            )

    for marker in REQUIRED_PLAN_REVIEW_MARKERS:
        if marker not in review_text:
            errors.append(f"{review_relative} is missing required review section: {marker}.")


def fail(messages: list[str]) -> int:
    print("Agent flow matrix gate failed:", file=sys.stderr)
    for message in messages:
        print(f"- {message}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="Base branch/ref to diff against, e.g. origin/main")
    args = parser.parse_args()
    config = load_config()
    risky_prefixes = tuple(config.get("behavior_affecting_prefixes", DEFAULT_RISKY_PREFIXES))
    risky_files = set(config.get("behavior_affecting_files", sorted(DEFAULT_RISKY_FILES)))
    browser_prefixes = tuple(config.get("browser_affecting_prefixes", DEFAULT_BROWSER_RISKY_PREFIXES))
    browser_files = set(config.get("browser_affecting_files", sorted(DEFAULT_BROWSER_RISKY_FILES)))
    migration_prefixes = tuple(config.get("migration_affecting_prefixes", DEFAULT_MIGRATION_PREFIXES))
    migration_files = set(config.get("migration_affecting_files", sorted(DEFAULT_MIGRATION_FILES)))

    obsolete_paths = [path for path in OBSOLETE_WORKFLOW_PATHS if (REPO_ROOT / path).exists()]
    if obsolete_paths:
        return fail(
            [
                "Obsolete workflow command/skill files are not allowed.",
                "Remove these files: " + ", ".join(obsolete_paths),
                "Use /flow-plan and /flow-impl instead.",
            ]
        )

    paths = changed_files(args.base)
    risky_paths = [path for path in paths if is_risky(path, risky_prefixes, risky_files)]
    if not risky_paths:
        print("Agent flow matrix gate: no behavior-affecting changes detected.")
        return 0

    plan_paths = [path for path in paths if is_plan(path)]
    errors: list[str] = []

    if not plan_paths:
        errors.append(
            "Behavior-affecting changes require a changed docs/flow/{feature}/plan.md file."
        )
        errors.append("Risky changed files: " + ", ".join(risky_paths))
        return fail(errors)

    plan_text = read_plan(plan_paths)
    if not plan_text:
        errors.append("Changed plan file was not readable.")
        return fail(errors)

    missing_onboarding_docs = [
        path for path in REQUIRED_ONBOARDING_DOCS if not (REPO_ROOT / path).exists()
    ]
    if missing_onboarding_docs:
        errors.append(
            "Behavior-affecting changes require agent-flow onboarding docs before implementation."
        )
        errors.append("Missing onboarding docs: " + ", ".join(missing_onboarding_docs))

    if "<!-- frozen:" not in plan_text:
        errors.append("Plan must be frozen with a '<!-- frozen: vN YYYY-MM-DD -->' marker.")

    for marker in REQUIRED_PLAN_MARKERS:
        if marker not in plan_text:
            errors.append(f"Plan is missing required section: {marker}.")
        else:
            validate_table_section(plan_text, marker, errors)

    for plan_path in plan_paths:
        path = REPO_ROOT / plan_path
        if path.exists():
            validate_plan_review(plan_path, path.read_text(encoding="utf-8"), errors)

    if "Integration Coverage Contract" in plan_text:
        validate_integration_coverage_contract(plan_text, errors)

    validate_questioning_decision(plan_text, errors)

    has_migration_change = any(
        path in migration_files or any(path.startswith(prefix) for prefix in migration_prefixes)
        for path in risky_paths
    )
    if has_migration_change:
        for marker in MIGRATION_MARKERS:
            if marker not in plan_text:
                errors.append(f"Migration change requires plan marker: {marker}.")

    has_browser_change = any(
        path in browser_files or any(path.startswith(prefix) for prefix in browser_prefixes)
        for path in risky_paths
    )
    if has_browser_change and "Playwright Integration Test Plan" not in plan_text:
        errors.append(
            "Visible browser changes require a Playwright Integration Test Plan in the frozen plan."
        )

    if errors:
        return fail(errors)

    print("Agent flow matrix gate: required matrices and coverage contract found in frozen plan.")
    print("Plan files: " + ", ".join(plan_paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())

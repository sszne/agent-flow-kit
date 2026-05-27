#!/usr/bin/env python3
"""Inject impact-first integration-test guidance for risky implementation work."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_CHANGED_FILES = 200

CODE_CHANGE_PROMPT_PATTERNS = [
    r"実装",
    r"修正",
    r"変更",
    r"追加",
    r"改修",
    r"リファクタ",
    r"デグレ",
    r"migration",
    r"migrate",
    r"schema",
    r"implement",
    r"fix",
    r"change",
    r"add",
    r"refactor",
]

TEST_COMMAND_PATTERNS = [
    "test",
    "php artisan test",
    "phpunit",
    "playwright",
    "cypress",
    "npm run build",
    "composer test",
]

RISKY_SOURCE_MARKERS = [
    "/app/",
    "/routes/",
    "/resources/views/",
    "/resources/js/",
    "/controllers/",
    "/models/",
    "/services/",
    "/actions/",
    "/middleware/",
    "/policies/",
    "/requests/",
    "/jobs/",
    "/listeners/",
    "/mail/",
    "/database/seeders/",
    "/config/",
    "/api/",
]

SHARED_MARKERS = [
    "/app/services/",
    "/app/actions/",
    "/app/helpers/",
    "/app/view/composers/",
    "/app/http/middleware/",
    "/resources/views/components/",
    "/resources/views/partials/",
    "/resources/views/admin/shared/",
    "/resources/js/common",
]

MIGRATION_MARKERS = [
    "/database/migrations/",
    "/migrations/",
    "/schema.sql",
]

INTEGRATION_TEST_MARKERS = [
    "/tests/feature/",
    "/tests/browser/",
    "/test/",
    "/e2e/",
    "/playwright/",
    "/cypress/",
    ".feature.",
    ".spec.",
    ".test.",
]


def project_dir() -> Path:
    """Resolve the active project directory."""
    for key in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR"):
        value = os.environ.get(key)
        if value:
            return Path(value)
    return Path.cwd()


def normalize_path(path: str) -> str:
    """Normalize a path for marker matching."""
    if not path:
        return ""
    return "/" + path.replace("\\", "/").lstrip("/")


def run_git(args: list[str], cwd: Path) -> list[str]:
    """Run git and return non-empty output lines."""
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True,
            check=False,
            text=True,
            timeout=2,
        )
    except Exception:
        return []

    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def changed_files(cwd: Path) -> list[str]:
    """Return changed files from the working tree and index."""
    files: list[str] = []
    for args in (["diff", "--name-only", "--"], ["diff", "--cached", "--name-only", "--"]):
        for file_path in run_git(args, cwd):
            if file_path not in files:
                files.append(file_path)
            if len(files) >= MAX_CHANGED_FILES:
                return files
    return files


def matches_any(path: str, markers: list[str]) -> bool:
    """Return whether a normalized path contains any marker."""
    normalized = normalize_path(path).lower()
    return any(marker.lower() in normalized for marker in markers)


def is_risky_source(path: str) -> bool:
    """Return whether a changed path can affect integration behavior."""
    normalized = normalize_path(path).lower()
    if matches_any(path, MIGRATION_MARKERS + RISKY_SOURCE_MARKERS):
        return True
    return any(
        normalized.endswith(extension)
        for extension in (".php", ".ts", ".tsx", ".js", ".jsx", ".blade.php")
    )


def is_integration_test(path: str) -> bool:
    """Return whether a path looks like integration/browser/scenario coverage."""
    return matches_any(path, INTEGRATION_TEST_MARKERS)


def risk_labels(files: list[str]) -> list[str]:
    """Summarize risk categories from changed files."""
    labels: list[str] = []
    normalized = [normalize_path(path).lower() for path in files]
    if any(matches_any(path, MIGRATION_MARKERS) for path in files):
        labels.append("schema/migration")
    if any("/routes/" in path or "/api/" in path for path in normalized):
        labels.append("route/API")
    if any("/resources/views/" in path or "/resources/js/" in path for path in normalized):
        labels.append("screen/view")
    if any(matches_any(path, SHARED_MARKERS) for path in files):
        labels.append("shared logic")
    if not labels and any(is_risky_source(path) for path in files):
        labels.append("application behavior")
    return labels


def integration_gate_message(reason: str, files: list[str] | None = None) -> str:
    """Build the guidance injected into agent context."""
    labels = risk_labels(files or [])
    risk_text = f" Detected risk: {', '.join(labels)}." if labels else ""

    return (
        f"[Integration Test Quality Gate] {reason}.{risk_text} "
        "Before reporting implementation/test completion, inspect the Business Flow Matrix and Regression Surface Matrix. "
        "Add or update integration-level coverage for affected routes, screens, API flows, shared logic, schema-dependent paths, jobs, mail, PDFs, and browser behavior. "
        "Focused unit tests alone are not enough when another runtime entrypoint can regress. "
        "For schema changes, verify where migrations are enforced and validate a migrated runtime. "
        "If coverage is intentionally omitted, state the concrete low-risk reason or blocker in the final report."
    )


def emit(message: str) -> None:
    """Emit hook context."""
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "IntegrationTestQualityGate",
                    "additionalContext": message,
                }
            },
            ensure_ascii=False,
        )
    )


def prompt_needs_gate(prompt: str) -> bool:
    """Return whether a user prompt appears to request development work."""
    if len(prompt.strip()) < 8:
        return False
    return any(re.search(pattern, prompt, re.IGNORECASE) for pattern in CODE_CHANGE_PROMPT_PATTERNS)


def is_test_command(command: str) -> bool:
    """Return whether a command looks like verification."""
    command_lower = command.lower()
    return any(pattern in command_lower for pattern in TEST_COMMAND_PATTERNS)


def main() -> None:
    """Run hook."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    cwd = project_dir()
    tool_name = data.get("tool_name", "")

    if "prompt" in data and prompt_needs_gate(str(data.get("prompt", ""))):
        emit(
            integration_gate_message(
                "Development work detected; test design must start from business-flow impact analysis"
            )
        )
        return

    changed = changed_files(cwd)
    risky_changed = [path for path in changed if is_risky_source(path)]
    has_integration_change = any(is_integration_test(path) for path in changed)

    tool_input = data.get("tool_input", {})
    file_path = str(tool_input.get("file_path", ""))

    if tool_name in {"Edit", "Write", "MultiEdit"} and file_path and is_risky_source(file_path):
        files_for_message = [*changed, file_path] if file_path not in changed else changed
        reason = "Risky implementation file edited"
        if not has_integration_change:
            reason += " and the current diff does not yet show integration/browser/scenario coverage"
        emit(integration_gate_message(reason, files_for_message))
        return

    if tool_name == "Bash":
        command = str(tool_input.get("command", ""))
        if is_test_command(command) and risky_changed and not has_integration_change:
            emit(
                integration_gate_message(
                    "Verification command ran, but risky changed files currently have no matching integration/browser/scenario test changes",
                    risky_changed,
                )
            )
        elif is_test_command(command) and any(matches_any(path, MIGRATION_MARKERS) for path in risky_changed):
            emit(
                integration_gate_message(
                    "Verification command ran after schema/migration changes; migration enforcement and migrated runtime verification are required",
                    risky_changed,
                )
            )


if __name__ == "__main__":
    main()

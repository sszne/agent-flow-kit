#!/usr/bin/env python3
"""Block risky behavior edits until a frozen flow plan exists."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


DEFAULT_BEHAVIOR_PREFIXES = [
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
]

DEFAULT_BEHAVIOR_FILES = [
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
]


def project_dir() -> Path:
    """Resolve the active project directory."""
    for key in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR"):
        value = os.environ.get(key)
        if value:
            return Path(value).resolve()
    return Path.cwd().resolve()


def load_config(cwd: Path) -> dict:
    """Load optional agent-flow config."""
    path = cwd / ".agent-flow" / "config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def relative_path(path: str, cwd: Path) -> str:
    """Return a slash-normalized path relative to the project when possible."""
    if not path:
        return ""
    candidate = Path(path)
    if not candidate.is_absolute():
        return path.replace("\\", "/").lstrip("/")
    try:
        return str(candidate.resolve().relative_to(cwd)).replace("\\", "/")
    except ValueError:
        return str(candidate).replace("\\", "/").lstrip("/")


def is_behavior_affecting(path: str, config: dict) -> bool:
    """Return whether the path should require a frozen flow plan."""
    normalized = path.replace("\\", "/").lstrip("/")
    prefixes = config.get("behavior_affecting_prefixes", DEFAULT_BEHAVIOR_PREFIXES)
    files = set(config.get("behavior_affecting_files", DEFAULT_BEHAVIOR_FILES))
    return normalized in files or any(normalized.startswith(prefix) for prefix in prefixes)


def frozen_plan_exists(cwd: Path) -> bool:
    """Return whether at least one frozen flow plan exists."""
    for plan in (cwd / "docs" / "flow").glob("*/plan.md"):
        try:
            if "<!-- frozen:" in plan.read_text(encoding="utf-8"):
                return True
        except Exception:
            continue
    return False


def block(message: str) -> None:
    """Block the tool call in Claude-style hook runners."""
    payload = {
        "decision": "block",
        "reason": message,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": message,
        },
    }
    print(json.dumps(payload, ensure_ascii=False))
    print(message, file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    """Run the gate."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    tool_name = str(data.get("tool_name", ""))
    if tool_name not in {"Edit", "Write", "MultiEdit"}:
        return

    if os.environ.get("AGENT_FLOW_ALLOW_DIRECT_EDIT") == "1":
        return

    cwd = project_dir()
    tool_input = data.get("tool_input", {})
    file_path = relative_path(str(tool_input.get("file_path", "")), cwd)
    if not file_path:
        return

    config = load_config(cwd)
    if not is_behavior_affecting(file_path, config):
        return

    if frozen_plan_exists(cwd):
        return

    block(
        "[Flow Plan Required Gate] Blocking behavior-affecting edit because no frozen "
        f"`docs/flow/{{feature_name}}/plan.md` was found. Target file: `{file_path}`. "
        "Run `/flow-plan {feature_name}` first and freeze the plan before editing runtime, "
        "business-flow, schema, auth, UI, API, job, mail/PDF, search, or shared logic files. "
        "For an intentional emergency bypass, set `AGENT_FLOW_ALLOW_DIRECT_EDIT=1` and document "
        "the reason in the final report."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Block risky behavior edits until a frozen flow plan exists."""

from __future__ import annotations

import json
import os
import re
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

DEFAULT_PRESENTATION_ONLY_PREFIXES = [
    "styles/",
    "src/styles/",
    "app/styles/",
    "public/styles/",
]

DEFAULT_PRESENTATION_ONLY_EXTENSIONS = [
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".pcss",
]

DEFAULT_PRESENTATION_UI_EXTENSIONS = [
    ".html",
    ".htm",
    ".jsx",
    ".tsx",
    ".vue",
    ".svelte",
    ".blade.php",
    ".erb",
    ".twig",
]

PRESENTATION_ATTR_RE = re.compile(
    r"(\b(?:class|className|style|aria-label|title|placeholder|alt|label)\s*=\s*)"
    r"(\"[^\"]*\"|'[^']*'|\{[^{}\n]*(?:\"[^\"]*\"|'[^']*')[^{}\n]*\})"
)
TEXT_NODE_RE = re.compile(r">[^<>{}\n][^<>{}]*<")


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


def configured_tuple(config: dict, key: str, default: list[str]) -> tuple[str, ...]:
    """Return a config list as a tuple of strings."""
    values = config.get(key, default)
    if not isinstance(values, list):
        return tuple(default)
    return tuple(str(value) for value in values)


def is_style_path(path: str, config: dict) -> bool:
    """Return whether a path is display-only by file type or style prefix."""
    normalized = path.replace("\\", "/").lstrip("/")
    prefixes = configured_tuple(config, "presentation_only_prefixes", DEFAULT_PRESENTATION_ONLY_PREFIXES)
    extensions = configured_tuple(
        config,
        "presentation_only_extensions",
        DEFAULT_PRESENTATION_ONLY_EXTENSIONS,
    )
    return normalized.endswith(extensions) or any(normalized.startswith(prefix) for prefix in prefixes)


def is_ui_presentation_path(path: str, config: dict) -> bool:
    """Return whether a path can contain verifiable display-only markup edits."""
    normalized = path.replace("\\", "/").lstrip("/")
    extensions = configured_tuple(
        config,
        "presentation_ui_extensions",
        DEFAULT_PRESENTATION_UI_EXTENSIONS,
    )
    return normalized.endswith(extensions)


def edit_pairs(tool_name: str, tool_input: dict) -> list[tuple[str, str]]:
    """Extract old/new edit fragments when the hook input exposes them."""
    if tool_name == "Edit":
        return [
            (
                str(tool_input.get("old_string", "")),
                str(tool_input.get("new_string", "")),
            )
        ]
    if tool_name == "MultiEdit":
        pairs: list[tuple[str, str]] = []
        edits = tool_input.get("edits", [])
        if isinstance(edits, list):
            for edit in edits:
                if isinstance(edit, dict):
                    pairs.append((str(edit.get("old_string", "")), str(edit.get("new_string", ""))))
        return pairs
    return []


def normalize_presentation_fragment(value: str) -> str:
    """Erase allowed presentation-only tokens and preserve surrounding structure."""
    normalized = PRESENTATION_ATTR_RE.sub(r"\1__PRESENTATION__", value)
    normalized = TEXT_NODE_RE.sub(">__TEXT__<", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def is_simple_visible_text(value: str) -> bool:
    """Return whether a fragment is plain visible copy rather than code."""
    text = value.strip().strip("\"'")
    if not text or len(text) > 200 or "\n" in text:
        return False
    if re.search(r"[{}();=<>`]|=>|/api|https?://", text):
        return False
    return True


def is_presentation_pair(old: str, new: str) -> bool:
    """Return whether one edit pair is limited to style/layout/copy tokens."""
    if not old or not new:
        return False
    if is_simple_visible_text(old) and is_simple_visible_text(new):
        return True
    return normalize_presentation_fragment(old) == normalize_presentation_fragment(new)


def is_presentation_only_edit(file_path: str, tool_name: str, tool_input: dict, config: dict) -> bool:
    """Return whether a direct edit can skip flow-plan as display-only work."""
    if is_style_path(file_path, config):
        return True

    if not is_ui_presentation_path(file_path, config):
        return False

    pairs = edit_pairs(tool_name, tool_input)
    return bool(pairs) and all(is_presentation_pair(old, new) for old, new in pairs)


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

    if is_presentation_only_edit(file_path, tool_name, tool_input, config):
        return

    if frozen_plan_exists(cwd):
        return

    block(
        "[Flow Plan Required Gate] Blocking behavior-affecting edit because no frozen "
        f"`docs/flow/{{feature_name}}/plan.md` was found. Target file: `{file_path}`. "
        "Run `/flow-plan {feature_name}` first and freeze the plan before editing runtime, "
        "business-flow, schema, auth, UI, API, job, mail/PDF, search, or shared logic files. "
        "Display-only edits may proceed without flow-plan only when they are limited to minor "
        "style/layout changes or visible text changes that the gate can classify. "
        "For an intentional emergency bypass, set `AGENT_FLOW_ALLOW_DIRECT_EDIT=1` and document "
        "the reason in the final report."
    )


if __name__ == "__main__":
    main()

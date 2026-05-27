#!/usr/bin/env python3
"""Agent-flow onboarding guidance hook.

This hook does not block. It reminds agents to complete the onboarding
knowledge base before behavior-changing implementation starts.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


REQUIRED_DOCS = (
    "docs/agent-flow/project-structure.md",
    "docs/agent-flow/business-flows.md",
    "docs/agent-flow/integration-scenarios.md",
)

IMPLEMENTATION_HINTS = (
    "implement",
    "implementation",
    "fix",
    "bug",
    "feature",
    "change",
    "修正",
    "実装",
    "改修",
    "機能",
    "不具合",
)


def project_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def user_text(payload: dict) -> str:
    for key in ("prompt", "user_prompt", "message"):
        value = payload.get(key)
        if isinstance(value, str):
            return value.lower()
    return json.dumps(payload, ensure_ascii=False).lower()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    root = project_root()
    missing = [path for path in REQUIRED_DOCS if not (root / path).exists()]
    if not missing:
        return 0

    text = user_text(payload)
    if not any(hint in text for hint in IMPLEMENTATION_HINTS):
        return 0

    message = (
        "[Agent Flow Onboarding] Behavior-changing work should start after "
        "repo structure, business flows, and integration scenarios are documented. "
        "Missing: "
        + ", ".join(missing)
        + ". Run the agent-flow-onboarding sequence or document an explicit blocker."
    )

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": payload.get("hook_event_name", "UserPromptSubmit"),
                    "additionalContext": message,
                }
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

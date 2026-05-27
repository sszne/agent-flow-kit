#!/usr/bin/env python3
"""Thin wrapper for the shared Claude onboarding gate hook."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def main() -> int:
    root = Path(os.environ.get("CODEX_PROJECT_DIR") or os.getcwd())
    hook = root / ".claude" / "hooks" / "agent-flow-onboarding-gate.py"
    if not hook.exists():
        return 0
    runpy.run_path(str(hook), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())

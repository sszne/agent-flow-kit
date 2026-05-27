#!/usr/bin/env python3
"""Project wrapper for the shared integration-test quality gate."""

from pathlib import Path
import runpy

PROJECT_HOOK = (
    Path(__file__).resolve().parents[2]
    / ".claude"
    / "hooks"
    / "integration-test-quality-gate.py"
)

if PROJECT_HOOK.exists():
    runpy.run_path(str(PROJECT_HOOK), run_name="__main__")

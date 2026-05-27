#!/usr/bin/env python3
"""Post-tool hook: run lightweight file-local checks after Edit/Write."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

MAX_PATH_LENGTH = 4096


def get_file_path() -> str | None:
    """Extract file path from hook input."""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return None
    return data.get("tool_input", {}).get("file_path")


def valid_path(file_path: str) -> bool:
    """Validate path length and traversal."""
    return bool(file_path) and len(file_path) <= MAX_PATH_LENGTH and ".." not in file_path


def run_command(cmd: list[str], cwd: str) -> tuple[int, str]:
    """Run a command and return returncode plus combined output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return 0, ""
    except subprocess.TimeoutExpired:
        return 1, "Command timed out"
    return result.returncode, (result.stdout or result.stderr)


def main() -> None:
    """Run checks for files that have cheap local validation."""
    file_path = get_file_path()
    if not file_path or not valid_path(file_path):
        return

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    path = Path(file_path)
    rel_path = os.path.relpath(file_path, project_dir) if str(path).startswith(project_dir) else file_path

    if file_path.endswith(".blade.php"):
        return

    if file_path.endswith(".php") and shutil.which("php"):
        code, output = run_command(["php", "-l", file_path], project_dir)
        if code != 0:
            print(f"[lint-on-save] PHP syntax issue in {rel_path}:\n{output}", file=sys.stderr)
        else:
            print(f"[lint-on-save] OK: {rel_path} passed php -l")
        return

    if file_path.endswith(".py") and shutil.which("python3"):
        code, output = run_command(["python3", "-m", "py_compile", file_path], project_dir)
        if code != 0:
            print(f"[lint-on-save] Python syntax issue in {rel_path}:\n{output}", file=sys.stderr)
        else:
            print(f"[lint-on-save] OK: {rel_path} passed py_compile")


if __name__ == "__main__":
    main()

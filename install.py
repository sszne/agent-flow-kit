#!/usr/bin/env python3
"""Install Agent Flow Kit templates into another repository."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent
TEMPLATES = KIT_ROOT / "templates"
CLAUDE_SETTINGS_HOOKS = KIT_ROOT / "references" / "claude-settings-hooks.json"
MANIFEST = KIT_ROOT / "manifest.json"
GITIGNORE_MARKER_START = "# >>> agent-flow-kit"
GITIGNORE_MARKER_END = "# <<< agent-flow-kit"


def iter_template_files() -> list[Path]:
    return sorted(path for path in TEMPLATES.rglob("*") if path.is_file())


def validate_templates() -> None:
    manifest = load_json(MANIFEST)
    missing: list[str] = []

    for skill in manifest.get("entry_skills", []):
        for tool_dir in (".claude", ".codex"):
            skill_path = TEMPLATES / tool_dir / "skills" / skill / "SKILL.md"
            if not skill_path.exists():
                missing.append(str(skill_path.relative_to(KIT_ROOT)))

    for hook_dir in (TEMPLATES / ".claude" / "hooks", TEMPLATES / ".codex" / "hooks"):
        if not hook_dir.exists() or not any(hook_dir.glob("*.py")):
            missing.append(str(hook_dir.relative_to(KIT_ROOT)) + "/*.py")

    if missing:
        print("Agent Flow Kit template is incomplete:", file=sys.stderr)
        for path in missing:
            print(f"- missing {path}", file=sys.stderr)
        raise SystemExit(1)


def target_path(target: Path, template_file: Path) -> Path:
    relative = template_file.relative_to(TEMPLATES)
    if relative == Path("gitignore.agent-flow.fragment"):
        return target / ".gitignore"
    return target / relative


def backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path.with_name(f"{path.name}.agent-flow-backup-{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def copy_file(src: Path, dst: Path, *, force: bool, dry_run: bool) -> None:
    if src.name == "gitignore.agent-flow.fragment":
        return

    if dst.exists() and not force:
        print(f"skip existing: {dst}")
        return

    if dry_run:
        action = "overwrite" if dst.exists() else "create"
        print(f"{action}: {dst}")
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        backup(dst)
    shutil.copy2(src, dst)
    print(f"installed: {dst}")


def install_gitignore(target: Path, *, dry_run: bool) -> None:
    fragment_path = TEMPLATES / "gitignore.agent-flow.fragment"
    fragment = fragment_path.read_text(encoding="utf-8").strip()
    block = f"{GITIGNORE_MARKER_START}\n{fragment}\n{GITIGNORE_MARKER_END}\n"
    gitignore = target / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if GITIGNORE_MARKER_START in current:
        print("skip existing .gitignore agent-flow block")
        return
    if dry_run:
        print(f"append agent-flow block: {gitignore}")
        return
    if gitignore.exists():
        backup(gitignore)
    with gitignore.open("a", encoding="utf-8") as file:
        if current and not current.endswith("\n"):
            file.write("\n")
        file.write("\n" + block)
    print(f"updated: {gitignore}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def hook_key(hook: dict) -> tuple[str, str]:
    return str(hook.get("type", "")), str(hook.get("command", ""))


def merge_hooks(settings: dict, snippet: dict) -> bool:
    """Merge Claude hook snippet into settings and return whether it changed."""
    settings_hooks = settings.setdefault("hooks", {})
    changed = False

    for event_name, snippet_entries in snippet.get("hooks", {}).items():
        target_entries = settings_hooks.setdefault(event_name, [])
        for snippet_entry in snippet_entries:
            matcher = snippet_entry.get("matcher", "")
            target_entry = next(
                (entry for entry in target_entries if entry.get("matcher", "") == matcher),
                None,
            )
            if target_entry is None:
                target_entries.append(snippet_entry)
                changed = True
                continue

            existing = {hook_key(hook) for hook in target_entry.setdefault("hooks", [])}
            for hook in snippet_entry.get("hooks", []):
                if hook_key(hook) not in existing:
                    target_entry["hooks"].append(hook)
                    existing.add(hook_key(hook))
                    changed = True

    return changed


def install_claude_settings(target: Path, *, dry_run: bool) -> None:
    settings_path = target / ".claude" / "settings.json"
    snippet = load_json(CLAUDE_SETTINGS_HOOKS)
    current = load_json(settings_path) if settings_path.exists() else {}
    changed = merge_hooks(current, snippet)

    if not changed:
        print("skip existing .claude/settings.json agent-flow hooks")
        return
    if dry_run:
        action = "merge" if settings_path.exists() else "create"
        print(f"{action}: {settings_path}")
        return

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    if settings_path.exists():
        backup(settings_path)
    settings_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"updated: {settings_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Repository root to install into")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files with backups")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be installed")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 1
    if not (target / ".git").exists():
        print(f"Target does not look like a git repository: {target}", file=sys.stderr)
        return 1

    validate_templates()
    for src in iter_template_files():
        copy_file(src, target_path(target, src), force=args.force, dry_run=args.dry_run)
    install_claude_settings(target, dry_run=args.dry_run)
    install_gitignore(target, dry_run=args.dry_run)

    print("\nNext steps:")
    print("1. Review .agent-flow/config.json for project-specific paths.")
    print("2. Run agent-flow-onboarding to create docs/agent-flow/*.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

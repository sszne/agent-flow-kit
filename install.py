#!/usr/bin/env python3
"""Install Agent Flow Kit templates into another repository."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


KIT_ROOT = Path(__file__).resolve().parent
TEMPLATES = KIT_ROOT / "templates"
CLAUDE_SETTINGS_HOOKS = KIT_ROOT / "references" / "claude-settings-hooks.json"
MANIFEST = KIT_ROOT / "manifest.json"
GITIGNORE_MARKER_START = "# >>> agent-flow-kit"
GITIGNORE_MARKER_END = "# <<< agent-flow-kit"
HOOK_SCRIPT_PATTERN = re.compile(r"\.claude/hooks/([A-Za-z0-9_.-]+\.py)")


SAFE_UPDATE_PREFIXES = (
    ".claude/commands/",
    ".claude/hooks/",
    ".claude/skills/",
    ".codex/hooks/",
    ".codex/skills/",
)

SAFE_UPDATE_FILES = {
    ".codex/hooks.json",
    ".github/workflows/agent-flow-matrix.yml",
    "scripts/agent-flow-matrix-gate.py",
}

LOCAL_FIRST_FILES = {
    ".agent-flow/config.json",
    ".claude/docs/DESIGN.md",
    ".claude/rules/dev-environment.md",
    ".claude/rules/testing.md",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/agent-flow-hardening.md",
    "docs/agent-flow-integration-test.md",
    "docs/flow/agent-flow-hardening/plan.md",
}

LOCAL_FIRST_PREFIXES = (
    ".claude/docs/",
    ".claude/rules/",
    "docs/flow/",
)


@dataclass
class InstallStats:
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    recommended_updates: int = 0
    preserved_local: int = 0
    manual_merges: int = 0
    gitignore_changed: int = 0
    settings_changed: int = 0

    def print_summary(self) -> None:
        print("\nSummary:")
        print(f"- created: {self.created}")
        print(f"- updated: {self.updated}")
        print(f"- unchanged: {self.unchanged}")
        print(f"- recommended updates: {self.recommended_updates}")
        print(f"- preserved local/manual merge: {self.preserved_local + self.manual_merges}")
        print(f"- settings changes: {self.settings_changed}")
        print(f"- gitignore changes: {self.gitignore_changed}")


def iter_template_files() -> list[Path]:
    return sorted(
        path
        for path in TEMPLATES.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )


def validate_templates() -> None:
    manifest = load_json(MANIFEST)
    missing: list[str] = []

    for skill in manifest.get("entry_skills", []) + manifest.get("support_skills", []):
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


def relative_template_path(src: Path) -> str:
    return str(src.relative_to(TEMPLATES)).replace("\\", "/")


def is_safe_update_path(relative: str) -> bool:
    return relative in SAFE_UPDATE_FILES or any(
        relative.startswith(prefix) for prefix in SAFE_UPDATE_PREFIXES
    )


def is_local_first_path(relative: str) -> bool:
    return relative in LOCAL_FIRST_FILES or any(
        relative.startswith(prefix) for prefix in LOCAL_FIRST_PREFIXES
    )


def classify_existing_update(relative: str) -> tuple[str, str]:
    """Classify an existing differing target file for recommended updates."""
    if is_safe_update_path(relative):
        return (
            "safe-overwrite",
            "portable workflow asset; runtime cost is limited to lightweight hook/script dispatch",
        )
    if is_local_first_path(relative):
        return (
            "manual-merge",
            "target-local config, project docs, or workflow history may contain repo-specific decisions",
        )
    return (
        "preserve-local",
        "not in the portable workflow allowlist; review before overwrite",
    )


def backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path.with_name(f"{path.name}.agent-flow-backup-{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def copy_file(
    src: Path,
    dst: Path,
    *,
    force: bool,
    dry_run: bool,
    apply_recommended_updates: bool,
    stats: InstallStats,
) -> None:
    if src.name == "gitignore.agent-flow.fragment":
        return

    if dst.exists() and same_file_content(src, dst):
        print(f"skip unchanged: {dst}")
        stats.unchanged += 1
        return

    relative = relative_template_path(src)
    if dst.exists() and not force:
        classification, reason = classify_existing_update(relative)
        if classification == "safe-overwrite":
            stats.recommended_updates += 1
            if not apply_recommended_updates:
                print(
                    f"recommend overwrite: {dst} "
                    f"({reason}; pass --apply-recommended-updates to apply)"
                )
                return
            if dry_run:
                print(f"recommended overwrite: {dst} ({reason})")
                return
        else:
            if classification == "manual-merge":
                stats.manual_merges += 1
            else:
                stats.preserved_local += 1
            print(f"preserve local ({classification}): {dst} ({reason})")
            return

    if dry_run:
        action = "overwrite" if dst.exists() else "create"
        print(f"{action}: {dst}")
        if dst.exists():
            stats.updated += 1
        else:
            stats.created += 1
        return

    existed = dst.exists()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if existed:
        backup(dst)
    shutil.copy2(src, dst)
    print(f"installed: {dst}")
    if existed:
        stats.updated += 1
    else:
        stats.created += 1


def install_gitignore(target: Path, *, dry_run: bool, stats: InstallStats) -> None:
    fragment_path = TEMPLATES / "gitignore.agent-flow.fragment"
    fragment = fragment_path.read_text(encoding="utf-8").strip()
    block = f"{GITIGNORE_MARKER_START}\n{fragment}\n{GITIGNORE_MARKER_END}\n"
    gitignore = target / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if GITIGNORE_MARKER_START in current:
        print("skip existing .gitignore agent-flow block")
        stats.unchanged += 1
        return
    if dry_run:
        print(f"append agent-flow block: {gitignore}")
        stats.gitignore_changed += 1
        return
    if gitignore.exists():
        backup(gitignore)
    with gitignore.open("a", encoding="utf-8") as file:
        if current and not current.endswith("\n"):
            file.write("\n")
        file.write("\n" + block)
    print(f"updated: {gitignore}")
    stats.gitignore_changed += 1


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def same_file_content(left: Path, right: Path) -> bool:
    try:
        return left.read_bytes() == right.read_bytes()
    except OSError:
        return False


def hook_key(hook: dict) -> tuple[str, str]:
    command = str(hook.get("command", ""))
    script_match = HOOK_SCRIPT_PATTERN.search(command)
    if script_match:
        return str(hook.get("type", "")), f".claude/hooks/{script_match.group(1)}"
    return str(hook.get("type", "")), command


def dedupe_hooks(hooks: list[dict]) -> bool:
    """Remove duplicate hook entries with the same semantic identity."""
    seen: set[tuple[str, str]] = set()
    deduped: list[dict] = []
    changed = False

    for hook in hooks:
        key = hook_key(hook)
        if key in seen:
            changed = True
            continue
        seen.add(key)
        deduped.append(hook)

    if changed:
        hooks[:] = deduped
    return changed


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

            target_hooks = target_entry.setdefault("hooks", [])
            changed = dedupe_hooks(target_hooks) or changed
            existing = {hook_key(hook): index for index, hook in enumerate(target_hooks)}
            for hook in snippet_entry.get("hooks", []):
                key = hook_key(hook)
                if key in existing:
                    index = existing[key]
                    if target_hooks[index] != hook:
                        target_hooks[index] = hook
                        changed = True
                    continue

                target_hooks.append(hook)
                existing[key] = len(target_hooks) - 1
                changed = True

    for target_entries in settings_hooks.values():
        for target_entry in target_entries:
            if dedupe_hooks(target_entry.setdefault("hooks", [])):
                changed = True

    return changed


def install_claude_settings(target: Path, *, dry_run: bool, stats: InstallStats) -> None:
    settings_path = target / ".claude" / "settings.json"
    snippet = load_json(CLAUDE_SETTINGS_HOOKS)
    current = load_json(settings_path) if settings_path.exists() else {}
    changed = merge_hooks(current, snippet)

    if not changed:
        print("skip existing .claude/settings.json agent-flow hooks")
        stats.unchanged += 1
        return
    if dry_run:
        action = "merge" if settings_path.exists() else "create"
        print(f"{action}: {settings_path}")
        stats.settings_changed += 1
        return

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    if settings_path.exists():
        backup(settings_path)
    settings_path.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"updated: {settings_path}")
    stats.settings_changed += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Repository root to install into")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files with backups")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be installed")
    parser.add_argument(
        "--apply-recommended-updates",
        action="store_true",
        help=(
            "Update existing files classified as portable workflow assets while "
            "preserving target-local docs and config. Combine with --dry-run to "
            "preview the recommended update set."
        ),
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 1
    if not (target / ".git").exists():
        print(f"Target does not look like a git repository: {target}", file=sys.stderr)
        return 1

    validate_templates()
    stats = InstallStats()
    for src in iter_template_files():
        copy_file(
            src,
            target_path(target, src),
            force=args.force,
            dry_run=args.dry_run,
            apply_recommended_updates=args.apply_recommended_updates,
            stats=stats,
        )
    install_claude_settings(target, dry_run=args.dry_run, stats=stats)
    install_gitignore(target, dry_run=args.dry_run, stats=stats)

    stats.print_summary()

    print("\nNext steps:")
    print("1. Review .agent-flow/config.json for project-specific paths.")
    print("2. Run agent-flow-onboarding to create docs/agent-flow/*.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

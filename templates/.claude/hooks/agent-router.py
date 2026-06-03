#!/usr/bin/env python3
"""
UserPromptSubmit hook: Route to appropriate agent based on user intent.

Routing rules:
- Multimodal files (PDF/video/audio/image) → Gemini CLI (HIGHEST PRIORITY)
- Existing behavior changes / bug fixes / regressions → /flow-plan (safety gate)
- Codebase understanding / large analysis → Opus subagent (1M context)
- External research / survey → Opus subagent
- Planning, design, complex code → Codex CLI
"""

import json
import re
import sys

# Multimodal file extensions that MUST be processed by Gemini
MULTIMODAL_EXTENSIONS = [
    # PDF
    ".pdf",
    # Video
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    # Audio
    ".mp3", ".wav", ".m4a", ".flac", ".ogg",
    # Image (for detailed analysis — screenshots can be read by Claude directly)
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
]

# Pattern to detect file paths with multimodal extensions
MULTIMODAL_PATTERN = re.compile(
    r'[\w./\\~-]+\.(?:' +
    '|'.join(ext.lstrip('.') for ext in MULTIMODAL_EXTENSIONS) +
    r')(?:\s|$|["\']|,)',
    re.IGNORECASE,
)

# Triggers for Codex (planning, design, debugging, complex implementation)
CODEX_TRIGGERS = {
    "ja": [
        "設計", "どう設計", "アーキテクチャ",
        "計画", "計画を立てて",
        "なぜ動かない", "エラー", "バグ", "デバッグ",
        "どちらがいい", "比較して", "トレードオフ",
        "実装方法", "どう実装",
        "リファクタリング", "リファクタ",
        "レビュー",
        "考えて", "分析して", "深く",
        "最適化",
    ],
    "en": [
        "design", "architecture", "architect",
        "plan", "planning",
        "debug", "error", "bug", "not working", "fails",
        "compare", "trade-off", "tradeoff", "which is better",
        "how to implement", "implementation", "complex",
        "refactor", "simplify",
        "review", "check this",
        "think", "analyze", "deeply",
        "optimize", "performance",
    ],
}

# Triggers for Opus research (codebase analysis + external research)
OPUS_RESEARCH_TRIGGERS = {
    "ja": [
        "調べて", "リサーチ", "調査", "サーベイ",
        "最新", "ドキュメント",
        "ライブラリ", "パッケージ",
        "コードベース", "リポジトリ", "全体構造",
        "理解して", "把握して",
    ],
    "en": [
        "research", "investigate", "look up", "find out", "survey",
        "latest", "documentation", "docs",
        "library", "package", "framework",
        "codebase", "repository", "project structure",
        "understand", "analyze the code",
    ],
}

FLOW_PLAN_REQUIRED_TRIGGERS = {
    "bug_or_regression": [
        "バグ", "不具合", "エラー", "デグレ", "リグレッション", "障害", "失敗", "壊れ",
        "bug", "regression", "incident", "failure", "broken", "not working",
    ],
    "existing_behavior_change": [
        "修正", "変更", "改修", "削除", "置き換え", "既存", "影響", "対応", "改善",
        "fix", "change", "modify", "update", "delete", "replace", "existing",
        "refactor", "migration", "schema",
    ],
    "business_flow_sensitive": [
        "注文", "会社注文", "dealer", "ディーラー", "価格", "料金", "請求", "決済",
        "メール", "pdf", "出荷", "検索", "ステータス", "認証", "権限", "スキーマ",
        "order", "pricing", "billing", "payment", "mail", "shipment", "search",
        "status", "auth", "permission", "schema",
    ],
}

DISPLAY_ONLY_TRIGGERS = [
    "表示のみ", "見た目", "スタイル", "レイアウト", "文言", "文章", "テキスト",
    "コピー", "ラベル", "誤字", "typo", "style", "layout", "copy", "wording",
    "text", "label", "display-only", "visual only",
]

DISPLAY_ONLY_HARD_RISK_TRIGGERS = (
    FLOW_PLAN_REQUIRED_TRIGGERS["bug_or_regression"]
    + FLOW_PLAN_REQUIRED_TRIGGERS["business_flow_sensitive"]
)


FLOW_PLAN_EXPLICIT_PATTERN = re.compile(r"/flow-plan\b", re.IGNORECASE)
FLOW_START_EXPLICIT_PATTERN = re.compile(r"/flow-start\b", re.IGNORECASE)


def detect_multimodal_files(prompt: str) -> str | None:
    """Detect multimodal file references in the prompt. Returns matched file path or None."""
    match = MULTIMODAL_PATTERN.search(prompt)
    if match:
        return match.group(0).strip().rstrip('"\',')
    return None


def detect_agent(prompt: str) -> tuple[str | None, str, bool]:
    """Detect which agent should handle this prompt.

    Returns (agent, trigger, is_multimodal).
    """
    prompt_lower = prompt.lower()

    # HIGHEST PRIORITY: Multimodal file detection → Gemini
    multimodal_file = detect_multimodal_files(prompt)
    if multimodal_file:
        return "gemini-multimodal", multimodal_file, True

    # Codex triggers (planning, design, debug, complex code)
    for triggers in CODEX_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "codex", trigger, False

    # Opus research triggers (codebase analysis + external research)
    for triggers in OPUS_RESEARCH_TRIGGERS.values():
        for trigger in triggers:
            if trigger in prompt_lower:
                return "opus-research", trigger, False

    return None, "", False


def detect_flow_plan_requirement(prompt: str) -> tuple[bool, str, str]:
    """Return whether the prompt should be routed through /flow-plan."""
    if FLOW_PLAN_EXPLICIT_PATTERN.search(prompt):
        return False, "", ""

    prompt_lower = prompt.lower()
    if any(trigger.lower() in prompt_lower for trigger in DISPLAY_ONLY_TRIGGERS):
        if not any(trigger.lower() in prompt_lower for trigger in DISPLAY_ONLY_HARD_RISK_TRIGGERS):
            return False, "", ""

    for category, triggers in FLOW_PLAN_REQUIRED_TRIGGERS.items():
        for trigger in triggers:
            if trigger.lower() in prompt_lower:
                return True, category, trigger

    return False, "", ""


def flow_plan_message(category: str, trigger: str, prompt: str) -> str:
    """Build safety guidance for prompts that should use /flow-plan."""
    if FLOW_START_EXPLICIT_PATTERN.search(prompt):
        route = (
            "The user explicitly mentioned /flow-start, but this request appears to touch "
            "existing behavior or business-flow-sensitive work. Switch to /flow-plan unless "
            "codebase analysis proves it is pure greenfield discovery."
        )
    else:
        route = (
            "Route this request through /flow-plan before implementation. Do not proceed with "
            "behavior-changing edits until a frozen docs/flow/{feature_name}/plan.md exists."
        )

    return (
        f"[Agent Flow Safety Gate] Detected '{trigger}' ({category}). {route} "
        "Use /flow-start only for new-feature discovery or greenfield scope shaping. "
        "If the work changes an existing runtime path, bug, regression, refactor, auth/schema/status/order/search/mail/PDF/job flow, "
        "the canonical entry point is /flow-plan. The plan must resolve ambiguity, run residual-risk preflight, "
        "and include business-flow, regression-surface, test-design, and integration-coverage sections when behavior changes."
    )


def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Skip short prompts
        if len(prompt) < 10:
            sys.exit(0)

        needs_flow_plan, flow_category, flow_trigger = detect_flow_plan_requirement(prompt)
        agent, trigger, is_multimodal = detect_agent(prompt)

        if is_multimodal:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Multimodal File Detected] Found '{trigger}' in prompt. "
                        "**MUST** use Gemini CLI to process this file. "
                        "Pass the file to Gemini with specific extraction instructions: "
                        f'`gemini -p "Extract: {{what to extract}}" < {trigger} 2>/dev/null` '
                        "Do NOT attempt to read this file directly — use Gemini for content extraction."
                    )
                }
            }
            print(json.dumps(output))

        elif needs_flow_plan:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": flow_plan_message(flow_category, flow_trigger, prompt),
                }
            }
            print(json.dumps(output, ensure_ascii=False))

        elif agent == "codex":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Agent Routing] Detected '{trigger}' — this task may benefit from "
                        "Codex CLI for planning, design, or complex implementation. Consider: "
                        "`codex exec --model gpt-5.5-codex --sandbox read-only --full-auto "
                        '"{task description}"` for design decisions, planning, debugging, '
                        "or complex analysis."
                    )
                }
            }
            print(json.dumps(output))

        elif agent == "opus-research":
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        f"[Opus Research] Detected '{trigger}' — use a general-purpose subagent (Opus) "
                        "for this task. Opus subagents handle research, codebase analysis, and investigation "
                        "with 1M context and WebSearch/WebFetch. "
                        "Use via general-purpose subagent: "
                        "Agent tool with subagent_type='general-purpose'. "
                        "Save results to .claude/docs/research/."
                    )
                }
            }
            print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

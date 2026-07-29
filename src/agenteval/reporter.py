"""Generate human-readable evaluation reports."""

from __future__ import annotations

import json
from typing import Any

from agenteval.scorer import ScoreResult


def _bar(value: float, width: int = 30) -> str:
    """Render a simple ASCII progress bar."""
    filled = int(value / 100 * width)
    return "#" * filled + "-" * (width - filled)


def _grade(value: float) -> str:
    if value >= 90:
        return "Excellent"
    if value >= 75:
        return "Good"
    if value >= 60:
        return "Fair"
    if value >= 40:
        return "Needs Improvement"
    return "Poor"


def format_text_report(
    file_path: str,
    conversation: dict[str, Any],
    scores: ScoreResult,
) -> str:
    """Return a formatted plain-text evaluation report."""
    meta = conversation.get("metadata", {})
    lines: list[str] = []

    lines.append("=" * 72)
    lines.append("  AgentEval - Conversation Evaluation Report")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"  File:          {file_path}")
    lines.append(f"  Conversation:  {meta.get('conversation_id', 'N/A')}")
    lines.append(f"  Language:      {meta.get('language', 'N/A')}")
    lines.append(f"  Scenario:      {meta.get('scenario', 'N/A')}")
    lines.append(f"  Domain:        {meta.get('domain', 'N/A')}")

    n_turns = len(conversation.get("turns", []))
    lines.append(f"  Turns:         {n_turns}")
    lines.append("")
    lines.append("-" * 72)
    lines.append("  Scores (0-100)")
    lines.append("-" * 72)
    lines.append("")

    score_dict = scores.to_dict()
    for label, value in score_dict.items():
        if label == "overall_score":
            continue
        display = label.replace("_", " ").title()
        lines.append(f"  {display:<25s} {value:6.2f}  {_bar(value)}  {_grade(value)}")

    lines.append("")
    lines.append("-" * 72)
    overall = score_dict["overall_score"]
    lines.append(f"  {'Overall Score':<25s} {overall:6.2f}  {_bar(overall)}  {_grade(overall)}")
    lines.append("-" * 72)
    lines.append("")
    lines.append("  NOTE: These scores are produced by deterministic heuristic")
    lines.append("  analysis. They capture surface-level patterns and are NOT a")
    lines.append("  substitute for human evaluation or model-based (LLM-as-judge)")
    lines.append("  scoring. Use as a fast, reproducible baseline only.")
    lines.append("")
    lines.append("=" * 72)

    return "\n".join(lines)


def format_json_report(
    file_path: str,
    conversation: dict[str, Any],
    scores: ScoreResult,
) -> str:
    """Return a JSON-formatted evaluation report."""
    meta = conversation.get("metadata", {})
    report: dict[str, Any] = {
        "file": file_path,
        "metadata": {
            "conversation_id": meta.get("conversation_id"),
            "language": meta.get("language"),
            "scenario": meta.get("scenario"),
            "domain": meta.get("domain"),
            "turns": len(conversation.get("turns", [])),
        },
        "scores": scores.to_dict(),
        "overall_grade": _grade(scores.overall_score),
        "disclaimer": (
            "Scores are produced by deterministic heuristic analysis. "
            "They are not a substitute for human or model-based evaluation."
        ),
    }
    return json.dumps(report, indent=2, ensure_ascii=False)

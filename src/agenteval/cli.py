"""Command-line interface for AgentEval."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from agenteval import __version__
from agenteval.reporter import format_json_report, format_text_report
from agenteval.scorer import score_conversation
from agenteval.validator import validate_conversation


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agenteval",
        description=(
            "Provider-neutral multilingual evaluation toolkit for conversational AI agents."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"agenteval {__version__}",
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- validate ---
    p_val = sub.add_parser("validate", help="Validate conversation JSON files")
    p_val.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Path(s) to conversation JSON file(s)",
    )

    # --- score ---
    p_score = sub.add_parser("score", help="Score conversation JSON files")
    p_score.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Path(s) to conversation JSON file(s)",
    )
    p_score.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    # --- report ---
    p_report = sub.add_parser("report", help="Generate full evaluation reports")
    p_report.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Path(s) to conversation JSON file(s)",
    )
    p_report.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    return parser


def _cmd_validate(files: Sequence[Path]) -> int:
    """Run validation and print results. Returns exit code."""
    all_valid = True
    for fpath in files:
        result = validate_conversation(fpath)
        if result.valid:
            print(f"[PASS] {result.file_path}: valid")
        else:
            all_valid = False
            print(f"[FAIL] {result.file_path}: {result.error_count} error(s)")
            for err in result.errors:
                print(f"    [{err.path}] {err.message}")
    return 0 if all_valid else 1


def _cmd_score(files: Sequence[Path], fmt: str) -> int:
    """Score conversations and print results."""
    for fpath in files:
        result = validate_conversation(fpath)
        if not result.valid:
            print(f"[FAIL] {result.file_path}: validation failed, cannot score", file=sys.stderr)
            for err in result.errors:
                print(f"    [{err.path}] {err.message}", file=sys.stderr)
            return 1

        assert result.conversation is not None
        scores = score_conversation(result.conversation)

        if fmt == "json":
            import json

            print(json.dumps(scores.to_dict(), indent=2))
        else:
            print(f"\n  Scores for: {fpath}")
            print("  " + "-" * 50)
            for label, value in scores.to_dict().items():
                display = label.replace("_", " ").title()
                print(f"  {display:<25s} {value:6.2f}")
            print()
    return 0


def _cmd_report(files: Sequence[Path], fmt: str) -> int:
    """Generate full reports."""
    for fpath in files:
        result = validate_conversation(fpath)
        if not result.valid:
            print(f"[FAIL] {result.file_path}: validation failed, cannot report", file=sys.stderr)
            for err in result.errors:
                print(f"    [{err.path}] {err.message}", file=sys.stderr)
            return 1

        assert result.conversation is not None
        scores = score_conversation(result.conversation)

        if fmt == "json":
            print(format_json_report(str(fpath), result.conversation, scores))
        else:
            print(format_text_report(str(fpath), result.conversation, scores))
    return 0


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point for the CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "validate":
        sys.exit(_cmd_validate(args.files))
    elif args.command == "score":
        sys.exit(_cmd_score(args.files, args.format))
    elif args.command == "report":
        sys.exit(_cmd_report(args.files, args.format))
    else:
        parser.print_help()
        sys.exit(1)

"""Tests for the reporting engine."""

from __future__ import annotations

import json
from typing import Any

from agenteval.reporter import format_json_report, format_text_report
from agenteval.scorer import score_conversation


class TestTextReport:
    def test_contains_header(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_text_report("test.json", valid_conversation, scores)
        assert "AgentEval" in report
        assert "Evaluation Report" in report

    def test_contains_scores(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_text_report("test.json", valid_conversation, scores)
        assert "Language Accuracy" in report
        assert "Safety" in report
        assert "Overall Score" in report

    def test_contains_disclaimer(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_text_report("test.json", valid_conversation, scores)
        assert "deterministic" in report.lower()
        assert "not" in report.lower() and "substitute" in report.lower()

    def test_contains_metadata(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_text_report("test.json", valid_conversation, scores)
        assert "test-001" in report
        assert "en" in report


class TestJsonReport:
    def test_valid_json(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_json_report("test.json", valid_conversation, scores)
        data = json.loads(report)
        assert isinstance(data, dict)

    def test_contains_scores(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_json_report("test.json", valid_conversation, scores)
        data = json.loads(report)
        assert "scores" in data
        assert len(data["scores"]) == 9

    def test_contains_grade(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_json_report("test.json", valid_conversation, scores)
        data = json.loads(report)
        assert "overall_grade" in data

    def test_contains_disclaimer(self, valid_conversation: dict[str, Any]) -> None:
        scores = score_conversation(valid_conversation)
        report = format_json_report("test.json", valid_conversation, scores)
        data = json.loads(report)
        assert "disclaimer" in data
        assert "deterministic" in data["disclaimer"].lower()

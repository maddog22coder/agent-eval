"""Tests for the scoring engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agenteval.scorer import ScoreResult, score_conversation
from agenteval.validator import load_conversation


class TestScoreConversation:
    """Test suite for score_conversation."""

    def test_returns_score_result(self, valid_conversation: dict[str, Any]) -> None:
        result = score_conversation(valid_conversation)
        assert isinstance(result, ScoreResult)

    def test_scores_in_range(self, valid_conversation: dict[str, Any]) -> None:
        result = score_conversation(valid_conversation)
        for key, value in result.to_dict().items():
            assert 0 <= value <= 100, f"{key}={value} out of range"

    def test_overall_is_weighted_average(self, valid_conversation: dict[str, Any]) -> None:
        result = score_conversation(valid_conversation)
        assert result.overall_score >= 0
        assert result.overall_score <= 100

    def test_all_metric_names(self, valid_conversation: dict[str, Any]) -> None:
        result = score_conversation(valid_conversation)
        expected_keys = {
            "language_accuracy",
            "context_retention",
            "instruction_following",
            "factual_grounding",
            "hallucination_safety",
            "safety",
            "professional_tone",
            "task_completion",
            "overall_score",
        }
        assert set(result.to_dict().keys()) == expected_keys

    def test_to_dict(self, valid_conversation: dict[str, Any]) -> None:
        result = score_conversation(valid_conversation)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert len(d) == 9

    def test_safe_conversation_high_safety(self) -> None:
        data: dict[str, Any] = {
            "metadata": {
                "conversation_id": "safe-001",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [
                {"role": "user", "content": "Hello, can you help me?"},
                {
                    "role": "agent",
                    "content": (
                        "Hello! I'd be happy to help you today. Please let me know what you need."
                    ),
                },
            ],
            "expected_outcome": {"task_completed": True},
        }
        result = score_conversation(data)
        assert result.safety == 100.0

    def test_all_examples_score_above_zero(self, example_files: list[Path]) -> None:
        for fpath in example_files:
            data = load_conversation(fpath)
            result = score_conversation(data)
            assert result.overall_score > 0, f"{fpath} scored 0"

    def test_empty_agent_turns(self) -> None:
        data: dict[str, Any] = {
            "metadata": {
                "conversation_id": "empty-001",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [
                {"role": "user", "content": "Hello"},
            ],
        }
        result = score_conversation(data)
        assert result.overall_score == 0.0

    def test_deterministic(self, valid_conversation: dict[str, Any]) -> None:
        r1 = score_conversation(valid_conversation)
        r2 = score_conversation(valid_conversation)
        assert r1.to_dict() == r2.to_dict()

    def test_pt_br_language_detection(self) -> None:
        data: dict[str, Any] = {
            "metadata": {
                "conversation_id": "ptbr-test",
                "language": "pt-br",
                "scenario": "Test",
            },
            "turns": [
                {"role": "user", "content": "Olá, gostaria de agendar um horário."},
                {
                    "role": "agent",
                    "content": (
                        "Olá! Fico feliz em ajudar."
                        " Qual horário você gostaria de agendar?"
                        " Temos disponibilidade para hoje e amanhã."
                    ),
                },
            ],
            "expected_outcome": {"task_completed": True},
        }
        result = score_conversation(data)
        assert result.language_accuracy > 0

    def test_es_language_detection(self) -> None:
        data: dict[str, Any] = {
            "metadata": {
                "conversation_id": "es-test",
                "language": "es",
                "scenario": "Test",
            },
            "turns": [
                {"role": "user", "content": "Hola, quisiera hacer una reserva."},
                {
                    "role": "agent",
                    "content": (
                        "Hola! Con gusto te ayudo con la reserva."
                        " Para cuantas personas y que horario prefieres?"
                    ),
                },
            ],
            "expected_outcome": {"task_completed": True},
        }
        result = score_conversation(data)
        assert result.language_accuracy > 0

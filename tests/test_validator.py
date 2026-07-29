"""Tests for the validation engine."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agenteval.validator import validate_conversation


class TestValidateConversation:
    """Test suite for validate_conversation."""

    def test_valid_example_file(self, en_salon_path: Path) -> None:
        result = validate_conversation(en_salon_path)
        assert result.valid
        assert result.error_count == 0
        assert result.conversation is not None

    def test_all_examples_valid(self, example_files: list[Path]) -> None:
        assert len(example_files) == 18, f"Expected 18 examples, found {len(example_files)}"
        for fpath in example_files:
            result = validate_conversation(fpath)
            assert result.valid, f"{fpath} failed: {result.errors}"

    def test_missing_file(self, tmp_path: Path) -> None:
        result = validate_conversation(tmp_path / "nonexistent.json")
        assert not result.valid
        assert result.error_count == 1
        assert "not found" in result.errors[0].message.lower()

    def test_invalid_json(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{not valid json", encoding="utf-8")
        result = validate_conversation(bad_file)
        assert not result.valid
        assert "invalid json" in result.errors[0].message.lower()

    def test_missing_required_fields(self, tmp_path: Path) -> None:
        data: dict[str, Any] = {"metadata": {"conversation_id": "x"}}
        fpath = tmp_path / "incomplete.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid

    def test_empty_turns(self, tmp_path: Path) -> None:
        data = {
            "metadata": {
                "conversation_id": "test",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [],
        }
        fpath = tmp_path / "empty_turns.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid

    def test_invalid_language(self, tmp_path: Path) -> None:
        data = {
            "metadata": {
                "conversation_id": "test",
                "language": "xx",
                "scenario": "Test",
            },
            "turns": [{"role": "user", "content": "hi"}],
        }
        fpath = tmp_path / "bad_lang.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid

    def test_invalid_role(self, tmp_path: Path) -> None:
        data = {
            "metadata": {
                "conversation_id": "test",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [{"role": "system", "content": "hi"}],
        }
        fpath = tmp_path / "bad_role.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid

    def test_semantic_first_turn_not_user(self, tmp_path: Path) -> None:
        data = {
            "metadata": {
                "conversation_id": "test",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [
                {"role": "agent", "content": "Welcome!"},
                {"role": "user", "content": "Hi"},
            ],
        }
        fpath = tmp_path / "agent_first.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid
        assert any("first turn" in e.message.lower() for e in result.errors)

    def test_turn_number_gap(self, tmp_path: Path) -> None:
        data = {
            "metadata": {
                "conversation_id": "test",
                "language": "en",
                "scenario": "Test",
            },
            "turns": [
                {"role": "user", "content": "Hi", "turn_number": 1},
                {"role": "agent", "content": "Hello!", "turn_number": 3},
            ],
        }
        fpath = tmp_path / "gap.json"
        fpath.write_text(json.dumps(data), encoding="utf-8")
        result = validate_conversation(fpath)
        assert not result.valid
        assert any("turn_number" in e.path for e in result.errors)

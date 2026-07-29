"""Shared test fixtures for AgentEval."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


@pytest.fixture()
def valid_conversation() -> dict[str, Any]:
    """Minimal valid conversation dict."""
    return {
        "metadata": {
            "conversation_id": "test-001",
            "language": "en",
            "scenario": "Test Scenario",
        },
        "turns": [
            {"role": "user", "content": "Hello, I need help.", "turn_number": 1},
            {
                "role": "agent",
                "content": "Hello! I'd be happy to help you. How can I assist you today?",
                "turn_number": 2,
            },
        ],
        "expected_outcome": {"task_completed": True, "summary": "Basic greeting."},
    }


@pytest.fixture()
def example_files() -> list[Path]:
    """Return all example JSON files."""
    return sorted(EXAMPLES_DIR.rglob("*.json"))


@pytest.fixture()
def en_salon_path() -> Path:
    """Path to the English salon example."""
    return EXAMPLES_DIR / "en" / "salon-appointment.json"

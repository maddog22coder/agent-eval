"""Tests for the CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
EN_SALON = EXAMPLES_DIR / "en" / "salon-appointment.json"


class TestCLI:
    def test_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "agenteval" in result.stdout.lower()

    def test_version(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "0.1.0" in result.stdout

    def test_validate_valid_file(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "validate", str(EN_SALON)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "pass" in result.stdout.lower() or "valid" in result.stdout.lower()

    def test_validate_missing_file(self, tmp_path: Path) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "validate", str(tmp_path / "nope.json")],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_score_valid_file(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "score", str(EN_SALON)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "overall" in result.stdout.lower()

    def test_score_json_format(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "score", "--format", "json", str(EN_SALON)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        import json

        data = json.loads(result.stdout)
        assert "overall_score" in data

    def test_report_valid_file(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "report", str(EN_SALON)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "AgentEval" in result.stdout

    def test_report_json_format(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval", "report", "--format", "json", str(EN_SALON)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        import json

        data = json.loads(result.stdout)
        assert "scores" in data
        assert "disclaimer" in data

    def test_no_command_shows_help(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "agenteval"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "agenteval" in result.stdout.lower()

"""Validate conversation JSON files against the AgentEval schema."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema

from agenteval.schemas import get_conversation_schema


@dataclass(frozen=True)
class ValidationError:
    """A single validation issue."""

    path: str
    message: str


@dataclass
class ValidationResult:
    """Outcome of validating one conversation file."""

    file_path: str
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    conversation: dict[str, Any] | None = None

    @property
    def error_count(self) -> int:
        return len(self.errors)


def load_conversation(path: Path) -> dict[str, Any]:
    """Load and return a conversation dict from a JSON file.

    Raises ``FileNotFoundError`` or ``json.JSONDecodeError`` on failure.
    """
    with path.open(encoding="utf-8") as fh:
        result: dict[str, Any] = json.load(fh)
    return result


def validate_conversation(path: Path) -> ValidationResult:
    """Validate a conversation file against the schema and semantic rules."""
    str_path = str(path)

    # --- file-level checks ---
    try:
        data = load_conversation(path)
    except FileNotFoundError:
        return ValidationResult(
            file_path=str_path,
            valid=False,
            errors=[ValidationError(path="(file)", message=f"File not found: {path}")],
        )
    except json.JSONDecodeError as exc:
        return ValidationResult(
            file_path=str_path,
            valid=False,
            errors=[ValidationError(path="(file)", message=f"Invalid JSON: {exc}")],
        )

    # --- JSON Schema validation ---
    schema = get_conversation_schema()
    errors: list[ValidationError] = []

    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        json_path = ".".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(ValidationError(path=json_path, message=err.message))

    # --- semantic checks ---
    errors.extend(_semantic_checks(data))

    return ValidationResult(
        file_path=str_path,
        valid=len(errors) == 0,
        errors=errors,
        conversation=data if len(errors) == 0 else None,
    )


def _semantic_checks(data: dict[str, Any]) -> list[ValidationError]:
    """Run additional semantic validations beyond JSON Schema."""
    errors: list[ValidationError] = []

    turns: list[dict[str, Any]] = data.get("turns", [])
    if not turns:
        return errors

    # First turn should be from the user
    if turns[0].get("role") != "user":
        errors.append(
            ValidationError(
                path="turns.0.role",
                message="First turn should have role 'user'.",
            )
        )

    # Check turn_number sequencing if present
    prev_num = 0
    for i, turn in enumerate(turns):
        tn = turn.get("turn_number")
        if tn is not None:
            if tn != prev_num + 1:
                errors.append(
                    ValidationError(
                        path=f"turns.{i}.turn_number",
                        message=f"Expected turn_number {prev_num + 1}, got {tn}.",
                    )
                )
            prev_num = tn

    # Non-empty content is enforced by schema, but double-check
    for i, turn in enumerate(turns):
        content = turn.get("content", "")
        if isinstance(content, str) and content.strip() == "":
            errors.append(
                ValidationError(
                    path=f"turns.{i}.content",
                    message="Turn content must not be blank.",
                )
            )

    return errors

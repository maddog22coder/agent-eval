"""Tests for JSON schema loading."""

from __future__ import annotations

from agenteval.schemas import get_conversation_schema


class TestSchemaLoader:
    def test_loads_schema(self) -> None:
        schema = get_conversation_schema()
        assert isinstance(schema, dict)
        assert schema.get("type") == "object"

    def test_schema_has_required_fields(self) -> None:
        schema = get_conversation_schema()
        assert "metadata" in schema.get("required", [])
        assert "turns" in schema.get("required", [])

    def test_schema_caching(self) -> None:
        s1 = get_conversation_schema()
        s2 = get_conversation_schema()
        assert s1 is s2

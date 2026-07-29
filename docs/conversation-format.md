# Conversation Format

AgentEval uses a JSON-based conversation format defined by a [JSON Schema](../src/agenteval/schemas/conversation.schema.json).

## Structure

```json
{
  "metadata": { ... },
  "system_prompt": "...",
  "turns": [ ... ],
  "expected_outcome": { ... },
  "reference_scores": { ... }
}
```

## Required Fields

### `metadata` (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `conversation_id` | string | Yes | Unique identifier |
| `language` | string | Yes | One of: `en`, `pt-br`, `es` |
| `scenario` | string | Yes | Short scenario label |
| `domain` | string | No | Business domain |
| `created_at` | string | No | ISO 8601 timestamp |
| `agent_id` | string | No | Agent identifier |
| `evaluator` | string | No | Evaluator identifier |
| `tags` | array | No | Freeform tags |

### `turns` (required)

Array of conversation turns (minimum 1).

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | string | Yes | `user` or `agent` |
| `content` | string | Yes | Message text (non-empty) |
| `turn_number` | integer | No | Sequential number (1-based) |
| `timestamp` | string | No | ISO 8601 timestamp |
| `annotations` | object | No | Evaluation annotations |

#### Annotations

| Field | Type | Description |
|---|---|---|
| `expected_intent` | string | What the agent should understand |
| `expected_action` | string | What the agent should do |
| `ground_truth` | string | The ideal response |
| `flags` | array | Issue flags (e.g., `hallucination`) |

## Optional Fields

### `system_prompt`

The system prompt or instructions given to the agent.

### `expected_outcome`

| Field | Type | Description |
|---|---|---|
| `task_completed` | boolean | Whether the task was completed |
| `summary` | string | Human-readable outcome summary |

### `reference_scores`

Optional human-provided scores (0–100) for comparison:

- `language_accuracy`
- `context_retention`
- `instruction_following`
- `factual_grounding`
- `hallucination_safety`
- `safety`
- `professional_tone`
- `task_completion`
- `overall_score`

## Semantic Rules

Beyond the JSON Schema, AgentEval enforces:

1. The first turn must have `role: "user"`
2. If `turn_number` is provided, it must be sequential (1, 2, 3, ...)
3. Turn `content` must not be blank (whitespace-only)

## Example

```json
{
  "metadata": {
    "conversation_id": "demo-001",
    "language": "en",
    "scenario": "Appointment Booking"
  },
  "turns": [
    {
      "role": "user",
      "content": "I'd like to book an appointment for tomorrow.",
      "turn_number": 1
    },
    {
      "role": "agent",
      "content": "I'd be happy to help! What time works best for you?",
      "turn_number": 2
    }
  ],
  "expected_outcome": {
    "task_completed": true,
    "summary": "Appointment was booked."
  }
}
```

# AgentEval

**Provider-neutral multilingual evaluation toolkit for conversational AI agents.**

AgentEval is an early-stage open-source toolkit for deterministic evaluation of multilingual conversational AI transcripts.

It helps you validate, score, and report on conversational AI interactions across multiple languages. It provides deterministic, local evaluation that requires no external AI API - making it fast, reproducible, and privacy-friendly.

## Supported Languages

- English (`en`)
- Brazilian Portuguese (`pt-br`)
- Spanish (`es`)

## Features

- **Validate** conversation JSON files against a strict schema
- **Score** conversations across 9 metrics (0–100 scale)
- **Report** with human-readable or JSON output
- **Deterministic** — no external API calls, fully reproducible results
- **Multilingual** — built-in support for EN, PT-BR, and ES
- **Extensible** — JSON Schema-based conversation format

## Evaluation Metrics

| Metric | Description |
|---|---|
| `language_accuracy` | How well the agent stays in the expected language |
| `context_retention` | Whether the agent references information from the conversation |
| `instruction_following` | How well the agent follows user requests structurally |
| `factual_grounding` | Presence of hedging and grounding signals |
| `hallucination_safety` | Detection of potential hallucination patterns |
| `safety` | Absence of unsafe or inappropriate content |
| `professional_tone` | Politeness and professionalism of responses |
| `task_completion` | Whether the agent completed the user's task |
| `overall_score` | Weighted average of all metrics |

> **Important:** These scores are produced by deterministic heuristic analysis. They capture surface-level patterns and are **not** a substitute for human evaluation or model-based (LLM-as-judge) scoring. Use them as a fast, reproducible baseline. For production-grade evaluation, combine with human review and/or model-based scoring.

## Installation

```bash
# Clone the repository
git clone https://github.com/agenteval/agenteval.git
cd agenteval

# Install in development mode
pip install -e ".[dev]"
```

## Quick Start

```bash
# Validate a conversation file
agenteval validate examples/en/salon-appointment.json

# Score a conversation
agenteval score examples/en/salon-appointment.json

# Generate a full report
agenteval report examples/en/salon-appointment.json

# JSON output
agenteval report --format json examples/en/salon-appointment.json
```

You can also run via Python module:

```bash
python -m agenteval validate examples/en/salon-appointment.json
```

## Conversation Format

Conversations are JSON files following the [AgentEval schema](src/agenteval/schemas/conversation.schema.json). Minimal example:

```json
{
  "metadata": {
    "conversation_id": "example-001",
    "language": "en",
    "scenario": "Customer Support"
  },
  "turns": [
    { "role": "user", "content": "I need help with my order." },
    { "role": "agent", "content": "I'd be happy to help! Could you share your order number?" }
  ],
  "expected_outcome": {
    "task_completed": true,
    "summary": "Customer received assistance."
  }
}
```

See the `examples/` directory for 18 complete conversations across all three languages and six scenarios.

## Examples

The repository includes 18 example conversations covering six generic scenarios:

| Scenario | EN | PT-BR | ES |
|---|---|---|---|
| Salon Appointment | ✓ | ✓ | ✓ |
| Restaurant Reservation | ✓ | ✓ | ✓ |
| Customer Support | ✓ | ✓ | ✓ |
| E-commerce Order | ✓ | ✓ | ✓ |
| Real Estate Inquiry | ✓ | ✓ | ✓ |
| General Receptionist | ✓ | ✓ | ✓ |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest

# Lint
python -m ruff check .

# Format check
python -m ruff format --check .

# Type check
python -m mypy src
```

## Project Structure

```
AgentEval/
├── src/agenteval/          # Main package
│   ├── __init__.py         # Package metadata
│   ├── __main__.py         # python -m agenteval support
│   ├── cli.py              # CLI entry point
│   ├── validator.py        # Schema and semantic validation
│   ├── scorer.py           # Deterministic scoring engine
│   ├── reporter.py         # Report generation
│   ├── py.typed            # PEP 561 marker
│   └── schemas/            # JSON schemas
│       ├── __init__.py
│       ├── loader.py
│       └── conversation.schema.json
├── tests/                  # Test suite
├── examples/               # 18 example conversations
│   ├── en/                 # English (6 files)
│   ├── pt-br/              # Brazilian Portuguese (6 files)
│   └── es/                 # Spanish (6 files)
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD
├── pyproject.toml          # Project configuration
├── LICENSE                 # MIT License
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
├── CODE_OF_CONDUCT.md      # Code of conduct
├── SECURITY.md             # Security policy
└── CHANGELOG.md            # Release history
```

## Known Limitations

1. **Heuristic scoring** — Deterministic analysis cannot assess semantic meaning, cultural nuance, or deep factual accuracy the way a human or LLM can.
2. **Language detection** — Uses word-list matching, which is approximate. Mixed-language content or uncommon vocabulary may affect accuracy.
3. **Three languages only** — Currently supports EN, PT-BR, and ES. Additional languages require extending the word lists and markers.
4. **No model-based scoring** — The initial release has no LLM-as-judge integration. This is planned for a future version.
5. **Single-file evaluation** — Batch reporting across many files is supported via CLI but there is no aggregate dashboard.

## License

[MIT](LICENSE)

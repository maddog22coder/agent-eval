# Contributing to AgentEval

Thank you for considering contributing to AgentEval! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Install development dependencies: `pip install -e ".[dev]"`

## Development Workflow

### Running Tests

```bash
python -m pytest
```

### Linting and Formatting

```bash
# Check linting
python -m ruff check .

# Auto-fix linting issues
python -m ruff check --fix .

# Check formatting
python -m ruff format --check .

# Auto-format
python -m ruff format .
```

### Type Checking

```bash
python -m mypy src
```

### Running All Checks

Before submitting a pull request, make sure all checks pass:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy src
```

## Pull Request Process

1. Ensure all tests pass and linting is clean
2. Update documentation if you're adding or changing features
3. Add tests for new functionality
4. Keep pull requests focused — one feature or fix per PR
5. Write clear commit messages describing what and why

## Adding a New Language

To add support for a new language:

1. Add the language code to the `language` enum in `src/agenteval/schemas/conversation.schema.json`
2. Add word lists for the language in `src/agenteval/scorer.py` (`_SUPPORTED_LANGUAGES`)
3. Add professional markers and hedging phrases for the language
4. Create 6 example conversations in `examples/<lang-code>/`
5. Update tests and documentation

## Adding a New Metric

To add a new evaluation metric:

1. Add the scoring function in `src/agenteval/scorer.py`
2. Add the field to `ScoreResult`
3. Include it in the `overall_score` weighted average
4. Add the field to the JSON schema's `reference_scores`
5. Update documentation and tests

## Code Style

- Follow existing patterns in the codebase
- Use type annotations everywhere
- Keep functions focused and well-named
- Avoid unnecessary comments — code should be self-documenting

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include reproduction steps for bugs
- Include expected vs actual behavior
- Mention your Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

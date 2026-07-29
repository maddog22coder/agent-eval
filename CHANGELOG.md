# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-15

### Added

- Initial release of AgentEval
- CLI with `validate`, `score`, and `report` commands
- JSON Schema-based conversation validation
- Deterministic scoring engine with 9 metrics:
  - language_accuracy
  - context_retention
  - instruction_following
  - factual_grounding
  - hallucination_safety
  - safety
  - professional_tone
  - task_completion
  - overall_score
- Human-readable and JSON report formats
- Support for English, Brazilian Portuguese, and Spanish
- 18 example conversations across 6 scenarios
- Comprehensive test suite
- GitHub Actions CI pipeline
- Full project documentation

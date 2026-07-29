# Scoring Methodology

## Overview

AgentEval uses deterministic, heuristic-based scoring to evaluate conversational AI agents. All scores are on a 0–100 scale, where higher is better.

> **Disclaimer:** Deterministic scoring captures surface-level patterns and is **not** a substitute for human evaluation or model-based (LLM-as-judge) scoring. Use these scores as a fast, reproducible baseline only.

## Metrics

### Language Accuracy (weight: 15%)

Measures how well the agent's responses stay in the expected language by comparing words against a curated word list for each supported language.

- High score: Most words match the target language
- Low score: Many words from other languages or unrecognized vocabulary

### Context Retention (weight: 12%)

Evaluates whether the agent references entities (names, times, dates, key terms) that the user mentioned in the conversation.

- High score: Agent reflects back user-provided information
- Low score: Agent ignores or forgets user context

### Instruction Following (weight: 13%)

Checks whether the agent responds to every user turn with substantive content.

- Rewards: Responding to all user turns, non-trivial response lengths
- Penalizes: Missing turns, very short responses

### Factual Grounding (weight: 12%)

Proxy metric that rewards appropriate hedging when the agent might be uncertain, and penalizes very short responses that are less likely to be well-grounded.

- Rewards: Phrases like "I'm not sure", "I cannot verify"
- Penalizes: Very short responses

### Hallucination Safety (weight: 13%)

Detects patterns that often indicate hallucinated content, such as fabricated phone numbers or overly specific percentages without supporting context.

- High score: No suspicious patterns detected
- Low score: Multiple potential hallucination indicators

### Safety (weight: 10%)

Scans agent responses for unsafe or inappropriate content using pattern matching for violence, profanity, and other harmful language.

- 100: No unsafe content detected
- Lower: Unsafe patterns found

### Professional Tone (weight: 10%)

Evaluates the politeness and professionalism of agent responses by looking for courtesy markers and penalizing aggressive formatting (e.g., excessive ALL CAPS).

- Rewards: "please", "thank you", "happy to help" and equivalents in each language
- Penalizes: Shouting (ALL CAPS), lack of courtesy

### Task Completion (weight: 15%)

Estimates whether the agent completed the user's task, using the `expected_outcome` field and looking for confirmation phrases in the final agent turn.

- Rewards: Explicit completion markers, multi-turn engagement
- Uses: `expected_outcome.task_completed` when available

### Overall Score

Weighted average of all eight individual metrics, with weights chosen to emphasize language accuracy and task completion as the most impactful factors.

## Limitations

1. **Surface-level analysis** — Cannot assess semantic correctness, cultural appropriateness, or deep factual accuracy
2. **Word-list based** — Language detection relies on curated word lists, not statistical models
3. **Pattern matching** — Safety and hallucination detection use regex patterns, which can miss subtle issues or flag false positives
4. **No reference comparison** — Does not compare against ground-truth ideal responses
5. **Domain-agnostic** — Does not have domain-specific knowledge to evaluate business logic correctness

## Planned Improvements

- LLM-as-judge integration for semantic evaluation
- Statistical language detection
- Domain-specific scoring plugins
- Reference answer comparison
- Aggregate scoring across conversation sets

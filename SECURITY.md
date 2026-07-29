# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✓         |

## Reporting a Vulnerability

If you discover a security vulnerability in AgentEval, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Send a description of the vulnerability via GitHub's private vulnerability reporting feature
3. Include steps to reproduce the issue if possible
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Considerations

AgentEval is designed to run locally and does not:

- Make any external network calls
- Require any API keys or credentials
- Access or transmit user data to external services
- Execute arbitrary code from conversation files

### Input Handling

- Conversation files are parsed as JSON only — no code execution
- JSON Schema validation is applied before processing
- File paths are resolved locally; no remote file access

### Data Privacy

- All evaluation is performed locally on your machine
- No telemetry or usage data is collected
- Conversation files remain on your local filesystem
- No data is sent to any external service

## Best Practices

When using AgentEval with real conversation data:

1. Do not commit real customer conversations to version control
2. Anonymize any personally identifiable information (PII) before evaluation
3. Store conversation files with appropriate filesystem permissions
4. Review conversation files for sensitive data before sharing

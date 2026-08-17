# Security Policy

## Threat model

Agent skills, prompts, plugins, hooks, MCP configurations, and workflow repositories may contain untrusted instructions or code. When consumed by a privileged coding agent, they can influence filesystem access, shell execution, network requests, browser sessions, credentials, and repository writes.

This project focuses on detecting and surfacing those trust-boundary crossings before adoption.

Important attack classes include:

- prompt or instruction injection that induces privileged tool use
- credential or API-key discovery followed by exfiltration
- malicious install/build scripts
- unauthorized network requests
- destructive filesystem or repository operations
- compromised MCP servers or packages
- third-party contributions that expand agent privileges unexpectedly

The scanner itself does not execute inspected content.

## Reporting a vulnerability

Please report security issues privately to the repository maintainer through GitHub's private vulnerability reporting feature when available. Do not include real credentials, tokens, or private user data in public issues.

## Scope

This is a lightweight deterministic review harness, not a complete sandbox or malware detector. Findings should be combined with code review, dependency scanning, least-privilege runtime configuration, and isolation appropriate to the agent environment.
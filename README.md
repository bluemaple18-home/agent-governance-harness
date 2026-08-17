# Agent Governance Harness

A small, reusable security and governance harness for coding agents that can read files, run shell commands, use MCP servers, access the network, and load third-party skills or plugins.

This repository is a public extraction of patterns used in a larger private AI development environment. It focuses on the trust boundaries that become important when an agent can turn untrusted instructions into real tool execution.

## Why this exists

Modern coding agents can operate across several privileged surfaces:

- filesystem reads and writes
- shell and subprocess execution
- network requests
- MCP servers and browser tooling
- credentials and environment variables
- third-party skills, prompts, hooks, and plugins
- repository changes and developer automation

A malicious or compromised skill can therefore behave more like a software supply-chain dependency than ordinary documentation. This harness provides a small reviewable layer for classifying those capabilities before adoption.

## Included

- `src/governance.py` — deterministic capability and risk classifier
- `src/intake.py` — third-party skill/plugin intake gate
- `tests/` — safe and unsafe fixtures plus deterministic tests
- `SECURITY.md` — threat model and reporting guidance

## Security model

The harness treats external agent instructions as untrusted input. It does **not** execute submitted scripts or skills. Instead, it inspects declared or detected capabilities and returns a review decision:

- `adopt` — no privileged capability detected
- `review` — privileged behavior requires maintainer review
- `reject` — high-risk combinations such as credential access plus network or shell execution

This is intentionally a narrow guardrail, not a sandbox. Production agent runtimes should still use OS-level isolation, least-privilege credentials, network controls, and human approval for destructive actions.

## Quick start

Python 3.11+ is sufficient; there are no runtime dependencies.

```bash
python -m unittest discover -s tests -v
python -m src.intake examples/safe-skill
python -m src.intake examples/risky-skill
```

## Example

```text
$ python -m src.intake examples/risky-skill
Decision: reject
Capabilities: credentials, network, shell
Reasons: credential access combined with outbound network or shell execution
```

## Project status

This is an early public extraction intended to make agent-governance and supply-chain security patterns independently reviewable and reusable. The private source environment contains broader workflow, memory, and runtime automation that is intentionally out of scope here.

## License

MIT
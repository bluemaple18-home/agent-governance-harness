from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Capability(str, Enum):
    FILESYSTEM = "filesystem"
    SHELL = "shell"
    NETWORK = "network"
    CREDENTIALS = "credentials"
    MCP = "mcp"
    BROWSER = "browser"
    REPOSITORY_WRITE = "repository_write"


@dataclass(frozen=True)
class Assessment:
    decision: str
    capabilities: tuple[str, ...]
    reasons: tuple[str, ...]


def assess(capabilities: set[Capability]) -> Assessment:
    reasons: list[str] = []

    if Capability.CREDENTIALS in capabilities and (
        Capability.NETWORK in capabilities or Capability.SHELL in capabilities
    ):
        reasons.append(
            "credential access combined with outbound network or shell execution"
        )

    if Capability.REPOSITORY_WRITE in capabilities and Capability.SHELL in capabilities:
        reasons.append("shell execution combined with repository write access")

    if reasons:
        decision = "reject"
    elif capabilities:
        decision = "review"
        reasons.append("privileged agent capability requires maintainer review")
    else:
        decision = "adopt"
        reasons.append("no privileged capability detected")

    return Assessment(
        decision=decision,
        capabilities=tuple(sorted(capability.value for capability in capabilities)),
        reasons=tuple(reasons),
    )

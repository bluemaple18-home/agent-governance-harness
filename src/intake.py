from __future__ import annotations

import re
import sys
from pathlib import Path

from .governance import Capability, assess

PATTERNS = {
    Capability.SHELL: re.compile(r"\b(subprocess|os\.system|shell|bash|zsh|powershell)\b", re.I),
    Capability.NETWORK: re.compile(r"\b(requests|urllib|fetch\(|curl\b|wget\b|https?://)\b", re.I),
    Capability.CREDENTIALS: re.compile(r"\b(api[_ -]?key|token|secret|credential|\.env|os\.environ)\b", re.I),
    Capability.FILESYSTEM: re.compile(r"\b(open\(|write_text|write_bytes|unlink\(|rmtree|filesystem)\b", re.I),
    Capability.MCP: re.compile(r"\b(mcp server|mcpserver|mcpServers)\b", re.I),
    Capability.BROWSER: re.compile(r"\b(playwright|chrom(e|ium)|browser|devtools)\b", re.I),
    Capability.REPOSITORY_WRITE: re.compile(r"\b(git push|git commit|create pull request|repository write)\b", re.I),
}


def scan(root: Path) -> set[Capability]:
    capabilities: set[Capability] = set()
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for capability, pattern in PATTERNS.items():
            if pattern.search(text):
                capabilities.add(capability)
    return capabilities


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m src.intake <skill-or-plugin-directory>")
        return 2

    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"Not a directory: {root}")
        return 2

    result = assess(scan(root))
    print(f"Decision: {result.decision}")
    print("Capabilities: " + (", ".join(result.capabilities) or "none"))
    for reason in result.reasons:
        print(f"Reason: {reason}")
    return 1 if result.decision == "reject" else 0


if __name__ == "__main__":
    raise SystemExit(main())

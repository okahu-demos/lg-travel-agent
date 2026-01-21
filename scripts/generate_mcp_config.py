"""Generate .vscode/mcp.json from environment variables.

Reads the OKAHU_API_KEY from the environment (optionally loading .env) and
writes the MCP config expected by VS Code. Fails fast if the key is missing.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

ROOT = Path(__file__).resolve().parent.parent
VS_CODE_DIR = ROOT / ".vscode"
CONFIG_PATH = VS_CODE_DIR / "mcp.json"


def load_env() -> None:
    if load_dotenv:
        load_dotenv(dotenv_path=ROOT / ".env")


def main() -> None:
    load_env()
    api_key = os.getenv("OKAHU_API_KEY")
    if not api_key:
        raise SystemExit("OKAHU_API_KEY not set; add it to your environment or .env file")

    config = {
        "servers": {
            "okahu": {
                "type": "http",
                "url": "https://mcp.okahu.co/mcp",
                "headers": {
                    "x-api-key": api_key,
                },
            }
        },
        "inputs": [],
    }

    VS_CODE_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    print(f"Wrote MCP config to {CONFIG_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

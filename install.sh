#!/usr/bin/env bash
set -euo pipefail

python3 -c 'import sys; sys.exit("Kowtow MCP requires Python 3.10+ because the official mcp package declares >=3.10." if sys.version_info < (3, 10) else 0)'
python3 -m pip install --upgrade pip
python3 -m pip install .

echo "Kowtow MCP installed. Run: kowtow-mcp"

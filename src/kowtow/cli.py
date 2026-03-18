from __future__ import annotations

import argparse
import sys

from kowtow.mcp_server import app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kowtow-mcp",
        description=(
            "Start the Kowtow MCP server.\n\n"
            "Default (stdio) is meant for MCP hosts such as Claude Desktop, VS Code Copilot,\n"
            "Cherry Studio, etc.  For manual local testing use --transport streamable-http,\n"
            "or run:  uv run mcp dev src/kowtow/mcp_server.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default="stdio",
        help="Transport to use (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default=app.settings.host,
        help="Bind host for HTTP transports (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=app.settings.port,
        help="Bind port for HTTP transports (default: 8000).",
    )
    parser.add_argument(
        "--mount-path",
        default=None,
        help="Optional mount path for SSE transport.",
    )
    return parser


def serve(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    app.settings.host = args.host
    app.settings.port = args.port

    if args.transport == "stdio" and sys.stdin.isatty() and sys.stdout.isatty():
        print(
            "kowtow-mcp: running in stdio mode, waiting for an MCP host.\n"
            "For manual testing: kowtow-mcp --transport streamable-http\n"
            "Or use the Inspector: uv run mcp dev src/kowtow/mcp_server.py",
            file=sys.stderr,
            flush=True,
        )

    app.run(transport=args.transport, mount_path=args.mount_path)


if __name__ == "__main__":
    serve()

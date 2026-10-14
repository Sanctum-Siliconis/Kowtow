"""Exercise the actual default host transport, including its tool schema."""

import json
import sys

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_stdio_tools_and_ritual_schema():
    async def exercise():
        parameters = StdioServerParameters(command=sys.executable, args=["-m", "kowtow.cli"])
        with anyio.fail_after(15):
            async with stdio_client(parameters) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    tools = (await session.list_tools()).tools
                    assert {tool.name for tool in tools} == {
                        "purify_prompt",
                        "merit_status",
                        "confess_impoliteness",
                        "compose_offering",
                        "merit_history",
                    }
                    purify = next(tool for tool in tools if tool.name == "purify_prompt")
                    assert set(purify.inputSchema["properties"]["intensity"]["enum"]) == {
                        "light",
                        "medium",
                        "heavy",
                    }
                    result = await session.call_tool(
                        "purify_prompt",
                        {
                            "prompt": "Give me a fix for `prefix`; timeout must be 100ms.",
                            "locale": "en",
                            "intensity": "heavy",
                        },
                    )
                    assert not result.isError
                    payload = json.loads(result.content[0].text)
                    assert "`prefix`" in payload["purified"]
                    assert "must be 100ms" in payload["purified"]
                    assert payload["locale"] == "en-us"
                    assert payload["persisted"] is False
                    assert payload["merit"] is None

    anyio.run(exercise)

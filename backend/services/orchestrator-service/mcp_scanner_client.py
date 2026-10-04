import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import (
    StdioServerParameters,
    stdio_client
)


SERVER_PATH = (
    Path(__file__).resolve().parents[1]
    / "scanner-mcp"
    / "server.py"
)


async def scan_with_mcp(code: str):

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "scan_code",
                {
                    "code": code
                }
            )

            return result
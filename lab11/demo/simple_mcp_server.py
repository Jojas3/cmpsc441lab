"""
Simple MCP Server Demo
This demonstrates how to create an MCP server using the official Python SDK.
The server exposes a simple tool that returns the current time.
"""

import asyncio
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create the MCP server instance
server = Server("demo-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools.
    This is called when a client sends a tools/list request.
    """
    return [
        Tool(
            name="get_current_time",
            description="Returns the current date and time",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Optional timezone (default: local)",
                        "default": "local"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="add_numbers",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls.
    This is called when a client sends a tools/call request.
    """
    if name == "get_current_time":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [TextContent(type="text", text=f"Current time: {current_time}")]

    elif name == "add_numbers":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(type="text", text=f"{a} + {b} = {result}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server using stdio transport."""
    import sys
    # Use stderr for logging since stdout is used for JSON-RPC protocol
    print("Starting demo MCP server...", file=sys.stderr, flush=True)
    print("This server exposes 'get_current_time' and 'add_numbers' tools.", file=sys.stderr, flush=True)
    print("Use simple_mcp_client.py to connect to this server.", file=sys.stderr, flush=True)

    # Run the server using stdio transport
    # This allows communication via stdin/stdout
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

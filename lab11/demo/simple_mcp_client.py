"""
Simple MCP Client Demo
This demonstrates how to connect to an MCP server and call its tools.
Also shows what the MCP protocol messages look like.
"""

import asyncio
import json
import sys
from pathlib import Path

# MCP imports - correct API
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def print_message(direction: str, method: str, content: dict):
    """Print a formatted MCP protocol message."""
    print()
    print("=" * 70)
    print(f"  {direction}  |  {method}")
    print("=" * 70)
    print(json.dumps(content, indent=2))
    print()


async def main():
    """Connect to the demo MCP server and demonstrate tool usage."""

    # Path to the demo server
    server_script = Path(__file__).parent / "simple_mcp_server.py"

    print("=" * 70)
    print("                    MCP Protocol Demo")
    print("=" * 70)
    print(f"\nConnecting to server: {server_script.name}")
    print("\nThis demo shows the actual MCP protocol messages that flow")
    print("between client and server using JSON-RPC format.\n")

    # Configure the server parameters
    server_params = StdioServerParameters(
        command=sys.executable,  # Python interpreter
        args=[str(server_script)]
    )

    # Connect to the server using stdio transport
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Create the client session
        async with ClientSession(read_stream, write_stream) as session:

            # =========================================================
            # STEP 1: Initialize the connection
            # =========================================================
            print("\n" + "#" * 70)
            print("# STEP 1: Initialize Connection")
            print("#" * 70)

            print_message(
                "CLIENT -> SERVER",
                "initialize (request)",
                {
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "clientInfo": {"name": "demo-client", "version": "1.0.0"}
                    }
                }
            )

            await session.initialize()

            print_message(
                "SERVER -> CLIENT",
                "initialize (response)",
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "demo-server", "version": "1.0.0"},
                        "capabilities": {"tools": {"listChanged": True}}
                    }
                }
            )

            print("[OK] Connection initialized!")

            # =========================================================
            # STEP 2: List available tools
            # =========================================================
            print("\n" + "#" * 70)
            print("# STEP 2: List Available Tools")
            print("#" * 70)

            print_message(
                "CLIENT -> SERVER",
                "tools/list (request)",
                {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {}
                }
            )

            tools_result = await session.list_tools()

            # Build the actual response content
            tools_list = []
            for tool in tools_result.tools:
                tools_list.append({
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                })

            print_message(
                "SERVER -> CLIENT",
                "tools/list (response)",
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": tools_list
                    }
                }
            )

            print(f"[OK] Found {len(tools_result.tools)} tools!")

            # =========================================================
            # STEP 3: Call a tool - get_current_time
            # =========================================================
            print("\n" + "#" * 70)
            print("# STEP 3: Call Tool - get_current_time")
            print("#" * 70)

            print_message(
                "CLIENT -> SERVER",
                "tools/call (request)",
                {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "get_current_time",
                        "arguments": {}
                    }
                }
            )

            result = await session.call_tool("get_current_time", {})

            print_message(
                "SERVER -> CLIENT",
                "tools/call (response)",
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": result.content[0].text}]
                    }
                }
            )

            print(f"[OK] Tool result: {result.content[0].text}")

            # =========================================================
            # STEP 4: Call a tool with arguments - add_numbers
            # =========================================================
            print("\n" + "#" * 70)
            print("# STEP 4: Call Tool with Arguments - add_numbers(5, 3)")
            print("#" * 70)

            print_message(
                "CLIENT -> SERVER",
                "tools/call (request)",
                {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "add_numbers",
                        "arguments": {"a": 5, "b": 3}
                    }
                }
            )

            result = await session.call_tool("add_numbers", {"a": 5, "b": 3})

            print_message(
                "SERVER -> CLIENT",
                "tools/call (response)",
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{"type": "text", "text": result.content[0].text}]
                    }
                }
            )

            print(f"[OK] Tool result: {result.content[0].text}")

            # =========================================================
            # Summary
            # =========================================================
            print("\n" + "#" * 70)
            print("# DEMO COMPLETE")
            print("#" * 70)
            print("""
Key Takeaways:
1. MCP uses JSON-RPC 2.0 format for all messages
2. Client sends 'initialize' first to establish the connection
3. 'tools/list' returns all available tools with their schemas
4. 'tools/call' executes a tool with the given arguments
5. All communication happens over stdio (stdin/stdout)
""")


if __name__ == "__main__":
    asyncio.run(main())

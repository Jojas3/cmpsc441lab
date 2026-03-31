"""
Lab 11: MCP + LangGraph Integration
=====================================
YOUR TASK: Connect your MCP server to a LangGraph ReAct agent for LLM-powered tool calling.

This script should:
1. Connect to your MCP server (mcp_server.py)
2. Load MCP tools as LangChain-compatible tools using load_mcp_tools()
3. Create a LangGraph ReAct agent with Ollama as the LLM
4. Send user queries through the agent, which handles tool calling automatically
5. Return the final response

Contrast this with Lab 05's manual approach - LangGraph handles the tool-calling
loop for you!
"""

import asyncio
import sys
from pathlib import Path

# MCP imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain MCP adapter - converts MCP tools to LangChain-compatible tools
from langchain_mcp_adapters.tools import load_mcp_tools

# LangGraph - prebuilt ReAct agent that handles the tool-calling loop
from langgraph.prebuilt import create_react_agent

# Ollama LLM via LangChain
from langchain_ollama import ChatOllama


# Configuration
MCP_SERVER_SCRIPT = Path(__file__).parent / "mcp_server.py"
OLLAMA_MODEL = "llama3.2:latest"
SYSTEM_PROMPT = (
    "You are a helpful DnD assistant. "
    "Use the available tools to help players with dice rolls, character stats, and damage calculations."
)


async def chat_with_tools(user_message: str, agent) -> str:
    """
    Send a message to the LangGraph agent and return the final response.

    TODO: Invoke the agent with the user message and extract the final answer.

    Hint: The agent accepts a dict with a "messages" key containing a list of
    (role, content) tuples:
        result = await agent.ainvoke({"messages": [("human", user_message)]})

    The result is also a dict with a "messages" key. The last message is the
    agent's final response - return its .content attribute.
    """
    # TODO: Invoke the LangGraph agent and return the final response
    # result = await agent.ainvoke({"messages": [("human", user_message)]})
    # return result["messages"][-1].content
    return "Not implemented yet"


async def main():
    """Main function to run the MCP + LangGraph integration."""

    print("=" * 60)
    print("Lab 11: MCP + LangGraph Integration")
    print("=" * 60)

    if not MCP_SERVER_SCRIPT.exists():
        print(f"\nError: MCP server not found at {MCP_SERVER_SCRIPT}")
        print("Make sure you've created mcp_server.py")
        return

    print(f"\nConnecting to MCP server: {MCP_SERVER_SCRIPT.name}")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_SCRIPT)]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("[OK] Connected to MCP server!")

            # TODO: Load MCP tools as LangChain-compatible tools
            # Use load_mcp_tools(session) - it returns a list of BaseTool objects
            # that LangGraph can use directly (no manual format conversion needed!)
            tools = []  # Replace with: tools = await load_mcp_tools(session)

            print(f"\nFound {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")

            if not tools:
                print("\nNo tools found! Make sure you've implemented list_tools() in mcp_server.py")
                return

            # Create the Ollama LLM
            llm = ChatOllama(model=OLLAMA_MODEL)

            # TODO: Create a LangGraph ReAct agent
            # Pass the llm, tools, and SYSTEM_PROMPT (as state_modifier) to create_react_agent.
            # The agent will automatically handle the tool-calling loop - no manual loop needed!
            # agent = create_react_agent(llm, tools, state_modifier=SYSTEM_PROMPT)
            agent = None  # Replace this line with the agent creation above

            # Interactive chat loop
            print("\n" + "-" * 60)
            print("Chat with the DnD assistant (type 'quit' to exit)")
            print("Try: 'Roll a d20 for an attack' or 'What is the fighter's strength?'")
            print("-" * 60 + "\n")

            while True:
                try:
                    user_input = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                response = await chat_with_tools(user_input, agent)
                print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())

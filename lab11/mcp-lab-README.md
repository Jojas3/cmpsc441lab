# Lab 11: Model Context Protocol (MCP)

## Introduction

The **Model Context Protocol (MCP)** is an open standard developed by Anthropic for connecting AI systems to external tools and data sources. Think of it as a "USB port" for AI - a standardized way for language models to interact with the outside world.

In Lab 05, you implemented tool calling using a custom approach specific to Ollama. While this works, every AI system has its own way of handling tools, making it difficult to reuse tools across different systems. MCP solves this by providing a universal protocol that works the same way regardless of which AI system you're using.

## What is MCP?

MCP uses a **client-server architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Host (Your App)                      │
│                   Contains MCP Client(s)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                    JSON-RPC over stdio
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  MCP Server   │   │  MCP Server   │   │  MCP Server   │
│  (Tools A)    │   │  (Tools B)    │   │  (Tools C)    │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Key Components:**
- **MCP Host**: Your application that contains the LLM (like your DnD agent)
- **MCP Client**: Manages the connection to MCP servers
- **MCP Server**: Exposes capabilities (tools, resources, prompts) to the client
- **Transport**: How messages are sent (see below)

**Transport Types:**

MCP supports two transport modes:

1. **stdio (standard I/O)** - The client spawns the server as a child process and communicates over stdin/stdout pipes. You only need to run a single command - the client starts the server automatically. This is the standard approach for local tools, and what we use in this lab. This is also how tools like Claude Desktop and Claude Code connect to MCP servers.

2. **HTTP + SSE (Server-Sent Events)** - The server runs independently on its own port (e.g. `python server.py` starts it on `http://localhost:8080`). The client connects to it over the network. The server stays running even after the client disconnects. This is used for shared/remote tools, multi-user scenarios, or when the server is on another machine.

**Three Primitives:**
1. **Tools** (model-controlled): Functions the LLM can call (like `roll_dice`)
2. **Resources** (app-controlled): Data/context the application provides
3. **Prompts** (user-controlled): Templates for structured interactions

## Learning Objectives

By completing this lab, you will:
1. Understand MCP's client-server architecture
2. Build an MCP server using the official Python SDK
3. See what MCP protocol messages look like (JSON-RPC format)
4. Compare MCP to the ad-hoc tool calling from Lab 05
5. Integrate MCP tools with a LangGraph ReAct agent for LLM inference
6. Prepare for using MCP in your final project

## Prerequisites

- Completed Lab 05 (Tool Use)
- Ollama installed with `llama3.2:latest` model
- Python 3.10+

> **Why LangGraph?** Lab 05 had you manually format tools, run a chat loop, and append tool results back into the message history. LangChain's `create_agent` handles all of that for you — you just give it an LLM and a list of tools.

## Setup

Install the required dependencies (delete the uv.lock file before running if the environment setup is stale):

```
uv sync
```

Ensure Ollama is running:

```bash
ollama serve
```

## Lab Structure

```
lab11/
├── mcp-lab-README.md              # This file
├── lab11.py                       # YOUR MAIN FILE - integrate MCP with Ollama
├── mcp_server.py                  # YOUR FILE - implement MCP server with DnD tools
├── demo/
│   ├── simple_mcp_server.py       # Reference: complete MCP server example
│   └── simple_mcp_client.py       # Reference: client that shows protocol messages
└── requirements.txt               # Dependencies
```

## Lab Tasks

### Task 1: Explore the Demo (20 points)

First, understand how MCP works by running the provided demo.

**Run the demo client:**
```bash
python demo/simple_mcp_client.py
```

The demo will show you the actual MCP protocol messages that flow between client and server. You'll see:
- `initialize` - Connection handshake
- `tools/list` - Listing available tools
- `tools/call` - Executing a tool

**Questions to answer in your reflection:**
- What method is called first when a client connects to a server?
- What information does `tools/list` return?
- What is the structure of a `tools/call` request?

### Task 2: Implement the DnD MCP Server (40 points)

Complete `mcp_server.py` to create an MCP server with three DnD-related tools.

**Implement the three standalone functions:**

1. **`roll_dice(n_dice: int, sides: int, modifier: int = 0) -> str`**
   - Rolls the specified dice and returns a result string
   - Example: `roll_dice(2, 6, 3)` → `"Rolled 2d6+3: [4, 2] + 3 = 9"`

2. **`get_character_stat(character: str, stat: str) -> str`**
   - Returns a stat value for a character from the `CHARACTERS` dictionary
   - Stats: strength, dexterity, constitution, intelligence, wisdom, charisma
   - Handle invalid character/stat names gracefully

3. **`calculate_damage(base_damage: int, armor_class: int, attack_roll: int) -> str`**
   - Returns a message describing damage dealt (base_damage if attack_roll >= armor_class, else 0)

**Test your server:**
```bash
python mcp_server.py
```

Then run the demo client against your server to verify your tools appear correctly.

### Task 3: Integrate with LangGraph (30 points)

Complete `lab11.py` to:

1. Connect to your MCP server
2. Load MCP tools as LangChain tools using `load_mcp_tools(session)`
3. Create a `ChatOllama` LLM instance
4. Build a LangChain based agent with `create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)`
5. Invoke the agent with user messages and return the final response

The `load_mcp_tools` adapter handles tool format conversion automatically — no need to write `format_tools_for_ollama()` by hand. The ReAct (Reasoning and Acting) agent handles the tool-calling loop — no need to manually append tool results to the message history.

**Test your integration:**
```bash
python lab11.py
```

Try queries like:
- "Roll a d20 for an attack"
- "What is the fighter's strength?"
- "Calculate damage: base 8, AC 15, attack roll 17"

### Task 4: Reflection (10 points)

Create a file `lab11_reflection.md` answering:

1. Compare the MCP + LangGraph approach to Lab 05's manual tool calling. What work does LangGraph remove? What are the advantages of using a standardized protocol like MCP?

2. Describe one specific way MCP could enhance your final DnD Dungeon Master project. Be specific about which tools you would create.

3. Copy the output from the demo client showing the protocol messages.

## Grading Rubric

| Task | Points | Criteria |
|------|--------|----------|
| Task 1 | 20 | Demo explored, questions answered in reflection |
| Task 2 | 40 | MCP server implements all 3 tools correctly |
| Task 3 | 30 | Ollama integration works, tool calls execute through MCP |
| Task 4 | 10 | Thoughtful reflection with demo output |

## References

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Anthropic MCP Course](https://www.anthropic.com/news/model-context-protocol)
- [LangGraph ReAct Agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)
- [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters)

## Tips

- The MCP Python SDK handles most of the protocol complexity for you
- Use `@server.list_tools()` and `@server.call_tool()` decorators to expose functions
- The demo client output shows exactly what the messages look like - use this for debugging
- Compare your protocol messages to the demo to ensure correctness

- What method is called first when a client connects to a server?
initialize

- What information does `tools/list` return?
A list of available tools, each with name, description, and inputSchema.

- What is the structure of a `tools/call` request?
A JSON-RPC 2.0 request with method "tools/call" and params containing "name" (string) and "arguments" (object).


1. Compare the MCP + LangGraph approach to Lab 05's manual tool calling. What work does LangGraph remove? What are the advantages of using a standardized protocol like MCP?

LangGraph removes the manual work of formatting tools for the specific LLM (like Ollama's custom format), running the chat loop, and appending tool call results back into the message history. It provides a ReAct agent that handles the tool-calling loop automatically, making integration much simpler.

The advantages of MCP include its standardized protocol that works across different AI systems, allowing tools to be reused without custom adaptations. It's like a universal "USB port" for AI, enabling better interoperability and reducing development effort for multi-system deployments.

2. Describe one specific way MCP could enhance your final DnD Dungeon Master project. Be specific about which tools you would create.

MCP could enhance the DnD Dungeon Master project by providing a standardized set of tools for game mechanics, allowing the AI DM to interact with game state in a consistent way. I would create tools such as:
- roll_dice: For rolling various dice (d20 for attacks, d6 for damage, etc.)
- get_character_stat: To look up character abilities and stats
- calculate_damage: To determine combat outcomes
- Additional tools like generate_encounter (to create random encounters), lookup_spell (for spell details), and manage_inventory (to track player items).

3. Copy the output from the demo client showing the protocol messages.
======================================================================
                    MCP Protocol Demo
======================================================================

Connecting to server: simple_mcp_server.py

This demo shows the actual MCP protocol messages that flow
between client and server using JSON-RPC format.


######################################################################
# STEP 1: Initialize Connection
######################################################################

======================================================================
  CLIENT -> SERVER  |  initialize (request)
======================================================================
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "demo-client",
      "version": "1.0.0"
    }
  }
}


======================================================================
  SERVER -> CLIENT  |  initialize (response)
======================================================================
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "serverInfo": {
      "name": "demo-server",
      "version": "1.0.0"
    },
    "capabilities": {
      "tools": {
        "listChanged": true
      }
    }
  }
}

[OK] Connection initialized!

######################################################################
# STEP 2: List Available Tools
######################################################################

======================================================================
  CLIENT -> SERVER  |  tools/list (request)
======================================================================
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {}
}


======================================================================
  SERVER -> CLIENT  |  tools/list (response)
======================================================================
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "get_current_time",
        "description": "Returns the current date and time",
        "inputSchema": {
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
      },
      {
        "name": "add_numbers",
        "description": "Adds two numbers together",
        "inputSchema": {
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
          "required": [
            "a",
            "b"
          ]
        }
      }
    ]
  }
}

[OK] Found 2 tools!

######################################################################
# STEP 3: Call Tool - get_current_time
######################################################################

======================================================================
  CLIENT -> SERVER  |  tools/call (request)
======================================================================
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_current_time",
    "arguments": {}
  }
}


======================================================================
  SERVER -> CLIENT  |  tools/call (response)
======================================================================
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current time: 2026-04-02 19:39:41"
      }
    ]
  }
}

[OK] Tool result: Current time: 2026-04-02 19:39:41

######################################################################
# STEP 4: Call Tool with Arguments - add_numbers(5, 3)
######################################################################

======================================================================
  CLIENT -> SERVER  |  tools/call (request)
======================================================================
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add_numbers",
    "arguments": {
      "a": 5,
      "b": 3
    }
  }
}


======================================================================
  SERVER -> CLIENT  |  tools/call (response)
======================================================================
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "5 + 3 = 8"
      }
    ]
  }
}

[OK] Tool result: 5 + 3 = 8

######################################################################
# DEMO COMPLETE
######################################################################

Key Takeaways:
1. MCP uses JSON-RPC 2.0 format for all messages
2. Client sends 'initialize' first to establish the connection
3. 'tools/list' returns all available tools with their schemas
4. 'tools/call' executes a tool with the given arguments
5. All communication happens over stdio (stdin/stdout)

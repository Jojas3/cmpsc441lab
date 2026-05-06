"""
Enhanced LLM utilities with tool calling support
"""
import json
import ollama
import logging
from pathlib import Path
from typing import Dict, Any, List, Callable


class ToolCallingAgent:
    """Agent that can use tools via Ollama"""
    
    def __init__(self, template_file: str, tools: List[Dict] = None, tool_functions: Dict[str, Callable] = None):
        """
        Initialize agent with template and tools
        
        Args:
            template_file: Path to JSON template
            tools: List of tool definitions
            tool_functions: Dict mapping tool names to functions
        """
        with open(Path(template_file), 'r') as f:
            self.template = json.load(f)
        
        self.messages = self.template['messages'].copy()
        self.model = self.template['model']
        self.options = self.template.get('options', {})
        
        self.tools = tools or []
        self.tool_functions = tool_functions or {}
        
        self.conversation_history = []
    
    def chat(self, user_message: str, max_tool_calls: int = 5) -> str:
        """
        Send a message and handle tool calls
        
        Args:
            user_message: User's message
            max_tool_calls: Maximum number of tool calls to allow
        
        Returns:
            Final response text
        """
        # Add user message
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        tool_call_count = 0
        
        while tool_call_count < max_tool_calls:
            # Make API call
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=self.messages,
                    tools=self.tools if self.tools else None,
                    options=self.options
                )
            except Exception as e:
                logging.error(f"[LLM] Error in chat: {e}")
                return f"Error: {e}"
            
            assistant_message = response['message']
            self.messages.append(assistant_message)
            
            # Check if there are tool calls
            if not assistant_message.get('tool_calls'):
                # No more tool calls, return the response
                content = assistant_message.get('content', '')
                
                # Check if content contains malformed tool call JSON
                if content.strip().startswith('{') and '"name"' in content and '"parameters"' in content:
                    logging.warning(f"[LLM] Model returned tool call as text instead of using tool calling API: {content[:100]}")
                    return "I understand your request. Let me help you with that directly."
                
                return content
            
            # Process tool calls
            for tool_call in assistant_message['tool_calls']:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                
                logging.info(f"[TOOL] Calling {tool_name} with args: {tool_args}")
                
                # Execute tool
                if tool_name in self.tool_functions:
                    try:
                        result = self.tool_functions[tool_name](**tool_args)
                        logging.info(f"[TOOL] Result: {result}")
                    except Exception as e:
                        result = {"error": str(e)}
                        logging.error(f"[TOOL] Error executing {tool_name}: {e}")
                else:
                    result = {"error": f"Tool {tool_name} not found"}
                
                # Add tool result to messages
                self.messages.append({
                    "role": "tool",
                    "content": json.dumps(result)
                })
            
            tool_call_count += 1
        
        # If we hit max tool calls, return last message
        return "Maximum tool calls reached. Please try again."
    
    def reset(self):
        """Reset conversation history"""
        self.messages = self.template['messages'].copy()
        self.conversation_history = []


class ChainOfThoughtAgent:
    """Agent that uses chain-of-thought reasoning"""
    
    def __init__(self, template_file: str):
        with open(Path(template_file), 'r') as f:
            self.template = json.load(f)
        
        self.messages = self.template['messages'].copy()
        self.model = self.template['model']
        self.options = self.template.get('options', {})
    
    def think_and_respond(self, user_message: str) -> Dict[str, str]:
        """
        Use chain-of-thought to think through a problem
        
        Returns:
            Dict with 'thinking' and 'response' keys
        """
        # First, ask the model to think
        thinking_prompt = f"{user_message}\n\nFirst, think step-by-step about how to handle this situation. Consider:\n1. What is the player trying to do?\n2. What rules apply?\n3. What rolls are needed?\n4. What would be interesting outcomes?\n\nThinking:"
        
        self.messages.append({
            "role": "user",
            "content": thinking_prompt
        })
        
        try:
            thinking_response = ollama.chat(
                model=self.model,
                messages=self.messages,
                options=self.options
            )
            
            thinking = thinking_response['message']['content']
            self.messages.append(thinking_response['message'])
            
            # Now ask for the actual response
            self.messages.append({
                "role": "user",
                "content": "Now, based on your thinking, provide your response as the Dungeon Master:"
            })
            
            final_response = ollama.chat(
                model=self.model,
                messages=self.messages,
                options=self.options
            )
            
            response = final_response['message']['content']
            self.messages.append(final_response['message'])
            
            return {
                "thinking": thinking,
                "response": response
            }
        except Exception as e:
            logging.error(f"[COT] Error: {e}")
            return {
                "thinking": "",
                "response": f"Error: {e}"
            }


class MultiModalAgent:
    """Agent that combines tool calling, CoT, and multimodal outputs"""
    
    def __init__(self, template_file: str, tools: List[Dict] = None, tool_functions: Dict[str, Callable] = None):
        self.tool_agent = ToolCallingAgent(template_file, tools, tool_functions)
        self.outputs = []  # Store all outputs (text, images, audio)
    
    def process_action(self, user_message: str, enable_cot: bool = False) -> Dict[str, Any]:
        """
        Process user action with full capabilities
        
        Returns:
            Dict with response and any generated media
        """
        response = self.tool_agent.chat(user_message)
        
        result = {
            "text": response,
            "images": [],
            "audio": [],
            "tool_calls": []
        }
        
        # Extract any generated media from tool calls
        for msg in self.tool_agent.messages:
            if msg.get('role') == 'tool':
                try:
                    tool_result = json.loads(msg['content'])
                    
                    # Check for images
                    if 'ascii_art' in tool_result:
                        result['images'].append(tool_result['ascii_art'])
                    
                    # Check for audio
                    if tool_result.get('success') and 'text' in tool_result:
                        result['audio'].append(tool_result['text'])
                    
                    result['tool_calls'].append(tool_result)
                except:
                    pass
        
        return result

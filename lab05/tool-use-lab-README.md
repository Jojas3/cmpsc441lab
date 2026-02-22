# Tool Use Lab

## Intro to Tool Use
Tool use in the context of language models refers to the ability of these models to interact with external tools or APIs to perform specific tasks. This capability allows language models to extend their functionality beyond generating text, enabling them to execute actions, retrieve information, and manipulate data in real-time. Tool use is particularly valuable for applications that require dynamic responses or interactions with external systems, such as chatbots, virtual assistants, and automated workflows.

## Lab Task 1

NOTE: Please don't change my code. Only edit the files that have the name of the lab and in places where the comments ask for it.

Based on the example shown, create an agent that can perform skill check based dice rolls for DnD. The agent should be able to roll a dice and successfully create the next response based on the tool's output.

Ensure that the template provides the tool information to the ollama model like in `demo/tool_template.json`.

Fill out the `process_response` method that will be used in the AgentTemplate._chat_generator() function.

Before submitting the commit link, ensure that the agent is able to make correct tool calls by ensuring that you see something like the following on the console after the player's message.

```
Tools Called:
 defaultdict(<class 'list'>, {'process_function_call_calls': [{'name': 'process_function_call', 'args': (Function(name='roll_for', arguments={'dc': 5, 'player': 'adventurer', 'skill': 'Athletics'}),), 'kwargs': {}, 'result': 'adventurer rolled 7 for Athletics and succeeded!'}]})
```

## Lab Task 2

In `lab05-tool-use.md`, describe (~250 words) an imaginative but realistic use of tool calling with language models. This is worth 30% of the lab grade. Most imaginative use cases are invited, but if you have a hard time coming up with something think of an imaginative addition that you could to your class project with tool use.

### Rubric
- **Creativity (10%)**: The idea is original and goes beyond trivial examples (e.g., not just "get the weather").
- **Feasibility (10%)**: The proposed use case is realistic and could be implemented with current technology.
- **Clarity (10%)**: The description is well-written and clearly explains what tools would be called and why.
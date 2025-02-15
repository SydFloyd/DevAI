"""
Utilities for managing and executing tool-based workflows with OpenAI's API.

This module facilitates automated workflows by dynamically calling tools, processing their outputs, and managing interactions with the OpenAI API in a threaded environment. It includes functions for creating and deleting assistants, executing tools based on a given run configuration, and handling user interactions through a threaded interface.

Functions:
    - get_client() -> OpenAI: Initializes and returns an OpenAI client using the configured API key.
    - delete_assistant(assistant_id): Deletes an assistant using its ID.
    - create_assistant() -> str: Creates a new assistant with specified instructions and tools, returning its ID.
    - execute_tools(run) -> List[Dict]: Executes tools specified in a run configuration and collects their outputs.
    - submit_tools_and_get_run(run, tool_outputs, thread_id) -> Run: Submits tool outputs and retrieves the updated run status.
    - interact(assistant_id, thread_id): Manages user interaction and tool execution within a thread.
    - output_messages(run, thread_id): Displays messages from a completed run.
    - main(): Initializes the assistant, manages the interaction loop, and ensures cleanup of resources.

Exceptions:
    - General exceptions during tool execution and submission are caught and logged for troubleshooting. Specific exceptions include errors in executing tool functions and failures in submitting tool outputs.
"""

from openai import OpenAI
from src.config import cfg
import importlib
import json

def get_client():
	client = OpenAI(
		api_key = cfg.openai_api_key
	)
	return client

def delete_assistant(assistant_id):
	client = get_client()
	client.beta.assistants.delete(assistant_id)
	print(f"Deleted assistant {assistant_id}")

def create_assistant():
	from src.tools_schema import dev_tools

	client = get_client()

	assistant = client.beta.assistants.create(
		instructions=cfg.ASSISTANT_INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)
	print(f"Created assistant {assistant.id}")

	return assistant.id

client = get_client()

def execute_tools(run):
    tool_outputs = []
    if hasattr(run, "required_action"):
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool.function.name
            function_args = tool.function.arguments
            try:
                tools_module = importlib.import_module(f"src.tools.{function_name}")
                tool_function = getattr(tools_module, function_name)
                if isinstance(function_args, str):
                    function_args = json.loads(function_args)  # Convert string to dict
                output = tool_function(**function_args)
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": str(output)  # Convert output to string if necessary
                })
            except Exception as e:
                print(f"Error executing {function_name}: {e}")
    return tool_outputs

def submit_tools_and_get_run(run, tool_outputs, thread_id):
    try:
        return client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    except Exception as e:
        print("Failed to submit tool outputs:", e)
        return run

def interact(assistant_id, thread_id):
    query = input(f"\n{cfg.agent_name}>> ")
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status == 'requires_action':
        tool_outputs = execute_tools(run)
        if tool_outputs:
            run = submit_tools_and_get_run(run, tool_outputs, thread_id)
            print("Tool outputs submitted successfully.")
        else:
            print("No tool outputs to submit.")
            break

    output_messages(run, thread_id)

def output_messages(run, thread_id):
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for message in messages:
            print(message.role + ":")
            for c in message.content:
                print(c.text.value)
            break
    else:
        print(run.status)

def main():
    assistant_id = create_assistant()
    thread = client.beta.threads.create()
    try:
        while True:
            interact(assistant_id, thread.id)
    finally:
        delete_assistant(assistant_id)

if __name__ == "__main__":
    main()




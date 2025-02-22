"""
Manage AI assistant workflows using OpenAI's API.

This module facilitates the creation, management, and interaction with AI assistants via OpenAI's API. It supports tool-based workflows and user interactions through a threaded interface, enabling efficient handling of concurrent interactions and real-time responses.

Functions:
    - get_client() -> OpenAI: Initializes and returns a new OpenAI client using the configured API key.
    - delete_assistant(assistant_id: str): Deletes an assistant using its ID.
    - create_assistant() -> str: Creates a new assistant with specified instructions, tools, and model "gpt-4o", returning its ID.
    - execute_tools(run) -> List[Dict]: Executes tools specified in a run configuration and collects their outputs.
    - submit_tools_and_get_run(run, tool_outputs: List[Dict], thread_id: str) -> Run: Submits tool outputs and retrieves the updated run status.
    - interact(assistant_id: str, thread_id: str): Manages user interaction and tool execution within a thread.
    - output_messages(run, thread_id: str): Prints the role and content of messages from a thread if the run is completed; otherwise, prints the current run status.
    - main(): Initializes the assistant, creates a thread, runs an infinite loop for interaction, and ensures cleanup of resources.

Exceptions:
    - General exceptions during tool execution and submission are caught and logged for troubleshooting. Users should be aware of potential issues related to API connectivity and tool execution errors.
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
    request = cfg.get_sys_message() + query
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=request,
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
    print(thread)
    try:
        while True:
            interact(assistant_id, thread.id)
    finally:
        delete_assistant(assistant_id)

if __name__ == "__main__":
    main()


"""
Facilitates the creation and management of AI assistants using OpenAI's API.

This module provides functionalities to create, manage, and interact with AI assistants through OpenAI's API, supporting tool-based workflows and user interactions. It dynamically executes tools and processes their outputs, enabling efficient handling of concurrent interactions and real-time responses.

Functions:
    - get_client() -> OpenAI: Initializes and returns a new OpenAI client using the configured API key.
    - delete_assistant(client: OpenAI, assistant_id: str) -> None: Deletes an assistant by its ID and prints a confirmation message.
    - create_assistant(client: OpenAI) -> str: Creates a new assistant with specified instructions, tools, and model "gpt-4o", returning its ID.
    - execute_tools(client: OpenAI, run) -> List[Dict]: Executes tools specified in a run configuration and collects their outputs.
    - submit_tools_and_get_run(client: OpenAI, run, tool_outputs: List[Dict], thread_id: str) -> Run: Submits tool outputs and retrieves the updated run status.
    - interact(client: OpenAI, assistant_id: str, thread_id: str) -> None: Manages user interaction and tool execution within a thread.
    - output_messages(client: OpenAI, run, thread_id: str) -> None: Prints the role and content of messages from a thread if the run is completed; otherwise, prints the current run status.
    - main() -> None: Initializes the assistant, creates a thread, runs an infinite loop for interaction, and ensures cleanup of resources.

Exceptions:
    - General exceptions during tool execution and submission are caught and logged for troubleshooting, highlighting potential issues related to API connectivity and tool execution errors.
"""

from src.config import cfg
from src.utils.openai_utils import execute_tools, submit_tools_and_get_run, get_client, create_assistant, delete_assistant, get_thread_messages

def interact(client, assistant_id, thread_id):
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
        tool_outputs = execute_tools(client, run)
        if tool_outputs:
            run = submit_tools_and_get_run(client, run, tool_outputs, thread_id)
            print("Tool outputs submitted successfully.")
        else:
            print("No tool outputs to submit.")
            break

    output_messages(client, run, thread_id)

def output_messages(client, run, thread_id):
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
    client = get_client()
    assistant_id = create_assistant(client)
    thread = client.beta.threads.create()
    try:
        while True:
            print(get_thread_messages(client, thread))
            interact(client, assistant_id, thread.id)
    finally:
        delete_assistant(client, assistant_id)

if __name__ == "__main__":
    main()





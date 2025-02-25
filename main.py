"""
Module for facilitating interactions with AI assistants using OpenAI's API.

This module provides a comprehensive framework for creating, managing, and interacting with AI assistants, leveraging OpenAI's API to execute dynamic tools and handle user interactions. It supports concurrent interactions and real-time responses, making it suitable for complex workflows.

Functions:
    - get_client() -> OpenAI: Initializes and returns a new OpenAI client using the configured API key.
    - delete_assistant(client: OpenAI, assistant_id: str) -> None: Deletes an assistant by its ID and prints a confirmation message.
    - create_assistant(client: OpenAI) -> str: Creates a new assistant with specified instructions and returns its ID.
    - execute_tools(client: OpenAI, run) -> List[Dict]: Executes tools specified in a run configuration and collects their outputs.
    - submit_tools_and_get_run(client: OpenAI, run, tool_outputs: List[Dict], thread_id: str) -> Run: Submits tool outputs and retrieves the updated run status.
    - interact(client: OpenAI, assistant_id: str, thread_id: str) -> bool: Manages user interaction and tool execution within a thread, using `cfg.get_sys_message()` to construct requests.
    - output_messages(client: OpenAI, run, thread_id: str) -> None: Prints the role and content of the first message from a thread if the run is completed; otherwise, prints the current run status.
    - get_thread_messages(client: OpenAI, thread) -> List[Dict]: Retrieves and returns messages from a specified thread.
    - main() -> None: Initializes the assistant, creates a thread using `client.beta.threads.create()`, runs an interaction loop, and ensures cleanup of resources.

Exceptions:
    - ConnectionError: Raised when there are issues connecting to the OpenAI API.
    - ToolExecutionError: Raised when a tool fails to execute properly.
    - InvalidAssistantError: Raised when an invalid assistant ID is provided.
"""

from src.doc.auto_document import update_documentation
from src.doc.auto_docstring import DocstringUpdater
from src.config import cfg
from src.utils.openai_utils import (
    execute_tools, 
    submit_tools_and_get_run, 
    get_client, 
    create_assistant, 
    delete_assistant, 
    provide_assistant_files,
    delete_vector_store,
    get_thread_messages
)

def interact(client, assistant_id, thread_id):
    query = input(f"\n{cfg.agent_name}>> ")

    # check for exit
    if query.strip().lower() in cfg.exit_commands:
        return True

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

    return False

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
    # first update codebase docs
    updater = DocstringUpdater()
    updater.update_docstrings_in_directory(cfg.project_root)

    # update docs
    docs_path = update_documentation(cfg.project_root)

    client = get_client()

    assistant_id = create_assistant(client)
    assistant_id, vector_store = provide_assistant_files(client, assistant_id, docs_path)

    thread = client.beta.threads.create()
    try:
        while True:
            # print(get_thread_messages(client, thread))
            quit = interact(client, assistant_id, thread.id)
            if quit:
                break
    finally:
        delete_assistant(client, assistant_id)
        delete_vector_store(client, vector_store)
        print("Session ended.\n")

if __name__ == "__main__":
    main()

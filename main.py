"""This module facilitates interaction with an AI assistant, allowing users to submit queries, receive responses, and update documentation automatically. Key components include:

- `interact`: Manages the interaction loop with the AI assistant, sending user queries and handling tool execution if required.
- `output_messages`: Outputs the messages from the AI assistant based on the current run status.
- `main`: Initializes the client and assistant, manages the session lifecycle, and optionally updates code documentation using `DocstringUpdater`.

Notable dependencies:
- `update_documentation` from `src.doc.auto_document` for regenerating documentation.
- `DocstringUpdater` from `src.doc.auto_docstring` for updating docstrings within the project.
- Various utilities from `src.utils.openai_utils` for assistant and client management, including `execute_tools`, `submit_tools_and_get_run`, and others.

The script relies on a configuration module `src.config` to access setup parameters such as `agent_name`, `exit_commands`, and `project_root`. It provides a command-line interface for user interaction and documentation maintenance."""

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
    update_docs = input("Regenerate documentation? (y/n)")
    if update_docs.lower().strip() == "y":
        # update codebase docs
        updater = DocstringUpdater()
        updater.update_docstrings_in_directory(cfg.project_root)

        # update docs
        docs_path = update_documentation(cfg.project_root)

    client = get_client()

    assistant_id = create_assistant(client)
    assistant_id, vector_store = provide_assistant_files(client, assistant_id, ["docs.md"])

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

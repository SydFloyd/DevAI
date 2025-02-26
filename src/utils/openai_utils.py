"""This module provides functionality to interact with the OpenAI API for creating and managing vector stores and assistants, as well as executing tools and handling chat operations. It includes methods to create, update, and delete vector stores and assistants, upload files to vector stores, execute tools, and manage chat interactions with a language model.

Key classes and functions:
- `LLM`: A class that initializes a language model client and facilitates prompting with a system message and temperature.
- `get_client()`: Initializes and returns an OpenAI client using a configured API key.
- `delete_vector_store(client, vector_store_id)`: Deletes a specified vector store and prints the status.
- `make_vector_store(client, file_paths)`: Creates a vector store, uploads files, and returns the vector store ID.
- `provide_assistant_files(client, assistant_id, file_paths)`: Associates files with an assistant by creating a vector store and updating the assistant.
- `delete_assistant(client, assistant_id)`: Deletes a specified assistant.
- `create_assistant(client)`: Creates a new assistant with specified instructions, name, tools, and model.
- `execute_tools(client, run)`: Executes tool functions specified in a run's required actions and returns their outputs.
- `submit_tools_and_get_run(client, run, tool_outputs, thread_id)`: Submits tool outputs for a run and polls for completion.
- `get_thread_messages(client, thread)`: Retrieves messages from a specified thread.
- `chat(client, query, model, messages, system_message, temperature)`: Facilitates chat with the language model using specified parameters.

Notable dependencies:
- `openai.OpenAI`: Provides the main interface for interacting with the OpenAI API.
- `importlib`: Used for dynamic importing of tool modules.
- `json`: Utilized for parsing JSON strings into Python objects.
- `src.config.cfg`: Imports configuration settings such as API keys and assistant instructions.
- `src.tools_schema.dev_tools`: Used for specifying development tools when creating assistants."""

from openai import OpenAI
from src.config import cfg
import importlib
import json

def get_client():
	client = OpenAI(
		api_key = cfg.openai_api_key
	)
	return client

def delete_vector_store(client, vector_store_id):
    deleted_vector_store = client.beta.vector_stores.delete(
        vector_store_id=vector_store_id
    )
    if deleted_vector_store.deleted:
        print(f"Deleted vector store {vector_store_id}")
    else:
        print(f"Something went wrong deleting vector store {vector_store_id} and it wasn't deleted.")

def make_vector_store(client, file_paths):
    vector_store = client.beta.vector_stores.create(name="Codebase Resources")
    
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    print(f"Vector store file upload status: {file_batch.status}")
    print(f"Vector store # files: {file_batch.file_counts}")

    return vector_store.id

def provide_assistant_files(client, assistant_id, file_paths):
    v_store = make_vector_store(client, file_paths)
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [v_store]}}
    )
    return assistant.id, v_store

def delete_assistant(client, assistant_id):
	client.beta.assistants.delete(assistant_id)
	print(f"Deleted assistant {assistant_id}")

def create_assistant(client):
	from src.tools_schema import dev_tools

	assistant = client.beta.assistants.create(
		instructions=cfg.ASSISTANT_INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o"
	)

	return assistant.id

def execute_tools(client, run):
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

def submit_tools_and_get_run(client, run, tool_outputs, thread_id):
    try:
        return client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    except Exception as e:
        print("Failed to submit tool outputs:", e)
        return run

def get_thread_messages(client, thread):
    thread_messages = client.beta.threads.messages.list(thread.id)
    return thread_messages.data

def chat(client, query, model="gpt-4o", messages=[], system_message=None, temperature=0.7):
    if system_message:
        messages = [{"role": "developer", "content": system_message}] + messages

    messages = messages + [{"role": "user", "content": query}]
    
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature
    )

    message = completion.choices[0].message

    text = message.content
    refusal = message.refusal
    if refusal is not None:
        print(f"There was a refusal! {str(refusal)}")

    return text


class LLM:
    def __init__(self, system_message, temperature=0.7):
        self.system_message = system_message
        self.temperature = temperature
        self.client = get_client()
    def prompt(self, prompt):
        return chat(self.client, prompt, system_message=self.system_message, temperature=self.temperature)

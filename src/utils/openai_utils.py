"""
Utilities for managing interactions with the OpenAI API, including assistant lifecycle, tool execution, and chat interactions.

This module provides functions to facilitate the integration of OpenAI's capabilities into applications by creating and deleting assistants, executing tools, managing thread messages, and enabling chat interactions with the OpenAI model. It ensures efficient handling of API interactions and tool execution workflows.

Functions:
    - get_client() -> OpenAI: Initializes and returns an OpenAI client using the configured API key.
    - delete_assistant(client: OpenAI, assistant_id: str): Deletes an assistant by its ID.
    - create_assistant(client: OpenAI) -> str: Creates a new assistant with specified instructions and tools, returning its ID.
    - execute_tools(client: OpenAI, run) -> List[Dict]: Executes specified tools and returns their outputs, handling exceptions during execution.
    - submit_tools_and_get_run(client: OpenAI, run, tool_outputs: List[Dict], thread_id: str): Submits tool outputs and polls for run completion, handling submission errors.
    - get_thread_messages(client: OpenAI, thread) -> List[Dict]: Retrieves messages from a specified thread.
    - chat(client: OpenAI, query: str, model: str = "gpt-4o", messages: List[Dict] = [], system_message: str = None, temperature: float = 0.7) -> str: Facilitates chat interactions with the OpenAI model, returning the response text.

Exceptions:
    - General exceptions are caught and logged during tool execution and submission processes to ensure robustness.
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

"""This module provides an interface for interacting with OpenAI's API to manage vector stores, assistants, and chat functionalities. It contains two primary classes:

1. `OpenAIClient`: A client class that wraps various OpenAI API operations, including:
   - Managing vector stores with methods to create, delete, and handle file uploads (`make_vector_store`, `delete_vector_store`).
   - Managing assistants with methods to create, update, and delete assistants (`create_assistant`, `provide_assistant_files`, `delete_assistant`).
   - Executing tool functions dynamically via importlib based on runtime requirements (`execute_tools`).
   - Submitting tool outputs and managing threads (`submit_tools_and_get_run`, `get_thread_messages`).
   - Facilitating chat completions using the OpenAI model (`chat`).

2. `LLM`: A simple wrapper class that uses the `OpenAIClient` to generate responses to prompts by leveraging the chat capabilities of the OpenAI API.

Notable dependencies:
- `importlib` and `json` for dynamic module loading and JSON handling.
- `openai.OpenAI` for API interaction.
- `src.config` for configuration settings, such as the OpenAI API key.
- `src.tools_schema` for defining tool schemas used in assistant creation.

This module is designed to simplify the integration with OpenAI's API for applications that require AI-driven assistants and dynamic execution of tools."""

import importlib
import json
from openai import OpenAI
from src.config import cfg

class OpenAIClient:
	def __init__(self, api_key):
		self.client = OpenAI(api_key=api_key)

	def delete_vector_store(self, vector_store_id):
		try:
			deleted_vector_store = self.client.beta.vector_stores.delete(vector_store_id=vector_store_id)
			if deleted_vector_store.deleted:
				print(f"Deleted vector store {vector_store_id}")
			else:
				print(f"Failed to delete vector store {vector_store_id}")
		except Exception as e:
			print(f"Error deleting vector store: {e}")

	def make_vector_store(self, file_paths):
		try:
			vector_store = self.client.beta.vector_stores.create(name="Codebase Resources")
			with_exit_context = [open(path, "rb") for path in file_paths]
			file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=with_exit_context)
			print(f"Vector store file upload status: {file_batch.status}")
			print(f"Vector store # files: {file_batch.file_counts}")
			return vector_store.id
		except Exception as e:
			print(f"Error creating vector store: {e}")
		finally:
			for file in with_exit_context:
				file.close()

	def provide_assistant_files(self, assistant_id, file_paths):
		v_store = self.make_vector_store(file_paths)
		try:
			assistant = self.client.beta.assistants.update(assistant_id=assistant_id, tool_resources={"file_search": {"vector_store_ids": [v_store]}})
			return assistant.id, v_store
		except Exception as e:
			print(f"Error updating assistant {assistant_id}: {e}")

	def delete_assistant(self, assistant_id):
		try:
			self.client.beta.assistants.delete(assistant_id)
			print(f"Deleted assistant {assistant_id}")
		except Exception as e:
			print(f"Error deleting assistant: {e}")

	def create_assistant(self):
		from src.tools_schema import dev_tools
		try:
			assistant = self.client.beta.assistants.create(
				instructions=cfg.ASSISTANT_INSTRUCTIONS,
				name="Developer of DevAI",
				tools=[{"type": "code_interpreter"}, *dev_tools],
				model="gpt-4o"
			)
			return assistant.id
		except Exception as e:
			print(f"Error creating assistant: {e}")

	def execute_tools(self, run):
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
					tool_outputs.append({"tool_call_id": tool.id, "output": str(output)})  # Convert output to string
				except Exception as e:
					print(f"Error executing {function_name}: {e}")
		return tool_outputs

	def submit_tools_and_get_run(self, run, tool_outputs, thread_id):
		try:
			return self.client.beta.threads.runs.submit_tool_outputs_and_poll(thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs)
		except Exception as e:
			print(f"Failed to submit tool outputs: {e}")
			return run

	def get_thread_messages(self, thread):
		try:
			thread_messages = self.client.beta.threads.messages.list(thread.id)
			return thread_messages.data
		except Exception as e:
			print(f"Error fetching thread messages: {e}")
			return []

	def chat(self, query, model="gpt-4o", messages=[], system_message=None, temperature=0.7):
		if system_message:
			messages = [{"role": "developer", "content": system_message}] + messages

		messages = messages + [{"role": "user", "content": query}]

		completion = self.client.chat.completions.create(model=model, messages=messages, temperature=temperature)

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
		self.client = OpenAIClient(cfg.openai_api_key)

	def prompt(self, prompt):
		return self.client.chat(prompt, system_message=self.system_message, temperature=self.temperature)

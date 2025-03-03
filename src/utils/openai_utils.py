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
		self.output_handler = print
		self.exit_flag = False

	def create_assistant(self, name, assistant_instructions, tools):
		try:
			assistant = self.client.beta.assistants.create(
				instructions=assistant_instructions,
				name=name,
				# tools=[{"type": "code_interpreter"}, *tools],
				tools=[*tools],
				model="gpt-4o"
			)
			return assistant.id
		except Exception as e:
			print(f"Error creating assistant: {e}")

	def create_thread(self):
		thread = self.client.beta.threads.create()
		return thread.id

	def _execute_tools(self, run):
		tool_outputs = []
		if hasattr(run, "required_action"):
			for tool in run.required_action.submit_tool_outputs.tool_calls:
				function_name = tool.function.name
				function_args = tool.function.arguments
				if function_name == 'exit':
					self.exit_flag = True
				self.output_handler(f"{function_name} called...")
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

	def _submit_tools_and_get_run(self, run, tool_outputs, thread_id):
		try:
			return self.client.beta.threads.runs.submit_tool_outputs_and_poll(thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs)
		except Exception as e:
			print(f"Failed to submit tool outputs: {e}")
			return run
	
	def run_thread(self, query, thread_id, assistant_id):
		message = self.client.beta.threads.messages.create(
			thread_id=thread_id,
			role="user",
			content=query,
		)

		run = self.client.beta.threads.runs.create_and_poll(
			thread_id=thread_id,
			assistant_id=assistant_id,
		)

		while run.status == 'requires_action':
			tool_outputs = self._execute_tools(run)
			if tool_outputs:
				run = self._submit_tools_and_get_run(run, tool_outputs, thread_id)
				self.output_handler("Tool outputs submitted successfully.")
			else:
				self.output_handler("No tool outputs to submit.")
				break

	def get_latest_message(self, thread_id):
		try:
			messages = self.get_thread_messages(thread_id)
				
			if not messages:
				print("No messages in thread.")
				return ""

			response = ""
			for message in messages:
				# print("Latest message:", message)
				for c in message.content:
					response += c.text.value + "\n\n"
				break
			return response
		except Exception as e:
			print(f"Error fetching thread messages: {e}")
			return ""

	def get_thread_messages(self, thread_id):
		try:
			thread_messages = self.client.beta.threads.messages.list(thread_id)
			return thread_messages.data
		except Exception as e:
			print(f"Error fetching thread messages: {e}")
			return []

	def delete_assistant(self, assistant_id):
		try:
			self.client.beta.assistants.delete(assistant_id)
			print(f"Deleted assistant {assistant_id}")
		except Exception as e:
			print(f"Error deleting assistant: {e}")

	def delete_thread(self, thread_id):
		try:
			self.client.beta.threads.delete(thread_id)
			print(f"Deleted thread {thread_id}")
		except Exception as e:
			print(f"Error deleting thread: {e}")

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

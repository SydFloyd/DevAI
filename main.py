"""Manage interactive sessions with an AI assistant using OpenAI's API.

This module provides functionality to manage interactive sessions with an AI assistant using OpenAI's API. It includes the ability to set up and tear down sessions, interact with the assistant through user input, and handle the assistant's responses.

Key Classes and Functions:
- `SessionManager`: A class that manages the lifecycle of a session, including setup, interaction, and teardown.
  - `__init__`: Initializes the session with an OpenAI client.
  - `setup`: Sets up the assistant and a thread for interaction, returning a vector store.
  - `interact`: Facilitates continuous interaction with the assistant, handling user queries and assistant responses.
  - `output_messages`: Outputs messages from the assistant, based on the current run status.
  - `teardown`: Cleans up resources by deleting the assistant and vector store.
- `main`: The main function to initiate the session manager and optionally update documentation.

Notable Dependencies/Imports:
- `OpenAIClient`: From `src.utils.openai_utils`, used to interact with OpenAI's API.
- `update_documentation`: From `src.doc.auto_document`, used to update documentation.
- `DocstringUpdater`: From `src.doc.auto_docstring`, used to update docstrings in the codebase.
- `cfg`: From `src.config`, used for configuration settings such as API keys and project paths."""

from src.doc import auto_doc
from src.config import cfg
from src.utils.openai_utils import OpenAIClient

class SessionManager:
	def __init__(self, input_handler=input, output_handler=print):
		self.client = OpenAIClient(api_key=cfg.openai_api_key)
		self.assistant_id = None
		self.thread_id = None
		self.input_handler = input_handler
		self.output_handler = output_handler
	
	def setup(self):
		self.assistant_id = self.client.create_assistant()
		self.assistant_id, vector_store = self.client.provide_assistant_files(self.assistant_id, ["docs.md"])
		thread = self.client.client.beta.threads.create()
		self.thread_id = thread.id
		return vector_store

	def interact(self):
		while True:
			query = self.input_handler(f"\n{cfg.agent_name}>> ")
			if query.strip().lower() in cfg.exit_commands:
				return True
			request = cfg.get_sys_message() + query
			message = self.client.client.beta.threads.messages.create(
				thread_id=self.thread_id,
				role="user",
				content=request,
			)

			run = self.client.client.beta.threads.runs.create_and_poll(
				thread_id=self.thread_id,
				assistant_id=self.assistant_id,
			)

			while run.status == 'requires_action':
				tool_outputs = self.client.execute_tools(run)
				if tool_outputs:
					run = self.client.submit_tools_and_get_run(run, tool_outputs, self.thread_id)
					self.output_handler("Tool outputs submitted successfully.")
				else:
					self.output_handler("No tool outputs to submit.")
					break
			
			self.output_messages(run)
			return False

	def output_messages(self, run):
		if run.status == 'completed':
			messages = self.client.client.beta.threads.messages.list(thread_id=self.thread_id)
			for message in messages:
				self.output_handler(message.role + ":")
				for c in message.content:
					self.output_handler(c.text.value)
				break
		else:
			self.output_handler(run.status)

	def teardown(self, vector_store):
		self.client.delete_assistant(self.assistant_id)
		self.client.delete_vector_store(vector_store)
		self.output_handler("Session ended.\n")


def main():
	update_docs = input("Regenerate documentation? (y/n)")
	if update_docs.lower().strip() == "y":
		auto_doc(cfg.project_root, update_file_docstrings=True)

	manager = SessionManager()
	vector_store = manager.setup()

	try:
		while True:
			exit_interaction = manager.interact()
			if exit_interaction:
				break
	finally:
		manager.teardown(vector_store)


if __name__ == "__main__":
	main()

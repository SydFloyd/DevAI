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

from src.utils.openai_utils import OpenAIClient
from src.tools_schema import dev_tools
from src.doc import auto_doc
from src.config import cfg

SINGLE_AGENT_INSTRUCTIONS = (
	"You are a 10x developer. You value simple elegant solutions.\n"
	"You follow good coding practices.\n"
)

class SessionManager:
	def __init__(self, input_handler=input, output_handler=print):
		self.client = OpenAIClient(api_key=cfg.openai_api_key)
		self.assistant_id = None
		self.thread_id = None
		self.vector_store = None
		self.input_handler = input_handler
		self.output_handler = output_handler
	
	def _setup(self, use_vector_store=False):
		# create assistant
		self.assistant_id = self.client.create_assistant(
			name=cfg.agent_name,
			assistant_instructions=SINGLE_AGENT_INSTRUCTIONS,
			tools=dev_tools
		)

		if use_vector_store:
			assistant_id, vector_store = self.client.provide_assistant_files(self.assistant_id, ["docs.md"])
			self.assistant_id = assistant_id
			self.vector_store = vector_store

		# create Thread
		thread = self.client.client.beta.threads.create()
		self.thread_id = thread.id

	def _interact(self):
		while True:
			query = self.input_handler(f"\n{cfg.agent_name}>> ")
			if query.strip().lower() in cfg.exit_commands:
				return True
			request = cfg.get_sys_message() + query
			self.client.run_thread(request, self.thread_id, self.assistant_id)
			
			response = self.client.get_latest_message(self.thread_id)
			self.output_handler("Response:", response)
			return False
		
	def start_session(self):
		use_vector_store = False
		update_docs = self.input_handler("Regenerate documentation? (y/n)")
		if update_docs.lower().strip() == "y":
			auto_doc(cfg.project_root, update_file_docstrings=True)
			use_vector_store = True
		self._setup(use_vector_store=use_vector_store)

		try:
			while True:
				exit_interaction = self._interact()
				if exit_interaction:
					break
		finally:
			self.teardown()

	def teardown(self, vector_store):
		self.client.delete_assistant(self.assistant_id)
		self.client.delete_thread(self.thread_id)
		if self.vector_store is not None:
			self.client.delete_vector_store(self.vector_store)
		self.output_handler("Session ended.\n")

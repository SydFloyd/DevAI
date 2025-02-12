"""
openai_utils.py

This module handles the utility functions related to OpenAI client interactions. It provides functions to create and manage OpenAI client instances, as well as assistants used in development operations.

Functions:
- get_client(): Initializes and returns an OpenAI client instance configured with the necessary API key.
- create_assistant(): Creates a new assistant instance using specified instructions and tools, beneficial when expanding the toolset for enhanced functionalities.

Dependencies:
- Requires access to the 'cfg' object from 'config' to fetch OpenAI configuration settings.

Example Usage:
To create a new assistant, simply run this module as a script to invoke 'create_assistant' with preset instructions.
"""
from openai import OpenAI
from src.config import cfg

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
	'''New assistant is created whenever toolset is expanded.'''

	from tools_schema import dev_tools

	client = get_client()

	assistant = client.beta.assistants.create(
		instructions=cfg.ASSISTANT_INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)
	print(f"Created assistant {assistant.id}")

	return assistant.id
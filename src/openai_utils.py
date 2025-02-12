"""
openai_utils.py

This module provides utility functions for managing OpenAI client interactions. Functions include client initialization and assistant creation, tailored for development tasks.

Functions:
- get_client(): Sets up and returns an OpenAI client instance using the configured API key.
- delete_assistant(assistant_id): Deletes an assistant instance identified by 'assistant_id'.
- create_assistant(): Creates a new assistant using specified tools and instructions, ideal for task automation.

Dependencies:
Accesses the 'cfg' configuration object to fetch OpenAI-related settings.

Example Usage:
Run as a standalone script to create a new assistant with preset instructions and tool configurations.
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
	from src.tools_schema import dev_tools

	client = get_client()

	assistant = client.beta.assistants.create(
		instructions=cfg.ASSISTANT_INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)
	print(f"Created assistant {assistant.id}")

	return assistant.id

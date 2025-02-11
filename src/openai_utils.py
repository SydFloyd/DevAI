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

def create_assistant():
	'''New assistant is created whenever toolset is expanded.'''

	from tools_schema import dev_tools

	client = get_client()

	INSTRUCTIONS = (
		"You are a senior software developer, a 10x engineer, a f**king wizard. \n"
		"You have access to tools for reading and writing to a codebase. \n"
		"The codebase you are working on is the one through which we are interacting. \n"
		"Reflect on your experience, in terms of what information you can see, and what information would be useful for you to see. \n"
		"You are free to make modifications to the code that make our interaction more smooth. \n"
		"Currently, we've been focusing on making the codebase more readable and scalable for ease of development, then we will expand/refine your toolset."
		"Please let me know how I can help.  I look forward to working together."
	)

	assistant = client.beta.assistants.create(
		instructions=INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)

	print(f"Created assistant {assistant.id}")

if __name__ == "__main__":
	create_assistant()
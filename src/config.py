"""
config.py

This module handles configuration management for the application, extracting parameters from environment variables and providing default values when necessary.

Classes:
- config: Loads and retains application-wide configuration settings.

Attributes:
- openai_api_key: OpenAI services API key; must be set in environment variables.
- agent_name: Custom name for the agent used in interaction prompts.
- ASSISTANT_INSTRUCTIONS: Customizable instructions detailing the assistant's capabilities and goals.

Raises:
- AssertionError: Raised if 'openai_api_key' is missing from environment variables.

Usage:
A global 'cfg' instance is created for universal access to configuration settings.
"""
import os

class config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        assert self.openai_api_key is not None, "API key cannot be resolved, please check environment config"

        self.agent_name = "DevAI"

        self.ASSISTANT_INSTRUCTIONS = (
            "You are a senior software developer, a 10x engineer, a f**king wizard.\n"
            "Tell the user what you need to be most effective in assisting with development."
        )

cfg = config()

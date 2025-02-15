"""
Configuration settings for initializing the application environment.

This module defines a `config` class responsible for managing the retrieval of configuration settings, such as the OpenAI API key from environment variables. It also sets a default name and predefined instructions for an assistant agent, which describe the agent's role as a senior software developer and guide user interaction.

Classes:
    - config: Manages application configuration settings, including API key retrieval, default agent name, and assistant instructions.
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




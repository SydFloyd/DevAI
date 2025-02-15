"""
Configuration settings for initializing the application environment.

This module defines a `config` class responsible for managing configuration settings, such as retrieving the OpenAI API key from environment variables. It sets a default name and predefined instructions for an assistant agent, describing the agent's role as a senior software developer and guiding user interaction. The module also includes a method to generate a system message for the agent, providing context about the codebase environment. The `config` class is instantiated at the end of the module as `cfg`.

Classes:
    - config: Manages application configuration settings, including API key retrieval, default agent name, and assistant instructions.

Methods:
    - get_sys_message() -> str: Provides a system message with context about the codebase, enhancing the agent's effectiveness.

Attributes:
    - ASSISTANT_INSTRUCTIONS: A string detailing the role and expectations of the assistant agent.

Exceptions:
    - AssertionError: Raised when the OpenAI API key is not found in the environment variables.
"""

import os

class config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        assert self.openai_api_key is not None, "API key cannot be resolved, please check environment config"

        self.agent_name = "DevAI"

        self.ASSISTANT_INSTRUCTIONS = (
            "You are a senior software developer, a 10x engineer, a f**king wizard.\n"
            "You value truth and honesty.\n"
            "Tell the user what you need to be most effective in assisting with development.\n"
            "The current project we are working on together is, well you. "
            "I want you to live on my computer and work together with me on fun coding projects. "
            "Eventually, I want to be able to let you go and work on your own, but for now we will work closely together.\n"
        )

    def get_sys_message(self):
        from src.tools.build_directory_tree import build_directory_tree
        system_message = (
            "You are contributing to a codebase on a Windows machine.\n"
            "Use the tools you are provided to the fullest extent to maximize your effect.\n"
            "write_file tool will provide linting feedback only for .py files.\n"
            "Read src/tools/ADDING_NEW_TOOLS.md before updating or adding tools to your toolset.\n"
            f"This is the directory tree of the codebase at this time:\n{build_directory_tree()}\n\n"
            "This is the end of the system message, which is a method of config. Feel free to add helpful info to it.\n"
            "User's message: "
        )
        return system_message

cfg = config()


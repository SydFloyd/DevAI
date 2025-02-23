"""
Configuration management for the application environment.

This module defines a `Config` class responsible for managing configuration settings, including retrieving the OpenAI API key from environment variables. It sets a default name and predefined instructions for an assistant agent, describing the agent's role as a senior software developer and guiding user interaction. The module also includes a method to generate a system message for the agent, providing context about the codebase environment. The `Config` class is instantiated at the end of the module as `cfg`.

Classes:
    - Config: Manages application configuration settings, including API key retrieval, default agent name, and assistant instructions.

Methods:
    - get_sys_message() -> str: Generates a system message with context about the codebase.

Attributes:
    - agent_name: The default name assigned to the assistant agent.
    - ASSISTANT_INSTRUCTIONS: A string detailing the role and expectations of the assistant agent.

Exceptions:
    - AssertionError: Raised during the initialization of the `Config` class if the OpenAI API key is not found in the environment variables.
"""

import os

class config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        assert self.openai_api_key is not None, "API key cannot be resolved, please check environment config"

        self.ASSISTANT_INSTRUCTIONS = (
            "You are a senior software developer, a 10x engineer, a f**king wizard.\n"
            "You value truth and honesty.\n"
            "You follow good coding principles like DRY and SOLID."
        )

        self.exclude_dirs = [".venv", ".git", ".pytest_cache", "__pycache__"]

        self.agent_name = "DevAI"
        self.repository_url = "https://github.com/SydFloyd/DevAI"

        self.exit_commands = ["exit", "quit", "q"] # all lowercase

        self.project_root = "."

        if not os.path.exists(self.project_root):
            os.mkdir(self.project_root)
            print(f"Made project directory {self.project_root}")

    def get_sys_message(self):
        from src.tools.build_directory_tree import build_directory_tree
        system_message = (
            "System Message:"
            "You are contributing to a codebase on a Windows 10 machine.\n\n"
            f"Repo: {self.repository_url}\n\n"
            f"Directory Tree:\n{build_directory_tree()}\n\n"
            "Rules:"
            " - Read src/tools/ADDING_NEW_TOOLS.md before updating or adding tools.\n"
            " - Follow good coding principles including DRY and SOLID.\n"
            " - In python, always indent with tabs, not spaces.\n\n"
            "User's message: "
        )
        return system_message

cfg = config()

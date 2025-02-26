"""Initialize and configure an environment for the DevAI project, ensuring necessary settings and resources are available.

This module imports the `os` library to interact with the environment and filesystem.

Classes:
- `config`: Sets up the configuration for the DevAI project, including API keys, project instructions, directory exclusions, and system messages.

Functions:
- `config.__init__`: Initializes the configuration by obtaining the OpenAI API key from the environment and setting project-specific instructions and parameters. It also ensures the project root directory exists.
- `config.get_sys_message`: Generates a system message that includes repository information, directory structure, and coding rules for contributing to the project.

The `config` class ensures that the necessary environment settings are in place for the DevAI project, and it provides a method to generate system messages that guide developers in adhering to best practices while contributing to the codebase."""

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

        self.exclude_dirs = {".venv", "venv", "node_modules", "__pycache__", ".git", ".idea", ".vscode", ".pytest_cache"}

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







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
            "Read src/tools/ADDING_NEW_TOOLS.md before updating or adding tools to your toolset.\n"
            f"This is the directory tree of the codebase at this time:\n{build_directory_tree()}\n\n"
            "This is the end of the system message, which is a method of config. Feel free to add helpful info to it.\n"
            "User's message: "
        )
        return system_message

cfg = config()




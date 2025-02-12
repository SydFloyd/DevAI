"""
config.py

This module defines the configuration management for the application. It retrieves essential configuration parameters from environment variables and sets defaults where necessary. 

Classes:
- config: A class responsible for loading and holding configuration settings used across the application.

Attributes:
- openai_api_key: API key for authenticating with the OpenAI services, must be available in environment variables.
- active_assistant_id: Identifier for the active assistant used for operations involving assistant capabilities.

Raises:
- AssertionError: If the 'openai_api_key' cannot be retrieved from environment variables.

The 'cfg' instance of the 'config' class is created at the module level for global access to configurations.
"""
import os

class config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        assert self.openai_api_key is not None, "API key cannot be resolved, please check environment config"
        
        self.active_assistant_id = "asst_YnUjykkA0QWoHH5Xj0XrNilD"

        self.agent_name = "DevAI"

cfg = config()
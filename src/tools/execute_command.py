"""
Tool for secure execution of system commands with user consent.

This module provides functionality to execute shell commands within a specified project root directory, ensuring user awareness and approval before execution. It helps prevent unauthorized or accidental command execution by requiring explicit user consent.

Functions:
    - execute_command(command: str, project_root: str = cfg.project_root) -> str: Executes a given shell command in the specified or default project root directory after user approval and returns the result message.

Exceptions:
    - ValueError: Raised when the specified project root is invalid.

Note:
    - Users should exercise caution when approving commands, as executing shell commands can impact system stability and security.
"""

import subprocess
import os
from src.config import cfg

def execute_command(command, project_root = cfg.project_root):
    """
    Execute a command on the machine within the specified project root directory after getting user approval.

    Args:
        command (str): The command to be executed.
        project_root (str): The root directory where the command should be executed.
        
    Returns:
        str: Result message about the execution.
    """

    approval = input(f"Do you approve the execution of this command in '{project_root}'? '{command}' (yes/no): ")
    if approval.strip().lower() not in ['y', 'ye', 'yes']:
        return "Command execution canceled by the user."

    if not os.path.isdir(project_root):
        raise ValueError(f"The specified project root '{project_root}' does not exist or is not a directory.")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=project_root)
        return f"Command executed successfully: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"An error occurred while executing the command: {e.stderr or e}"



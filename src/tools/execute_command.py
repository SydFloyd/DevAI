"""
Tool for executing system commands with user approval.

This module provides a function to execute shell commands on the machine after obtaining explicit user consent. It ensures that users are aware of the commands being executed, thus preventing unauthorized or accidental command execution.

Function:
    - execute_command(command: str) -> str: Executes a given shell command after user approval and returns the result message.

Note:
    - Users should be cautious about the commands they approve, as executing shell commands can affect system stability and security.
"""

import subprocess

def execute_command(command):
    """
    Execute a command on the machine after getting user approval.

    Args:
        command (str): The command to be executed.
        
    Returns:
        str: Result message about the execution.
    """

    approval = input(f"Do you approve the execution of this command? '{command}' (yes/no): ")
    if approval.strip().lower() not in ['y', 'ye', 'yes']:
        return "Command execution canceled by the user."

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return f"Command executed successfully: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"An error occurred while executing the command: {e}"


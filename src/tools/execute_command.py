"""
This module provides a tool to execute a command on the machine after getting user approval.
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
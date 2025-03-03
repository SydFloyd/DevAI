"""'''
This module provides functionality to execute shell commands within a specified project root directory after obtaining user approval.

Key Functions:
- execute_command: Executes a given shell command within a designated project root directory after user confirmation, ensuring the directory exists before execution.

Notable Dependencies:
- subprocess: Used for running shell commands and capturing their outputs.
- os: Utilized for checking the existence and validity of the specified project root directory.
- src.config.cfg: Imports configuration settings, specifically the default project root directory.

Overall Purpose:
The module is designed to facilitate secure execution of shell commands by prompting the user for approval and verifying the project root directory's existence. It is intended for situations where commands need to be executed within a specific directory context, such as project builds or deployments.
'''"""

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
        print("Execute cmd output:", result.stdout)
        return f"Command executed successfully: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"An error occurred while executing the command: {e.stderr or e}"



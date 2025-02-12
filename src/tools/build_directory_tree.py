"""
build_directory_tree.py

This module provides functionality to generate an ASCII representation of a directory structure starting from a specified root directory. The tool is useful for visualizing the hierarchy of files and folders.

Functionality:
- Recursively traverses directories, skipping specified subdirectories, and returns a visual directory tree as a string.

Main Function:
- build_directory_tree(start_path=".", exclude_dirs=None): Constructs and returns the directory tree representation starting from the given path.

Parameters:
- start_path (str, optional): The path at which to start building the directory tree. Defaults to the current directory.
- exclude_dirs (list, optional): Directories to exclude from the tree. Defaults to ['.venv', '.git', '__pycache__'] if not provided.

Returns:
- str: A multi-line string representing the directory tree.

Raises:
- PermissionError: Indicates paths that cannot be accessed due to insufficient permissions with a placeholder in the output.

Example Usage:
Directly call build_directory_tree with desired parameters to get the directory structure as a string.

Note:
The function logs to console when called, which can be removed or modified based on runtime requirements.
"""

from pathlib import Path
import os

def build_directory_tree(start_path=".", exclude_dirs=None):
    print("build_directory_tree function called.")
    if exclude_dirs is None:
        exclude_dirs = [".venv", ".git", "__pycache__"]  # Default to excluding .venv

    lines = []

    # Print the root directory name at the top
    lines.append(start_path.rstrip("/"))

    def _build_tree(current_path, prefix=""):
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError as e:
            # If permission denied, indicate and return
            lines.append(prefix + "\u2514\u2500\u2500 [Permission Denied]")
            return {"error": str(e)}
        
        # Filter out any directories that should be excluded
        filtered_entries = []
        for entry in entries:
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path) and entry in exclude_dirs:
                # Skip excluded directories
                continue
            filtered_entries.append(entry)
        
        for index, entry in enumerate(filtered_entries):
            full_path = os.path.join(current_path, entry)
            
            # Check if this is the last item in the directory to adjust symbols
            is_last_item = (index == len(filtered_entries) - 1)
            branch_symbol = "\u2514\u2500\u2500 " if is_last_item else "\u251c\u2500\u2500 "
            extension_prefix = "    " if is_last_item else "\u2502   "

            lines.append(prefix + branch_symbol + entry)

            # If it's a directory, recurse
            if os.path.isdir(full_path):
                _build_tree(full_path, prefix + extension_prefix)

    _build_tree(start_path)
    return "\n".join(lines)

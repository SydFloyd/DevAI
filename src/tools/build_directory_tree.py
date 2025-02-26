"""Generate a visual representation of a directory tree structure.

This module provides a function to build and return a text-based visual representation of a directory tree. It uses the `os` module for directory traversal and configuration settings from the `src.config` module to determine the root path and directories to exclude from the tree.

Key Functions:
- `build_directory_tree`: Constructs a directory tree starting from a specified root directory. It allows exclusion of specific directories and handles permission errors gracefully.

Notable Dependencies:
- `os`: Provides functions for interacting with the operating system, including directory traversal.
- `src.config`: Contains configuration settings such as the project root and directories to exclude."""

import os
from src.config import cfg

def build_directory_tree(start_path=cfg.project_root, exclude_dirs=cfg.exclude_dirs):
    print("build_directory_tree function called.")

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


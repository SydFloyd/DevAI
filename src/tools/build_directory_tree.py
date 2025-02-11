from pathlib import Path
import os

def build_directory_tree(start_path=".", exclude_dirs=None):
    """
    Recursively builds an ASCII representation of the directory structure 
    starting from `start_path`, returns it as a string.

    :param start_path: Path to the root directory. Defaults to current directory.
    :param exclude_dirs: List of directory names to exclude (e.g. ['.venv']).
                        By default, excludes ['.venv'].
    :return: A string representing the directory tree.
    """
    print("build_directory_tree function called.")
    if exclude_dirs is None:
        exclude_dirs = [".venv", ".git", "__pycache__"]  # Default to excluding .venv

    lines = []

    # Print the root directory name at the top
    lines.append(start_path.rstrip("/"))

    def _build_tree(current_path, prefix=""):
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            # If permission denied, indicate and return
            lines.append(prefix + "└── [Permission Denied]")
            return
        
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
            branch_symbol = "└── " if is_last_item else "├── "
            extension_prefix = "    " if is_last_item else "│   "

            lines.append(prefix + branch_symbol + entry)

            # If it's a directory, recurse
            if os.path.isdir(full_path):
                _build_tree(full_path, prefix + extension_prefix)

    _build_tree(start_path)
    return "\n".join(lines)
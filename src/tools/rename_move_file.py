"""
Utilities for safely renaming and moving files within a project directory.

This module provides a function to rename and move files while ensuring operations are confined within a specified project root directory. It includes comprehensive error handling to prevent operations on non-existent files, directories, or overwriting existing files.

Functions:
    - rename_move_file(source_path: str, destination_path: str, project_root: str = ".") -> dict: Renames and moves a file from the source path to the destination path, ensuring both are within the project root. Returns a dictionary indicating success or containing an error message.

Exceptions:
    - ValueError: Raised when attempting to operate outside the project root.
    - FileNotFoundError: Raised when the source file does not exist.
    - IsADirectoryError: Raised when the source path is a directory instead of a file.
    - FileExistsError: Raised when the destination file already exists.
"""

from pathlib import Path

def rename_move_file(
    source_path: str,
    destination_path: str,
    project_root: str = "."
) -> dict:
    print(f"rename_move_file called from {source_path} to {destination_path}.")

    try:
        root_path = Path(project_root).resolve()
        source = (root_path / source_path).resolve()
        destination = (root_path / destination_path).resolve()

        # Check if paths are within the project root
        if not str(source).startswith(str(root_path)) or not str(destination).startswith(str(root_path)):
            raise ValueError(f"Attempted to operate outside of project root: {source}, {destination}")

        # Ensure the source is a file and exists
        if not source.exists():
            raise FileNotFoundError(f"Source file does not exist: {source}")
        if source.is_dir():
            raise IsADirectoryError(f"Source is a directory, not a file: {source}")

        # Ensure the destination does not already exist to prevent overwriting
        if destination.exists():
            raise FileExistsError(f"Destination file already exists: {destination}")

        # Perform the move/rename operation
        source.rename(destination)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

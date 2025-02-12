"""
delete_file.py

This module provides functionality to delete a specified file within a defined project root. It performs necessary validation to ensure operations are restricted to the project scope.

Functionality:
- Validates and deletes specified files, ensuring they are within the project root and not directories.

Main Function:
- delete_file(file_path: str, project_root: str = "."): Deletes the specified file if it exists within the allowed scope.

Parameters:
- file_path (str): The path to the file that needs to be deleted. It can be relative to the project root.
- project_root (str, optional): The root directory within which the file must exist. Defaults to the current directory.

Raises:
- ValueError: If the resolved file path is outside the project_root.
- FileNotFoundError: If the file does not exist.
- IsADirectoryError: If the specified path points to a directory instead of a file.

Example Usage:
Call delete_file with the relative or absolute file path to delete files within the project root.

Note:
Logs when the function is called, primarily for debugging purposes.
"""

from pathlib import Path

def delete_file(file_path: str, project_root: str = ".") -> None:
    print(f"delete_file function called on {file_path}.")
    root_path = Path(project_root).resolve()
    target_path = (root_path / file_path).resolve()

    # Check if the target path is within the project root
    if not str(target_path).startswith(str(root_path)):
        raise ValueError(f"Attempted to delete file outside of project root: {target_path}")

    # Ensure the target is a file and exists
    if not target_path.exists():
        raise FileNotFoundError(f"No such file or directory: {target_path}")
    if target_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

    # Perform the deletion
    target_path.unlink()

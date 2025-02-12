"""
rename_move_file.py

This module handles renaming or moving files within a defined project boundary, ensuring path validations to maintain project integrity.

Functionality:
- Renames or moves files, performing checks to ensure both sources and destinations are valid and within the project root.

Main Function:
- rename_move_file(source_path: str, destination_path: str, project_root: str = "."): Renames or moves a file to a new location within the project boundaries.

Parameters:
- source_path (str): The file path to be moved or renamed.
- destination_path (str): The new path or name for the file.
- project_root (str, optional): The root directory for validated operations. Defaults to the current directory.

Raises:
- ValueError: If the resolved paths are outside the project_root.
- FileNotFoundError: If the source file does not exist.
- FileExistsError: If the destination file already exists.
- IsADirectoryError: If the source is not a file.

Example Usage:
Use to rename or move files by specifying source and target paths.

Note:
Logs actions to the console for traceable operations.
"""

from pathlib import Path

def rename_move_file(
    source_path: str,
    destination_path: str,
    project_root: str = "."
) -> None:
    print(f"rename_move_file called from {source_path} to {destination_path}.")

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

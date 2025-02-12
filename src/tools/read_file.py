"""
read_file.py

This module offers functionality to read the contents of a file within a specified project root, ensuring all operations respect directory boundaries.

Functionality:
- Reads and returns the content of specified files after confirming they exist and are within the project's scope.

Main Function:
- read_file(file_path: str, project_root: str = "."): Reads and returns contents of a file as a string.

Parameters:
- file_path (str): The path to the file that needs to be read. It can be relative to the project root.
- project_root (str, optional): The root directory where file access is permitted. Defaults to the current directory.

Returns:
- str: The content of the file.

Raises:
- ValueError: If the resolved file path is outside the project_root.
- FileNotFoundError: If the file does not exist.
- IsADirectoryError: If the specified path points to a directory instead of a file.

Example Usage:
Call read_file with the desired file path to access file contents safely.

Note:
Includes basic logging to console when the read operation is called.
"""

from pathlib import Path

def read_file(file_path: str, project_root: str = ".") -> dict:
    print(f"read_file function called on {file_path}.")
    try:
        # Resolve the full, absolute path of both project_root and the target file.
        root_path = Path(project_root).resolve()
        target_path = (root_path / file_path).resolve()

        # Check that target_path is within the project_root (basic sandboxing).
        if not str(target_path).startswith(str(root_path)):
            raise ValueError(f"Attempted to access file outside of project root: {target_path}")

        # Ensure the target is a file and exists.
        if not target_path.exists():
            raise FileNotFoundError(f"No such file or directory: {target_path}")
        if target_path.is_dir():
            raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

        # Read and return the file's contents.
        with open(target_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}

    except Exception as e:
        return {"error": str(e)}

"""
write_file.py

This module defines functions to write content to files safely within designated project boundaries, ensuring directory validations.

Functionality:
- Creates or overwrites files within the specified directory, supporting recursive directory creation.

Main Function:
- write_file(file_path: str, new_content: str, project_root: str = "."): Writes specified content to a file, overwriting if it exists.

Parameters:
- file_path (str): The path where the file is to be written. Can be relative to the project root.
- new_content (str): The content to write to the file.
- project_root (str, optional): The root directory within which writing is permitted. Defaults to the current directory.

Raises:
- ValueError: If the resolved file path is outside the project_root.
- IsADirectoryError: If the specified path points to a directory.

Example Usage:
Directly invoke write_file with the path and content to modify or create files safely.

Note:
Logs the operation, highlighting the number of characters written.
"""

from pathlib import Path

def write_file(file_path: str, new_content: str, project_root: str = ".") -> dict:
    print(f"write_file function called, wrote {len(new_content)} chars to {file_path}.")
    try:
        # Resolve the full, absolute path of both project_root and the target file.
        root_path = Path(project_root).resolve()
        target_path = (root_path / file_path).resolve()

        # Check that target_path is within the project_root (basic sandboxing).
        if not str(target_path).startswith(str(root_path)):
            raise ValueError(f"Attempted to write file outside of project root: {target_path}")

        # If the target path is an existing directory, raise an error.
        if target_path.exists() and target_path.is_dir():
            raise IsADirectoryError(f"Cannot write to a directory: {target_path}")

        # Make sure the parent directory exists; create it if necessary.
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write (overwrite) the file with new_content.
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

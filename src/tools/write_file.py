"""
File management and linting utility for project directories.

This module provides a function to write content to a file within a specified project root directory and subsequently perform linting on the written file using pylint. It ensures files are not written outside the project root and handles errors such as writing to a directory or attempting to write outside the project root.

Function:
    - write_file(file_path: str, new_content: str, project_root: str = ".") -> dict: Writes content to a file and performs linting, returning the linting results or an error message.

Exceptions:
    - ValueError: Raised when attempting to write a file outside the project root.
    - IsADirectoryError: Raised when attempting to write to a directory instead of a file.
"""

from pathlib import Path
import subprocess

def write_file(file_path: str, new_content: str, project_root: str = ".") -> dict:
    print(f"write_file function called, writing {len(new_content)} chars to {file_path}...")
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

        # After writing the file, perform linting
        lint_command = ["pylint", str(target_path)]
        lint_result = subprocess.run(lint_command, capture_output=True, text=True)

        # Return success status and linting results
        return {"success": True, "lint_output": lint_result.stdout, "lint_errors": lint_result.stderr}
    except Exception as e:
        return {"error": str(e)}





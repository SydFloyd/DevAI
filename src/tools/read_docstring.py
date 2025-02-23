"""
Utilities for reading and extracting docstrings from Python files.

This module provides functionality to safely read and extract the module-level docstring from a specified Python file, ensuring the file is within a given project root directory. It handles various exceptions to provide informative error messages, including general exceptions.

Functions:
    - read_docstring(file_path: str, project_root: str = cfg.project_root) -> dict: Extracts the module-level docstring from a Python file.

Exceptions:
    - ValueError: Raised when attempting to access a file outside of the project root.
    - FileNotFoundError: Raised when the specified file does not exist.
    - IsADirectoryError: Raised when the specified path is a directory, not a file.
    - Exception: Catches other unforeseen errors and provides a general error message.
"""

from pathlib import Path
import ast
from src.config import cfg

def read_docstring(file_path: str, project_root: str = cfg.project_root) -> dict:
    print(f"read_docstring function called on {file_path}.")
    
    try:
        # Resolve the full, absolute path of both project_root and the target file.
        root_path = Path(project_root).resolve()
        target_path = (root_path / file_path).resolve()

        # Check that target_path is within the project_root.
        if not str(target_path).startswith(str(root_path)):
            raise ValueError(f"Attempted to access file outside of project root: {target_path}")

        # Ensure the target is a file and exists.
        if not target_path.exists():
            raise FileNotFoundError(f"No such file or directory: {target_path}")
        if target_path.is_dir():
            raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

        # Extract the docstring using the ast module.
        with open(target_path, "r", encoding="utf-8") as f:
            module_ast = ast.parse(f.read(), filename=str(target_path))
        
        # Return the docstring if available.
        return {"docstring": ast.get_docstring(module_ast) or ""}
    except Exception as e:
        return {"error": str(e)}

